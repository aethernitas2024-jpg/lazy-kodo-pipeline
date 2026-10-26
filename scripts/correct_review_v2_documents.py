"""Targeted visual fixes after reviewing the rendered documents."""
import json,sys,time
import build_forever_review_v2 as v
for kind in ('official_subs_zoom','official_revenue'):
    p=v.A/('board_'+kind+'_.png')
    if p.exists():p.rename(p.with_name(p.stem+'_before_QA.png'))
    v.board(v.G(kind))
v.board(v.G('announcements'))
for n,indices in [(14,[2]),(16,[2]),(20,[0])]:
    p=v.OUT/('scene_%02d.mp4'%n)
    if p.exists():p.rename(p.with_name(p.stem+'_before_QA.mp4'))
    for i in indices:
        for p in v.WORK.glob('s%02d_%02d_*.mp4'%(n,i)):
            p.rename(p.with_name(p.stem+'_before_QA.mp4'))
    v.render_scene(next(s for s in v.scenes if s['n']==n))
