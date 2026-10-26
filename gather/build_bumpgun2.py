# -*- coding: utf-8 -*-
"""Short: the Booty Bay Bruiser's Buckshot knockback gun in WoW Forever (06/10/2026).

    py -3.11 build_bumpgun2.py

Item 274748 (nether tooltip), vendor Gezzy Gunkgear npc 265575 at Stranglethorn 28.2,74.8, cost 31088 copper.
Spell 1295313 (client 70205): Effect 98 knockback, base 50 / misc 400, ImplicitTarget 25 (any unit), range 10-40, CD 600000.
Works on allies + slow fall trick: Wowhead comment (said as player report).
"""
import os
import sys

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title, pill
from build_whimsy import line
import build_hyjal as HY

KIND = 'bumpgun2'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - RIP Booty Bay bump gun, hotfixed (EN).mp4'
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
    y = line(im, 'more WoW Forever guides every week', y + 40, 50, SICK)
    line(im, 'beta files  ·  may still change', y + 16, 40, GREY)
    return save(im, WORK, 'outro')


from build_whimsy import map_card
import build_cozy as C
C.WORK = WORK
PIN = (255, 190, 80, 255)
HORDE = (235, 90, 80, 255)
ALLI = (110, 170, 255, 255)
BOTH = (140, 225, 110, 255)
BLUEQ = (60, 140, 255, 255)


def mcard(name, kicker, big, col, glow, zone, pts, rows, zoom=None, mw=760, size=110):
    """Card with a zone map and pins, then lines."""
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


def tcard(name, kicker, big, col, glow, items, rows, size=110, tsize=38, twidth=880):
    """Card with real in-game tooltips (stats from Wowhead Forever), then short lines."""
    def fn():
        im = blank()
        B.backdrop(im, 900, 820, 800, 185)
        y = head(im, kicker, big, col, glow, y=250, size=size)
        y = TT.paste(im, items, y + 40, width=twidth, size=tsize, gap=22)
        for t, c, s in rows:
            y = line(im, t, y + 4, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


GOLDC = (255, 205, 90, 255)
GOLDG = (200, 120, 40, 255)

GUN = [
    (card('hook', 'WOW FOREVER  ·  HOTFIXED', 'R.I.P. BUMP GUN', RED, (150, 40, 30, 255), [135611],
          [('the Booty Bay gun that sent', BONE, 50), ('targets FLYING...', AMBER, 56),
           ('lasted about one day', SICK, 48)], size=140, isz=190),
     'eastern_kingdoms', 'Rest in peace, Booty Bay bump gun. It sent targets flying, and it lasted about one day.', 5.0),
    (tcard('before', 'BEFORE', 'THE BUMP', GOLDC, GOLDG, ['274748'],
           [('knocked any target away... even your allies', AMBER, 42)], size=150),
     'eastern_kingdoms', 'Before: a level thirty gun with an on use shot that knocked any target away. Even your own allies.', 5.5),
    (tcard('after', 'NOW', 'JUST A GUN', RED, (150, 40, 30, 255), ['274748_new'],
           [('the knockback is gone: server-side hotfix', BONE, 42), ('(the spell is still in the game files)', GREY, 38)], size=150),
     'eastern_kingdoms', 'Now: the knockback is gone. A server side hotfix. The spell is still in the game files, just no longer on the gun.', 6.0),
    (card('why', 'WHY?  ·  OUR GUESS', 'TOO MUCH FUN', AMBER, GOLDG, [],
          [('players launched their friends', BONE, 48), ('Slow Fall mid-air = across the zone', BONE, 44),
           ('and on Hardcore, a cliff means game over', SICK, 44)], size=150),
     'eastern_kingdoms', 'Why? Blizzard did not say. Our guess: players were launching their friends across the zone, and on Hardcore, a cliff means game over.', 6.0),
    (card('vote', 'YOUR CALL', 'FAIR NERF?', GOLDC, GOLDG, [135611],
          [('good call by Blizzard...', BONE, 50), ('... or should they let us have fun?', AMBER, 50),
           ('tell me in the comments', SICK, 48)], size=170, isz=150),
     'eastern_kingdoms', 'So, your call: good call by Blizzard, or should they let us have fun? Tell me in the comments.', 6.0),
]


PLAN = GUN
MUSIC = 'hunter'


def main():
    files, tl, say, t = [], [], [], 0.0
    for i, (fn, art, text, mind) in enumerate(PLAN):
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        files.append(BP.shot(WORK, i, art, dur, seed=i * 31 + 17,
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
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
