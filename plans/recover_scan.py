"""List every Write/Edit/Read touching the given basenames across transcripts, chronologically."""
import json, sys, os, glob
names = sys.argv[1].split(',')
out = []
for p in glob.glob(r'C:\Users\d2460n\.claude\projects\C--Users-d2460n\*.jsonl'):
    reads = {}
    with open(p, encoding='utf-8', errors='ignore') as f:
        for ln in f:
            if not any(n in ln for n in names): continue
            try: d = json.loads(ln)
            except Exception: continue
            ts = d.get('timestamp', '')
            msg = d.get('message') or {}
            c = msg.get('content')
            if not isinstance(c, list): continue
            for b in c:
                if b.get('type') == 'tool_use' and b.get('name') in ('Write', 'Edit', 'Read', 'MultiEdit'):
                    fp = b['input'].get('file_path', '')
                    if os.path.basename(fp) in names:
                        out.append((ts, os.path.basename(p)[:8], b['name'], fp, len(json.dumps(b['input']))))
for o in sorted(out): print(*o)
