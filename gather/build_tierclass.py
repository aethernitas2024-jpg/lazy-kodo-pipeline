# -*- coding: utf-8 -*-
"""Short per class: the Hyjal Summit tier set (helm + shoulders, 4 colors) and the helm on every race (WoW Forever beta).

    py -3.11 build_tierclass.py <class>

Assets: forever-casc/tier_pipeline.py -> scratchpad/tier/<class>/ (bust/ 180 frames, h_<race>_<sex>/ 90 frames each)
and scratchpad/tier/r_<class>_v<k>.png (still busts). Client 1.60.1.70245, models helm_<armor>_raid<class>hyjalc60_d_01.
Backdrop: official spec art (Documents/aout/WoWForever/ILLUSTRATIONS-SPECIALISATIONS). Watermark: watermark.py.
"""
import os
import sys

from PIL import Image, ImageDraw

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title
from build_whimsy import line

CLS = sys.argv[1] if len(sys.argv) > 1 else 'warrior'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', 'tier_' + CLS); os.makedirs(WORK, exist_ok=True)
T = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\tier'
SRC = os.path.join(T, CLS)
NAME = {'warrior': 'Warrior', 'paladin': 'Paladin', 'hunter': 'Hunter', 'shaman': 'Shaman', 'rogue': 'Rogue',
        'druid': 'Druid', 'mage': 'Mage', 'priest': 'Priest', 'warlock': 'Warlock'}[CLS]
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - Hyjal tier set %s (EN).mp4' % NAME
COL = {'warrior': (199, 156, 110), 'paladin': (245, 140, 186), 'hunter': (171, 212, 115), 'shaman': (0, 112, 221),
       'rogue': (255, 245, 105), 'druid': (255, 125, 10), 'mage': (105, 204, 240), 'priest': (255, 255, 255),
       'warlock': (148, 130, 201)}[CLS] + (255,)
GLOWC = tuple(int(c * 0.45) for c in COL[:3]) + (255,)
MUSIC = 'hyjal'
GREY = (200, 200, 190, 235)
AMBER = (255, 190, 80, 255)
RACES = [('hu', 'HUMAN'), ('dw', 'DWARF'), ('ni', 'NIGHT ELF'), ('gn', 'GNOME'), ('or', 'ORC'),
         ('sc', 'UNDEAD'), ('ta', 'TAUREN'), ('tr', 'TROLL'), ('be', 'BLOOD ELF')]
TT_Y = 470


