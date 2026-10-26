# -*- coding: utf-8 -*-
"""Short: Hyjal Summit, the new 20-player raid of WoW Forever, from the game files.

    py -3.11 build_hyjal.py

Every fact comes from the beta client (builds 70009/70058, identical data):
- 13 encounters and the final boss: achievement "Conquerer of the Wilds" (CriteriaTree 230811).
- Abilities: Spell/SpellName descriptions (ids in hyjal_spell_icons.json), icons from SpellMisc.
- Zone: UiMap 2482 "Mount Hyjal" (Hyjal_Camelot tiles + overlays), AreaTable subzones.
- Attunement: CriteriaTree "1.50.0 - Hyjal Attunement Quest - ..." + factions Leyara / Gol'gere.
- Gear: Interface/ICONS/*RaidHyjalc60* (a set per class + weapons); Malleable Essence of Nature.
- Lore hooks: Bloody Parchment ('The Pact' / 'Wild King'), Token of the Wild King.
Size / level (20 players, max level) = BlizzCon, via Warcraft Tavern. Boss order = achievement order.
"""
import json, os
from PIL import Image, ImageDraw

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title, icon, pill
from build_whimsy import line, map_card
import build_cozy as C

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', 'hyjal'); os.makedirs(WORK, exist_ok=True)
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - Hyjal Summit raid, every boss (EN).mp4'
NATURE = (140, 220, 120, 255)
MOON = (170, 190, 255, 255)
GREY = (200, 200, 190, 235)
EPIC = (163, 53, 238, 255)
# Hyjal-video data: lost in the 14/10/2026 Temp purge, only needed to rebuild that video itself.
_sp, _gear = os.path.join(HERE, 'hyjal_spell_icons.json'), os.path.join(HERE, 'hyjal_gear.txt')
SP = {k: v[1] for k, v in json.load(open(_sp)).items()} if os.path.exists(_sp) else {}
GEAR = {l.split(';')[1].strip(): int(l.split(';')[0]) for l in open(_gear)} if os.path.exists(_gear) else {}
HELMS = [GEAR[k] for k in GEAR if k.startswith('INV_Helm')]
WEAPONS = [GEAR[k] for k in GEAR if any(k.startswith('INV_' + w) for w in
           ('Sword', 'Staff', 'Bow', 'Axe', 'Mace', 'PoleArm', 'Wand', 'Shield', 'Knife', 'Hand'))]


def fd(f):
    return f'fd{f}'


def icon_row(im, fds, y, size=120, gap=26):
    tot = len(fds) * (size + 12) + (len(fds) - 1) * gap
    x = (W - tot) // 2
    for f in fds:
        im.alpha_composite(icon(fd(f), size, border=(200, 180, 120, 255)), (x - 24, y - 24))
        x += size + 12 + gap
    return y + size + 12


def head(im, kicker, big, col=BONE, y=170, glow=(60, 140, 60, 255), size=110):
    y = title(im, kicker, y, 44, fill=GOLD, spacing=14, glow=(0, 0, 0, 0))
    return title(im, big, y + 14, size, fill=col, spacing=6, glow=glow)


def abilities(im, rows, y):
    """rows: (icon fdid, ability name, one-line effect)."""
    for f, nm, fx in rows:
        im.alpha_composite(icon(fd(f), 104, border=(200, 180, 120, 255)), (70 - 24, y - 24))
        d = ImageDraw.Draw(im)
        x = 70 + 104 + 12 + 30
        d.text((x, y + 4), nm.upper(), font=B.fit(B.CINZEL, nm.upper(), 1030 - x, 40, 800), fill=GOLD)
        fb = B.fit(B.GEORGIA_I, fx, 1035 - x, 46)
        d.text((x + 3, y + 57), fx, font=fb, fill=(0, 0, 0, 230))
        d.text((x, y + 54), fx, font=fb, fill=BONE)
        y += 150
    return y


def boss_png(name, kicker, big, col, rows, quote=None, glow=(60, 140, 60, 255), size=104):
    im = blank()
    B.backdrop(im, 900, 760, 820, 175)
    y = head(im, kicker, big, col, glow=glow, size=size)
    y = abilities(im, rows, y + 60)
    if quote:
        f = B.fit(B.GEORGIA_I, quote, 980, 44)
        ImageDraw.Draw(im).text((W / 2, y + 20), quote, font=f, fill=MOON, anchor='ma')
    return save(im, WORK, name)


# ------------------------------------------------------------------ cards

