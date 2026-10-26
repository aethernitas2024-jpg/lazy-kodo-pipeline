import sys
from faster_whisper import WhisperModel
m=WhisperModel("small.en",device="cpu",compute_type="int8")
segs,info=m.transcribe(sys.argv[1],vad_filter=True)
with open("endgame_transcript.txt","w",encoding="utf-8") as f:
    for s in segs:
        f.write("[%d:%02d] %s\n"%(s.start//60,s.start%60,s.text.strip()))
print("dur",info.duration)
