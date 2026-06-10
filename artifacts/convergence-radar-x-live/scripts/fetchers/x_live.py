"""x_live — auto-ingest X (Twitter) signals by intercepting X's own GraphQL,
the way frontrun.pro's extension does, but headless on the Studio.

WHY THIS EXISTS
---------------
The radar already has a `frontrun_trending` source (adapter: inbox), but it is
MANUAL: a human opens frontrun.pro in Chrome, grabs the trending JSON via
DevTools, and drops a file into ~/.cache/convergence-radar/inbox/. That is the
one source in the whole radar that needs a human every cycle.

Reverse-engineering frontrun (2026-06) showed how it actually reads X without
the official API: a content script monkey-patches `fetch`/`XHR`/`WebSocket` in
the page's MAIN world and captures X's internal GraphQL responses
(HomeLatestTimeline, SearchTimeline, UserTweets, ...) from the user's own
logged-in session. No API keys, no rate caps, real-time.

This module does the same thing in a headless Playwright context that reuses a
persisted X login: it navigates X like a reader, lets X fire its own GraphQL,
captures the responses via `page.on("response")`, extracts tweets, scores a
lightweight surge per author, and writes the radar's standard inbox JSON. The
existing, tested `inbox` adapter then picks it up — so the blast radius is one
new fetcher plus one source row; the rest of the pipeline is unchanged.

SAFETY (the lesson from Xhunt, the shady twin of frontrun)
----------------------------------------------------------
- Read-only. No posting, no wallet surface, no DOM injection.
- No fingerprint/IP exfiltration, no open HTTP proxy. We only read X GraphQL
  responses X itself emits and write them to a local file.
- Session cookies stay in a local persistent profile dir; never transmitted.
- Captures are capped and the whole run is best-effort: any failure logs and
  returns success=False so the radar skips this source and keeps going (matches
  the radar's "never fully fail" contract).

CONFIG (env)
------------
  CR_X_PROFILE_DIR   persistent browser profile with a logged-in X session
                     (default: ~/.config/convergence-radar/x-profile)
  CR_INBOX_DIR       inbox the radar reads (default: XDG cache .../inbox)
  CR_X_QUERIES       comma-separated search terms to surface beyond the home
                     feed (default: a crypto/macro set)
  CR_X_MAX_TWEETS    capture cap per run (default: 300)
  CR_X_HEADLESS      "0" to watch it run for debugging (default: "1")

This file is dependency-light: Playwright only. If Playwright or a logged-in
profile is missing, it degrades to success=False without raising.
"""
from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

# GraphQL operationName -> the JSON path shape we know how to walk. We match on
# the operation substring in the request URL; X versions the hashes but keeps
# the operation name, exactly the seam frontrun keys off.
_GRAPHQL_OPS = (
    "HomeLatestTimeline",
    "HomeTimeline",
    "SearchTimeline",
    "UserTweets",
    "ListLatestTweetsTimeline",
)
_GRAPHQL_RE = re.compile(r"/i/api/graphql/[^/]+/(" + "|".join(_GRAPHQL_OPS) + r")")

_DEFAULT_QUERIES = (
    "crypto", "bitcoin OR btc", "stablecoin", "tokenomics",
    "rate cut OR fed", "airdrop OR TGE",
)


@dataclass
class _Item:
    url: str
    title: str
    body: str
    published_at: str
    author: str
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    views: int = 0


@dataclass
class _Capture:
    items: dict[str, _Item] = field(default_factory=dict)  # tweet_id -> item

    def add(self, it: _Item, tid: str) -> None:
        # keep the richest copy (a tweet seen twice may arrive with more counts)
        prev = self.items.get(tid)
        if prev is None or it.views >= prev.views:
            self.items[tid] = it


