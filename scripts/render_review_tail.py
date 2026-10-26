"""Render the second half into staging and publish completed scene files atomically."""
import os,json
import build_forever_review as b
delivery=b.OUT
scenes=json.loads((delivery/'scenes.json').read_text(encoding='utf-8'))
b.OUT=delivery/'render_staging';b.OUT.mkdir(exist_ok=True)
os.chdir(b.OUT)
for s in reversed(scenes[25:]):
    name='scene_%02d.mp4'%s['n']
    if (delivery/name).exists(): continue
    b.render(s)
    try: (b.OUT/name).replace(delivery/name)
    except PermissionError: print('Main renderer already owns',name,flush=True)
print('TAIL COMPLETE',flush=True)
