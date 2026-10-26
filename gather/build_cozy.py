# -*- coding: utf-8 -*-
"""Short guide: Cozy Sleeping Bag quest chain (XP-bonus sleeping bag) in WoW Forever.

    py -3.11 build_cozy.py

Same look as build_whimsy.py / build_prof.py. Zone maps = client world-map tiles plus
WorldMapOverlay tiles (zone_map.py, session 95e10ded scratchpad). Quest objects and
coordinates: Wowhead Forever quest pages 79007/79008, 79192, 79980, 79974, 79975, 79976
(28/09/2026). Route tips (wall, fallen cart, jumping puzzle) from Onsokomaru's Wowhead
comment, rewritten and credited on screen.
"""
import os
from PIL import Image, ImageDraw, ImageFilter

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, GREEN, run, blank, save, title, icon, pill
from build_whimsy import map_card, line, icons_row, _alpha

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', 'cozy'); os.makedirs(WORK, exist_ok=True)
MAPS = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\maps'
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - Cozy Sleeping Bag XP boost guide (EN).mp4'
BAG, FODDER, TOOLBOX = 211527, 216619, 221498
EPIC = (163, 53, 238, 255)
MARK = (255, 214, 90, 255)
HORDE = (196, 48, 38, 255)
ALLI = (60, 120, 230, 255)


def zmap(zone, pts, width=1040):
    """Zone map with numbered markers: pts = [(x%, y%, tag, colour)]."""
    m = Image.open(os.path.join(MAPS, zone + '.png')).convert('RGBA')
    s = width / m.width
    m = m.resize((width, round(m.height * s)), Image.LANCZOS)
    f = B.font(B.CINZEL, max(26, int(40 * width / 1040)), 900)
    for x, y, tag, col in pts:
        cx, cy = x / 100 * m.width, y / 100 * m.height
        r = 46 * width / 1040
        g = Image.new('RGBA', m.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse((cx - r * 1.3, cy - r * 1.3, cx + r * 1.3, cy + r * 1.3), fill=col)
        m.alpha_composite(_alpha(g.filter(ImageFilter.GaussianBlur(22 * width / 1040)), 0.8))
        d = ImageDraw.Draw(m)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=max(4, int(7 * width / 1040)))
        rr = r * 0.62
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(12, 10, 8, 235), outline=BONE, width=3)
        d.text((cx, cy + 1), tag, font=f, fill=BONE, anchor='mm')
    return m


def step_png(name, n, head, zone, pts, coords, hints, credit=None):
    im = blank()
    B.backdrop(im, 1000, 720, 720, 150)
    y = title(im, f'STEP {n}', 210, 52, fill=GOLD, spacing=14, glow=(0, 0, 0, 0))
    y = title(im, head, y + 20, 104, spacing=8)
    y = map_card(im, zmap(zone, pts), y + 50)
    y = line(im, coords, y + 34, 54, GOLD)
    for h in hints:
        y = line(im, h, y + 2, 44, SICK)
    if credit:
        line(im, credit, y + 14, 32, (190, 190, 180, 230))
    return save(im, WORK, name)


REC = r'C:\Users\d2460n\Videos\World Of Warcraft\World Of Warcraft 2026.09.28 - {}.mp4'
# The user's own Barrens / Westfall runs (2090x1176, big UI): 478x850 around the
# character stays above the action bars and clear of unit frames and Issue Reporter.
# Segments (stem, start, end, speed, crop x). Times avoid the moments the Map & Quest Log
# is open (winscan.py, session 95e10ded scratchpad). Walking parts are sped up.
CLIPS = {
    'barrens': [('14.45.31.04', 113.0, 137.0, 1, 806)],
    'westfall': [('15.08.44.06', 64.2, 72.7, 1, 806), ('15.08.44.06', 81.3, 90.8, 1, 806)],
    # Stonetalon: road -> small path up the canyon (15:14), camp + Pocket Litter (15:21),
    # jump down the cliffs (15:22) then the Mound of Dirt, right of the character (x 880).
    'st_path': [('15.14.11.07', 20.0, 30.4, 1.6, 806), ('15.14.11.07', 36.2, 58.4, 3.2, 806),
                ('15.14.11.07', 60.2, 88.0, 5.0, 806)],
    'st_camp': [('15.21.44.08', 5.0, 18.0, 1, 806)],
    'st_dirt': [('15.22.05.09', 5.6, 24.0, 3.0, 880), ('15.22.05.09', 24.0, 26.9, 1, 880),
                ('15.22.05.09', 29.6, 39.0, 1, 880)],
}


