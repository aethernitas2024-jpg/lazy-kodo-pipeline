import sys
sys.path.insert(0,r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\spec')
import voice as V
from faster_whisper import WhisperModel
m=WhisperModel("medium.en",device="cpu",compute_type="int8")
for t in sys.argv[1:]:
    w,d=V.line(V.readable(t))
    segs=m.transcribe(w,word_timestamps=True)[0]
    print(repr(t),round(d,2),w)
    for s in segs:
        print('   ',' '.join('%s@%.2f'%(x.word.strip(),x.start) for x in s.words))
