p = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\gather\build_tierchar.py'
s = open(p, encoding='utf-8').read()
a = "def outro():"
b = r'''BUST = os.path.join(r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\tier', CLS, 'bust')


def colors_card():
    im = blank()
    ImageDraw.Draw(im).rectangle((0, 0, W, 430), fill=(0, 0, 0, 110))
    y = title(im, 'IN THE FILES  ·  4 COLORS', 210, 44, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
    title(im, 'THE OTHER COLORS', y + 16, 110, fill=COL, spacing=6, glow=GLOWC)
    y = 1560
    y = line(im, 'helm + shoulders exist in 4 colors', y, 46, AMBER)
    line(im, 'the full set: only one color so far', y, 40, GREY)
    return save(im, WORK, 'colors')


def outro():'''
assert a in s and 'def colors_card' not in s
s = s.replace(a, b, 1)
a = "PLAN.append((outro, None,"
b = ("PLAN.append((colors_card, 'bust', 'The game files also hold three more colors for the helm and shoulders. "
     "The full set only exists in one color so far.', 6.0))\nPLAN.append((outro, None,")
assert a in s
s = s.replace(a, b, 1)
a = "    elif kind:\n        parts = []"
b = r'''    elif kind == 'bust':
        cmd += ['-stream_loop', '-1', '-framerate', '30', '-i', os.path.join(BUST, '%04d.png')]
        fc = ('[0:v]setsar=1[b];[2:v]fps=%d,format=rgba,scale=1080:1080[t];[b][t]overlay=0:%d[s];'
              '[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[o];[s][o]overlay=format=auto,format=yuv420p[v]' % (FPS, TOP))
    elif kind:
        parts = []'''
assert a in s
s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(s)
print('patched')
