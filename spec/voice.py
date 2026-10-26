# -*- coding: utf-8 -*-
"""English narration through Microsoft's neural voices (edge-tts).

Gives TikTok a clear spoken-English signal, which the music-only cuts did not
have: with no speech at all the platform falls back on the account's region to
decide who to show the video to.

Lines are cached on disk by (voice, rate, text) so rebuilds are cheap.
"""
import asyncio, hashlib, os, subprocess

try:
    import edge_tts
except Exception:
    edge_tts = None

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'voice_cache')
FF = r"C:\Users\d2460n\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
# edge-tts has been refused by Microsoft in France since 10/10/2026 (403): local Kokoro-82M instead.
ENGINE = 'edge'                    # edge-tts 7.3.1 fixed the 403 (14/10/2026); 'kokoro' = fallback
KOKORO_VOICE = 'am_adam'           # chosen by the user, 11/10/2026
KOKORO_SPEED = 1.06
VOICE = 'en-US-AndrewNeural'
RATE = '+6%'                      # a touch quicker than default, still natural


_KP = None


def _kokoro(text, path):
    global _KP
    import numpy as np, soundfile as sf
    if _KP is None:
        from kokoro import KPipeline
        _KP = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
    a = np.concatenate([x[2] for x in _KP(text, voice=KOKORO_VOICE, speed=KOKORO_SPEED)])
    sf.write(path, a, 24000)


def _say(text, voice, rate, path):
    async def go():
        await edge_tts.Communicate(text, voice, rate=rate).save(path)
    asyncio.run(go())


# Pronunciation dictionary (18/10/2026): name as written -> how the voice should say it.
# The screen keeps the real spelling; only the narration uses these. Check each one by transcription.
PRON = {
    'NohitJerome': 'No Hit Jerome',
    'Pshero': 'P S Hero',
    'Cdew': 'See Dew',
    'Venruki': 'Ven Rookie',
    'Warlockguy': 'Warlock Guy',
    'Oddwaffletv': 'Odd Waffle TV',
    'Fvp': 'F-V-P',
    'Minpojke': 'Min Poykeh',
    'Neepzen': 'Neep Zen',
    'Golemagg': 'Golem mag',
    'crocolisk': 'crocko-lisk',
}


def line(text, voice=VOICE, rate=RATE):
    """Render one line; returns (wav path, duration in seconds)."""
    # The voice reads "WoW" badly (user feedback, 27/09/2026): always say the full name.
    import re as _re
    text = _re.sub(r'\bW\s?o\s?W\b', 'World of Warcraft', text)
    for name, say in PRON.items():          # gamer tags the voice mangles: spoken spelling only
        text = _re.sub(r'\b%s\b' % _re.escape(name), say, text, flags=_re.I)
    os.makedirs(CACHE, exist_ok=True)
    tag = f'kokoro:{KOKORO_VOICE}:{KOKORO_SPEED}' if ENGINE == 'kokoro' else f'{voice}|{rate}'
    key = hashlib.sha1(f'{tag}|{text}'.encode('utf-8')).hexdigest()[:16] if ENGINE == 'kokoro' else         hashlib.sha1(f'{voice}|{rate}|{text}'.encode('utf-8')).hexdigest()[:16]
    mp3, wav = os.path.join(CACHE, key + ('.k.wav' if ENGINE == 'kokoro' else '.mp3')), os.path.join(CACHE, key + '.wav')
    if not os.path.exists(wav):
        if ENGINE == 'kokoro':
            _kokoro(text, mp3)
        else:
            _say(text, voice, rate, mp3)
        subprocess.run([FF, '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-ar', '48000', wav],
                       check=True)
    out = subprocess.run([FF, '-hide_banner', '-i', wav], capture_output=True, text=True).stderr
    dur = [l for l in out.splitlines() if 'Duration' in l][0].split('Duration:')[1].split(',')[0]
    h, m, s = dur.strip().split(':')
    return wav, float(h) * 3600 + float(m) * 60 + float(s)


def readable(t):
    """Fix what the voice reads literally.

    Checked by feeding each symbol through the voice and transcribing it back:
    '&' comes out as "and" and '+100%' as "plus 100 percent", both fine, but
    '/' is read as the word "slash".
    """
    return t.replace(' / ', ' or ').replace('/', ' or ')


def spoken(n):
    """Numbers read aloud the way a person would say them."""
    return {1: 'Number one', 2: 'Number two', 3: 'Number three',
            4: 'Number four', 5: 'Number five', 6: 'Number six'}[n]


if __name__ == '__main__':
    for t in ['Fury Warrior. Best stats, ranked.',
              'Weapon damage. Hit chance. Critical strike. Strength. Agility. Stamina.',
              'Number one. Weapon damage. The single most important stat while leveling.',
              'Remember. Dual wielding needs 27% hit to never miss a raid boss.',
              'Like and follow. One video for every spec. Which spec next?']:
        p, d = line(t)
        print(f'{d:5.2f}s  {t[:62]}')
