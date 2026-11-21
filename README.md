# The World in One Day — Saturday, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Iyannn11/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Iyannn11/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A front page that sums up the world's news of **Saturday, 21 November 2026**
in one image: Wall Street slides into correction as the AI trade unwinds,
three Houthi missiles at Riyadh are intercepted, COP31 runs into overtime
in Antalya, a 6.8 quake shakes Peru, and more — 12 stories across regions
and fields, each drawn as its own pictogram.

`render.py` (Pillow) draws `entry.png` deterministically, 1024x1024.
`main.ts` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`).
`SOURCES.md` lists every story with its source and date; stories from
other days were deliberately excluded.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
