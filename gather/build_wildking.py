# -*- coding: utf-8 -*-
"""Short (lore): who is the Wild King, Hyjal Summit final boss in WoW Forever (07/10/2026).

    py -3.11 build_wildking.py

Source: Documents\aout\WoWForever\WILD-KING.md (client 1.60.1.70245: SpellName/Spell/SpellMisc, ItemSparse 268967/273659,
Achievement 63580, helm_armor_wildkingc60). Gloomrise chain: Wowhead Forever. Theory cards are labelled as such.
"""
import os
import sys

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title, pill
from build_whimsy import line
import build_hyjal as HY

KIND = 'wildking'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - who is the Wild King (EN).mp4'
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
    y = line(im, 'more WoW Forever secrets every week', y + 40, 50, SICK)
    line(im, 'beta files  ·  may still change', y + 16, 40, GREY)
    return save(im, WORK, 'outro')


from build_whimsy import map_card
import build_cozy as C
C.WORK = WORK
PIN = (255, 190, 80, 255)
HORDE = (235, 90, 80, 255)
ALLI = (110, 170, 255, 255)
BOTH = (140, 225, 110, 255)
BLUEQ = (60, 140, 255, 255)


def mcard(name, kicker, big, col, glow, zone, pts, rows, zoom=None, mw=760, size=110):
    """Card with a zone map and pins, then lines."""
    def fn():
        im = blank()
        B.backdrop(im, 900, 800, 760, 185)
        y = head(im, kicker, big, col, glow, y=250, size=size)
        y = map_card(im, C.zmap(zone, pts, mw, zoom=zoom), y + 40)
        for t, c, s in rows:
            y = line(im, t, y + 16, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


WILD = (150, 230, 120, 255)
WILDG = (40, 110, 40, 255)
THEORY = (200, 170, 255, 255)

WK = [
    (card('hook', 'WOW FOREVER  ·  HYJAL SUMMIT', 'WHO IS THE WILD KING?', WILD, WILDG, [7813852, 1396983, 2011150],
          [('the final boss of the Hyjal raid', BONE, 50), ('everything the game files reveal', AMBER, 48),
           ('+ our theory', THEORY, 46)], size=96, isz=150),
     'hyjalmap', "Who is the Wild King? He's the final boss of WoW Forever's Hyjal raid. Here's everything the game files reveal, and our theory.", 6.0),
    (card('powers', 'IN THE GAME FILES', 'HIS POWERS', WILD, WILDG, [1394953, 136116, 840405, 1670851],
          [('Dreamfall: the Emerald Dream in turmoil', BONE, 42), ('Convoke the Spirits: wild spirits rush you', BONE, 42),
           ('Assimilation: your life flows back to him', BONE, 42), ('Royal Defiance: he draws on Nordrassil', AMBER, 42)],
          size=150, isz=120),
     'hyjalmap', "His spells are already in the files. Dreamfall throws the Emerald Dream into turmoil. Convoke the Spirits sends wild spirits at you. "
                 "Assimilation drains your life back to him. And Royal Defiance: he draws power from Nordrassil itself.", 9.0),
    (card('wildform', 'PHASE 2', 'WILD FORM', WILD, WILDG, [2011150, 2027952],
          [('"overwhelmed by his own powers..."', AMBER, 44), ('"...a horrific new form"', AMBER, 44),
           ('he takes the forms of Wild Gods:', BONE, 44), ('a spider  ·  a thunder lizard', SICK, 46),
           ('+ Druids of the Claw and of the Talon', BONE, 42)], size=160, isz=140),
     'hyjalmap', "Then phase two, Wild Form. Quote: overwhelmed by his own powers, the Wild King assumes a horrific new form, "
                 "with the abilities of several Wild Gods. A spider, a thunder lizard. And he calls Druids of the Claw and of the Talon.", 10.0),
    (card('token', 'HIS TOKEN', 'BEAR? STAG? EAGLE?', AMBER, (200, 120, 40, 255), [1396983],
          [('"Token of the Wild King"', BONE, 46), ('"a crude necklace... bear? stag? eagle?', AMBER, 42),
           ('Steaglebear?"', AMBER, 46), ('bear, stag, eagle: three Wild Gods?', THEORY, 42)], size=130, isz=170),
     'moonglademap', "His token is a crude necklace, and the game itself jokes: a bear? A stag? An eagle? Steaglebear? "
                     "Bear, stag and eagle sound a lot like three Wild Gods.", 7.0),
    (card('pact', 'THE FIRST CLUE  ·  MULGORE', 'THE PACT', HORDE, (150, 40, 30, 255), [237431, 134938],
          [('Gloomrise: Broodmother Valraxx', BONE, 44), ('a druid twisted into a spider', AMBER, 44),
           ('her letter mentions "The Pact"', BONE, 44), ('... and a "Wild King"', SICK, 48),
           ('Horde quest chain, level 30', GREY, 40)], size=160, isz=140),
     'kalimdor', "The first clue is already in the game. At Gloomrise in Mulgore, Broodmother Valraxx is a druid twisted into a spider. "
                 "The letter she carries mentions The Pact, and a Wild King.", 8.0),
    (card('theory', 'OUR THEORY  ·  NOT CONFIRMED', 'A DRUID KING', THEORY, (90, 50, 150, 255), [],
          [('a druid who took the Wild Gods\' power', BONE, 44), ('his Pact: druids lost in beast forms', BONE, 44),
           ('his throne: Nordrassil, at Hyjal', AMBER, 46), ('and it is starting to consume him', SICK, 44)], size=150),
     'moonglademap', "Our theory: the Wild King is a druid who took the power of the Wild Gods. His Pact, druids lost in their beast forms. "
                     "His seat of power, Nordrassil. And that power is starting to consume him. Just a theory.", 9.0),
    (card('hidden', 'STILL HIDDEN', 'WHAT WE DON\'T KNOW', WILD, WILDG, [7813852],
          [('his look and his real name: server-side', BONE, 42), ('the thunder lizard quest: not found yet', BONE, 42),
           ('but his HELM is already in the files', AMBER, 46), ('modelled for every race', SICK, 42)], size=110, isz=170),
     'hyjalmap', "Still hidden: his look and his real name are server side, and we haven't found a thunder lizard quest yet. "
                 "But his helm is already in the files, modelled for every race.", 8.0),
    (outro_png, 'hyjalmap', 'Who do you think the Wild King is? Tell me in the comments, and follow for more WoW Forever secrets.', 4.5),
]


PLAN = WK
MUSIC = 'hyjal'


def main():
    files, tl, say, t = [], [], [], 0.0
    for i, (fn, art, text, mind) in enumerate(PLAN):
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        files.append(BP.shot(WORK, i, art, dur, seed=i * 23 + 11,
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
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
