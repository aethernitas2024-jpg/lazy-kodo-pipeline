p = r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\gather\build_tierchar.py'
s = open(p, encoding='utf-8').read()

# 1. race cards: support solo (male / female alone) layout
a = "def race_card(i, label):\n    def fn():"
b = "def race_card(i, label, mode='pair'):\n    def fn():"
assert a in s; s = s.replace(a, b, 1)
a = """        for x, t in ((270, 'MALE'), (810, 'FEMALE')):
            d.text((x + 3, 1503), t, font=f, fill=(0, 0, 0, 220), anchor='ma')
            d.text((x, 1500), t, font=f, fill=BONE, anchor='ma')
        return save(im, WORK, 'race_%02d' % i)"""
b = """        labels = ((270, 'MALE'), (810, 'FEMALE')) if mode == 'pair' else ((540, mode.upper()),)
        for x, t in labels:
            d.text((x + 3, 1503), t, font=f, fill=(0, 0, 0, 220), anchor='ma')
            d.text((x, 1500), t, font=f, fill=BONE, anchor='ma')
        return save(im, WORK, 'race_%02d_%s' % (i, mode))"""
assert a in s; s = s.replace(a, b, 1)

# 2. plan: solo shots for classes with few races, durations computed so the video lasts > 60 s
a = """for i, (r, label) in enumerate(RACES):
    PLAN.append((race_card(i, label), r, label.title() + ('. New in Forever!' if r in NEW else '.'), 3.0))"""
b = """SOLO = len(RACES) <= 4
NSEG = len(RACES) * (3 if SOLO else 1)
SEGDUR = max(5.0, (63.0 - 9.0 - 9.0 - 6.5) / NSEG)
for i, (r, label) in enumerate(RACES):
    say = label.title() + ('. New in Forever!' if r in NEW else '.')
    if SOLO:
        PLAN.append((race_card(i, label, 'male'), r + '|male', say, SEGDUR))
        PLAN.append((race_card(i, label, 'female'), r + '|female', '', SEGDUR))
        PLAN.append((race_card(i, label), r, '', SEGDUR))
    else:
        PLAN.append((race_card(i, label), r, say, SEGDUR))"""
assert a in s; s = s.replace(a, b, 1)
s = s.replace("Here it is on every playable race.\" %\n         (NAME, (', ' + SETNAME) if SETNAME else ''), 6.0)]",
              "Here it is on every playable race.\" %\n         (NAME, (', ' + SETNAME) if SETNAME else ''), 9.0)]")
s = s.replace("The full set only exists in one color so far.', 6.0))", "The full set only exists in one color so far.', 9.0))")
s = s.replace("follow for the other classes.', 6.0))", "follow for the other classes.', 6.5))")

# 3. seg: solo kind 'race|sex'
a = "    elif kind == 'bust':"
b = """    elif kind and '|' in kind:
        r, sx = kind.split('|')
        seq = os.path.join(SRC, '%s_%s' % (r, sx))
        flt, ow, oh = fit(seq, 900, 1000)
        cmd += ['-stream_loop', '-1', '-framerate', '30', '-i', os.path.join(seq, '%04d.png')]
        fc = ('[0:v]setsar=1[b];[2:v]fps=%d,format=rgba,%s[t];[b][t]overlay=%d:%d[s];'
              '[1:v]format=rgba,fade=t=in:st=0:d=0.2:alpha=1[o];[s][o]overlay=format=auto,format=yuv420p[v]'
              % (FPS, flt, (W - ow) // 2, TOP + 1000 - oh))
    elif kind == 'bust':"""
assert a in s; s = s.replace(a, b, 1)

# 4. main: segments without narration
a = """        wav, vd = V.line(V.readable(text))
        dur = max(mind, BP.LEAD + vd + BP.TAIL)
        finals.append(seg(i, fn(), kind, dur))
        say.append((t + BP.LEAD, wav)); tl.append((t, dur)); t += dur"""
b = """        if text:
            wav, vd = V.line(V.readable(text))
            dur = max(mind, BP.LEAD + vd + BP.TAIL)
            say.append((t + BP.LEAD, wav))
        else:
            dur = mind
        finals.append(seg(i, fn(), kind, dur))
        tl.append((t, dur)); t += dur"""
assert a in s; s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(s)
print('patched')
