# -*- coding: utf-8 -*-
"""Short: one week of WoW Forever beta left (14/10/2026). Plan in plan_betaend.py.

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

KIND = 'betaend'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - one week of beta left (EN).mp4'
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


GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)
EPIC = (190, 120, 255, 255)
EPICG = (100, 40, 170, 255)

BETA = [
    (card('hook', 'WOW FOREVER BETA', '7 DAYS LEFT', AMBER, GOLDG, [],
          [('last full day: October 21', AMBER, 52), ('then every character is deleted', BONE, 46),
           ('what to do before it ends', SICK, 46)], size=140),
     'emeralddream', 'Only one week left in the WoW Forever beta. The last full day of testing is October twenty first, '
                     'then every character gets deleted. Here is what to do before it ends.', 6.5),
    (card('wipe', 'THE FULL WIPE', 'NOTHING CARRIES OVER', RED, (150, 40, 30, 255), [],
          [('levels, gold and gear: gone', BONE, 46), ('professions + Legacy Points: gone', BONE, 44),
           ('beta names are not kept', BONE, 44), ('only your knowledge stays', SICK, 48)], size=110),
     'emeralddream', 'Nothing carries over. Levels, gold, gear, professions and Legacy Points are all wiped, '
                     'and your beta name is not kept. The only thing you keep is what you learned.', 7.0),
    (card('todo', 'BEFORE OCTOBER 21', 'LAST THINGS TO DO', GOLDC, GOLDG, [],
          [('try every class you hesitate on', BONE, 44), ('run the new dungeons:', BONE, 44),
           ('Hall of Thanes  ·  Ruins of Lordaeron', AMBER, 40), ('Excavation Site', AMBER, 40),
           ('practice your leveling route', BONE, 44), ('report every bug you find', SICK, 44)], size=110),
     'emeralddream', 'Before it ends: try every class you are hesitating on, run the new dungeons like Hall of Thanes, '
                     'Ruins of Lordaeron and the Excavation Site, practice your leveling route, and report every bug you find.', 8.0),
    (card('open', 'THIS WEEKEND', 'THE FOREVER OPEN', GOLDC, GOLDG, [],
          [('$100,000 in level 30 duels', AMBER, 50), ('October 17 + 18', BONE, 48), ('streamed by Esfand + Xaryu', BONE, 44)], size=120),
     'emeralddream', 'And this weekend: the hundred thousand dollar Forever Open, level thirty duels on October seventeenth and eighteenth.', 6.0),
    (card('next', 'WHAT COMES NEXT', 'THE ROAD TO LAUNCH', EPIC, EPICG, [],
          [('Oct 27 - Nov 3: reserve up to 3 names', BONE, 42), ('first come, first served', AMBER, 44),
           ('(eligible edition required)', GREY, 36), ('Nov 4, 3 PM PST: launch', SICK, 50), ('Dec 9: the first 3 raids', BONE, 44)], size=110),
     'emeralddream', 'Then from October twenty seventh to November third, you can reserve up to three character names, '
                     'first come, first served. Launch is November fourth at three PM Pacific, and the first raids open December ninth.', 9.0),
    (card('outro', 'NOVEMBER 4', 'WHAT IS YOUR MAIN?', EPIC, EPICG, [],
          [('tell me your launch main in the comments', AMBER, 42), ('follow for every Forever update', SICK, 44)], size=110),
     'emeralddream', 'So, what is your main at launch? Tell me in the comments, and follow for every Forever update.', 5.5),
]


PLAN = BETA
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
