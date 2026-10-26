# -*- coding: utf-8 -*-
"""Short: 72 items silently nerfed for WoW Forever (build 1.60.1.70170, 02/10/2026).

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

KIND = 'nerf72'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - 72 items silently nerfed (EN).mp4'
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
import oldstats as OS
BLUEQ = (0, 112, 221, 255)
GREENQ = (30, 255, 0, 255)
NERF72 = [int(x) for x in open(os.path.join(HERE, 'nerf72.txt')).read().split()]


def bacard(name, iid, big, rows=()):
    """Before (blue, recomputed) above after (green, live Wowhead) tooltip."""
    key, rep = OS.make_old(iid)

    def fn():
        im = blank()
        B.backdrop(im, 900, 840, 820, 185)
        y = head(im, 'SILENT NERF', big, RED, (150, 40, 30, 255), y=200, size=96)
        y = line(im, 'BEFORE', y + 26, 46, BLUEQ)
        y = TT.paste(im, [key], y + 8, width=860, size=32, gap=10)
        y = line(im, 'NOW', y + 10, 46, GREENQ)
        y = TT.paste(im, [iid], y + 8, width=860, size=32, gap=10)
        for t, c, s in rows:
            y = line(im, t, y + 6, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn, rep


def grid_png():
    im = blank()
    B.backdrop(im, 900, 860, 860, 185)
    y = head(im, 'SERVER HOTFIX', '72 BLUES TURNED GREEN', RED, (150, 40, 30, 255), y=250, size=96)
    per = 8
    for r in range(0, len(NERF72), per):
        y = HY.icon_row(im, NERF72[r:r + per], y + (30 if r == 0 else 6), 86, gap=10) - 4
    line(im, 'same item level  ·  less stats  ·  less damage', y + 34, 44, AMBER)
    return save(im, WORK, 'grid')


def ba(name, iid, big, say, rows=(), dur=7.0):
    fn, rep = bacard(name, iid, big, rows)
    return (fn, 'eastern_kingdoms', say, dur)


NERF = [
    (card('hook', 'WOW FOREVER  ·  BETA', 'SILENTLY NERFED', RED, (150, 40, 30, 255), [6804, 17042, 17043],
          [('72 items dropped from blue to green', BONE, 50), ('same item level, weaker stats', AMBER, 48),
           ('pushed by a server hotfix', SICK, 46)], size=110, isz=150),
     'eastern_kingdoms', 'WoW Forever just silently nerfed seventy two items. Blue to green, same item level, weaker stats, pushed straight from the server.', 6.0),
    (grid_png, 'eastern_kingdoms', 'Here they all are. Drops and quest rewards from level twenty to forty two, all pushed by a server hotfix.', 7.0),
    (card('why', 'HOW IT WORKS', 'BLUE TO GREEN', AMBER, (200, 120, 40, 255), [6804, 251963],
          [('stats come from item level AND quality', BONE, 46), ('a green gets a smaller stat budget', BONE, 46),
           ('about -30% stats', RED, 54), ('weapons: about -20% DPS', RED, 54),
           ('"before" values recomputed from the', GREY, 38), ("game's own stat tables", GREY, 38)], size=120),
     'eastern_kingdoms', "Why it hurts: stats come from item level and quality. A green gets a smaller budget, so about thirty percent less stats, and weapons lose about twenty percent damage.", 7.0),
    ba('hammer', 6804, 'WINDSTORM HAMMER', 'Windstorm Hammer: from thirty eight to seventy one damage, down to thirty to fifty six. Strength and stamina, gone from five and six to three and four.', dur=8.0),
    ba('nail', 17042, 'NAIL SPITTER', 'Nail Spitter, the gun: twenty DPS down to sixteen.', dur=6.5),
    ba('zealot', 17043, "ZEALOT'S ROBE", "Zealot's Robe: spell power from fifteen to eleven, intellect and spirit from ten to seven.", dur=7.0),
    ba('cultist', 270054, "CULTIST'S CHESTGUARD", "Cultist's Chestguard: every stat loses about a third.", dur=6.5),
    ba('ursine', 270027, 'URSINE HAMMER', 'Ursine Hammer: three stats down, and the DPS from twenty two to eighteen.', dur=7.0),
    ba('monkey', 6748, 'MONKEY RING', 'Even the classic rings: Monkey Ring and Tiger Band, sevens become fives.', dur=6.5),
    ba('gravewalker', 251963, 'GRAVEWALKER BOOTS', "And the brand new City of Dalaran: the side quest rewards turned green too. Only the main quest chain stays blue.", dur=8.0),
    (card('more', 'ALSO IN THE HOTFIX', 'WHAT ELSE', AMBER, (200, 120, 40, 255), [2034, 279839, 279841],
          [('60+ more items: stats reshuffled', BONE, 44), ('24 Al\'Aketh pieces: now bind on equip', BONE, 44),
           ('one winner: Scholarly Robes, green to blue', SICK, 44), ('Dalaran main chain rewards: still blue', AMBER, 42),
           ('beta  ·  may still change', GREY, 38)], size=120, isz=130),
     'eastern_kingdoms', "Also in the hotfix: sixty more items with reshuffled stats, the Al'Aketh pieces now bind on equip, and one lucky winner, Scholarly Robes, went from green to blue.", 7.5),
    (card('outro', 'YOUR CALL', 'FAIR NERF OR TOO MUCH?', RED, (150, 40, 30, 255), [6804, 270054, 251963],
          [('tell me in the comments', BONE, 48), ('follow for every WoW Forever change', SICK, 44)], size=100, isz=130),
     'eastern_kingdoms', 'Fair nerf to slow down leveling gear, or too much? Tell me in the comments, and follow for every WoW Forever change.', 6.0),
]


PLAN = NERF
MUSIC = 'warrior'


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
