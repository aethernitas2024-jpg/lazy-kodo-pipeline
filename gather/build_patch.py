# -*- coding: utf-8 -*-
"""Short: Oct 15 development notes + build 70450 datamine (17/10/2026). Plan in plan_patch.py.

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

KIND = 'patch1015'
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - patch notes Oct 15 + build 70450 (EN).mp4'
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

from PIL import Image, ImageDraw
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

PLAN = PATCH
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
