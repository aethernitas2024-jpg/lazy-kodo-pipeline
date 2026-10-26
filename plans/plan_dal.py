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
    (tcard('set1', 'NEW CLOTH SET  ·  1 / 2', "VIOLET SORCERER'S", VIO, VIOG, [273051, 286988, 286989], []),
     'dalaran', "The new cloth set, Violet Sorcerer's Vestments. Five pieces, item level thirty two to thirty five: the mantle, the leggings, and the wraps with one percent hit.", 8.0),
    (tcard('set2', 'NEW CLOTH SET  ·  2 / 2', 'VESTMENTS', VIO, VIOG, [286987, 273044], []),
     'dalaran', 'And the sandals, plus the Arcanowisp Robes, which can reduce your threat when you get hit.', 6.0),
    (card('bonus', "VIOLET SORCERER'S VESTMENTS", 'SET BONUSES', VIO, VIOG, [273051, 286988, 286987, 286989, 273044],
          [('2  +5 Arcane Resistance', BONE, 46), ('3  +10 Spirit', BONE, 46),
           ('4  spells can let mana regen continue', AMBER, 42), ('while casting  ·  doubled in Cities', AMBER, 42),
           ('5  chance to summon an Arcane', SICK, 46), ('Elemental to fight with you', SICK, 46)], size=110, isz=110),
     'dalaran', 'The set bonuses come from the game files. Four pieces: your damaging spells can let mana regeneration keep going while you cast, doubled in Strongholds and Cities. '
                'Five pieces: a chance to summon an arcane elemental that fights with you.', 8.0),
    (outro_png, 'dalaran', 'Save this for your Dalaran run, and follow for more WoW Forever dungeon guides.', 3.5),
]
