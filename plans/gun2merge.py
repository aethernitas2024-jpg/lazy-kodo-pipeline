import os
G = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\gather'
S = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\gun2plan.py'
s = open(os.path.join(G, 'build_rares.py'), encoding='utf-8').read()
plan = open(S, encoding='utf-8').read()
a = s.index('RARES = ['); b = s.index('PLAN = RARES')
s = s[:a] + plan + '\n\n' + s[b:]
s = s.replace('PLAN = RARES', 'PLAN = GUN')
s = s.replace("KIND = 'rares'", "KIND = 'bumpgun2'")
s = s.replace("OUT = r'C:\\Users\\d2460n\\Videos\\World Of Warcraft\\WoW Forever - rares worth hunting 20-30 (EN).mp4'",
              "OUT = r'C:\\Users\\d2460n\\Videos\\World Of Warcraft\\WoW Forever - RIP Booty Bay bump gun, hotfixed (EN).mp4'")
assert 'hotfixed (EN)' in s and 'PLAN = GUN' in s
s = s.replace('seed=i * 37 + 59', 'seed=i * 31 + 17')
d = s.index('"""', s.index('"""') + 3)
head = ('# -*- coding: utf-8 -*-\n"""Short: the Booty Bay Bruiser\'s Buckshot knockback gun in WoW Forever (06/10/2026).\n\n'
        '    py -3.11 build_bumpgun2.py\n\n'
        'Item 274748 (nether tooltip), vendor Gezzy Gunkgear npc 265575 at Stranglethorn 28.2,74.8, cost 31088 copper.\n'
        'Spell 1295313 (client 70205): Effect 98 knockback, base 50 / misc 400, ImplicitTarget 25 (any unit), range 10-40, CD 600000.\n'
        'Works on allies + slow fall trick: Wowhead comment (said as player report).\n')
s = head + s[d:]
open(os.path.join(G, 'build_bumpgun2.py'), 'w', encoding='utf-8').write(s)
print('ok')