def hook():
    im = blank()
    ImageDraw.Draw(im).rectangle((0, 0, W, 470), fill=(0, 0, 0, 120))
    y = title(im, 'WOW FOREVER  ·  HYJAL SUMMIT', 190, 44, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
    y = title(im, '%s TIER SET' % NAME.upper(), y + 14, 120, fill=COL, spacing=6, glow=GLOWC)
    line(im, 'helm + shoulders  ·  4 colors', y + 18, 52, BONE)
    y = TT_Y + 1080 + 20
    y = line(im, 'straight from the beta files', y, 48, AMBER)
    line(im, 'next: the helm on every race', y, 46, SICK)
    return save(im, WORK, 'hook')


def race_card(i, label):
    def fn():
        im = blank()
        ImageDraw.Draw(im).rectangle((0, 0, W, 430), fill=(0, 0, 0, 110))
        y = title(im, '%s HELM  ·  %d / %d' % (NAME.upper(), i + 1, len(RACES)), 210, 44, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
        title(im, label, y + 16, 120, fill=COL, spacing=6, glow=GLOWC)
        d = ImageDraw.Draw(im)
        y = TT_Y + 860
        f = B.font(B.CINZEL, 46, 900)
        for x, t in ((270, 'MALE'), (810, 'FEMALE')):
            d.text((x + 3, y + 3), t, font=f, fill=(0, 0, 0, 220), anchor='ma')
            d.text((x, y), t, font=f, fill=BONE, anchor='ma')
        line(im, 'color %d of 4' % (i % 4 + 1), y + 90, 46, AMBER)
        return save(im, WORK, 'race_%02d' % i)
    return fn


def outro():
    im = blank()
    ImageDraw.Draw(im).rectangle((0, 0, W, H), fill=(0, 0, 0, 130))
    y = title(im, 'WHICH COLOR?', 300, 110, fill=COL, spacing=6, glow=GLOWC)
    sz = 480
    for k in range(4):
        t = Image.open(os.path.join(T, 'r_%s_v%d.png' % (CLS, k))).convert('RGBA').resize((sz, sz), Image.LANCZOS)
        r, c = divmod(k, 2)
        im.alpha_composite(t, (60 + c * sz, y + 30 + r * (sz - 40)))
    y = y + 30 + 2 * (sz - 40) + 40
    y = line(im, 'which color, on which race? tell me', y, 50, BONE)
    y = line(im, 'follow for the other 8 classes', y, 44, SICK)
    line(im, 'beta files  ·  may still change', y, 38, GREY)
    return save(im, WORK, 'outro')


PLAN = [(hook, 'bust', "The %s tier set from WoW Forever's Hyjal Summit raid. Helm and shoulders, in four colors, straight from the beta files." % NAME, 6.0)]
for i, (r, label) in enumerate(RACES):
    PLAN.append((race_card(i, label), r, label.title() + '.', 3.0))
PLAN.append((outro, None, 'Which color do you want, and on which race? Tell me in the comments, and follow for the other classes.', 6.0))


def seg(i, ov, kind, dur):
    out = os.path.join(WORK, 'final_%02d.mp4' % i)
    bg = BP.shot(WORK, i, 'spec_' + CLS, dur, seed=i * 13 + 5, bright=-0.52)
    cmd = [FF, '-v', 'error', '-y', '-i', bg, '-loop', '1', '-framerate', str(FPS), '-t', '%.3f' % dur, '-i', ov]
    if kind == 'bust':
        cmd += ['-stream_loop', '-1', '-framerate', '30', '-i', os.path.join(SRC, 'bust', '%04d.png')]
        fc = ('[0:v]setsar=1[b];[2:v]fps=%d,format=rgba,scale=1080:1080[t];[b][t]overlay=0:%d[s];'
              '[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[o];[s][o]overlay=format=auto,format=yuv420p[v]' % (FPS, TT_Y))
    elif kind:
        for sx in ('m', 'f'):
            cmd += ['-stream_loop', '-1', '-framerate', '30', '-i', os.path.join(SRC, 'h_%s_%s' % (kind, sx), '%04d.png')]
        fc = ('[0:v]setsar=1[b];[2:v]fps=%d,format=rgba,scale=600:600[m];[3:v]fps=%d,format=rgba,scale=600:600[f];'
              '[b][m]overlay=-30:%d[s1];[s1][f]overlay=510:%d[s2];'
              '[1:v]format=rgba,fade=t=in:st=0:d=0.2:alpha=1[o];[s2][o]overlay=format=auto,format=yuv420p[v]' % (FPS, FPS, TT_Y + 220, TT_Y + 220))
    else:
        fc = ('[0:v]setsar=1[b];[1:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1[o];'
              '[b][o]overlay=format=auto,fade=t=out:st=%.3f:d=0.8,format=yuv420p[v]' % (dur - 0.8))
    cmd += ['-filter_complex', fc, '-map', '[v]', '-an', '-t', '%.3f' % dur, '-r', str(FPS),
            '-c:v', 'h264_nvenc', '-preset', 'p7', '-tune', 'hq', '-rc', 'vbr', '-cq', '22', '-b:v', '0', '-maxrate', '13M', '-bufsize', '26M', out]
    run(cmd)
    return out


def main():
    finals, say, tl, t = [], [], [], 0.0
    for i, (fn, kind, text, mind) in enumerate(PLAN):
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        finals.append(seg(i, fn(), kind, dur))
        say.append((t + BP.LEAD, wav)); tl.append((t, dur)); t += dur
    total = t
    lst = os.path.join(WORK, 'list.txt')
    open(lst, 'w').write(''.join("file '%s'\n" % p.replace(os.sep, '/') for p in finals))
    base = os.path.join(WORK, 'base.mp4')
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base])
    audio = BP.mix_audio(WORK, MUSIC, total, say)
    run([FF, '-v', 'error', '-y', '-i', base, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', '%.3f' % total, OUT])
    import watermark
    watermark.apply(OUT, center=(850, 590))   # above the two helms, right side (left helm sits on the default spot)
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
