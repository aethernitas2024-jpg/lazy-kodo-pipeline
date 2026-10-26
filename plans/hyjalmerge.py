import os, re
G = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\gather'
s = open(os.path.join(G, 'build_barrowweapons.py'), encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)


d = s.index('"""', s.index('"""') + 3)
s = ('# -*- coding: utf-8 -*-\n"""Short: every Hyjal Summit raid weapon model in 3D + the Wild King\'s helm (WoW Forever beta, 07/10/2026).\n\n'
     '    py -3.11 build_hyjalweapons.py\n\n'
     'Models: client 1.60.1.70245 (forever-db2/1.60.1.70245/extra/hyjal.py). Blender turntables in scratchpad/hyjal (45 frames/color @30).\n'
     'Readable names sharing a raid model: Ironwood Blade, Forest Defender\'s Axe, Greenhammer, Evergreen Shield, Stillwind String.\n'
     'Backdrop: official Emerald Dream loading screen (FDID 5344997). Watermark: watermark.py.\n') + s[d:]
rep("WORK = os.path.join(HERE, 'build', 'barrowweapons')", "WORK = os.path.join(HERE, 'build', 'hyjalweapons')")
rep(r"scratchpad\barrow'", r"scratchpad\hyjal'")
rep("Barrow Deeps raid weapons in 3D (EN).mp4", "Hyjal Summit raid weapons in 3D (EN).mp4")
rep("MUSIC = 'barrow'", "MUSIC = 'hyjal'")
rep("FROST = (150, 200, 255, 255)\nFROSTG = (40, 80, 150, 255)", "FROST = (160, 235, 130, 255)\nFROSTG = (40, 110, 40, 255)")
a = s.index('WEAPONS = ['); b = s.index(']\n', a) + 2
s = s[:a] + '''WEAPONS = [
    (7956163, 'TWO-HANDED SWORD', 'Two handed sword.', None),
    (7956165, 'TWO-HANDED AXE', "Two handed axe. The same model as the Forest Defender's Axe.", "same look: Forest Defender's Axe"),
    (7956169, 'TWO-HANDED MACE', 'Two handed mace.', None),
    (7956172, 'POLEARM', 'Polearm.', None),
    (7956161, 'STAFF', 'Staff.', None),
    (7956164, 'BOW', 'Bow. Same model as the Stillwind String.', 'same look: Stillwind String'),
    (7956174, 'ONE-HANDED SWORD', 'One handed sword, like the Ironwood Blade.', 'same look: Ironwood Blade'),
    (7956173, 'ONE-HANDED AXE', 'One handed axe.', None),
    (7956168, 'ONE-HANDED MACE', 'One handed mace, the Greenhammer model.', 'same look: Greenhammer'),
    (7956170, 'DAGGER', 'Dagger.', None),
    (7956171, 'FIST WEAPON', 'Fist weapon.', None),
    (7956166, 'WAND', 'Wand.', None),
    (7956167, 'SHIELD', 'Shield, the Evergreen Shield look.', 'same look: Evergreen Shield'),
    (7710249, "THE WILD KING'S HELM", "And a bonus: the helm of the Wild King himself, the final boss.", "the final boss's crown of antlers"),
]
''' + s[b:]
rep("'BARROW DEEPS RAID  ·  %d / %d' % (i, n)", "('HYJAL SUMMIT RAID  ·  %d / %d' % (i, n - 1)) if i < n else 'HYJAL SUMMIT  ·  BONUS'")
rep("""        y = line(im, 'color %d of %d' % (k + 1, nv), y + 10, 46, AMBER)""",
    """        y = line(im, ('color %d of %d' % (k + 1, nv)) if nv > 1 else 'one look', y + 10, 46, AMBER)""")
rep("""        return [one(k) for k in range(4)]""",
    """        nv = len(json.load(open(os.path.join(SRC, '%d.json' % fdid)))['variants'])
        return [one(k) for k in range(nv)]""")
rep("y = title(im, 'BARROW DEEPS', y + 14, 130,", "y = title(im, 'HYJAL SUMMIT', y + 14, 130,")
rep("line(im, '13 weapons  ·  4 colors each', y, 46, SICK)", "line(im, \"13 weapons  ·  + the Wild King's helm\", y, 46, SICK)")
rep("PLAN = [(hook, 7816289, 'The Barrow Deeps raid in WoW Forever. Every weapon model, in 3D, straight from the beta files.', 6.0)]",
    "PLAN = [(hook, 7956161, 'The Hyjal Summit raid in WoW Forever. Every weapon model, in 3D, straight from the beta files.', 6.0)]")
rep("    PLAN.append((card(k, len(WEAPONS), f, label, name), f, voice, 6.0))",
    "    nv = len(json.load(open(os.path.join(SRC, '%d.json' % f)))['variants'])\n    PLAN.append((card(k, len(WEAPONS), f, label, name), f, voice, 1.5 * nv if nv > 1 else 6.0))")
rep("BP.shot(WORK, i, 'vault', dur,", "BP.shot(WORK, i, 'emeralddream', dur,")
open(os.path.join(G, 'build_hyjalweapons.py'), 'w', encoding='utf-8').write(s)
print('ok')
