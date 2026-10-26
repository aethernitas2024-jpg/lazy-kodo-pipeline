# -*- coding: utf-8 -*-
"""Short: Forever endgame for WoW Forever (build 1.60.1.70170, 02/10/2026).

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

KIND = 'endgame'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - the endgame explained (EN).mp4'
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

END = [
    (card('hook', 'WOW FOREVER  ·  WHAT THE DEVS SAID', 'THE ENDGAME', EPIC, EPICG, [280904, 18423, 280930],
          [('raids, gear, dungeons, PvP, legacy', BONE, 46), ('everything from the latest interviews', AMBER, 44),
           ('+ what the game files add', SICK, 44)], size=130, isz=150),
     'emeralddream', 'What will you do at level sixty in WoW Forever? Here is everything the developers revealed in their latest interviews and podcast, plus what the game files add.', 7.5),
    (card('calendar', 'THE ROADMAP', 'KEY DATES', GOLDC, GOLDG, [],
          [('Nov 4: launch', BONE, 52), ('Dec 9: first 3 raids open', AMBER, 50), ('Winter: Forever Hardcore', BONE, 46),
           ('Spring 2027: 2 raids, 2 dungeons, new zone', BONE, 40), ('+ a legendary questline', SICK, 42),
           ('Summer 2027: a revamped iconic raid + a new one', BONE, 38)], size=120),
     'emeralddream', 'The key dates: launch on November fourth, the first three raids on December ninth, Hardcore in winter. Spring brings two raids, two dungeons, a new zone and a legendary questline. Summer, a revamped iconic raid.', 9.5),
    (card('tier1', 'RAID TIER 1  ·  DECEMBER 9', '3 RAIDS AT ONCE', EPIC, EPICG, [280904, 280930, 18423],
          [('Barrow Deeps: 10 players', BONE, 48), ('Hyjal Summit: 20 players', BONE, 48), ("Onyxia's Lair: 40 players", BONE, 48),
           ('"every tier: a 10-man AND a 20-man"', AMBER, 42), ('the 40-man is the exception', GREY, 40)], size=120, isz=130),
     'emeralddream', "Tier one, December ninth: Barrow Deeps for ten players, Hyjal Summit for twenty, and Onyxia's Lair for forty. Lead designer Tim Jones promised a ten and a twenty player raid every tier. The forty is the exception.", 9.5),
    (card('rules', 'HOW RAIDING WORKS', 'NO SHORTCUTS', RED, (150, 40, 30, 255), [],
          [('no flex raid sizes', BONE, 48), ('no heroic difficulty', BONE, 48), ('no automated raid finder', BONE, 48),
           ('no GDKP', RED, 54), ('build your own group', SICK, 46)], size=120),
     'emeralddream', 'And the rules: fixed raid sizes, no heroic mode, no automated raid finder, and no GDKP. You build your own group.', 8.0),
    (card('horiz', 'PAX AUSTRALIA  ·  LONGDALE + STONE', 'NOT GUILD WARS 2', TEAL, (40, 120, 100, 255), [],
          [('horizontal = the world, not your gear', AMBER, 44), ('level 60 forever, same continents', BONE, 42),
           ('professions grow sideways, no 300 to 500', BONE, 40), ('zones, events, Legacy: all stay relevant', BONE, 40),
           ('but raid gear still goes up', SICK, 46)], size=110),
     'emeralddream', "Now the big misunderstanding. At PAX Australia, Holly Longdale and Clay Stone explained it: horizontal means the world. Level sixty forever, same continents, professions that grow sideways. But raid gear still goes up.", 10.0),
    (card('vertical', 'GEAR BETWEEN TIERS', 'SMALL VERTICAL JUMPS', EPIC, EPICG, [],
          [('every new raid: strictly better loot', BONE, 44), ('"as narrow as possible"  ·  Clay Stone', AMBER, 42),
           ('slow stat inflation, nothing like retail', BONE, 40), ('Season of Discovery Naxx went too far', RED, 40),
           ('no free catch-up gear announced', GREY, 40)], size=110),
     'emeralddream', "Each new raid tier gives strictly better loot, but Clay Stone wants that jump as narrow as possible. Slow stat inflation, nothing like retail. Tim Jones said Season of Discovery's Naxxramas went too far, and it won't happen again.", 10.0),
    (card('evergreen', 'OLD RAIDS STAY EVERGREEN', 'WHY GO BACK?', GOLDC, GOLDG, [],
          [('every boss: an ultra-rare chase item', AMBER, 44), ('bonuses vs creature types + biomes', BONE, 42),
           ('an old drop can be BiS in a future raid', SICK, 42), ('"BiS for a very long time"  ·  Stone', BONE, 40),
           ('soft resets: maybe, years from now', GREY, 40)], size=110),
     'emeralddream', "So why go back to old raids? Every boss gets an ultra rare chase item, with bonuses against creature types or in specific biomes. An old drop can become best in slot in a future raid. Soft resets? Maybe, but years from now.", 10.0),
    (card('attune', 'ATTUNEMENTS ARE BACK', "ONYXIA'S KEY", GOLDC, GOLDG, [18423],
          [('the classic Onyxia chain is still required', BONE, 42), ('not account-wide at launch', AMBER, 44),
           ('Hyjal + Barrow Deeps: extra steps', BONE, 42), ('"to get the full experience"', GREY, 40)], size=120, isz=150),
     'emeralddream', "Attunements are back. Onyxia still needs the long classic quest chain, and it is not account wide at launch. Hyjal and Barrow Deeps also have extra steps to get the full experience.", 8.5),
    (card('dungeons', 'LEVEL 60 DUNGEONS', 'BIGGER THAN BRD', EPIC, EPICG, [],
          [('the pitch grew: 4, then 6, then 9 new dungeons', BONE, 40), ('Blackmaw Hold: bigger than Blackrock Depths', AMBER, 42),
           ('in the files: Alcaz Prison', SICK, 44), ("and The Shaper's Terrace", SICK, 44), ('no heroic dungeons either', GREY, 40)], size=110),
     'emeralddream', "Dungeons: the original pitch was four new dungeons, then six, then nine. Blackmaw Hold is bigger than Blackrock Depths, and the files already list Alcaz Prison and The Shaper's Terrace at level sixty.", 9.0),
    (card('pvp', 'PVP SEASONS', 'RANK 1 TO 14', HORDE, (150, 40, 30, 255), [],
          [('the classic rank system is back', BONE, 44), ('rank 2: PvP trinket  ·  rank 11: mounts', BONE, 40),
           ('rank 14: epic weapons', AMBER, 46), ('honor buys a blue + an epic set', BONE, 42), ('weekly season tasks: 3 Legacy Points', SICK, 42)], size=120),
     'emeralddream', 'PvP: the classic ranks one to fourteen are back, with a new reward at each rank, up to epic weapons at rank fourteen. Honor buys a blue and an epic set, and each season gives three Legacy Points.', 9.0),
    (card('legacy', 'THE LONG GAME', 'LEGACY POINTS', GOLDC, GOLDG, [],
          [('account progress across seasons', BONE, 44), ('earned from achievements + PvP seasons', BONE, 42),
           ('beta testers already got 16', AMBER, 46), ('spent on account-wide perks', BONE, 42)], size=120),
     'emeralddream', 'And the long game: Legacy Points, an account progression that carries over seasons. Beta testers already received sixteen.', 7.5),
    (card('outro', 'DECEMBER 9', 'WHICH RAID FIRST?', EPIC, EPICG, [280904, 18423, 280930],
          [('Barrow Deeps, Hyjal or Onyxia?', AMBER, 46), ('tell me in the comments', BONE, 46), ('follow for every Forever update', SICK, 44)], size=110, isz=120),
     'emeralddream', 'So, which raid are you clearing first on December ninth? Tell me in the comments, and follow for every Forever update.', 6.5),
]


PLAN = END
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
