# Lazy Kodo — pipeline de shorts automatisés

Chaîne de production de vidéos verticales (TikTok / Shorts) pour la chaîne **The Lazy Kodo**, consacrée à WoW Forever. Chaque vidéo est un script Python qui assemble de A à Z la narration, les visuels, les sous-titres et le rendu final.

Ce dépôt ne contient que le code et les notes. Les rendus, voix, captures et données de jeu (≈ 10 Go) restent en local.

## Ce que fait le pipeline

| Étape | Outils | Fichiers |
|---|---|---|
| Collecte des données (objets, stats, notes de patch) | JSON Wowhead mis en cache | `gather/tooltip.py`, `gather/oldstats.py`, `plans/dbdiff.py` |
| Plan de la vidéo (scènes, timings) | Python | `gather/plan_*.py`, `plans/plan_*.py` |
| Narration | voix neuronales (edge-tts), cache par hash | `spec/voice.py`, `plans/tvoice.py` |
| Transcription et calage des sous-titres | faster-whisper, sous-titres ASS | `plans/transcribe.py` |
| Composition visuelle | Pillow, NumPy (infobulles façon jeu, cartes, icônes) | `gather/build_*.py`, `plans/route_map.py` |
| Rendu et compression | FFmpeg | `scripts/render_*.py`, `scripts/compress_*.py` |
| Filigrane de la chaîne | Pillow + FFmpeg | `gather/watermark.py` |

Exemples de séries produites : guides de métiers 1-300 (`build_prof.py`), routes de leveling par faction (`build_route_*.py`, `build_r30_*.py`), analyses de patch (`build_patch.py`), présentations de donjons (`spec/build.py`).

## Méthode de travail

Tout le pipeline a été écrit avec **Claude Code**. Chaque short suit le même schéma : un script `plan_*` qui fixe le contenu et le timing, puis un script `build_*` qui rend la vidéo de façon reproductible. On peut ainsi corriger un détail et relancer le rendu sans retoucher la vidéo à la main.

Voir aussi le dépôt **wowedit**, le moteur de montage calé sur le rythme de la musique.
