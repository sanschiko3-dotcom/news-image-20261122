# The World Today — 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/rank/news-image-20261122)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/reward/news-image-20261122)](https://make.fun/bounty/news-image-20261122)

One image that sums up 22 November's world news: a newspaper front page,
"THE WORLD TODAY". Iran strikes US defences as the Gulf braces, plus
Kryvyi Rih, the FBI database breach, Nvidia, the ATP final, and the
Norway oil ruling — six stories that shaped the day, in one page.

Competition: https://make.fun/bounty/news-image-20261122

## Run

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render.py` draws `assets/entry.png` (1024×1024) with Pillow.
`main.py` verifies the PNG (signature, size, IHDR dimensions) and copies
it byte-for-byte to `$MAKEFUN_OUTPUT_DIR` (default `/output`) as
`entry.png`, then re-reads and compares the written file.
