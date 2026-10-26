# -*- coding: utf-8 -*-
"""Short guide: Savory Whimsyfin Delight (ogre / murloc transform) in WoW Forever.

    py -3.11 build_whimsy.py

Reuses the profession-guide look (build_prof.py): loading-screen pans, icons read
from the beta client, edge-tts narration. Redridge map = client world-map tiles plus
its WorldMapOverlay tiles (redridge_map.py in session 95e10ded's scratchpad).
Facts (28/09/2026): Wowhead drop data, Icy Veins, ForeverChanges, AHledger beta prices.
"""
import os
from PIL import Image, ImageDraw, ImageFilter

import build_prof as BP
from build_prof import B, V, W, H, FPS, FF, GOLD, BONE, SICK, GREEN, run, blank, save, title, icon, pill

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'build', 'whimsy'); os.makedirs(WORK, exist_ok=True)
MAP = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\plans\redridge_full.png'
OUT = r'C:\Users\d2460n\Videos\World Of Warcraft\WoW Forever - Ogre or Murloc, Savory Whimsyfin Delight guide (EN).mp4'
UNCOMMON = (30, 255, 0, 255)
CYAN = (110, 210, 255, 255)
RECIPE, DISH, FISH, SPICE = 251526, 251525, 251524, 2678


REC = r'C:\Users\d2460n\Videos\World Of Warcraft\World Of Warcraft 2026.09.28 - 11.02.31.01.mp4'


def rec_shot(i, start, dur, bright=-0.05):
    """The user's own Redridge farming footage, 9:16 on the character, no UI.

    580x1030 at x=913 stays above the action bars (y~1040) and left of the minimap
    and quest tracker; the red error text at the top is blurred away."""
    out = os.path.join(WORK, f'rec_{i:02d}_{start}_{dur:.2f}_{bright}.mp4')
    if os.path.exists(out):
        return out
    fc = (f'[0:v]crop=580:1030:913:0,split[a][b];[b]crop=580:230:0:0,boxblur=18:2[t];'
          f'[a][t]overlay=0:0,scale=1080:1920:flags=lanczos,fps={FPS},'
          f'eq=gamma=1.16:brightness={bright}:saturation=1.08,unsharp=5:5:0.5,format=yuv420p[v]')
    run([FF, '-v', 'error', '-y', '-ss', str(start), '-t', f'{dur:.3f}', '-i', REC,
         '-filter_complex', fc, '-map', '[v]', '-an', '-t', f'{dur:.3f}',
         '-c:v', 'h264_nvenc', '-preset', 'p5', '-rc', 'vbr', '-cq', '19', '-b:v', '0', out])
    return out


def redridge(marker=False):
    """Redridge map, 1040 px wide, with the stray 'PPES' label painted over."""
    m = Image.open(MAP).convert('RGBA')
    patch = m.crop((880, 30, 970, 75))
    m.paste(patch, (770, 30))
    s = 1040 / m.width
    m = m.resize((1040, round(m.height * s)), Image.LANCZOS)
    if marker:
        cx, cy = 0.619 * m.width, 0.706 * m.height
        g = Image.new('RGBA', m.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=CYAN)
        m.alpha_composite(_alpha(g.filter(ImageFilter.GaussianBlur(26)), 0.75))
        d = ImageDraw.Draw(m)
        d.ellipse((cx - 58, cy - 58, cx + 58, cy + 58), outline=CYAN, width=7)
        d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=BONE, outline=(10, 30, 50, 255), width=3)
    return m


def _alpha(im, k):
    r, g, b, a = im.split()
    return Image.merge('RGBA', (r, g, b, a.point(lambda v: int(v * k))))


