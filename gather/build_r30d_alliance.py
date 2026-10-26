# -*- coding: utf-8 -*-
"""Short: full 1-30 leveling route for WoW Forever (build 1.60.1.70170, 02/10/2026).

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

KIND = 'r30d_alliance'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - full 1-30 leveling route Alliance (EN).mp4'
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


def hook(side, extra):
    return (card('hook', 'WOW FOREVER  ·  %s  ·  1 TO 30' % side, 'FULL LEVELING ROUTE', FCOL, FGLOW, [],
                 [('every hub, hearth and flight path', BONE, 46), ('the quests worth doing', AMBER, 46),
                  ('new Forever dungeons at the right level', SICK, 42), ('+20% dungeon XP since Oct 8', SICK, 42), (extra, GREY, 36)], size=110),
            'kalimdor', 'The full one to thirty leveling route for WoW Forever, %s side: every hub, hearthstone and flight path, the quests worth doing, '
                        'and the new Forever dungeons at the right level.' % side.lower(), 8.5)


def tips(side_tip):
    return (card('tips', 'BEFORE YOU START', 'ROUTE RULES', FCOL, FGLOW, [],
                 [('kill everything on your path', BONE, 44), ('never travel empty-handed: stack quests', BONE, 42),
                  ('skip elite quests unless grouped', BONE, 42), ('dungeon kills: +20% XP in Forever', SICK, 42),
                  ('group XP uses YOUR level now', SICK, 42), (side_tip, AMBER, 40)], size=120),
            'kalimdor', 'Rules for this route: kill everything on your way, stack quests so you never travel empty handed, skip elites unless you have a group, '
                        'and use dungeons: since October eighth they give twenty percent more XP.', 8.0)


def outro():
    return (card('outro', 'LEVEL 30 REACHED', 'NEXT: 30 TO 60', FCOL, FGLOW, [],
                 [('save this route for launch', BONE, 48), ('November 4', AMBER, 52), ('follow for part 2', SICK, 48)], size=120),
            'kalimdor', 'Level thirty. Save this route for launch on November fourth, and follow for part two, thirty to sixty.', 6.0)


HORDE30 = [
    hook('HORDE', 'orc & troll from step 1  ·  tauren / undead / Skyborne join at step 5'),
    tips('hearth: Razor Hill, Crossroads, Taurajo, Orgrimmar'),
    step(1, '1 - 4', 'Durotar', 'Valley of Trials',
         ['Cutting Teeth, Sarkoth, Sting of the Scorpid', 'Lazy Peons, Thazz\'ril\'s Pick', 'Burning Blade cave at the end', 'hearth stays in the Valley'],
         "Step one, the Valley of Trials: Cutting Teeth, Sarkoth, Sting of the Scorpid, Lazy Peons and Thazz'ril's Pick. Finish with the Burning Blade cave."),
    step(2, '5 - 6', 'Durotar', "Sen'jin Village",
         ['Report to Sen\'jin: grab all 6 quests', 'crabs, makrura, Tiragarde Keep', "The Admiral's Orders"],
         "Step two: Sen'jin Village. Take all six quests, clear the coast, crabs and makrura, and Tiragarde Keep for The Admiral's Orders."),
    step(3, '7 - 9', 'Durotar', 'Razor Hill (hearth)',
         ['beach toolboxes, Razormane quilboars', 'swim to the Echo Isles: Zalazane', 'Encroachment, harpies: Securing the Lines'],
         'Step three: hearth in Razor Hill. Beach toolboxes, the quilboars, a swim to the Echo Isles for Zalazane, then the harpies.'),
    step(4, '10 - 11', 'Durotar', 'Orgrimmar  ·  Thunder Ridge',
         ['Hidden Enemies, Cleft of Shadows', 'Thunder Ridge: Fizzle Darkstorm', 'train, then walk into the Barrens'],
         'Step four: Orgrimmar for Hidden Enemies and the Cleft of Shadows, Thunder Ridge for Fizzle Darkstorm, then walk into the Barrens.'),
    step(5, '11 - 12', 'The Barrens', 'Far Watch  ·  The Crossroads',
         ['Skull Rock cultists, The Demon Seed', 'flight path + hearth: Crossroads', 'tauren, undead, Skyborne: join here'],
         'Step five: the Crossroads. Take the flight path, set your hearth, and grab every quest. Tauren, undead and Skyborne join the route here.'),
    step(6, '12 - 13', 'The Barrens', 'Crossroads ring',
         ['plainstriders, raptors, Forgotten Pools', 'Barak Kodobane + Kolkar Leaders', 'Ratchet: flight path, pirates, Dizzywig'],
         'Step six: plainstriders, raptors and the Forgotten Pools, Barak Kodobane and the Kolkar leaders. Then Ratchet: flight path and the pirates.'),
    step(7, '14', 'The Barrens', 'Thunder Bluff run  ·  Camp Taurajo',
         ['run to Thunder Bluff: flight path', "Mankrik's wife, Samophlange", 'Echeyakee, Kreenig Snarlsnout'],
         "Step seven: a run to Thunder Bluff for the flight path, then Mankrik's wife, Samophlange, Echeyakee and Kreenig Snarlsnout."),
    step(8, '15 - 16', 'The Barrens', 'Stagnant Oasis  ·  Camp Taurajo (hearth)',
         ['Verog the Dervish', 'Raptor Grounds, Lushwater Oasis', 'Hezrul Bloodmark, Raptor Horns'],
         'Step eight: the Stagnant Oasis and Verog, then hearth in Camp Taurajo. Raptor Grounds, Lushwater Oasis, Hezrul Bloodmark.'),
    step(9, '13 - 18', 'Orgrimmar', 'Ragefire Chasm',
         ['all RFC quests in Orgrimmar', 'Taragaman + Bazzalan', '+20% dungeon XP in Forever'],
         'Step nine: Ragefire Chasm, right under Orgrimmar. Grab every quest first. With the Forever XP boost, one run is worth it.'),
    step(10, '17', 'Stonetalon Mountains', "Sludge Fen  ·  Mor'shan  ·  Ashenvale",
         ['Ignition + The Escape', 'Ashenvale flight paths: Splintertree, Zoram\'gar', 'Stonetalon: Avenge My Village, Protect Kaya'],
         "Step ten: Sludge Fen for Ignition and The Escape, the Ashenvale flight paths, then Stonetalon: Avenge My Village and Protect Kaya."),
    step(11, '18 - 19', 'The Barrens', "Malaka'jin  ·  Boulder Lode  ·  Northwatch",
         ['Blood Feeders, Leaders of the Fang', 'Boss Copperplug', 'Tribes at War, Cannoneer Smythe'],
         "Step eleven: Malaka'jin, the Leaders of the Fang, Boss Copperplug, Tribes at War, and Northwatch Hold to close the Barrens."),
    step(12, '20', 'The Barrens', 'Wailing Caverns',
         ['quests at the oasis entrance + Crossroads', 'Serpentbloom, Leaders of the Fang', 'or Shadowfang Keep'],
         'Step twelve: Wailing Caverns at twenty, with the quests from the oasis and the Crossroads. Shadowfang Keep works too.'),
    step(13, '21 - 22', 'Tirisfal Glades', 'Undercity  ·  Brill',
         ['A Frightened Request, Light\'s Justice', "The Wrath of Rath'mael (Brill)", 'Unending Torment chain, The New Plague'],
         "Step thirteen: zeppelin to the Undercity. Grab the new Ruins of Lordaeron quests: A Frightened Request, Light's Justice, Rath'mael and the Unending Torment chain.",
         new='Ruins of Lordaeron (21-22), 9 quests'),
    step(14, '22', 'Hillsbrad Foothills', 'Tarren Mill',
         ['Sepulcher flight path', 'Durnholde Keep: free the prisoners', 'Tarren Mill flight path'],
         "Step fourteen: the Sepulcher flight path, then Tarren Mill and Durnholde Keep."),
    step(15, '23', 'Hillsbrad Foothills', 'Hillsbrad Fields',
         ['the farmers, Stanley', 'the town and the fields', 'turn in at Tarren Mill'],
         'Step fifteen: Hillsbrad Fields, the farmers and Stanley, then back to Tarren Mill.'),
    step(16, '24', 'Ashenvale', "Zoram'gar  ·  Splintertree Post",
         ['Vorsha the Lasher, Muglash escort', 'Thistlefur Village', 'Torek\'s Assault on Silverwing'],
         "Step sixteen: Ashenvale. Zoram'gar for Vorsha and Muglash, Thistlefur Village, and Torek's Assault."),
    step(17, '25', 'Ashenvale', 'Mystral Lake  ·  Greenpaw',
         ['Mystral Lake quests', 'Greenpaw village', 'then Bael Modan in the Barrens'],
         'Step seventeen: Mystral Lake and Greenpaw, then Bael Modan in the Barrens.'),
    step(18, '26 - 27', 'Ashenvale', 'Satyrnaar  ·  Blackfathom Deeps',
         ['Shadumbra, Laughing Sisters', 'Satyrnaar, Sharptalon', "Blackfathom Deeps near Zoram'gar"],
         'Step eighteen: Shadumbra, the Laughing Sisters, Satyrnaar and Sharptalon. Then Blackfathom Deeps.'),
    step(19, '28', 'Hillsbrad Foothills', 'Tarren Mill round 2',
         ['the forge, the town, the mine', 'Mudsnout gnolls', 'then the Great Lift to Thousand Needles'],
         'Step nineteen: Tarren Mill again: the forge, the town, the mine and the Mudsnout gnolls.'),
    step(20, '28 - 29', 'Thousand Needles', 'Freewind Post',
         ['centaurs, Test of Faith', 'Alien Egg, Highperch wyverns', 'Darkcloud Pinnacle, Screeching Canyon'],
         'Step twenty: Thousand Needles from Freewind Post. Centaurs, Test of Faith, Highperch and Darkcloud Pinnacle.',
         new='10 new quests in the zone'),
    step(21, '29 - 30', 'Wetlands', 'Excavation Site',
         ['Changing Tastes (Orgrimmar)', 'Dragonmaw Rumors: Deathstalker Agent', 'Open the Maw, Elder Knowledge, Earthen Echo'],
         'Step twenty one: the new Excavation Site dungeon. Changing Tastes from Orgrimmar, then the Deathstalker agent above the Dragonmaw camp.',
         new='Excavation Site (28-31), 5 quests'),
    step(22, '30', 'Hillsbrad Foothills', 'Tarren Mill: Magus Wordeen Voidglare',
         ['Prison Break In', 'Dalaran Patrols', 'Key to the City: City of Dalaran unlocked'],
         'And at thirty: Magus Wordeen Voidglare in Tarren Mill. His three quests unlock the City of Dalaran.',
         new='City of Dalaran chain'),
    outro(),
]

ALLI30 = [
    hook('ALLIANCE', 'human from step 1  ·  dwarf, gnome, night elf, Skyborne join at step 5-6'),
    tips('hearth: Goldshire, Auberdine, Lakeshire, Menethil'),
    step(1, '1 - 4', 'Elwynn Forest', 'Northshire Abbey',
         ['wolves + kobolds to level 2', 'Defias, Garrick Padfoot', 'then Goldshire: set your hearth'],
         'Step one, Northshire: wolves and kobolds to level two, the Defias and Garrick Padfoot. Then hearth in Goldshire.'),
    step(2, '4 - 6', 'Elwynn Forest', 'Goldshire',
         ['Fargodeep Mine', 'Stonefield + Maclure farms', 'Goldtooth, Billy'],
         'Step two: Fargodeep Mine and the farms, Goldtooth and Billy.'),
    step(3, '6 - 9', 'Elwynn Forest', 'Eastvale',
         ['Jasperlode Mine, Crystal Lake kelp', 'Guard Thomas, Eastvale logging', "Stormwind: Elmore's Task"],
         "Step three: Jasperlode Mine, Crystal Lake, Guard Thomas and Eastvale, then Stormwind for Elmore's Task."),
    step(4, '9 - 10', 'Dun Morogh', 'Deeprun Tram  ·  Ironforge',
         ['Ironforge: flight path + hearth', 'the quarry, Public Servant', 'tunnel north to Loch Modan'],
         'Step four: the tram to Ironforge, flight path and hearth, a few Dun Morogh quests, then the tunnel to Loch Modan.'),
    step(5, '10 - 11', 'Loch Modan', 'Thelsamar',
         ['first Thelsamar quests', 'fly back to Ironforge', 'Menethil, then the boat to Darkshore'],
         'Step five: Thelsamar, then Menethil Harbor and the boat to Darkshore. Dwarves and gnomes join here.'),
    step(6, '11 - 13', 'Darkshore', 'Auberdine (hearth)',
         ['grab every Auberdine quest', "Bashal'aran, the Red Crystal", 'night elves + Skyborne: join here'],
         "Step six: hearth in Auberdine and take every quest. Bashal'aran and the red crystal. Night elves and Skyborne join here."),
    step(7, '13 - 15', 'Darkshore', "Ameth'Aran  ·  the coast",
         ["Ameth'Aran ruins", 'deep ocean quests', 'hearth back to Ironforge'],
         "Step seven: Ameth'Aran and the ocean quests, then hearth back to Ironforge."),
    step(8, '15 - 16', 'Dun Morogh', 'Old Ironforge: Hall of Thanes',
         ['Old Ironforge Incursion: Durgen Dirgehammer', 'The Restless Dead, Important Heirlooms', 'An Ancient Grudge (inside)'],
         'Step eight: the new Hall of Thanes, beneath Old Ironforge. Four quests: Old Ironforge Incursion, The Restless Dead, Important Heirlooms and An Ancient Grudge.',
         new='Hall of Thanes (15-16), 4 quests'),
    step(9, '16', 'Westfall', 'Stormwind  ·  Sentinel Hill',
         ['Cathedral: Tome of Divinity (paladins)', 'Sentinel Hill flight path', 'fly to Lakeshire'],
         'Step nine: Stormwind, the Westfall flight path at Sentinel Hill, then fly to Lakeshire.'),
    step(10, '16 - 18', 'Redridge Mountains', 'Lakeshire (hearth)',
         ['lake items + murlocs', 'gnoll camps', 'hearth Lakeshire, fly out'],
         'Step ten: Redridge from Lakeshire: the lake, the murlocs and the gnolls.'),
    step(11, '18', 'Loch Modan', 'Thelsamar (hearth)',
         ['the dam, Hunter\'s Lodge', 'Gathering Idols', 'quarry troggs'],
         "Step eleven: Loch Modan round two: the dam, the Hunter's Lodge, Gathering Idols and the quarry troggs."),
    step(12, '18 - 20', 'Darkshore', 'Auberdine round 2',
         ['Onu, Murkdeep', 'Twilight Camp, furbolgs, Xabraxxis', 'Absent Minded Prospector escort'],
         'Step twelve: Darkshore again: Onu, Murkdeep, the Twilight camp, the furbolgs and the prospector escort.'),
    step(13, '20 - 21', 'Ashenvale', "Maestra's Post  ·  Astranaar (hearth)",
         ["Maestra's Post quests", 'Zoram Strand: Talen, Ruuzel', 'boat back to Menethil'],
         "Step thirteen: walk south to Maestra's Post, hearth in Astranaar, and the Zoram Strand."),
    step(14, '21 - 22', 'Wetlands', 'Menethil Harbor',
         ['murlocs, gnolls, crocolisks', 'Tramping Paws, Fire Taboo (optional)', 'Ruins of Lordaeron quests: Stormwind'],
         'Step fourteen: the Wetlands from Menethil: murlocs, gnolls and crocolisks. And grab the new Ruins of Lordaeron quests in Stormwind.',
         new='Ruins of Lordaeron (21-22)'),
    step(15, '22 - 23', 'Redridge Mountains', 'Lakeshire round 2',
         ['Yowler, the gnolls', 'Lieutenant Fangore', 'then run south to Darkshire'],
         'Step fifteen: Redridge again: Yowler and Lieutenant Fangore.'),
    step(16, '23 - 24', 'Duskwood', 'Darkshire',
         ['Raven Hill, Sven\'s Camp', 'the Stalvan chain starts', 'Blind Mary, the graveyard'],
         "Step sixteen: Duskwood from Darkshire. Raven Hill, Sven's Camp, Blind Mary, and the start of the Stalvan chain."),
    step(17, '24 - 25', 'Ashenvale', 'Astranaar',
         ['furbolgs, Iris Lake', 'the Moonwell', 'Ruins of Stardust'],
         'Step seventeen: Ashenvale: furbolgs, Iris Lake, the moonwell and the Ruins of Stardust.'),
    step(18, '25 - 26', 'Wetlands', 'Menethil (hearth)',
         ['Dun Modr, Ironbeard\'s Tomb', 'Thandol Span letter', 'Highland Hides (Menethil tanner)'],
         "Step eighteen: the Wetlands: Dun Modr, Ironbeard's Tomb, the Thandol Span letter, and the new Highland Hides quest.",
         new='Highland Hides'),
    step(19, '26 - 27', 'Duskwood', 'Darkshire  ·  Stockade (optional)',
         ['Westfall: Sven, Raven Hill, Jitters', 'Stockade run if you have a group', 'fly to Stormwind'],
         'Step nineteen: Duskwood and Westfall again, with an optional Stockade run.'),
    step(20, '27 - 28', 'Ashenvale', 'Shrine of Aessina  ·  Forest Song',
         ['Fallen Sky Lake, the satyrs', 'Forest Song flight path', 'Wetlands wreckage: Cursed Crew'],
         "Step twenty: the Wetlands wreckage, then Ashenvale: the Shrine of Aessina, Fallen Sky Lake, Forest Song and the satyrs."),
    step(21, '28 - 30', 'Wetlands', 'Excavation Site',
         ['Menethil: Seeking Caitlin, Heartwoven', 'Songblade Search, Horrors in the Highland', 'Titan Relic: Prehistoric Prism (Ironforge)'],
         'Step twenty one: the new Excavation Site. Nine Alliance quests from Menethil Harbor: Caitlin, the Songblade brothers, the Highland Horror and the Titan Relic.',
         new='Excavation Site (28-31), 9 quests'),
    step(22, '29 - 30', 'Duskwood', 'Darkshire (hearth)',
         ["Mor'ladim, Abercrombie", 'Raven Hill, Sven', 'Old Town: Dashel Stonefist at 30'],
         "Step twenty two: Duskwood to finish: Mor'ladim, Abercrombie and Raven Hill."),
    step(23, '30', 'Hillsbrad Foothills', 'Southshore: Emissary Jacques',
         ['An Alarming Request', 'Image of Archmage Modera', 'City of Dalaran unlocked'],
         'And at thirty: Emissary Jacques in Southshore starts the City of Dalaran chain.',
         new='City of Dalaran chain'),
    outro(),
]

PLANX = HORDE30 if FACTION == 'horde' else ALLI30


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
