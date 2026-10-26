"""Documentary revision: source-based shot editing, archives and genuine official graphics."""
import asyncio,concurrent.futures,copy,hashlib,json,math,os,re,subprocess,sys,wave
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageEnhance,ImageFilter,ImageOps
import build_forever_review as b

OLD=b.OUT; OUT=b.ROOT/'review_v2'; A=OUT/'assets'; WORK=OUT/'work'
OUT.mkdir(exist_ok=True);WORK.mkdir(exist_ok=True)
b.OUT=OUT
scenes=copy.deepcopy(json.loads((OLD/'scenes.json').read_text(encoding='utf-8')))
scenes=[s for s in scenes if s['n']!=49]
for s in scenes:
    s.pop('captions',None)
    if s['n']==30:
        s['text']=s['text'].replace('Cataclysm had great gameplay ideas.','Some past expansions had great gameplay ideas.')
        s.pop('words',None);s.pop('audio',None)

FILES={
'forever':'forever_gameplay_clean.mp4','horizons':'xXaXYxcbA6A_hls.mp4','vanilla':'vlVSJ0AvZe0_hls.mp4',
'wrath':'BCr7y4SLhck_hls.mp4','bfa':'jSJr3dXZfcg_hls.mp4','midnight':'ijN4EW6meRk_hls.mp4','blizzcon':'CQbdeL9p52Q_hls.mp4'}
CREDITS={
'forever':'BLIZZARD / FOREVER GAMEPLAY TRAILER / 2026',
'horizons':'BLIZZARD / FOREVER: NEW HORIZONS / 2026',
'vanilla':'BLIZZARD / ORIGINAL WOW CINEMATIC / 2004',
'wrath':'BLIZZARD / WRATH CINEMATIC / 2008',
'bfa':'BLIZZARD / BATTLE FOR AZEROTH CINEMATIC / 2017',
'midnight':'BLIZZARD / MIDNIGHT OPENING / 2025 / VIA IGN',
'blizzcon':'BLIZZCON 2026 / ANNOUNCEMENT EXCERPT / VIA ENFANT TERRIBLE'}
URLS={
'forever':'https://www.youtube.com/watch?v=uQuKE0KDgiM',
'horizons':'https://www.youtube.com/watch?v=xXaXYxcbA6A',
'vanilla':'https://www.youtube.com/watch?v=vlVSJ0AvZe0',
'wrath':'https://www.youtube.com/watch?v=BCr7y4SLhck',
'bfa':'https://www.youtube.com/watch?v=jSJr3dXZfcg',
'midnight':'https://www.youtube.com/watch?v=ijN4EW6meRk',
'blizzcon':'https://www.youtube.com/watch?v=CQbdeL9p52Q'}
def V(key,t,style='wide',focus=.5):return dict(kind='video',key=key,t=t,style=style,focus=focus)
def I(i):return dict(kind='official',i=i)
def S(i):return dict(kind='skyborne',i=i)
def H(i):return dict(kind='archive',i=i)
def G(key):return dict(kind=key)

