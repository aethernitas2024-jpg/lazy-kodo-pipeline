import compress_review_v2 as c
target=c.WORK/'max_HEVC31_validated.mp4'
c.run(['-i',c.SRC,'-map','0:v:0','-map','0:a:0']+c.codec('hevc',31)+['-c:a','copy','-map_metadata','0','-movflags','+faststart','-progress',c.WORK/'hevc31_progress.txt',target])
c.run(['-i',target,'-f','null','-'])
print('HEVC31 COMPLETE',target.stat().st_size,flush=True)
