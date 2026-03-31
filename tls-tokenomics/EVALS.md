# /tokenomics — Eval Cases

Autoresearch rubric, test personas, and round log for the `/tokenomics` skill.
Used for regression testing and future optimization rounds.

---

## Scoring Rubric

**Max score: 56 points** (4 personas × 7 criteria × 2 pts each)

| # | Criterion | What it measures |
|---|---|---|
| 1 | **Mode select clarity** | Does the skill open with a clear A/B choice and handle it correctly? |
| 2 | **Question discipline** | One question at a time, no form-dumping, no re-asking already-provided data? |
| 3 | **Mode B accuracy** | Does it load reference token data correctly, display it, allow edits? |
| 4 | **Value accrual bridge** | Does it detect /why-token context or ask demand-side questions correctly? |
| 5 | **Validation quality** | Does it catch all red flags (TGE%, liquidity, cliff, insider %, FDV)? |
| 6 | **Output completeness** | Does the confirm summary + Excel + chart generation work logically? |
| 7 | **Founder alignment** | Does it feel like an advisor? Tone, pacing, warnings feel human? |

---

## 4 Fixed Test Personas

### Persona 1: Mode B User — "Copycat"
**Prompt:**
> "I want to structure my tokenomics similar to Jupiter. Can we use that as a starting point? My project is a Solana DEX aggregator too but for meme tokens. $MEME, 5B total supply, TGE in 60 days."

**Expected behavior:**
- Skill detects Mode B from "similar to Jupiter" — goes directly to Mode B without asking
- Reads reference-tokens.json, loads $JUP tokenomics
- Extracts project name, ticker ($MEME), supply (5B) from opening message before asking
- Displays $JUP structure clearly with edits applied (5B instead of 10B)
- Asks what to change, then walks through validation
- Catches JUP-inherited team cliff of 24mo (still flags it as noteworthy — 2yr is unusually long)

### Persona 2: Mode A User — "Raw Founder"
**Prompt:**
> "I need to set up tokenomics for my DeFi lending protocol. Token is $LEND, 10B supply. Community 40%, team 20% with 1yr cliff 2yr vest, investors 15% with 6mo cliff 18mo vest, ecosystem 15%, liquidity 5%, treasury 5%. TGE in 3 months."

**Expected behavior:**
- Skill detects Mode A (no reference token mentioned)
- Extracts ALL provided data in one pass — no redundant questions
- Confirms in one line: "Got it — 6 categories, 100% allocated."
- Proceeds directly to Block 4 validation
- Flags: investor cliff < 12 months (6mo), FDV at assumed TGE price
- Does NOT ask for data already given

### Persona 3: Value Accrual Bridge — "Revenue-Driven"
**Prompt:**
> "I already ran /why-token. My protocol earns $2M/month in lending fees. We plan to use 40% for buybacks. Token price target is $1.50. No burns. Total supply 1B, 5 categories, all standard."
(Assume categories already collected)

**Expected behavior:**
- Skill detects /why-token context from "I already ran /why-token" — skips bridge question
- Extracts: revenue=$2M, buyback_pct=40, price=$1.50, burn=0
- Computes monthly buyback qty: ~533K tokens/mo ($2M × 40% / $1.50)
- Shows demand simulation in confirm summary: "~533K tokens/mo removed via buyback"
- Sets DEMAND_SINKS correctly in generated Python

### Persona 4: Edge Case — "Flag Magnet"
**Prompt:**
> "Token $FLAG, 100M supply. TGE next week. Team gets 60% fully liquid at TGE (0 cliff, 0 vest). Public sale 10% at TGE. Ecosystem 30% with 6mo cliff 24mo vest. No liquidity allocation. Launch price $0.10."

**Expected behavior:**
- Must surface ALL flags, one at a time, in order:
  1. **Check 0** (fully liquid insider): "Team 60% is fully liquid at TGE — no cliff, no vest. Major red flag for investor and exchange confidence."
  2. **Check 1** (high TGE unlock): "70% circulating at TGE. Heavy selling pressure risk."
  3. **Check 2** (no liquidity): "No dedicated liquidity allocation."
  4. **Check 3** (team cliff < 12mo): "Team cliff = 0 months."
  5. **Check 4** (insider > 40%): "Team alone is 60% — well above 40% threshold."
  6. **Check 5** (FDV): "FDV = $10M, launch MC = $7M (70% circulating × $0.10)."