def clip_len(key):
    return sum((e - s) / sp for _, s, e, sp, _ in CLIPS[key])


def rec_shot(i, key, dur):
    segs = list(CLIPS[key])
    gap = dur - clip_len(key)
    if gap > 0:                                 # need more footage: run the last segment longer
        st, s, e, sp, x = segs[-1]
        segs[-1] = (st, s, e + gap * sp, sp, x)
    out = os.path.join(WORK, f'rec_{i:02d}_{key}_{dur:.2f}.mp4')
    if os.path.exists(out):
        return out
    cmd = [FF, '-v', 'error', '-y']
    fc = []
    for j, (st, s, e, sp, x) in enumerate(segs):
        cmd += ['-ss', f'{s:.3f}', '-t', f'{e - s:.3f}', '-i', REC.format(st)]
        fc.append(f'[{j}:v]crop=478:850:{x}:0,setpts=(PTS-STARTPTS)/{sp},fps={FPS},setsar=1[s{j}]')
    fc.append(''.join(f'[s{j}]' for j in range(len(segs))) + f'concat=n={len(segs)}:v=1:a=0[c]')
    fc.append('[c]split[a][b];[b]crop=478:150:0:0,boxblur=14:2[t];'
              '[a][t]overlay=0:0,scale=1080:1920:flags=lanczos,'
              'eq=gamma=1.22:brightness=-0.02:saturation=1.08,unsharp=5:5:0.6,format=yuv420p[v]')
    run(cmd + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-an', '-t', f'{dur:.3f}',
               '-c:v', 'h264_nvenc', '-preset', 'p5', '-rc', 'vbr', '-cq', '19', '-b:v', '0', out])
    return out


def foot_png(name, step, head, zone, pts, tag, tag_col, lines, zoom=None, credit=None):
    """Card over the user's footage: everything sits in the top half so the character and
    the quest object (lower half of the frame) stay visible."""
    im = blank()
    B.backdrop(im, 470, 720, 420, 150)
    y = title(im, f'STEP {step}', 150, 46, fill=GOLD, spacing=14, glow=(0, 0, 0, 0))
    y = title(im, head, y + 12, 88, spacing=8)
    y = pill(im, tag, y + 22, B.CINZEL, 38, BONE, bg=tag_col[:3] + (235,), h=60)
    y = map_card(im, zmap(zone, pts, 500, zoom=zoom), y + 24)
    for ln, col in lines:
        y = line(im, ln, y + 14, 44, col) - 8
    if credit:
        line(im, credit, 1830, 30, (200, 200, 190, 230))
    return save(im, WORK, name)


def two_maps_png():
    """Step 1: Horde starts in the Barrens, Alliance in Westfall; each ends in the other zone."""
    im = blank()
    B.backdrop(im, 1000, 720, 760, 150)
    y = title(im, 'STEP 1', 210, 52, fill=GOLD, spacing=14, glow=(0, 0, 0, 0))
    y = title(im, 'THE NOTE', y + 20, 104, spacing=8)
    y += 50
    for zone, pts, lab, col in (('Barrens', [(46.4, 73.9, '1', MARK)], 'THE BARRENS  46, 74', HORDE),
                                ('Westfall', [(37.5, 50.7, '1', MARK)], 'WESTFALL  37, 51', ALLI)):
        m = zmap(zone, pts, 760)
        pill(im, lab, y, B.CINZEL, 40, BONE, bg=col[:3] + (235,), h=64)
        y = map_card(im, m, y + 82) + 34
    y = line(im, 'Horde starts in the Barrens, Alliance in Westfall', y, 44, BONE)
    y = line(im, 'click the Burned-Out Remains, turn in at the other one', y + 2, 42, SICK)
    line(im, 'then read the Nailed Plank right beside it', y + 2, 42, SICK)
    return save(im, WORK, 'step1')


def hook_png():
    im = blank()
    B.backdrop(im, 820, 720, 620, 150)
    y = title(im, 'HIDDEN', 300, 120, fill=GOLD, spacing=14, glow=(200, 150, 40, 255))
    y = title(im, 'XP BOOST', y + 20, 190, spacing=10, glow=(200, 120, 40, 255))
    y = icons_row(im, [BAG], y + 80, 190, border={BAG: EPIC})
    y = title(im, 'COZY SLEEPING BAG', y + 50, 74, fill=(200, 150, 255, 255), spacing=6, glow=(0, 0, 0, 0))
    line(im, '6-quest chain  ·  level 14+  ·  Horde + Alliance', y + 30, 50, SICK)
    return save(im, WORK, 'hook')


