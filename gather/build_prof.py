# -*- coding: utf-8 -*-
"""One vertical short per gathering profession: 1-300 route + what Forever changed.

    py -3.11 build_prof.py mining [herbalism skinning]

Backdrops: WoW Forever's own loading-screen paintings (Camelot160), panned.
Icons: item icons read from the beta client. Narration: edge-tts (voice.py).
Each shot lasts as long as its narration needs, so nothing is cut off.
"""
import os, sys, subprocess, textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SPEC = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\spec'
sys.path.insert(0, SPEC)
import build as B          # noqa: E402  fonts + text helpers of the spec shorts
import voice as V          # noqa: E402
import profdata as P       # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FF, W, H, FPS = B.FF, B.W, B.H, 60
OUTDIR = r'C:\Users\d2460n\Videos\World Of Warcraft\profession guides'
GOLD, BONE = B.GOLD, B.BONE
SICK = (245, 205, 120, 255)
GREEN = (150, 214, 120, 255)
RED = (196, 48, 38, 255)
QUAL = {1: (255, 255, 255, 255), 2: (30, 255, 0, 255), 3: (0, 112, 221, 255)}
GEORGIA_B = r'C:\Windows\Fonts\georgiab.ttf'


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(' '.join(str(c) for c in cmd)[:600]); print(r.stderr[-2500:]); raise SystemExit(1)


# ------------------------------------------------------------ backdrops

def tall(name):
    """Loading-screen painting without its letterbox, scaled to 1920 px high."""
    out = os.path.join(HERE, 'load', f'tall_{name}.jpg')
    if not os.path.exists(out):
        im = Image.open(os.path.join(HERE, 'load', f'{name}.jpg'))
        top = 345 if name == 'old_ironforge' else 280
        im = im.crop((0, top, im.width, 1410))
        im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
        im.save(out, quality=93)
    return out


def shot(work, i, art, dur, seed, bright=-0.06):
    """Slow horizontal pan across a painting."""
    out = os.path.join(work, f'shot_{i:02d}.mp4')
    src = tall(art)
    wid = Image.open(src).width
    span = wid - W
    rng = np.random.default_rng(seed)
    x0 = int(rng.uniform(0.05, 0.75) * span)
    v = min(38.0, (span - x0 - 1) / dur) * (1 if rng.random() < 0.5 or x0 < span * 0.3 else -1)
    if v < 0:
        v = -min(38.0, x0 / dur)
    vf = (f"crop={W}:{H}:x='{x0}+t*{v:.3f}':y=0,"
          f"eq=brightness={bright}:saturation=1.05:contrast=1.04,format=yuv420p")
    run([FF, '-v', 'error', '-y', '-loop', '1', '-framerate', str(FPS), '-t', f'{dur:.3f}', '-i', src,
         '-vf', vf, '-an', '-t', f'{dur:.3f}',
         '-c:v', 'h264_nvenc', '-preset', 'p5', '-rc', 'vbr', '-cq', '19', '-b:v', '0', out])
    return out


# ------------------------------------------------------------- overlays

def blank():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def save(im, work, name):
    p = os.path.join(work, name + '.png'); im.save(p); return p


