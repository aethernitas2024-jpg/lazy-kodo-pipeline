# -*- coding: utf-8 -*-
"""Short: Datamined mounts + Blizzard's answer (18/10/2026). Plan in plan_mounts.py.

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

KIND = 'mounts'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - new mounts datamined (EN).mp4'
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
SPEC = (140, 220, 255, 255)
SPECG = (30, 100, 150, 255)

MOUNTS = [
    (card('hook', 'WOW FOREVER  ·  DATAMINE', 'NEW MOUNTS', SPEC, SPECG, ['m_wolf', 'm_rooster', 'm_turtle'],
          [('the newest ones were just decrypted', BONE, 42), ('and Blizzard already answered', AMBER, 44),
           ('+ every Forever mount we know', SICK, 42)], size=130, isz=130),
     'vault', 'New mounts were just decrypted in the WoW Forever beta, and Blizzard already answered. '
              'Here is what they are, and every Forever mount we know about.', 8.0),
    (card('new', 'DECRYPTED  ·  OCTOBER 15-16', 'THE LATEST THREE', SPEC, SPECG, ['m_wolf', 'm_turtle', 'm_rooster'],
          [('Spectral Wolf Pack', AMBER, 48), ('two ghost wolves run beside you', BONE, 38),
           ('party members can join the pack (reported)', GREY, 34),
           ('Verdant Sea Turtle', AMBER, 46), ('Crimson Rooster', AMBER, 46)], size=110, isz=120),
     'vault', 'The latest three: the Spectral Wolf Pack, where two ghost wolves run beside you, and party members could reportedly join your pack. '
              'Plus a Verdant Sea Turtle, and a Crimson Rooster.', 10.0),
    (card('blizz', "BLIZZARD'S ANSWER", 'NOT FOR FOREVER', RED, (150, 40, 30, 255), [],
          [('"these assets are not intended', BONE, 42), ('for this version of World of Warcraft"', BONE, 42),
           ('so where do they go?', AMBER, 44), ('retail, or the Chinese version?', BONE, 40),
           ('the turtle looks like a statue shown in China', GREY, 34)], size=110),
     'vault', 'But Blizzard answered on the forums: these assets are not intended for this version of World of Warcraft. '
              'So where do they go? Maybe retail, maybe the Chinese version: the turtle looks a lot like a statue shown at an event in China.', 10.5),
    (card('confirmed', 'IN FOREVER  ·  WITH A SOURCE', 'THE REAL ONES', GOLDC, GOLDG, ['m_galestrider', 'm_prideclaw', 'm_bear', 'm_kodo'],
          [('Skyborne Galestriders: 4 at level 40, 4 swift at 60', BONE, 34), ('Cerulean Prideclaw: pre-order reward', BONE, 36),
           ('Spectral Bear: Legacy system reward', BONE, 36), ('Pack Kodo: faction supply reward', BONE, 36),
           ('new kodo and skeletal horse colors', BONE, 36), ('Forsaken Charger: undead paladins', AMBER, 36)], size=110, isz=110),
     'vault', 'The ones that really are in Forever: eight Skyborne Galestriders, four at level forty and four swift ones at sixty. '
              'The Cerulean Prideclaw from the pre-order, the Spectral Bear from the Legacy system, the Pack Kodo from faction supplies, '
              'new kodo and skeletal horse colors, and the Forsaken Charger for undead paladins.', 13.0),
    (card('mystery', 'STILL IN THE FILES  ·  NO SOURCE', 'THE MYSTERIES', SHADOW, (90, 40, 150, 255), [],
          [('5 Devilsaurs  ·  4 Warden Sabers', BONE, 42), ('4 Druid Moose  ·  Swift Hyjal Stag', BONE, 42),
           ('Striped Dawnsaber', BONE, 42), ('+ 15 mount items still encrypted', SICK, 42), ('in build 70450 (my datamine)', SICK, 36)], size=110),
     'vault', 'And the mysteries, still in the files with no source: five devilsaurs, four warden sabers, four druid moose, a Swift Hyjal Stag. '
              'And in build seventy four fifty, I count fifteen mount items whose names are still encrypted.', 10.0),
    (card('outro', 'YOUR PICK', 'WHICH ONE DO YOU WANT?', SPEC, SPECG, ['m_wolf', 'm_galestrider', 'm_turtle'],
          [('should Blizzard add the wolf pack?', AMBER, 42), ('follow for every Forever datamine', SICK, 42)], size=96, isz=110),
     'emeralddream', 'Which one do you want? Should Blizzard bring the wolf pack to Forever anyway? Tell me, and follow for every Forever datamine.', 7.0),
]

PLAN = MOUNTS
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