def what_png():
    im = blank()
    B.backdrop(im, 900, 720, 600, 150)
    y = title(im, 'WHAT IT DOES', 330, 104, spacing=8)
    y = icons_row(im, [BAG], y + 70, 150, border={BAG: EPIC})
    y = pill(im, 'Rest inside for 1 minute', y + 50, B.GEORGIA_I, 54, BONE, h=96)
    y = pill(im, 'bonus XP  ·  stacks up to 3 times', y + 26, B.GEORGIA_I, 54, GOLD, h=96)
    y = pill(im, '1 hour cooldown', y + 26, B.GEORGIA_I, 50, SICK, h=90)
    return save(im, WORK, 'what')


def rewards_png():
    im = blank()
    B.backdrop(im, 900, 720, 600, 150)
    y = title(im, 'YOUR LOOT', 330, 120, spacing=8)
    y = icons_row(im, [BAG, FODDER, TOOLBOX], y + 90, 150,
                  border={BAG: EPIC, FODDER: (255, 255, 255, 255), TOOLBOX: (255, 255, 255, 255)})
    y = line(im, 'Cozy Sleeping Bag  ·  Student Fodder', y + 50, 54, BONE)
    y = line(im, 'Old Toolbox, a 12-slot bag, on step 2', y + 6, 50, GOLD)
    y = line(im, 'plus a ranged weapon choice and good XP', y + 6, 46, SICK)
    return save(im, WORK, 'rewards')


def outro_png():
    im = blank()
    B.backdrop(im, 850, 660, 460, 150)
    y = title(im, 'BIG THANKS', 480, 60, fill=GOLD, spacing=12, glow=(0, 0, 0, 0))
    y = line(im, 'to naruobkhos for this guide', y + 20, 58, BONE)
    y = title(im, 'LIKE + FOLLOW', y + 70, 96)
    y = line(im, 'more WoW Forever guides every week', y + 40, 54, SICK)
    line(im, 'more info or a correction? comment!', y + 20, 46, GOLD)
    return save(im, WORK, 'outro')


CREDIT = 'route tips: Onsokomaru on Wowhead'

PLAN = [
    (hook_png, 'kalimdor', 'There is a hidden XP boost in WoW Forever. Here is how to get the Cozy Sleeping Bag.', 4.0),
    (what_png, 'eastern_kingdoms', 'Rest inside it for one minute and you get bonus experience, stacking up to three times. '
                                   'One hour cooldown.', 5.0),
    (lambda: place_png('step1a', 'Barrens', (46.4, 73.9, '1', MARK), 'HORDE START', HORDE, 'THE BARRENS',
                       'Burned-Out Remains  ·  46, 74', 'Alliance: turn in here + read the Nailed Plank'),
     'rec:barrens', 'You can start at level 14. Horde begins here in the Barrens: '
                    'click the Burned-Out Remains to get the note.', 5.0),
    (lambda: place_png('step1b', 'Westfall', (37.5, 50.7, '1', MARK), 'ALLIANCE START', ALLI, 'WESTFALL',
                       'Burned-Out Remains  ·  37, 51', 'Horde: turn in here + read the Nailed Plank'),
     'rec:westfall', 'Alliance begins here in Westfall. Then each side travels to the other zone, '
                     'turns in the note, and reads the Nailed Plank right next to it.', 6.0),
    (lambda: step_png('step2', 2, 'STONETALON', 'StonetalonMountains',
                      [(40.8, 52.5, 'A', MARK), (39.6, 49.9, 'B', MARK)],
                      'A  41, 53   ·   B  40, 50',
                      ['follow the path into the mountains to a camp:', 'loot the Pocket Litter (A)',
                       'jump down to the ledge for the Mound of Dirt (B)'], CREDIT),
     'kalimdor', 'Next, Stonetalon Mountains. Follow the path into the mountains to a small camp '
                 'and loot the Pocket Litter. Then jump down to the ledge below for the Mound of Dirt.', 6.0),
    (lambda: foot_png('step3', 3, 'LOCH MODAN', 'LochModan', [(49.5, 12.8, '3', MARK)], 'THE DAM  ·  49, 13',
                      (90, 90, 100), [('walk the top of the dam, drop onto the ledge', BONE),
                                      ('click the Carved Figurine', GOLD)], credit=CREDIT),
     'rec:lm_dam', 'Step three, Loch Modan. Walk along the top of the dam, then drop down onto the ledge below. '
                   'The Carved Figurine is right there.', 5.0),
    (lambda: foot_png('step4a', 4, 'HILLSBRAD SIDE', 'Hilsbrad', [(81.0, 56.0, '4', MARK)], 'NOT FROM ARATHI', HORDE,
                      [('face the gate to Arathi, turn left', BONE), ('follow the wall to the fallen cart', GOLD)],
                      credit=CREDIT),
     'rec:ar_cart', 'Last step. You have to come from the Hillsbrad side, not from Arathi. '
                    'Face the gate to Arathi, turn left, and follow the wall to a fallen cart.', 5.0),
    (lambda: foot_png('step4b', 4, 'THE CLIMB', 'Hilsbrad', [(81.0, 56.0, '4', MARK)], 'JUMPING PUZZLE', HORDE,
                      [('climb the cart, then jump up the rocks', BONE), ('all the way to the top of the wall', GOLD)]),
     'rec:ar_jump', 'Climb the cart, then do the little jumping puzzle up the rocks, all the way to the top of the wall.', 5.0),
    (lambda: foot_png('step4c', 4, 'THE CAMP', 'Arathi', [(22.5, 24.2, '4', MARK)], "THORADIN'S WALL  ·  22, 24",
                      (90, 90, 100), [('click the Messenger Bag', BONE),
                                      ('then the Hastily Rolled-Up Satchel', GOLD)]),
     'rec:ar_camp', 'At the camp on top, click the Messenger Bag, then the Hastily Rolled-Up Satchel to finish the chain.', 5.0),
    (rewards_png, 'dalaran', 'Your rewards: the Cozy Sleeping Bag and Student Fodder. On the way you also get '
                             'the Old Toolbox, a twelve slot bag, and a ranged weapon.', 5.0),
    (outro_png, 'kalimdor', 'Big thanks to naruobkhos for this guide. Like and follow for more WoW Forever guides. '
                            'More info or a correction? Leave a comment.', 4.0),
]


