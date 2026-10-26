import json as _json
import re as _re
_C = {int(k): v for k, v in _json.load(open(os.path.join(HERE, 'coins.json'), encoding='utf-8')).items()}
NOTES = {286287: 'the future lich just wants a hug', 286281: '"frozen"... foreshadowing?',
         286279: 'a jab at Anduin staying a kid since 2004', 286293: 'he flattened Dalaran. The fountain survived.',
         286273: 'some things never change', 286267: 'a secret crush on High General Abbendis',
         286311: 'a nod to his novel appearances', 286300: "Forever's own raid boss is confused",
         286290: 'Onyxia in disguise', 286302: 'caught in the act', 286327: 'a nod to the Caverns of Time',
         286274: 'the three tones of the Karazhan bells?', 286328: "who copied who's fountain?"}
INTRO = {286290: 'Lady Katrana Prestor, Onyxia in disguise', 286281: 'Arthas, before the fall', 286300: 'Sonya Darkhallow, the Barrow Deeps boss',
         286291: 'Sylvanas, long ago', 286267: 'Arcanist Doan, of the Scarlet Monastery', 286308: 'Attumen the Huntsman'}
# gold first (Kel'Thuzad opens), then silver, copper; the two sad ones close the list
_ORDER = ([286287] + [i for i in GOLDS if i not in (286287, 286291, 286288)] + SILVERS + COPPERS + [286291, 286288])


def _who(i):
    n = _re.sub(r"'s? (Gold|Silver|Copper) Coin$", '', _C[i][0])
    return n.replace("A Footman", 'A Footman')


def _spoken(t):
    t = t.replace('<', '').replace('>', '')
    return t


ALL_COINS = []
for _i in _ORDER:
    _name, _wish = _C[_i]
    _who_ = _who(_i)
    _col = GOLDC if 'Gold' in _name else (SILV if 'Silver' in _name else COPP)
    _intro = INTRO.get(_i, _who_)
    _say = '%s: %s' % (_intro, _spoken(_wish))
    _dur = 4.2
    ALL_COINS.append(coin('c%d' % _i, _i, _who_.upper(), _say, col=_col, dur=_dur, note=NOTES.get(_i)))
