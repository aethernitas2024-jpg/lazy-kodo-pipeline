# -*- coding: utf-8 -*-
"""Short: Blackmaw Hold datamine for WoW Forever (build 1.60.1.70170, 02/10/2026).

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

KIND = 'blackmaw'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - Blackmaw Hold, bigger than BRD (EN).mp4'
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


FEL = (130, 230, 90, 255)
FELG = (40, 120, 30, 255)

BM = [
    (card('hook', 'WOW FOREVER  ·  LEVEL 60 DUNGEON', 'BLACKMAW HOLD', FEL, FELG, [276893, 273050, 235256],
          [('bigger than Blackrock Depths', AMBER, 54), ('corrupted furbolgs and demons', BONE, 46),
           ("here's what's already in the game files", SICK, 44)], size=120, isz=150),
     'kalimdor', "Blackmaw Hold, WoW Forever's new level sixty dungeon. The developers say it is bigger than Blackrock Depths. Here is what is already hidden in the game files.", 6.5),
    (card('devs', 'OFFICIAL  ·  DEV PODCAST EP. 3', 'WHAT WE KNOW', AMBER, (200, 120, 40, 255), [],
          [('Azshara, an old unused', BONE, 46), ('Timbermaw Hold entrance', BONE, 46),
           ('larger footprint than BRD', AMBER, 48), ('vertical, non-linear', BONE, 46),
           ('made for level 60, one long session', BONE, 44), ('"tons of secrets"', SICK, 50),
           ('not playable in the beta', RED, 44)], size=120),
     'kalimdor', 'Officially, from the dev podcast: it sits in Azshara, at an old unused Timbermaw entrance. Bigger than Blackrock Depths, vertical and non-linear, built for level sixty, with tons of secrets. And it will not be in the beta.', 9.0),
    (mcard('map', 'AZSHARA', 'A VANILLA LEFTOVER', FEL, FELG, 'Azshara',
           [(38.0, 32.5, '?', AMBER)],
           [('"Blackmaw Hold" already existed in', BONE, 42), ('the 2004 files: an unused area name', BONE, 42),
            ('? the old cave on the Winterspring border', AMBER, 40), ('(our guess, not confirmed)', GREY, 36)],
           zoom=(10, 5, 75, 70), mw=860, size=110),
     'kalimdor', 'Fun fact: Blackmaw Hold was already in the original 2004 files, an unused area name in Azshara. Twenty two years later, it becomes a dungeon. Our guess for the door: the old cave on the Winterspring border.', 8.0),
    (card('rep', 'NEW REPUTATION?', 'THE BLACKMAW FURBOLGS', FEL, FELG, [273050, 235256, 276893],
          [('Blackmaw Pouch:', AMBER, 42), ('"gathered for the Blackmaw furbolgs', BONE, 40), ('in Ursolan to earn their trust"', BONE, 40),
           ('Severed Legashi Horn: same idea', AMBER, 42), ('+ a Blackmaw Ritual Totem', SICK, 42)], size=100, isz=140),
     'kalimdor', 'And not every Blackmaw is hostile. Two items are gathered for the Blackmaw furbolgs in Ursolan, to earn their trust: a Blackmaw Pouch, and Severed Legashi Horns. A friendly furbolg tribe, just like Timbermaw.', 8.0),
    (card('legashi', 'THE DEMONS', 'LEGASHI SATYRS', RED, (150, 40, 30, 255), [235256, 235472, 235645],
          [('Legashi Encampment: a classic Azshara camp', BONE, 40), ('NEW area in the files: Legashi Stronghold', AMBER, 42),
           ('+ Legashi Firewater and its recipe', BONE, 42), ('"Strongholds" = a new Forever content type', SICK, 40)], size=110, isz=140),
     'kalimdor', "The demons are the Legashi satyrs. Their camp gets a new name in the files: Legashi Stronghold. And Strongholds are a new kind of content in Forever, like Krol'dok Stronghold.", 7.5),
    (card('boss', 'IN THE GAME FILES', 'THE FINAL BOSS', RED, (150, 40, 30, 255), [],
          [('the "Master Spelunker" achievement', BONE, 44), ('already lists Blackmaw Hold', BONE, 44),
           ('beat its final boss to complete it', AMBER, 44), ('creature #247234: name still hidden', SICK, 44),
           ('57 dungeon encounters are encrypted', GREY, 40)], size=120),
     'kalimdor', 'Even better: the Master Spelunker achievement already lists Blackmaw Hold. To complete it, you must beat its final boss, creature two four seven two three four. Its name is still hidden, like fifty seven encrypted dungeon encounters.', 8.5),
    (card('sixty', 'MASTER SPELUNKER  ·  LEVEL 60', 'THE NEW 60 DUNGEONS', AMBER, (200, 120, 40, 255), [],
          [('Alcaz Prison', AMBER, 50), ("The Shaper's Terrace", AMBER, 50),
           ('bosses: Nanaya, Cinder, Bolt, Snowtalon', BONE, 40), ('Blackmaw Hold', FEL, 54),
           ('+ BRD, LBRS, UBRS, Scholo, Strat, DM...', GREY, 38)], size=110),
     'kalimdor', "It sits next to the other new level sixty dungeons in that list: Alcaz Prison, and The Shaper's Terrace, with Nanaya, Cinder, Bolt and Snowtalon. Plus all the classics.", 7.5),
    (card('outro', 'BIGGER THAN BRD?', 'HYPED OR WORRIED?', FEL, FELG, [276893, 273050, 235256],
          [('tell me in the comments', BONE, 48), ('beta files  ·  may still change', GREY, 38),
           ('follow for every WoW Forever secret', SICK, 44)], size=110, isz=130),
     'kalimdor', 'A dungeon bigger than Blackrock Depths: hyped, or worried about the run time? Tell me in the comments, and follow for every WoW Forever secret.', 6.0),
]


PLAN = BM
MUSIC = 'rogue'


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