# The sources follow the subject: modern footage is explicitly labelled when discussing retail.
PLAN={
1:[V('forever',18,'fill'),V('forever',72),V('horizons',42,'fill',.22),G('comparison')],
2:[V('forever',57,'fill')],
3:[V('forever',81),I(20),V('forever',88,'fill')],
4:[V('forever',54),V('forever',58,'fill')],
5:[I(9),V('forever',69),I(15)],
6:[V('forever',73),V('forever',77,'fill')],
7:[H(9),V('forever',73),H(2)],
8:[V('forever',107,'fill')],
9:[V('horizons',105),V('forever',104,'fill'),I(22)],
10:[V('forever',8),H(6),V('forever',111,'fill'),I(17)],
11:[I(22),V('forever',104),V('horizons',103,'fill'),I(18)],
12:[I(17),V('forever',108,'fill')],
13:[V('horizons',115,'fill'),V('forever',32,'fill')],
14:[V('blizzcon',8),V('blizzcon',72),G('announcements')],
15:[H(0),H(10),H(1)],
16:[V('midnight',52),G('official_subs'),G('official_subs_zoom'),G('sales'),V('wrath',65,'fill')],
17:[G('datamine'),I(20),V('forever',76),G('datamine')],
18:[V('forever',84),I(20),G('datamine')],
19:[H(5),V('forever',23,'fill'),H(0)],
20:[G('official_revenue'),V('forever',75,'fill')],
21:[V('blizzcon',15),V('horizons',113,'fill'),V('forever',136)],
22:[G('comparison'),V('forever',88),V('forever',121),I(20),V('forever',40),V('forever',129,'fill')],
23:[V('forever',54),H(3),G('comparison'),V('forever',129)],
24:[I(5),G('price'),V('forever',93,'fill'),S(6)],
25:[V('forever',21),I(22),G('policy')],
26:[G('price'),V('forever',91,'fill'),I(5),V('forever',123),I(20)],
27:[I(5),S(6),G('skeleton'),S(7),S(13),G('skeleton')],
28:[S(7),I(5),G('price')],
29:[G('roadmap'),G('roadmap_zoom'),V('forever',77),G('roadmap')],
30:[V('forever',81),V('wrath',66,'fill'),V('forever',87),H(7),V('forever',138,'fill')],
31:[V('bfa',30,'fill'),V('wrath',97)],
32:[V('midnight',44,'fill'),V('midnight',63),V('midnight',83,'fill'),V('midnight',105)],
33:[V('vanilla',48,'fill'),V('vanilla',109),V('bfa',38,'fill'),H(0)],
34:[V('bfa',42,'fill'),G('quote'),V('vanilla',106,'fill')],
35:[V('vanilla',65),V('bfa',20,'fill'),V('wrath',106,'fill'),H(9),V('bfa',134),V('forever',131)],
36:[V('forever',53),G('comparison'),I(0),V('forever',69)],
37:[V('forever',27),H(2),V('forever',57),I(0),V('horizons',55,'fill')],
38:[V('horizons',50,'fill'),V('forever',19),H(1),V('forever',102)],
39:[V('bfa',28),V('bfa',44,'fill'),V('vanilla',102,'fill'),V('bfa',135)],
40:[V('forever',65),V('forever',77,'fill'),G('comparison')],
41:[V('horizons',58),G('scenarios'),V('forever',32,'fill')],
42:[V('forever',8),V('forever',27,'fill'),G('scenarios')],
43:[V('forever',105,'fill'),V('forever',60)],
44:[V('horizons',44,'fill'),V('forever',53),V('horizons',76),G('comparison')],
45:[V('forever',32,'fill'),G('scenarios')],
46:[V('midnight',54,'fill'),V('midnight',91),V('wrath',95,'fill'),V('midnight',117),V('bfa',136,'fill'),V('midnight',35),V('wrath',126)],
47:[V('horizons',70),H(2)],
48:[V('forever',58,'fill'),V('horizons',112)],
50:[V('forever',144),V('forever',52,'fill')]
}

TITLES={1:'I LOVE IT. I’M WORRIED.',3:'MORE DEPTH',4:'THE WORLD FEELS ALIVE',5:'THREE NEW DUNGEONS',7:'DON’T FORGET THE OLD ONES',9:'WELCOME THE NEW PLAYERS',10:'ONE WORLD. TOO MUCH NOISE.',11:'LET THE WORLD TALK',12:'PVP: AN EMPTY QUEUE',13:'MY THEORY',14:'A FUTURE YEARS AWAY',15:'THE CLASSIC PLUS DEMAND',16:'WHEN WOW WAS EVERYWHERE',17:'WHAT THE CLIENT CONTAINS',18:'REUSE IS NOT A TIMELINE',19:'A MARKET TO WIN',20:'WITH THESE RESOURCES?',21:'BEYOND VIDEO GAMES',22:'01 / IDENTITY',23:'SAME SOUL. BETTER TEXTURES.',24:'02 / MONEY',25:'THE PROMISE: RIGHT NOW',26:'MY MONETIZATION FEAR',27:'A NEW RACE. FAMILIAR BONES.',28:'THIRTY DOLLARS',29:'03 / THE PACE',30:'04 / GAMEPLAY',31:'05 / THE TONE',32:'LIADRIN / SPOILERS',33:'WHERE IS THAT OLD SPIRIT?',34:'A NAME THAT INTIMIDATES?',35:'WARCRAFT MUST STAY WARCRAFT',36:'THIS WORLD DESERVES MORE',37:'GIVE IT THE TIME IT NEEDS',38:'A NEW GAME. AN OLD SOUL.',39:'THE WORLD. THE CONFLICT.',40:'BLIZZARD CAN DO BETTER',41:'THREE POSSIBLE FUTURES',42:'01 / THE HYPE FADES',43:'02 / FOREVER TAKES THE LEAD',44:'03 / WORLD OF WARCRAFT 2',45:'TESTING THE WATERS',46:'MY RETAIL PREDICTION',47:'THIRTY YEARS LATER?',48:'BLIZZARD, JUST SAY IT',50:'AM I WRONG?'}

