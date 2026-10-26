import tooltip as TT
GOLDC = (255, 210, 90, 255)
GOLDG = (200, 140, 40, 255)
HG = (150, 40, 30, 255)


def tcard(name, kicker, big, col, glow, items, rows, size=100, tsize=34, twidth=860):
    def fn():
        im = blank()
        B.backdrop(im, 900, 820, 800, 185)
        y = head(im, kicker, big, col, glow, y=230, size=size)
        y = TT.paste(im, items, y + 30, width=twidth, size=tsize, gap=18)
        for t, c, s in rows:
            y = line(im, t, y + 6, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


DUEL = [
    (card('hook', 'WOW FOREVER  ·  THE FOREVER OPEN', '$100,000 DUELS', GOLDC, GOLDG, [277254, 282720, 216619],
          [('a level 30 dueling tournament', BONE, 50), ('October 17 + 18', AMBER, 54), ('everything you need to know', SICK, 46)], size=120, isz=140),
     'darkspear', 'One hundred thousand dollars for level thirty duels. The Forever Open happens on October seventeenth and eighteenth. Here is everything you need to know.', 7.0),
    (card('origin', 'HOW IT STARTED', '$50K, THEN DOUBLED', GOLDC, GOLDG, [],
          [('organizer: TipsOut', AMBER, 48), ('with Xaryu + Esfand', BONE, 46), ('announced with $50,000', BONE, 46),
           ('then TimTheTatman added $50,000', SICK, 46), ('"for the love of Classic WoW"', GREY, 42)], size=120),
     'darkspear', 'It started at fifty thousand dollars, announced by TipsOut with Xaryu and Esfand. Then TimTheTatman added fifty thousand more, for the love of Classic WoW.', 8.0),
    (card('format', 'THE FORMAT', 'HORDE  ·  LEVEL 30', HORDE, HG, [],
          [('PvP realm rules', BONE, 48), ('Horde side only', BONE, 48), ('every class can enter', BONE, 46),
           ('open tournament, sign-ups on Raider.io', BONE, 42), ('4,000 sign-ups: closed early, Oct 2', AMBER, 46)], size=120),
     'darkspear', 'The format: Horde side, level thirty, PvP rules. It was open to everyone, and four thousand players signed up, so registration closed early on October second.', 8.0),
    (card('prize', 'THE PRIZE SPLIT', 'WHO GETS PAID', GOLDC, GOLDG, [],
          [('champion: $50,000', GOLDC, 60), ('+ "Death\'s Duelist" title', BONE, 44),
           ('best player of each class: $5,555', AMBER, 48), ('9 classes x $5,555', BONE, 44),
           ("winner's class: goes to the #2 of that class", GREY, 38)], size=120),
     'darkspear', "The champion takes fifty thousand dollars. The other fifty thousand is split between the best player of each class: five thousand five hundred fifty five dollars each.", 8.0),
    (tcard('bow', 'BANNED  ·  OCTOBER 6', "TRUTHSEEKER'S BOW", RED, HG, [277254],
           [('the best bow in the beta: banned', BONE, 44), ('then on Oct 8 Blizzard raised it to level 40', AMBER, 40),
            ('so nobody at 30 can use it anyway', SICK, 42)], size=100),
     'darkspear', "Banned: Truthseeker's Bow, the best bow in the beta. Funny detail: two days later, Blizzard raised it to level forty, so nobody at thirty can equip it anymore.", 8.0),
    (tcard('cons', 'BANNED CONSUMABLES', 'NO PET ARMIES', RED, HG, [282720, 216619],
           [('all non-equippable pet summons', BONE, 42), ('+ Flash Bomb', BONE, 42)], size=110, tsize=30),
     'darkspear', 'Also banned: Spider Swarm and every other pet you summon from a bag, Student Fodder, and the Flash Bomb.', 7.5),
    (card('items', 'MORE RULES', 'BANNED  vs  ALLOWED', AMBER, GOLDG, [7375, 10646, 3456],
          [('banned: Green Whelp Armor', RED, 44), ('banned: Goblin Sapper Charge', RED, 44),
           ('allowed: Dog Whistle + pet trinkets', SICK, 44), ('transmog must be off', BONE, 42)], size=110, isz=130),
     'darkspear', "Green Whelp Armor and Goblin Sapper Charges are banned too. But equippable pet items like the Dog Whistle from Scarlet Monastery are allowed.", 7.5),
    (card('rules', 'DUEL ETIQUETTE', 'THE OPENER RULE', AMBER, GOLDG, [],
          [('stealth classes always get the opener', BONE, 44), ('no moving, no traps until it lands', BONE, 42),
           ('pre-HoTs banned', RED, 46), ('Power Word: Shield before: allowed', SICK, 44), ('only your own class buffs', BONE, 42)], size=110),
     'darkspear', 'Duel etiquette: stealth classes always get a free opener, no traps or moving until it lands. Healing over time before the duel is banned, but a priest shield is allowed.', 8.5),
    (card('signups', 'EARLY SIGN-UPS  ·  2,876 PLAYERS', 'WHO SIGNED UP', HORDE, HG, [],
          [('Priest: the most popular', AMBER, 48), ('Hunter ~500  ·  Shaman ~429', BONE, 44), ('Warlock ~280  ·  Warrior ~188', BONE, 44),
           ('Mage: lower than expected', GREY, 40), ('races: Undead 33%  ·  Orc 31%  ·  Troll 21%', BONE, 40)], size=110),
     'darkspear', 'In the early sign ups, priest was the most popular class, then hunters and shamans. Undead led the races, ahead of orcs and trolls.', 8.0),
    (card('outro', 'OCTOBER 17 + 18', 'WHICH CLASS WINS?', GOLDC, GOLDG, [277254, 282720, 3456],
          [('streamed by Esfand + Xaryu', BONE, 44), ('tell me your pick in the comments', AMBER, 46), ('follow for the results', SICK, 46)], size=110, isz=120),
     'darkspear', 'So, which class wins the hundred thousand dollars? Tell me your pick in the comments, and follow for the results.', 6.5),
]
