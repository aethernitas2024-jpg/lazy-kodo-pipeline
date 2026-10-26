"""Point every script of the pipeline at this permanent folder instead of the old Temp scratchpads."""
import os

P = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline'
T = r'C:\Users\d2460n\AppData\Local\Temp\claude\C--Users-d2460n'
MAP = [(T + r'\061be861-66dd-49ff-9545-a1d33911f7dc\scratchpad\gather', P + r'\gather'),
       (T + r'\97ef56bb-069a-48ad-92f7-8edb5b997dd1\scratchpad', P + r'\spec'),
       (T + r'\95e10ded-1f23-4157-8eac-c380c8d1ca95\scratchpad', P + r'\plans')]
BS, FS = '\\', '/'


def forms(x):
    return [x, x.replace(BS, FS), x.replace(BS, BS + BS), '/c/' + x[3:].replace(BS, FS)]


n = 0
for root, _, files in os.walk(P):
    if 'voice_cache' in root or os.sep + 'build' in root:
        continue
    for f in files:
        if not f.endswith(('.py', '.sh')) or f == '_repath.py':
            continue
        p = os.path.join(root, f)
        s = open(p, encoding='utf-8', errors='surrogateescape').read()
        o = s
        for a, b in MAP:
            for fa, fb in zip(forms(a), forms(b)):
                s = s.replace(fa, fb)
        if s != o:
            open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
            n += 1
print('patched', n)
