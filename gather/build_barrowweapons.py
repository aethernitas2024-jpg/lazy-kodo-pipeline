# -*- coding: utf-8 -*-
"""Short: every Barrow Deeps raid weapon model in 3D, from the WoW Forever beta client (07/10/2026).

    py -3.11 build_barrowweapons.py

Models: client 1.60.1.70245, ModelFileData/ItemDisplayInfo/ItemAppearance/ItemModifiedAppearance (forever-db2/1.60.1.70245/extra,
barrow.py). Meshes: forever-casc/export_m2b.py; turntables rendered in Blender 5.2 (scratchpad/barrow/turntable.py, 135 frames @30).
Item names: only "Torch of Light" (279246) is readable; the rest are encrypted.
"""
import base64
import io
import json
import os

from PIL import Image, ImageDraw

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title
from build_whimsy import line

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', 'barrowweapons'); os.makedirs(WORK, exist_ok=True)
SRC = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\barrow'
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - Barrow Deeps raid weapons in 3D (EN).mp4'
MUSIC = 'barrow'
GREY = (200, 200, 190, 235)
AMBER = (255, 190, 80, 255)
FROST = (150, 200, 255, 255)
FROSTG = (40, 80, 150, 255)
TT_Y = 470                 # top of the 1080x1080 turntable

WEAPONS = [
    (7816286, 'TWO-HANDED SWORD', 'Two handed sword.', None),
    (7816288, 'TWO-HANDED AXE', 'Two handed axe.', None),
    (7816299, 'TWO-HANDED MACE', 'Two handed mace.', None),
    (7816304, 'POLEARM', 'Polearm.', None),
    (7816289, 'STAFF', 'Staff.', None),
    (7816287, 'BOW', 'Bow.', None),
    (7816306, 'ONE-HANDED SWORD', 'A one handed sword. Yes, the game files say this ring is a sword.', 'yes, the game files call it a sword'),
    (7816305, 'ONE-HANDED AXE', 'One handed axe.', None),
    (7816295, 'ONE-HANDED MACE', 'One handed mace.', None),
    (7816302, 'DAGGER', 'Dagger.', None),
    (7816303, 'FIST WEAPON', 'Fist weapon.', None),
    (7816291, 'WAND', 'And a wand, the only one with a readable name: Torch of Light.', 'Torch of Light'),
    (7816338, 'SHIELD', 'And the shield.', None),
]


def swatches(im, fdid, y, active=None):
    d = json.load(open(os.path.join(SRC, '%d.json' % fdid)))
    vs = d['variants']
    sz, gap = 96, 22
    x = (W - (len(vs) * sz + (len(vs) - 1) * gap)) // 2
    for v in vs:
        t = Image.open(io.BytesIO(base64.b64decode(v['uri'].split(',', 1)[1]))).convert('RGBA')
        t = t.resize((sz, sz), Image.LANCZOS)
        on = active is not None and vs.index(v) == active
        if active is not None and not on:
            t.putalpha(t.getchannel('A').point(lambda a: a * 0.45))
        b = 7 if on else 3
        fr = Image.new('RGBA', (sz + 2 * b, sz + 2 * b), (255, 230, 150, 255) if on else (120, 110, 90, 200))
        fr.alpha_composite(t, (b, b))
        im.alpha_composite(fr, (x - b, y - b))
        x += sz + gap
    return y + sz + 6, len(vs)


