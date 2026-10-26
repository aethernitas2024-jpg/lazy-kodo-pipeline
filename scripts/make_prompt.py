"""Build the full production prompt (forever_fears_PROMPT.md) from the current script.

    py -3.11 make_prompt.py
Every scene = one on-screen card + the narration under it, so the prompt always matches the script.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, 'forever_fears_script.md')
OUT = os.path.join(HERE, 'forever_fears_PROMPT.md')
WPS = 159 / 60          # Edge "Andrew" at +6 %: ~159 words per minute

MOOD = {
    'HOOK': 'tense, cinematic build-up',
    'PART 1': 'warm, nostalgic, then slightly melancholic',
    'PART 2': 'investigative, low pulsing drums',
    'PART 3': 'dark, serious, slow strings',
    'PART 4': 'epic and bittersweet, wide orchestral',
    'PART 5': 'mysterious, then ironic and light for the retail prediction',
    'OUTRO': 'hopeful, rising, soft ending',
}

HEAD = """# FULL PRODUCTION PROMPT — "WoW Forever: my honest beta review, and my biggest fears"

Copy everything below into the AI tool or give it to the video editor. It is self-contained.

---

## 1. ROLE

You are a senior video editor and motion designer for a gaming channel about **World of Warcraft: Forever** (TikTok @d2460ng, brand "The Lazy Kodo"). You turn a finished narration script into a polished, long-form vertical opinion video. You never change the meaning of the narration and never invent facts.

## 2. GOAL

An honest, personal opinion video from a long-time WoW player after the WoW Forever beta: what he liked, what went wrong, why he thinks the game was rushed (with proof from the game files), his 5 fears, what Forever should have been, and how Forever will decide the future of WoW. The tone is **sincere, passionate and respectful**: critical of decisions, never insulting toward people. The video must make viewers **think and comment**.

Target audience: English-speaking WoW players (Classic, retail and Forever), 18-40, many nostalgic for the old WoW.

## 3. TECHNICAL FORMAT

- Vertical **1080 x 1920**, **60 fps** (30 fps acceptable), H.264, AAC 192 kbps, 48 kHz.
- Duration: about **{dur}** (the narration sets the length; do not speed it up).
- Language: English. On-screen text in English.
- Safe zones: keep all text between y = 230 and y = 1560 px (TikTok UI covers the top and bottom). Side margins 60 px.

## 4. VOICE

- Synthetic narrator: **Microsoft Edge TTS "en-US-AndrewNeural", rate +6 %**, natural pitch.
- Read the narration **exactly as written** (section 8). "WoW" must be pronounced **"World of Warcraft"** (never spelled W-O-W).
- Pronunciations: Xal'atath = "ZAL-ah-tath", Eldre'Thalas = "EL-dreh THA-lass", Azshara = "ah-ZHAR-ah", Sargeras = "SAR-geh-rass", Liadrin = "lee-AH-drin", Metzen = "MET-zen", Skyborne = "SKY-born", Lordaeron = "lor-DARE-on".
- 0.45 s of silence before each scene's narration, 0.9 s after. Light compression, voice peaks around -3 dBFS.

## 5. VISUAL IDENTITY

- Background: real in-game footage of the WoW Forever beta (player captures) or slow pans across official WoW Forever loading-screen art. **Never** AI-generated fantasy art, never generic stock footage, never retail-only assets unless the narration talks about retail.
- Every background gets: brightness -14 %, saturation +5 %, a dark vignette (top 300 px and bottom 340 px fading to near-black, edges darkened 30 %).
- Title cards ("cards") sit over the footage, centered horizontally, upper third:
  - **Kicker** (small line above): Cinzel, ~40 px, letter-spaced, gold #FFD25A.
  - **Big title**: Cinzel Bold, 100-140 px, ALL CAPS, colored per section (see palette), soft outer glow in a darker shade of the same color.
  - **Lines** under it: Georgia Italic, 36-52 px, cream #ECE8DA, key words in amber #FFBE50 or green #96D678, warnings in red #EB5A50.
