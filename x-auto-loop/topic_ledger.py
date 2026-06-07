#!/usr/bin/env python3
"""topic_ledger.py — persistent, language-agnostic dedup ledger for the x auto loop.

Why this exists: the loop posted the "gh copilot" topic twice because there was no
durable record of what had already gone out, and because "gh copilot" /
"GitHub Copilot" / "github-copilot" look like different strings. This tool fixes
both: it keeps an append-only ledger that survives loop restarts, and it normalizes
topics (case, punctuation, whitespace, known synonyms) before comparing.

Call it from any language — Python, Node, or Bash — by shelling out:

    # before posting: skip if this exits non-zero
    python3 topic_ledger.py check "GitHub Copilot" || continue
    # ... post the tweet ...
    # after a SUCCESSFUL post: record it (atomic, flock-protected)
    python3 topic_ledger.py commit "GitHub Copilot" --tweet-id 1234567890

Exit codes for `check`:
    0  -> topic is NEW (safe to post)
    1  -> topic is a DUPLICATE (do not post)
    2  -> usage / internal error

Ledger location (override with $TOPIC_LEDGER_PATH):
    ~/.x-auto-loop/posted_topics.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone

try:
    import fcntl  # POSIX (macOS + Linux). Used for atomic append + check locking.
    _HAVE_FCNTL = True
except ImportError:  # pragma: no cover - Windows fallback
    _HAVE_FCNTL = False


DEFAULT_LEDGER = os.path.expanduser(
    os.environ.get("TOPIC_LEDGER_PATH", "~/.x-auto-loop/posted_topics.jsonl")
)

# Canonical-form synonyms: every variant on the left collapses to the key it maps
# to AFTER basic normalization. Seeded with the gh-copilot case that bit us. Add
# more as you notice near-duplicate topics slipping through.
SYNONYMS = {
    "gh copilot": "github copilot",
    "githubcopilot": "github copilot",
    "github co pilot": "github copilot",
    "copilot": "github copilot",
}


def normalize(topic: str) -> str:
    """Reduce a topic to a stable comparison key.

    lowercase -> NFKC unicode fold -> drop punctuation -> collapse whitespace ->
    apply synonym map. So "GitHub Copilot!!", "gh copilot", and "github-copilot"
    all become the same key.
    """
    s = unicodedata.normalize("NFKC", topic).lower()
    s = re.sub(r"[^\w\s]", " ", s)        # punctuation/symbols -> space
    s = re.sub(r"_", " ", s)              # underscores too (\w keeps them)
    s = re.sub(r"\s+", " ", s).strip()
    return SYNONYMS.get(s, s)


def _read_records(path: str):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as fh:
        if _HAVE_FCNTL:
            fcntl.flock(fh.fileno(), fcntl.LOCK_SH)
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue  # tolerate a torn final line rather than crashing the loop


def _within_window(posted_at: str, window_days: float) -> bool:
    if window_days <= 0:
        return True  # 0 / negative == dedup forever
    try:
        then = datetime.fromisoformat(posted_at)
    except ValueError:
        return True  # unparseable timestamp -> treat as still-counting, be safe
    if then.tzinfo is None:
        then = then.replace(tzinfo=timezone.utc)
    age_days = (datetime.now(timezone.utc) - then).total_seconds() / 86400.0
    return age_days <= window_days


def find_duplicate(path: str, key: str, window_days: float):
    """Return the first matching record within the window, or None."""
    for rec in _read_records(path):
        if rec.get("normalized_topic") == key and _within_window(
            rec.get("posted_at", ""), window_days
        ):
            return rec
    return None


def cmd_check(args) -> int:
    key = normalize(args.topic)
    dup = find_duplicate(args.ledger, key, args.window_days)
    if dup:
        when = dup.get("posted_at", "?")
        raw = dup.get("raw_topic", key)
        sys.stderr.write(
            f"DUPLICATE\tkey={key!r}\tfirst_posted={when}\tas={raw!r}\n"
        )
        print("DUPLICATE")
        return 1
    print("NEW")
    return 0


def cmd_commit(args) -> int:
    key = normalize(args.topic)
    if not args.force:
        dup = find_duplicate(args.ledger, key, args.window_days)
        if dup:
            sys.stderr.write(
                f"REFUSED\talready in ledger as {dup.get('raw_topic', key)!r} "
                f"at {dup.get('posted_at', '?')} (use --force to override)\n"
            )
            return 1

    rec = {
        "normalized_topic": key,
        "raw_topic": args.topic,
        "tweet_id": args.tweet_id,
        "posted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.ledger)), exist_ok=True)
    # O_APPEND + exclusive flock makes concurrent loop instances safe: the
    # select-post-record step can't interleave into a torn/duplicate write.
    fd = os.open(args.ledger, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        if _HAVE_FCNTL:
            fcntl.flock(fd, fcntl.LOCK_EX)
        os.write(fd, (json.dumps(rec, ensure_ascii=False) + "\n").encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    print(f"RECORDED\t{key}")
    return 0


def cmd_list(args) -> int:
    n = 0
    for rec in _read_records(args.ledger):
        n += 1
        print(
            f"{rec.get('posted_at', '?'):<25} "
            f"{rec.get('normalized_topic', ''):<28} "
            f"id={rec.get('tweet_id') or '-':<20} "
            f"({rec.get('raw_topic', '')})"
        )
    sys.stderr.write(f"\n{n} topic(s) in {args.ledger}\n")
    return 0


def cmd_normalize(args) -> int:
    print(normalize(args.topic))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="topic_ledger.py",
        description="Persistent dedup ledger for the x auto loop.",
    )
    p.add_argument(
        "--ledger",
        default=DEFAULT_LEDGER,
        help=f"ledger path (default: {DEFAULT_LEDGER} or $TOPIC_LEDGER_PATH)",
    )
    p.add_argument(
        "--window-days",
        type=float,
        default=float(os.environ.get("TOPIC_LEDGER_WINDOW_DAYS", "0")),
        help="dedup window in days; 0 = forever (default). "
        "Set e.g. 30 to allow re-posting a topic after a month.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="exit 0 if topic is new, 1 if duplicate")
    c.add_argument("topic")
    c.set_defaults(func=cmd_check)

    c = sub.add_parser("commit", help="record a successfully posted topic")
    c.add_argument("topic")
    c.add_argument("--tweet-id", default=None, help="id of the posted tweet")
    c.add_argument("--force", action="store_true", help="record even if duplicate")
    c.set_defaults(func=cmd_commit)

    c = sub.add_parser("list", help="print the ledger")
    c.set_defaults(func=cmd_list)

    c = sub.add_parser("normalize", help="print the normalized key for a topic")
    c.add_argument("topic")
    c.set_defaults(func=cmd_normalize)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except BrokenPipeError:  # e.g. `... list | head`
        return 0
    except Exception as exc:  # never let a ledger hiccup crash the loop silently
        sys.stderr.write(f"topic_ledger error: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
