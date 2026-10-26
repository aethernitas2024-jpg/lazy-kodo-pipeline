import sys as _sys
_sys.path.insert(0, r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans')
import route_map as RM
FACTION = globals().get('FACTION', 'horde')
FCOL = HORDE if FACTION == 'horde' else ALLI
FGLOW = (150, 40, 30, 255) if FACTION == 'horde' else (40, 80, 160, 255)


def step(n, lv, zone, hub, rows, say, new=None, dur=7.0, zoom=None):
    p = RM.pos(zone)
    pts = [(p[0], p[1], str(n), SICK if new else FCOL)] if p else []
    r = [(hub, AMBER, 40)] + [(t, BONE, 36) for t in rows]
    if new:
        r.append(('NEW IN FOREVER: ' + new, SICK, 36))
    return (mcard('s%02d' % n, 'STEP %d  ·  LEVEL %s' % (n, lv), zone.upper(), FCOL, FGLOW, 'World2', pts, r,
                  zoom=zoom, mw=780, size=96), 'kalimdor', say, dur)


def hook(side, extra):
    return (card('hook', 'WOW FOREVER  ·  %s  ·  1 TO 30' % side, 'OPTIMIZED ROUTE', FCOL, FGLOW, [],
                 [('the classic speedrun route', BONE, 48), ('updated with Forever content', AMBER, 48),
                  ('new dungeons at the right level', SICK, 44), ('+20% dungeon XP since Oct 8', SICK, 44), (extra, GREY, 38)], size=110),
            'kalimdor', 'The optimized one to thirty route for WoW Forever, %s side: the classic speedrun route, updated with the new Forever dungeons '
                        'at the right level, and the twenty percent dungeon XP boost from the October eighth patch.' % side.lower(), 8.5)


def outro():
    return (card('outro', 'NEXT: 30 TO 60', 'SAVE THIS ROUTE', FCOL, FGLOW, [],
                 [('based on the Warcraft Tavern Classic guides', GREY, 36), ('(Nightfall Horde  ·  Judgement Alliance)', GREY, 34),
                  ('+ WoW Forever beta quests and dungeons', GREY, 36), ('follow for part 2', SICK, 48)], size=110),
            'kalimdor', 'Built on the Warcraft Tavern classic guides, updated with the WoW Forever beta. Save it, and follow for part two, thirty to sixty.', 7.0)


HORDE30 = [
    hook('HORDE', 'orc & troll: follow from step 1  ·  others join at 12'),
    step(1, '1 - 6', 'Durotar', 'Valley of Trials, then Sen\'jin Village',
         ['clear every Valley quest before leaving', 'Sen\'jin: grab all 6 hub quests', 'Tauren / Undead / Skyborne: own start zone'],
         "Step one, Durotar. Finish every quest in the Valley of Trials, then grab all six quests in Sen'jin Village. Tauren, undead and Skyborne do their own start zone and join at level twelve."),
    step(2, '6 - 11', 'Durotar', 'Razor Hill  ·  Echo Isles  ·  Thunder Ridge',
         ['set your hearthstone in Razor Hill', 'quilboars + harpies on the way', 'Orgrimmar turn-ins, then head west'],
         'Step two: Razor Hill is your base. Hearth there, chain the quilboar and harpy quests, swim to the Echo Isles, then Orgrimmar and the Barrens.'),
    step(3, '11 - 14', 'The Barrens', 'The Crossroads (hearth + flight path)',
         ['plainstriders, raptors, centaur camps', 'take the Ratchet flight path early', 'quick run to Thunder Bluff for its flight path'],
         'Step three, the Barrens: hearth at the Crossroads, clear the first ring of quests, and grab the Ratchet and Thunder Bluff flight paths early.'),
    step(4, '14 - 17', 'The Barrens', 'Stagnant Oasis  ·  Camp Taurajo',
         ['move your hearth to Camp Taurajo', 'Lushwater Oasis + raptor quests', 'Ragefire Chasm fits here (13-18)'],
         'Step four: the south Barrens. Move your hearth to Camp Taurajo. Ragefire Chasm fits perfectly here, and dungeon kills now give twenty percent more XP.'),
    step(5, '17 - 20', 'Stonetalon Mountains', 'Sludge Fen  ·  Ashenvale flight paths  ·  Sun Rock',
         ['Ignition + The Escape in Sludge Fen', 'unlock the Ashenvale flight paths', 'Northwatch Hold to close the Barrens'],
         'Step five: Sludge Fen, then unlock the Ashenvale flight paths, Stonetalon and Sun Rock Retreat, and close the Barrens at Northwatch Hold.'),
    step(6, '20 - 22', 'Tirisfal Glades', 'Undercity + Brill: dungeon quests',
         ['Wailing Caverns run at 20', 'then grab the Ruins of Lordaeron quests', 'Brill, Apothecarium, Royal Quarter'],
         'Step six: a Wailing Caverns run at twenty. Then the new Ruins of Lordaeron dungeon: grab its quests in Brill and the Undercity.',
         new='Ruins of Lordaeron (21-22), 9 Horde quests'),
    step(7, '22 - 24', 'Hillsbrad Foothills', 'Tarren Mill',
         ['Durnholde prisoners + Hillsbrad Fields', 'farmers and the town', 'then back to Kalimdor'],
         'Step seven: zeppelin to the Undercity, then Tarren Mill in Hillsbrad: Durnholde Keep, the fields and the farmers.'),
    step(8, '24 - 27', 'Ashenvale', "Splintertree Post  ·  Zoram'gar",
         ['Thistlefur, Mystral Lake, Silverwing', 'Bael Modan in the Barrens on the way', 'Blackfathom Deeps fits at 27'],
         "Step eight, Ashenvale: Splintertree Post and Zoram'gar Outpost. Thistlefur, Mystral Lake, Bael Modan in the Barrens, and Blackfathom Deeps at twenty seven."),
    step(9, '27 - 30', 'Thousand Needles', 'Freewind Post',
         ['centaurs, Highperch, Darkcloud Pinnacle', 'Hillsbrad round 2 before it', 'zone updated in Forever'],
         'Step nine: a second round of Hillsbrad, then Thousand Needles from Freewind Post. The zone was updated in Forever.'),
    step(10, '28 - 31', 'Wetlands', 'Excavation Site dungeon',
         ['Changing Tastes (Orgrimmar)', 'Deathstalker Agent above the Dragonmaw camp', 'Titan Relic: Thunder Bluff + Mulgore turn-ins'],
         'Step ten: the new Excavation Site dungeon in the Wetlands. Grab Changing Tastes in Orgrimmar, and meet the Deathstalker agent above the Dragonmaw camp.',
         new='Excavation Site (28-31), 5 Horde quests'),
    step(11, '30', 'Hillsbrad Foothills', 'Tarren Mill: Magus Wordeen Voidglare',
         ['Prison Break In  ·  Dalaran Patrols', 'Key to the City', 'unlocks City of Dalaran (33)'],
         'And at thirty, back to Tarren Mill: Magus Wordeen Voidglare\'s three quests unlock the City of Dalaran. That is part two.',
         new='City of Dalaran chain'),
    outro(),
]

ALLI30 = [
    hook('ALLIANCE', 'human: from step 1  ·  dwarf, gnome, night elf: join at 9-11'),
    step(1, '1 - 9', 'Elwynn Forest', 'Northshire, then Goldshire (hearth)',
         ['Fargodeep Mine + the farms', 'Jasperlode Mine, Crystal Lake, Eastvale', 'others: own start zone, join at step 2'],
         'Step one, Elwynn Forest: Northshire, then hearth in Goldshire. Fargodeep, the farms, Jasperlode, Crystal Lake and Eastvale. Other races do their start zone and join at step two.'),
    step(2, '9 - 11', 'Loch Modan', 'Ironforge flight path, then Thelsamar',
         ['Deeprun Tram to Ironforge', 'quick Dun Morogh + Loch Modan quests', 'then Menethil and the boat to Darkshore'],
         'Step two: the tram to Ironforge, take the flight path, a few quests in Dun Morogh and Loch Modan, then Menethil Harbor and the boat to Darkshore.'),
    step(3, '11 - 15', 'Darkshore', 'Auberdine (hearth)',
         ['Ameth\'Aran, Bashal\'aran, the Red Crystal', 'deep ocean quests', 'then hearth back to Ironforge'],
         "Step three, Darkshore: hearth in Auberdine. Ameth'Aran, Bashal'aran, the red crystal and the ocean quests."),
    step(4, '15 - 16', 'Dun Morogh', 'Old Ironforge: Hall of Thanes',
         ['4 quests  ·  4 bosses', '+20% dungeon XP since Oct 8', 'then Stormwind and Westfall flight path'],
         'Step four: the new Hall of Thanes dungeon, beneath Old Ironforge. Four quests, perfect at fifteen. Then Stormwind and the Westfall flight path.',
         new='Hall of Thanes (15-16)'),
    step(5, '16 - 18', 'Redridge Mountains', 'Lakeshire',
         ['lake items, murlocs, gnolls', 'hearth in Lakeshire', 'then fly out to Loch Modan'],
         'Step five, Redridge: Lakeshire, the lake, murlocs and gnolls.'),
    step(6, '18 - 21', 'Darkshore', 'Loch Modan, then Darkshore round 2',
         ['Thelsamar: dam + Hunter\'s Lodge', 'Auberdine: Onu, Murkdeep, furbolgs', 'walk south to Ashenvale'],
         'Step six: a second round of Loch Modan, then Darkshore: Onu, Murkdeep and the furbolgs. Then walk south to Ashenvale.'),
    step(7, '21 - 23', 'Wetlands', 'Menethil Harbor',
         ['murlocs, gnolls, crocolisks', 'Ruins of Lordaeron quests: Stormwind', 'Nightingale, Dena Kennedy, General Jonathan'],
         'Step seven: Maestra\'s Post in Ashenvale, then the Wetlands. Grab the new Ruins of Lordaeron quests in Stormwind if you want a dungeon break.',
         new='Ruins of Lordaeron (21-22)'),
    step(8, '23 - 25', 'Duskwood', 'Redridge, then Darkshire',
         ['Raven Hill, Sven\'s Camp', 'Stalvan chain starts here', 'take the Darkshire flight path'],
         "Step eight: Redridge again, then Duskwood from Darkshire. Raven Hill, Sven's Camp and the start of the Stalvan chain."),
    step(9, '25 - 27', 'Wetlands', 'Astranaar, then Menethil',
         ['Ashenvale: furbolgs, Iris Lake, Moonwell', 'Wetlands: Dun Modr, Ironbeard\'s Tomb', 'Highland Hides (Menethil tanner)'],
         "Step nine: Ashenvale, then the Wetlands from Menethil: Dun Modr, Ironbeard's Tomb, and the new Highland Hides quest.",
         new='Excavation Site quests in Menethil'),
    step(10, '27 - 30', 'Duskwood', 'Ashenvale, then Darkshire',
         ['Ashenvale satyrs + Forest Song', 'Duskwood: Mor\'ladim, Abercrombie', 'Excavation Site dungeon (28-31)'],
         "Step ten: Ashenvale's satyrs, then Duskwood to thirty. And the new Excavation Site dungeon in the Wetlands, with quests from Menethil Harbor.",
         new='Excavation Site (28-31), 9 Alliance quests'),
    step(11, '30', 'Hillsbrad Foothills', 'Southshore: Emissary Jacques',
         ['An Alarming Request', 'Image of Archmage Modera', 'unlocks City of Dalaran (33)'],
         'And at thirty, Southshore: Emissary Jacques starts the City of Dalaran chain. That is part two.',
         new='City of Dalaran chain'),
    outro(),
]

PLANX = HORDE30 if FACTION == 'horde' else ALLI30
