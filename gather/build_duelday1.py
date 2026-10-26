# -*- coding: utf-8 -*-
"""Short: Forever Open day 1 recap (18/10/2026): Raider.IO standings + news. Plan in plan_duelday1.py.

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

KIND = 'duelday1'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - Forever Open day 1 recap (EN).mp4'
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

GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)
HG = (150, 40, 30, 255)

DUEL1 = [
    (card('hook', 'THE FOREVER OPEN  ·  DAY 1', '$100K DUELS: RECAP', GOLDC, GOLDG, [],
          [('Sodapoppin goes 6-0', AMBER, 48), ('NoHitJerome DISQUALIFIED', RED, 52), ('the favorites, the tiebreaker rage', BONE, 40),
           ('before tonight’s finals', SICK, 42)], size=104),
     'vault', 'Day one of the hundred thousand dollar Forever Open is over. Sodapoppin went undefeated, NohitJerome got disqualified, '
              'and the tiebreaker made a lot of people angry. Here is everything, before the finals.', 9.0),
    (card('numbers', 'THE QUALIFIERS', '1,380 DUELISTS', GOLDC, GOLDG, [],
          [('48 pods  ·  6 Swiss rounds', BONE, 46), ('only the top 4 of each class go through', AMBER, 40),
           ('36 finalists out of 1,380', SICK, 46)], size=120),
     'vault', 'One thousand three hundred eighty players checked in, split into forty eight pods for six Swiss rounds. '
              'Only the top four of each class went through: thirty six finalists.', 9.0),
    (card('meta', 'CLASS BY CLASS', 'WHO DOMINATED', SHADOW, (90, 40, 150, 255), [],
          [('most players: Hunter 241, Shaman 217, Priest 201', BONE, 36),
           ('fewest: Warrior 80, Mage 89', BONE, 38),
           ('Paladin, Priest, Warlock: all 4 finalists 6-0', AMBER, 38),
           ('Warrior: no undefeated finalist at all', RED, 40)], size=110),
     'vault', 'Class by class: hunters were the most popular, warriors the least. Paladins, priests and warlocks were brutal: '
              'all four finalists of each went six and oh. Warriors are the only class with no undefeated player.', 10.0),
    (card('soda', 'THE BIG SURPRISE', 'SODAPOPPIN 6-0', NATURE, (40, 110, 40, 255), [],
          [('#1 druid of the whole qualifier', AMBER, 44), ('undefeated: 6 wins, 0 losses', BONE, 44),
           ('the same streamer who found druid', GREY, 38), ('"so bad" in Forever', GREY, 38)], size=120),
     'vault', 'The biggest surprise: Sodapoppin finished first among all druids, six wins, zero losses. '
              'The same streamer who said druid felt terrible in Forever.', 8.5),
    (card('favs', 'THE FAVORITES', 'THEY DELIVERED', GOLDC, GOLDG, [],
          [('Cdew: #1 shaman, 6-0', AMBER, 44), ('he wanted scrolls banned before the event', GREY, 36),
           ('Venruki: mage finalist, 5-1', BONE, 42), ('Pshero: rogue, 6-0', BONE, 42), ('Korleone: warlock, 6-0', BONE, 42)], size=120),
     'vault', 'The favorites delivered: Cdew, number one shaman, six and oh, after asking for scrolls to be banned. '
              'Venruki made it as a mage at five and one, and Pshero and Korleone went perfect on rogue and warlock.', 9.5),
    (card('jerome', 'DRAMA #1', 'NOHITJEROME DISQUALIFIED', RED, HG, [],
          [('vs Savix: left the duel zone at low health', BONE, 38), ('then cast Psychic Scream', BONE, 40),
           ('ruled a forfeit, then DISQUALIFIED', AMBER, 42), ('later: "I said those things', GREY, 36),
           ('in the heat of the moment, I’m sorry"', GREY, 36)], size=110),
     'vault', 'Drama number one: NohitJerome, against Savix, left the duel zone at low health and cast Psychic Scream. '
              'The admins ruled a forfeit, he disputed it, and he was disqualified. He later apologized on X.', 10.5),
    (card('buch', 'DRAMA #2', 'THE TIEBREAKER RAGE', RED, HG, [],
          [('5-1 players eliminated by "Buchholz"', BONE, 40), ('= the strength of the opponents you faced', AMBER, 36),
           ('a hard pod could knock you out', BONE, 40), ('plus the gold and consumables debate:', GREY, 36),
           ('"biggest bag or best duelist?"', GREY, 38)], size=110),
     'vault', 'Drama number two: many five and one players were eliminated by the Buchholz tiebreaker, which counts how strong your opponents were. '
              'A hard pod could knock you out. Add the endless debate on gold and consumables: biggest bag or best duelist?', 10.5),
    (card('final', 'TONIGHT  ·  THE FINALS', 'HYJAL CRATER', GOLDC, GOLDG, [],
          [('Blizzard built a dueling arena for it', BONE, 40), ('the same "Hyjal Crater" I datamined', SICK, 40),
           ('in build 70450 yesterday', SICK, 40), ('36 players, double elimination', BONE, 40),
           ('$50,000 champion  ·  $5,555 per class', AMBER, 38)], size=120),
     'vault', 'Tonight, the finals move to a dueling arena Blizzard built in Hyjal Crater. The same Hyjal Crater I found in the newest build yesterday. '
              'Thirty six players, double elimination, fifty thousand dollars for the champion.', 10.0),
    (card('outro', 'YOUR PICK', 'WHO WINS $50K?', GOLDC, GOLDG, [],
          [('a paladin? a warlock? Sodapoppin?', AMBER, 42), ('follow for the results', SICK, 44)], size=110),
     'emeralddream', 'So who wins the fifty thousand? A paladin, a warlock, or Sodapoppin? Tell me, and follow for the results.', 6.5),
]

PLAN = DUEL1
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
