# -*- coding: utf-8 -*-
"""Backdrop for build_stress.py: the user's stress test screenshot, cropped above the French UI text.

Inpainting the tooltip left visible smears, so the crop stops above it (the crowd is all in the top 950 px).
"""
from PIL import Image

SRC = 'F:/blizz/World of Warcraft/_forever_/Screenshots/WoWScrnShot_102126_231657.jpg'
im = Image.open(SRC).convert('RGB').crop((120, 0, 4820, 950))   # minimap starts at x 4840
im = im.resize((round(im.width * 1920 / im.height), 1920), Image.LANCZOS)
im.save('load/tall_stress.jpg', quality=93)
print(im.size)
