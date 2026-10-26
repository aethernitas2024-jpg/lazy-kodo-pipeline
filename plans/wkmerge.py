import os
G = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\gather'
S = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\wkplan.py'
s = open(os.path.join(G, 'build_rares.py'), encoding='utf-8').read()
plan = open(S, encoding='utf-8').read()
a = s.index('RARES = ['); b = s.index('PLAN = RARES')
s = s[:a] + plan + '\n\n' + s[b:]
s = s.replace('PLAN = RARES', 'PLAN = WK').replace("MUSIC = 'hunter'", "MUSIC = 'hyjal'")
s = s.replace("KIND = 'rares'", "KIND = 'wildking'")
s = s.replace("OUT = r'C:\\Users\\d2460n\\Videos\\World Of Warcraft\\WoW Forever - rares worth hunting 20-30 (EN).mp4'",
              "OUT = r'C:\\Users\\d2460n\\Videos\\World Of Warcraft\\WoW Forever - who is the Wild King (EN).mp4'")
s = s.replace("'more WoW Forever guides every week'", "'more WoW Forever secrets every week'")
assert 'Wild King (EN)' in s and 'PLAN = WK' in s and "MUSIC = 'hyjal'" in s
s = s.replace('seed=i * 37 + 59', 'seed=i * 23 + 11')
d = s.index('"""', s.index('"""') + 3)
head = ('# -*- coding: utf-8 -*-\n"""Short (lore): who is the Wild King, Hyjal Summit final boss in WoW Forever (07/10/2026).\n\n'
        '    py -3.11 build_wildking.py\n\n'
        'Source: Documents\\aout\\WoWForever\\WILD-KING.md (client 1.60.1.70245: SpellName/Spell/SpellMisc, ItemSparse 268967/273659,\n'
        'Achievement 63580, helm_armor_wildkingc60). Gloomrise chain: Wowhead Forever. Theory cards are labelled as such.\n')
s = head + s[d:]
open(os.path.join(G, 'build_wildking.py'), 'w', encoding='utf-8').write(s)
print('ok')
