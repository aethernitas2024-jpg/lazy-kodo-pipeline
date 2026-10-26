import asyncio,time
import build_forever_review_v2 as v
for n in (1,2,4,48,50):
    p=v.OUT/('scene_%02d.mp4'%n)
    if p.exists():p.rename(p.with_name(p.stem+'_before_framing_QA.mp4'))
asyncio.run(v.main())
