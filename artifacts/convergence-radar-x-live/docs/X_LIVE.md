# x_live — automated X GraphQL ingest (the frontrun mechanism, headless)

## What it replaces

The radar already ships a `frontrun_trending` source with `adapter: inbox`. It
works, but it's the **only source that needs a human every cycle**: you open
frontrun.pro in Chrome, copy the trending JSON out of DevTools, and drop a file
into `~/.cache/convergence-radar/inbox/`.

`x_live.py` removes the human. It reads X the way frontrun's extension does —
intercepting X's own internal GraphQL — and writes the same inbox JSON the
radar already parses.

## How frontrun actually reads X (reverse-engineered 2026-06)

frontrun's Chrome extension injects a content script into x.com that
monkey-patches `fetch` / `XMLHttpRequest` / `WebSocket` in the page's MAIN
world and captures the responses of ~12 X GraphQL operations
(`HomeLatestTimeline`, `SearchTimeline`, `UserTweets`, followers, following,
search, …) straight from your logged-in session. No official X API, no API
keys, no rate caps, real-time.

`x_live.py` does the same capture, but in a headless Playwright context that
reuses a persisted X login instead of a browser extension — because the radar
runs as a Studio cron, not inside a browser. It navigates X like a reader,
lets X fire its own GraphQL, and grabs the responses via `page.on("response")`.

## What it does NOT do (the Xhunt lesson)

Xhunt is frontrun's shady twin: it exfiltrates IP / city / ISP / FingerprintJS
device fingerprints / every Twitter URL you visit to `kb.xhunt.ai`, obfuscates
its headers with RC4, and ships an unrestricted HTTP proxy + a wired-up wallet
injection surface. `x_live.py` deliberately does none of that:

- **Read-only.** No posting, no DOM injection, no wallet surface.
- **No exfiltration.** It only reads X GraphQL responses X itself emits and
  writes them to a local inbox file. No fingerprinting, no proxy.
- **Local session.** Cookies live in a local persistent profile dir and are
  never transmitted anywhere.
- **Best-effort.** Any failure logs and returns `success=False`; the radar
  skips the source and keeps going (the "never fully fail" contract).

## One-time setup

```bash
# 1) create a persistent profile and log into X once (interactive)
CR_X_HEADLESS=0 python -m playwright open --browser chromium \
  --user-data-dir ~/.config/convergence-radar/x-profile https://x.com/login
#    log in, pass any checkpoint, then close the window.

# 2) dry-run the fetcher
python scripts/fetchers/x_live.py
#    -> writes ~/.cache/convergence-radar/inbox/x_live_<ts>.json
```

## Wiring into the radar

`x_live.py` writes to the inbox under the **existing** `frontrun_trending`
source id, so no scoring/config change is strictly required — the tested inbox
adapter ingests it on the next cycle. To run it on the cron, add one call
before the radar's fetch step (e.g. in the cycle wrapper):

```python
from scripts.fetchers import x_live
res = x_live.fetch_x_live()
log.info("x_live: %s", res)   # success/skip is logged like any source
```

Optionally give it its own source row so it scores as a distinct source in the
cross-source spread (recommended — see `social.yaml.patch`).

## Config (env)

| var | default | meaning |
|---|---|---|
| `CR_X_PROFILE_DIR` | `~/.config/convergence-radar/x-profile` | logged-in X profile |
| `CR_INBOX_DIR` | `$XDG_CACHE_HOME/convergence-radar/inbox` | radar inbox |
| `CR_X_QUERIES` | crypto/macro set | extra live searches beyond home feed |
| `CR_X_OWN_HANDLE` | `ChaseWang` | own tweets are skipped |
| `CR_X_MAX_TWEETS` | `300` | capture cap per run |
| `CR_X_TOP_N` | `50` | how many trending items to emit |
| `CR_X_HEADLESS` | `1` | `0` to watch it run |

## Maintenance note

GraphQL capture breaks when X reshapes a timeline payload. `_walk()` is written
against the invariant (a `legacy` tweet body + `core.user_results` author)
rather than a hard-coded path, so it survives most refactors — but if captures
drop to zero, check `_GRAPHQL_OPS` and the `legacy` shape first.

## Real-time upgrade (later)

frontrun also hooks `WebSocket` for sub-second delivery. Playwright can capture
WS frames via `page.on("websocket")` → `ws.on("framereceived")`. For the radar's
4-hour cadence the polling capture above is enough; the WS hook only matters if
x_live later feeds the X-auto reply cockpit's "15-minute front-run" window,
where latency is the alpha.