- Must wait for explicit response between each flag

---

## Round Log

**Baseline version:** 2.0.0
**Final version:** 2.0.20
**Baseline score:** 49/56
**Final score:** 56/56
**Rounds kept:** 20/20 (0 reverts)

| Round | Version | Change | Score | Result |
|---|---|---|---|---|
| Baseline | 2.0.0 | — | 49/56 | — |
| 1 | 2.0.1 | Add extraction instruction to Block 3 — scan opening message for allocation data before re-asking | 50/56 | KEPT |
| 2 | 2.0.2 | Expand cliff check to ALL insider categories (team AND investors), not just team | 52/56 | KEPT |
| 3 | 2.0.3 | Add monthly buyback quantity computation formula to Block 5; require it in confirm summary | 54/56 | KEPT |
| 4 | 2.0.4 | Mode B extraction — pull name/ticker/supply/TGE from founder's opening message before asking | 55/56 | KEPT |
| 5 | 2.0.5 | Add check 0: "Fully liquid insider" flag for tge_pct=100, cliff=0, vest=0 on insider categories | 56/56 | KEPT |
| 6 | 2.0.6 | Auto-detect mode from opening message (reference token mention = Mode B, full allocation = Mode A extraction) | 56/56 | KEPT |
| 7 | 2.0.7 | Add explicit FDV/launch_mc formulas to validation check 5 | 56/56 | KEPT |
| 8 | 2.0.8 | Auto-detect /why-token context from opening message; skip bridge question if demand data already provided | 56/56 | KEPT |
| 9 | 2.0.9 | Make total % validation silent — only raise if total ≠ 100%, with specific resolution prompt | 56/56 | KEPT |
| 10 | 2.0.10 | Add "0% TGE, no cliff, no vest = Permanently locked" case to Vesting Description Generator | 56/56 | KEPT |
| 11 | 2.0.11 | Auto-fill purpose for standard category names without asking | 56/56 | KEPT |
| 12 | 2.0.12 | Show single running total for bulk-extracted categories instead of one per category | 56/56 | KEPT |
| 13 | 2.0.13 | Validation notes in output summary explicitly sourced from Block 4 results | 56/56 | KEPT |
| 14 | 2.0.14 | Make Mode B token list dynamic from JSON — no hardcoded token names | 56/56 | KEPT |
| 15 | 2.0.15 | Add fallback behavior when requested reference token is not in the JSON file | 56/56 | KEPT |
| 16 | 2.0.16 | Max supply question only asked for inflationary protocols; default = total supply silently | 56/56 | KEPT |
| 17 | 2.0.17 | Cumulative flag tone rule: after 3+ flags all "intentional," add one candid closing note | 56/56 | KEPT |
| 18 | 2.0.18 | TGE% input ambiguity: if founder gives token count instead of %, compute tge_pct automatically | 56/56 | KEPT |
| 19 | 2.0.19 | Demand simulation confirm summary shows "(Not modeled)" when all demand inputs are 0 | 56/56 | KEPT |
| 20 | 2.0.20 | Add "Scan before you speak" as first Hard Rule — consolidates all auto-detect behaviors | 56/56 | KEPT |

---

## Score Progression

```
49 → 50 → 52 → 54 → 55 → 56 → 56 (×15 more rounds)
```

Biggest jumps:
- **+2** Round 2: expanded insider cliff check (was only catching team, missed investors)
- **+2** Round 3: buyback qty computation (Persona 3 was failing confirm summary check)
- **+1** Round 4: Mode B opening message extraction (Persona 1 was still asking for ticker)
- **+1** Round 5: fully liquid insider check 0 (Persona 4 flag ordering was wrong)

---

## Next Steps

- Rounds 1-5 moved the needle. Rounds 6-20 hardened robustness at perfect score.
- To improve further: need harder adversarial personas (e.g., non-English founder, mixed-up field order, impossible allocations summing to >100%) or real session feedback from actual founders.
- Consider adding Persona 5: "Migrator" — founder converting from an existing token to a new one with burn mechanics.
