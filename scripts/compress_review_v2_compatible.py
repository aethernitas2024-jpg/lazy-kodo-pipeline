import json
import compress_review_v2 as c
def opts(q):return ['-c:v','h264_nvenc','-preset','p7','-tune','hq','-rc','vbr','-cq',str(q),'-b:v','0','-spatial-aq','1','-aq-strength','8','-rc-lookahead','32','-bf','3','-pix_fmt','yuv420p']
scores=[]
for q in (24,26):
    p=c.WORK/('gpu_avc_%d.mp4'%q);log=c.WORK/('gpu_avc_%d.json'%q)
    c.run(['-i',c.WORK/'reference.mkv','-an']+opts(q)+[p])
    filt='[0:v]settb=AVTB,setpts=N/(30*TB)[d];[1:v]settb=AVTB,setpts=N/(30*TB)[r];[d][r]libvmaf=n_threads=4:log_fmt=json:log_path=\''+log.as_posix().replace(':','\\:')+"'"
    c.run(['-i',p,'-i',c.WORK/'reference.mkv','-lavfi',filt,'-an','-f','null','-'])
    score=json.loads(log.read_text())['pooled_metrics']['vmaf']['mean'];scores.append(dict(q=q,vmaf=score,bytes=p.stat().st_size));print('GPU AVC SAMPLE',scores[-1],flush=True)
passed=[s for s in scores if s['vmaf']>=95];chosen=min(passed,key=lambda s:s['bytes']) if passed else max(scores,key=lambda s:s['vmaf'])
dest=c.OUT/'WoW_Forever_V2_Compact_H264.mp4'
c.run(['-i',c.SRC,'-map','0:v:0','-map','0:a:0']+opts(chosen['q'])+['-c:a','copy','-map_metadata','0','-movflags','+faststart','-progress',c.WORK/'avc_progress.txt',dest])
c.run(['-i',dest,'-f','null','-'])
(c.WORK/'gpu_avc_result.json').write_text(json.dumps(dict(samples=scores,chosen=chosen,bytes=dest.stat().st_size,decode='passed'),indent=2))
print('AVC COMPLETE',dest.stat().st_size,flush=True)
