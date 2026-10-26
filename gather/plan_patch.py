from PIL import ImageFont

ARIAL, ARIALB = 'C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf'
BLUE_TXT = (148, 205, 255, 255)
BLUE_NAME = (0, 180, 255, 255)


def _wrap(d, text, f, maxw):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) > maxw and cur:
            out.append(cur); cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def bluecard(name, kicker, big, section, quotes, size=88, fs=34):
    """Excerpt of Kaivax's blue post (Oct 15 development notes), forum-style, quotes verbatim."""
    def fn():
        im = blank()
        B.backdrop(im, 900, 860, 820, 190)
        y = head(im, kicker, big, BLUE_NAME, (20, 70, 130, 255), y=230, size=size)
        x0, x1 = 70, W - 70
        f, fb, fh = ImageFont.truetype(ARIAL, fs), ImageFont.truetype(ARIALB, fs), ImageFont.truetype(ARIALB, 30)
        lines = []
        for lead, txt in quotes:
            lines.append((lead, _wrap(ImageDraw.Draw(im), txt, f, x1 - x0 - 90)))
        h = 150 + sum(42 + len(t) * (fs + 12) + 14 for _, t in lines)
        top = y + 40
        panel = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(panel).rounded_rectangle((x0, top, x1, top + h), 18, fill=(18, 24, 36, 238), outline=(40, 90, 150, 255), width=3)
        im.alpha_composite(panel)
        d = ImageDraw.Draw(im)
        d.ellipse((x0 + 30, top + 28, x0 + 92, top + 90), fill=(10, 60, 120, 255), outline=BLUE_NAME, width=3)
        d.text((x0 + 61, top + 59), 'K', font=fb, fill=BLUE_NAME, anchor='mm')
        d.text((x0 + 112, top + 30), 'Kaivax', font=fh, fill=BLUE_NAME)
        d.text((x0 + 112, top + 66), 'Blizzard  ·  WoW Forever Beta Development Notes  ·  Oct 15', font=ImageFont.truetype(ARIAL, 24), fill=(150, 160, 175, 255))
        d.text((x0 + 30, top + 112), section, font=fh, fill=(235, 235, 240, 255))
        yy = top + 162
        for lead, wrapped in lines:
            d.text((x0 + 30, yy), lead, font=fb, fill=(235, 210, 120, 255)); yy += 42
            for t in wrapped:
                d.text((x0 + 60, yy), t, font=f, fill=BLUE_TXT); yy += fs + 12
            yy += 14
        return save(im, WORK, name)
    return fn


PC = (120, 230, 200, 255)
PG = (40, 120, 100, 255)
GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)