def hook_png():
    im = blank()
    B.backdrop(im, 760, 740, 640, 175)
    y = title(im, 'NEW 20-PLAYER RAID', 300, 60, fill=GOLD, spacing=12, glow=(0, 0, 0, 0))
    y = title(im, 'HYJAL', y + 20, 220, fill=NATURE, spacing=14, glow=(60, 160, 60, 255))
    y = title(im, 'SUMMIT', y + 6, 150, fill=BONE, spacing=14, glow=(60, 160, 60, 255))
    y = icon_row(im, [SP['Royal Defiance'], HELMS[3], SP['Starfall'], HELMS[5]], y + 70, 130)
    line(im, 'all 13 bosses, found in the WoW Forever files', y + 40, 50, SICK)
    return save(im, WORK, 'hook')


def zone_png():
    im = blank()
    B.backdrop(im, 900, 760, 760, 175)
    y = head(im, '20 PLAYERS  ·  MAX LEVEL', 'MOUNT HYJAL')
    m = C.zmap('Hyjal', [], 1000)
    y = map_card(im, m, y + 50)
    y = line(im, 'a brand-new zone with 9 areas', y + 30, 50, BONE)
    line(im, 'Nordrassil, the World Tree, at the Summit of Eternity', y + 4, 42, NATURE)
    return save(im, WORK, 'zone')


def attune_png():
    im = blank()
    B.backdrop(im, 900, 740, 600, 175)
    y = head(im, 'BEFORE THE RAID', 'ATTUNEMENT')
    y = pill(im, '3 opening quests', y + 70, B.GEORGIA_I, 52, BONE, h=96)
    y = pill(im, 'Distilled Demonic Essence', y + 30, B.GEORGIA_I, 52, BONE, h=96)
    y = pill(im, "final step: defeat Gol'gere and Leyara", y + 30, B.GEORGIA_I, 52, GOLD, h=96)
    line(im, 'new faction: Guardians of Hyjal (Cenarion Circle offshoot)', y + 60, 40, NATURE)
    return save(im, WORK, 'attune')


BOSSES = ['Bandalar', 'Ancient of Decay', 'Time-Lost Battalion', 'Sylvestris Dusksong', 'Old Gloomlurker',
          'Gharalis the Abyssal', 'Kathris the Haunted', 'Anara Chillwind', 'Elder Minderel', 'Tracker Stillwind',
          'Council of Thorns', 'Nythus the Dreambound', 'The Wild King']


def list_png():
    im = blank()
    B.backdrop(im, 960, 760, 860, 175)
    y = head(im, 'CONQUEROR OF THE WILDS', '13 BOSSES', size=120)
    y += 40
    d = ImageDraw.Draw(im)
    for i, n in enumerate(BOSSES, 1):
        last = n == 'The Wild King'
        f = B.fit(B.CINZEL, n.upper(), 780, 54 if last else 46, 900 if last else 700)
        d.text((190, y), f'{i:>2}', font=B.font(B.CINZEL, 40, 700), fill=GREY, anchor='ra')
        d.text((230 + 3, y + 3), n.upper(), font=f, fill=(0, 0, 0, 230))
        d.text((230, y), n.upper(), font=f, fill=NATURE if last else BONE)
        y += 70 if not last else 80
    line(im, 'achievement order  ·  the Wild King is the final boss', y + 10, 38, GREY)
    return save(im, WORK, 'list')


def anara_png():
    return boss_png('anara', 'PRIESTESS OF ELUNE', 'ANARA CHILLWIND', MOON, [
        (SP['Lunar Fire'], 'Lunar Fire', 'arcane burn that explodes on the group'),
        (SP['Umbral Fire'], 'Umbral Fire', 'the same, in shadow: "the rage of Elune"'),
        (SP['Starfall'], 'Starfall', 'stars crash down on random players')], glow=(80, 90, 200, 255))


def duo_png():
    return boss_png('duo', 'TWO BOSSES, ONE HEALTH BAR', 'SYLVESTRIS & STORMWRAITH', MOON, [
        (SP['Everlasting Bond'], 'Everlasting Bond', 'Sylvestris and Stormwraith share health'),
        (SP["Elune's Grace"], "Elune's Grace", 'Elune shields one of them at a time'),
        (SP['Ricochet'], 'Ricochet', 'arrows that bounce between players'),
        (SP['Stormcharged'], 'Stormcharged', "charges Nordrassil's branch with the storm")],
        glow=(80, 90, 200, 255), size=78)


def nythus_png():
    return boss_png('nythus', 'THE EMERALD DREAM', 'NYTHUS', NATURE, [
        (SP['Dreamfall'], 'Dreamfall', 'throws the Emerald Dream into turmoil'),
        (SP['Unstable Dream'], 'Unstable Dream', 'more mana and haste, but everyone takes more'),
        (SP['Emerald Stasis'], 'Emerald Stasis', 'players commune with the Dream to subdue him'),
        (SP['Dreamless Waking'], 'Dreamless Waking', 'woken up: stunned and vulnerable')])


