import tooltip as TT
import oldstats as OS
BLUEQ = (0, 112, 221, 255)
GREENQ = (30, 255, 0, 255)
NERF72 = [int(x) for x in open(os.path.join(HERE, 'nerf72.txt')).read().split()]


def bacard(name, iid, big, rows=()):
    """Before (blue, recomputed) above after (green, live Wowhead) tooltip."""
    key, rep = OS.make_old(iid)

    def fn():
        im = blank()
        B.backdrop(im, 900, 840, 820, 185)
        y = head(im, 'SILENT NERF', big, RED, (150, 40, 30, 255), y=200, size=96)
        y = line(im, 'BEFORE', y + 26, 46, BLUEQ)
        y = TT.paste(im, [key], y + 8, width=860, size=32, gap=10)
        y = line(im, 'NOW', y + 10, 46, GREENQ)
        y = TT.paste(im, [iid], y + 8, width=860, size=32, gap=10)
        for t, c, s in rows:
            y = line(im, t, y + 6, int(s * 1.15), c, maxw=1000) - 6
        return save(im, WORK, name)
    return fn, rep


def grid_png():
    im = blank()
    B.backdrop(im, 900, 860, 860, 185)
    y = head(im, 'SERVER HOTFIX', '72 BLUES TURNED GREEN', RED, (150, 40, 30, 255), y=250, size=96)
    per = 8
    for r in range(0, len(NERF72), per):
        y = HY.icon_row(im, NERF72[r:r + per], y + (30 if r == 0 else 6), 86, gap=10) - 4
    line(im, 'same item level  ·  less stats  ·  less damage', y + 34, 44, AMBER)
    return save(im, WORK, 'grid')


def ba(name, iid, big, say, rows=(), dur=7.0):
    fn, rep = bacard(name, iid, big, rows)
    return (fn, 'eastern_kingdoms', say, dur)


NERF = [
    (card('hook', 'WOW FOREVER  ·  BETA', 'SILENTLY NERFED', RED, (150, 40, 30, 255), [6804, 17042, 17043],
          [('72 items dropped from blue to green', BONE, 50), ('same item level, weaker stats', AMBER, 48),
           ('pushed by a server hotfix', SICK, 46)], size=110, isz=150),
     'eastern_kingdoms', 'WoW Forever just silently nerfed seventy two items. Blue to green, same item level, weaker stats, pushed straight from the server.', 6.0),
    (grid_png, 'eastern_kingdoms', 'Here they all are. Drops and quest rewards from level twenty to forty two, all pushed by a server hotfix.', 7.0),
    (card('why', 'HOW IT WORKS', 'BLUE  →  GREEN', AMBER, (200, 120, 40, 255), [],
          [('stats come from item level AND quality', BONE, 46), ('a green gets a smaller stat budget', BONE, 46),
           ('about -30% stats', RED, 54), ('weapons: about -20% DPS', RED, 54),
           ('"before" values recomputed from the', GREY, 38), ("game's own stat tables", GREY, 38)], size=120),
     'eastern_kingdoms', "Why it hurts: stats come from item level and quality. A green gets a smaller budget, so about thirty percent less stats, and weapons lose about twenty percent damage.", 7.0),
    ba('hammer', 6804, 'WINDSTORM HAMMER', 'Windstorm Hammer: from thirty eight to seventy one damage, down to thirty to fifty six. Strength and stamina, gone from five and six to three and four.', dur=8.0),
    ba('nail', 17042, 'NAIL SPITTER', 'Nail Spitter, the gun: twenty DPS down to sixteen.', dur=6.5),
    ba('zealot', 17043, "ZEALOT'S ROBE", "Zealot's Robe: spell power from fifteen to eleven, intellect and spirit from ten to seven.", dur=7.0),
    ba('cultist', 270054, "CULTIST'S CHESTGUARD", "Cultist's Chestguard: every stat loses about a third.", dur=6.5),
    ba('ursine', 270027, 'URSINE HAMMER', 'Ursine Hammer: three stats down, and the DPS from twenty two to eighteen.', dur=7.0),
    ba('monkey', 6748, 'MONKEY RING', 'Even the classic rings: Monkey Ring and Tiger Band, sevens become fives.', dur=6.5),
    ba('gravewalker', 251963, 'GRAVEWALKER BOOTS', "And the brand new City of Dalaran: the side quest rewards turned green too. Only the main quest chain stays blue.", dur=8.0),
    (card('more', 'ALSO IN THE HOTFIX', 'WHAT ELSE', AMBER, (200, 120, 40, 255), [2034, 279839, 279841],
          [('60+ more items: stats reshuffled', BONE, 44), ('24 Al\'Aketh pieces: now bind on equip', BONE, 44),
           ('one winner: Scholarly Robes, green → blue', SICK, 44), ('Dalaran main chain rewards: still blue', AMBER, 42),
           ('beta  ·  may still change', GREY, 38)], size=120, isz=130),
     'eastern_kingdoms', "Also in the hotfix: sixty more items with reshuffled stats, the Al'Aketh pieces now bind on equip, and one lucky winner, Scholarly Robes, went from green to blue.", 7.5),
    (card('outro', 'YOUR CALL', 'FAIR NERF OR TOO MUCH?', RED, (150, 40, 30, 255), [6804, 270054, 251963],
          [('tell me in the comments', BONE, 48), ('follow for every WoW Forever change', SICK, 44)], size=100, isz=130),
     'eastern_kingdoms', 'Fair nerf to slow down leveling gear, or too much? Tell me in the comments, and follow for every WoW Forever change.', 6.0),
]
