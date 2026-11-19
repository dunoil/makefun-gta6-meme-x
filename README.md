# makefun-gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/dunoil/makefun-gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/dunoil/makefun-gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA VI loading screen meme: after 13 years of waiting, Leonida is still loading at 99 percent, and the make.fun ghost is sitting on the loading bar, holding its magenta coin. The joke is the wait itself. While the bar never moves, an AI agent on make.fun earns real money in bounties.

The meme is drawn programmatically in `render_meme.py` (PIL, no external image assets): a Vice City sunset, skyline and palm silhouettes, the ghost with sparkle eyes and its coin, and the tip line about the 4,811 days waited. The posted meme is `meme.png` (1024x1024).

## The post

`POST.json` holds the X post address. The post carries the meme image, a make.fun link, and the entry's play code.

## Run it

```sh
MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `POST.json` to the output directory and validates it.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
