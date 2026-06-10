# convergence-radar × frontrun — x_live patch (staged here, not yet applied)

This folder is a **ready-to-apply patch** for the `convergence-radar` repo. It
lives in the `tls` branch because that is the only repo this session can write
to — see "Why it's here" below.

## What it does

Automates the radar's one manual source. Today `frontrun_trending` needs a human
to copy JSON out of frontrun.pro's Chrome extension via DevTools every cycle.
`x_live.py` reads X the way frontrun does — intercepting X's internal GraphQL
from a logged-in session — and writes the same inbox JSON automatically.

## Files

| file | drop into convergence-radar at |
|---|---|
| `scripts/fetchers/x_live.py` | `scripts/fetchers/x_live.py` |
| `docs/X_LIVE.md` | `docs/X_LIVE.md` |
| `social.yaml.patch` | append to `sources/social.yaml` (optional) |

## Apply

```bash
cd ~/convergence-radar   # or wherever the canonical repo is
cp <this-folder>/scripts/fetchers/x_live.py scripts/fetchers/x_live.py
cp <this-folder>/docs/X_LIVE.md docs/X_LIVE.md
# optional: append the source row in social.yaml.patch to sources/social.yaml
# one-time login per docs/X_LIVE.md, then:
python scripts/fetchers/x_live.py     # smoke test → writes an inbox file
```

Then wire `x_live.fetch_x_live()` into the cycle wrapper before the fetch step
(one line, shown in `docs/X_LIVE.md`).

## Sync to Studio

This does NOT auto-reach the Mac Studio. Based on how the other skills sync
(e.g. chase-voice's `.github/workflows/sync-to-monorepo.yml` mirrors into the
`chasewang-skills` monorepo, and "Mac Studio pulls the monorepo via its
existing skillsync cron"), the path once applied to the canonical repo is:

1. commit + push to canonical `convergence-radar`
2. the repo's sync workflow mirrors it into `chasewang-skills`
3. the Studio's `skillsync` cron pulls the monorepo

I can't trigger any of that from here (no write access to convergence-radar or
the Studio).

## Why it's here and not in convergence-radar

This session's git proxy and GitHub tools are scoped to `ckpxgfnksd-max/tls`
only. Cloning/pushing `convergence-radar` returns 502 (repo not authorized),
and no `add_repo` tool is mounted in this session. So the patch is staged here,
verified (`py_compile` clean), ready to copy. To have me apply + push it
directly, add `convergence-radar` to the session scope.
