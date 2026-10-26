"""Before/after item stats for server-side quality nerfs (blue -> green at the same item level).

Stats  = round(RandPropPoints[ilvl][quality][slot] * StatPercentEditor / 10000)
Weapon = ItemDamage<type>[ilvl][quality] * speed, min/max = avg * (1 -/+ DmgVariance/2)
Armor  = ItemArmorTotal[ilvl][material] * ArmorLocation[invtype][material] * ItemArmorQuality[ilvl][quality]
Old rows: forever-db2/1.60.1.70245/hotfix, new rows: 1.60.1.70291/hotfix. The new values are checked against the
live Wowhead Forever tooltip; make_old() writes a 'before' tooltip JSON (tooltips/<id>_old.json) for tooltip.py.
"""
import csv, json, os, re, struct

DB = r'C:\Users\d2460n\Documents\aout\tmp\forever-db2'
EX = os.path.join(DB, '1.60.1.70334', 'extra')
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.join(HERE, 'tooltips')
F = lambda v: struct.unpack('<f', struct.pack('<I', int(v) & 0xffffffff))[0]


def _rows(t):
    return {r['ID']: r for r in csv.DictReader(open(os.path.join(EX, t + '.csv')))}


RPP = _rows('RandPropPoints')
DMG = {t: _rows(t) for t in ('ItemDamageOneHand', 'ItemDamageTwoHand', 'ItemDamageRanged', 'ItemDamageOneHandCaster', 'ItemDamageTwoHandCaster')}
AQ, AT, AL = _rows('ItemArmorQuality'), _rows('ItemArmorTotal'), _rows('ArmorLocation')
OLD = {r['ID']: r for r in csv.DictReader(open(os.path.join(DB, '1.60.1.70245', 'hotfix', 'hotfix_ItemSparse.csv'), encoding='utf-8', errors='ignore'))}
NEW = {r['ID']: r for r in csv.DictReader(open(os.path.join(DB, '1.60.1.70291', 'hotfix', 'hotfix_ItemSparse.csv'), encoding='utf-8', errors='ignore'))}
ITEM = {r['ID']: r for r in csv.DictReader(open(os.path.join(DB, '1.60.1.70291', 'named', 'Item.csv'), encoding='utf-8'))}
QCOL = {'f7': 4, 'f8': 3, 'f9': 2}
SLOT = {1: 0, 5: 0, 20: 0, 7: 0, 17: 0, 3: 1, 10: 1, 6: 1, 8: 1, 9: 2, 2: 2, 11: 2, 16: 2, 23: 2, 14: 2,
        13: 3, 21: 3, 22: 3, 15: 4, 25: 4, 26: 4, 28: 4}
STATN = {3: 'Agility', 4: 'Strength', 5: 'Intellect', 6: 'Spirit', 7: 'Stamina'}


def rpp(ilvl, q, slot):
    col = {4: 'f7', 3: 'f8', 2: 'f9'}[q]
    return json.loads(RPP[str(ilvl)][col])[slot]


def stats(r, q, inv):
    out = {}
    for i in range(10):
        t = int(r.get('StatModifier_bonusStat_%d' % i) or -1)
        p = int(r.get('StatPercentEditor_%d' % i) or 0)
        if t in (-1, 4294967295) or p == 0:
            continue
        out[t] = int(rpp(int(r['ItemLevel']), q, SLOT.get(inv, 0)) * p / 10000 + 0.5)
    return out


def weapon(r, q, it):
    inv, sub = int(it['InventoryType']), int(it['SubclassID'])
    if inv in (15, 25, 26):
        tab = 'ItemDamageRanged'
    elif inv == 17:
        tab = 'ItemDamageTwoHandCaster' if sub == 10 else 'ItemDamageTwoHand'
    else:
        tab = 'ItemDamageOneHand'
    dps = F(json.loads(DMG[tab][r['ItemLevel']]['f1'])[q])
    spd = int(r['ItemDelay']) / 1000
    var = F(int(r['DmgVariance']))
    avg = dps * spd
    return int(avg * (1 - var / 2)), int(avg * (1 + var / 2) + 0.5), dps, spd


