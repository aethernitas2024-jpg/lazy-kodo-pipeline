import sys, collections
sys.path.insert(0, r'C:\Users\d2460n\Documents\aout\tmp\forever-casc')
import casc
WOW = r'F:\blizz\World of Warcraft'
OLD, NEW = '0bf141260c698dfc9cb3b5b7947b78c3', 'e8dd824cf6c3d96cd01f804ca2ea5a63'
names = {}
for line in open(r'C:\Users\d2460n\Documents\aout\tmp\forever-casc\1.60.1.69893\filelist.csv', encoding='utf-8'):
    p = line.split(';')
    if len(p) >= 2: names[int(p[0])] = p[1]
def root(bc):
    c = casc.CASC(WOW, bc)
    r = c.root_lookup(None, locales=(casc.LOCALE_ENUS,))
    return {k: (v.get('enUS') or v.get('all') or next(iter(v.values()))) for k, v in r.items()}
try:
    a = root(OLD)
except Exception as e:
    print('OLD build not readable:', e); sys.exit()
b = root(NEW)
new = [k for k in b if k not in a]; gone = [k for k in a if k not in b]
chg = [k for k in b if k in a and b[k] != a[k]]
print('files old', len(a), 'new', len(b), '| +', len(new), '-', len(gone), '~', len(chg))
def cat(ks):
    c = collections.Counter()
    for k in ks:
        n = names.get(k, '?unknown')
        top = n.split('/')[0].lower() if n != '?unknown' else '?unknown'
        if top in ('interface','dbfilesclient','world','creature','item','character','sound','spells','tileset','textures'):
            top = '/'.join(n.lower().split('/')[:2])
        c[top] += 1
    return c.most_common(25)
print('NEW by folder:', cat(new)); print('CHANGED by folder:', cat(chg)); print('GONE by folder:', cat(gone))
open(r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\rootdiff.txt','w',encoding='utf-8').write(
 '\n'.join(['+ %d %s' % (k, names.get(k,'?')) for k in sorted(new)] + ['~ %d %s' % (k, names.get(k,'?')) for k in sorted(chg)] + ['- %d %s' % (k, names.get(k,'?')) for k in sorted(gone)]))