# ── GraphQL response walking ────────────────────────────────────────────────
def _legacy(tweet_result: dict) -> dict | None:
    """X wraps the real tweet under result.legacy (sometimes via .tweet)."""
    res = tweet_result.get("result") or tweet_result
    if res.get("__typename") == "TweetWithVisibilityResults":
        res = res.get("tweet", res)
    return res.get("legacy")


def _walk(obj, cap: _Capture, *, own_handle: str | None) -> None:
    """Recursively find tweet_results entries anywhere in a GraphQL payload.
    X reshapes timelines constantly, so we don't hard-code the entry path —
    we look for the invariant: a dict carrying a `legacy` tweet body + a
    `core.user_results` author. This survives most timeline refactors."""
    if isinstance(obj, list):
        for x in obj:
            _walk(x, cap, own_handle=own_handle)
        return
    if not isinstance(obj, dict):
        return

    legacy = _legacy(obj) if ("result" in obj or "legacy" in obj) else None
    if legacy and legacy.get("full_text") and legacy.get("id_str"):
        author = _author_handle(obj)
        if not author or (own_handle and author.lower() == own_handle.lower()):
            pass  # skip own tweets; still recurse below for quoted/retweeted
        else:
            tid = legacy["id_str"]
            text = legacy["full_text"]
            cap.add(
                _Item(
                    url=f"https://x.com/{author}/status/{tid}",
                    title=_first_line(text),
                    body=text,
                    published_at=_iso(legacy.get("created_at")),
                    author=author,
                    likes=int(legacy.get("favorite_count") or 0),
                    retweets=int(legacy.get("retweet_count") or 0),
                    replies=int(legacy.get("reply_count") or 0),
                    views=_views(obj),
                ),
                tid,
            )
    for v in obj.values():
        _walk(v, cap, own_handle=own_handle)


def _author_handle(tweet_result: dict) -> str | None:
    res = tweet_result.get("result") or tweet_result
    if res.get("__typename") == "TweetWithVisibilityResults":
        res = res.get("tweet", res)
    core = (res.get("core") or {}).get("user_results") or {}
    ul = (core.get("result") or {}).get("legacy") or {}
    return ul.get("screen_name")


def _views(tweet_result: dict) -> int:
    res = tweet_result.get("result") or tweet_result
    v = (res.get("views") or {}).get("count")
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def _first_line(text: str) -> str:
    line = text.strip().splitlines()[0] if text.strip() else text
    return (line[:140]).strip()


def _iso(created_at: str | None) -> str:
    # X uses "Wed Jun 10 06:30:00 +0000 2026"; fall back to now on parse fail.
    if created_at:
        try:
            t = time.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
            return time.strftime("%Y-%m-%dT%H:%M:%S+00:00", t)
        except (ValueError, TypeError):
            pass
    return time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())


# ── surge scoring ───────────────────────────────────────────────────────────
def _engagement(it: _Item) -> float:
    # reply+repost weighted over likes — the same "is this moving" shape the
    # radar's killswitch reads, and what X's banger screen rewards.
    return it.likes + 3 * it.retweets + 2 * it.replies + 0.01 * it.views


def _trending(cap: _Capture, top_n: int) -> list[_Item]:
    items = sorted(cap.items.values(), key=_engagement, reverse=True)
    # de-dupe near-identical bodies (quote chains repeat text) by first line
    seen: set[str] = set()
    out: list[_Item] = []
    for it in items:
        key = it.title.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
        if len(out) >= top_n:
            break
    return out


# ── inbox emission (the radar's standard schema) ────────────────────────────
def _inbox_dir() -> Path:
    env = os.environ.get("CR_INBOX_DIR")
    if env:
        return Path(env)
    cache = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(cache) / "convergence-radar" / "inbox"


