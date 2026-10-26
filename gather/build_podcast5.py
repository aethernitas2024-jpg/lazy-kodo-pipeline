# -*- coding: utf-8 -*-
"""Short: official WoW Forever podcast ep. 5, End of Beta Special (22/10/2026). Plan in plan_podcast5.py.

    py -3.11 build_podcast5.py

Source: the episode's YouTube captions (uOlxa3xvNq4), read in full.
"""
import os
import sys

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title, pill
from build_whimsy import line
import build_hyjal as HY

KIND = 'podcast5'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - podcast ep 5 news (EN).mp4'
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


HORDE = (235, 90, 80, 255)
ALLI = (110, 170, 255, 255)

import tooltip as TT

RINGC = (190, 140, 255, 255)
RINGG = (90, 40, 150, 255)
GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)


def tcard(name, kicker, big, items, rows, col=RINGC, glow=RINGG, size=100, tsize=30, twidth=820, y0=240):
    def fn():
        im = blank()
        B.backdrop(im, 900, 820, 800, 185)
        y = head(im, kicker, big, col, glow, y=y0, size=size)
        y = TT.paste(im, items, y + 30, width=twidth, size=tsize, gap=18)
        for t, c, s in rows:
            y = line(im, t, y + 6, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)
HG = (150, 40, 30, 255)
BLUE = (120, 190, 255, 255)
BLUEG = (30, 80, 150, 255)
FIRE = (255, 140, 60, 255)
FIREG = (150, 50, 20, 255)

POD5 = [
    (card('hook', 'OFFICIAL PODCAST  ·  EPISODE 5', 'END OF BETA NEWS', GOLDC, GOLDG, [],
          [('the launch raids and new bosses', BONE, 42), ('Molten Core "revamped"', FIRE, 46),
           ('hidden secrets + a datamine warning', BONE, 40), ('and what comes after', SICK, 42)], size=110),
     'vault', 'The official WoW Forever podcast just dropped its end of beta special, with four developers. '
              'Here is everything new: the launch raids, Molten Core, the hidden secrets, and what comes next.', 9.0),
    (card('raids', 'RAIDS AT LAUNCH', '10  ·  20  ·  40', GOLDC, GOLDG, [],
          [('10 players: the Barrow Deeps', BONE, 44), ('20 players: Hyjal Summit', BONE, 44),
           ('40 players: Onyxia’s Lair', BONE, 44), ('20+ brand new bosses', AMBER, 44),
           ('10 AND 20 player content every patch', SICK, 38)], size=130),
     'vault', 'Three raids at launch: the Barrow Deeps for ten players, Hyjal Summit for twenty, and Onyxia’s Lair for forty. '
              'More than twenty brand new bosses, and they promise ten and twenty player content in every patch.', 11.0),
    (card('bosses', 'THE ENCOUNTER DESIGNER TEASED', '3 NEW BOSSES', SHADOW, (90, 40, 150, 255), [],
          [('Barrow Deeps: a damage buff', BONE, 40), ('that can get you killed', BONE, 40),
           ('Barrow Deeps: a pair of spiders', BONE, 40), ('Hyjal Summit: an undead crocolisk god', AMBER, 38),
           ('kill the husk, then the ghost inside', AMBER, 38)], size=110),
     'vault', 'The lead encounter designer teased three bosses: one gives you a damage buff that can get you killed, '
              'a pair of spiders, and in Hyjal Summit, an undead crocolisk wild god. You kill the husk, then the ghost possessing it, back and forth.', 11.5),
    (card('mc', 'AND THE OLD RAIDS?', 'MOLTEN CORE', FIRE, FIREG, [],
          [('"revamped", like at BlizzCon', AMBER, 46), ('no more simple tank and spank', BONE, 42),
           ('raid goal: "beer and pretzels"', BONE, 42), ('fun with friends, consumables optional', GREY, 36)], size=120),
     'vault', 'And Molten Core? Still secret, but they repeated the word revamped, and hinted you will not just tank and spank Golemagg anymore. '
              'Their goal for raids: beer and pretzels. Fun with friends, not a hardcore grind.', 10.5),
    (card('secrets', 'UNSOLVING THE GAME', 'STILL HIDDEN', NATURE, (40, 110, 40, 255), [],
          [('"thousands" of things held back', BONE, 42), ('loot invisible until someone finds it', BONE, 40),
           ('dungeon maps locked during the beta', BONE, 40), ('the torch was hidden in week one', GREY, 36),
           ('now guards carry torches at night', AMBER, 40)], size=120),
     'emeralddream', 'A lot is still hidden. Loot stays invisible until someone finds it, and dungeon maps were locked in the beta. '
                     'Even the torch was hidden at first, and now city guards will carry torches at night.', 10.5),
    (card('datamine', 'A WARNING FROM BLIZZARD', 'DATAMINING', RED, HG, [],
          [('some datamined assets', BONE, 44), ('are NOT meant for Forever', AMBER, 46),
           ('every WoW version shares', BONE, 42), ('assets and code', BONE, 42)], size=120),
     'vault', 'And a warning: some datamined assets are not meant for Forever, because every version of WoW shares assets and code. '
              'Remember those mounts Blizzard said were not for this game.', 9.0),
    (card('servers', 'REALMLESS, EXPLAINED', 'WHO YOU PLAY WITH', BLUE, BLUEG, [],
          [('a mix of familiar and new faces', BONE, 42), ('language option in the settings', AMBER, 42),
           ('US and EU stay separate at launch', BONE, 40), ('"never say never" for later', GREY, 38)], size=104),
     'vault', 'Realmless servers: they mix familiar faces with new ones, and you can pick your language in the settings. '
              'But North America and Europe stay separate at launch. Never say never, for later.', 10.0),
    (card('future', 'THE FUTURE', 'LEVEL 60 FOREVER', GOLDC, GOLDG, [],
          [('the level cap stays at 60', BONE, 42), ('homes and manors already found', AMBER, 42),
           ('hidden instance portals', AMBER, 42), ('shared quest drops: "never say never"', GREY, 36),
           ('next: a tech episode', SICK, 40)], size=110),
     'vault', 'For the future: the level cap stays at sixty. They teased homes and manors players already found, and hidden instance portals. '
              'Shared quest drops? Never say never. And a tech episode is coming.', 10.5),
    (card('outro', 'YOUR PICK', 'MOST HYPED?', GOLDC, GOLDG, [],
          [('Barrow Deeps, Hyjal Summit', AMBER, 42), ('or a revamped Molten Core?', AMBER, 42),
           ('follow for everything Forever', SICK, 42)], size=120),
     'emeralddream', 'So, what are you most hyped for? Barrow Deeps, Hyjal Summit, or a revamped Molten Core? Tell me, and follow for everything Forever.', 7.0),
]

PLAN = POD5
MUSIC = 'hyjal'



def main():
    files, tl, say, t = [], [], [], 0.0
    for i, (fn, art, text, mind) in enumerate(PLAN):
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        files.append(BP.shot(WORK, i, art, dur, seed=34 if i in (0, len(PLAN) - 1) else i * 37 + 23,
                             bright=0.13 if art == 'stress' else -0.14))   # the screenshot read too dark at -0.14 (user, 22/10)
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
