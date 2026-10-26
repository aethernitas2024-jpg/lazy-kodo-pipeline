"""V2 corrections (16/10/2026), on top of build_forever_review_v2.

    py -3.11 repair_review_v2_corrections.py

- Scene 35: the Overwatch line said "Overwatch is that game"; the creator meant that Overwatch is a good
  example of an original title that fits that other audience better.
- Scene 15: "Turtle World of Warcraft" -> "Turtle WoW" (a proper name). Scene 25: "World of Warcraft Token"
  -> "WoW Token". The voice is given "Wow" (Edge reads "WoW" badly), the captions show "WoW".
- 2nd pass: scene 9 "some veteran players"; scene 34 Metzen and Garrosh instead of Thrall.
- The small grey "THE LAZY KODO" text is replaced by the real channel badge (watermark.py, centre 540,1730).
Every scene is re-rendered (the old text is burned in); shots are cached, so only overlays are redone.
The previous masters are moved to review_v2/before_corrections/.
"""
import asyncio
import inspect
import json
import re
import shutil
import sys
from pathlib import Path

import build_forever_review as b
import build_forever_review_v2 as v

sys.path.insert(0, str(b.ROOT / 'gather'))
import watermark  # noqa: E402

OLD_OW = ("they can make another game. Overwatch is that game, and I don't mind, Overwatch is Overwatch.")
NEW_OW = ("they can make another game, for that audience. Overwatch is a good example: an original title "
          "that fits that other audience much better. And I don't mind, Overwatch is Overwatch.")
FIX = {15: [('Turtle World of Warcraft', 'Turtle Wow')],
       25: [('no World of Warcraft Token', 'no Wow Token')],
       35: [(OLD_OW, NEW_OW)],
       # 16/10, 2nd pass: "some" veterans, not "a lot of"; Metzen: his writing of Garrosh rather than voicing Thrall.
       9: [('but a lot of veteran players are really hard on beginners', 'but some veteran players are really hard on beginners')],
       34: [('Really? The man who voiced Thrall, the Warchief of the Horde? I find that very hard to believe.',
             'Really? The man who helped write Garrosh Hellscream, one of the most brutal warlords in Warcraft? '
             'I find that very hard to believe. Unless he said it in a sarcastic way.')]}
FIX[6] = [("They don't play like Classic dungeons. The bosses have more mechanics, more ideas. And honestly, I love it.",
           "Some bosses have a few more mechanics than in Classic. Nothing revolutionary, but it's a nice touch.")]
v.TITLES[6] = 'A FEW NEW IDEAS'   # was "SMARTER BOSSES": the creator found his first claim exaggerated
FIX[46] = [("And retail? Come on, we all know how that ends. Xal'atath didn't get to merge with Azeroth, so someone else will.",
            "And retail? Honestly, I wouldn't be surprised if it ends like this. Xal'atath fails to merge with Azeroth, "
            "so someone else does it instead.")]
# Scenes to rebuild on this run (default: all corrected scenes). e.g. py repair_review_v2_corrections.py 9 34
REDO = {int(a) for a in sys.argv[1:] if a.isdigit()} or (set() if '--captions' in sys.argv else set(FIX))
ALL_SCENES = '--captions' in sys.argv   # re-render every scene for the new captions (voices and shots kept)

SAVE = v.OUT / 'before_corrections'


def fix_texts():
    for s in v.scenes:
        for a, z in FIX.get(s['n'], []):
            if a not in s['text']:
                raise SystemExit('scene %d: text not found: %r' % (s['n'], a))
            s['text'] = s['text'].replace(a, z)
            s.pop('words', None)
            s.pop('audio', None)


async def voices():
    for s in v.scenes:
        if s['n'] in FIX:
            await b.speech(s, asyncio.Semaphore(1))
            timing = v.OUT / ('voice_%02d.json' % s['n'])
            fixed = timing.read_text(encoding='utf-8').replace('"text": "Wow"', '"text": "WoW"')
            timing.write_text(fixed, encoding='utf-8')
            s['words'] = [dict(w, text='WoW' if w['text'] == 'Wow' else w['text']) for w in s['words']]


MAXC = 42   # characters per caption (2 lines on screen)


def _norm(x):
    return re.sub(r'[^0-9a-z]', '', x.lower())