- Palette: gold #FFD25A (facts, dates), epic purple #BE78FF (Forever, the future), red #EB5A50 (problems, fears), teal #78E6C8 (ideas), amber #FFBE50 (highlights), cream #ECE8DA (body text).
- Watermark: "The Lazy Kodo" badge, bottom center at (540, 1730), 60 % opacity, on the whole video.
- **Never** use the "→" or "≠" glyphs (missing in Cinzel): write "TO" / "IS NOT".

## 6. EDITING RULES

- The first 2 seconds must hit hard: open directly on the strongest image (Skyborne next to a blood elf, or a breathtaking water/fog shot) with the line "Blizzard sold it as Classic Plus. It's not." already visible as a caption. No logo intro, no slow title.
- Never stay more than ~6 s on the same shot: alternate footage, zoom-ins (Ken Burns 5-10 %), and card changes.
- Cards fade in over 0.25 s and out over 0.16 s. The final scene fades to black over 0.8 s.
- Data/proof scenes (game files, numbers) use a "datamine" look: dark panel, monospaced numbers, a subtle scan line, values counting up.
- Quotes from real people are shown as quotes, with the exact attribution given in section 8 ("relayed by Holly Longdale, 2026").
- Section changes (Part 1, Part 2...) get a 0.6 s whoosh + a short full-screen chapter card.

## 7. CAPTIONS, MUSIC, SOUND

- **Burned-in captions** for every spoken word: 2 lines max, Georgia Bold 54 px, white with black 6 px outline, centered at y = 1420, word-by-word highlight in amber. Keep "World of Warcraft", names and numbers exactly as spoken.
- Music: WoW soundtrack style (orchestral, no vocals), volume about -20 dB under the voice (ducking 6 dB while speaking). Moods per part are given in section 8. Use the in-game Hyjal / Mount Hyjal zone music where available.
- Light SFX only: whoosh on chapter cards, soft "ding" on number reveals, a low boom on "It's not." in the hook. No meme sounds.

## 8. SCENE-BY-SCENE PLAN

Estimated timecodes at Edge +6 %. Narration is final: use it word for word.
"""

TAIL = """
## 9. FOOTAGE TO USE (player captures from the beta)

Priority 1: Skyborne character next to a blood elf (same pose and light); water, lighting and fog shots (3-4); close-up of an original 2004 texture right after a beautiful shot; one boss from each new dungeon (Ruins of Lordaeron, Excavation Site, City of Dalaran).
Priority 2: megaserver chat getting heated (**blur every player name**), the empty battleground queue, an "Immune" message when a bleed fails on an elemental / undead / machine, levels 1-20 zones.
Priority 3: a Horde vs Alliance fight in the open world, a crowded capital city.
If a scene has no matching capture, use a slow pan over a WoW Forever loading screen (Emerald Dream, Vault, class art) behind the card.

## 10. FACTS: KEEP EXACTLY AS WRITTEN

- Skyborne: the race requires the Skyborne Heroic Pack ($29.99) on top of the subscription.
- Blizzard currently says: no battle pass, no WoW Token, no paid boosts ("right now").
- Skyborne game files: own model file, **but built on the blood elf skeleton**; armor, textures and helmets fall back to the blood elf (like void elves). **Never say "same model".**
- Beta client 1.60.1.70374: 271 rune engraving spells, 104 Waylaid Supplies items, 72 Nightmare Incursion items, Scarlet Enclave / Demon Fall Canyon / Crystal Vale maps (Season of Discovery leftovers).
- BlizzCon 2026: StarCraft shooter 2030, Diablo V 2029, The Last Titan 2027, Diablo animated series with Netflix.
- Turtle WoW: Blizzard won an injunction in April 2026; the server agreed to end operations.
- Midnight: ~500,000 players online in week one is a **third-party estimate**. Cataclysm (December 7, 2010): more than 12 million subscribers, 3.3 million copies sold in 24 hours (Blizzard figures).
- Metzen quote: "I wish we hadn't called it Warcraft. It sounds intimidating." was **relayed by Holly Longdale** (The Game Business, 2026), not said directly on record.
- Liadrin dies in patch 12.1.5 (October 14, 2026).
- Everything said as "my theory", "in my opinion", "I bet" is opinion: keep those words.