def frame_png(work):
    y = np.arange(H)[:, None] / 1.0
    x = np.arange(W)[None, :] / 1.0
    a_row = np.maximum(np.clip(1 - y / 300, 0, 1) ** 1.5 * 0.72, np.clip((y - 1580) / 340, 0, 1) ** 1.4 * 0.80)
    dx = np.abs((x - W / 2) / (W / 2))
    a = np.clip(a_row + np.clip(dx - 0.72, 0, None) / 0.28 * 0.30, 0, 1)
    arr = np.zeros((H, W, 4), np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = 4, 8, 6
    arr[..., 3] = (a * 255).astype(np.uint8)
    return save(Image.fromarray(arr, 'RGBA'), work, 'frame')


def title(im, text, y, size, fill=BONE, glow=(200, 120, 40, 255), spacing=8, font=None, maxw=990):
    f = B.fit(font or B.CINZEL, text, maxw, size, 900, spacing=spacing)
    im.alpha_composite(B.glow_layer(
        lambda dd, v: B.draw_spaced(dd, (W / 2, y), text, f, v, spacing=spacing), 24, glow))
    d = ImageDraw.Draw(im)
    B.draw_spaced(d, (W / 2 + 4, y + 5), text, f, (0, 0, 0, 225), spacing=spacing)
    B.draw_spaced(d, (W / 2, y), text, f, fill, spacing=spacing)
    return y + f.getbbox('Ag')[3]


def icon(item, size, border=(150, 150, 150, 255)):
    ic = Image.open(os.path.join(HERE, 'icons', f'{item}.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    box = Image.new('RGBA', (size + 12, size + 12), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle((0, 0, size + 11, size + 11), 12, fill=(10, 10, 14, 255),
                                          outline=border, width=4)
    box.alpha_composite(ic, (6, 6))
    sh = Image.new('RGBA', (size + 60, size + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((24, 30, size + 36, size + 42), 14, fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    sh.alpha_composite(box, (24, 24))
    return sh           # icon sits at (+24, +24) inside


def pill(im, text, y, font, size, fill, bg=(8, 10, 14, 232), outline=GOLD, maxw=920, pad=80, h=None):
    d = ImageDraw.Draw(im)
    f = B.fit(font, text, maxw, size)
    tw = B.text_w(f, text) + pad
    hh = h or f.getbbox('Ag')[3] + 44
    sh = blank()
    ImageDraw.Draw(sh).rounded_rectangle([(W - tw) / 2, y, (W + tw) / 2, y + hh], 22, fill=(0, 0, 0, 205))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([(W - tw) / 2, y, (W + tw) / 2, y + hh], 22, fill=bg, outline=outline, width=3)
    d.text((W / 2, y + hh / 2), text, font=f, fill=fill, anchor='mm')
    return y + hh


def kicker_png(work, prof):
    im = blank()
    d = ImageDraw.Draw(im)
    t = f"{prof['title']} 1–300   ·   WOW FOREVER"
    f = B.fit(B.CINZEL, t, 900, 40, 700, spacing=6)
    tw = B.text_w(f, t, 6) + 60
    d.rounded_rectangle([(W - tw) / 2, 128, (W + tw) / 2, 196], 18, fill=(8, 10, 14, 205), outline=GOLD, width=2)
    B.draw_spaced(d, (W / 2, 144), t, f, SICK, spacing=6)
    return save(im, work, 'kicker')


def hook_png(work, prof):
    im = blank()
    B.backdrop(im, 860, 700, 560, 215)
    y = title(im, prof['title'], 380, 190, spacing=10)
    y = title(im, '1  →  300', y + 40, 120, fill=GOLD, spacing=6)
    ics = prof['hook_icons']
    sz, gap = 132, 26
    tot = len(ics) * (sz + 12) + (len(ics) - 1) * gap
    x = (W - tot) // 2
    for it in ics:
        c = icon(it, sz)
        im.alpha_composite(c, (x - 24, y + 70 - 24)); x += sz + 12 + gap
    y += 70 + sz + 70
    d = ImageDraw.Draw(im)
    f = B.fit(B.GEORGIA_I, 'the route + everything Forever changed', 960, 62)
    d.text((W / 2, y), 'the route + everything Forever changed', font=f, fill=SICK, anchor='ma')
    return save(im, work, 'hook')


def bracket_png(work, i, br):
    rng, items, names, zones, tip, _ = br
    im = blank()
    B.backdrop(im, 1000, 700, 620, 220)
    y = title(im, rng, 360, 150, fill=BONE, spacing=6)
    y = title(im, 'SKILL', y + 18, 44, fill=GOLD, spacing=18, glow=(0, 0, 0, 0))
    n = len(items)
    sz = 190 if n == 1 else 170 if n == 2 else 150
    colw = 330 if n == 3 else 380
    y += 70
    d = ImageDraw.Draw(im)
    for k, (it, nm) in enumerate(zip(items, names)):
        cx = W / 2 + (k - (n - 1) / 2) * colw
        c = icon(it, sz, border=GOLD)
        im.alpha_composite(c, (int(cx - (sz + 12) / 2) - 24, y - 24))
        d = ImageDraw.Draw(im)
        f = B.fit(GEORGIA_B, nm, colw - 20, 48)
        d.text((cx + 3, y + sz + 40 + 3), nm, font=f, fill=(0, 0, 0, 230), anchor='ma')
        d.text((cx, y + sz + 40), nm, font=f, fill=BONE, anchor='ma')
    y += sz + 150
    # zones panel
    fz = B.font(B.GEORGIA_I, 50)
    lines = []
    for z in zones:
        head, _, rest = z.partition(': ')
        if not rest:
            head, rest = '', z
        lines.append((head, rest))
    ph = 60 + sum((fz.getbbox('Ag')[3] + 14) * (2 if h else 1) for h, _ in lines) + 30
    sh = blank()
    ImageDraw.Draw(sh).rounded_rectangle([70, y, W - 70, y + ph], 26, fill=(0, 0, 0, 200))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([70, y, W - 70, y + ph], 26, fill=(8, 10, 14, 225), outline=(120, 100, 60, 220), width=3)
    yy = y + 34
    fh = B.font(B.CINZEL, 40, 800)
    colours = {'Horde': (230, 80, 60, 255), 'Alliance': (90, 150, 240, 255), 'Contested': GOLD}
    for head, rest in lines:
        if head:
            B.draw_spaced(d, (W / 2, yy), head.upper(), fh, colours.get(head, GOLD), spacing=10)
            yy += fh.getbbox('Ag')[3] + 14
        f = B.fit(B.GEORGIA_I, rest, W - 200, 50)
        d.text((W / 2, yy), rest, font=f, fill=BONE, anchor='ma')
        yy += fz.getbbox('Ag')[3] + 14
    y += ph + 40
    if tip:
        pill(im, tip, y, B.GEORGIA_I, 46, SICK)
    return save(im, work, f'br_{i:02d}')


def new_png(work, i, head, rows, first):
    im = blank()
    n = len(rows)
    isz = 150 if n <= 3 else 118
    fq = B.font(B.GEORGIA_I, 40 if n <= 3 else 36)
    lay = []
    for it, name, q, desc in rows:
        fname = B.fit(GEORGIA_B, name, 980 - isz - 90, 54 if n <= 3 else 46)
        wrap = textwrap.wrap(desc, 30) if desc else []
        hgt = max(isz + 12, fname.getbbox('Ag')[3] + 14 + len(wrap) * (fq.getbbox('Ag')[3] + 8))
        lay.append((it, name, q, wrap, fname, hgt))
    gap = 46
    fh = B.fit(B.CINZEL, head, 900, 80, 900, spacing=10)
    total = fh.getbbox('Ag')[3] + 70 + sum(r[5] for r in lay) + gap * (n - 1)
    y = max(420, (H - total) // 2 - 40)
    panel = blank()
    ImageDraw.Draw(panel).rounded_rectangle((40, y - 60, W - 40, y + total + 60), 28, fill=(6, 8, 16, 222),
                                            outline=(214, 180, 104, 200), width=4)
    im.alpha_composite(panel)
    pill(im, 'NEW IN WOW FOREVER', y - 150, B.CINZEL, 40, BONE, bg=(110, 12, 10, 240), h=74)
    title(im, head, y, 80, fill=GOLD, spacing=10, glow=(200, 120, 40, 200))
    y += fh.getbbox('Ag')[3] + 28
    d = ImageDraw.Draw(im)
    d.line([(W / 2 - 170, y), (W / 2 + 170, y)], fill=(214, 180, 104, 170), width=3)
    y += 42
    for it, name, q, wrap, fname, hgt in lay:
        im.alpha_composite(icon(it, isz), (76 - 24, y - 24))
        d = ImageDraw.Draw(im)
        tx = 76 + isz + 46
        ty = y + max(0, (isz + 12 - (fname.getbbox('Ag')[3] + 14 + len(wrap) * (fq.getbbox('Ag')[3] + 8))) // 2)
        d.text((tx, ty), name, font=fname, fill=QUAL.get(q, BONE))
        ty += fname.getbbox('Ag')[3] + 14
        for ln in wrap:
            d.text((tx, ty), ln, font=fq, fill=(255, 209, 0, 255)); ty += fq.getbbox('Ag')[3] + 8
        y += hgt + gap
    fb = B.font(B.GEORGIA_I, 30)
    d.text((W / 2, y + 40), P.BUILD, font=fb, fill=(190, 190, 180, 230), anchor='ma')
    return save(im, work, f'new_{i:02d}')


def closer_png(work, text):
    words = text.split()
    best, score = len(words), None
    for cut in range(1, len(words)):
        s = abs(len(' '.join(words[:cut])) - len(' '.join(words[cut:])))
        if score is None or s < score:
            best, score = cut, s
    im = blank()
    B.backdrop(im, 900, 700, 360, 215)
    title(im, 'REMEMBER', 580, 74, fill=GOLD, spacing=10)
    d = ImageDraw.Draw(im)
    y = 780
    for ln in (' '.join(words[:best]), ' '.join(words[best:])):
        f = B.fit(B.GEORGIA_I, ln, 950, 76)
        d.text((W / 2 + 4, y + 5), ln, font=f, fill=(0, 0, 0, 235), anchor='ma')
        d.text((W / 2, y), ln, font=f, fill=BONE, anchor='ma')
        y += f.getbbox('Ag')[3] + 26
    d.line([(250, y + 30), (W - 250, y + 30)], fill=GOLD, width=3)
    return save(im, work, 'closer')


def outro_png(work, prof):
    im = blank()
    B.backdrop(im, 850, 660, 330, 215)
    y = title(im, 'LIKE + FOLLOW', 700, 96)
    d = ImageDraw.Draw(im)
    f = B.fit(B.GEORGIA_I, 'one guide for every profession', 900, 54)
    d.text((W / 2, y + 40), 'one guide for every profession', font=f, fill=SICK, anchor='ma')
    f2 = B.fit(B.GEORGIA_I, prof['next'], 900, 46)
    d.text((W / 2, y + 130), prof['next'], font=f2, fill=GREEN, anchor='ma')
    return save(im, work, 'outro')


# ----------------------------------------------------------------- audio

def mix_audio(work, music, total, say):
    src = os.path.join(SPEC, 'music_class', music)
    tracks = [os.path.join(src, f) for f in sorted(os.listdir(src)) if f.endswith('.mp3')]
    lst = os.path.join(work, 'music.txt')
    open(lst, 'w').write(''.join(f"file '{p.replace(os.sep, '/')}'\n" for p in tracks * 3))
    bed = os.path.join(work, 'music.wav')
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-af',
         f'atrim=0:{total},asetpts=PTS-STARTPTS,volume=0.72,afade=t=in:d=1.0,'
         f'afade=t=out:st={total - 3.0}:d=3.0,aresample=48000', '-ac', '2', bed])
    out = os.path.join(work, 'audio.wav')
    cmd = [FF, '-v', 'error', '-y', '-i', bed]
    for _, p in say:
        cmd += ['-i', p]
    fc, names = ['[0:a]volume=0.24[m]'], ['[m]']
    for j, (t, _) in enumerate(say, start=1):
        ms = int(t * 1000)
        fc.append(f'[{j}:a]adelay={ms}|{ms},volume=1.5[v{j}]'); names.append(f'[v{j}]')
    fc.append(''.join(names) + f'amix=inputs={len(names)}:normalize=0:duration=first[a]')
    cmd += ['-filter_complex', ';'.join(fc), '-map', '[a]', '-ac', '2', '-ar', '48000', '-t', f'{total:.3f}', out]
    run(cmd)
    return out


# ----------------------------------------------------------------- build

LEAD, TAIL = 0.45, 0.9       # voice starts LEAD s into a shot; shot outlasts it by TAIL


def build(key):
    prof = P.PROF[key]
    work = os.path.join(HERE, 'build', key); os.makedirs(work, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, f"{prof['title'].title()} 1-300 - WoW Forever guide (EN).mp4")

    # plan: (kind, payload, art, voice text, min duration)
    plan = [('hook', None, prof['art'][0], prof['hook_voice'], 4.0)]
    for j, br in enumerate(prof['brackets']):
        plan.append(('br', br, prof['art'][j % len(prof['art'])], V.readable(br[5]), 5.5))
    for j, nw in enumerate(prof['new']):
        plan.append(('new', nw, prof['new_art'][j % len(prof['new_art'])], nw[2], 6.0))
    plan.append(('close', None, prof['art'][1], f"Remember. {prof['closer']}", 5.0))
    plan.append(('outro', None, prof['new_art'][0],
                 f"Like and follow. One guide for every profession. {prof['next']}.", 4.5))

    files, tl, say, t = [], [], [], 0.0
    for i, (kind, pay, art, text, mind) in enumerate(plan):
        wav, vd = V.line(text)
        dur = max(mind, LEAD + vd + TAIL)
        files.append(shot(work, i, art, dur, seed=hash((key, i)) % 1000, bright=0.02 if kind == 'hook' else -0.07))
        say.append((t + LEAD, wav))
        tl.append((t, dur)); t += dur
    total = t

    lst = os.path.join(work, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p.replace(os.sep, '/')}'\n" for p in files))
    base = os.path.join(work, 'base.mp4')
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base])

    ovs = [(frame_png(work), 0, total, 0, 0)]
    ovs.append((kicker_png(work, prof), tl[1][0], tl[-1][0], 0.4, 0.4))
    for i, (kind, pay, *_ ) in enumerate(plan):
        a, d = tl[i]
        if kind == 'hook':
            # on screen from frame zero: TikTok uses the first frame as the cover
            ovs.append((hook_png(work, prof), 0.0, a + d, 0.0, 0.15))
        elif kind == 'br':
            ovs.append((bracket_png(work, i, pay), a + 0.1, a + d, 0.25, 0.16))
        elif kind == 'new':
            ovs.append((new_png(work, i, pay[0], pay[1], i == len(prof['brackets']) + 1), a + 0.1, a + d, 0.25, 0.16))
        elif kind == 'close':
            ovs.append((closer_png(work, prof['closer']), a + 0.2, a + d, 0.3, 0.2))
        else:
            ovs.append((outro_png(work, prof), a + 0.2, total, 0.35, 0.7))

    audio = mix_audio(work, prof['music'], total, say)
    cmd = [FF, '-v', 'error', '-y', '-i', base]
    for p, a, b, fi, fo in ovs:
        cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{b - a:.3f}', '-i', p]
    cmd += ['-i', audio]
    fc, last = ['[0:v]setsar=1[g0]'], '[g0]'
    for j, (p, a, b, fi, fo) in enumerate(ovs, start=1):
        ch = f'[{j}:v]format=rgba'
        if fi: ch += f',fade=t=in:st=0:d={fi}:alpha=1'
        if fo: ch += f',fade=t=out:st={max(0, b - a - fo):.3f}:d={fo}:alpha=1'
        fc.append(ch + f',setpts=PTS+{a:.3f}/TB[o{j}]')
        fc.append(f'{last}[o{j}]overlay=eof_action=pass:format=auto[v{j}]'); last = f'[v{j}]'
    fc.append(f'{last}fade=t=out:st={total - 0.8:.3f}:d=0.8,format=yuv420p,setsar=1[vout]')
    cmd += ['-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', f'{len(ovs) + 1}:a',
            '-c:v', 'h264_nvenc', '-preset', 'p7', '-tune', 'hq', '-rc', 'vbr', '-cq', '22', '-b:v', '0',
            '-maxrate', '13M', '-bufsize', '26M', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart', '-t', f'{total:.3f}', out]
    run(cmd)
    print('OK', out, round(total, 2))
    return out, tl


if __name__ == '__main__':
    for k in sys.argv[1:]:
        build(k)
