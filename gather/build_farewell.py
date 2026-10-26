# -*- coding: utf-8 -*-
"""Short: goodbye to the WoW Forever beta (21/10/2026).

    py -3.11 build_farewell.py

A montage of the creator's own beta screenshots (his tauren Drakhon Duskhorn), then reminders:
the free stress test (Oct 21, 19:00 CEST / 14:00 PDT), name reservation (Oct 27 - Nov 3), launch (Nov 4).
Screenshots: F:\\blizz\\World of Warcraft\\_classic_beta_\\Screenshots. Each one is cropped to 9:16 around
the character, above the action bars, then slowly zoomed.
"""
import os
import subprocess

from PIL import Image, ImageFilter, ImageEnhance

import build_prof as BP
from build_prof import V, W, H, FPS, FF, BONE, SICK, run, blank, save
import build_leafre as L

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', 'farewell'); os.makedirs(WORK, exist_ok=True)
L.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - goodbye beta (EN).mp4'
SHOTS = r'F:\blizz\World of Warcraft\_classic_beta_\Screenshots'
MUSIC = os.path.join(BP.SPEC, 'music_class', 'hyjal', '1_summit_1.mp3')
GOLD = (255, 210, 90, 255)
AMBER = (255, 190, 80, 255)
GREY = (200, 200, 190, 235)
RED = (235, 90, 80, 255)

# (screenshot stamp, crop centre x 0..1, caption)
MONTAGE = [
    ('092826_160318', .50, ''),                       # sunrise on the peak: title over it
    ('092026_165450', .50, 'the first steps'),
    ('092126_155022', .45, 'quiet mornings'),
    ('092226_161440', .50, 'endless roads'),
    ('092826_155031', .45, 'golden evenings'),
    ('092826_160226', .50, 'into the light'),
    ('092826_183719', .60, 'meeting Saurfang himself'),
    ('092226_222044', .45, 'burning skies'),
    ('092526_145459', .50, 'old stones'),
    ('100526_233212', .45, 'the long road south'),
    ('100526_002624', .52, 'Master Angler of Booty Bay'),
    ('101326_175831', .50, 'set sail'),
    ('092826_160954', .40, 'one last view'),
    ('101126_124905', .55, 'goodbye, beta'),
]
SHOT_LEN = 3.0
FADE = 0.5


def find(stamp):
    for f in os.listdir(SHOTS):
        if stamp in f:
            return os.path.join(SHOTS, f)
    raise SystemExit('screenshot not found: ' + stamp)


KEEP = {'100526_233212': 0.74, '100526_002624': 0.80}   # shots whose action bars sit higher on screen