def kathris_png():
    return boss_png('kathris', 'SOULS & THE AFTERLIFE', 'KATHRIS', (210, 170, 255, 255), [
        (SP['Soul Rip'], 'Soul Rip', 'your soul fractures, then you are stunned'),
        (SP['Soul Tether'], 'Soul Tether', 'fragmented souls are pulled to Kathris'),
        (SP['Aura of Fear'], 'Aura of Fear', 'fear')],
        quote='"You have looked into the afterlife and Kathris looked back."', glow=(120, 60, 180, 255))


def trio_png():
    return boss_png('trio', 'MORE BOSSES', 'DECAY, ICE & THE DEEP', BONE, [
        (SP['Rotting Spit'], 'Gharalis the Abyssal', 'acid spit, and a body that rots mid-fight'),
        (SP['Minderel freeze'], 'Elder Minderel', 'freeze him in ice, he becomes weak to fire'),
        (SP['Gloomlurker heal'], 'Old Gloomlurker', 'something heals while he is near'),
        (SP['Charged Shot'], 'Tracker Stillwind', 'drops the Stillwind String')], size=92)


def names_png():
    im = blank()
    B.backdrop(im, 900, 740, 560, 175)
    y = head(im, 'NAMES ONLY  ·  FOR NOW', 'STILL HIDDEN', size=110)
    y += 50
    for n in ('Bandalar', 'Ancient of Decay', 'Time-Lost Battalion', 'Council of Thorns'):
        y = pill(im, n, y + 22, B.CINZEL, 50, BONE, bg=(20, 40, 20, 235), outline=NATURE, h=92)
    line(im, 'no abilities in the files yet', y + 50, 42, GREY)
    return save(im, WORK, 'names')


def king1_png():
    return boss_png('king1', 'FINAL BOSS', 'THE WILD KING', NATURE, [
        (SP['Royal Defiance'], 'Royal Defiance', 'draws on the power of Nordrassil'),
        (SP['Convoke the Spirits'], 'Convoke the Spirits', 'wild spirits hunt players and explode'),
        (SP['Assimilation'], 'Assimilation', 'pools that drain your health to heal him'),
        (SP['Dreadful Screech'], 'Dreadful Screech', 'the whole raid runs in fear')], size=120,
        glow=(60, 180, 60, 255))


def king2_png():
    im = blank()
    B.backdrop(im, 900, 760, 700, 175)
    y = head(im, 'LAST PHASE', 'WILD FORM', NATURE, size=150, glow=(60, 180, 60, 255))
    y = icon_row(im, [SP['Wild Form']], y + 60, 170)
    for txt, col in (('"Overwhelmed by his own powers,', BONE), ('the Wild King assumes a horrific new form,', BONE),
                     ('granting access to the abilities', NATURE), ('of several Wild Gods."', NATURE)):
        y = line(im, txt, y + 10, 50, col) - 4
    y = line(im, "a level-30 letter already mentions 'The Pact' and a 'Wild King'", y + 40, 38, GOLD)
    return save(im, WORK, 'king2')


def loot_png():
    im = blank()
    B.backdrop(im, 900, 760, 720, 175)
    y = head(im, 'THE LOOT', 'A SET FOR EVERY CLASS', EPIC, size=84, glow=(120, 40, 170, 255))
    y = icon_row(im, HELMS[:5], y + 70, 118, 22)
    y = icon_row(im, HELMS[5:], y + 40, 118, 22)
    y = icon_row(im, WEAPONS[:6], y + 50, 100, 20)
    y = line(im, '9 class armor sets + weapons (icons in the files)', y + 40, 44, BONE)
    line(im, 'disenchants into Malleable Essence of Nature', y + 4, 40, NATURE)
    return save(im, WORK, 'loot')


def outro_png():
    im = blank()
    B.backdrop(im, 800, 660, 460, 175)
    y = title(im, 'LIKE + FOLLOW', 640, 96)
    y = line(im, 'more WoW Forever guides every week', y + 40, 54, SICK)
    line(im, 'from the beta files  ·  may still change', y + 20, 40, GREY)
    return save(im, WORK, 'outro')


