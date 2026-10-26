# -*- coding: utf-8 -*-
"""Short: 1-60 leveling route for WoW Forever (build 1.60.1.70170, 02/10/2026).

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

KIND = 'route_alliance'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - 1-60 leveling route Alliance (EN).mp4'
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


FACTION = 'alliance'
import sys as _sys
_sys.path.insert(0, r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans')
import route_map as RM
FACTION = globals().get('FACTION', 'horde')
FCOL = HORDE if FACTION == 'horde' else ALLI
FGLOW = (150, 40, 30, 255) if FACTION == 'horde' else (40, 80, 160, 255)
NEW = {'Riverglades', 'Mount Hyjal', "Shen'dralas"}


def seg(name, lv, big, zones, dungeons, say, tested=False, extra=None, dur=8.0):
    pts = []
    for i, z in enumerate(zones):
        p = RM.pos(z)
        if p:
            pts.append((p[0], p[1], str(i + 1), SICK if z in NEW else FCOL))
    rows = [('  ·  '.join('%d %s' % (i + 1, z + (' (NEW)' if z in NEW else '')) for i, z in enumerate(zones[:2])), BONE, 38)]
    if len(zones) > 2:
        rows.append(('  ·  '.join('%d %s' % (i + 3, z + (' (NEW)' if z in NEW else '')) for i, z in enumerate(zones[2:4])), BONE, 38))
    if len(zones) > 4:
        rows.append(('  ·  '.join('%d %s' % (i + 5, z + (' (NEW)' if z in NEW else '')) for i, z in enumerate(zones[4:6])), BONE, 38))
    if dungeons:
        rows.append(('dungeons: ' + ', '.join(dungeons), AMBER, 36))
    if extra:
        rows.append((extra, SICK, 36))
    rows.append(('playable in the beta today' if tested else 'theory: may change at launch', GREY, 32))
    return (mcard(name, 'LEVEL ' + lv, big, FCOL, FGLOW, 'World2', pts, rows, mw=820, size=100), 'kalimdor', say, dur)


def intro_cards(side):
    return [
        (card('hook', 'WOW FOREVER  ·  %s' % side, 'LEVEL 1 TO 60 ROUTE', FCOL, FGLOW, [],
              [('every zone and dungeon in order', AMBER, 50), ('new Forever zones included', SICK, 46),
               ('1 to 30: playable in the beta today', BONE, 44), ('30 to 60: built from the game files', GREY, 42)], size=110),
         'kalimdor', 'The WoW Forever leveling route from one to sixty, %s side. Every zone and dungeon in order, new zones included. '
                     'One to thirty is playable in the beta today, thirty to sixty is built from the game files.' % side.lower(), 8.0),
    ]


def outro():
    return (card('outro', 'SAVE IT FOR NOVEMBER 4', 'LAUNCH ROUTE', FCOL, FGLOW, [],
                 [('zone levels: Wowhead Forever + beta files', GREY, 38), ('beta caps at 30: 30+ may change', GREY, 38),
                  ('tell me your favorite zone', BONE, 46), ('follow for the other faction', SICK, 44)], size=110),
            'kalimdor', 'Save this route for launch on November fourth. Tell me your favorite zone, and follow for more WoW Forever guides.', 6.5)


HORDE_ROUTE = intro_cards('HORDE') + [
    seg('h1', '1 - 10', 'START ZONES', ['Durotar', 'Mulgore', 'Tirisfal Glades'], [],
        'One to ten: your race starting zone. Durotar, Mulgore or Tirisfal. Windshaper Skyborne start on Zephras Isle, levels one to twelve.',
        tested=True, extra='Skyborne Windshaper: Zephras Isle (1-12)'),
    seg('h2', '10 - 20', 'THE BARRENS', ['The Barrens', 'Silverpine Forest'], ['Ragefire Chasm', 'Wailing Caverns'],
        'Ten to twenty: the Barrens, or Silverpine for the undead. Ragefire Chasm, then Wailing Caverns.', tested=True),
    seg('h3', '20 - 25', 'STONETALON + HILLSBRAD', ['Stonetalon Mountains', 'Hillsbrad Foothills'], ['Ruins of Lordaeron (21-22)', 'Shadowfang Keep'],
        "Twenty to twenty five: Stonetalon, then Hillsbrad from Tarren Mill. New dungeon: Ruins of Lordaeron, then Shadowfang Keep.", tested=True),
    seg('h4', '25 - 30', 'ASHENVALE', ['Ashenvale', 'Thousand Needles', 'Hillsbrad Foothills'], ['Excavation Site (28-31)', 'Blackfathom Deeps'],
        'Twenty five to thirty: Ashenvale and the updated Thousand Needles. New dungeon: the Excavation Site in the Wetlands.', tested=True,
        extra='level 30: Voidglare quests in Tarren Mill = Dalaran key'),
    seg('h5', '30 - 37', 'DALARAN TIME', ['Alterac Mountains', 'Arathi Highlands', 'Desolace', 'Stranglethorn Vale'], ['City of Dalaran (33)', 'Scarlet Monastery', 'Razorfen Kraul'],
        'Thirty to thirty seven: Alterac and the new City of Dalaran dungeon, then Arathi, Desolace and Stranglethorn. Scarlet Monastery and Razorfen Kraul.'),
    seg('h6', '37 - 44', 'RIVERGLADES', ['Riverglades', 'Dustwallow Marsh', 'Badlands', 'Swamp of Sorrows'], ['Razorfen Downs', 'Uldaman'],
        'Thirty seven to forty four: the brand new Riverglades zone, then Dustwallow, Badlands and Swamp of Sorrows. Razorfen Downs and Uldaman.'),
    seg('h7', '44 - 50', 'TANARIS + FERALAS', ['Tanaris', 'Feralas', 'The Hinterlands', 'Azshara'], ["Zul'Farrak", 'Maraudon'],
        "Forty four to fifty: Tanaris, Feralas, the updated Hinterlands and Azshara. Zul'Farrak and Maraudon."),
    seg('h8', '50 - 55', "UN'GORO + FELWOOD", ["Un'Goro Crater", 'Felwood', 'Searing Gorge', 'Burning Steppes'], ['Sunken Temple', 'Blackrock Depths'],
        "Fifty to fifty five: Un'Goro, Felwood, Searing Gorge and Burning Steppes. Sunken Temple and Blackrock Depths."),
    seg('h9', '55 - 60', 'THE FINAL STRETCH', ['Winterspring', 'Western Plaguelands', 'Eastern Plaguelands', 'Silithus', 'Mount Hyjal'],
        ['Strat', 'Scholo', 'Dire Maul', 'LBRS'],
        'Fifty five to sixty: Winterspring, the Plaguelands, Silithus. Then Mount Hyjal, the new endgame zone, and the new level sixty dungeons.',
        extra='new 60 dungeons: Alcaz Prison, Shaper\'s Terrace, Blackmaw Hold'),
    outro(),
]

ALLI_ROUTE = intro_cards('ALLIANCE') + [
    seg('a1', '1 - 10', 'START ZONES', ['Elwynn Forest', 'Dun Morogh', 'Teldrassil'], [],
        'One to ten: your race starting zone. Elwynn, Dun Morogh or Teldrassil. High Order Skyborne start on Zephras Isle, levels one to twelve.',
        tested=True, extra='Skyborne High Order: Zephras Isle (1-12)'),
    seg('a2', '10 - 20', 'WESTFALL + LOCH MODAN', ['Westfall', 'Loch Modan', 'Darkshore'], ['Hall of Thanes (15-16)', 'Deadmines', 'Stockade'],
        'Ten to twenty: Westfall, Loch Modan or Darkshore. New dungeon: the Hall of Thanes, then Deadmines and the Stockade.', tested=True),
    seg('a3', '20 - 25', 'REDRIDGE + DUSKWOOD', ['Redridge Mountains', 'Duskwood', 'Wetlands'], ['Ruins of Lordaeron (21-22)', 'Wailing Caverns'],
        'Twenty to twenty five: Redridge, Duskwood and the Wetlands. New dungeon: Ruins of Lordaeron.', tested=True),
    seg('a4', '25 - 30', 'ASHENVALE + HILLSBRAD', ['Ashenvale', 'Hillsbrad Foothills', 'Wetlands'], ['Excavation Site (28-31)', 'Gnomeregan', 'SFK', 'BFD'],
        'Twenty five to thirty: Ashenvale, Hillsbrad from Southshore, and the Wetlands. New dungeon: the Excavation Site.', tested=True,
        extra='level 30: Emissary Jacques in Southshore = Dalaran key'),
    seg('a5', '30 - 37', 'DALARAN TIME', ['Alterac Mountains', 'Arathi Highlands', 'Desolace', 'Stranglethorn Vale'], ['City of Dalaran (33)', 'Scarlet Monastery', 'Razorfen Kraul'],
        'Thirty to thirty seven: Alterac and the new City of Dalaran dungeon, then Arathi, Desolace and Stranglethorn. Scarlet Monastery and Razorfen Kraul.'),
    seg('a6', '37 - 44', 'RIVERGLADES', ['Riverglades', 'Dustwallow Marsh', 'Badlands', 'Swamp of Sorrows'], ['Razorfen Downs', 'Uldaman'],
        'Thirty seven to forty four: the brand new Riverglades zone, then Theramore in Dustwallow, Badlands and Swamp of Sorrows. Razorfen Downs and Uldaman.'),
    seg('a7', '44 - 50', 'TANARIS + FERALAS', ['Tanaris', 'Feralas', 'The Hinterlands', 'Azshara'], ["Zul'Farrak", 'Maraudon'],
        "Forty four to fifty: Tanaris, Feralas from Feathermoon, the updated Hinterlands and Azshara. Zul'Farrak and Maraudon."),
    seg('a8', '50 - 55', "UN'GORO + FELWOOD", ["Un'Goro Crater", 'Felwood', 'Searing Gorge', 'Burning Steppes'], ['Sunken Temple', 'Blackrock Depths'],
        "Fifty to fifty five: Un'Goro, Felwood, Searing Gorge and Burning Steppes. Sunken Temple and Blackrock Depths."),
    seg('a9', '55 - 60', 'THE FINAL STRETCH', ['Winterspring', 'Western Plaguelands', 'Eastern Plaguelands', 'Silithus', 'Mount Hyjal'],
        ['Strat', 'Scholo', 'Dire Maul', 'LBRS'],
        'Fifty five to sixty: Winterspring, the Plaguelands, Silithus. Then Mount Hyjal, the new endgame zone, and the new level sixty dungeons.',
        extra='new 60 dungeons: Alcaz Prison, Shaper\'s Terrace, Blackmaw Hold'),
    outro(),
]

PLANX = HORDE_ROUTE if FACTION == 'horde' else ALLI_ROUTE


PLAN = PLANX
MUSIC = 'paladin'


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
