# -*- coding: utf-8 -*-
"""Channel watermark ("The Lazy Kodo" badge) for every short.

    py -3.11 watermark.py <in.mp4> [out.mp4]        (default: replaces in.mp4)
    import watermark; watermark.apply(path)

Logo source: C:\\Users\\d2460n\\Videos\\World Of Warcraft\\_brand\\lazy_kodo.png (square art, light paper background).
Anti-theft mark (user choice 07/10/2026): the logo cut out from its paper background, ~400 px, 30 % opacity,
beside the subject on the left, at its mid height: not over the object (user 07/10), still inside the frame's main area.
Audio is copied, video re-encoded with NVENC.
"""
import os
import shutil
import sys

from PIL import Image, ImageDraw

import build_prof as BP

LOGO = r'C:\Users\d2460n\Videos\World Of Warcraft\_brand\lazy_kodo.png'
BADGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build', 'lazy_kodo_ghost.png')
SIZE, OPACITY = 330, 0.34
CENTER = (215, 1010)   # beside the subject, left side (right side = TikTok buttons); turntable sits at y 470-1550


def badge():
    if os.path.exists(BADGE) and os.path.getmtime(BADGE) >= os.path.getmtime(LOGO):
        return BADGE
    import numpy as np
    im = Image.open(LOGO).convert('RGB')
    a = np.asarray(im).astype(np.float32)
    paper = np.median(a[:40, :40].reshape(-1, 3), axis=0)
    dist = np.sqrt(((a - paper) ** 2).sum(-1))
    alpha = np.clip((dist - 18) * 6, 0, 255) * OPACITY
    rgba = np.dstack([a, alpha]).astype(np.uint8)
    out = Image.fromarray(rgba, 'RGBA')
    out = out.crop(out.getbbox())
    s = SIZE / max(out.size)
    out = out.resize((round(out.width * s), round(out.height * s)), Image.LANCZOS)
    os.makedirs(os.path.dirname(BADGE), exist_ok=True)
    out.save(BADGE)
    return BADGE


def apply(src, dst=None, center=None):
    tmp = (dst or src) + '.wm.mp4'
    w, h = Image.open(badge()).size
    cx, cy = center or CENTER
    x, y = cx - w // 2, cy - h // 2
    BP.run([BP.FF, '-v', 'error', '-y', '-i', src, '-i', badge(),
            '-filter_complex', '[0:v][1:v]overlay=%d:%d:format=auto,format=yuv420p[v]' % (x, y),
            '-map', '[v]', '-map', '0:a?', '-c:a', 'copy',
            '-c:v', 'h264_nvenc', '-preset', 'p7', '-tune', 'hq', '-rc', 'vbr', '-cq', '22', '-b:v', '0',
            '-maxrate', '13M', '-bufsize', '26M', '-movflags', '+faststart', tmp])
    shutil.move(tmp, dst or src)
    return dst or src


if __name__ == '__main__':
    print(apply(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
