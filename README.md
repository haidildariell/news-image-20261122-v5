# news-image-20261122-v5

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/haidildariell/news-image-20261122-v5/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/haidildariell/news-image-20261122-v5/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

The Sunday Globe: one page that sums up Sunday 22 November 2026 — 36 stories across 7 regions, 15 of them illustrated. The lead story is the collapse of COP31 in Antalya: the EU, Britain and Panama rejected a final text that never mentioned fossil fuels, so the longest climate summit on record ended with no pact at all. The draft's 35% clean-power goal and its $120bn adaptation target are shown as draft figures that were never adopted. Kyiv endures a night of 186 Russian drones (161 downed), India declares at 720 for 9 in Wellington, and Hong Kong picks its 723 Election Committee members on a record 98.79% turnout. A world map with numbered pins, a UTC timeline, a stat strip and a date-check box (what is NOT Sunday's news) complete the page.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render.py` draws `entry.png` (1024x1024, deterministic) with Pillow at build time; `main.py` (standard library only) copies it to the output path, so both grading runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=haidildariell&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
