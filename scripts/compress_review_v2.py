"""Compare perceptual quality, then deliver a smaller AVC and a maximum HEVC copy."""
from pathlib import Path
import concurrent.futures,json,subprocess,time

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review_v2';WORK=OUT/'compression_tests';WORK.mkdir(exist_ok=True)
FF=r'C:\Users\d2460n\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
SRC=OUT/'WoW_Forever_Review_V2_EN.mp4'
def run(args):
    r=subprocess.run([FF,'-hide_banner','-loglevel','error','-y']+list(map(str,args)),capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stderr[-4000:])
    return r
def codec(kind,q):
    if kind=='avc':return ['-c:v','libx264','-preset','slow','-crf',str(q),'-threads','10','-pix_fmt','yuv420p']
    return ['-c:v','hevc_nvenc','-preset','p7','-tune','hq','-rc','vbr','-cq',str(q),'-b:v','0','-spatial-aq','1','-aq-strength','8','-rc-lookahead','32','-bf','4','-tag:v','hvc1','-pix_fmt','yuv420p']
ref=WORK/'reference.mkv'
if not ref.exists():
    args=[]
    for t in (18,184,598):args+=['-ss',t,'-t','6','-i',SRC]
    fc=';'.join('[%d:v]setpts=PTS-STARTPTS,fps=30[v%d]'%(i,i) for i in range(3))+';[v0][v1][v2]concat=n=3:v=1:a=0[v]'
    run(args+['-filter_complex',fc,'-map','[v]','-an','-c:v','libx264','-crf','0','-preset','ultrafast','-threads','8',ref])
def test(pair):
    kind,q=pair;dest=WORK/('%s_%d.mp4'%(kind,q));log=WORK/('%s_%d_aligned_vmaf.json'%(kind,q))
    if not dest.exists():run(['-i',ref,'-an']+codec(kind,q)+[dest])
    if not log.exists():
        # VMAF is relative to the delivered master, not a claim about the original game capture.
        filt='[0:v]settb=AVTB,setpts=N/(30*TB)[d];[1:v]settb=AVTB,setpts=N/(30*TB)[r];[d][r]libvmaf=n_threads=4:log_fmt=json:log_path='+log.as_posix().replace(':','\\:')
        filt=filt.replace('log_path=','log_path=\'')+"'"
        run(['-i',dest,'-i',ref,'-lavfi',filt,'-an','-f','null','-'])
    data=json.loads(log.read_text());score=data['pooled_metrics']['vmaf']['mean'];result=dict(codec=kind,q=q,vmaf=score,sample_bytes=dest.stat().st_size)
    print('SAMPLE',json.dumps(result),flush=True);return result
def encode(pair):
    kind,q=pair;name='WoW_Forever_V2_Compact_H264.mp4' if kind=='avc' else 'WoW_Forever_V2_Max_Compression_HEVC.mp4';dest=OUT/name
    run(['-i',SRC,'-map','0:v:0','-map','0:a:0']+codec(kind,q)+['-c:a','copy','-map_metadata','0','-movflags','+faststart',dest])
    run(['-i',dest,'-f','null','-'])
    result=dict(file=name,codec=kind,q=q,bytes=dest.stat().st_size,reduction_percent=round(100*(1-dest.stat().st_size/SRC.stat().st_size),1),full_decode='passed')
    print('ENCODED',json.dumps(result),flush=True);return result
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(2) as ex:results=list(ex.map(test,[('avc',24),('avc',26),('hevc',28),('hevc',31)]))
    selected=[]
    for kind in ('avc','hevc'):
        threshold=94.5 if kind=='hevc' else 95
        options=[r for r in results if r['codec']==kind and r['vmaf']>=threshold]
        if not options:options=[max((r for r in results if r['codec']==kind),key=lambda r:r['vmaf'])]
        best=min(options,key=lambda r:r['sample_bytes']);selected.append((kind,best['q']))
    (WORK/'comparison.json').write_text(json.dumps(results,indent=2))
    with concurrent.futures.ThreadPoolExecutor(2) as ex:delivery=list(ex.map(encode,selected))
    (OUT/'compression_report.json').write_text(json.dumps(dict(original_bytes=SRC.stat().st_size,samples=results,deliverables=delivery),indent=2))
    print('COMPLETE',flush=True)
