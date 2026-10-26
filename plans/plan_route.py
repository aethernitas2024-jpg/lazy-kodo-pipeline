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
