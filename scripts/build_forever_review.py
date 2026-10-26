"""Reproducible 50-scene editorial cut. Run with Python 3.11."""
import asyncio, json, math, re, subprocess, sys, textwrap, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import edge_tts

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'review_pro'; OUT.mkdir(exist_ok=True)
FF=r'C:\Users\d2460n\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
FONT=Path(r'C:\Users\d2460n\Documents\aout\output\paris_paloma_lyrics\fonts\Cinzel.ttf')
GEORGIA=Path(r'C:\Windows\Fonts\georgiab.ttf')
W,H,FPS=1080,1920,30
GOLD='#FFD25A'; CREAM='#ECE8DA'; RED='#EB5A50'; PURPLE='#BE78FF'; TEAL='#78E6C8'
def run(args):
    p=subprocess.run([FF,'-hide_banner','-loglevel','error','-y']+list(map(str,args)),capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-5000:])
def font(n,serif=False): return ImageFont.truetype(str(GEORGIA if serif else FONT),n)
def wrap(txt,f,width):
    lines=[]; line=''
    for word in txt.split():
        test=(line+' '+word).strip()
        if f.getlength(test)>width and line: lines.append(line); line=word
        else: line=test
    if line: lines.append(line)
    return lines
def center(d,txt,y,size,col=CREAM,width=920,serif=False):
    f=font(size,serif)
    for line in wrap(txt,f,width):
        d.text((540,y),line,font=f,fill=col,anchor='mt',stroke_width=1,stroke_fill='#080B13'); y+=size*1.28
    return y
def stamp(t,ass=False):
    if ass:
        c=round(t*100); return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
    c=round(t*1000); return f'{c//3600000:02}:{c//60000%60:02}:{c//1000%60:02},{c%1000:03}'
prompt=(ROOT/'scripts/forever_fears_PROMPT.md').read_text(encoding='utf-8')
scenes=[]
for match in re.finditer(r'### Scene (\d+) · ([^\n]+)\n(.*?)(?=\n### Scene|\n## 9\.)',prompt,re.S):
    n=int(match[1]); body=match[3]
    screen=re.search(r'\*\*On screen:\*\* (.*)',body)[1]
    narration=re.search(r'\*\*Narration:\*\* "(.*?)"\s*$',body,re.S)[1]
    title=re.search(r'"([^"]+)"',screen)
    title=title[1] if title else 'LIGHT. FOG. WATER.'
    scenes.append(dict(n=n,part=match[2].split(' · ')[-1],screen=screen,title=title,text=re.sub(r'\bWoW\b','World of Warcraft',narration)))
assert len(scenes)==50,len(scenes)

async def speech(s,sem):
    target=OUT/f'voice_{s["n"]:02}.mp3'; timing=target.with_suffix('.json')
    async with sem:
        if not (target.exists() and timing.exists()):
            for attempt in range(3):
                try:
                    words=[]
                    with target.open('wb') as f:
                        async for e in edge_tts.Communicate(s['text'],'en-US-AndrewNeural',rate='+6%',boundary='WordBoundary').stream():
                            if e['type']=='audio': f.write(e['data'])
                            elif e['type']=='WordBoundary': words.append(dict(t=e['offset']/1e7,d=e['duration']/1e7,text=e['text']))
                    timing.write_text(json.dumps(words,ensure_ascii=False),encoding='utf-8'); break
                except Exception:
                    if attempt==2: raise
                    await asyncio.sleep(2)
        wav=target.with_suffix('.wav')
        if not wav.exists(): run(['-i',target,'-ar','48000','-ac','1',wav])
        with wave.open(str(wav)) as f: dur=f.getnframes()/f.getframerate()
        s.update(audio=str(wav),words=json.loads(timing.read_text(encoding='utf-8')),duration=math.ceil((dur+1.35)*FPS)/FPS)
        print('VOICE',s['n'],round(dur,2),flush=True)