def smart_captions(s):
    """Captions cut at sentence ends and voice pauses, with the script's punctuation (16/10/2026).

    Same .ass layout and karaoke timing as build_forever_review.captions; only the grouping and the shown
    words change. Words are re-aligned on the scene text to get their punctuation back.
    """
    words = s['words']
    toks = s['text'].replace('Wow', 'WoW').split()
    shown, k = [], 0
    for w in words:
        span = len(w['text'].split())          # the voice sometimes merges tokens ("24 hours")
        nw = _norm(w['text'])
        j = k
        while j < len(toks) and j < k + 6 and _norm(''.join(toks[j:j + span])) != nw:
            j += 1
        if j < len(toks) and _norm(''.join(toks[j:j + span])) == nw:
            shown.append(' '.join(toks[j:j + span])); k = j + span
        else:
            shown.append(w['text'])
    n = len(words)
    gap = [(words[i + 1]['t'] - words[i]['t'] - words[i]['d']) if i + 1 < n else 1.0 for i in range(n)]
    end_s = [bool(re.search(r'[.?!]["”\']?$', x)) for x in shown]
    end_c = [bool(re.search(r'[,:;—-]$', x)) for x in shown]

    def cost(i, j):          # caption = words i..j-1
        txt = ' '.join(shown[i:j])
        if len(txt) > MAXC and j - i > 1:
            return None
        last = j - 1
        c = 0.0 if (end_s[last] or j == n) else (1.0 if end_c[last] or gap[last] > 0.25 else 6.0)
        c += 4.0 * sum(end_s[i:last])                       # avoid mixing two sentences
        if len(txt) < 14 and not (end_s[last] or j == n):
            c += 3.0                                        # no tiny fragments mid-sentence
        return c + 0.6 * (1 - len(txt) / MAXC)
    best = [0.0] + [None] * n
    prev = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - 14), j):
            if best[i] is None:
                continue
            c = cost(i, j)
            if c is not None and (best[j] is None or best[i] + c < best[j]):
                best[j], prev[j] = best[i] + c, i
    cuts, j = [], n
    while j > 0:
        cuts.append((prev[j], j)); j = prev[j]
    lines = []
    s['captions'] = []
    for i, j in reversed(cuts):
        g = words[i:j]
        start, end = g[0]['t'] + .45, g[-1]['t'] + g[-1]['d'] + .45
        txt = ''
        for q, w in enumerate(g):
            dur = (g[q + 1]['t'] - w['t']) if q + 1 < len(g) else w['d']
            txt += r'{\kf' + str(max(1, round(dur * 100))) + '}' + shown[i + q] + ' '
        lines.append(f'Dialogue: 0,{b.stamp(start, True)},{b.stamp(end, True)},Default,,0,0,0,,{txt.strip()}')
        s['captions'].append((start, end, ' '.join(shown[i:j])))
    path = b.OUT / f'captions_{s["n"]:02}.ass'
    path.write_text(b.ASSHEAD + '\n'.join(lines), encoding='utf-8')
    return path


# 16/10/2026: the creator wants no source credits on screen (they stay listed in SOURCES_ET_MODIFICATIONS.md).
# Notes that explain the content (not a source) are kept: "Historical subscribers. Not concurrent players.",
# "RELAYED BY HOLLY LONGDALE", "CURRENT STATED POLICY...", "POSSIBLE FUTURES / MY OPINION".
DROP_LABELS = {
    'BLIZZARD PROMOTIONAL ARCHIVE / VIA OUTNOW', 'BLIZZARD / FOREVER PANEL RECAP / SEPTEMBER 2026',
    'BLIZZARD / SKYBORNE ANNOUNCEMENT / 2026', 'ARCHIVE: OUTNOW / FOREVER: BLIZZARD',
    'BLIZZARD / WHAT’S NEXT PANEL / SEPTEMBER 12, 2026', 'BLIZZCON 2026 / EDITORIAL TIMELINE',
    'CREATOR DATAMINE / EDITORIAL GRAPHIC', 'Build 1.60.1.70374 / not an official Blizzard chart',
    'CREATOR-REPORTED CLIENT FINDINGS', 'BLIZZARD / US STORE PRICE / 2026',
    'BLIZZARD / DECEMBER 13, 2010 / SALES, NOT CONCURRENCY', 'THE GAME BUSINESS / FEBRUARY 2026'}
RENAME_LABELS = {'ORIGINAL ERA / PROMOTIONAL ARCHIVE': 'ORIGINAL ERA', 'FOREVER / BLIZZARD / 2026': 'WOW FOREVER',
                 'ORIGINAL PUBLISHED GRAPHIC / 2010': 'BACK IN 2010'}


def no_sources():
    real = v.label

    def label(d, txt, *a, **k):
        if txt in DROP_LABELS or txt.startswith('ACTIVISION BLIZZARD / 2010 ANNUAL REPORT'):
            return
        return real(d, RENAME_LABELS.get(txt, txt), *a, **k)
    v.label = label


def drop_board_cache():
    """Boards are cached as PNG (assets) and as clips (work, keyed without the image): clear both."""
    (SAVE / 'boards').mkdir(exist_ok=True)
    for p in v.A.glob('board_*.png'):
        shutil.move(str(p), str(SAVE / 'boards' / p.name))
    for cf in v.OUT.glob('cuts_[0-9][0-9].json'):
        n = int(cf.stem[-2:])
        for i, cut in enumerate(json.loads(cf.read_text())):
            if cut['kind'] != 'video':
                for p in v.WORK.glob('s%02d_%02d_*' % (n, i)):
                    shutil.move(str(p), str(SAVE / 'work' / p.name))


