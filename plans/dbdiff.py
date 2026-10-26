"""Diff two extracted Forever builds (named CSVs, enUS): per table added/removed/changed rows."""
import csv, sys, os
csv.field_size_limit(10**9)
A, B = sys.argv[1], sys.argv[2]
SHOW = int(sys.argv[3]) if len(sys.argv) > 3 else 15
def load(p):
    with open(p, encoding='utf-8', newline='') as f:
        r = csv.reader(f); h = next(r)
        return h, {row[0]: row for row in r}
for fn in sorted(os.listdir(os.path.join(B, 'named'))):
    if fn.endswith('_frFR.csv'): continue
    pa, pb = os.path.join(A, 'named', fn), os.path.join(B, 'named', fn)
    if not os.path.exists(pa): print('NEW TABLE', fn); continue
    ha, a = load(pa); hb, b = load(pb)
    add = [k for k in b if k not in a]; rem = [k for k in a if k not in b]
    ch = [k for k in b if k in a and a[k] != b[k]]
    if not (add or rem or ch): continue
    print(f'== {fn}: +{len(add)} -{len(rem)} ~{len(ch)}')
    name = next((i for i, c in enumerate(hb) if c in ('Display_lang', 'Name_lang', 'LogTitle_lang', 'MapName_lang', 'AreaName_lang', 'Title_lang')), None)
    for k in add[:SHOW]: print('  +', k, b[k][name] if name is not None else ','.join(b[k][:6])[:120])
    for k in rem[:SHOW]: print('  -', k, a[k][name] if name is not None and name < len(a[k]) else ','.join(a[k][:6])[:120])
    for k in ch[:SHOW]:
        d = [f'{hb[i]}: {a[k][i]!r}->{b[k][i]!r}' for i in range(min(len(hb), len(a[k]), len(b[k]))) if ha[i:i+1] == hb[i:i+1] and a[k][i] != b[k][i]]
        print('  ~', k, (b[k][name] if name is not None else ''), '|', '; '.join(d)[:300])
