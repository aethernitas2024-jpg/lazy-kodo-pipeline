# -*- coding: utf-8 -*-
"""Shorts: one racial guide per WoW Forever race (24/10/2026). Plan in plan_races.py.

    py -3.11 build_races.py <human|dwarf|nightelf|gnome|orc|undead|tauren|troll|skyborne>

Values: Spell / SpellEffect / SpellDuration / SpellCooldowns of build 1.60.1.70450 (enUS, identical to the
1.60.1.70532 release client), icons from SpellMisc.SpellIconFileDataID. Class combos: Warcraft Tavern.
"""
import os
import sys

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, run, blank, save, title, pill
from build_whimsy import line
import build_hyjal as HY

RACE = sys.argv[1] if len(sys.argv) > 1 else 'human'
NAMES = {'human': 'Human', 'dwarf': 'Dwarf', 'nightelf': 'Night Elf', 'gnome': 'Gnome', 'orc': 'Orc',
         'undead': 'Undead', 'tauren': 'Tauren', 'troll': 'Troll', 'skyborne': 'Skyborne'}
KIND = 'race_' + RACE
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', KIND); os.makedirs(WORK, exist_ok=True)
HY.WORK = WORK
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - %s racials guide (EN).mp4' % NAMES[RACE]
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
ALLY = (110, 170, 255, 255)
ALLYG = (30, 70, 160, 255)
HORDE = (235, 80, 70, 255)
HORDEG = (140, 30, 25, 255)
NEWC = (140, 225, 110, 255)


def acard(name, kicker, big, col, glow, rows, note=None, size=110):
    """Two racials: (icon fdid, name, one-line effect), then an optional grey note."""
    def fn():
        im = blank()
        B.backdrop(im, 880, 820, 760, 185)
        y = head(im, kicker, big, col, glow, y=300, size=size)
        y = HY.abilities(im, rows, y + 70)
        if note:
            line(im, note, y + 10, 36, GREY, maxw=980)
        return save(im, WORK, name)
    return fn


def classes_card(name, col, glow, old, new):
    def fn():
        im = blank()
        B.backdrop(im, 880, 820, 700, 185)
        y = head(im, 'WHO CAN BE ONE', 'CLASSES', col, glow, y=300, size=120) + 40
        for c in old:
            y = line(im, c, y + 10, 52, BONE) - 4
        for c in new:
            y = line(im, c + '  ·  NEW', y + 10, 52, NEWC) - 4
        return save(im, WORK, name)
    return fn


# achievement_character_<race>_<male|female> icons (FDIDs); the Skyborne have none, their racial icons stand in.
PORTRAITS = {'Human': [236448, 236447], 'Dwarf': [236444, 236443], 'Night Elf': [236450, 236449],
             'Gnome': [236446, 236445], 'Orc': [236452, 236451], 'Undead': [236458, 236457],
             'Tauren': [236454, 236453], 'Troll': [236456, 236455], 'Skyborne': [132845, 463565]}


# Loading screens tied to each race (load/race_<key>.jpg, 2992x1684), see build_races.py docstring.
ARTS = {'Human': 'race_human', 'Dwarf': 'race_dwarf', 'Night Elf': 'race_nightelf', 'Gnome': 'race_gnome',
        'Orc': 'race_orc', 'Undead': 'race_undead', 'Tauren': 'race_tauren', 'Troll': 'race_troll',
        'Skyborne': 'race_skyborne'}


def race_plan(race, faction, col, glow, actives, passives, old, new, say_hook, say_act, say_pas, say_cls, say_out):
    fac = HORDE if faction == 'HORDE' else ALLY
    art = ARTS[race]
    return [
        (card('hook', f'WOW FOREVER  ·  {faction}', race.upper(), col, glow, PORTRAITS[race],
              [('every racial explained', BONE, 46), ('real numbers from the game files', AMBER, 42),
               ('+ every class it can play', SICK, 42)], size=130, isz=150),
         art, say_hook, 6.5),
        (acard('act', 'ACTIVE RACIALS', 'ON YOUR BAR', fac, glow, actives[0], actives[1]), art, say_act, 9.0),
        (acard('pas', 'PASSIVE RACIALS', 'ALWAYS ON', fac, glow, passives[0], passives[1]), art, say_pas, 9.0),
        (classes_card('cls', col, glow, old, new), art, say_cls, 7.0),
        (card('outro', 'YOUR TURN', f'PLAYING {race.upper()}?', col, glow, PORTRAITS[race],
              [('which class are you rolling?', AMBER, 44), ('follow for every race guide', SICK, 42)], size=110, isz=130),
         art, say_out, 6.0),
    ]


