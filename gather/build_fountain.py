# -*- coding: utf-8 -*-
"""Short: wishing fountain coins for WoW Forever (build 1.60.1.70170, 02/10/2026).

    py -3.11 build_bfd.py

Quests, givers and rewards: Wowhead Forever (zone 719). Item spots: long-standing Wowhead comments.
Backdrop: LoadScreenBlackFathomDeeps (FDID 131823, via wago.tools, unstretched to 4:3). Maps: BlackFathomDeeps1/2 world map art from the client, pins on its skull markers.
"""
import os
import sys

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title, pill
from build_whimsy import line
import build_hyjal as HY

KIND = 'fountain'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - the wishing fountain coins (EN).mp4'
GREY = (200, 200, 190, 235)
NATURE = (140, 225, 110, 255)
SHADOW = (190, 130, 255, 255)
AMBER = (255, 190, 80, 255)
RED = (235, 90, 80, 255)
TEAL = (120, 230, 200, 255)
GLOW = (60, 140, 60, 255)


def head(im, kicker, big, col, glow, y=170, size=110):
    y = title(im, kicker, y, 44, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
    return title(im, big, y + 14, size, fill=col, spacing=6, glow=glow)


def card(name, kicker, big, col, glow, icons, rows, size=110, isz=120, cy=900):
    """Generic card: kicker + title, icon row, then lines [(text, colour, font size)]."""
    def fn():
        im = blank()
        B.backdrop(im, cy, 800, 760, 185)
        y = head(im, kicker, big, col, glow, y=300, size=size)
        if icons:
            y = HY.icon_row(im, icons, y + 60, int(isz * 1.3), gap=28)
        for t, c, s in rows:
            if t.startswith('>'):
                s = int(s * 1.22)
                y = pill(im, t[1:], y + 30, B.GEORGIA_I, s, c, h=s + 50)
            else:
                y = line(im, t, y + 16, int(s * 1.22), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


def outro_png():
    im = blank()
    B.backdrop(im, 860, 740, 520, 185)
    y = title(im, 'LIKE + FOLLOW', 660, 100, fill=BONE, spacing=8)
    y = line(im, 'more WoW Forever dungeon guides', y + 40, 50, SICK)
    line(im, 'beta files  ·  may still change', y + 16, 40, GREY)
    return save(im, WORK, 'outro')


from build_whimsy import map_card
import build_cozy as C
C.WORK = WORK
BLUE = (110, 170, 255, 255)
PIN = (255, 190, 80, 255)
HORDE = (235, 90, 80, 255)
ALLI = (110, 170, 255, 255)
SEA = (90, 200, 220, 255)
SEAG = (20, 90, 110, 255)


def mcard(name, kicker, big, col, glow, zone, pts, rows, zoom=None, mw=760, size=110):
    """Card with a zone/dungeon map and pins, then lines."""
    def fn():
        im = blank()
        B.backdrop(im, 900, 800, 760, 185)
        y = head(im, kicker, big, col, glow, y=250, size=size)
        y = map_card(im, C.zmap(zone, pts, mw, zoom=zoom), y + 40)
        for t, c, s in rows:
            y = line(im, t, y + 16, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


import tooltip as TT
VIO = (190, 140, 255, 255)
VIOG = (90, 40, 160, 255)
GOLDC = (255, 210, 90, 255)
SILV = (215, 220, 235, 255)
COPP = (225, 140, 90, 255)
GOLDS = [286279, 286280, 286281, 286283, 286284, 286287, 286288, 286290, 286291, 286292, 286293, 286294, 286298, 286299, 286300, 286302, 286327]
SILVERS = [286263, 286264, 286265, 286266, 286267, 286268, 286270, 286271, 286272, 286273, 286274, 286275, 286328]
COPPERS = [286304, 286306, 286307, 286308, 286309, 286310, 286311, 286312, 286313, 286314, 286315, 286316, 286317, 286318]


def tcard(name, kicker, big, col, glow, items, rows, size=110, tsize=40, twidth=900):
    """One coin: real in-game tooltip, big, then a short line."""
    def fn():
        im = blank()
        B.backdrop(im, 880, 760, 640, 185)
        y = head(im, kicker, big, col, glow, y=470, size=size)
        y = TT.paste(im, items, y + 50, width=twidth, size=tsize, gap=18)
        for t, c, s in rows:
            y = line(im, t, y + 10, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


def grid_png():
    im = blank()
    B.backdrop(im, 900, 860, 820, 185)
    y = head(im, 'IN THE GAME FILES', '44 WISHING COINS', GOLDC, (200, 140, 40, 255), y=290, size=110)
    for label, ids, col in (('17 GOLD', GOLDS, GOLDC), ('13 SILVER', SILVERS, SILV), ('14 COPPER', COPPERS, COPP)):
        y = line(im, label, y + 30, 50, col)
        per = 9
        for r in range(0, len(ids), per):
            row = ids[r:r + per]
            y = HY.icon_row(im, row, y + 14, 84, gap=12) - 4
    line(im, 'every coin = a famous character\'s wish', y + 34, 46, BONE)
    return save(im, WORK, 'grid')


def coin(name, cid, who, say, col=GOLDC, dur=6.0, note=None):
    rows = [(note, SICK, 44)] if note else []
    return (tcard(name, 'WISHING COIN', who, col, (120, 90, 20, 255), [cid], rows),
            'dalaran', say, dur)


import json as _json
import re as _re
_C = {int(k): v for k, v in _json.load(open(os.path.join(HERE, 'coins.json'), encoding='utf-8')).items()}
NOTES = {286287: 'the future lich just wants a hug', 286281: '"frozen"... foreshadowing?',
         286279: 'a jab at Anduin staying a kid since 2004', 286293: 'he flattened Dalaran. The fountain survived.',
         286273: 'some things never change', 286267: 'a secret crush on High General Abbendis',
         286311: 'a nod to his novel appearances', 286300: "Forever's own raid boss is confused",
         286290: 'Onyxia in disguise', 286302: 'caught in the act', 286327: 'a nod to the Caverns of Time',
         286274: 'the three tones of the Karazhan bells?', 286328: "who copied who's fountain?"}
INTRO = {286290: 'Lady Katrana Prestor, Onyxia in disguise', 286281: 'Arthas, before the fall', 286300: 'Sonya Darkhallow, the Barrow Deeps boss',
         286291: 'Sylvanas, long ago', 286267: 'Arcanist Doan, of the Scarlet Monastery', 286308: 'Attumen the Huntsman'}
# gold first (Kel'Thuzad opens), then silver, copper; the two sad ones close the list
_ORDER = ([286287] + [i for i in GOLDS if i not in (286287, 286291, 286288)] + SILVERS + COPPERS + [286291, 286288])


def _who(i):
    n = _re.sub(r"'s? (Gold|Silver|Copper) Coin$", '', _C[i][0])
    return n.replace("A Footman", 'A Footman')


def _spoken(t):
    t = t.replace('<', '').replace('>', '')
    return t


ALL_COINS = []
for _i in _ORDER:
    _name, _wish = _C[_i]
    _who_ = _who(_i)
    _col = GOLDC if 'Gold' in _name else (SILV if 'Silver' in _name else COPP)
    _intro = INTRO.get(_i, _who_)
    _say = '%s: %s' % (_intro, _spoken(_wish))
    _dur = 4.2
    ALL_COINS.append(coin('c%d' % _i, _i, _who_.upper(), _say, col=_col, dur=_dur, note=NOTES.get(_i)))


FOUNT = [
    (card('hook', 'WOW FOREVER  ·  HIDDEN IN THE FILES', 'THE WISHING FOUNTAIN', GOLDC, (200, 140, 40, 255), [286287, 286281, 286279],
          [("44 coins tossed by Warcraft's biggest names", BONE, 48), ('each one carries a secret wish', AMBER, 48),
           ('some are... unexpected', SICK, 46)], size=100, isz=150),
     'dalaran', "WoW Forever has a wishing fountain, and the game files hold forty four coins. Each one carries the wish of a famous Warcraft character. Some are unexpected.", 6.0),
    (grid_png, 'dalaran', 'Seventeen gold coins, thirteen silver and fourteen copper. Here is every single wish.', 6.0),
    *ALL_COINS,
    (tcard('lucky', 'HOW IT WORKS', 'SHINY SILVER COIN', SILV, (90, 100, 130, 255), [286732],
           [('toss a lucky coin in the water: +30 Fishing', AMBER, 42), ('11 hidden coin spots in the files', BONE, 42),
            ('fish the wishes back up?', SICK, 44)], size=100),
     'dalaran', 'How do you get them? A Shiny Silver Coin raises your fishing when you toss it into the water, and the files hide eleven coin spots. '
                'Just like the Dalaran fountain in Wrath, you will probably fish them up.', 8.0),
    (card('outro', 'WHICH ONE IS YOUR FAVORITE?', 'TELL ME BELOW', GOLDC, (200, 140, 40, 255), [286287, 286273, 286293, 286300],
          [('beta files  ·  may still change', GREY, 40), ('follow for more WoW Forever secrets', SICK, 46)], size=120, isz=130),
     'dalaran', 'Which wish is your favorite? Tell me in the comments, and follow for more WoW Forever secrets.', 5.0),
]


PLAN = FOUNT
MUSIC = 'mage'


def main():
    files, tl, say, t = [], [], [], 0.0
    for i, (fn, art, text, mind) in enumerate(PLAN):
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        files.append(BP.shot(WORK, i, art, dur, seed=34 if i in (0, len(PLAN) - 1) else i * 37 + 23,
                             bright=0.0 if i == 0 else -0.14))
        say.append((t + BP.LEAD, wav)); tl.append((t, dur)); t += dur
    total = t

    frame = BP.frame_png(WORK)
    finals = []
    for i, (fn, *_ ) in enumerate(PLAN):
        a, d = tl[i]
        card_png = fn()
        fi, fo = (0.0, 0.15) if i == 0 else ((0.35, 0.0) if i == len(PLAN) - 1 else (0.25, 0.16))
        ch = '[2:v]format=rgba'
        if fi: ch += f',fade=t=in:st=0.1:d={fi}:alpha=1'
        if fo: ch += f',fade=t=out:st={max(0, d - fo):.3f}:d={fo}:alpha=1'
        tail = f',fade=t=out:st={d - 0.8:.3f}:d=0.8' if i == len(PLAN) - 1 else ''
        out = os.path.join(WORK, f'final_{i:02d}.mp4')
        run([FF, '-v', 'error', '-y', '-i', files[i],
             '-loop', '1', '-framerate', str(FPS), '-t', f'{d:.3f}', '-i', frame,
             '-loop', '1', '-framerate', str(FPS), '-t', f'{d:.3f}', '-i', card_png,
             '-filter_complex', f'[0:v]setsar=1[b];[1:v]format=rgba[f];[b][f]overlay=format=auto[bf];{ch}[c];'
                                f'[bf][c]overlay=format=auto{tail},format=yuv420p,setsar=1[v]',
             '-map', '[v]', '-an', '-t', f'{d:.3f}', '-r', str(FPS),
             '-c:v', 'h264_nvenc', '-preset', 'p7', '-tune', 'hq', '-rc', 'vbr', '-cq', '22', '-b:v', '0',
             '-maxrate', '13M', '-bufsize', '26M', out])
        finals.append(out)

    lst = os.path.join(WORK, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p.replace(os.sep, '/')}'\n" for p in finals))
    base = os.path.join(WORK, 'base.mp4')
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base])
    audio = BP.mix_audio(WORK, MUSIC, total, say)
    run([FF, '-v', 'error', '-y', '-i', base, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', f'{total:.3f}', OUT])
    for i, (a, d) in enumerate(tl):
        print(f'{i} {a:6.2f} +{d:5.2f}')
    import watermark
    watermark.apply(OUT, center=(540, 1730))
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