def label(d,txt,y=1515,col=b.GOLD,size=22):b.center(d,txt,y,size,col,width=960,serif=True)
def fitpaste(base,im,box):
    x,y,w,h=box; im=ImageOps.contain(im.convert('RGBA'),(w,h),Image.Resampling.LANCZOS);base.alpha_composite(im,(x+(w-im.width)//2,y+(h-im.height)//2))
def board(shot):
    kind=shot['kind'];name=kind+'_'+str(shot.get('i',''));dest=A/('board_'+name+'.png')
    if dest.exists():return dest
    im=Image.new('RGBA',(1080,1920),'#080D18');d=ImageDraw.Draw(im)
    # Subtle paper/film treatment, never a fake screenshot or a fabricated source document.
    d.rectangle((65,310,70,1270),fill=b.GOLD)
    if kind=='archive':
        src=Image.open(A/('archive_%02d.jpg'%shot['i']));bg=ImageOps.fit(src,(1080,1920)).filter(ImageFilter.GaussianBlur(24));im=ImageEnhance.Brightness(bg).enhance(.3).convert('RGBA');d=ImageDraw.Draw(im)
        label(d,'FROM THE ORIGINAL ERA',320,size=33);fitpaste(im,src,(45,460,990,830));d=ImageDraw.Draw(im)
        label(d,'BLIZZARD PROMOTIONAL ARCHIVE / VIA OUTNOW',1515,size=21)
    elif kind in ('official','skyborne'):
        src=Image.open(A/('official_%02d.png'%shot['i']) if kind=='official' else b.SKY/('Skyborne_Blizzard_%02d.jpg'%shot['i']));bg=ImageOps.fit(src,(1080,1920)).filter(ImageFilter.GaussianBlur(24));im=ImageEnhance.Brightness(bg).enhance(.36).convert('RGBA')
        fitpaste(im,src,(0,430,1080,840));d=ImageDraw.Draw(im);label(d,'BLIZZARD / FOREVER PANEL RECAP / SEPTEMBER 2026' if kind=='official' else 'BLIZZARD / SKYBORNE ANNOUNCEMENT / 2026',1515,size=20)
    elif kind=='comparison':
        label(d,'THE SAME WORLD. TWO ERAS.',310,size=36)
        fitpaste(im,Image.open(A/'archive_06.jpg'),(35,440,1010,435));fitpaste(im,Image.open(A/'official_04.png'),(35,920,1010,435));d=ImageDraw.Draw(im)
        label(d,'ORIGINAL ERA / PROMOTIONAL ARCHIVE',405,size=24);label(d,'FOREVER / BLIZZARD / 2026',885,size=24)
        label(d,'ARCHIVE: OUTNOW / FOREVER: BLIZZARD',1530,size=21)
    elif kind in ('official_subs','official_subs_zoom','official_revenue'):
        revenue=kind=='official_revenue';src=Image.open(A/('official_digital_revenue_2010.png' if revenue else 'official_graph_full.png'))
        crop=(380,790,1190,1740) if revenue else (230,780,1190,1735)
        if kind=='official_subs':crop=(200,510,1170,1740)
        fitpaste(im,src.crop(crop),(70,350,940,1000));d=ImageDraw.Draw(im)
        label(d,'ORIGINAL PUBLISHED GRAPHIC / 2010',280,size=30)
        label(d,'ACTIVISION BLIZZARD / 2010 ANNUAL REPORT / P. '+('1' if revenue else '3'),1515,size=21)
        label(d,'Historical group digital revenue. Not a Forever budget.' if revenue else 'Historical subscribers. Not concurrent players.',1570,size=21,col=b.CREAM)
    elif kind in ('roadmap','roadmap_zoom'):
        src=Image.open(A/'official_28.png')
        if kind=='roadmap_zoom':src=src.crop((src.width//3,0,src.width,src.height))
        label(d,'THE ACTUAL BLIZZARD ROADMAP',320,size=34);fitpaste(im,src,(35,490,1010,800));d=ImageDraw.Draw(im)
        label(d,'BLIZZARD / WHAT’S NEXT PANEL / SEPTEMBER 12, 2026',1515,size=21)
    elif kind=='announcements':
        label(d,'THE ANNOUNCED HORIZON',350,size=36)
        for i,(year,game) in enumerate([('2027','THE LAST TITAN'),('2029','DIABLO V'),('2030','STARCRAFT')]):
            b.center(d,year,560+i*235,83,b.GOLD);label(d,game,670+i*235,size=34,col=b.CREAM)
        label(d,'BLIZZCON 2026 / EDITORIAL TIMELINE',1515,size=22)
    elif kind=='datamine':
        label(d,'SEASON OF DISCOVERY LEFTOVERS',380,size=33)
        for i,(n,txt) in enumerate([(271,'Rune engraving spells'),(104,'Waylaid Supplies items'),(72,'Nightmare Incursion items')]):
            y=600+i*205;d.rounded_rectangle((90,y+80,990,y+120),radius=12,fill='#1B2535');d.rounded_rectangle((90,y+80,90+round(900*n/271),y+120),radius=12,fill=b.PURPLE)
            d.text((90,y),txt,font=b.font(34,True),fill=b.CREAM);d.text((990,y),str(n),font=b.font(48),fill=b.GOLD,anchor='rt')
        label(d,'CREATOR DATAMINE / EDITORIAL GRAPHIC',1515,size=23);label(d,'Build 1.60.1.70374 / not an official Blizzard chart',1570,size=20,col=b.CREAM)
    elif kind=='skeleton':
        label(d,'THE MODEL AND THE SKELETON',360,size=34)
        for i,(head,txt) in enumerate([('DISTINCT MODEL FILE','Skyborne'),('SHARED SKELETON','Blood elf / 4690403 + 4690402'),('BLOOD ELF FALLBACKS','Armor / textures / helmets')]):
            y=560+i*220;d.rounded_rectangle((80,y-20,1000,y+150),24,fill='#142033',outline='#354453');label(d,head,y,col=b.GOLD,size=32);label(d,txt,y+73,col=b.CREAM,size=28)
        label(d,'CREATOR-REPORTED CLIENT FINDINGS',1515,size=23)
    elif kind=='price':
        label(d,'SKYBORNE HEROIC PACK',500,size=42);b.center(d,'$29.99',760,148,b.GOLD);label(d,'PLUS AN ACTIVE SUBSCRIPTION',1010,size=34,col=b.CREAM);label(d,'BLIZZARD / US STORE PRICE / 2026',1515,size=23)
    elif kind=='sales':
        label(d,'CATACLYSM / DECEMBER 2010',480,size=40);b.center(d,'3.3 MILLION',740,92,b.GOLD);label(d,'COPIES SOLD IN THE FIRST 24 HOURS',930,size=30,col=b.CREAM);label(d,'BLIZZARD / DECEMBER 13, 2010 / SALES, NOT CONCURRENCY',1515,size=20)
    elif kind=='policy':
        for i,t in enumerate(['NO BATTLE PASS','NO TOKEN','NO PAID BOOSTS']):b.center(d,t,570+i*180,66,b.TEAL)
        label(d,'CURRENT STATED POLICY / NOT A PERMANENT GUARANTEE',1515,size=21)
    elif kind=='quote':
        b.center(d,'“I WISH WE HADN’T CALLED IT WARCRAFT. IT SOUNDS INTIMIDATING.”',490,65,b.CREAM,width=890)
        label(d,'RELAYED BY HOLLY LONGDALE',1070,size=31);label(d,'THE GAME BUSINESS / FEBRUARY 2026',1150,size=25)
    elif kind=='scenarios':
        for i,t in enumerate(['01 / LAUNCH HYPE FADES','02 / FOREVER TAKES THE LEAD','03 / A NEW WORLD OF WARCRAFT']):b.center(d,t,510+i*240,55,[b.GOLD,b.PURPLE,b.TEAL][i])
        label(d,'POSSIBLE FUTURES / MY OPINION',1515,size=24)
    else:raise ValueError(kind)
    im.convert('RGB').save(dest);return dest

def duration_file(p):
    r=subprocess.run([b.FF,'-hide_banner','-i',str(p)],capture_output=True,text=True);m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r.stderr)
    return int(m[1])*3600+int(m[2])*60+float(m[3])

def render_shot(shot,dur,name):
    cache_spec=dict(shot)
    if shot['kind']=='video':cache_spec.update(render_revision=3,duration=dur)
    retain_wide=shot['kind']=='video' and shot['key']=='forever' and 36<=shot['t']<=70 and shot['style']=='fill'
    if retain_wide:cache_spec['effective_style']='wide'
    name+='_'+hashlib.sha1(json.dumps(cache_spec,sort_keys=True).encode()).hexdigest()[:8]
    target=WORK/(name+'.mp4')
    if target.exists():return target
    if shot['kind']=='video':
        src=A/FILES[shot['key']];t=shot['t'];style='wide' if retain_wide else shot['style']
        # Clean official footage stays sharp. No blanket blur is applied to the subject.
        if style=='fill':
            filt="crop=iw:trunc(ih*0.80/2)*2,scale=-2:1920,crop=1080:1920:x='(iw-ow)*%.3f',setsar=1,eq=contrast=1.04:saturation=1.05"%shot.get('focus',.5)
            inputs=['-ss',t,'-i',src];fc=False
        else:
            # The wide insert preserves the action and silhouettes lost by a narrow vertical crop.
            poster=WORK/(name+'_bg.png')
            if not poster.exists():
                temp=WORK/(name+'_still.png');b.run(['-ss',t+.2,'-i',src,'-frames:v','1',temp]);im=Image.open(temp).convert('RGB');im=ImageOps.fit(im,(1080,1920)).filter(ImageFilter.GaussianBlur(24));ImageEnhance.Brightness(im).enhance(.36).save(poster)
            inputs=['-ss',t,'-i',src,'-loop','1','-framerate','30','-i',poster]
            filt='[0:v]crop=iw:trunc(ih*0.80/2)*2,scale=1350:-2,crop=1080:trunc(ih/2)*2,setsar=1[sharp];[1:v][sharp]overlay=0:520:shortest=1[v]';fc=True
        if fc:filt=filt.replace('shortest=1[v]','shortest=1,setpts=PTS-STARTPTS,fps=30,tpad=stop_mode=clone:stop_duration=5[v]')
        else:filt+=',setpts=PTS-STARTPTS,fps=30,tpad=stop_mode=clone:stop_duration=5'
        credit=CREDITS[shot['key']]
    else:
        src=board(shot);inputs=['-loop','1','-framerate','30','-i',src];fc=False
        # A small camera movement, rather than large jumps between crops.
        filt="scale=1120:1992,crop=1080:1920:x='20+12*sin(t/3)':y='36+18*cos(t/4)',setsar=1"
        credit=None
    args=inputs+(['-filter_complex',filt,'-map','[v]'] if fc else ['-vf',filt])
    b.run(args+['-t',dur,'-an','-r','30','-c:v','h264_nvenc','-preset','p4','-cq','19','-b:v','0','-pix_fmt','yuv420p','-color_range','tv',target])
    return target

HEAD=b.ASSHEAD.replace('Style: Default,Georgia,54','Style: Default,Georgia,50').replace('475,1','450,1')
EXTRA='Style: Title,Cinzel,68,&H00DAE8EC,&H00DAE8EC,&H00201008,&H00000000,0,0,0,0,100,100,0,0,1,2,1,8,65,65,285,1\nStyle: Credit,Arial,22,&H00DAE8EC,&H00DAE8EC,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,1,2,65,65,370,1\nStyle: Brand,Cinzel,25,&H008AADA8,&H008AADA8,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,1,2,65,65,185,1\n'

def render_scene(s):
    n=s['n'];dest=OUT/('scene_%02d.mp4'%n)
    if dest.exists():return
    shotdir=WORK;plan=PLAN[n];count=max(len(plan),math.ceil(s['duration']/4.7));frame_total=round(s['duration']*30)
    frames=[frame_total//count+(i<frame_total%count) for i in range(count)]
    clips=[];cuts=[];elapsed=0
    for i,fr in enumerate(frames):
        shot=copy.deepcopy(plan[i%len(plan)])
        if shot['kind']=='video' and i>=len(plan):shot['t']+=1.2*(i//len(plan))
        dur=fr/30;name='s%02d_%02d'%(n,i)
        clips.append(render_shot(shot,dur,name));cuts.append(dict(start=elapsed,duration=dur,**shot));elapsed+=dur
    concat=WORK/('list_%02d.txt'%n);concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in clips))
    base=WORK/('base_%02d.mp4'%n);b.run(['-f','concat','-safe','0','-i',concat,'-c','copy',base])
    # Local caption file has the new scene's exact word timings; titles are brief overlays.
    ass=b.captions(s);raw=ass.read_text(encoding='utf-8');raw=raw.replace(b.ASSHEAD,HEAD).replace('[Events]',EXTRA+'[Events]')
    title=TITLES.get(n,s['title']);size=58 if len(title)>28 else 68;title_lines=b.wrap(title,b.font(size),940);title=r'\N'.join(title_lines)
    # Documents already have their own headings; avoid stacking a second headline on them.
    if plan[0]['kind'] not in ('archive','comparison','roadmap','official_revenue'):
        raw+=f'\nDialogue: 1,0:00:00.00,{b.stamp(min(s["duration"],3.7),True)},Title,,0,0,0,,{{\\fs{size}\\fad(150,400)}}{title}'
    raw+=f'\nDialogue: 1,0:00:00.00,{b.stamp(s["duration"],True)},Brand,,0,0,0,,THE LAZY KODO'
    for cut in cuts:
        if cut['kind']=='video':
            txt=CREDITS[cut['key']]
            if n==32:txt+=' / INTRO ARCHIVE, NOT THE 12.1.5 DEATH SCENE'
            raw+=f'\nDialogue: 0,{b.stamp(cut["start"],True)},{b.stamp(cut["start"]+cut["duration"],True)},Credit,,0,0,0,,{txt}'
    if n==16:
        raw+='\nDialogue: 2,0:00:00.00,0:00:07.00,Title,,0,0,0,,{\\fs25\\pos(540,405)}MIDNIGHT 500K ESTIMATE: UNCORROBORATED\\NDO NOT COMPARE DIFFERENT METRICS'
    if n==46:raw+=f'\nDialogue: 2,0:00:00.00,{b.stamp(s["duration"],True)},Title,,0,0,0,,{{\\fs25\\pos(540,410)}}SPECULATIVE STORY PREDICTION'
    ass.write_text(raw,encoding='utf-8')
    vf="ass=filename='"+ass.as_posix().replace(':','\\:')+"':fontsdir='"+b.FONT.parent.as_posix().replace(':','\\:')+"'"
    if n==50:vf+=',fade=t=out:st=%.3f:d=0.8'%(s['duration']-.8)
    b.run(['-i',base,'-i',s['audio'],'-filter_complex','[0:v]'+vf+'[v];[1:a]adelay=450:all=1,apad,highpass=f=70,acompressor=threshold=0.13:ratio=2.5:attack=8:release=120,alimiter=limit=0.707[a]','-map','[v]','-map','[a]','-t',s['duration'],'-c:v','h264_nvenc','-preset','p4','-cq','19','-b:v','0','-pix_fmt','yuv420p','-color_range','tv','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',dest])
    (OUT/('cuts_%02d.json'%n)).write_text(json.dumps(cuts,indent=2),encoding='utf-8');print('SCENE',n,'CUTS',len(cuts),flush=True)

async def main():
    await b.speech(next(s for s in scenes if s['n']==30),asyncio.Semaphore(1))
    (OUT/'scenes.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'narration_v2.md').write_text('# Revised narration\n\n'+'\n\n'.join('## Scene %02d\n\n%s'%(s['n'],s['text']) for s in scenes),encoding='utf-8')
    for plan in PLAN.values():
        for shot in plan:
            if shot['kind']!='video':board(shot)
    workers=int(os.environ.get('REVIEW_WORKERS','2'))
    with concurrent.futures.ThreadPoolExecutor(workers) as pool:
        for f in [pool.submit(render_scene,s) for s in scenes]:f.result()
    import cv2
    for s in scenes:
        cap=cv2.VideoCapture(str(OUT/('scene_%02d.mp4'%s['n'])))
        frames=cap.get(cv2.CAP_PROP_FRAME_COUNT);fps=cap.get(cv2.CAP_PROP_FPS);cap.release()
        if not fps or abs(frames/fps-s['duration'])>.08:raise RuntimeError('Video duration mismatch for scene %d: %s frames at %s fps; expected %s seconds'%(s['n'],frames,fps,s['duration']))
    elapsed=0;srt=[];idx=0;review=['# V2 scene timecodes\n','| Scene | Start | End | Title |','|---|---|---|---|'];allcuts=[]
    for s in scenes:
        s.pop('captions',None);b.captions(s)
        review.append('| %02d | %s | %s | %s |'%(s['n'],b.stamp(elapsed),b.stamp(elapsed+s['duration']),TITLES.get(s['n'],s['title'])))
        for a,z,txt in s['captions']:
            idx+=1;srt.append(f'{idx}\n{b.stamp(elapsed+a)} --> {b.stamp(elapsed+z)}\n{txt}\n')
        cuts=json.loads((OUT/('cuts_%02d.json'%s['n'])).read_text())
        for cut in cuts:cut['global_start']=elapsed+cut['start'];cut['scene']=s['n'];allcuts.append(cut)
        elapsed+=s['duration']
    (OUT/'captions.srt').write_text('\n'.join(srt),encoding='utf-8');(OUT/'scene_timecodes.md').write_text('\n'.join(review),encoding='utf-8');(OUT/'shot_manifest.json').write_text(json.dumps(allcuts,indent=2),encoding='utf-8')
    (OUT/'concat.txt').write_text('\n'.join("file 'scene_%02d.mp4'"%s['n'] for s in scenes))
    b.run(['-f','concat','-safe','0','-i',OUT/'concat.txt','-c','copy',OUT/'assembly.mp4'])
    # Rebuild the proven chapter score on the revised timeline, without the guild scene.
    import finish_forever_review as finish
    finish.b.OUT=OUT
    # Its score layout uses positions of 50 original scenes; build against the 49 kept scenes.
    score_v1=json.loads((OLD/'scenes.json').read_text(encoding='utf-8'))
    with wave.open(str(OLD/'chapter_score.wav')) as w:sr=w.getframerate();music=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)
    starts=np.cumsum([0]+[s['duration'] for s in score_v1]);chunks=[]
    for s in scenes:
        i=s['n']-1;a=round(starts[i]*sr);z=round(starts[i+1]*sr);chunk=music[a:z];need=round(s['duration']*sr)
        if len(chunk)<need:chunk=np.tile(chunk,(math.ceil(need/len(chunk)),1))
        chunks.append(chunk[:need])
    combined=np.concatenate(chunks)
    with wave.open(str(OUT/'chapter_score.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(combined.tobytes())
    b.run(['-i',OUT/'assembly.mp4','-i',OUT/'chapter_score.wav','-filter_complex','[0:a]asplit=2[voice][key];[1:a][key]sidechaincompress=threshold=0.015:ratio=4:attack=30:release=650[duck];[voice][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[out]','-map','0:v','-map','[out]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',OUT/'WoW_Forever_Review_V2_EN.mp4'])
    print('COMPLETE',b.stamp(elapsed),len(allcuts),'shots',flush=True)

if __name__=='__main__':asyncio.run(main())