RACES = {
    'human': race_plan('Human', 'ALLIANCE', GOLDC, GOLDG,
        ([(136129, 'Will to Survive', 'Removes all stuns  ·  3 min'),
          (136090, 'Perception', 'Huge stealth detection for 20 sec  ·  3 min')], 'Will to Survive is new in Forever'),
        ([(132292, 'Ruthless', '+2% crit chance, spells and attacks'),
          (132874, 'The Human Spirit', '+5% Spirit')], 'Ruthless replaces the old weapon specializations'),
        ['Warrior', 'Paladin', 'Rogue', 'Priest', 'Mage', 'Warlock'], ['Hunter'],
        'Humans in WoW Forever: every racial, with the real numbers from the game files.',
        'Your active racials: Will to Survive, new in Forever, removes every stun on a three minute cooldown. '
        'And Perception gives you huge stealth detection for twenty seconds.',
        'Passives: Ruthless gives two percent crit chance with spells and attacks, replacing the old weapon specializations. '
        'And The Human Spirit gives five percent more Spirit.',
        'Humans can play every class except shaman and druid, and Human Hunter is new in Forever.',
        'Playing a human? Which class are you rolling? Follow for every race guide.'),
    'dwarf': race_plan('Dwarf', 'ALLIANCE', (230, 160, 90, 255), (130, 70, 30, 255),
        ([(136225, 'Stoneform', 'Cleanses bleed, poison, disease  ·  -10% physical damage'),
          (135725, 'Find Treasure', 'Shows nearby treasure on the minimap')], 'Stoneform lasts 8 sec  ·  3 min cooldown'),
        ([(462325, 'Earth Fury', '+2% critical strike damage and healing'),
          (135614, 'Big Game Hunter', '+5% damage against Beasts')], 'both passives are new in Forever'),
        ['Warrior', 'Paladin', 'Hunter', 'Rogue', 'Priest'], ['Shaman'],
        'Dwarves in WoW Forever: every racial, with the real numbers from the game files.',
        'Your actives: Stoneform removes and blocks bleeds, poisons and diseases, and cuts physical damage taken by ten percent for eight seconds. '
        'And Find Treasure shows nearby treasure on your minimap.',
        'Both passives are new in Forever: Earth Fury adds two percent critical strike damage and healing, '
        'and Big Game Hunter adds five percent damage against beasts.',
        'Dwarves can be warriors, paladins, hunters, rogues and priests, and Dwarf Shaman is new, the first Alliance shaman.',
        'Playing a dwarf? Which class are you rolling? Follow for every race guide.'),
    'nightelf': race_plan('Night Elf', 'ALLIANCE', (190, 140, 255, 255), (90, 40, 150, 255),
        ([(136057, "Elune's Light", '+10% crit chance for 15 sec  ·  3 min'),
          (132089, 'Shadowmeld', 'Slip into the shadows until you move')], "Elune's Light is new in Forever"),
        ([(132279, 'Quickness', '+1% dodge  ·  +2% movement speed'),
          (136116, 'Wisp Spirit', 'Become a wisp when you die  ·  +75% speed')], 'night elf rogues and druids are also harder to spot in stealth'),
        ['Warrior', 'Hunter', 'Rogue', 'Priest', 'Druid'], [],
        'Night elves in WoW Forever: every racial, with the real numbers from the game files.',
        "Your actives: Elune's Light, new in Forever, gives ten percent crit chance for fifteen seconds. "
        'And Shadowmeld lets you slip into the shadows until you move.',
        'Passives: Quickness gives one percent dodge and two percent movement speed, '
        'and Wisp Spirit turns you into a wisp when you die, seventy five percent faster.',
        'Night elves can be warriors, hunters, rogues, priests and druids. No new combination for them.',
        'Playing a night elf? Which class are you rolling? Follow for every race guide.'),
    'gnome': race_plan('Gnome', 'ALLIANCE', (255, 140, 200, 255), (140, 40, 100, 255),
        ([(132309, 'Escape Artist', 'Breaks every snare and root  ·  2 min'),
          (4226119, 'Eureka!', '-10% cost and +10% damage for 8 sec')], 'Eureka! is new in Forever  ·  2 min cooldown'),
        ([(132864, 'Expansive Mind', '+5% maximum mana, rage or energy'),
          (134063, 'Engineering Specialization', '-20% engineering failures')], 'Expansive Mind now works for every class'),
        ['Warrior', 'Rogue', 'Mage', 'Warlock'], ['Priest'],
        'Gnomes in WoW Forever: every racial, with the real numbers from the game files.',
        'Your actives: Escape Artist breaks every snare and root. And Eureka, new in Forever: '
        'for eight seconds, your abilities cost ten percent less and deal ten percent more damage.',
        'Passives: Expansive Mind now gives five percent more maximum mana, rage or energy, for every class. '
        'And Engineering Specialization cuts engineering failures by twenty percent.',
        'Gnomes can be warriors, rogues, mages and warlocks, and Gnome Priest is new in Forever.',
        'Playing a gnome? Which class are you rolling? Follow for every race guide.'),
    'orc': race_plan('Orc', 'HORDE', HORDE, HORDEG,
        ([(135726, 'Blood Fury', '+10% attack and spell power for 15 sec'),
          (136082, 'Shatter Curse', 'Removes curses  ·  -5% magic damage for 8 sec')], 'both on a 3 min cooldown  ·  Shatter Curse is new'),
        ([(132393, 'Savage', '+1% crit chance, spells and abilities'),
          (133125, 'Hardiness', 'Stuns on you last 20% less')], 'Savage replaces the old Axe Specialization'),
        ['Warrior', 'Hunter', 'Rogue', 'Shaman', 'Warlock'], ['Mage'],
        'Orcs in WoW Forever: every racial, with the real numbers from the game files.',
        'Your actives: Blood Fury gives ten percent attack power and spell power for fifteen seconds. '
        'And Shatter Curse, new in Forever, removes curses and cuts magic damage taken by five percent for eight seconds.',
        'Passives: Savage gives one percent crit chance, replacing the old axe specialization. And Hardiness makes stuns twenty percent shorter.',
        'Orcs can be warriors, hunters, rogues, shamans and warlocks, and Orc Mage is new in Forever.',
        'Playing an orc? Which class are you rolling? Follow for every race guide.'),
    'undead': race_plan('Undead', 'HORDE', (150, 220, 140, 255), (40, 100, 40, 255),
        ([(136187, 'Will of the Forsaken', 'Breaks charm, fear and sleep  ·  2 min'),
          (132278, 'Cannibalize', '7% health and mana every 2 sec from a corpse')], 'Cannibalize lasts 10 sec  ·  any action cancels it'),
        ([(136148, 'Underwater Breathing', 'Breath lasts 300% longer'),
          (136157, 'Touch of the Grave', 'Attacks can drain up to 5% of your max health')], 'Touch of the Grave is new in Forever'),
        ['Warrior', 'Rogue', 'Priest', 'Mage', 'Warlock'], ['Paladin'],
        'The undead in WoW Forever: every racial, with the real numbers from the game files.',
        'Your actives: Will of the Forsaken breaks charm, fear and sleep. '
        'And Cannibalize restores seven percent health and mana every two seconds while you eat a corpse.',
        'Passives: your breath lasts three hundred percent longer underwater. '
        'And Touch of the Grave, new in Forever, lets your attacks drain up to five percent of your maximum health.',
        'Undead can be warriors, rogues, priests, mages and warlocks, and Undead Paladin is new, the only Horde paladin.',
        'Playing undead? Which class are you rolling? Follow for every race guide.'),
    'tauren': race_plan('Tauren', 'HORDE', (220, 170, 110, 255), (120, 70, 30, 255),
        ([(132368, 'War Stomp', 'Stuns nearby enemies for 2 sec  ·  90 sec'),
          (133938, 'Cultivation', 'Grow a copy of a herb, no Herbalism needed')], 'Cultivation: 15 min cooldown'),
        ([(236717, 'Plainsrunning', '+1% speed every 5 sec moving, up to 30%'),
          (136112, 'Endurance', '+5% health  ·  +2% crit damage and healing')], 'Plainsrunning also gives +3% mounted speed'),
        ['Warrior', 'Hunter', 'Shaman', 'Druid'], [],
        'Tauren in WoW Forever: every racial, with the real numbers from the game files.',
        'Your actives: War Stomp stuns nearby enemies for two seconds. '
        'And Cultivation grows a copy of a herb that you can pick without herbalism.',
        'Passives: Plainsrunning gives one percent speed every five seconds you keep moving, up to thirty percent, '
        'and three percent faster on a mount. Endurance gives five percent health and two percent critical damage and healing.',
        'Tauren can be warriors, hunters, shamans and druids. No new combination for them.',
        'Playing a tauren? Which class are you rolling? Follow for every race guide.'),
    'troll': race_plan('Troll', 'HORDE', (90, 210, 220, 255), (20, 90, 110, 255),
        ([(135727, 'Berserking', '+10% attack and casting speed for 10 sec'),
          (1850550, 'Rapid Regeneration', 'Regain 10% of your health over 6 sec')], 'both on a 3 min cooldown  ·  Rapid Regeneration is new'),
        ([(136077, 'Regeneration', '+20% health regen  ·  20% keeps going in combat'),
          (134357, 'Beast Slaying', '+5% damage against Beasts')], 'Regeneration is doubled from 10% in Classic'),
        ['Warrior', 'Hunter', 'Rogue', 'Priest', 'Shaman', 'Mage'], ['Warlock'],
        'Trolls in WoW Forever: every racial, with the real numbers from the game files.',
        'Your actives: Berserking gives ten percent attack and casting speed for ten seconds. '
        'And Rapid Regeneration, new in Forever, heals ten percent of your health over six seconds.',
        'Passives: Regeneration is doubled from Classic: twenty percent more health regen, and twenty percent of it keeps going in combat. '
        'And Beast Slaying adds five percent damage against beasts.',
        'Trolls can be warriors, hunters, rogues, priests, shamans and mages, and Troll Warlock is new in Forever.',
        'Playing a troll? Which class are you rolling? Follow for every race guide.'),
    'skyborne': race_plan('Skyborne', 'BOTH FACTIONS', (140, 220, 255, 255), (30, 100, 150, 255),
        ([(132845, 'Walk on Air', 'Glide through the air for 10 sec  ·  90 sec'),
          (236219, 'Read Leyline / Skysight', 'Alliance: +100% regen  ·  Horde: +10% speed')],
         'both last 30 sec, or 15 min near a leyline or elemental convergence'),
        ([(463565, 'Wind Blessed', '+3% haste'),
          (4630367, 'Elemental Insight', '+5% damage against Elementals')], 'the only race on both factions'),
        ['Warrior', 'Hunter', 'Rogue', 'Druid', 'Mage (Alliance)', 'Shaman (Horde)'], [],
        'The Skyborne, the new race of WoW Forever: every racial, with the real numbers from the game files.',
        'Your actives: Walk on Air lets you glide for ten seconds. Then it depends on your faction: '
        'Alliance Skyborne read a leyline for one hundred percent more health and mana regen, Horde Skyborne get ten percent movement speed.',
        'Passives: Wind Blessed gives three percent haste, and Elemental Insight adds five percent damage against elementals.',
        'Skyborne can be warriors, hunters, rogues and druids on both sides, plus mage for the Alliance and shaman for the Horde.',
        'Playing a Skyborne? Alliance or Horde? Follow for every race guide.'),
}

PLAN = RACES[RACE]
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