def map_card(im, m, y):
    sh = blank()
    ImageDraw.Draw(sh).rounded_rectangle(((W - m.width) // 2 - 6, y + 8, (W + m.width) // 2 + 6, y + m.height + 24),
                                         20, fill=(0, 0, 0, 235))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    im.alpha_composite(m, ((W - m.width) // 2, y))
    ImageDraw.Draw(im).rectangle(((W - m.width) // 2 - 2, y - 2, (W + m.width) // 2 + 1, y + m.height + 1),
                                 outline=GOLD, width=3)
    return y + m.height


def line(im, text, y, size=54, fill=BONE, maxw=960):
    f = B.fit(B.GEORGIA_I, text, maxw, size)
    d = ImageDraw.Draw(im)
    d.text((W / 2 + 3, y + 4), text, font=f, fill=(0, 0, 0, 235), anchor='ma')
    d.text((W / 2, y), text, font=f, fill=fill, anchor='ma')
    return y + f.getbbox('Ag')[3] + 18


def step_head(im, n, head, y=300):
    y = title(im, f'STEP {n}', y, 56, fill=GOLD, spacing=14, glow=(0, 0, 0, 0))
    return title(im, head, y + 26, 120, spacing=8)


def icons_row(im, items, y, size=150, border=None, sep=None):
    parts = []
    for it in items:
        parts.append(('i', it))
    gap = 40 if not sep else 110
    tot = len(items) * (size + 12) + (len(items) - 1) * gap
    x = (W - tot) // 2
    d = ImageDraw.Draw(im)
    for k, it in enumerate(items):
        im.alpha_composite(icon(it, size, border=(border or {}).get(it, (150, 150, 150, 255))), (x - 24, y - 24))
        if sep and k < len(items) - 1:
            f = B.font(B.CINZEL, 90, 900)
            d = ImageDraw.Draw(im)
            d.text((x + size + 12 + gap / 2, y + size / 2), sep[k], font=f, fill=GOLD, anchor='mm')
        x += size + 12 + gap
    return y + size + 12


# ----------------------------------------------------------------- cards

def hook_png():
    im = blank()
    B.backdrop(im, 820, 720, 600, 225)
    y = title(im, 'OGRE', 330, 200, spacing=14, glow=(200, 120, 40, 255))
    y = title(im, 'OR', y + 20, 80, fill=GOLD, spacing=12, glow=(0, 0, 0, 0))
    y = title(im, 'MURLOC?', y + 20, 180, fill=(150, 214, 255, 255), spacing=10, glow=(40, 120, 200, 255))
    y = icons_row(im, [DISH], y + 80, 190, border={DISH: (255, 255, 255, 255)})
    y = title(im, 'SAVORY WHIMSYFIN DELIGHT', y + 50, 64, fill=BONE, spacing=6, glow=(0, 0, 0, 0))
    line(im, 'the full guide  ·  WoW Forever', y + 30, 56, SICK)
    return save(im, WORK, 'hook')


def recipe_png():
    im = blank()
    B.backdrop(im, 900, 720, 560, 220)
    y = step_head(im, 1, 'THE RECIPE')
    y = icons_row(im, [RECIPE], y + 90, 170, border={RECIPE: UNCOMMON})
    y = title(im, 'Recipe: Savory Whimsyfin Delight', y + 50, 60, fill=UNCOMMON, spacing=0,
              font=BP.GEORGIA_B, glow=(0, 0, 0, 0))
    y = pill(im, 'Drops from mobs in Redridge Mountains', y + 60, B.GEORGIA_I, 50, BONE, h=92)
    pill(im, 'Requires Cooking 85', y + 30, B.GEORGIA_I, 50, SICK, h=92)
    return save(im, WORK, 'recipe')


def anymob_png():
    im = blank()
    B.backdrop(im, 1000, 720, 700, 225)
    y = title(im, 'WHICH MOB?', 250, 110, spacing=8)
    y = title(im, 'ANY OF THEM', y + 24, 80, fill=GOLD, spacing=10, glow=(0, 0, 0, 0))
    y = map_card(im, redridge(), y + 60)
    y = line(im, 'a zone-wide drop, like Savory Deviate Delight', y + 40, 48, SICK)
    y = line(im, 'confirmed: Great Goretusk  ·  Black Dragon Whelp', y + 6, 46, BONE)
    return save(im, WORK, 'anymob')


def buy_png():
    im = blank()
    B.backdrop(im, 900, 720, 520, 225)
    y = title(im, 'OR JUST BUY IT', 400, 110, spacing=8)
    y = icons_row(im, [RECIPE], y + 70, 130, border={RECIPE: UNCOMMON})
    y = title(im, '8 – 13 GOLD', y + 60, 170, fill=GOLD, spacing=8, glow=(200, 150, 40, 255))
    y = line(im, 'not bound  ·  Alliance auction house', y + 50, 54, BONE)
    line(im, 'beta prices, 28 Sept 2026', y + 10, 42, (190, 190, 180, 230))
    return save(im, WORK, 'buy')


def fish_png():
    im = blank()
    B.backdrop(im, 1000, 720, 700, 225)
    y = step_head(im, 2, 'THE FISH', 230)
    y = map_card(im, redridge(marker=True), y + 60)
    d = ImageDraw.Draw(im)
    y += 36
    f = B.fit(B.GEORGIA_I, 'Whimsyfin pools  ·  around 62, 71', 800, 50)
    lab = 'Whimsyfin pools  ·  around 62, 71'
    tw = B.text_w(f, lab) + 50
    x0 = (W - tw) // 2
    d.ellipse((x0, y + 6, x0 + 34, y + 40), outline=CYAN, width=6)
    d.text((x0 + 50, y + 23), lab, font=f, fill=BONE, anchor='lm')
    y = line(im, 'river south of Stonewatch Keep + the small lake', y + 80, 46, SICK)
    line(im, 'only 2 pools up at a time', y + 4, 46, SICK)
    return save(im, WORK, 'fish')


def fishtip_png():
    im = blank()
    B.backdrop(im, 900, 720, 520, 225)
    y = icons_row(im, [FISH], 380, 170)
    y = title(im, 'WHIMSYFIN', y + 50, 110, spacing=8)
    y = pill(im, 'Fishing ~150 to stop losing catches', y + 60, B.GEORGIA_I, 50, BONE, h=92)
    pill(im, 'or buy them: 4 – 7 silver each', y + 30, B.GEORGIA_I, 50, SICK, h=92)
    return save(im, WORK, 'fishtip')


def cook_png():
    im = blank()
    B.backdrop(im, 900, 720, 520, 225)
    y = step_head(im, 3, 'COOK IT', 380)
    y = icons_row(im, [FISH, SPICE, DISH], y + 110, 150, sep=['+', '='],
                  border={DISH: (255, 255, 255, 255)})
    y = line(im, '1 Whimsyfin  +  1 Mild Spices', y + 60, 58, BONE)
    line(im, 'Mild Spices: any cooking supplies vendor', y + 10, 46, SICK)
    return save(im, WORK, 'cook')


def effect_png():
    im = blank()
    B.backdrop(im, 900, 720, 560, 225)
    y = title(im, 'EAT IT', 330, 130, spacing=10)
    y = pill(im, '1 hour  ·  stays on in combat', y + 60, B.GEORGIA_I, 54, GOLD, h=96)
    y = title(im, 'MALE  →  MURLOC', y + 90, 86, fill=(150, 214, 255, 255), spacing=6, glow=(40, 120, 200, 255))
    y = title(im, 'FEMALE  →  OGRE', y + 50, 86, fill=(255, 170, 110, 255), spacing=6, glow=(200, 90, 40, 255))
    line(im, 'on the beta right now  ·  may change', y + 60, 46, (190, 190, 180, 230))
    return save(im, WORK, 'effect')


def outro_png():
    im = blank()
    B.backdrop(im, 850, 660, 330, 215)
    y = title(im, 'LIKE + FOLLOW', 700, 96)
    line(im, 'more WoW Forever guides every week', y + 40, 54, SICK)
    return save(im, WORK, 'outro')


# ------------------------------------------------------------------ plan

PLAN = [
    (hook_png, 'tall_eastern_kingdoms', 'Want to turn into an ogre or a murloc in WoW Forever? Here is how.', 4.0),
    (recipe_png, 'eastern_kingdoms', 'Step one, the recipe. It drops from random mobs in Redridge Mountains, '
                                     'and you need Cooking 85 to learn it.', 5.0),
    (anymob_png, 'old_ironforge', 'Which mob? Any of them. Just like Savory Deviate Delight in the Barrens, '
                                  'it is a zone-wide drop. So farm whatever dies fastest.', 5.0),
    (buy_png, 'dalaran', 'Or skip the grind. The recipe is not bound, and it sells for about 8 to 13 gold '
                         'on the beta auction house.', 5.0),
    (fish_png, 'eastern_kingdoms', 'Step two, the fish. Whimsyfin pools spawn east of Lake Everstill, '
                                   'in the river south of Stonewatch Keep. Only two pools are up at a time.', 5.0),
    (fishtip_png, 'zephras_isle', 'Bring about 150 fishing so you stop losing catches. '
                                  'Or buy the fish for a few silver each.', 4.5),
    (cook_png, 'old_ironforge', 'Step three, cook it. One Whimsyfin and one Mild Spices, '
                                'sold by any cooking supplies vendor.', 4.5),
    (effect_png, 'dalaran', 'Eat it and you transform for one hour, even in combat. On the beta, '
                            'male characters become murlocs, and female characters become ogres.', 5.0),
    (outro_png, 'tall_eastern_kingdoms', 'Like and follow for more WoW Forever guides.', 3.5),
]


def main():
    files, tl, say, t = [], [], [], 0.0
    for i, (fn, art, text, mind) in enumerate(PLAN):
        art = art.replace('tall_', '')
        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        files.append(BP.shot(WORK, i, art, dur, seed=i * 11 + 3, bright=0.0 if i == 0 else -0.08))
        say.append((t + BP.LEAD, wav)); tl.append((t, dur)); t += dur
    total = t

    lst = os.path.join(WORK, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p.replace(os.sep, '/')}'\n" for p in files))
    base = os.path.join(WORK, 'base.mp4')
    run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base])

    ovs = [(BP.frame_png(WORK), 0, total, 0, 0)]
    for i, (fn, *_ ) in enumerate(PLAN):
        a, d = tl[i]
        if i == 0:
            ovs.append((fn(), 0.0, a + d, 0.0, 0.15))      # frame zero = TikTok cover
        elif i == len(PLAN) - 1:
            ovs.append((fn(), a + 0.2, total, 0.35, 0.7))
        else:
            ovs.append((fn(), a + 0.1, a + d, 0.25, 0.16))

    audio = BP.mix_audio(WORK, 'paladin', total, say)
    cmd = [FF, '-v', 'error', '-y', '-i', base]
    for p, a, b, fi, fo in ovs:
        cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{b - a:.3f}', '-i', p]
    cmd += ['-i', audio]
    fc, last = ['[0:v]setsar=1[g0]'], '[g0]'
    for j, (p, a, b, fi, fo) in enumerate(ovs, start=1):
        ch = f'[{j}:v]format=rgba'
        if fi: ch += f',fade=t=in:st=0:d={fi}:alpha=1'
        if fo: ch += f',fade=t=out:st={max(0, b - a - fo):.3f}:d={fo}:alpha=1'
        fc.append(ch + f',setpts=PTS+{a:.3f}/TB[o{j}]')
        fc.append(f'{last}[o{j}]overlay=eof_action=pass:format=auto[v{j}]'); last = f'[v{j}]'
    fc.append(f'{last}fade=t=out:st={total - 0.8:.3f}:d=0.8,format=yuv420p,setsar=1[vout]')
    cmd += ['-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', f'{len(ovs) + 1}:a',
            '-c:v', 'h264_nvenc', '-preset', 'p7', '-tune', 'hq', '-rc', 'vbr', '-cq', '22', '-b:v', '0',
            '-maxrate', '13M', '-bufsize', '26M', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart', '-t', f'{total:.3f}', OUT]
    run(cmd)
    for i, (a, d) in enumerate(tl):
        print(f'{i} {a:6.2f} +{d:5.2f}  {PLAN[i][0].__name__}')
    print('OK', OUT, round(total, 2))


if __name__ == '__main__':
    main()