def _write_inbox(items: list[_Item], source: str = "frontrun_trending") -> Path:
    """Write the exact shape the radar's inbox adapter already parses:
    {source, domain, items:[{url,title,body,published_at}]}. We reuse the
    existing `frontrun_trending` source id so no scoring/config changes are
    needed — this just removes the human from that source."""
    inbox = _inbox_dir()
    inbox.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": source,
        "domain": "social",
        "fetched_at": _iso(None),
        "items": [
            {
                "url": it.url,
                "title": it.title,
                "body": it.body,
                "published_at": it.published_at,
                # extra fields are ignored by the adapter but useful in raw_json
                "engagement": _engagement(it),
                "author": it.author,
            }
            for it in items
        ],
    }
    dest = inbox / f"x_live_{int(time.time())}.json"
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


# ── driver ──────────────────────────────────────────────────────────────────
def _profile_dir() -> Path:
    env = os.environ.get("CR_X_PROFILE_DIR")
    if env:
        return Path(env)
    return Path.home() / ".config" / "convergence-radar" / "x-profile"


def _queries() -> list[str]:
    raw = os.environ.get("CR_X_QUERIES")
    return [q.strip() for q in raw.split(",")] if raw else list(_DEFAULT_QUERIES)


def fetch_x_live() -> dict:
    """Capture X GraphQL from a logged-in session and write inbox JSON.

    Returns a small result dict (success, count, path|error) so the radar's
    fetch loop can log + skip on failure exactly like every other source."""
    try:
        from playwright.sync_api import sync_playwright  # local dep, optional
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": f"playwright unavailable: {e}"}

    profile = _profile_dir()
    if not profile.exists():
        return {
            "success": False,
            "error": f"no X profile at {profile} — run the one-time login "
            f"(see docs/X_LIVE.md) before enabling this source",
        }

    cap = _Capture()
    own = os.environ.get("CR_X_OWN_HANDLE", "ChaseWang")
    max_tweets = int(os.environ.get("CR_X_MAX_TWEETS", "300"))
    headless = os.environ.get("CR_X_HEADLESS", "1") != "0"

    def _on_response(resp) -> None:
        try:
            if not _GRAPHQL_RE.search(resp.url):
                return
            data = resp.json()
        except Exception:  # noqa: BLE001 — any capture error is non-fatal
            return
        _walk(data, cap, own_handle=own)

    try:
        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(
                str(profile), headless=headless,
                args=["--disable-blink-features=AutomationControlled"],
            )
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.on("response", _on_response)

            # 1) home feed — what X thinks is hot for this account
            _visit(page, "https://x.com/home")
            # 2) targeted searches — surface beyond the follow graph (OON)
            for q in _queries():
                if len(cap.items) >= max_tweets:
                    break
                url = "https://x.com/search?f=live&q=" + _enc(q)
                _visit(page, url)
            ctx.close()
    except Exception as e:  # noqa: BLE001
        # still emit whatever we captured before the failure
        if cap.items:
            dest = _write_inbox(
                _trending(cap, top_n=50),
                source=os.environ.get("CR_X_SOURCE_ID", "frontrun_trending"),
            )
            return {"success": True, "count": len(cap.items),
                    "path": str(dest), "warning": f"partial: {e}"}
        return {"success": False, "error": str(e)}

    if not cap.items:
        return {"success": False, "error": "captured 0 tweets (login expired?)"}

    top = _trending(cap, top_n=int(os.environ.get("CR_X_TOP_N", "50")))
    dest = _write_inbox(top, source=os.environ.get("CR_X_SOURCE_ID", "frontrun_trending"))
    return {"success": True, "count": len(cap.items),
            "written": len(top), "path": str(dest)}


def _visit(page, url: str) -> None:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        # let X fire its lazy GraphQL + a couple of scrolls for more entries
        for _ in range(3):
            page.wait_for_timeout(1500)
            page.mouse.wheel(0, 4000)
        page.wait_for_timeout(1500)
    except Exception:  # noqa: BLE001 — a slow page shouldn't kill the run
        pass


def _enc(q: str) -> str:
    from urllib.parse import quote
    return quote(q)


if __name__ == "__main__":
    print(json.dumps(fetch_x_live(), ensure_ascii=False, indent=2))
