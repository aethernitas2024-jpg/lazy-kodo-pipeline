from PIL import ImageFont

GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)
HG = (150, 40, 30, 255)
WL = (170, 110, 255, 255)
WLG = (80, 30, 150, 255)

CLASSC = {'Warlock': (148, 130, 201, 255), 'Shaman': (0, 112, 221, 255), 'Paladin': (245, 140, 186, 255),
          'Druid': (255, 124, 10, 255), 'Priest': (230, 230, 230, 255), 'Hunter': (170, 211, 114, 255),
          'Rogue': (255, 244, 104, 255), 'Warrior': (198, 155, 109, 255), 'Mage': (63, 199, 235, 255)}
RATES = [('Warlock', 79), ('Shaman', 63), ('Paladin', 55), ('Druid', 46), ('Priest', 43),
         ('Hunter', 39), ('Rogue', 31), ('Warrior', 27), ('Mage', 25)]


def barcard(name, kicker, big, note):
    """Finals duel win rate vs other classes (mirrors excluded), one bar per class."""
    def fn():
        im = blank()
        B.backdrop(im, 900, 860, 800, 190)
        y = head(im, kicker, big, WL, WLG, y=250, size=100) + 50
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 36)
        x0, x1 = 300, 940
        for cls, pct in RATES:
            col = CLASSC[cls]
            d.text((x0 - 20, y + 22), cls, font=f, fill=col, anchor='rm')
            d.rounded_rectangle((x0, y + 4, x1, y + 40), 10, fill=(30, 30, 40, 220))
            d.rounded_rectangle((x0, y + 4, x0 + (x1 - x0) * pct / 100, y + 40), 10, fill=col)
            d.text((x0 + (x1 - x0) * pct / 100 + 14 if pct < 85 else x1 - 14, y + 22), '%d%%' % pct, font=f,
                   fill=BONE, anchor='lm' if pct < 85 else 'rm')
            y += 62
        line(im, note, y + 20, 34, GREY, maxw=1000)
        return save(im, WORK, name)
    return fn


DUEL2 = [
    (card('hook', 'THE FOREVER OPEN  ·  FINALS', 'A WARLOCK WINS $50K', WL, WLG, [],
          [('the last seed won it all', AMBER, 46), ('warlocks finish 1st AND 2nd', BONE, 44),
           ('and the mages collapsed', RED, 44)], size=104),
     'vault', 'The Forever Open is over, and a warlock wins fifty thousand dollars. The last warlock seed won it all, '
              'warlocks finished first and second, and the mages completely collapsed.', 8.0),
    (card('final', 'THE ROAD TO THE TITLE', 'WARLOCKGUY', WL, WLG, [],
          [('upper final: lost 2-1 to Neepzen', BONE, 42), ('dropped to the lower bracket', GREY, 38),
           ('lower final: beat Cdew 2-0', BONE, 42), ('grand final rematch: won 3-1', AMBER, 46),
           ('$50,000 + the "Death\u2019s Duelist" title', SICK, 40)], size=120),
     'vault', 'Warlockguy lost the upper final to Neepzen, two to one, and dropped to the lower bracket. '
              'He beat Cdew two to oh in the lower final, then won the grand final rematch three to one: '
              'fifty thousand dollars and the Death\u2019s Duelist title.', 11.0),
    (card('underdog', 'THE UNDERDOG STORY', 'FROM LAST TO FIRST', GOLDC, GOLDG, [],
          [('Warlockguy: 4th of 4 qualified warlocks', BONE, 40), ('the weakest tiebreaker of all 36 finalists', AMBER, 38),
           ('top seed Korleone: out in 9th-12th', BONE, 40), ('Oddwaffletv: 31st seed, finished 4th', SICK, 40)], size=110),
     'vault', 'And it is an underdog story: Warlockguy only qualified as the fourth of four warlocks, with the weakest tiebreaker of all thirty six finalists. '
              'Meanwhile the top seed, Korleone, went out early, and Oddwaffletv went from thirty first seed to fourth place.', 11.0),
    (barcard('rates', 'FINALS  ·  WIN RATE VS OTHER CLASSES', 'WARLOCKS: 79%', 'mirror matches excluded  ·  finals day only'),
     'vault', 'On finals day, warlocks won seventy nine percent of their duels against other classes. Shamans sixty three, paladins fifty five. '
              'At the bottom: warriors twenty seven, and mages twenty five percent.', 9.5),
    (card('why', 'WHY WARLOCKS?', 'FEAR, DOTS, UNDEAD', WL, WLG, [],
          [('Fear + Seduction: control everything', BONE, 40), ('DoTs stop healing and stealth', BONE, 40),
           ('Soul Link now a 21-point talent', BONE, 40), ('all 4 warlock finalists: Undead', AMBER, 40),
           ('Will of the Forsaken breaks fear', GREY, 36)], size=110),
     'vault', 'Why warlocks? Fear and Seduction control everything, damage over time stops healing and stealth, '
              'and Soul Link is now a twenty one point talent. Plus all four warlock finalists were undead, with Will of the Forsaken.', 10.0),
    (card('mages', 'THE MAGE COLLAPSE', 'ALL 4 OUT AT ONCE', (63, 199, 235, 255), (20, 90, 130, 255), [],
          [('every mage finalist lost in the same round', BONE, 38), ('so the $5,555 mage prize', AMBER, 40),
           ('is split four ways', AMBER, 40), ('after weeks of "nerf mages" threads', GREY, 36)], size=110),
     'vault', 'And the mages: all four were eliminated in the same lower bracket round, so the mage prize is split four ways. '
              'After weeks of people asking for mage nerfs.', 8.5),
    (card('classes', '$5,555 EACH', 'THE CLASS WINNERS', GOLDC, GOLDG, [],
          [('Warlock: Neepzen  \u00b7  Shaman: Cdew', BONE, 38), ('Paladin: Azzu  \u00b7  Druid: Minpojke', BONE, 38),
           ('Priest: Nieze  \u00b7  Rogue: Justwoo', BONE, 38), ('Hunter: Fvp  \u00b7  Warrior: Mag', BONE, 38),
           ('Mage: 4-way tie', GREY, 36), ('Sodapoppin: outside the top 8', AMBER, 38)], size=110),
     'vault', 'The class winners, five thousand five hundred fifty five dollars each: Neepzen, Cdew, Azzu, Minpojke, Nieze, Justwoo, Fvp and Mag. '
              'Sodapoppin, undefeated on day one, did not make the top eight.', 10.0),
    (card('after', 'THE AFTERMATH', '"NERF WARLOCKS"', RED, HG, [],
          [('Reddit: "nerf warlock" + "who is rerolling"', BONE, 36), ('no warlock change from Blizzard yet', BONE, 38),
           ('next: a level 60 tournament?', SICK, 42), ('an Alliance edition is also floated', GREY, 36)], size=110),
     'vault', 'The aftermath: Reddit is full of nerf warlock and who is rerolling warlock threads, but Blizzard has not changed warlocks yet. '
              'And Tips Out is already talking about a level sixty tournament.', 9.0),
    (card('outro', 'YOUR TAKE', 'REROLLING WARLOCK?', WL, WLG, [],
          [('should Blizzard nerf them?', AMBER, 44), ('follow for every Forever update', SICK, 42)], size=110),
     'emeralddream', 'So, are you rerolling warlock? Should Blizzard nerf them? Tell me, and follow for every Forever update.', 6.5),
]
