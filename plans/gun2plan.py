import tooltip as TT


def tcard(name, kicker, big, col, glow, items, rows, size=110, tsize=38, twidth=880):
    """Card with real in-game tooltips (stats from Wowhead Forever), then short lines."""
    def fn():
        im = blank()
        B.backdrop(im, 900, 820, 800, 185)
        y = head(im, kicker, big, col, glow, y=250, size=size)
        y = TT.paste(im, items, y + 40, width=twidth, size=tsize, gap=22)
        for t, c, s in rows:
            y = line(im, t, y + 4, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn


GOLDC = (255, 205, 90, 255)
GOLDG = (200, 120, 40, 255)

GUN = [
    (card('hook', 'WOW FOREVER  ·  HOTFIXED', 'R.I.P. BUMP GUN', RED, (150, 40, 30, 255), [135611],
          [('the Booty Bay gun that sent', BONE, 50), ('targets FLYING...', AMBER, 56),
           ('lasted about one day', SICK, 48)], size=140, isz=190),
     'eastern_kingdoms', 'Rest in peace, Booty Bay bump gun. It sent targets flying, and it lasted about one day.', 5.0),
    (tcard('before', 'BEFORE', 'THE BUMP', GOLDC, GOLDG, ['274748'],
           [('knocked any target away... even your allies', AMBER, 42)], size=150),
     'eastern_kingdoms', 'Before: a level thirty gun with an on use shot that knocked any target away. Even your own allies.', 5.5),
    (tcard('after', 'NOW', 'JUST A GUN', RED, (150, 40, 30, 255), ['274748_new'],
           [('the knockback is gone: server-side hotfix', BONE, 42), ('(the spell is still in the game files)', GREY, 38)], size=150),
     'eastern_kingdoms', 'Now: the knockback is gone. A server side hotfix. The spell is still in the game files, just no longer on the gun.', 6.0),
    (card('why', 'WHY?', 'TOO MUCH FUN', AMBER, GOLDG, [],
          [('players launched their friends', BONE, 48), ('Slow Fall mid-air = across the zone', BONE, 44),
           ('and on Hardcore, a cliff means game over', SICK, 44)], size=150),
     'eastern_kingdoms', 'Why? Players were launching their friends, with slow fall they flew across the zone, and on Hardcore, a cliff means game over.', 6.0),
    (card('vote', 'YOUR CALL', 'FAIR NERF?', GOLDC, GOLDG, [135611],
          [('good call by Blizzard...', BONE, 50), ('... or should they let us have fun?', AMBER, 50),
           ('tell me in the comments', SICK, 48)], size=170, isz=150),
     'eastern_kingdoms', 'So, your call: good call by Blizzard, or should they let us have fun? Tell me in the comments.', 6.0),
]
