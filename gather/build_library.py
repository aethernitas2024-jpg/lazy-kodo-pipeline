# -*- coding: utf-8 -*-
"""Short: all 40 Library Books of WoW Forever, mapped (16/10/2026). Plan in plan_library.py.

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

KIND = 'library'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - every library book (EN).mp4'
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

import sys as _sys
_sys.path.insert(0, r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans')
import route_map as RM
import tooltip as TT
from PIL import Image, ImageDraw, ImageFilter

BOOKC = (190, 140, 255, 255)
BOOKG = (90, 40, 150, 255)
GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)
MAPS = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\maps'


def zmap(pts, width, pad=4.0):
    """World2 cropped around the pins (x%, y%, tag, colour), pins drawn after the crop."""
    m = Image.open(MAPS + r'\World2.png').convert('RGBA')
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1 = max(0, min(xs) - pad * 2.2), min(100, max(xs) + pad * 2.2)
    y0, y1 = max(0, min(ys) - pad * 1.6), min(100, max(ys) + pad * 1.6)
    # keep a pleasant aspect (not thinner than 4:3 landscape, not taller than square)
    while (x1 - x0) * m.width < (y1 - y0) * m.height * 1.0:
        x0, x1 = max(0, x0 - 1), min(100, x1 + 1)
        if x0 == 0 and x1 == 100:
            break
    while (x1 - x0) * m.width > (y1 - y0) * m.height * 1.45:
        y0, y1 = max(0, y0 - 1), min(100, y1 + 1)
        if y0 == 0 and y1 == 100:
            break
    box = (round(x0 / 100 * m.width), round(y0 / 100 * m.height), round(x1 / 100 * m.width), round(y1 / 100 * m.height))
    c = m.crop(box)
    s = width / c.width
    c = c.resize((width, round(c.height * s)), Image.LANCZOS)
    f = B.font(B.CINZEL, 30, 900)
    for x, y, tag, col in pts:
        cx = (x / 100 * m.width - box[0]) * s
        cy = (y / 100 * m.height - box[1]) * s
        r = 27
        g = Image.new('RGBA', c.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse((cx - r * 1.4, cy - r * 1.4, cx + r * 1.4, cy + r * 1.4), fill=col)
        g = g.filter(ImageFilter.GaussianBlur(12))
        c.alpha_composite(g)
        d = ImageDraw.Draw(c)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(12, 10, 8, 240), outline=col, width=5)
        d.text((cx, cy + 1), tag, font=f, fill=BONE, anchor='mm')
    return c


def bcard(name, kicker, big, books, mw=560, size=96, fs=(33, 27)):
    """Map card: books = [(n, book, zone, mx, my, where, note)]."""
    def fn():
        im = blank()
        B.backdrop(im, 900, 820, 800, 185)
        y = head(im, kicker, big, BOOKC, BOOKG, y=215, size=size)
        pts = []
        for n, book, zone, mx, my, where, note in books:
            p = RM.point(zone, mx, my)
            pts.append((p[0], p[1], str(n), AMBER if not note else RED))
        y = map_card(im, zmap(pts, mw), y + 34)
        y += 18
        for n, book, zone, mx, my, where, note in books:
            y = line(im, '%d. %s' % (n, book), y + 6, fs[0], AMBER, maxw=1000) - 4
            y = line(im, '%s%s' % (where, ('  ·  ' + note) if note else ''), y, fs[1], BONE if not note else (255, 160, 140, 255), maxw=1000) - 2
        return save(im, WORK, name)
    return fn


def tcard(name, kicker, big, items, rows, size=104, tsize=30, twidth=820):
    def fn():
        im = blank()
        B.backdrop(im, 900, 820, 800, 185)
        y = head(im, kicker, big, GOLDC, GOLDG, y=230, size=size)
        y = TT.paste(im, items, y + 30, width=twidth, size=tsize, gap=18)
        for t, c, s in rows:
            y = line(im, t, y + 6, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


A = [(1, "Archmage Theocritus' Research Journal", 'Elwynn Forest', 65.4, 70.1, 'Elwynn · Tower of Azora, top floor · 65, 70', None),
     (2, 'Archmage Antonidas: The Unabridged Autobiography', 'Ironforge', 76.3, 10.8, 'Ironforge · Hall of Explorers, back room · 76, 11', None),
     (3, 'Bewitchments and Glamours', 'Westfall', 45.4, 70.5, 'Westfall · Moonbrook, house on the west edge · 45, 70', None),
     (4, 'Rumi of Gnomeregan: The Collected Works', 'Westfall', 52.7, 53.8, 'Sentinel Hill inn (or Thelsamar inn) · counts once', None),
     (5, 'Runes of the Sorcerer-Kings', 'Loch Modan', 77.5, 14.1, "Loch Modan · Mo'grosh ogre cave · 77, 14", 'elites')]
H = [(6, "The Lessons of Ta'zo", 'Orgrimmar', 38.7, 78.4, 'Orgrimmar · Valley of Spirits, painted mural · 39, 78', None),
     (7, "The Apothecary's Metaphysical Primer", 'Tirisfal Glades', 59.5, 52.3, 'Tirisfal · Brill alchemy shop, shelf · 59, 52', None),
     (8, 'Ataeric: On Arcane Curiosities', 'Silverpine Forest', 43.4, 41.2, 'Silverpine · The Sepulcher, lower room · 43, 41', None),
     (9, 'The Dalaran Digest, Vol. 23', 'Silverpine Forest', 63.5, 63.1, 'Silverpine · Ambermill town hall · 63, 63', None)]
K1 = [(10, "Nar'thalas Almanac, Vol. 74", 'Darkshore', 59.6, 22.2, 'Darkshore · Ruins of Mathystra, down the stairs · 60, 22', None),
      (11, 'Arcanic Systems Manual', 'The Barrens', 56.3, 8.8, 'Barrens · Sludge Fen oil rig, control room · 56, 9', None),
      (12, 'Baxtan: On Destructive Magics', 'The Barrens', 62.7, 36.3, 'Ratchet · engineering shop, upstairs · 63, 36', None),
      (13, 'Secrets of the Dreamers', 'The Barrens', 46.0, 36.4, 'Barrens · Wailing Caverns entrance cave', None),
      (14, 'Fury of the Land', 'Stonetalon Mountains', 74.4, 85.7, 'Stonetalon · Grimtotem Post, small hut · 74, 86', None),
      (15, 'Geomancy: The Stone-Cold Truth', 'Thousand Needles', 34.0, 40.0, 'Thousand Needles · Darkcloud Pinnacle · 34, 40', None)]
E1 = [(16, 'Crimes Against Anatomy', 'Duskwood', 16.0, 38.5, 'Duskwood · Raven Hill catacombs, last room', 'level 27+'),
      (17, 'Goaz Scrolls', 'Wetlands', 33.6, 47.9, "Wetlands · Whelgar's Excavation, half-buried urn · 34, 48", None),
      (18, 'Defensive Magics 101', 'Alterac Mountains', 48.5, 57.6, 'Alterac · ogre fortress, first tower · 49, 58', None),
      (19, 'A Web of Lies: Debunking Myths and Legends', 'Arathi Highlands', 73.0, 65.0, 'Arathi · Witherbark Village, by a tent · 73, 65', None),
      (20, 'Basilisks: Should Petrification be Feared?', 'Stranglethorn Vale', 41.5, 50.8, 'Stranglethorn · Crystalvein Mine entrance · 42, 51', None)]
E2 = [(21, "A Luddite's Guide to Caring for Your Demonic Pet", 'Swamp of Sorrows', 61.0, 22.0, 'Swamp of Sorrows · Fallow Sanctuary, in a cage · 61, 22', None),
      (22, 'Sanguine Sorcery', 'Swamp of Sorrows', 70.0, 51.0, 'Sunken Temple · on top, outside the dungeon', None),
      (23, 'Mummies: A Guide to the Unsavory Undead', 'Badlands', 57.0, 39.0, 'Badlands · crypt on the butte · 57, 39', None),
      (24, 'Venomous Journeys', 'The Hinterlands', 36.0, 72.7, "Hinterlands · Shadra'Alor · 36, 73", None),
      (25, 'A Mind of Metal', 'Searing Gorge', 37.8, 49.6, 'Searing Gorge · table under a tent · 38, 50', None)]
K2 = [(26, 'Demons and You', 'Desolace', 55.0, 28.0, 'Desolace · Thunder Axe Fortress, on a bench · 55, 28', None),
      (27, 'RwlRwlRwlRwl!', 'Dustwallow Marsh', 57.0, 21.0, 'Dustwallow · murloc camp, east side · 57, 21', None),
      (28, 'Legends of the Tidesages', 'Tanaris', 72.6, 47.8, 'Tanaris · pirate camp bookshelf · 73, 48', None),
      (29, 'The Liminal and the Arcane', 'Feralas', 50.6, 15.7, 'Feralas · near Jademir Lake', 'moved, unconfirmed')]
E3 = [(30, "Conjurer's Codex", 'Blasted Lands', 55.3, 32.2, 'Blasted Lands · 55, 32', None),
      (31, 'Magma or Lava?', 'Burning Steppes', 22.0, 30.0, 'Blackrock Mountain · before the BRD entrance', None),
      (32, 'Stonewrought Design', 'Burning Steppes', 23.0, 29.0, "Blackrock Mountain · Franclorn Forgewright's altar", None),
      (33, 'Undead Potatoes', 'Western Plaguelands', 38.3, 54.6, 'Western Plaguelands · Felstone farmhouse · 38, 55', None),
      (34, 'Necromancy 101', 'Western Plaguelands', 69.4, 72.8, 'Caer Darrow · top of Scholomance, outside · 69, 73', None),
      (35, 'A Study of the Light', 'Eastern Plaguelands', 71.8, 48.2, "Eastern Plaguelands · Light's Hope Chapel · 72, 48", None),
      (36, 'Scourge: Undead Menace or Misunderstood?', 'Eastern Plaguelands', 26.5, 15.0, 'Eastern Plaguelands · before Stratholme bridge', None),
      (37, 'The Knight and the Lady', 'Eastern Plaguelands', 47.3, 42.3, 'Eastern Plaguelands · 47, 42 (moved)', None)]
K3 = [(38, 'Everyday Etiquette', 'Azshara', 20.7, 62.0, 'Azshara · Haldarr Encampment, on a crate · 21, 62', None),
      (39, 'Northern Kalimdor: A Comprehensive Guide', 'Felwood', 65.2, 3.2, 'Felwood · Timbermaw Hold, by the bridge · 65, 3', None),
      (40, 'Ka-Boom!', 'Winterspring', 60.7, 37.7, 'Everlook · alchemy shop shelf · 61, 38', None)]

LIB = [
    (tcard('hook', 'WOW FOREVER  ·  LIBRARY BOOKS', 'READ BOOKS. GET GEAR.', [277254],
           [('the bow banned from the $100K tournament', AMBER, 40), ('is a reward for collecting books', BONE, 40),
            ('all 40 books, mapped', SICK, 44)], size=96),
     'emeralddream', "Truthseeker's Bow, the best bow in the beta, the one banned from the hundred thousand dollar tournament. "
                     "You get it by collecting books. Here are all forty library books, mapped.", 8.0),
    (card('how', 'HOW IT WORKS', 'THE LIBRARIANS', BOOKC, BOOKG, [203755],
          [('Alliance: Garion Wendell', ALLI, 46), ('Stormwind, Mage Quarter tower', BONE, 40),
           ('Horde: Owen Thadd', HORDE, 46), ('Undercity, Magic Quarter', BONE, 40),
           ('pick up a book, hand it in: it counts', AMBER, 40), ('rewards at 10, 20 and 25 books', SICK, 44)], size=100, isz=110),
     'emeralddream', 'How it works: pick up a book anywhere in the world and hand it to the librarian. Garion Wendell in the '
                     'Stormwind mage tower for the Alliance, Owen Thadd in the Undercity magic quarter for the Horde. '
                     'Every book counts toward rewards at ten, twenty and twenty five books.', 10.0),
    (tcard('r10', 'REWARDS  ·  10 AND 20 BOOKS', 'NECK + RING', [277203, 277204, 281634, 281635],
           [('pick one at 10, one at 20', AMBER, 38)], size=96, tsize=23, twidth=700),
     'emeralddream', 'At ten books, pick a neck: Scholarly Pendant or Erudite\'s Amulet. At twenty, a ring: Field Researcher\'s Loop, '
                     'or Philanthropist\'s Ring with spell power.', 8.5),
    (tcard('r25', 'REWARD  ·  25 BOOKS', 'PICK ONE', [277254, 277258, 277260],
           [('all three require level 40', GREY, 36)], size=96, tsize=24, twidth=720),
     'emeralddream', "At twenty five books, the big one: Truthseeker's Bow, the Crest of Elucidation shield, or Researcher's Night Light. "
                     "All three require level forty.", 8.0),
    (bcard('m1', 'ALLIANCE START  ·  BOOKS 1 TO 5', 'EASTERN KINGDOMS', A),
     'vault', 'Alliance starting zones: the Tower of Azora in Elwynn, the Hall of Explorers in Ironforge, Moonbrook in Westfall, '
              'Rumi of Gnomeregan in the Sentinel Hill or Thelsamar inn, it only counts once, and the ogre cave in Loch Modan, with elites.', 11.0),
    (bcard('m2', 'HORDE START  ·  BOOKS 6 TO 9', 'ORGRIMMAR + LORDAERON', H),
     'vault', 'Horde side: the painted mural of Ta\'zo in Orgrimmar, the Brill alchemy shop, the Sepulcher, and the Ambermill town hall in Silverpine.', 9.5),
    (bcard('m3', 'KALIMDOR  ·  BOOKS 10 TO 15', 'LEVEL 10 TO 35', K1, mw=500),
     'vault', 'Kalimdor, levels ten to thirty five: Ruins of Mathystra in Darkshore, the Sludge Fen oil rig, the Ratchet engineering shop, '
              'the Wailing Caverns entrance cave, Grimtotem Post in Stonetalon, and Darkcloud Pinnacle in Thousand Needles.', 11.5),
    (bcard('m4', 'EASTERN KINGDOMS  ·  16 TO 20', 'LEVEL 20 TO 45', E1),
     'vault', "Eastern Kingdoms, levels twenty to forty five: the Raven Hill catacombs in Duskwood, Whelgar's Excavation in the Wetlands, "
              'the ogre fortress in Alterac, Witherbark Village in Arathi, and the Crystalvein Mine in Stranglethorn.', 11.0),
    (bcard('m5', 'EASTERN KINGDOMS  ·  21 TO 25', 'LEVEL 35 TO 50', E2),
     'vault', 'Then the caged book in the Swamp of Sorrows, the top of the Sunken Temple, the Badlands crypt, '
              "Shadra'Alor in the Hinterlands, and a tent in Searing Gorge.", 10.0),
    (bcard('m6', 'KALIMDOR  ·  BOOKS 26 TO 29', 'LEVEL 30 TO 50', K2),
     'vault', 'Kalimdor again: Thunder Axe Fortress in Desolace, the murloc camp in Dustwallow, the pirate camp in Tanaris, '
              'and Feralas, where the book has moved and its new spot is not confirmed yet.', 10.0),
    (bcard('m7', 'LEVEL 50 TO 60  ·  30 TO 37', 'THE ENDGAME ZONES', E3, mw=390, size=90, fs=(29, 24)),
     'vault', 'Endgame zones: the Blasted Lands, two books in Blackrock Mountain without entering the dungeon, '
              'the Plaguelands farm and Caer Darrow, then Light\'s Hope, the Stratholme bridge and the Plaguelands lake.', 12.0),
    (bcard('m8', 'KALIMDOR  ·  BOOKS 38 TO 40', 'THE LAST THREE', K3),
     'vault', 'And the last three: Azshara, Timbermaw Hold in Felwood, and the Everlook alchemy shop in Winterspring.', 8.0),
    (card('outro', 'YOU ONLY NEED 25', 'SAVE THIS GUIDE', BOOKC, BOOKG, [277254],
          [('25 books = every reward', AMBER, 46), ('the beta ends Oct 21: progress is wiped', GREY, 38),
           ('use it again at launch, Nov 4', SICK, 44), ('follow for more Forever guides', BONE, 42)], size=104, isz=110),
     'emeralddream', 'You only need twenty five books for every reward. The beta ends on October twenty first and progress is wiped, '
                     'so save this guide for launch on November fourth, and follow for more Forever guides.', 8.5),
]

PLAN = LIB
MUSIC = 'hyjal'



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