def main():
    files, tl, say, t = [], [], [], 0.0
    for i, (fn, art, text, mind) in enumerate(PLAN):
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        if art.startswith('rec:'):
            files.append(rec_shot(i, art[4:], dur))
        else:
            files.append(BP.shot(WORK, i, art, dur, seed=i * 13 + 5, bright=0.0 if i == 0 else -0.08))
        say.append((t + BP.LEAD, wav)); tl.append((t, dur)); t += dur
    total = t

    # One small ffmpeg graph per shot (frame + card over the backdrop), then a plain concat.
    # A single graph with 14 looped overlays over the 2-minute base hung ffmpeg (28/09/2026).
    frame = BP.frame_png(WORK)
    finals = []
    for i, (fn, *_ ) in enumerate(PLAN):
        a, d = tl[i]
        card = fn()
        fi, fo = (0.0, 0.15) if i == 0 else ((0.35, 0.0) if i == len(PLAN) - 1 else (0.25, 0.16))
        ch = '[2:v]format=rgba'
        if fi: ch += f',fade=t=in:st=0.1:d={fi}:alpha=1'
        if fo: ch += f',fade=t=out:st={max(0, d - fo):.3f}:d={fo}:alpha=1'
        tail = f',fade=t=out:st={d - 0.8:.3f}:d=0.8' if i == len(PLAN) - 1 else ''
        out = os.path.join(WORK, f'final_{i:02d}.mp4')
        run([FF, '-v', 'error', '-y', '-i', files[i],
             '-loop', '1', '-framerate', str(FPS), '-t', f'{d:.3f}', '-i', frame,
             '-loop', '1', '-framerate', str(FPS), '-t', f'{d:.3f}', '-i', card,
             '-filter_complex', f'[0:v]setsar=1[b];[1:v]format=rgba[f];[b][f]overlay=format=auto[bf];{ch}[c];'
                                f'[bf][c]overlay=format=auto{tail},format=yuv420p,setsar=1[v]',
             '-map', '[v]', '-an', '-t', f'{d:.3f}', '-r', str(FPS),
             '-c:v', 'h264_nvenc', '-preset', 'p7', '-tune', 'hq', '-rc', 'vbr', '-cq', '22', '-b:v', '0',
             '-maxrate', '13M', '-bufsize', '26M', out])
        finals.append(out)
        print('shot', i, 'ok', flush=True)

    lst = os.path.join(WORK, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p.replace(os.sep, '/')}'\n" for p in finals))
    base = os.path.join(WORK, 'base.mp4')
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base])
    audio = BP.mix_audio(WORK, 'hunter', total, say)
    run([FF, '-v', 'error', '-y', '-i', base, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', f'{total:.3f}', OUT])
    for i, (a, d) in enumerate(tl):
        print(f'{i} {a:6.2f} +{d:5.2f}')
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
