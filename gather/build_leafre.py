# -*- coding: utf-8 -*-
"""Short: Leafre's Ring of Precise Spell Power, cautious take (16/10/2026). Plan in plan_leafre.py.

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

KIND = 'leafre'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - the mystery +100 spell power ring (EN).mp4'
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


HORDE = (235, 90, 80, 255)
ALLI = (110, 170, 255, 255)

import tooltip as TT

RINGC = (190, 140, 255, 255)
RINGG = (90, 40, 150, 255)
GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)


def tcard(name, kicker, big, items, rows, col=RINGC, glow=RINGG, size=100, tsize=30, twidth=820, y0=240):
    def fn():
        im = blank()
        B.backdrop(im, 900, 820, 800, 185)
        y = head(im, kicker, big, col, glow, y=y0, size=size)
        y = TT.paste(im, items, y + 30, width=twidth, size=tsize, gap=18)
        for t, c, s in rows:
            y = line(im, t, y + 6, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


LEAFRE = [
    (tcard('hook', 'WOW FOREVER  ·  A MYSTERY RING', '+100 SPELL POWER', [276765],
           [('epic, item level 66', AMBER, 42), ('equippable at level 1', BONE, 42), ('real loot, or not?', SICK, 46)], size=104),
     'vault', "A ring with one hundred spell power, equippable at level one. It is on the WoW Forever servers. "
              "But can you actually get it? Let's look at what we really know.", 7.5),
    (card('claim', 'THE RUMOR', 'FISHED UP?', GOLDC, GOLDG, [276765],
          [('reported as an ultra-rare fishing catch', BONE, 42), ('Stormwind Stockade, low level character', BONE, 40),
           ('no drop rate, no video proof yet', AMBER, 42), ('one boosting site even sells the farm', GREY, 38)], size=110, isz=110),
     'vault', 'The rumor: it would be an ultra rare fishing catch, in the Stormwind Stockade, on a low level character. '
              'But there is no drop rate and no clear video proof yet, and one boosting site is already selling the farm.', 9.0),
    (tcard('family', 'IT HAS TWO SIBLINGS', "LEAFRE'S RINGS", [274978, 285326],
           [('item level 1, +150 to every resistance', AMBER, 38), ('armor penetration: not a Classic stat', AMBER, 38),
            ('a modern retail icon', GREY, 36)], size=100, tsize=28),
     'vault', "And it is not alone. There are two other Leafre's rings: one with one hundred fifty to every resistance at item level one, "
              "and one with armor penetration, a stat that does not even exist in Classic, with an icon from modern retail.", 10.0),
    (card('doubt', 'WHAT IT LOOKS LIKE', 'TEST GEAR?', RINGC, RINGG, [274978, 276765, 285326],
          [('stats like these are typical', BONE, 42), ('of developer testing items', BONE, 42),
           ('but nothing is confirmed', AMBER, 44), ('no word from Blizzard', GREY, 38)], size=120, isz=110),
     'vault', "Stats like these look a lot like the testing gear developers use. But nothing is confirmed either way, "
              "and Blizzard has not said a word about it.", 8.0),
    (card('known', 'WHAT WE KNOW', 'FACTS ONLY', GOLDC, GOLDG, [],
          [('it exists on the servers', SICK, 44), ('it binds when picked up', BONE, 42), ('so you can never buy it from a player', BONE, 40),
           ('nobody has shown a confirmed catch', AMBER, 42)], size=120),
     'vault', 'What we know: it exists on the servers, it binds when picked up, so no player can ever sell it to you, '
              'and nobody has shown a confirmed catch so far.', 8.0),
    (card('advice', 'MY ADVICE', 'BE CAREFUL', RED, (150, 40, 30, 255), [],
          [('do not pay anyone to farm it', AMBER, 46), ('until a real drop is confirmed', BONE, 42),
           ('fished it? show us in the comments', SICK, 44)], size=120),
     'vault', 'So be careful: do not pay anyone to farm it until a real drop is confirmed. And if you fished it, show us in the comments.', 7.0),
    (card('outro', 'YOUR TAKE', 'REAL LOOT OR TEST ITEM?', RINGC, RINGG, [276765],
          [('tell me what you think', AMBER, 44), ('follow for more Forever secrets', SICK, 42)], size=96, isz=110),
     'emeralddream', 'Real loot or test item? Tell me what you think, and follow for more Forever secrets.', 6.0),
]

PLAN = LEAFRE
MUSIC = 'hyjal'



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