def vertical(src, cx, name):
    """9:16 crop centred on cx, keeping the top 87% (action bars cut), upscaled for the zoom."""
    im = Image.open(src).convert('RGB')
    h = int(im.height * next((v for k, v in KEEP.items() if k in src), 0.87))
    w = round(h * 9 / 16)
    x = min(max(0, round(cx * im.width - w / 2)), im.width - w)
    im = im.crop((x, 0, x + w, h)).resize((W + 216, H + 384), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    p = os.path.join(WORK, name + '.png'); im.save(p); return p


def caption(text, name, title=False):
    im = blank()
    if title:
        y = L.head(im, 'WOW FOREVER  ·  SEPT 17 - OCT 21', 'GOODBYE, BETA', GOLD, (200, 140, 40, 255), y=300, size=120)
        L.line(im, 'five weeks with Drakhon', y + 20, 52, BONE)
    elif text:
        from PIL import ImageDraw
        band = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(band).rounded_rectangle((90, 1350, W - 90, 1480), 40, fill=(0, 0, 0, 150))
        im.alpha_composite(band.filter(ImageFilter.GaussianBlur(18)))
        L.line(im, text, 1380, 58, BONE)
    return save(im, WORK, name)


def kenburns(png, ov, dur, out, zoom_in=True):
    z = "'1+0.06*on/%d'" % int(dur * FPS) if zoom_in else "'1.06-0.06*on/%d'" % int(dur * FPS)
    run([FF, '-v', 'error', '-y', '-loop', '1', '-framerate', str(FPS), '-t', f'{dur:.3f}', '-i', png,
         '-loop', '1', '-framerate', str(FPS), '-t', f'{dur:.3f}', '-i', ov,
         '-filter_complex', f"[0:v]zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(dur * FPS)}:s={W}x{H}:fps={FPS},setsar=1[b];"
                            f"[1:v]format=rgba,fade=t=in:st=0.2:d=0.4:alpha=1,fade=t=out:st={dur - 0.6:.2f}:d=0.4:alpha=1[o];"
                            f"[b][o]overlay=format=auto,format=yuv420p[v]",
         '-map', '[v]', '-t', f'{dur:.3f}', '-r', str(FPS), '-c:v', 'h264_nvenc', '-preset', 'p5', '-cq', '19', '-b:v', '0', out])
    return out


CARDS = [
    (L.card('stress', 'TONIGHT  ·  OCTOBER 21', 'FREE STRESS TEST', SICK, (40, 110, 40, 255), [],
            [('19:00 Paris  ·  14:00 PDT', AMBER, 50), ('open to ANY World of Warcraft account', BONE, 40),
             ('no subscription, no beta key', BONE, 40), ('characters are deleted after', GREY, 38)], size=110),
     'Last chance tonight: a free stress test, open to any World of Warcraft account, no subscription needed. '
     'Seven PM in Paris, two PM Pacific. Characters are deleted after.', 8.5),
    (L.card('names', 'OCTOBER 27  TO  NOVEMBER 3', 'RESERVE YOUR NAME', GOLD, (200, 140, 40, 255), [],
            [('up to 3 character names', AMBER, 46), ('first come, first served', BONE, 44),
             ('beta names are NOT kept', RED, 42), ('eligible edition required', GREY, 36)], size=110),
     'Then from October twenty seventh to November third, reserve up to three character names, first come, first served. '
     'Your beta names are not kept.', 8.0),
    (L.card('launch', 'SEE YOU IN AZEROTH', 'NOVEMBER 4', L.RINGC, L.RINGG, [],
            [('launch: 3 PM PST  ·  midnight in Paris', AMBER, 42), ('thanks for following the beta', BONE, 42),
             ('follow for everything Forever', SICK, 42)], size=130),
     'And on November fourth, World of Warcraft Forever launches. Thank you for following the beta with me. See you in Azeroth.', 8.0),
]
INTRO_SAY = "The World of Warcraft Forever beta ends today. Five weeks, one tauren, and a lot of memories. Goodbye, beta."


def main():
    parts, t = [], 0.0
    say = []
    # montage
    wav, vd = V.line(V.readable(INTRO_SAY)); say.append((0.6, wav))
    for i, (stamp, cx, cap) in enumerate(MONTAGE):
        dur = max(SHOT_LEN, vd + 1.2) if i == 0 else SHOT_LEN
        png = vertical(find(stamp), cx, 'm%02d' % i)
        ov = caption(cap, 'c%02d' % i, title=(i == 0))
        parts.append((kenburns(png, ov, dur + FADE, os.path.join(WORK, 'm%02d.mp4' % i), zoom_in=i % 2 == 0), dur + FADE))
        t += dur
    # reminder cards over the last shot, blurred
    bg = Image.open(os.path.join(WORK, 'm%02d.png' % (len(MONTAGE) - 1))).filter(ImageFilter.GaussianBlur(10))
    bg = ImageEnhance.Brightness(bg).enhance(0.55); bgp = os.path.join(WORK, 'cardbg.png'); bg.save(bgp)
    for j, (fn, text, mind) in enumerate(CARDS):
        w2, d2 = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + d2 + BP.TAIL)
        say.append((t + BP.LEAD, w2))
        parts.append((kenburns(bgp, fn(), dur + FADE, os.path.join(WORK, 'k%02d.mp4' % j), zoom_in=j % 2 == 0), dur + FADE))
        t += dur
    total = t + FADE
    # crossfade chain
    args, fc, prev, off = [], [], '[0:v]', 0.0
    for k, (p, d) in enumerate(parts):
        args += ['-i', p]
    for k in range(1, len(parts)):
        off += parts[k - 1][1] - FADE
        lab = '[x%d]' % k
        fc.append(f'{prev}[{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}{lab}')
        prev = lab
    fc[-1] = fc[-1].rsplit('[', 1)[0] + ',fade=t=out:st=%.3f:d=1.0[v]' % (total - 1.0)
    base = os.path.join(WORK, 'base.mp4')
    run([FF, '-v', 'error', '-y'] + args + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-r', str(FPS),
                                            '-c:v', 'h264_nvenc', '-preset', 'p7', '-cq', '21', '-b:v', '0', base])
    # music louder under the montage, ducked under the voice
    ins, mix = ['-stream_loop', '-1', '-i', MUSIC], []
    for k, (st, w) in enumerate(say):
        ins += ['-i', w]; ms = int(st * 1000)
        mix.append(f'[{k + 1}:a]adelay={ms}|{ms},volume=1.5[v{k}]')
    vlab = ''.join('[v%d]' % k for k in range(len(say)))
    fca = (';'.join(mix) + f';{vlab}amix=inputs={len(say)}:normalize=0:duration=longest,apad[voice];'
           f'[voice]asplit=2[vo][key];[0:a]volume=0.55,afade=t=in:d=1.5,afade=t=out:st={total - 3:.2f}:d=3[m];'
           f'[m][key]sidechaincompress=threshold=0.02:ratio=6:attack=40:release=600[duck];'
           f'[vo][duck]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.9[a]')
    audio = os.path.join(WORK, 'audio.wav')
    run([FF, '-v', 'error', '-y'] + ins + ['-filter_complex', fca, '-map', '[a]', '-t', f'{total:.3f}', '-ar', '48000', '-ac', '2', audio])
    run([FF, '-v', 'error', '-y', '-i', base, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', f'{total:.3f}', OUT])
    import watermark
    watermark.apply(OUT, center=(540, 1730))
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