PANELS={
14:[('2030','StarCraft'),('2029','Diablo V'),('2027','The Last Titan')],
16:[('12M+','Subscribers | 2010'),('3.3M','Copies sold in 24h | 2010'),('~500K','Online estimate | unverified')],
17:[('271','Rune engraving spells'),('104','Waylaid Supplies items'),('72','Nightmare Incursion items')],
24:[('$29.99','Skyborne Heroic Pack'),('+ SUB','Active subscription required')],
25:[('NO','Battle pass'),('NO','World of Warcraft Token'),('NO','Paid boosts | currently')],
27:[('OWN MODEL','Blood elf skeleton'),('4690403 / 4690402','Skeleton file IDs'),('FALLBACKS','Armor / textures / helmets')],
29:[('DEC 9','Raids'),('WINTER','Hardcore'),('SPRING / SUMMER','Major content updates')],
42:[('01','Big hype. Fast fade.')],43:[('02','Forever becomes the main game')],44:[('03','A modern World of Warcraft 2')]
}
NOTES={16:'Different metrics. No direct audience comparison.',17:'Creator-reported client findings | build 1.60.1.70374',18:'OPINION | Reused files do not establish development time.',27:'Creator-reported datamine | distinct model, shared skeleton',32:'SPOILERS | Retail patch 12.1.5',34:'Reported by Holly Longdale | The Game Business, 2026',46:'SPECULATIVE STORY PREDICTION'}
SOURCES={14:'BlizzCon 2026 | announcements',15:'Blizzard v. Turtle WoW | court filings, 2026',16:'Blizzard, Dec 2010 | Midnight estimate not corroborated',24:'Blizzard | Forever editions',25:'Blizzard | current stated policy',34:'The Game Business interview | indirect quotation'}
SOURCES.update({5:'Ruins of Lordaeron | personal beta capture | names obscured',6:'Ruins of Lordaeron | personal beta capture | names obscured'})
SKY=ROOT.parent/'WoWForever/SKYWALL-MEDIAS/01_IMAGES/02_SKYBORNE/Annonce_officielle'
SCENIC={1:2,3:1,4:3,11:4,22:2,23:3,30:4,36:2,37:1,38:3,39:4,40:2,41:3,45:1,47:4,48:2,49:1,50:3}
def card(s):
    n=s['n']; col=GOLD if n<13 else PURPLE if n>=41 else RED if n<36 else TEAL
    im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    # Vignette and editorial panel preserve real client artwork underneath.
    a=np.zeros((H,W,4),dtype=np.uint8); yy=np.arange(H)[:,None]; xx=np.arange(W)[None,:]
    alpha=np.maximum(np.clip((350-yy)/350,0,1)*215,np.clip((yy-1480)/440,0,1)*240)+np.abs(xx-540)/540*60
    a[:,:,3]=np.minimum(alpha,245); im=Image.fromarray(a); d=ImageDraw.Draw(im)
    cinematic=n in SCENIC or n in (5,6)
    d.rounded_rectangle((60,260,1020,680 if cinematic else 1250),radius=30,fill=(6,10,20,175),outline=(255,210,90,85),width=2)
    d.rectangle((95,302,175,308),fill=col)
    center(d,'THE LAZY KODO  /  BETA REVIEW',330,27,GOLD)
    title=s['title'].replace('—',' / ').replace('→','TO').replace('≠','IS NOT')
    if n==1: title='BLIZZARD SOLD IT AS CLASSIC PLUS. IT’S NOT.'
    if n==27: title='SKYBORNE / SHARED SKELETON'
    if n==16: title='TWO ERAS. THREE METRICS.'
    if n==34: title='“I WISH WE HADN’T CALLED IT WARCRAFT. IT SOUNDS INTIMIDATING.”'
    size=78 if len(title)<50 else 62
    y=center(d,title,420,size,col)
    if n in PANELS:
        y=max(y+60,720)
        for value,label in PANELS[n]:
            y=center(d,value,y,60,col); y=center(d,label,y+4,30,CREAM,serif=True)+28
    else:
        extra=s['screen'].split(' — ',1)[-1] if ' — ' in s['screen'] else ''
        if extra and extra!=s['screen'] and not extra.startswith('"'): center(d,extra.strip('"'),max(y+80,820),38,CREAM,serif=True)
        elif n==1:
            center(d,'What I loved. What went wrong.',1040,36,CREAM,serif=True)
            center(d,'Five fears for the future.',1100,36,GOLD,serif=True)
        else:
            center(d,s['part'],1150 if cinematic else 1040,32,col)
    if n in (24,26,28):
        # Genuine Blizzard announcement imagery; no invented side-by-side comparison.
        picture=Image.open(SKY/'Skyborne_Blizzard_13.jpg').convert('RGBA')
        picture.thumbnail((850,400),Image.Resampling.LANCZOS)
        im.alpha_composite(picture,((W-picture.width)//2,770 if n in (26,28) else 1050))
        d=ImageDraw.Draw(im)
    if n in NOTES: center(d,NOTES[n],1175,24,GOLD,width=860,serif=True)
    # Source tags stay separate from narration captions.
    if n in SOURCES: center(d,SOURCES[n],1510,23,GOLD,width=940,serif=True)
    d.text((80,244),f'{n:02} / 50',font=font(24),fill=CREAM)
    center(d,'THE LAZY KODO',1700,30,'#B3AFA4')
    d.rectangle((60,1658,1020,1662),fill='#323440'); d.rectangle((60,1658,60+int(960*n/50),1662),fill=col)
    p=OUT/f'card_{n:02}.png'; im.save(p); return p

ASSHEAD='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Georgia,54,&H0050BEFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,1,2,70,70,475,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
def captions(s):
    lines=[]; groups=[]; group=[]
    for word in s['words']:
        test=' '.join(w['text'] for w in group+[word])
        if len(test)>45 and group: groups.append(group); group=[]
        group.append(word)
    if group: groups.append(group)
    for g in groups:
        start=g[0]['t']+.45; end=g[-1]['t']+g[-1]['d']+.45
        txt=''
        for j,w in enumerate(g):
            duration=(g[j+1]['t']-w['t']) if j+1<len(g) else w['d']
            txt+=r'{\kf'+str(max(1,round(duration*100)))+'}'+w['text']+' '
        lines.append(f'Dialogue: 0,{stamp(start,True)},{stamp(end,True)},Default,,0,0,0,,{txt.strip()}')
        s.setdefault('captions',[]).append((start,end,' '.join(w['text'] for w in g)))
    p=OUT/f'captions_{s["n"]:02}.ass'; p.write_text(ASSHEAD+'\n'.join(lines),encoding='utf-8'); return p

def render(s):
    n=s['n']; target=OUT/f'scene_{n:02}.mp4'
    if target.exists(): return
    overlay=card(s); ass=captions(s); dur=s['duration']
    arts=list((ROOT/'gather/load').glob('tall_*.jpg'))
    preferred=ROOT/'gather/load'/('tall_emeralddream.jpg' if n<13 or n>=36 else 'tall_vault.jpg')
    art=preferred if n%3 else arts[n%len(arts)]
    if n in SCENIC: art=SKY/f'Skyborne_Blizzard_{SCENIC[n]:02}.jpg'
    if n in (24,26,27,28): art=SKY/'Skyborne_Blizzard_06.jpg'
    # Alternate crops every five seconds, with a slow continuous drift.
    vf=f"[0:v]scale=-2:2040,crop=1080:1920:x='(in_w-out_w)*(0.15+0.65*mod(floor(t/5)+{n},3)/2)+20*sin(t/4)':y='60+40*sin(t/6)',eq=brightness=-0.14:saturation=1.05,setsar=1[bg];[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[card];[bg][card]overlay=0:0,ass=filename='{ass.name}',fade=t=out:st={dur-.8 if n==50 else dur-.16}:d={.8 if n==50 else .16}[v]"
    inp=['-loop','1','-framerate',FPS,'-i',art]
    if n in (5,6):
        recording=Path(r'C:\Users\d2460n\Videos\World Of Warcraft\World Of Warcraft 2026.09.21 - 15.05.07.08.mp4')
        inp=['-ss',194 if n==5 else 444,'-i',recording]
        vf='[0:v]scale=-2:1920,crop=1080:1920,boxblur=8:1,eq=gamma=1.5:brightness=0.03:saturation=1.10,setsar=1[bg];'+vf.split('[bg];',1)[1]
    run(inp+['-loop','1','-framerate',FPS,'-i',overlay,'-i',s['audio'],'-filter_complex',vf+';[2:a]adelay=450:all=1,apad,highpass=f=70,acompressor=threshold=0.13:ratio=2.5:attack=8:release=120,alimiter=limit=0.707[a]', '-map','[v]','-map','[a]','-t',dur,'-r',FPS,'-c:v','h264_nvenc','-preset','p4','-cq','20','-b:v','0','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',target])
    print('RENDERED',n,flush=True)

async def main():
    sem=asyncio.Semaphore(3)
    await asyncio.gather(*(speech(s,sem) for s in scenes))
    (OUT/'scenes.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2),encoding='utf-8')
    import os
    os.chdir(OUT)
    for s in scenes: render(s)
    # Ensure caption metadata also exists when restarting completed renders.
    for s in scenes:
        if 'captions' not in s: captions(s)
    t=0; srt=[]; review=['# Final scene timecodes\n']; idx=0
    for s in scenes:
        review.append(f'| {s["n"]:02} | {stamp(t)} | {stamp(t+s["duration"])} | {s["title"]} |')
        for a,b,txt in s['captions']:
            idx+=1; srt.append(f'{idx}\n{stamp(t+a)} --> {stamp(t+b)}\n{txt}\n')
        t+=s['duration']
    (OUT/'captions.srt').write_text('\n'.join(srt),encoding='utf-8')
    (OUT/'scene_timecodes.md').write_text('\n'.join(review),encoding='utf-8')
    (OUT/'concat.txt').write_text('\n'.join(f"file 'scene_{s['n']:02}.mp4'" for s in scenes))
    run(['-f','concat','-safe','0','-i','concat.txt','-c','copy','assembly.mp4'])
    music=ROOT/'spec/music_class/hyjal/1_summit_1.mp3'
    run(['-i','assembly.mp4','-stream_loop','-1','-i',music,'-filter_complex',f'[0:a]asplit=2[voice][key];[1:a]volume=0.10,afade=t=in:d=2,afade=t=out:st={t-4}:d=4[m];[m][key]sidechaincompress=threshold=0.015:ratio=4:attack=30:release=650[duck];[voice][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[out]','-map','0:v','-map','[out]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',t,'-movflags','+faststart','WoW_Forever_Honest_Review_EN.mp4'])
    run(['-ss','3','-i','WoW_Forever_Honest_Review_EN.mp4','-frames:v','1','cover.png'])
    print('COMPLETE',stamp(t),flush=True)
if __name__=='__main__': asyncio.run(main())
