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


LEAFRE = [
    (tcard('hook', 'WOW FOREVER  ·  A MYSTERY RING', '+100 SPELL POWER', [276765],
           [('epic, item level 66', AMBER, 42), ('equippable at level 1', BONE, 42), ('real loot, or not?', SICK, 46)], size=104),
     'vault', "A ring with one hundred spell power, equippable at level one. It is on the WoW Forever servers. "
              "But can you actually get it? Let's look at what we really know.", 7.5),
    (card('claim', 'THE RUMOR', 'FISHED UP?', GOLDC, GOLDG, [276765],
          [('reported as an ultra-rare fishing catch', BONE, 42), ('Stormwind Stockade, low level character', BONE, 40),
           ('no drop rate, no video proof yet', AMBER, 42), ('one boosting site even sells the farm', GREY, 38)], size=110, isz=110),
     'vault', 'The rumor: it would be an ultra rare fishing catch, in the Stormwind Stockade, on a low level character. '
              'But there is no drop rate and no clear video proof yet, and one boosting site is already selling the farm.', 9.0),
    (tcard('family', 'IT HAS TWO SIBLINGS', "LEAFRE'S RINGS", [274978, 285326],
           [('item level 1, +150 to every resistance', AMBER, 38), ('armor penetration: not a Classic stat', AMBER, 38),
            ('a modern retail icon', GREY, 36)], size=100, tsize=28),
     'vault', "And it is not alone. There are two other Leafre's rings: one with one hundred fifty to every resistance at item level one, "
              "and one with armor penetration, a stat that does not even exist in Classic, with an icon from modern retail.", 10.0),
    (card('doubt', 'WHAT IT LOOKS LIKE', 'TEST GEAR?', RINGC, RINGG, [274978, 276765, 285326],
          [('stats like these are typical', BONE, 42), ('of developer testing items', BONE, 42),
           ('but nothing is confirmed', AMBER, 44), ('no word from Blizzard', GREY, 38)], size=120, isz=110),
     'vault', "Stats like these look a lot like the testing gear developers use. But nothing is confirmed either way, "
              "and Blizzard has not said a word about it.", 8.0),
    (card('known', 'WHAT WE KNOW', 'FACTS ONLY', GOLDC, GOLDG, [],
          [('it exists on the servers', SICK, 44), ('it binds when picked up', BONE, 42), ('so you can never buy it from a player', BONE, 40),
           ('nobody has shown a confirmed catch', AMBER, 42)], size=120),
     'vault', 'What we know: it exists on the servers, it binds when picked up, so no player can ever sell it to you, '
              'and nobody has shown a confirmed catch so far.', 8.0),
    (card('advice', 'MY ADVICE', 'BE CAREFUL', RED, (150, 40, 30, 255), [],
          [('do not pay anyone to farm it', AMBER, 46), ('until a real drop is confirmed', BONE, 42),
           ('fished it? show us in the comments', SICK, 44)], size=120),
     'vault', 'So be careful: do not pay anyone to farm it until a real drop is confirmed. And if you fished it, show us in the comments.', 7.0),
    (card('outro', 'YOUR TAKE', 'REAL LOOT OR TEST ITEM?', RINGC, RINGG, [276765],
          [('tell me what you think', AMBER, 44), ('follow for more Forever secrets', SICK, 42)], size=96, isz=110),
     'emeralddream', 'Real loot or test item? Tell me what you think, and follow for more Forever secrets.', 6.0),
]
