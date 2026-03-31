# TLS — Token Launch Stack

A CLI advisory tool that guides founders through token launch decisions. Built for people who care about getting it right, not just getting it live.

Created by **Chase Wang** (https://x.com/ChaseWang) — ex-Binance listing team, reviewed over 1,000 projects, launched ~100 tokens in 2025.

---

## What This Is

TLS is a collection of skills that walk founders through the entire token launch journey — from "should I even have a token?" to a professional vesting schedule ready for exchanges and investors. Each skill is a standalone advisory session that produces structured output you can share with your team, advisors, or legal counsel.

The tool thinks WITH you, never FOR you. It uses forcing questions to surface what you actually know (and don't know) before making any recommendations.

---

## Install

Copy the skill folder into your agent's skill directory:

**Claude Code:**
```bash
cp -r tls-why-token ~/.claude/skills/why-token
cp -r tls-tokenomics ~/.claude/skills/tokenomics
```

**OpenClaw:**
```bash
cp -r tls-why-token ~/.openclaw/skills/why-token
cp -r tls-tokenomics ~/.openclaw/skills/tokenomics
```

Then start a session and type `/why-token` or `/tokenomics`.

---

## Available Skills

### `/why-token` — v1.0.3

The starting point. Answers the most important question before anything else: *why a token at all?*

- Silently detects founder sophistication from how they talk — no patronizing intro for experienced builders
- Forces honest answers on motivation (liquidity event, product-embedded, attention, exit)
- Routes pure meme launches to a quick checklist — this tool is for people who care about fundamentals
- Deep-dives value accrual: distinguishes cash-flow-backed mechanisms (buyback, burn, fee-capture) from willingness-to-pay (MV=PQ dynamics)
- Covers key parties, timeline, fundraise, and Q7 regulatory awareness (March 2026 SEC/CFTC joint guidance — 5-category taxonomy)
- Produces a structured document: **Decisions** (what you've resolved) + **Context** (supporting analysis)
- References 19 real token launches with CoinMarketCap links so you can study what worked

**Run:** `/why-token`

---

### `/tokenomics` — v2.0.20

Takes the thesis from `/why-token` and turns it into numbers. Two modes, one output.

**Mode A — Build from scratch**
Full Q&A flow collecting supply, allocation categories, vesting schedules, and demand-side inputs. Validates as you go.

**Mode B — Start from a real token**
Pick a reference token from the built-in database ($UNI, $JUP, $SOL, $BNB, $LINK, $ENA, $ONDO, and more). The skill loads their allocation structure as your starting template. Modify what you need, keep what fits.

**What it produces:**
- Excel token release schedule (`tokenomics-{TICKER}-{DATE}.xlsx`) — 2 sheets:
  - `3-1. Token Allocation Breakdown` — allocation table + monthly vesting schedule, formatted for exchange due diligence
  - `Token Release Chart` — supply/demand simulation chart: stacked monthly unlocks by category + gross vs. net circulating supply after buybacks and burns
- Smart validation: flags high TGE unlock, missing liquidity, insider-heavy allocation, sub-12mo team cliff, FDV sanity check
- Value Accrual Bridge: connects `/why-token` demand model (revenue → buyback qty → net circulating) to the chart

**Run:** `/tokenomics`

---

## Reference Token Database

`tls-why-token/data/reference-tokens.json` — 19 curated token launches with full advisory fields and tokenomics data.

**Structured (full vesting data):**
$UNI, $BNB, $SOL, $ETH, $LINK, $HYPE, $SKY, $AAVE, $ONDO, $ENA, $MORPHO, $ZRO, $JUP

**Fair-launch (no structured allocation):**
$DOGE, $PEPE, $FARTCOIN, $TAO

**Low-confidence (partial/estimated — verify before use):**
$PUMP, $KITE

Each entry includes: category tags, mechanism tags, launch tags, case summary, key lesson, CoinMarketCap link, and a full tokenomics block (total supply, TGE date, allocation categories with cliff/vest data).

The database is designed to grow. Adding a new token = adding a JSON block.

---

## Evals

Each skill ships with an `EVALS.md` alongside the `SKILL.md`:

- `tls-why-token/EVALS.md` — 7-criterion rubric, 4 fixed personas, round-by-round optimization log
- `tls-tokenomics/EVALS.md` — same format; baseline 49/56 → 56/56 after 20 autoresearch rounds

Skills are optimized using the Karpathy autoresearch method: fixed personas, fixed rubric, one change per round, keep if score improves. Round logs are published so you can see what changed and why.

---

## Roadmap

### `/launch-strategy` — Next

The operational playbook from T-90 days to TGE. Coordinates all the parties from `/why-token` into an actual timeline: exchange selection, market maker engagement, KOL strategy, launchpad decision, legal, and community. Who does what, when, and what blocks what.

### `/mv-pq` — Token Valuation Framework

Applies the MV=PQ (Fisher 1911) framework to token design. Connects qualitative value accrual decisions to quantitative modeling: velocity assumptions, implied price levels, sensitivity to supply changes. Bridges `/why-token` and `/tokenomics` with formal economic grounding.

### `/market-making` — Liquidity Strategy

How market making actually works. CEX vs DEX liquidity, how to evaluate and engage market makers, what terms to expect, and what the common traps are (predatory loan structures, inventory risk misalignment, spread manipulation).

---

## For Deeper Work

This tool is free advisory — a public good for founders. If your situation requires custom work (multi-round fundraise structuring, exchange strategy, market maker negotiation), reach out:

**Chase Wang** — https://x.com/ChaseWang | GitHub Issues: https://github.com/ckpxgfnksd-max/tls/issues

---

## Stack

- SKILL.md files (markdown) — skill definitions compatible with Claude Code and OpenClaw
- Python + openpyxl + matplotlib — Excel and chart generation (no external API dependencies)
- JSON — reference token database

## License

MIT
