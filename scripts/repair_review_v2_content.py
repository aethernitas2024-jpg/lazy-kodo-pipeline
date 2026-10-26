import asyncio
import build_forever_review_v2 as v
for n in (7,15,19,20,22,24,27,28,29):
    p=v.OUT/('scene_%02d.mp4'%n)
    if p.exists():p.rename(p.with_name(p.stem+'_before_content_QA.mp4'))
asyncio.run(v.main())
