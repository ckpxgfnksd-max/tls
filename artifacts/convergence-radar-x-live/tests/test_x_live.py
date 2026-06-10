"""Standalone unit tests for x_live's pure (no-browser) functions.

Runs WITHOUT Playwright or a live X session: it feeds a synthetic X GraphQL
payload through the same _walk -> _trending -> _write_inbox path the fetcher
uses, and asserts the emitted inbox JSON matches the radar's documented schema
{source, domain, items:[{url, title, body, published_at}]}.

This is deliberately self-contained so it can run in the staging repo before
convergence-radar is reachable. When the patch lands in radar, drop it next to
the repo's other tests (it imports x_live by locating scripts/fetchers).

Run:  python tests/test_x_live.py        # plain, no deps
  or: pytest tests/test_x_live.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

# locate scripts/fetchers/x_live.py relative to this test, regardless of cwd
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "scripts" / "fetchers"))
import x_live  # noqa: E402


def _tweet(tid, handle, text, *, likes=0, rts=0, replies=0, views=0):
    """A minimal but realistic slice of an X GraphQL tweet_results entry,
    matching the invariant _walk keys off: result.legacy + core.user_results."""
    return {
        "result": {
            "__typename": "Tweet",
            "core": {"user_results": {"result": {"legacy": {"screen_name": handle}}}},
            "views": {"count": str(views)},
            "legacy": {
                "id_str": tid,
                "full_text": text,
                "created_at": "Wed Jun 10 06:30:00 +0000 2026",
                "favorite_count": likes,
                "retweet_count": rts,
                "reply_count": replies,
            },
        }
    }


def _payload(*tweets):
    """Bury the tweets under a couple of junk wrapper layers so the test also
    exercises _walk's recursion rather than a flat hand-fed list."""
    return {"data": {"home": {"timeline": {"instructions": [
        {"type": "TimelineAddEntries", "entries": list(tweets)}
    ]}}}}


def test_walk_extracts_tweets():
    cap = x_live._Capture()
    x_live._walk(_payload(_tweet("1", "alice", "hello world", likes=5)),
                 cap, own_handle="ChaseWang")
    assert set(cap.items) == {"1"}
    it = cap.items["1"]
    assert it.author == "alice"
    assert it.body == "hello world"
    assert it.url == "https://x.com/alice/status/1"
    assert it.published_at == "2026-06-10T06:30:00+00:00"


def test_skips_own_handle():
    cap = x_live._Capture()
    x_live._walk(_payload(_tweet("9", "ChaseWang", "my own tweet")),
                 cap, own_handle="ChaseWang")
    assert cap.items == {}


def test_trending_orders_by_engagement_and_dedupes():
    cap = x_live._Capture()
    x_live._walk(
        _payload(
            _tweet("1", "a", "low signal", likes=1),
            _tweet("2", "b", "high signal", likes=10, rts=10),  # strongest
            _tweet("3", "c", "low signal", likes=2),            # dup first line
        ),
        cap, own_handle=None,
    )
    top = x_live._trending(cap, top_n=10)
    assert top[0].body == "high signal"        # engagement-ranked first
    titles = [t.title.lower() for t in top]
    assert len(titles) == len(set(titles))     # "low signal" de-duped to one


def test_write_inbox_canonical_schema():
    cap = x_live._Capture()
    x_live._walk(_payload(_tweet("1", "alice", "schema check", likes=3)),
                 cap, own_handle=None)
    with tempfile.TemporaryDirectory() as d:
        os.environ["CR_INBOX_DIR"] = d
        os.environ.pop("CR_X_RICH_ITEMS", None)  # default = rich on
        dest = x_live._write_inbox(x_live._trending(cap, top_n=10))
        payload = json.loads(Path(dest).read_text(encoding="utf-8"))
    assert payload["source"] == "frontrun_trending"
    assert payload["domain"] == "social"
    item = payload["items"][0]
    for k in ("url", "title", "body", "published_at"):
        assert k in item, f"missing canonical key {k}"
    # rich default also carries the extras
    assert "engagement" in item and "author" in item


def test_write_inbox_minimal_when_rich_disabled():
    cap = x_live._Capture()
    x_live._walk(_payload(_tweet("1", "alice", "minimal", likes=3)),
                 cap, own_handle=None)
    with tempfile.TemporaryDirectory() as d:
        os.environ["CR_INBOX_DIR"] = d
        os.environ["CR_X_RICH_ITEMS"] = "0"
        try:
            dest = x_live._write_inbox(x_live._trending(cap, top_n=10))
            payload = json.loads(Path(dest).read_text(encoding="utf-8"))
        finally:
            os.environ.pop("CR_X_RICH_ITEMS", None)
    item = payload["items"][0]
    assert set(item) == {"url", "title", "body", "published_at"}  # nothing extra


def test_source_id_override():
    cap = x_live._Capture()
    x_live._walk(_payload(_tweet("1", "alice", "id override", likes=1)),
                 cap, own_handle=None)
    with tempfile.TemporaryDirectory() as d:
        os.environ["CR_INBOX_DIR"] = d
        dest = x_live._write_inbox(x_live._trending(cap, top_n=10), source="x_live")
        payload = json.loads(Path(dest).read_text(encoding="utf-8"))
    assert payload["source"] == "x_live"


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok   {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL {name}: {e}")
            except Exception as e:  # noqa: BLE001
                failures += 1
                print(f"ERR  {name}: {e!r}")
    print(f"\n{'PASS' if not failures else 'FAIL'} — {failures} failure(s)")
    sys.exit(1 if failures else 0)
