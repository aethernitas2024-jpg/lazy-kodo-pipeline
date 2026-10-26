import tooltip as TT
VIO = (190, 140, 255, 255)
VIOG = (90, 40, 160, 255)
GOLDC = (255, 210, 90, 255)
SILV = (215, 220, 235, 255)
COPP = (225, 140, 90, 255)
GOLDS = [286279, 286280, 286281, 286283, 286284, 286287, 286288, 286290, 286291, 286292, 286293, 286294, 286298, 286299, 286300, 286302, 286327]
SILVERS = [286263, 286264, 286265, 286266, 286267, 286268, 286270, 286271, 286272, 286273, 286274, 286275, 286328]
COPPERS = [286304, 286306, 286307, 286308, 286309, 286310, 286311, 286312, 286313, 286314, 286315, 286316, 286317, 286318]


def tcard(name, kicker, big, col, glow, items, rows, size=110, tsize=40, twidth=900):
    """One coin: real in-game tooltip, big, then a short line."""
    def fn():
        im = blank()
        B.backdrop(im, 880, 760, 640, 185)
        y = head(im, kicker, big, col, glow, y=470, size=size)
        y = TT.paste(im, items, y + 50, width=twidth, size=tsize, gap=18)
        for t, c, s in rows:
            y = line(im, t, y + 10, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


def grid_png():
    im = blank()
    B.backdrop(im, 900, 860, 820, 185)
    y = head(im, 'IN THE GAME FILES', '44 WISHING COINS', GOLDC, (200, 140, 40, 255), y=290, size=110)
    for label, ids, col in (('17 GOLD', GOLDS, GOLDC), ('13 SILVER', SILVERS, SILV), ('14 COPPER', COPPERS, COPP)):
        y = line(im, label, y + 30, 50, col)
        per = 9
        for r in range(0, len(ids), per):
            row = ids[r:r + per]
            y = HY.icon_row(im, row, y + 14, 84, gap=12) - 4
    line(im, 'every coin = a famous character\'s wish', y + 34, 46, BONE)
    return save(im, WORK, 'grid')


def coin(name, cid, who, say, col=GOLDC, dur=6.0, note=None):
    rows = [(note, SICK, 44)] if note else []
    return (tcard(name, 'WISHING COIN', who, col, (120, 90, 20, 255), [cid], rows),
            'dalaran', say, dur)


FOUNT = [
    (card('hook', 'WOW FOREVER  ·  HIDDEN IN THE FILES', 'THE WISHING FOUNTAIN', GOLDC, (200, 140, 40, 255), [286287, 286281, 286279],
          [("44 coins tossed by Warcraft's biggest names", BONE, 48), ('each one carries a secret wish', AMBER, 48),
           ('some are... unexpected', SICK, 46)], size=100, isz=150),
     'dalaran', "WoW Forever has a wishing fountain, and the game files hold forty four coins. Each one carries the wish of a famous Warcraft character. Some are unexpected.", 6.0),
    (grid_png, 'dalaran', 'Seventeen gold coins, thirteen silver and fourteen copper. Here are the best ones.', 6.0),
    coin('kt', 286287, "KEL'THUZAD", "Kel'Thuzad: sometimes, I wish someone would come along and just give me a big, long hug.",
         note='the future lich just wants a hug'),
    coin('arthas', 286281, 'PRINCE ARTHAS', 'Arthas, before the fall: a kingdom to rule. What to ask for? Perhaps a frozen scone.',
         note='"frozen"... foreshadowing?'),
    coin('anduin', 286279, 'ANDUIN WRYNN', "Anduin: I wish I would grow up, it feels like I've been ten for years.",
         note='a jab at Anduin staying a kid since 2004'),
    coin('archi', 286293, 'ARCHIMONDE', 'Archimonde himself: I wish to know how you survived my wrath, little fountain.',
         note='he flattened Dalaran. The fountain survived.'),
    coin('katrana', 286290, 'LADY KATRANA PRESTOR', "Lady Katrana Prestor, Onyxia in disguise: listen, little wishing fountain. You'll give me all your power if you know what's good for you."),
    coin('maiev', 286273, 'MAIEV SHADOWSONG', "Maiev's whole wish: Where's Illidan?", col=SILV, dur=5.0, note='some things never change'),
    coin('doan', 286267, 'ARCANIST DOAN', "Arcanist Doan, of the Scarlet Monastery: oh, why won't you notice me? Abbendis, I would follow you anywhere.", col=SILV,
         note='a secret crush on High General Abbendis'),
    coin('mekka', 286270, 'HIGH TINKER MEKKATORQUE', 'Mekkatorque: how does this fountain even work? I wonder if I could make one.', col=SILV),
    coin('attumen', 286308, 'ATTUMEN', 'Attumen the Huntsman: can I have a more comfortable saddle? My hindquarters ache.', col=COPP),
    coin('falstad', 286311, 'FALSTAD WILDHAMMER', 'Falstad: I hope I end up in another book eventually.', col=COPP, dur=5.0, note='a nod to his novel appearances'),
    coin('sonya', 286300, 'SONYA DARKHALLOW', "Sonya Darkhallow, the Barrow Deeps boss: this doesn't make sense. Why am I putting a coin in a fountain?",
         note="Forever's own raid boss is confused"),
    coin('sylvanas', 286291, 'SYLVANAS WINDRUNNER', 'And a sad one. Sylvanas, long ago: I hope my sisters and I can grow up and get married together. This coin appears to be very old.'),
    coin('jaina', 286288, 'LADY JAINA PROUDMOORE', 'And Jaina: Arthas, my love, please come back to me.', dur=5.5),
    (tcard('lucky', 'HOW IT WORKS', 'SHINY SILVER COIN', SILV, (90, 100, 130, 255), [286732],
           [('toss a lucky coin in the water: +30 Fishing', AMBER, 42), ('11 hidden coin spots in the files', BONE, 42),
            ('fish the wishes back up?', SICK, 44)], size=100),
     'dalaran', 'How do you get them? A Shiny Silver Coin raises your fishing when you toss it into the water, and the files hide eleven coin spots. '
                'Just like the Dalaran fountain in Wrath, you will probably fish them up.', 8.0),
    (card('outro', 'WHICH ONE IS YOUR FAVORITE?', 'TELL ME BELOW', GOLDC, (200, 140, 40, 255), [286287, 286273, 286293, 286300],
          [('beta files  ·  may still change', GREY, 40), ('follow for more WoW Forever secrets', SICK, 46)], size=120, isz=130),
     'dalaran', 'Which wish is your favorite? Tell me in the comments, and follow for more WoW Forever secrets.', 5.0),
]