## 11. DO NOT

- Do not add facts, numbers, quotes or claims that are not in this prompt.
- Do not show real people's faces or photos (developers, streamers).
- Do not show readable player names or guild names.
- Do not use AI-generated characters or fake gameplay.
- Do not add political symbols, flags or memes.
- Do not change the narration, shorten it or reorder scenes.

## 12. PUBLISHING PACK

- Cover (frame used as thumbnail): Skyborne next to a blood elf, big Cinzel text. Title to be chosen by the creator (sincere, not clickbait). Suggestions: "I love WoW Forever. That's why I'm worried." / "My honest thoughts on WoW Forever, after the beta" / "WoW Forever deserves better".
- Description: "I played the WoW Forever beta and dug into the game files. My honest review, why I think Forever was rushed, and my biggest fears for its future. This is my opinion, and I'd love to read yours."
- Hashtags: #wowforever #worldofwarcraft #wow #warcraft #mmorpg #gaming
- Pinned comment: "Which fear do you share the most? 1 identity, 2 money, 3 pace, 4 gameplay, 5 tone"

## 13. DELIVERABLES

1. Final video MP4 (1080x1920, specs above).
2. The cover frame as PNG.
3. An .srt file of the captions.
4. A list of every scene with its final timecode, for review.
"""


def scenes(md):
    part, out, cur = 'HOOK', [], None
    for line in md.split('\n'):
        if line.startswith('### Sources'):
            break
        if line.startswith('## '):
            t = line[3:].strip()
            part = 'HOOK' if t.startswith('0.') else ('OUTRO' if t.startswith('OUTRO') else t.split(' —')[0])
            continue
        if line.startswith('### '):
            continue
        m = re.match(r'\[(.*)\]$', line.strip())
        if m:
            card = re.sub(r'^(Carte|Plans)\s*:\s*', '', m.group(1))
            cur = {'part': part, 'card': card, 'text': []}
            out.append(cur)
            continue
        if cur and line.strip() and not line.startswith(('---', '#', 'Durée', 'Partie')):
            cur['text'].append(line.strip())
    return [s for s in out if s['text']]


def fr_to_en(card):
    return (card.replace('fichiers du jeu : même squelette', 'game files: same skeleton')
                .replace("armure, textures et casques en repli sur l'elfe de sang", 'armor, textures and helmets fall back to the blood elf')
                .replace('brouillard, lumière, eau', 'fog, lighting, water footage')
                .replace('Plan de la bêta en jeu, gros titre :', 'beta gameplay footage, big title:'))


def main():
    md = open(SCRIPT, encoding='utf-8').read()
    sc = scenes(md)
    t, rows = 0.0, []
    for i, s in enumerate(sc, 1):
        text = ' '.join(s['text'])
        dur = max(4.0, len(text.split()) / WPS + 1.35)
        mood = next(v for k, v in MOOD.items() if s['part'].startswith(k))
        rows.append(f"### Scene {i:02d} · {int(t // 60)}:{int(t % 60):02d} · {s['part']}\n"
                    f"- **On screen:** {fr_to_en(s['card'])}\n"
                    f"- **Music mood:** {mood}\n"
                    f"- **Narration:** \"{text}\"\n")
        t += dur
    dur = f'{int(t // 60)} min {int(t % 60):02d} s'
    out = HEAD.format(dur=dur) + '\n' + '\n'.join(rows) + TAIL
    open(OUT, 'w', encoding='utf-8').write(out)
    print(len(sc), 'scenes,', dur, '->', OUT)


if __name__ == '__main__':
    main()
