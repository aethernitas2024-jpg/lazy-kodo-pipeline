import sys
sys.path.insert(0,r'C:\Users\d2460n\Documents\aout\tiktok-pipeline\spec')
import voice as V
from faster_whisper import WhisperModel
m=WhisperModel("small.en",device="cpu",compute_type="int8")
for t in sys.argv[1:]:
    w,d=V.line(V.readable(t))
    print(repr(t),'->',' '.join(s.text for s in m.transcribe(w)[0]))
