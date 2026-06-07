# x auto loop — topic dedup ledger

Drop-in fix for "the same topic got posted twice" (e.g. **gh copilot** went out
twice because nothing remembered it had already been posted, and `gh copilot` /
`GitHub Copilot` / `github-copilot` compared as different strings).

`topic_ledger.py` is a standalone CLI with **no dependencies** (Python 3, already
on macOS). Call it from your loop regardless of what language the loop is written
in.

## The rule

1. **Before posting** — `check`. If it exits non-zero, skip the topic.
2. **After a SUCCESSFUL post** — `commit` (with the tweet id). Never commit before
   posting, or a failed post will permanently block the topic.

The ledger is append-only and `flock`-protected, so it survives loop restarts and
is safe even if two loop instances run at once.

## Wiring it in

**Bash**
```bash
LEDGER="python3 /path/to/x-auto-loop/topic_ledger.py"

if ! $LEDGER check "$topic"; then
    echo "skip: already posted -> $topic"; continue
fi
tweet_id=$(post_to_x "$text")          # your existing post call
$LEDGER commit "$topic" --tweet-id "$tweet_id"
```

**Python**
```python
import subprocess
LEDGER = ["python3", "/path/to/x-auto-loop/topic_ledger.py"]

if subprocess.run(LEDGER + ["check", topic]).returncode != 0:
    continue                                   # duplicate -> skip
tweet_id = post_to_x(text)                      # your existing post call
subprocess.run(LEDGER + ["commit", topic, "--tweet-id", str(tweet_id)], check=True)
```

**Node**
```js
const { spawnSync } = require("child_process");
const LEDGER = ["python3", "/path/to/x-auto-loop/topic_ledger.py"];

if (spawnSync(LEDGER[0], [LEDGER[1], "check", topic]).status !== 0) continue;
const tweetId = await postToX(text);            // your existing post call
spawnSync(LEDGER[0], [LEDGER[1], "commit", topic, "--tweet-id", String(tweetId)]);
```

## Config

| Setting | How | Default |
|---|---|---|
| Ledger file | `$TOPIC_LEDGER_PATH` or `--ledger` | `~/.x-auto-loop/posted_topics.jsonl` |
| Dedup window | `$TOPIC_LEDGER_WINDOW_DAYS` or `--window-days` | `0` = forever |

Set a window (e.g. `--window-days 30`) if you *want* to allow re-posting a topic
after a while; leave it at `0` to never repeat.

## Catching more near-duplicates

If two phrasings of the same topic still slip through, add them to the `SYNONYMS`
map at the top of `topic_ledger.py`. Each left-hand variant (in normalized form:
lowercase, no punctuation) collapses to the canonical key on the right. The
gh-copilot family is already seeded there.

Inspect what's been posted:
```bash
python3 topic_ledger.py list
python3 topic_ledger.py normalize "GitHub Copilot!!"   # -> github copilot
```

## Backfill (important)

Your existing loop already has post history that isn't in this ledger. Seed it once
so old topics are recognized, e.g.:
```bash
python3 topic_ledger.py commit "github copilot" --tweet-id <id-of-the-real-post>
```
Add a `commit ... --force` line per already-posted topic (or script it from your
existing history) before turning the `check` gate on.
