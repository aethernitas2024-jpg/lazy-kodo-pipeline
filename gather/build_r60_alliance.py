# -*- coding: utf-8 -*-
"""Short: full 30-60 leveling route for WoW Forever (build 1.60.1.70170, 02/10/2026).

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

KIND = 'r60_alliance'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - full 30-60 leveling route Alliance (EN).mp4'
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


def step(n, lv, zone, hub, rows, say, new=None, dur=7.5):
    p = RM.pos(zone)
    pts = [(p[0], p[1], str(n), SICK if new else FCOL)] if p else []
    r = [(hub, AMBER, 38)] + [(t, BONE, 33) for t in rows]
    if new:
        r.append(('FOREVER: ' + new, SICK, 34))
    zoom = ((0, 0, 51.4, 100) if p[0] < 51.4 else (51.4, 0, 100, 100)) if p else None
    return (mcard('s%02d' % n, 'STEP %d  ·  LEVEL %s' % (n, lv), zone.upper(), FCOL, FGLOW, 'World2', pts, r,
                  zoom=zoom, mw=560, size=90), 'kalimdor', say, dur)


def hook(side):
    return (card('hook', 'WOW FOREVER  ·  %s  ·  PART 2' % side, 'LEVELING 30 TO 60', FCOL, FGLOW, [],
                 [('every hub, hearth and flight path', BONE, 46), ('City of Dalaran, Desolace rework,', AMBER, 44),
                  ('the new Riverglades and Hyjal', AMBER, 44), ('beta caps at 30: built from the game files', GREY, 38),
                  ('may change at launch', GREY, 38)], size=110),
            'kalimdor', 'Part two: thirty to sixty, %s side. Every hub, hearthstone and flight path, with the City of Dalaran, the reworked Desolace, '
                        'the new Riverglades and Mount Hyjal. The beta stops at thirty, so this part is built from the game files.' % side.lower(), 8.5)


def tips(t):
    return (card('tips', 'BEFORE YOU START', 'ROUTE RULES', FCOL, FGLOW, [],
                 [('do dungeons with their quests only', BONE, 42), ('+20% dungeon XP in Forever', SICK, 42),
                  ('grind the last bar instead of travelling', BONE, 42), ('stack turn-ins in capital cities', BONE, 42), (t, AMBER, 40)], size=120),
            'kalimdor', 'Rules for this part: only run dungeons with their quests, they give twenty percent more XP in Forever. '
                        'Grind the last bar instead of travelling, and stack your turn ins in the capital cities.', 7.5)


def outro():
    return (card('outro', 'LEVEL 60 REACHED', 'HYJAL AWAITS', FCOL, FGLOW, [],
                 [('save this route for launch', BONE, 48), ('November 4', AMBER, 52), ('which zone are you skipping?', SICK, 46)], size=120),
            'kalimdor', 'Level sixty. Save this route for launch on November fourth, and tell me which zone you are skipping.', 6.0)


HORDE60 = [
    hook('HORDE'),
    tips('hearth: Orgrimmar, Tarren Mill, Gadgetzan, Camp Mojache'),
    step(1, '30', 'Feralas', 'Camp Mojache flight path  ·  Thunder Bluff',
         ['grab the Mojache flight path', 'Thunder Bluff: A Vengeful Fate, Steelsnap', 'Razorfen Kraul: Charlga\'s heart'],
         "Step one: grab the Camp Mojache flight path, then Thunder Bluff for A Vengeful Fate and Steelsnap, and a Razorfen Kraul run."),
    step(2, '31', 'Thousand Needles', 'Darkcloud Pinnacle  ·  Highperch',
         ['summon Arikara at Darkcloud Pinnacle', 'Whitereach Post gizmo', 'Steelsnap at Highperch, Roguefeather Den'],
         'Step two: Thousand Needles. Arikara at Darkcloud Pinnacle, the Whitereach gizmo, Steelsnap at Highperch and Roguefeather Den.',
         new='10 new quests in the zone'),
    step(3, '32', 'Thousand Needles', 'Shimmering Flats: Mirage Raceway',
         ['take all 7 raceway quests', 'turtle meat + flats mobs', 'one sweep, one turn-in'],
         'Step three: the Shimmering Flats. Take all seven Mirage Raceway quests and clear them in one sweep.'),
    step(4, '33', 'Alterac Mountains', 'City of Dalaran dungeon',
         ['Heart of Disruption (key from part 1)', 'The Grave Knight, Source of Power', 'Opportunistic Education, ilvl 36 blues'],
         'Step four: the new City of Dalaran dungeon. Heart of Disruption, The Grave Knight, Source of Power and Opportunistic Education.',
         new='City of Dalaran (33)'),
    step(5, '33 - 34', 'Stranglethorn Vale', "Grom'gol  ·  Nesingwary's camp",
         ['Goblin Sponsorship chain', "Nesingwary's tiger, panther, raptor hunts", "Bal'lal Ruins"],
         "Step five: Stranglethorn from Grom'gol. The Goblin Sponsorship chain, Nesingwary's hunts and the Bal'lal Ruins."),
    step(6, '34', 'Hillsbrad Foothills', 'Tarren Mill (hearth)',
         ["Helcular's quests", 'murloc eyes + naga scales', 'Dun Garok, Witherbark trolls'],
         "Step six: Tarren Mill. Helcular's quests, the murlocs and nagas, Dun Garok and the Witherbark trolls."),
    step(7, '35', 'Alterac Mountains', 'Alterac  ·  Lordamere',
         ['braziers: summon Frostmaw', 'Worn Stone Tokens at Lordamere', "Helcular's Grave, Battle of Hillsbrad"],
         "Step seven: Alterac. Light the braziers for Frostmaw, the stone tokens at Lordamere, and Helcular's grave."),
    step(8, '36', 'Arathi Highlands', 'Hammerfall',
         ['Dalaran patrols', 'Raising Spirits, Guile of the Raptor', 'Dabyrie Farmstead'],
         'Step eight: Hammerfall in Arathi. Raising Spirits, Guile of the Raptor and the Dabyrie farmers.'),
    step(9, '37', 'Desolace', 'Ghost Walker Post  ·  Shadowprey',
         ['Magram centaurs, Thunder Axe Fortress', 'Shadowprey fishing, Raznajar Isle', 'Gelkis + Magram quests need level 35'],
         'Step nine: Desolace, the most changed zone in Forever: thirty one new quests, and the centaur quests now need level thirty five.',
         new='31 new quests'),
    step(10, '38', 'Stranglethorn Vale', "Grom'gol  ·  Booty Bay",
         ['Ruins of Zuuldaia, Mizjah', 'fly to Booty Bay', 'Scarlet Monastery wings'],
         'Step ten: Stranglethorn again, the Ruins of Zuuldaia and Mizjah, then Scarlet Monastery.'),
    step(11, '39', 'Badlands', "Faldir's Cove  ·  Kargath",
         ['Sunken Treasure dive', 'Loch Modan road to the Badlands', 'Kargath flight path + elementals'],
         "Step eleven: Faldir's Cove for the sunken treasure, then the Badlands from Kargath."),
    step(12, '40 - 42', 'Swamp of Sorrows', 'Stonard  ·  Kargath',
         ['Noboru the Cudgel, Pool of Tears', 'Boss Tho\'grun, Apocryphan\'s Rest', 'Misty Reed Post murlocs'],
         "Step twelve: Swamp of Sorrows from Stonard: Noboru and the Pool of Tears. Badlands: Boss Tho'grun."),
    step(13, '38 - 44', 'Riverglades', 'NEW ZONE  ·  levels 36-44',
         ['content still hidden in the beta', 'could replace steps 10 to 14', 'worth checking at launch'],
         'Option: the brand new Riverglades, levels thirty six to forty four. Its quests are still hidden in the beta, but it could replace part of this loop.',
         new='Riverglades'),
    step(14, '43 - 44', 'Stranglethorn Vale', 'Booty Bay  ·  pirates',
         ['Bloodsail Buccaneers, Cortello\'s Riddle', 'Venture Co. mining, Zul\'Mamwe', 'Razorfen Downs before 45'],
         "Step fourteen: Booty Bay and the pirates, Cortello's Riddle, Zul'Mamwe, and Razorfen Downs before forty five."),
    step(15, '45 - 46', 'Feralas', 'Brackenwall  ·  Gadgetzan  ·  Camp Mojache (hearth)',
         ['Dustwallow: Den of Flame', 'Gordunni Outpost, Writhing Deep', 'Grimtotem Village, Ruins of Isildien'],
         'Step fifteen: Dustwallow from Brackenwall, then Feralas from Camp Mojache: the Gordunni, the Writhing Deep and the Grimtotem.'),
    step(16, '47', 'Tanaris', 'Gadgetzan (hearth)',
         ['Lost Rigger Cove, Andre Firebeard', 'Dunemaul Compound, Thistleshrub Valley', "Zul'Farrak run"],
         "Step sixteen: Tanaris from Gadgetzan: Lost Rigger Cove, Dunemaul, Thistleshrub, and Zul'Farrak."),
    step(17, '48 - 49', 'The Hinterlands', 'Revantusk Village',
         ["Altar of Zul, Rin'ji escort", 'Overlook Cliffs', 'Feralas: Frayfeather, Twin Colossals'],
         "Step seventeen: the Hinterlands from Revantusk: the Altar of Zul and Rin'ji. Then Feralas: Frayfeather and the Twin Colossals."),
    step(18, '50 - 51', 'Searing Gorge', 'Blasted Lands  ·  Thorium Point',
         ['Blasted Lands beast quests', 'Thorium Point, watchtower bowls', 'Forging the Shaft, Slag Pit'],
         'Step eighteen: the Blasted Lands beast quests, then Searing Gorge from Thorium Point.'),
    step(19, '52 - 53', "Un'Goro Crater", "Marshal's Refuge  ·  Azshara",
         ['soil + crystals, Morrowgrain', 'Azshara: Valormok flight path', 'Betrayed chain, Jediga deliveries'],
         "Step nineteen: Un'Goro from Marshal's Refuge, then Azshara from Valormok.",
         new='Azshara: Blackmaw furbolg reputation'),
    step(20, '54 - 56', 'Felwood', 'Bloodvenom Post  ·  Everlook',
         ['Jaedenar moonwell + braziers', 'Timbermaw Hold, Winterspring yetis', "Sunken Temple, Lar'korwi, A-Me 01"],
         "Step twenty: Felwood, Timbermaw Hold and Winterspring. Back to Un'Goro, and a Sunken Temple run."),
    step(21, '57', 'Burning Steppes', 'Flame Crest  ·  The Bulwark',
         ['Dreadmaul Rock, Krom\'grul', 'Western Plaguelands: Scourge cauldrons', 'Blackrock Depths runs'],
         "Step twenty one: Burning Steppes from Flame Crest, Blackrock Depths, and the Western Plaguelands cauldrons."),
    step(22, '58 - 59', 'Eastern Plaguelands', "Light's Hope  ·  The Bulwark",
         ["Darrowshire, Pamela's doll", 'Andorhal towers, the Undercroft', 'Plaguewood, Northdale, Scholomance'],
         "Step twenty two: the Plaguelands. Darrowshire and Pamela's doll, Andorhal, the Undercroft and Scholomance."),
    step(23, '60', 'Mount Hyjal', 'Mount Hyjal  ·  Guardians of Hyjal',
         ['new 60 dungeons: Alcaz Prison,', "Shaper's Terrace, Blackmaw Hold", 'raids: Hyjal + Barrow Deeps'],
         'And at sixty: Mount Hyjal, the Guardians of Hyjal, the three new level sixty dungeons, and the Hyjal and Barrow Deeps raids.',
         new='endgame zone + 3 dungeons'),
    outro(),
]

ALLI60 = [
    hook('ALLIANCE'),
    tips('hearth: Booty Bay, Menethil, Theramore, Gadgetzan'),
    step(1, '30 - 33', 'Stranglethorn Vale', 'Rebel Camp  ·  Nesingwary  ·  Booty Bay (hearth)',
         ['Kurzen Camp, Bad Medicine', 'Second Rebellion', "Nesingwary's hunting quests"],
         "Step one: Stranglethorn. Rebel Camp, Kurzen Camp, Bad Medicine, and Nesingwary's hunts. Hearth in Booty Bay."),
    step(2, '33', 'Alterac Mountains', 'Southshore  ·  City of Dalaran dungeon',
         ['Heart of Disruption (key from part 1)', 'A Green Sample, Power Overwhelming', 'Starving Arcane, ilvl 36 blues'],
         'Step two: Southshore and the new City of Dalaran dungeon: Heart of Disruption, A Green Sample, Power Overwhelming and Starving Arcane.',
         new='City of Dalaran (33)'),
    step(3, '33 - 34', 'Alterac Mountains', 'Southshore  ·  Alterac',
         ['Yeti cave', 'Syndicate camps', 'then Menethil and the Darkshore boat'],
         'Step three: Alterac from Southshore: the yeti cave and the Syndicate camps.'),
    step(4, '34 - 35', 'Desolace', "Nijel's Point (hearth)",
         ['Thunder Axe Fortress, Karnitol Shipwreck', 'Gelkis + Magram quests need level 35', '31 new quests in Forever'],
         "Step four: Desolace from Nijel's Point. The most changed zone in Forever: thirty one new quests, and the centaur quests now need level thirty five.",
         new='Desolace rework'),
    step(5, '35', 'Badlands', 'Hall of Explorers  ·  Loch Modan',
         ['Ironforge: Hall of Explorers quest', 'Excavation site', 'Murdaloc'],
         'Step five: a short Badlands stop with the Hall of Explorers quest and Murdaloc.'),
    step(6, '35 - 36', 'Stranglethorn Vale', 'Booty Bay',
         ['Nesingwary, Kurzen Camp', 'Goblin Sponsorship', 'fly to Refuge Pointe'],
         'Step six: Stranglethorn again: Nesingwary and Goblin Sponsorship.'),
    step(7, '36 - 37', 'Arathi Highlands', 'Refuge Pointe',
         ["Go'shek farm", 'Princess Trapped escort', 'Stromgarde elites (grouped)'],
         "Step seven: Arathi from Refuge Pointe: Go'shek farm, Princess Trapped, and the Stromgarde elites with a group."),
    step(8, '37 - 38', 'Alterac Mountains', 'Strahnbrad  ·  Chillwind',
         ['ogre camps, Nagaz', 'Ensorcelled Parchment', 'Chillwind Camp flight path'],
         'Step eight: the Alterac ogres, Nagaz and the parchment, and the Chillwind Camp flight path.'),
    step(9, '38', 'Dustwallow Marsh', 'Theramore (hearth)',
         ['Theramore goblin quests', 'Swamplight Manor', 'Balos Jacken'],
         'Step nine: Theramore in Dustwallow: the goblin quests, Swamplight Manor and Balos Jacken.'),
    step(10, '38 - 39', 'Swamp of Sorrows', 'Darkshire  ·  Nethergarde',
         ['Misty Valley elementals', 'Draenethyst Crystals', 'Noboru the Cudgel'],
         'Step ten: Swamp of Sorrows: Misty Valley, the Draenethyst crystals and Noboru.'),
    step(11, '39 - 40', 'Badlands', 'Thelsamar (hearth)  ·  dwarf camp',
         ['Hammertoe digsite', 'Reagent Run', 'grind to 40'],
         'Step eleven: the Badlands dwarf camp, the Hammertoe digsite and Reagent Run.'),
    step(12, '38 - 44', 'Riverglades', 'NEW ZONE  ·  levels 36-44',
         ['content still hidden in the beta', 'could replace steps 10 to 15', 'worth checking at launch'],
         'Option: the brand new Riverglades, levels thirty six to forty four. Its quests are still hidden in the beta, but it could replace part of this loop.',
         new='Riverglades'),
    step(13, '40 - 41', 'Stranglethorn Vale', 'Booty Bay',
         ['Desolace: Down the Scarlet Path', 'pirate quests, Mistvale gorillas', 'Nesingwary finale'],
         'Step thirteen: Desolace for Down the Scarlet Path, then Stranglethorn: pirates, the Mistvale gorillas and Nesingwary.'),
    step(14, '41 - 42', 'Arathi Highlands', "Faldir's Cove  ·  Nethergarde",
         ['Faldir\'s Cove nagas, Tidal Charm', 'Swamp: Nethergarde supplies', 'Driftwood beach'],
         "Step fourteen: Faldir's Cove and the Tidal Charm, then the Nethergarde supplies in the Swamp."),
    step(15, '42 - 43', 'Badlands', 'Uldaman  ·  Booty Bay',
         ['Study of the Elements', 'Uldaman run with its quests', 'Bloodsail captains, Cortello\'s Riddle'],
         "Step fifteen: Uldaman with all its quests, then the Bloodsail captains and Cortello's Riddle."),
    step(16, '43 - 45', 'Tanaris', 'Gadgetzan (hearth)',
         ['Shimmering Flats', 'Steamwheedle Port, Caliph Scorpidsting', 'hippogryph eggs, pirates'],
         'Step sixteen: Tanaris from Gadgetzan: the Shimmering Flats, Steamwheedle Port and Caliph Scorpidsting.'),
    step(17, '45 - 47', 'The Hinterlands', "Aerie Peak (hearth)  ·  Zul'Farrak",
         ['troll cages, Altar of Zul', "Booty Bay turn-ins", "Zul'Farrak run"],
         "Step seventeen: the Hinterlands from Aerie Peak, then Zul'Farrak."),
    step(18, '47 - 49', 'Feralas', 'Searing Gorge  ·  Feathermoon',
         ['Thorium Point, Slag Pit', 'Stave of Equinex, Rockbiter', 'Tanaris: Noxious Lair'],
         'Step eighteen: Searing Gorge, Feralas from Feathermoon, and the Noxious Lair in Tanaris.'),
    step(19, '49 - 50', 'Felwood', 'Blasted Lands  ·  Emerald Sanctuary',
         ['Blasted Lands beast quests', 'Felwood: Jaedenar', 'Azshara road'],
         'Step nineteen: the Blasted Lands beast quests, then Felwood.'),
    step(20, '50 - 53', "Un'Goro Crater", "Marshal's Refuge  ·  Burning Steppes",
         ["pylons, Lar'Korwi", 'Chillwind Camp', "Morgan's Vigil, Dreadmaul Rock"],
         "Step twenty: Un'Goro, Chillwind Camp, and Burning Steppes from Morgan's Vigil."),
    step(21, '53 - 55', 'Azshara', 'Azshara  ·  Felwood  ·  Timbermaw',
         ["Kim'jael quests", 'Timbermaw Tunnel, Everlook', 'Emerald Sanctuary, Jaedenar'],
         "Step twenty one: Azshara and Kim'jael, then Felwood through the Timbermaw tunnel.",
         new='Azshara: Blackmaw furbolg reputation'),
    step(22, '55 - 57', 'Eastern Plaguelands', "Light's Hope  ·  Chillwind Camp",
         ['Tirion Fordring chain', 'Andorhal, Darrowshire', 'Scholomance key, the Undercroft'],
         "Step twenty two: the Plaguelands. Tirion Fordring, Andorhal, Darrowshire and the Scholomance key."),
    step(23, '57 - 60', 'Winterspring', 'Everlook  ·  Silithus',
         ['Winterfall furbolgs', 'Cenarion Hold quests', 'Winterfall Village grind to 60'],
         'Step twenty three: Winterspring from Everlook, a Silithus trip, and the Winterfall grind to sixty.'),
    step(24, '60', 'Mount Hyjal', 'Mount Hyjal  ·  Guardians of Hyjal',
         ['new 60 dungeons: Alcaz Prison,', "Shaper's Terrace, Blackmaw Hold", 'raids: Hyjal + Barrow Deeps'],
         'And at sixty: Mount Hyjal, the Guardians of Hyjal, the three new level sixty dungeons, and the Hyjal and Barrow Deeps raids.',
         new='endgame zone + 3 dungeons'),
    outro(),
]

PLANX = HORDE60 if FACTION == 'horde' else ALLI60


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
