"""Chapter score, quiet transition design, dedicated cover and delivery QC."""
import sys,json,subprocess,wave,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageEnhance
import build_forever_review as b

def score():
    scenes=json.loads((b.OUT/'scenes.json').read_text(encoding='utf-8'))
    sr=48000; length=round(sum(s['duration'] for s in scenes)*sr)
    mix=np.zeros((length,2),np.float32)
    mus=b.ROOT/'spec/music_class/hyjal'
    files=[mus/'1_summit_1.mp3',mus/'2_hyjal_general_3.mp3',mus/'3_summit_3.mp3',mus/'4_hyjal_general_1.mp3']
    cache=[]
    for p in files:
        r=subprocess.run([b.FF,'-v','error','-i',str(p),'-f','f32le','-ac','2','-ar',str(sr),'-'],capture_output=True,check=True)
        cache.append(np.frombuffer(r.stdout,dtype=np.float32).reshape(-1,2))
    starts=np.cumsum([0]+[s['duration'] for s in scenes])
    chapters=[(0,12,0),(12,21,1),(21,35,2),(35,40,3),(40,47,1),(47,50,0)]
    for first,end,track in chapters:
        a=round(starts[first]*sr); z=min(length,round(starts[end]*sr)); count=z-a
        src=cache[track]; take=np.tile(src,(math.ceil(count/len(src)),1))[:count].copy()
        fade=min(sr*2,len(take)//2); env=np.ones(count,np.float32)
        env[:fade]=np.linspace(0,1,fade); env[-fade:]=np.linspace(1,0,fade)
        mix[a:z]+=take*env[:,None]*.09
    rng=np.random.default_rng(48)
    for chapter in [1,12,21,35,40,47]:
        a=round(starts[chapter]*sr); count=round(.6*sr)
        noise=rng.standard_normal(count).astype(np.float32)
        noise=np.convolve(noise,np.ones(32)/32,mode='same')
        env=np.sin(np.linspace(0,np.pi,count))**2
        end=min(a+count,length); mix[a:end]+=(noise*env*.12)[:end-a,None]
    for chapter in [15,16,23,26,28]:
        a=round((starts[chapter]+1)*sr); count=round(.45*sr); t=np.arange(count)/sr
        ding=np.sin(2*np.pi*880*t)*np.exp(-t*12)*.025
        end=min(a+count,length); mix[a:end]+=ding[:end-a,None]
    mix[:sr]*=np.linspace(0,1,sr)[:,None]; mix[-sr*3:]*=np.linspace(1,0,sr*3)[:,None]
    with wave.open(str(b.OUT/'chapter_score.wav'),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes())
    print('Chapter score ready',flush=True)

def final():
    b.run(['-i',b.OUT/'assembly.mp4','-i',b.OUT/'chapter_score.wav','-filter_complex','[0:a]asplit=2[voice][key];[1:a][key]sidechaincompress=threshold=0.015:ratio=4:attack=30:release=650[duck];[voice][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[out]','-map','0:v','-map','[out]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',b.OUT/'delivery_temp.mp4'])
    (b.OUT/'delivery_temp.mp4').replace(b.OUT/'WoW_Forever_Honest_Review_EN.mp4')
    image=Image.open(b.SKY/'Skyborne_Blizzard_13.jpg').convert('RGB')
    # Full official scene stays visible inside a blurred portrait background.
    from PIL import ImageOps,ImageFilter
    base=ImageOps.fit(image,(1080,1920)).filter(ImageFilter.GaussianBlur(22))
    base=ImageEnhance.Brightness(base).enhance(.42).convert('RGBA')
    top=ImageOps.contain(image,(1080,820));base.alpha_composite(top.convert('RGBA'),((1080-top.width)//2,650))
    d=ImageDraw.Draw(base);b.center(d,'THE LAZY KODO',280,38,b.GOLD)
    b.center(d,'I LOVE WOW FOREVER.',390,76,b.CREAM)
    b.center(d,'THAT’S WHY I’M WORRIED.',1390,67,b.GOLD)
    b.center(d,'MY HONEST BETA REVIEW',1630,32,b.CREAM)
    base.convert('RGB').save(b.OUT/'cover.png')
    # Decode first and last frames and read the actual container/codec headers.
    p=subprocess.run([b.FF,'-hide_banner','-i',str(b.OUT/'WoW_Forever_Honest_Review_EN.mp4')],capture_output=True,text=True)
    report='\n'.join(x for x in p.stderr.splitlines() if 'Duration:' in x or 'Stream #' in x)
    b.run(['-sseof','-1','-i',b.OUT/'WoW_Forever_Honest_Review_EN.mp4','-frames:v','1',b.OUT/'qa_last.png'])
    (b.OUT/'technical_QA.txt').write_text(report,encoding='utf-8')
    print(report,flush=True)
if __name__=='__main__':
    if '--score' in sys.argv: score()
    else: final()
