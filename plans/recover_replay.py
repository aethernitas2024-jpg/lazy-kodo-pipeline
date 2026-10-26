"""Rebuild files from transcripts: replay successful Write/Edit tool calls in time order.

    py recover_replay.py <outdir> name1.py,name2.py
Also keeps the last Read result (line-numbered) per file to cross-check.
"""
import json, sys, os, glob, re
outdir, names = sys.argv[1], sys.argv[2].split(',')
PATHF = sys.argv[3] if len(sys.argv) > 3 else ''
ev, errs, reads = {}, set(), {}
uses = {}
for p in glob.glob(r'C:\Users\d2460n\.claude\projects\C--Users-d2460n\**\*.jsonl', recursive=True):
    with open(p, encoding='utf-8', errors='ignore') as f:
        for ln in f:
            if not any(n in ln for n in names) and 'tool_result' not in ln: continue
            try: d = json.loads(ln)
            except Exception: continue
            c = (d.get('message') or {}).get('content')
            if not isinstance(c, list): continue
            for b in c:
                if b.get('type') == 'tool_use' and b.get('name') in ('Write', 'Edit', 'Read'):
                    fp = b['input'].get('file_path', '')
                    bn = os.path.basename(fp)
                    if bn in names and PATHF in fp:
                        uses[b['id']] = (d.get('timestamp', ''), bn, b['name'], b['input'])
                elif b.get('type') == 'tool_result' and b.get('tool_use_id') in uses or b.get('type') == 'tool_result':
                    tid = b.get('tool_use_id')
                    if b.get('is_error'): errs.add(tid)
                    cc = b.get('content')
                    txt = cc if isinstance(cc, str) else ''.join(x.get('text', '') for x in (cc or []) if isinstance(x, dict))
                    if 'has been updated' not in txt and 'File created' not in txt and 'successfully' not in txt:
                        reads[tid] = txt
seen = set(); files = {}
for tid, (ts, bn, kind, inp) in sorted(uses.items(), key=lambda kv: kv[1][0]):
    key = (ts, bn, kind, json.dumps(inp, sort_keys=True))
    if key in seen: continue
    seen.add(key)
    if tid in errs: print('skip-error', ts, bn, kind); continue
    if kind == 'Write': files[bn] = inp['content']; print('write', ts, bn, len(inp['content']))
    elif kind == 'Edit':
        s = files.get(bn)
        if s is None: print('EDIT-NO-BASE', ts, bn); continue
        o, n = inp['old_string'], inp['new_string']
        if o not in s: print('EDIT-MISS', ts, bn, repr(o[:60])); continue
        files[bn] = s.replace(o, n) if inp.get('replace_all') else s.replace(o, n, 1)
    elif kind == 'Read' and tid in reads and not inp.get('offset') and not inp.get('limit'):
        lines = [re.sub(r'^\s*\d+\t', '', l, count=1) for l in reads[tid].split('\n') if re.match(r'^\s*\d+\t', l)]
        if lines:
            rd = '\n'.join(lines)
            cur = files.get(bn, '')
            same = rd.strip() == cur.strip()
            print('read', ts, bn, 'MATCH' if same else 'DIFF -> adopting read', len(rd))
            if not same: files[bn] = rd + '\n'
os.makedirs(outdir, exist_ok=True)
for bn, s in files.items():
    open(os.path.join(outdir, bn), 'w', encoding='utf-8', newline='\n').write(s); print('saved', bn, len(s))
