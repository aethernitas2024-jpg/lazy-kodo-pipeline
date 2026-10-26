# -*- coding: utf-8 -*-
"""In-game style item tooltips for the shorts, from Wowhead Forever tooltip JSON (cached in tooltips/).

    import tooltip as TT
    img = TT.render(276895, width=800)          # RGBA image: icon + tooltip box
    y = TT.paste(im, [276895, 280766], y)       # centred, stacked, returns new y

Sell price is dropped; everything else (ilvl, binds, slot, stats, requirements, Use/Equip) is kept.
"""
import html
import json
import os
import re
import subprocess
from html.parser import HTMLParser

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'tooltips'); os.makedirs(CACHE, exist_ok=True)
ICONS = os.path.join(HERE, 'icons')
FONT = r'C:\Windows\Fonts\georgia.ttf'
FONT_B = r'C:\Windows\Fonts\georgiab.ttf'
W = 1080
COL = {'q0': (157, 157, 157), 'q1': (255, 255, 255), 'q2': (30, 255, 0), 'q3': (0, 112, 221), 'q4': (163, 53, 238),
       'q5': (255, 128, 0), 'q': (255, 209, 0), 'q10': (255, 32, 32)}
WHITE = (255, 255, 255)


def data(item):
    p = os.path.join(CACHE, f'{item}.json')
    if not os.path.exists(p):
        raw = subprocess.run(['curl', '-s', f'https://nether.wowhead.com/forever/tooltip/item/{item}'],
                             capture_output=True, check=True).stdout
        json.loads(raw)
        open(p, 'wb').write(raw)
    return json.load(open(p, encoding='utf-8'))


class _P(HTMLParser):
    """Turns the tooltip HTML into lines: [(left runs, right runs)], runs = [(text, colour, bold)]."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.left, self.right = [], [], []
        self.side, self.stack, self.skip = 'l', [], 0

    def flush(self):
        if any(t.strip() for t, *_ in self.left + self.right):
            self.lines.append((self.left, self.right))
        self.left, self.right = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'br':
            self.flush(); return
        if tag == 'div' and 'whtt-sellprice' in (a.get('class') or ''):
            self.skip += 1
        if tag in ('tr', 'table'):
            self.flush()
        if tag == 'th':
            self.side = 'r'
        if tag == 'td':
            self.side = 'l'
        cls = (a.get('class') or '').split()
        col = next((COL[c] for c in cls if c in COL), None)
        self.stack.append((tag, col, tag == 'b'))

    def handle_endtag(self, tag):
        if tag == 'div' and self.skip:
            self.skip -= 1
        while self.stack:
            t, *_ = self.stack.pop()
            if t == tag:
                break
        if tag in ('tr', 'table', 'div'):
            self.flush()
        if tag in ('th', 'tr', 'table'):
            self.side = 'l'   # stats after an inline "Neck | Bow" table must go back to the left column

    def handle_data(self, d):
        if self.skip or not d:
            return
        col = next((c for _, c, _ in reversed(self.stack) if c), WHITE)
        bold = any(b for *_, b in self.stack)
        (self.right if self.side == 'r' else self.left).append((d, col, bold))


def lines(item):
    j = data(item)
    p = _P(); p.feed(j['tooltip']); p.flush()
    out = []
    for l, r in p.lines:
        txt = re.sub(r'\s+', ' ', ''.join(t for t, *_ in l)).strip()
        if (not txt and not r) or txt.startswith('Durability'):
            continue
        out.append((l, r))
    return j, out


def _wrap(draw, runs, font, fontb, maxw):
    """Word-wrap coloured runs: returns rows of [(word, colour, bold)]."""
    words = []
    for t, c, b in runs:
        for w in re.split(r'(\s+)', t.replace('\n', ' ')):
            if w:
                words.append((w, c, b))
    rows, cur, x = [], [], 0
    for w, c, b in words:
        f = fontb if b else font
        ww = draw.textlength(w, font=f)
        if w.isspace():
            if cur:
                cur.append((' ', c, b)); x += draw.textlength(' ', font=f)
            continue
        if x + ww > maxw and cur:
            while cur and cur[-1][0] == ' ':
                cur.pop()
            rows.append(cur); cur, x = [], 0
        cur.append((w, c, b)); x += ww
    if cur:
        rows.append(cur)
    return rows


def render(item, width=820, size=30, icon=True):
    j, ls = lines(item)
    font, fontb = ImageFont.truetype(FONT, size), ImageFont.truetype(FONT_B, size)
    namef = ImageFont.truetype(FONT_B, int(size * 1.25))
    pad, lh = 26, int(size * 1.32)
    tmp = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    rows = []  # (rows of runs, right runs, font for name?)
    for k, (l, r) in enumerate(ls):
        isname = k == 0
        f = namef if isname else font
        rw = sum(tmp.textlength(t.strip(), font=font) for t, *_ in r) if r else 0
        wr = _wrap(tmp, l, f, namef if isname else fontb, width - 2 * pad - (rw + 30 if rw else 0))
        for i, row in enumerate(wr):
            rows.append((row, r if i == 0 else [], isname))
    h = pad * 2 + sum(int(lh * 1.2) if n else lh for *_, n in rows)
    box = Image.new('RGBA', (width, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(box)
    d.rounded_rectangle((0, 0, width - 1, h - 1), 14, fill=(6, 8, 22, 238), outline=(185, 185, 195, 255), width=3)
    d.rounded_rectangle((5, 5, width - 6, h - 6), 10, outline=(70, 72, 90, 255), width=1)
    y = pad
    for row, r, isname in rows:
        x = pad
        for w, c, b in row:
            f = namef if isname else (fontb if b else font)
            d.text((x, y), w, font=f, fill=c + (255,))
            x += d.textlength(w, font=f)
        if r:
            t = ''.join(t for t, *_ in r).strip()
            d.text((width - pad, y), t, font=font, fill=r[0][1] + (255,), anchor='ra')
        y += int(lh * 1.2) if isname else lh
    if not icon:
        return box
    isz = 112
    ic = None
    fd = None
    try:
        import csv
        ip = os.path.join(ICONS, f'{item}.png')
        if os.path.exists(ip):
            ic = Image.open(ip).convert('RGBA')
    except Exception:
        ic = None
    out = Image.new('RGBA', (width + (isz + 16 if ic else 0), max(h, isz)), (0, 0, 0, 0))
    if ic:
        ic = ic.resize((isz, isz), Image.LANCZOS)
        fr = Image.new('RGBA', (isz + 8, isz + 8), (200, 180, 120, 255))
        fr.alpha_composite(ic, (4, 4))
        out.alpha_composite(fr, (0, 0))
        out.alpha_composite(box, (isz + 16, 0))
    else:
        out.alpha_composite(box, (0, 0))
    return out


def paste(im, items, y, width=820, size=30, gap=26):
    for it in items:
        t = render(it, width, size)
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
        x = (im.width - t.width) // 2
        ImageDraw.Draw(sh).rounded_rectangle((x + 10, y + 14, x + t.width + 10, y + t.height + 14), 16, fill=(0, 0, 0, 200))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
        im.alpha_composite(t, (x, y))
        y += t.height + gap
    return y


if __name__ == '__main__':
    import sys
    ids = [int(a) for a in sys.argv[1:]] or [276895]
    for i in ids:
        render(i).save(os.path.join(CACHE, f'{i}.png'))
        print(i, [''.join(t for t, *_ in l) + (' | ' + ''.join(t for t, *_ in r) if r else '') for l, r in lines(i)[1]])
