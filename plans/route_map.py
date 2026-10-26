"""Both continents side by side (Kalimdor left, Eastern Kingdoms right) + zone centre positions in % of that image.

Positions come from UiMapAssignment (zone world rectangle) projected into the continent UiMap rectangle,
so the Forever-only zones (Riverglades, Zephras Isle, Hyjal, Shen'dralas, Darkspear Islands) land where the client puts them.
"""
import csv, json, os, struct
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__))
DB = r'C:\Users\d2460n\Documents\aout\tmp\forever-db2\1.60.1.70338'
F = lambda v: struct.unpack('<f', struct.pack('<I', int(v) & 0xffffffff))[0]
CROP = {'Kalimdor': (330, 20, 700, 668), 'EK': (350, 20, 700, 668)}
CONT = {'1414': 'Kalimdor', '1415': 'EK'}

names = {r['ID']: r['f0s'] for r in csv.DictReader(open(os.path.join(DB, 'UiMap.csv'), encoding='utf-8'))}
parent = {r['ID']: r['f2'] for r in csv.DictReader(open(os.path.join(DB, 'UiMap.csv'), encoding='utf-8'))}
REG = {}
for r in csv.DictReader(open(os.path.join(DB, 'UiMapAssignment.csv'))):
    if r['f5'] == '0' and r['rel'] not in REG:
        REG[r['rel']] = [F(x) for x in json.loads(r['f2'])]


def build(out=os.path.join(S, 'maps', 'World2.png')):
    a = Image.open(os.path.join(S, 'maps', 'Kalimdor.png')).convert('RGBA').crop(CROP['Kalimdor'])
    b = Image.open(os.path.join(S, 'maps', 'EK.png')).convert('RGBA').crop(CROP['EK'])
    im = Image.new('RGBA', (a.width + b.width, max(a.height, b.height)))
    im.paste(a, (0, 0)); im.paste(b, (a.width, 0))
    im.save(out)
    return im.size


W2 = None


def pos(zone):
    """Zone name -> (x%, y%) in World2.png."""
    global W2
    if W2 is None:
        W2 = build()
    zid = next((k for k, v in names.items() if v == zone and k in REG and parent.get(k) in CONT), None)
    if zid is None:
        return None
    cont = CONT[parent[zid]]
    cid = [k for k, v in CONT.items() if v == cont][0]
    x0, y0, _, x1, y1, _ = REG[cid]
    zx0, zy0, _, zx1, zy1, _ = REG[zid]
    cx, cy = (zx0 + zx1) / 2, (zy0 + zy1) / 2
    u, v = (y1 - cy) / (y1 - y0), (x1 - cx) / (x1 - x0)
    px, py = u * 1002, v * 668
    l, t, r, bt = CROP[cont]
    off = 0 if cont == 'Kalimdor' else CROP['Kalimdor'][2] - CROP['Kalimdor'][0]
    return round((px - l + off) / W2[0] * 100, 2), round((py - t) / W2[1] * 100, 2)


if __name__ == '__main__':
    print(build())
    for z in ('Durotar', 'Elwynn Forest', 'Riverglades', 'Mount Hyjal', 'Zephras Isle', "Shen'dralas", 'Teldrassil', 'Silithus', 'Eastern Plaguelands'):
        print(z, pos(z))


def point(zone, mx, my):
    """Map coordinates inside a zone (mx, my in %, as in-game) -> (x%, y%) in World2.png."""
    global W2
    if W2 is None:
        W2 = build()
    zid = next((k for k, v in names.items() if v == zone and k in REG and parent.get(k) in CONT), None)
    if zid is None:
        return None
    cont = CONT[parent[zid]]
    cid = [k for k, v in CONT.items() if v == cont][0]
    x0, y0, _, x1, y1, _ = REG[cid]
    zx0, zy0, _, zx1, zy1, _ = REG[zid]
    wy = zy1 - mx / 100 * (zy1 - zy0)
    wx = zx1 - my / 100 * (zx1 - zx0)
    u, v = (y1 - wy) / (y1 - y0), (x1 - wx) / (x1 - x0)
    px, py = u * 1002, v * 668
    l, t, r, bt = CROP[cont]
    off = 0 if cont == 'Kalimdor' else CROP['Kalimdor'][2] - CROP['Kalimdor'][0]
    return round((px - l + off) / W2[0] * 100, 2), round((py - t) / W2[1] * 100, 2)
