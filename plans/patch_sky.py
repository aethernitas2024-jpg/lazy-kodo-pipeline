p = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\gather\build_tierchar.py'
s = open(p, encoding='utf-8').read()
a = "       ('scourge', 'UNDEAD'), ('tauren', 'TAUREN'), ('troll', 'TROLL')]"
b = "       ('scourge', 'UNDEAD'), ('tauren', 'TAUREN'), ('troll', 'TROLL'), ('skyborne', 'SKYBORNE')]"
assert a in s; s = s.replace(a, b, 1)
# Skyborne (races 95 High Order / 96 Windshaper, ChrModel 218/219): warrior hunter rogue druid (both), mage (95), shaman (96)
for cls in ('warrior', 'hunter', 'rogue', 'druid', 'mage', 'shaman'):
    key = "'%s': '" % cls
    i = s.index(key, s.index('PLAYABLE = {'))
    j = s.index("'", i + len(key))
    s = s[:j] + ' skyborne' + s[j:]
a = "       'warlock': ['troll']}.get(CLS, [])"
b = "       'warlock': ['troll']}.get(CLS, []) + ['skyborne']"
assert a in s; s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(s)
print('patched')
