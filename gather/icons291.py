"""Item icons pulled from the WoW Forever beta client (read-only CASC), saved as PNG.

    py -3.11 icons.py 2770 2771 2775 ...      -> icons/<itemid>.png
"""
import csv, io, os, sys

sys.path.insert(0, r'C:\Users\d2460n\Documents\aout\tmp\forever-casc')
import casc                                   # noqa: E402
from extract_db2 import beta_build, WOW       # noqa: E402
from PIL import Image                         # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'icons')
ITEM = r'C:\Users\d2460n\Documents\aout\tmp\forever-db2\1.60.1.70291\named\Item.csv'


def blp_to_image(data):
    """Pillow, plus BLP2 encoding 3 (raw BGRA) which Pillow does not read."""
    try:
        return Image.open(io.BytesIO(data)).convert('RGBA')
    except Exception:
        import struct
        if data[:4] != b'BLP2' or data[8] != 3:
            raise
        w, h = struct.unpack_from('<II', data, 12)
        off = struct.unpack_from('<I', data, 20)[0]
        return Image.frombuffer('RGBA', (w, h), data[off:off + w * h * 4], 'raw', 'BGRA', 0, 1).copy()


def icon_fdids(ids):
    want, got = {int(i) for i in ids}, {}
    with open(ITEM, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if int(r['ID']) in want:
                got[int(r['ID'])] = int(r['IconFileDataID'])
    return got


def extract(ids):
    os.makedirs(OUT, exist_ok=True)
    fd = icon_fdids(ids)
    missing = [i for i in ids if int(i) not in fd]
    todo = {i: f for i, f in fd.items() if f and not os.path.exists(os.path.join(OUT, f'{i}.png'))}
    if todo:
        _, bc = beta_build()
        c = casc.CASC(WOW, bc)
        rm = c.root_lookup(set(todo.values()))
        for i, f in todo.items():
            try:
                r = c.read_fdid(f, rm)
                blp_to_image(r.data).save(os.path.join(OUT, f'{i}.png'))
                print(i, f, 'ok')
            except Exception as e:
                print(i, f, 'FAILED', e)
    if missing:
        print('no Item row:', missing)
    return {i: os.path.join(OUT, f'{i}.png') for i in fd}


if __name__ == '__main__':
    extract(sys.argv[1:])
