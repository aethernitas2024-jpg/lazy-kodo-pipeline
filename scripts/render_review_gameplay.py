import json,os,time
import build_forever_review as b
os.chdir(b.OUT)
scenes=json.loads((b.OUT/'scenes.json').read_text(encoding='utf-8'))
for n in (5,6):
    p=b.OUT/('scene_%02d.mp4'%n)
    if p.exists(): p.rename(p.with_suffix('.backup_'+str(int(time.time()))+'.mp4'))
    b.render(scenes[n-1])
