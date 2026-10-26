import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
t = open('wk_viewer_tpl.html', encoding='utf-8').read()
t = t.replace("<title>Wild King's Helm</title>", '<title>Forever Raid Staves</title>')
t = t.replace("<h1>The Wild King's Helm</h1>", '<h1>New Staves in the Beta Files</h1>')
t = re.sub(r'<p class="sub">.*?</p>', '<p class="sub">Three staff models added for WoW Forever, extracted from the beta client: the Hyjal Summit raid, the Barrow Deeps raid and the Skyborne set. Each ships with four color variants. Drag to rotate, scroll or pinch to zoom.</p>', t, flags=re.S)
t = re.sub(r'<div class="races" role="group".*?</div>\n', '''<div class="races" role="group" aria-label="Staff">
        <button id="m-hyjal" data-k="hyjal" aria-pressed="true">Hyjal Summit</button>
        <button id="m-barrow" data-k="barrow" aria-pressed="false">Barrow Deeps</button>
        <button id="m-skyborne" data-k="skyborne" aria-pressed="false">Skyborne</button>
      </div>
      <div class="races" role="group" aria-label="Color variant" id="vars"></div>
      <div class="races"><button id="spin" class="tog" aria-pressed="true">Auto-rotate</button></div>
''', t, count=1, flags=re.S)
t = re.sub(r'<div class="tip">.*?</div>\n      </div>', '''<div class="tip">
        <div class="n" id="t-name">Hyjal Summit staff</div>
        <div class="w">Two-Hand · Staff</div>
        <div class="y" id="t-src">Raid: Hyjal Summit (final boss: the Wild King)</div>
        <div class="g" id="t-file">staff_2h_raidhyjalc60_d_01</div>
      </div>''', t, count=1, flags=re.S)
t = re.sub(r'<dl class="ledger">.*?</dl>', '''<dl class="ledger">
        <div><dt>Model</dt><dd id="m-file">-</dd></div>
        <div><dt>FileDataID</dt><dd id="m-fdid">-</dd></div>
        <div><dt>Mesh</dt><dd id="m-mesh">-</dd></div>
        <div><dt>Texture</dt><dd id="m-tex">-</dd></div>
        <div><dt>"c60"</dt><dd>art tag used for WoW Forever assets</dd></div>
      </dl>''', t, count=1, flags=re.S)
t = t.replace('Item name and stats are still encrypted; only the model and icon are readable.',
              'Item names, stats and which boss drops each staff are not readable yet; only the models and textures are.')
t = t.replace('aria-label="3D model of the Wild King helm"', 'aria-label="3D model of the selected staff"')
t = t.replace('.stage { position: relative; aspect-ratio: 4 / 3;', '.stage { position: relative; aspect-ratio: 3 / 4; max-height: 78vh; margin-inline: auto; width: 100%;')
s0 = t.index('<script>\nconst TEX')
s1 = t.index('</script>', s0) + len('</script>')
js = open('staves_js.txt', encoding='utf-8').read()
M = {k: json.load(open('st_%s.json' % k)) for k in ('hyjal', 'barrow', 'skyborne')}
t = t[:s0] + js.replace('__MODELS__', json.dumps(M, separators=(',', ':'))) + t[s1:]
open('forever-staves.html', 'w', encoding='utf-8').write(t)
print(len(t), t.count('__MODELS__'), t.count('races" role="group"'))
