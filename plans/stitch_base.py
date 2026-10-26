import re, sys
sys.path.insert(0, r'C:\Users\d2460n\Documents\aout\tmp\forever-casc')
sys.path.insert(0, r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\gather')
import casc
from extract_db2 import beta_build, WOW
from icons import blp_to_image
from PIL import Image
folder, prefix, out = sys.argv[1:4]
base = {}
for line in open(r'C:\Users\d2460n\Documents\aout\tmp\forever-casc\1.60.1.69893\filelist.csv', encoding='utf-8'):
    i, p, _ = line.rstrip('\n').split(';')
    m = re.fullmatch(r'interface/worldmap/%s/%s(\d+)\.blp' % (folder.lower(), prefix.lower()), p.lower())
    if m: base[int(m.group(1))] = int(i)
_, bc = beta_build(); c = casc.CASC(WOW, bc)
rm = c.root_lookup(set(base.values()))
im = Image.new('RGBA', (1024, 768))
for n, f in base.items():
    im.paste(blp_to_image(c.read_fdid(f, rm).data), (((n - 1) % 4) * 256, ((n - 1) // 4) * 256))
im.crop((0, 0, 1002, 668)).save(out); print(len(base), 'tiles')
