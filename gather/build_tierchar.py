# -*- coding: utf-8 -*-
"""Short per class: the full Hyjal tier set worn by every race (male + female), WoW Forever beta.

    py -3.11 build_tierchar.py <class> "<set name>"

Characters: wow.export 0.2.19 saved characters (race/model + set item IDs from ItemSet.db2) -> glTF export ->
forever-casc/fix_attach.py (helm/shoulders on the M2 attachment points) -> forever-casc/blender_char.py (90-frame turntable)
in scratchpad/chars/<class>/<race>_<sex>/. Backdrop: official spec art. Watermark: watermark.py.
"""
import os
import sys

from PIL import Image, ImageDraw

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title
from build_whimsy import line

CLS = sys.argv[1] if len(sys.argv) > 1 else 'warrior'
SETNAME = sys.argv[2] if len(sys.argv) > 2 else ''
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', 'tierchar_' + CLS); os.makedirs(WORK, exist_ok=True)
SRC = os.path.join(r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\chars', CLS)
NAME = CLS.title()
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - %s tier set on every race (EN).mp4' % NAME
COL = {'warrior': (199, 156, 110), 'paladin': (245, 140, 186), 'hunter': (171, 212, 115), 'shaman': (0, 112, 221),
       'rogue': (255, 245, 105), 'druid': (255, 125, 10), 'mage': (105, 204, 240), 'priest': (255, 255, 255),
       'warlock': (148, 130, 201)}[CLS] + (255,)
GLOWC = tuple(int(c * 0.45) for c in COL[:3]) + (255,)
MUSIC = 'hyjal'
GREY = (200, 200, 190, 235)
AMBER = (255, 190, 80, 255)
ALL = [('human', 'HUMAN'), ('dwarf', 'DWARF'), ('nightelf', 'NIGHT ELF'), ('gnome', 'GNOME'), ('orc', 'ORC'),
       ('scourge', 'UNDEAD'), ('tauren', 'TAUREN'), ('troll', 'TROLL'), ('skyborne', 'SKYBORNE')]
# playable combos in WoW Forever: client CharBaseInfo.db2 (1.60.1.70245); NEW = not possible in original Classic
PLAYABLE = {'warrior': 'human orc dwarf nightelf tauren scourge gnome troll skyborne', 'paladin': 'human dwarf scourge',
            'hunter': 'orc dwarf nightelf tauren troll human skyborne', 'shaman': 'orc tauren troll dwarf skyborne',
            'rogue': 'human orc nightelf scourge dwarf gnome troll skyborne', 'druid': 'nightelf tauren skyborne',
            'mage': 'human scourge gnome troll orc skyborne', 'priest': 'human dwarf scourge nightelf troll gnome',
            'warlock': 'human orc scourge gnome troll'}[CLS].split()
NEW = {'paladin': ['scourge'], 'hunter': ['human'], 'shaman': ['dwarf'], 'mage': ['orc'], 'priest': ['gnome'],
       'warlock': ['troll']}.get(CLS, []) + ['skyborne']
RACES = [(r, l) for r, l in ALL if r in PLAYABLE]
TOP = 470          # characters area: y 470 .. 1470


def crop_box(seq):
    """Union of the alpha bounding boxes over a few frames of a turntable."""
    box = None
    names = sorted(os.listdir(seq))
    for f in names[::max(1, len(names) // 8)]:
        b = Image.open(os.path.join(seq, f)).getchannel('A').getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    return box


def fit(seq, bw, bh):
    """ffmpeg filter to crop a turntable to its content and fit it in bw x bh (keeps aspect)."""
    x0, y0, x1, y1 = crop_box(seq)
    w, h = x1 - x0, y1 - y0
    s = min(bw / w, bh / h)
    ow, oh = int(w * s) // 2 * 2, int(h * s) // 2 * 2
    return 'crop=%d:%d:%d:%d,scale=%d:%d' % (w, h, x0, y0, ow, oh), ow, oh


def hook():
    im = blank()
    ImageDraw.Draw(im).rectangle((0, 0, W, 470), fill=(0, 0, 0, 120))
    y = title(im, 'WOW FOREVER  ·  HYJAL SUMMIT', 170, 44, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
    y = title(im, '%s TIER SET' % NAME.upper(), y + 12, 120, fill=COL, spacing=6, glow=GLOWC)
    if SETNAME:
        y = line(im, SETNAME, y + 14, 56, BONE)
    y = 1560
    y = line(im, 'the full set, on every playable race', y, 50, AMBER)
    line(im, 'straight from the beta files', y, 42, SICK)
    return save(im, WORK, 'hook')


def race_card(i, label, mode='pair'):
    def fn():
        im = blank()
        ImageDraw.Draw(im).rectangle((0, 0, W, 430), fill=(0, 0, 0, 110))
        y = title(im, '%s SET  ·  %d / %d' % (NAME.upper(), i + 1, len(RACES)), 210, 44, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
        y = title(im, label, y + 16, 120, fill=COL, spacing=6, glow=GLOWC)
        if RACES[i][0] in NEW:
            from build_prof import pill
            pill(im, 'NEW IN FOREVER', y + 20, B.CINZEL, 40, (255, 210, 90, 255), h=72)
        d = ImageDraw.Draw(im)
        f = B.font(B.CINZEL, 44, 900)
        labels = ((270, 'MALE'), (810, 'FEMALE')) if mode == 'pair' else ((540, mode.upper()),)
        for x, t in labels:
            d.text((x + 3, 1503), t, font=f, fill=(0, 0, 0, 220), anchor='ma')
            d.text((x, 1500), t, font=f, fill=BONE, anchor='ma')
        return save(im, WORK, 'race_%02d_%s' % (i, mode))
    return fn


BUST = os.path.join(r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\tier', CLS, 'bust')


def colors_card():
    im = blank()
    ImageDraw.Draw(im).rectangle((0, 0, W, 430), fill=(0, 0, 0, 110))
    y = title(im, 'IN THE FILES  ·  4 COLORS', 210, 44, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
    title(im, 'THE OTHER COLORS', y + 16, 110, fill=COL, spacing=6, glow=GLOWC)
    y = 1560
    y = line(im, 'helm + shoulders exist in 4 colors', y, 46, AMBER)
    line(im, 'the full set: only one color so far', y, 40, GREY)
    return save(im, WORK, 'colors')


def outro():
    im = blank()
    ImageDraw.Draw(im).rectangle((0, 0, W, H), fill=(0, 0, 0, 140))
    y = title(im, 'WHICH RACE WEARS IT BEST?', 260, 70, fill=COL, spacing=4, glow=GLOWC)
    n = 2 * len(RACES)
    cols = 6 if n > 15 else 5
    rows = (n + cols - 1) // cols
    cw, ch = (1000 // cols), 250
    k = 0
    for r, _ in RACES:
        for sx in ('male', 'female'):
            seq = os.path.join(SRC, '%s_%s' % (r, sx))
            fr = Image.open(os.path.join(seq, '0001.png')).convert('RGBA').crop(crop_box(seq))
            s = min(cw / fr.width, ch / fr.height)
            fr = fr.resize((int(fr.width * s), int(fr.height * s)), Image.LANCZOS)
            row, col = divmod(k, cols)
            im.alpha_composite(fr, (40 + col * cw + (cw - fr.width) // 2, y + 30 + row * (ch + 10) + ch - fr.height))
            k += 1
    y = y + 30 + rows * (ch + 10) + 40
    y = line(im, 'tell me in the comments', y, 50, BONE)
    y = line(im, 'follow for the other 8 classes', y, 44, SICK)
    line(im, 'beta files  ·  may still change', y, 38, GREY)
    return save(im, WORK, 'outro')


PLAN = [(hook, 'hook', "The %s tier set from WoW Forever's Hyjal Summit raid%s. Here it is on every playable race." %
         (NAME, (', ' + SETNAME) if SETNAME else ''), 9.0)]
SOLO = len(RACES) <= 4
NSEG = len(RACES) * (3 if SOLO else 1)
SEGDUR = max(5.0, (63.0 - 9.0 - 9.0 - 6.5) / NSEG)
for i, (r, label) in enumerate(RACES):
    say = label.title() + ('. New in Forever!' if r in NEW else '.')
    if SOLO:
        PLAN.append((race_card(i, label, 'male'), r + '|male', say, SEGDUR))
        PLAN.append((race_card(i, label, 'female'), r + '|female', '', SEGDUR))
        PLAN.append((race_card(i, label), r, '', SEGDUR))
    else:
        PLAN.append((race_card(i, label), r, say, SEGDUR))
PLAN.append((colors_card, 'bust', 'The game files also hold three more colors for the helm and shoulders. The full set only exists in one color so far.', 9.0))
PLAN.append((outro, None, 'Which race wears it best? Tell me in the comments, and follow for the other classes.', 6.5))


def seg(i, ov, kind, dur):
    out = os.path.join(WORK, 'final_%02d.mp4' % i)
    bg = BP.shot(WORK, i, 'spec_' + CLS, dur, seed=i * 13 + 5, bright=-0.52)
    cmd = [FF, '-v', 'error', '-y', '-i', bg, '-loop', '1', '-framerate', str(FPS), '-t', '%.3f' % dur, '-i', ov]
    if kind == 'hook':
        seq = os.path.join(SRC, 'human_male' if 'human' in PLAYABLE else RACES[0][0] + '_male')
        flt, ow, oh = fit(seq, 900, 1060)
        cmd += ['-stream_loop', '-1', '-framerate', '30', '-i', os.path.join(seq, '%04d.png')]
        fc = ('[0:v]setsar=1[b];[2:v]fps=%d,format=rgba,%s[t];[b][t]overlay=%d:%d[s];'
              '[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[o];[s][o]overlay=format=auto,format=yuv420p[v]'
              % (FPS, flt, (W - ow) // 2, TOP + 1040 - oh))
    elif kind and '|' in kind:
        r, sx = kind.split('|')
        seq = os.path.join(SRC, '%s_%s' % (r, sx))
        flt, ow, oh = fit(seq, 900, 1000)
        cmd += ['-stream_loop', '-1', '-framerate', '30', '-i', os.path.join(seq, '%04d.png')]
        fc = ('[0:v]setsar=1[b];[2:v]fps=%d,format=rgba,%s[t];[b][t]overlay=%d:%d[s];'
              '[1:v]format=rgba,fade=t=in:st=0:d=0.2:alpha=1[o];[s][o]overlay=format=auto,format=yuv420p[v]'
              % (FPS, flt, (W - ow) // 2, TOP + 1000 - oh))
    elif kind == 'bust':
        cmd += ['-stream_loop', '-1', '-framerate', '30', '-i', os.path.join(BUST, '%04d.png')]
        fc = ('[0:v]setsar=1[b];[2:v]fps=%d,format=rgba,scale=1080:1080[t];[b][t]overlay=0:%d[s];'
              '[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[o];[s][o]overlay=format=auto,format=yuv420p[v]' % (FPS, TOP))
    elif kind:
        parts = []
        for sx in ('male', 'female'):
            seq = os.path.join(SRC, '%s_%s' % (kind, sx))
            parts.append(fit(seq, 500, 1000) + (seq,))
            cmd += ['-stream_loop', '-1', '-framerate', '30', '-i', os.path.join(seq, '%04d.png')]
        (fm, wm, hm, _), (ff, wf, hf, _) = parts
        fc = ('[0:v]setsar=1[b];[2:v]fps=%d,format=rgba,%s[m];[3:v]fps=%d,format=rgba,%s[f];'
              '[b][m]overlay=%d:%d[s1];[s1][f]overlay=%d:%d[s2];'
              '[1:v]format=rgba,fade=t=in:st=0:d=0.2:alpha=1[o];[s2][o]overlay=format=auto,format=yuv420p[v]'
              % (FPS, fm, FPS, ff, 270 - wm // 2, TOP + 1000 - hm, 810 - wf // 2, TOP + 1000 - hf))
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
        if text:
            wav, vd = V.line(V.readable(text))
            dur = max(mind, BP.LEAD + vd + BP.TAIL)
            say.append((t + BP.LEAD, wav))
        else:
            dur = mind
        finals.append(seg(i, fn(), kind, dur))
        tl.append((t, dur)); t += dur
    total = t
    lst = os.path.join(WORK, 'list.txt')
    open(lst, 'w').write(''.join("file '%s'\n" % p.replace(os.sep, '/') for p in finals))
    base = os.path.join(WORK, 'base.mp4')
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base])
    audio = BP.mix_audio(WORK, MUSIC, total, say)
    run([FF, '-v', 'error', '-y', '-i', base, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', '%.3f' % total, OUT])
    import watermark
    watermark.apply(OUT, center=(540, 1650))   # under the characters, between MALE and FEMALE
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
