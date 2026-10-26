# -*- coding: utf-8 -*-
"""Short: WoW Forever stress test feedback (22/10/2026). Plan in plan_stress.py.

    py -3.11 build_stress.py

Sources: Mein-MMO live ticker, Blizzard forum threads (21-22/10).
Backdrop 'stress': the user's own stress test screenshot (Camp Narache, 21/10 23:16), cropped into load/tall_stress.jpg.
"""
import os
import sys

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title, pill
from build_whimsy import line
import build_hyjal as HY

KIND = 'stress'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - stress test feedback (EN).mp4'
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


GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)
HG = (150, 40, 30, 255)
BLUE = (120, 190, 255, 255)
BLUEG = (30, 80, 150, 255)

STRESS = [
    (card('hook', 'WOW FOREVER  ·  THE STRESS TEST', 'HOW DID IT GO?', BLUE, BLUEG, [],
          [('a rough first hour', RED, 46), ('then surprisingly smooth', SICK, 46),
           ('the good, the bad, and November 4', BONE, 40)], size=110),
     'stress', 'Last night, anyone could play WoW Forever for free in the stress test. So how did it go? '
               'A rough first hour, then surprisingly smooth. Here is the good, the bad, and what it means for launch.', 9.0),
    (card('start', 'THE FIRST HOUR', 'NO REALMS', RED, HG, [],
          [('"realm types not available"', BONE, 44), ('error after error at 7 PM Paris', BONE, 40),
           ('some waited almost an hour', AMBER, 42), ('to get into the game', AMBER, 42)], size=120),
     'stress', 'The start was rough. At seven PM Paris time, many players got realm types not available, error after error. '
               'Some waited almost an hour before getting in.', 9.0),
    (card('smooth', 'AFTER THAT', 'NO QUEUES', SICK, (40, 110, 40, 255), [],
          [('around 100 FPS, no stutter', BONE, 42), ('packed starting zones', BONE, 42),
           ('Camp Narache, last night (my screenshot)', GREY, 34), ('about 8 hours of play, until 3 AM Paris', AMBER, 38)], size=120),
     'stress', 'But after that? No queues, high frame rates, and packed starting zones. This is Camp Narache last night. '
               'The test ran for about eight hours, until three AM Paris time.', 9.5),
    (card('broke', 'WHAT BROKE', 'NOT PERFECT', RED, HG, [],
          [('chain disconnects for some players', BONE, 40), ('NPCs not loading, slow quest turn-ins', BONE, 38),
           ('mobs vanishing mid-fight', BONE, 40), ('"jumping shadows" leaving Durotar', BONE, 38),
           ('devs crashed services on purpose', AMBER, 40)], size=120),
     'stress', 'It was not perfect. Some players got chain disconnects, N P Cs not loading, and very slow quest turn-ins. '
               'Mobs vanished mid-fight, shadows jumped around, and the devs even crashed some background services on purpose.', 10.5),
    (card('layers', 'THE BIG DEBATE', 'LAYERING', SHADOW, (90, 40, 150, 255), [],
          [('some were alone in Elwynn Forest', BONE, 40), ('others stuck in a laggy Stormwind', BONE, 40),
           ('"too empty" and "too crowded"', AMBER, 42), ('at the same time', AMBER, 42),
           ('a PvP realm overloaded by a streamer guild?', GREY, 34)], size=120),
     'stress', 'The big debate: layering. Some players were alone in Elwynn Forest, others stuck in a laggy Stormwind. '
               'Too empty and too crowded, at the same time. And players say a streamer guild overloaded an Alliance PvP realm.', 10.5),
    (card('end', 'THE LAST MINUTES', 'EVERYTHING VANISHED', GOLDC, GOLDG, [],
          [('around 3 AM, every NPC disappeared', BONE, 40), ('players danced in Goldshire', BONE, 42),
           ('and dueled until the end', BONE, 42), ('stress test characters are deleted', GREY, 36)], size=104),
     'stress', 'The ending was very World of Warcraft: around three AM, every N P C disappeared, '
               'and players just danced in Goldshire and dueled until the servers closed.', 8.5),
    (card('next', 'WHAT’S NEXT', 'NOVEMBER 4', GOLDC, GOLDG, [],
          [('beta extended: until Friday Oct 23', SICK, 42), ('10 AM PDT  ·  7 PM Paris', BONE, 40),
           ('name reservation: Oct 27 - Nov 3', AMBER, 40), ('launch: November 4', AMBER, 44)], size=120),
     'vault', 'What is next? The beta is extended until Friday, October twenty third, seven PM Paris. '
              'Name reservation runs from October twenty seventh to November third, and launch is November fourth.', 9.5),
    (card('outro', 'YOUR VERDICT', 'READY FOR LAUNCH?', BLUE, BLUEG, [],
          [('did you get in? smooth or broken?', AMBER, 42), ('follow for everything Forever', SICK, 42)], size=104),
     'emeralddream', 'So, is Forever ready for launch? Did you get in, and was it smooth or broken for you? Tell me, and follow for everything Forever.', 7.0),
]

PLAN = STRESS
MUSIC = 'hyjal'



def main():
    files, tl, say, t = [], [], [], 0.0
    for i, (fn, art, text, mind) in enumerate(PLAN):
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        files.append(BP.shot(WORK, i, art, dur, seed=34 if i in (0, len(PLAN) - 1) else i * 37 + 23,
                             bright=0.13 if art == 'stress' else -0.14))   # the screenshot read too dark at -0.14 (user, 22/10)
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