def card(i, n, fdid, label, name):
    def one(k):
        im = blank()
        ImageDraw.Draw(im).rectangle((0, 0, W, 430), fill=(0, 0, 0, 110))
        y = title(im, 'BARROW DEEPS RAID  ·  %d / %d' % (i, n), 210, 44, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
        title(im, label, y + 16, 110, fill=FROST, spacing=6, glow=FROSTG)
        y = TT_Y + 1080 + 10
        y, nv = swatches(im, fdid, y, k)
        y = line(im, 'color %d of %d' % (k + 1, nv), y + 10, 46, AMBER)
        line(im, name if name else 'name and stats: still encrypted', y - 4, 42, SICK if name else GREY)
        return save(im, WORK, 'card_%02d_%d' % (i, k))

    def fn():
        return [one(k) for k in range(4)]
    return fn


def hook():
    im = blank()
    ImageDraw.Draw(im).rectangle((0, 0, W, 470), fill=(0, 0, 0, 110))
    y = title(im, 'WOW FOREVER  ·  RAID', 190, 46, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
    y = title(im, 'BARROW DEEPS', y + 14, 130, fill=FROST, spacing=6, glow=FROSTG)
    line(im, 'every weapon model, in 3D', y + 20, 54, BONE)
    y = TT_Y + 1080 + 30
    y = line(im, 'straight from the beta files', y, 48, AMBER)
    line(im, '13 weapons  ·  4 colors each', y, 46, SICK)
    return save(im, WORK, 'hook')


def outro():
    im = blank()
    ImageDraw.Draw(im).rectangle((0, 0, W, H), fill=(0, 0, 0, 120))
    y = title(im, 'WHICH ONE?', 300, 120, fill=FROST, spacing=6, glow=FROSTG)
    thumbs = [Image.open(os.path.join(SRC, 'cy_%d' % f, '0012.png')).convert('RGBA') for f, *_ in WEAPONS]
    cols, sz = 5, 200
    for k, t in enumerate(thumbs):
        t = t.resize((sz, sz), Image.LANCZOS)
        r, c = divmod(k, cols)
        n = cols if r < len(thumbs) // cols else len(thumbs) % cols
        x0 = (W - n * sz) // 2
        im.alpha_composite(t, (x0 + c * sz, y + 40 + r * (sz + 10)))
    y = y + 40 + 3 * (sz + 10) + 30
    y = line(im, 'tell me which one you want', y, 52, BONE)
    y = line(im, 'follow: names & stats when Blizzard reveals them', y, 40, SICK)
    line(im, 'beta files  ·  may still change', y, 38, GREY)
    return save(im, WORK, 'outro')


PLAN = [(hook, 7816289, 'The Barrow Deeps raid in WoW Forever. Every weapon model, in 3D, straight from the beta files.', 6.0)]
for k, (f, label, voice, name) in enumerate(WEAPONS, 1):
    PLAN.append((card(k, len(WEAPONS), f, label, name), f, voice, 6.0))
PLAN.append((outro, None, 'Which one do you want? Tell me in the comments, and follow for the names and stats when Blizzard reveals them.', 6.0))


def seg(i, ov, fdid, dur):
    out = os.path.join(WORK, 'final_%02d.mp4' % i)
    bg = BP.shot(WORK, i, 'vault', dur, seed=i * 19 + 7, bright=-0.30)
    ovs = ov if isinstance(ov, list) else [ov]
    cmd = [FF, '-v', 'error', '-y', '-i', bg]
    for o in ovs:
        cmd += ['-loop', '1', '-framerate', str(FPS), '-t', '%.3f' % dur, '-i', o]
    if fdid:
        ti = 1 + len(ovs)
        cmd += ['-stream_loop', '-1', '-framerate', '30', '-i', os.path.join(SRC, 'cy_%d' % fdid, '%04d.png')]
        fc = '[0:v]setsar=1[b];[%d:v]fps=%d,format=rgba,scale=1080:1080[t];[b][t]overlay=0:%d:shortest=0[s0];' % (ti, FPS, TT_Y)
        if len(ovs) == 1:
            fc += '[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[o];[s0][o]overlay=format=auto,format=yuv420p[v]'
        else:
            per = 1.5
            for k in range(len(ovs)):
                a, b = k * per, (k + 1) * per if k < len(ovs) - 1 else dur + 1
                last = '[v]' if k == len(ovs) - 1 else '[s%d]' % (k + 1)
                fc += "[s%d][%d:v]overlay=format=auto:enable='between(t,%.3f,%.3f)'%s%s" % (
                    k, k + 1, a, b - 0.001, ',format=yuv420p' if k == len(ovs) - 1 else '', last)
                if k < len(ovs) - 1:
                    fc += ';'
    else:
        fc = '[0:v]setsar=1[b];[1:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1[o];[b][o]overlay=format=auto,fade=t=out:st=%.3f:d=0.8,format=yuv420p[v]' % (dur - 0.8)
    cmd += ['-filter_complex', fc, '-map', '[v]', '-an', '-t', '%.3f' % dur, '-r', str(FPS),
            '-c:v', 'h264_nvenc', '-preset', 'p7', '-tune', 'hq', '-rc', 'vbr', '-cq', '22', '-b:v', '0', '-maxrate', '13M', '-bufsize', '26M', out]
    run(cmd)
    return out


def main():
    finals, say, tl, t = [], [], [], 0.0
    for i, (fn, fdid, text, mind) in enumerate(PLAN):
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        finals.append(seg(i, fn(), fdid, dur))
        say.append((t + BP.LEAD, wav)); tl.append((t, dur)); t += dur
    total = t
    lst = os.path.join(WORK, 'list.txt')
    open(lst, 'w').write(''.join("file '%s'\n" % p.replace(os.sep, '/') for p in finals))
    base = os.path.join(WORK, 'base.mp4')
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base])
    audio = BP.mix_audio(WORK, MUSIC, total, say)
    run([FF, '-v', 'error', '-y', '-i', base, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', '%.3f' % total, OUT])
    for i, (a, d) in enumerate(tl):
        print('%d %6.2f +%5.2f' % (i, a, d))
    import watermark
    watermark.apply(OUT)
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