PLAN = [
    (hook_png, 'hyjalmap', "WoW Forever's new raid, Hyjal Summit, is already in the game files. Here are all thirteen bosses.", 4.0),
    (zone_png, 'kalimdor', 'It is a twenty player raid at max level, on a brand new zone: Mount Hyjal, '
                           'with Nordrassil, the World Tree, at the Summit of Eternity.', 5.0),
    (attune_png, 'hyjalmap', "To get in, there is an attunement quest. It ends with a fight against Gol'gere and Leyara.", 5.0),
    (list_png, 'kalimdor', 'Thirteen encounters. Here is what the files reveal about them.', 6.0),
    (anara_png, 'hyjalmap', 'Anara Chillwind, a priestess of Elune: lunar and umbral fire, and stars falling on the raid.', 5.0),
    (duo_png, 'kalimdor', 'Sylvestris Dusksong and Stormwraith share one health bar, while Elune shields one of them at a time.', 5.0),
    (nythus_png, 'hyjalmap', 'Nythus the Dreambound is tied to the Emerald Dream. You have to commune with the Dream to subdue him, '
                             'and wake him up to make him vulnerable.', 5.0),
    (kathris_png, 'kalimdor', 'Kathris the Haunted fractures your soul. You have looked into the afterlife, and Kathris looked back.', 5.0),
    (trio_png, 'hyjalmap', 'Gharalis rots mid fight. Elder Minderel can be frozen in ice, making him weak to fire. '
                           'And something heals Old Gloomlurker while he is near.', 5.0),
    (names_png, 'kalimdor', 'Four encounters are still just names: Bandalar, the Ancient of Decay, '
                            'the Time-Lost Battalion, and the Council of Thorns.', 5.0),
    (king1_png, 'hyjalmap', 'And the final boss, the Wild King. He draws on the power of Nordrassil, '
                            'summons wild spirits, and drains your health to heal himself.', 5.0),
    (king2_png, 'kalimdor', 'In his last phase, he takes a horrific new form, with the powers of several Wild Gods. '
                            'A letter you find at level thirty already mentions him, and a mysterious Pact.', 6.0),
    (loot_png, 'hyjalmap', 'The loot: a full armor set for every class, and new weapons, already in the files.', 5.0),
    (outro_png, 'kalimdor', 'Like and follow for more WoW Forever news.', 3.5),
]


def main():
    files, tl, say, t = [], [], [], 0.0
    for i, (fn, art, text, mind) in enumerate(PLAN):
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        files.append(BP.shot(WORK, i, art, dur, seed=i * 19 + 7, bright=0.0 if i == 0 else -0.10))
        say.append((t + BP.LEAD, wav)); tl.append((t, dur)); t += dur
    total = t

    frame = BP.frame_png(WORK)
    finals = []
    for i, (fn, *_ ) in enumerate(PLAN):
        a, d = tl[i]
        card = fn()
        fi, fo = (0.0, 0.15) if i == 0 else ((0.35, 0.0) if i == len(PLAN) - 1 else (0.25, 0.16))
        ch = '[2:v]format=rgba'
        if fi: ch += f',fade=t=in:st=0.1:d={fi}:alpha=1'
        if fo: ch += f',fade=t=out:st={max(0, d - fo):.3f}:d={fo}:alpha=1'
        tail = f',fade=t=out:st={d - 0.8:.3f}:d=0.8' if i == len(PLAN) - 1 else ''
        out = os.path.join(WORK, f'final_{i:02d}.mp4')
        run([FF, '-v', 'error', '-y', '-i', files[i],
             '-loop', '1', '-framerate', str(FPS), '-t', f'{d:.3f}', '-i', frame,
             '-loop', '1', '-framerate', str(FPS), '-t', f'{d:.3f}', '-i', card,
             '-filter_complex', f'[0:v]setsar=1[b];[1:v]format=rgba[f];[b][f]overlay=format=auto[bf];{ch}[c];'
                                f'[bf][c]overlay=format=auto{tail},format=yuv420p,setsar=1[v]',
             '-map', '[v]', '-an', '-t', f'{d:.3f}', '-r', str(FPS),
             '-c:v', 'h264_nvenc', '-preset', 'p7', '-tune', 'hq', '-rc', 'vbr', '-cq', '22', '-b:v', '0',
             '-maxrate', '13M', '-bufsize', '26M', out])
        finals.append(out)

    lst = os.path.join(WORK, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p.replace(os.sep, '/')}'\n" for p in finals))
    base = os.path.join(WORK, 'base.mp4')
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base])
    audio = BP.mix_audio(WORK, 'hyjal', total, say)
    run([FF, '-v', 'error', '-y', '-i', base, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', f'{total:.3f}', OUT])
    for i, (a, d) in enumerate(tl):
        print(f'{i} {a:6.2f} +{d:5.2f}')
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
