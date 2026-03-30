# TLS — Token Launch Stack

A CLI advisory tool that guides founders through token launch decisions. Built for people who care about getting it right, not just getting it live.

Created by **Chase Wang** (https://x.com/ChaseWang) — ex-Binance listing team, reviewed over 1,000 projects, launched ~100 tokens in 2025.

---

## What This Is

TLS is a collection of skills that walk founders through the entire token launch journey — from "should I even have a token?" to live market operations. Each skill is a standalone advisory session that produces a structured document you can share with your team, advisors, or legal counsel.

The tool thinks WITH you, never FOR you. It uses forcing questions to surface what you actually know (and don't know) before making any recommendations.

## Install

Drop the skill folder into your agent's skill directory:

**Claude Code:**
```bash
cp -r tls-why-token ~/.claude/skills/why-token
```

**OpenClaw:**
```bash
cp -r tls-why-token ~/.openclaw/skills/why-token
```

Then start a session and type `/why-token`.

---

## Available Skills

### `/why-token` — Live Now

The starting point. Answers the most important question before anything else: *why a token at all?*

- Forces founders to be honest about their motivation (liquidity, product-embedded, attention, exit)
- Routes pure meme launches to a quick checklist — this tool is for people who care about fundamentals
- Walks through value accrual, key parties, timeline, fundraise, and monetary policy basics
- Produces a structured document with two parts: **Decisions** (what you've resolved) and **Context** (supporting analysis)
- References real token launches with CoinMarketCap links so you can study what worked

---

## Coming Soon

These skills are on the roadmap. Each ships independently — you don't need to wait for the full stack.

### `/tokenomics` — Token Design

Deep dive into allocation, vesting schedules, and supply design. Takes the output from `/why-token` and turns it into actual numbers: how much goes to team, investors, ecosystem, treasury, and public. Vesting cliff and unlock schedules. Circulating supply projections over time.

### `/market-making` — Liquidity Strategy

How market making actually works. CEX vs DEX liquidity, how to evaluate and engage market makers, what terms to expect, and what the common traps are. Covers spread management, inventory risk, and how market maker incentives align (or don't) with yours.

### `/liquidity` — Live Liquidity Testing

Connects to on-chain data to test your liquidity assumptions against reality. Pool depth analysis, slippage modeling, and liquidity concentration metrics. Uses real market data to pressure-test your launch plan before you commit capital.

### `/launch-strategy` — Go-to-Market

The operational playbook from T-90 days to TGE and beyond. Coordinates all the parties from `/why-token` into an actual timeline: legal, exchange, market maker, community, and marketing — who does what, when, and what blocks what.

### `/mv-pq` — Token Valuation Framework

Applies the MV=PQ (Money Velocity × Price = Quantity) framework to your token design. Connects the qualitative decisions from earlier skills to quantitative modeling. How fast does your token circulate? What does that imply about sustainable price levels?

---

## Reference Token Database

TLS includes a curated database of real token launches across three categories:

- **Meme / Attention** — $DOGE, $PEPE, $FARTCOIN
- **Value Accrual** — $ETH, $BNB, $PUMP
- **Well-Executed Launches** — $KITE, $SOL, $TAO, $UNI

Each entry includes a case summary, key lesson, CoinMarketCap link, and tags for matching to your situation. The database lives in `data/reference-tokens.json` and is designed to be updated regularly.

A subscription API for expanded token references is planned for the future.

---

## For Deeper Work

This tool is free advisory — a public good for founders. If your situation gets complex (custom tokenomics design, multi-round fundraise structuring, exchange strategy), reach out for a 1:1 consultation:

**Chase Wang** — https://x.com/ChaseWang

---

## Stack

- TypeScript + Bun (CLI-first)
- Compatible with Claude Code and OpenClaw
- Web interface planned for future

## License

TBD