def no_brand_text():
    src = inspect.getsource(v.render_scene)
    line = "    raw+=f'\\nDialogue: 1,0:00:00.00,{b.stamp(s[\"duration\"],True)},Brand,,0,0,0,,THE LAZY KODO'\n"
    if line not in src:
        raise SystemExit('brand line not found in render_scene')
    # Scene 16: the "500K UNCORROBORATED / DO NOT COMPARE" overlay contradicted the narration and sat on the
    # chart's own title; the caption under the chart ("Not concurrent players") already gives the nuance.
    i = src.index('    if n==16:')
    j = src.index('\n', src.index('\n', i) + 1) + 1
    if 'UNCORROBORATED' not in src[i:j]:
        raise SystemExit('scene 16 overlay not found in render_scene')
    src = src[:i] + src[j:]
    # No source credit under the video clips either (see DROP_LABELS).
    i = src.index("    for cut in cuts:\n        if cut['kind']=='video':")
    j = src.index(",Credit,,0,0,0,,{txt}'\n", i) + len(",Credit,,0,0,0,,{txt}'\n")
    src = src[:i] + src[j:]
    exec(compile(src.replace(line, ''), v.__file__, 'exec'), v.__dict__)


def main():
    SAVE.mkdir(exist_ok=True)
    for p in list(v.OUT.glob('scene_[0-9][0-9].mp4')) + [v.OUT / 'WoW_Forever_Review_V2_EN.mp4',
                                                         v.OUT / 'WoW_Forever_V2_Compact_H264.mp4']:
        if p.exists() and not (SAVE / p.name).exists():   # never overwrite the saved originals on a rerun
            shutil.move(str(p), str(SAVE / p.name))
    # Still-image shots are cached without their duration: drop the cached clips of the re-voiced scenes.
    (SAVE / 'work').mkdir(exist_ok=True)
    for n in REDO:
        for p in v.WORK.glob('s%02d_*' % n):
            shutil.move(str(p), str(SAVE / 'work' / p.name))
        done = v.OUT / ('scene_%02d.mp4' % n)
        if done.exists():
            done.unlink()   # an already corrected render (the originals are in before_corrections)
    if ALL_SCENES:
        for p in v.OUT.glob('scene_[0-9][0-9].mp4'):
            p.unlink()
        drop_board_cache()
    no_sources()
    b.captions = smart_captions
    b.PANELS[25] = [(x, 'WoW Token' if y == 'World of Warcraft Token' else y) for x, y in b.PANELS[25]]
    stale = v.A / 'board_policy_.png'
    if stale.exists():
        shutil.move(str(stale), str(SAVE / stale.name))
    for n in REDO:
        for ext in ('.mp3', '.json', '.wav'):
            old = v.OUT / ('voice_%02d%s' % (n, ext))
            if old.exists():
                old.unlink()
    fix_texts()
    asyncio.run(voices())
    no_brand_text()
    asyncio.run(v.main())
    master = v.OUT / 'WoW_Forever_Review_V2_EN.mp4'
    w, h = watermark.Image.open(watermark.badge()).size
    out = v.OUT / 'WoW_Forever_V2_Compact_H264.mp4'
    b.run(['-i', master, '-i', watermark.badge(), '-filter_complex',
           '[0:v][1:v]overlay=%d:%d:format=auto,format=yuv420p[v]' % (540 - w // 2, 1730 - h // 2),
           '-map', '[v]', '-map', '0:a', '-c:a', 'copy', '-c:v', 'h264_nvenc', '-preset', 'p7', '-tune', 'hq',
           '-rc', 'vbr', '-cq', '24', '-b:v', '0', '-spatial-aq', '1', '-aq-strength', '8', '-bf', '3',
           '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out])
    derivatives()
    print('DONE', out)


def derivatives():
    """HEVC copy for TikTok (~150 MB) and a 720p H.264 copy for WhatsApp (~70 MB), both with the badge."""
    w, h = watermark.Image.open(watermark.badge()).size
    b.run(['-i', v.OUT / 'WoW_Forever_Review_V2_EN.mp4', '-i', watermark.badge(), '-filter_complex',
           '[0:v][1:v]overlay=%d:%d:format=auto,format=yuv420p[v]' % (540 - w // 2, 1730 - h // 2),
           '-map', '[v]', '-map', '0:a', '-c:a', 'copy', '-c:v', 'hevc_nvenc', '-preset', 'p7', '-tune', 'hq',
           '-rc', 'vbr', '-cq', '31', '-b:v', '0', '-spatial-aq', '1', '-aq-strength', '8', '-rc-lookahead', '32',
           '-bf', '4', '-tag:v', 'hvc1', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
           v.OUT / 'WoW_Forever_V2_Max_Compression_HEVC.mp4'])
    common = ['-i', v.OUT / 'WoW_Forever_V2_Compact_H264.mp4', '-vf', 'scale=720:1280:flags=lanczos,format=yuv420p',
              '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'main', '-level', '4.0',
              '-b:v', '620k', '-maxrate', '1200k', '-bufsize', '2400k', '-passlogfile', v.WORK / 'wa2pass']
    b.run(common + ['-pass', '1', '-an', '-f', 'null', 'NUL'])
    b.run(common + ['-pass', '2', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-movflags', '+faststart',
                    v.OUT / 'WoW_Forever_V2_WhatsApp_720p.mp4'])


if __name__ == '__main__':
    main()