PATCH = [
    (card('hook', 'WOW FOREVER  ·  PATCH NOTES  ·  OCT 15', 'EVERY RACIAL CHANGED', PC, PG, [],
          [('racials, classes, quality of life', BONE, 44), ('hunter pets nerfed', AMBER, 44),
           ('+ what the newest build hides', SICK, 44)], size=104),
     'vault', "The biggest WoW Forever patch notes of the beta: almost every racial changed, raid wide auras, hunter pet nerfs. "
              "And I dug into the newest build to see what it hides.", 8.0),
    (bluecard('race1', 'RACIALS  ·  PART 1', 'NO MORE WEAPON SPECS', 'Racial Changes', [
        ('Human', 'Sword Specialization: Replaced with Ruthless: 2% increased critical strike chance.'),
        ('Orc', 'Axe Specialization: Replaced with Savage: 1% increased critical strike chance.'),
        ('Orc', 'Shatter Curse: Now dispels Curses and Banes (was granting immunity). Magic damage taken reduced by 5% (was 15%).'),
        ('Dwarf', 'Mace Specialization: Replaced with Earth Fury: 2% increased critical damage and healing.')]),
     'vault', 'Racials, part one: the weapon specializations are gone. Humans get Ruthless, two percent crit. '
              'Orcs get Savage, one percent crit, and Blood Fury drops to three minutes. Dwarves get Earth Fury, '
              'two percent crit damage and healing, and Find Treasure can now give extra loot from chests.', 12.0),
    (bluecard('race2', 'RACIALS  ·  PART 2', 'EVERYONE GETS SOMETHING', 'Racial Changes', [
        ('Tauren', 'Endurance: Now grants 2% increased critical damage and healing (was 1% hit chance).'),
        ('Troll', 'Regeneration: Health regeneration bonuses increased to 20% (was 10%).'),
        ('Gnome', 'Eureka!: Now an 8 second buff with no charges. Same effect on damage and ability costs.'),
        ('Night Elf', 'Quickness: Movement speed increase now stacks with other movement speed increases.'),
        ('Skyborne', 'Wind Blessed: Haste bonus increased to 3% (was 1%).')], fs=32),
     'vault', 'Part two: Tauren get two percent crit damage and healing, with War Stomp at ninety seconds. '
              'Troll regeneration doubles to twenty percent. Undead, Gnome, Night Elf and Skyborne racials are all reworked too.', 11.0),
    (bluecard('class', 'CLASSES  ·  HIGHLIGHTS', 'RAID-WIDE AURAS', 'Class Changes', [
        ('Warrior / Hunter', 'Battle Shout is now Raid wide. Trueshot Aura is now Raid wide.'),
        ('Shaman', 'Grace of Air Totem, Strength of Earth Totem, Windfury Totem, and Flametongue Totem are now Raid wide.'),
        ("Mage", "Frost Blast: This new spell is learned at level 24. It deals damage and slows the target's movement by 40%."),
        ('Shaman', 'Elemental Mastery: This talent has returned as the new 31-point gold medal talent.'),
        ('Paladin', 'Paladins now also learn Revoke when Salvation is learned.')], fs=31),
     'vault', 'Classes: Battle Shout, Trueshot Aura, Moonkin Aura and totems now affect the whole raid. '
              'Mages get Frost Blast at level twenty four, Shamans get Elemental Mastery back, '
              'and Paladins get Salvation, Mass Salvation and a new Revoke ability.', 11.0),
    (bluecard('qol', 'QUALITY OF LIFE', 'SMALL BUT BIG', 'General', [
        ('Wands / Auto Shot', 'Now require you to stand still for 0.5 seconds before shooting, matching early versions of World of Warcraft.'),
        ('Tutorial', 'Added a new tutorial experience for new players.'),
        ('Auction House', 'Auction House now displays a column for equippable level.'),
        ('PvP', 'Battleground Marks of Honor now stack up to 30 (was 20).'),
        ('Dalaran', 'Members of the Horde are no longer welcome in Dalaran under any circumstances and will be attacked on sight.')], fs=31),
     'vault', 'Quality of life: wands and Auto Shot now need half a second standing still. A new tutorial for new players, '
              'the Auction House shows the required level, and the Horde is now attacked on sight in Dalaran.', 10.5),
    (bluecard('pets', 'HUNTERS  ·  PET NERFS', 'DISMEMBER + SONIC BLAST', 'Hunter Pets', [
        ('Dismember (Crocolisk)', 'Healing reduction reduced to 25% (was 50%). Duration reduced to 6 seconds (was 10 seconds). Cooldown increased to 15 seconds (was 6 seconds).'),
        ('Sonic Blast (Bat)', 'Cast speed reduction reduced to 30% (was 60%). Duration reduced to 20 seconds (was 30 seconds). Cooldown increased to 60 seconds (was 30 seconds).'),
        ('Mine! (Bird of Prey)', 'Duration reduced to 3 seconds (was 4 seconds). Cooldown increased to 90 seconds (was 60 seconds).')], fs=31),
     'vault', 'Hunters, sorry: the crocolisk Dismember goes from fifty percent healing reduction for ten seconds, '
              'to twenty five percent for six. Sonic Blast and the bird of prey were nerfed too. '
              'And druids can finally loot the relics they need for Cat Form.', 11.0),
    (card('dm', 'DATAMINE  ·  BUILD 70450', 'WHAT IT HIDES', SICK, (40, 110, 40, 255), [],
          [('Darkspear Islands battleground achievements', AMBER, 36), ('two "Skycutter" transports: Dalaran + Mulgore', BONE, 34),
           ('new areas: Hyjal Crater, Sunken Hollow', BONE, 34), ('Engineering Tinkerbox removed', BONE, 34),
           ('"L70 ETC" spells: Lightning Cloud, Rain of Fire', SICK, 34), ('an Elite Tauren Chieftain fight? no idea yet', GREY, 32)], size=104),
     'vault', 'And in the newest build: achievements for a Darkspear Islands battleground, two Skycutter transports for Dalaran and Mulgore, '
              'new Hyjal Crater and Sunken Hollow areas, and the engineering Tinkerbox removed. '
              'Strangest of all: spells called L70 E T C. An Elite Tauren Chieftain fight? No idea yet.', 13.0),
    (card('outro', 'YOUR TAKE', 'BEST CHANGE?', PC, PG, [],
          [('which racial will you pick now?', AMBER, 44), ('follow for every Forever patch', SICK, 42)], size=110),
     'emeralddream', 'So, which racial will you pick now? Tell me in the comments, and follow for every Forever patch.', 6.0),
]