def armor(r, q, it):
    inv, mat = int(it['InventoryType']), int(it['SubclassID'])
    if mat not in (1, 2, 3, 4):
        return None
    tot = F(int(AT[r['ItemLevel']]['f%d' % mat]))
    loc = F(int(AL[str(inv if inv != 20 else 5)]['f%d' % (mat - 1)])) if str(inv) in AL or inv == 20 else 0
    if inv == 16:
        tot, loc = F(int(AT[r['ItemLevel']]['f1'])), F(int(AL['16']['f0'])) if '16' in AL else 0
    qm = F(json.loads(AQ[r['ItemLevel']]['f0'])[q])
    return int(tot * loc * qm + 0.5)


def tooltip_new(i):
    p = os.path.join(TT, '%s.json' % i)
    if not os.path.exists(p):
        import subprocess
        raw = subprocess.run(['curl', '-s', 'https://nether.wowhead.com/forever/tooltip/item/%s' % i], capture_output=True).stdout
        open(p, 'wb').write(raw)
    return json.load(open(p, encoding='utf-8'))


def make_old(i):
    """Returns (old_id_key, report) or raises if the computed new values do not match Wowhead."""
    i = str(i)
    o, n, it = OLD[i], NEW[i], ITEM[i]
    qo, qn, inv = int(o['OverallQualityID']), int(n['OverallQualityID']), int(it['InventoryType'])
    j = tooltip_new(i)
    html = j['tooltip']
    rep = []
    so, sn = stats(o, qo, inv), stats(n, qn, inv)
    if set(so) != set(sn):
        raise ValueError('%s: stat types changed %s -> %s' % (i, sorted(so), sorted(sn)))
    for t, v in sn.items():
        if t in STATN:
            pat = '+%d %s' % (v, STATN[t])
            if pat not in html:
                raise ValueError('%s: %s not in tooltip' % (i, pat))
            if t in so:
                html = html.replace(pat, '+%d %s' % (so[t], STATN[t]), 1)
                rep.append((STATN[t], so[t], v))
        elif t == 45:
            m = re.search(r'effects by up to (?:<[^>]*>)*(\d+)', html)
            if not m or int(m.group(1)) != v:
                raise ValueError('%s: spell power %s vs %s' % (i, m and m.group(1), v))
            if 45 in so:
                html = html[:m.start(1)] + str(so[45]) + html[m.end(1):]
                rep.append(('Spell Power', so[45], v))
    if int(it['ClassID']) == 2:
        mn, mx, dps, spd = weapon(n, qn, it)
        m = re.search(r'(\d+) - (\d+)\s*(?:<[^>]*>\s*)*Damage', html)
        if not m or (int(m.group(1)), int(m.group(2))) != (mn, mx):
            raise ValueError('%s: dmg %s vs %s-%s' % (i, m and m.groups(), mn, mx))
        omn, omx, odps, _ = weapon(o, qo, it)
        html = html.replace(m.group(0), m.group(0).replace('%d - %d' % (mn, mx), '%d - %d' % (omn, omx)), 1)
        html = re.sub(r'\(([\d.]+) damage per second\)', '(%.2f damage per second)' % ((omn + omx) / 2 / spd), html, 1)
        rep.append(('DPS', round((omn + omx) / 2 / spd, 2), round((mn + mx) / 2 / spd, 2)))
    html = html.replace('class="q%d"' % qn, 'class="q%d"' % qo, 1)
    old = dict(j, tooltip=html, quality=qo)
    json.dump(old, open(os.path.join(TT, '%s_old.json' % i), 'w', encoding='utf-8'))
    return '%s_old' % i, rep


if __name__ == '__main__':
    import sys
    for i in sys.argv[1:]:
        try:
            print(i, NEW[i]['Display_lang'], make_old(i)[1])
        except Exception as e:
            print(i, 'SKIP', e)
