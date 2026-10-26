# -*- coding: utf-8 -*-
"""Short: City of Dalaran dungeon guide for WoW Forever (build 1.60.1.70170, 02/10/2026).

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

KIND = 'dalaran'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - City of Dalaran dungeon guide (EN).mp4'
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
VIO = (190, 140, 255, 255)
VIOG = (90, 40, 160, 255)


def tcard(name, kicker, big, col, glow, items, rows, size=100, tsize=34, twidth=860):
    """Card with real in-game tooltips (Wowhead Forever), then short lines."""
    def fn():
        im = blank()
        B.backdrop(im, 900, 820, 800, 185)
        y = head(im, kicker, big, col, glow, y=230, size=size)
        y = TT.paste(im, items, y + 30, width=twidth, size=tsize, gap=18)
        for t, c, s in rows:
            y = line(im, t, y + 4, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


DAL = [
    (card('hook', 'WOW FOREVER  ·  NEW DUNGEON', 'CITY OF DALARAN', VIO, VIOG, [273044, 251961, 279841],
          [('level 33  ·  quests from level 24', AMBER, 52), ('how to unlock the entrance', BONE, 46),
           ('8 quests  ·  9 bosses  ·  new cloth set', SICK, 46)], size=110, isz=140),
     'dalaran', 'City of Dalaran, a brand new dungeon in WoW Forever. How to unlock the entrance, every quest, every boss, and the new cloth set.', 5.0),
    (mcard('alli_unlock', 'UNLOCK  ·  ALLIANCE  ·  LEVEL 30', 'SOUTHSHORE', ALLI, (40, 80, 160, 255), 'Hillsbrad',
           [(48.3, 60.1, 'A', ALLI)],
           [('Emissary Jacques (48, 60)', AMBER, 46), ('An Alarming Request', BONE, 48),
            ('report to the Image of Archmage Modera', BONE, 42), ('Lordamere Lake shore, Silverpine (68, 45)', GREY, 40),
            ('she gives the key: Heart of Disruption', SICK, 42)], zoom=(20, 25, 85, 85), mw=820, size=120),
     'dalaran', "Alliance: at level thirty, talk to Emissary Jacques in Southshore. An Alarming Request sends you to the Image of Archmage Modera, "
                'on the Silverpine shore of Lordamere Lake. She hands you a key and the quest Heart of Disruption.', 6.5),
    (mcard('horde_unlock', 'UNLOCK  ·  HORDE  ·  LEVEL 30', 'TARREN MILL', HORDE, (150, 40, 30, 255), 'Hillsbrad',
           [(61.6, 20.6, 'H', HORDE)],
           [('Magus Wordeen Voidglare (62, 21)', AMBER, 44), ('finish all 3: Prison Break In,', BONE, 42),
            ('Dalaran Patrols, Key to the City', BONE, 42), ('the Sewer Key opens Blood in the Streets', SICK, 40),
            ("Keeper Bel'Varil's quests: optional", GREY, 38)], zoom=(30, 0, 95, 60), mw=820, size=120),
     'dalaran', "Horde: in Tarren Mill, finish all three quests from Magus Wordeen Voidglare: Prison Break In, Dalaran Patrols and Key to the City. "
                "That unlocks the next step of the chain. Keeper Bel'Varil's quests in the same house are optional.", 7.0),
    (mcard('entrance', 'GETTING IN', 'NEW DALARAN', VIO, VIOG, 'Alterac',
           [(16.7, 65.9, 'D', VIO), (17.0, 52.0, 'S', HORDE)],
           [('D  the rebuilt city, west Alterac', BONE, 44), ('S  Horde: the sewers, north edge of the city', HORDE, 40),
            ("Alliance: Modera's key gets you inside", ALLI, 40), ('meet her at the Violet Citadel', AMBER, 42)],
           zoom=(0, 35, 45, 95), mw=820, size=120),
     'dalaran', "Dalaran has been rebuilt in western Alterac, behind its barrier. The Horde sneaks in through the sewers on the north edge, "
                "the Alliance uses Modera's key. Both meet her inside, at the Violet Citadel.", 6.0),
    (card('heart', 'MAIN QUEST  ·  BOTH FACTIONS', 'HEART OF DISRUPTION', AMBER, (200, 120, 40, 255), [251961, 279839, 279840, 279841],
          [('Arcane Mote: Shade of the Archmage', BONE, 44), ('top of the Violet Citadel', GREY, 40),
           ('then hand it to Archmage Celindra', BONE, 42), ('Alliance: Spellguard Pauldrons, Renewing', AMBER, 38),
           ('Footpads or Defender of Dalaran (mace)', AMBER, 38), ('Horde: Battle Spaulders, Enchanted Sandals', HORDE, 38),
           ('or Striking Staff  ·  all item level 36', HORDE, 38)], size=100, isz=120),
     'dalaran', 'The main quest: grab the Arcane Mote from the Shade of the Archmage, at the top of the Violet Citadel, then bring it to Archmage Celindra. '
                'Item level thirty six blue rewards for both factions.', 7.0),
    (card('alli_q', 'ALLIANCE  ·  3 MORE QUESTS', 'GRAB THESE TOO', ALLI, (40, 80, 160, 255), [279835, 279837, 251962],
          [('A Green Sample: Shylamiir, Stormwind', AMBER, 42), ('herbalist in the park (31, 63)', GREY, 38),
           ('Fel Infused Blossom: central garden', BONE, 40), ('Starving Arcane: Image of Modera', AMBER, 42),
           ('8 + 8 Remnants, 8 Mana Echoes: 2 runs', BONE, 40), ('Power Overwhelming: Andromath, SW', AMBER, 42),
           ('defeat the Mana Elemental', BONE, 40)], size=110, isz=120),
     'dalaran', "Alliance, three more: A Green Sample, from Shylamiir in the Stormwind park. Starving Arcane, from Modera's image: players say "
                'there are not enough elementals for one run. And Power Overwhelming, from High Sorcerer Andromath: defeat the Mana Elemental.', 8.0),
    (card('horde_q', 'HORDE  ·  3 MORE QUESTS', 'GRAB THESE TOO', HORDE, (150, 40, 30, 255), [251963, 279845, 279847],
          [('The Grave Knight: Melisara, Tarren Mill', AMBER, 40), ('defeat Atrexis the Grave Knight', BONE, 40),
           ('Opportunistic Education: Rexxie', AMBER, 40), ('at the sewers: the Founding of Dalaran book', BONE, 38),
           ('past the portal room, back wall', GREY, 38), ('Source of Power: Dr. Martin Felben, UC', AMBER, 40),
           ('6 Cracked Sentry Cores (split drops)', BONE, 40)], size=110, isz=120),
     'dalaran', 'Horde, three more: The Grave Knight, from Melisara in Tarren Mill. Opportunistic Education, from Rexxie at the sewer entrance: '
                'the book sits past the portal room, on the back wall. And Source of Power from the Undercity: six sentry cores.', 8.0),
    (card('bosses', 'INSIDE  ·  9 ENCOUNTERS', 'THE BOSSES', VIO, VIOG, [],
          [('1  Arcane Anomaly', BONE, 44), ('2  Fel Ancient', BONE, 44), ('3  Mana Devourer', BONE, 44),
           ('4  Mana Elemental', BONE, 44), ('5  Unstable Sentinel', BONE, 44), ('6  Shade of the Archmage', AMBER, 46),
           ('7  Lyn the Ignored  ·  RARE', SICK, 44), ('8  Atrexis the Grave Knight', BONE, 44), ('9  Mana Wraith', BONE, 44)],
          size=120),
     'dalaran', 'Nine encounters, in the order of the game files. The Shade of the Archmage counts for the dungeon achievement. '
                'Lyn the Ignored is a rare elite: nobody has found the spot yet. Tell me if you do.', 7.5),
    (tcard('set1', 'NEW CLOTH SET  ·  1 / 3', "VIOLET SORCERER'S", VIO, VIOG, [273051, 286988], []),
     'dalaran', "The new cloth set, Violet Sorcerer's Vestments. Five pieces, item level thirty two to thirty five. The mantle, and the leggings with spell power.", 7.0),
    (tcard('set2', 'NEW CLOTH SET  ·  2 / 3', 'VESTMENTS', VIO, VIOG, [286989, 286987], []),
     'dalaran', 'The wraps, with one percent hit, and the sandals.', 5.5),
    (tcard('set3', 'NEW CLOTH SET  ·  3 / 3', 'ARCANOWISP ROBES', VIO, VIOG, [273044], []),
     'dalaran', 'And the Arcanowisp Robes, which can reduce your threat when you get hit.', 5.0),
    (card('bonus', "VIOLET SORCERER'S VESTMENTS", 'SET BONUSES', VIO, VIOG, [273051, 286988, 286987, 286989, 273044],
          [('2  +5 Arcane Resistance', BONE, 46), ('3  +10 Spirit', BONE, 46),
           ('4  spells can let mana regen continue', AMBER, 42), ('while casting  ·  doubled in Cities', AMBER, 42),
           ('5  chance to summon an Arcane', SICK, 46), ('Elemental to fight with you', SICK, 46)], size=110, isz=110),
     'dalaran', 'The set bonuses come from the game files. Four pieces: your damaging spells can let mana regeneration keep going while you cast, doubled in Strongholds and Cities. '
                'Five pieces: a chance to summon an arcane elemental that fights with you.', 8.0),
    (outro_png, 'dalaran', 'Save this for your Dalaran run, and follow for more WoW Forever dungeon guides.', 3.5),
]



PLAN = DAL
MUSIC = 'mage'


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
