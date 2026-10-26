import sys, struct, re
sys.path.insert(0, r'C:\Users\d2460n\Documents\aout\tmp\forever-casc')
import casc
c = casc.CASC(r'F:\blizz\World of Warcraft', 'e8dd824cf6c3d96cd01f804ca2ea5a63')
r = c.root_lookup(None)
ks = sorted(r)
names = {}
for lf in (r'F:\blizz\wow-export-profile\Default\casc\listfile\listfile-pf-models.dat', r'F:\blizz\wow-export-profile\Default\casc\listfile\listfile-pf-textures.dat'):
    s = open(lf,'rb').read()
    for x in re.finditer(rb'[a-z0-9_/\-\.]+\.(?:blp|m2|wmo|skin|anim)', s):
        names[struct.unpack('>I', s[x.start()-4:x.start()])[0]] = x.group().decode()
mx = max(names)
print('root files', len(ks), 'max fdid', ks[-1], 'listfile max', mx)
hi = [k for k in ks if k > mx]
print('fdids above listfile max:', len(hi), hi[:5], hi[-5:])
