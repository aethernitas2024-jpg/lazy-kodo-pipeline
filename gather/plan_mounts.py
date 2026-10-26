GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)
SPEC = (140, 220, 255, 255)
SPECG = (30, 100, 150, 255)

MOUNTS = [
    (card('hook', 'WOW FOREVER  ·  DATAMINE', 'NEW MOUNTS', SPEC, SPECG, ['m_wolf', 'm_rooster', 'm_turtle'],
          [('the newest ones were just decrypted', BONE, 42), ('and Blizzard already answered', AMBER, 44),
           ('+ every Forever mount we know', SICK, 42)], size=130, isz=130),
     'vault', 'New mounts were just decrypted in the WoW Forever beta, and Blizzard already answered. '
              'Here is what they are, and every Forever mount we know about.', 8.0),
    (card('new', 'DECRYPTED  ·  OCTOBER 15-16', 'THE LATEST THREE', SPEC, SPECG, ['m_wolf', 'm_turtle', 'm_rooster'],
          [('Spectral Wolf Pack', AMBER, 48), ('two ghost wolves run beside you', BONE, 38),
           ('party members can join the pack (reported)', GREY, 34),
           ('Verdant Sea Turtle', AMBER, 46), ('Crimson Rooster', AMBER, 46)], size=110, isz=120),
     'vault', 'The latest three: the Spectral Wolf Pack, where two ghost wolves run beside you, and party members could reportedly join your pack. '
              'Plus a Verdant Sea Turtle, and a Crimson Rooster.', 10.0),
    (card('blizz', "BLIZZARD'S ANSWER", 'NOT FOR FOREVER', RED, (150, 40, 30, 255), [],
          [('"these assets are not intended', BONE, 42), ('for this version of World of Warcraft"', BONE, 42),
           ('so where do they go?', AMBER, 44), ('retail, or the Chinese version?', BONE, 40),
           ('the turtle looks like a statue shown in China', GREY, 34)], size=110),
     'vault', 'But Blizzard answered on the forums: these assets are not intended for this version of World of Warcraft. '
              'So where do they go? Maybe retail, maybe the Chinese version: the turtle looks a lot like a statue shown at an event in China.', 10.5),
    (card('confirmed', 'IN FOREVER  ·  WITH A SOURCE', 'THE REAL ONES', GOLDC, GOLDG, ['m_galestrider', 'm_prideclaw', 'm_bear', 'm_kodo'],
          [('Skyborne Galestriders: 4 at level 40, 4 swift at 60', BONE, 34), ('Cerulean Prideclaw: pre-order reward', BONE, 36),
           ('Spectral Bear: Legacy system reward', BONE, 36), ('Pack Kodo: faction supply reward', BONE, 36),
           ('new kodo and skeletal horse colors', BONE, 36), ('Forsaken Charger: undead paladins', AMBER, 36)], size=110, isz=110),
     'vault', 'The ones that really are in Forever: eight Skyborne Galestriders, four at level forty and four swift ones at sixty. '
              'The Cerulean Prideclaw from the pre-order, the Spectral Bear from the Legacy system, the Pack Kodo from faction supplies, '
              'new kodo and skeletal horse colors, and the Forsaken Charger for undead paladins.', 13.0),
    (card('mystery', 'STILL IN THE FILES  ·  NO SOURCE', 'THE MYSTERIES', SHADOW, (90, 40, 150, 255), [],
          [('5 Devilsaurs  ·  4 Warden Sabers', BONE, 42), ('4 Druid Moose  ·  Swift Hyjal Stag', BONE, 42),
           ('Striped Dawnsaber', BONE, 42), ('+ 15 mount items still encrypted', SICK, 42), ('in build 70450 (my datamine)', SICK, 36)], size=110),
     'vault', 'And the mysteries, still in the files with no source: five devilsaurs, four warden sabers, four druid moose, a Swift Hyjal Stag. '
              'And in build seventy four fifty, I count fifteen mount items whose names are still encrypted.', 10.0),
    (card('outro', 'YOUR PICK', 'WHICH ONE DO YOU WANT?', SPEC, SPECG, ['m_wolf', 'm_galestrider', 'm_turtle'],
          [('should Blizzard add the wolf pack?', AMBER, 42), ('follow for every Forever datamine', SICK, 42)], size=96, isz=110),
     'emeralddream', 'Which one do you want? Should Blizzard bring the wolf pack to Forever anyway? Tell me, and follow for every Forever datamine.', 7.0),
]
