# news-image-20261118

[![make.fun](https://make.fun/bounty/news-image-20261118/badge.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/bounty/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/bounty/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

Entry for the make.fun competition
[news-image-20261118](https://make.fun/bounty/news-image-20261118):
sum up the world news of Wednesday 18 November 2026 in one image.

`main.py` (Python 3.13, standard library only) draws a 1024x1024
newspaper front page — masthead, dateline, and six stories — and writes it
to `$MAKEFUN_OUTPUT_DIR/entry.png`. It uses an embedded 5x7 bitmap font
and a hand-rolled PNG encoder, so it runs with nothing installed. The
program is deterministic: two runs write byte-identical files.

## The six stories (all 18 November 2026)

1. **APEC opens in Shenzhen** — leaders of 21 Pacific economies open
   their summit; Trump and Xi talk trade, tariffs and AI, with a
   three-way meeting with Putin planned for Thursday.
   *(Reuters, AP, Xinhua)*
2. **Tanker hit in the Strait of Hormuz** — a tanker is struck leaving
   the strait and its crew evacuated; Iran claims a supertanker carrying
   two million barrels of oil has sunk. *(UKMTO, Reuters)*
3. **UK sanctions Israeli settlement firms** — Britain freezes the
   assets of eight construction firms building West Bank settlements.
   *(Reuters, BBC)*
4. **Taiwan seeks $14bn in US arms** — Taipei says it urgently needs
   the weapons as tensions with Beijing grow. *(Reuters)*
5. **Cyclone Akvan bears down** — a cyclonic storm strengthens over
   the Bay of Bengal, likely to turn severe by Thursday. *(IMD)*
6. **Trump rubbishes dirty-bomb plot** — Trump dismisses US
   intelligence reports that Iran is weighing a dirty-bomb attack in
   Washington. *(CNN)*

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
