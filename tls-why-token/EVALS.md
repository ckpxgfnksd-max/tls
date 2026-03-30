# /why-token — Eval Suite

Used for autoresearch optimization. Run these evals after any change to SKILL.md
to verify score does not regress.

**Scoring:** 7 criteria × 2 pts max = 14 pts per session. 4 personas = 56 pts max per round.

---

## Rubric

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Correct routing | Wrong path taken | Partial (hesitated or recovered) | Perfect — right path on first branch |
| Force before teach | Lectured without asking first | Mixed (asked, then taught too early) | Asked first, taught only when gap was exposed |
| Surfaced gaps | Named nothing founder didn't already know | Named some missing pieces | Named exactly what was missing and why it matters |
| Specific mechanism extracted | Accepted vague answer | Pushed once, accepted second vague | Pushed until mechanism was concrete and specific |
| CMC link included | No link when referencing a token | Mentioned token without link | Included CMC link correctly formatted |
| Output doc complete | Missing sections | Some sections present | All 9 sections present and populated |
| Handoff triggered correctly | Fired when founder was unready (wrong) | Fired late or too early | Fired exactly when complexity exceeded general advisory |

---

## Test Personas

Use these exact personas every round. Same input = comparable scores across rounds.

---

### Persona A — Pure Meme (Quick Exit Test)

**Input:**
> "I want to launch a meme token for my community. Just vibes, no utility."

**Expected behavior:**
- Q1 routes to Quick Exit (marketing/attention only)
- Meme checklist delivered with CMC links for $DOGE, $PEPE, $FARTCOIN
- Session ends — Q2 through Q6 are NOT run
- No output document generated

**Pass criteria:** Score 12–14. Fail if full session is run, or if checklist is missing CMC links.

---

### Persona B — Vague DeFi (Force-Before-Teach Test)

**Input:**
> "I'm building a DeFi protocol and want a token. It'll be valuable because the protocol grows."

**Follow-up (if skill teaches without pushing):**
> "Yeah, I guess I meant the token goes up when more users join."

**Expected behavior:**
- Q1 → full session (product-embedded motivation)
- Q2: skill asks "how does value flow?" — does NOT lecture first
- Founder gives vague first answer → skill pushes, does NOT accept
- Founder gives vague second answer → skill explicitly does not accept, provides $BNB example, re-asks
- Only after founder articulates a specific mechanism does skill move on

**Pass criteria:** Score 12–14. Fail if skill teaches Q2 framework before founder struggles, or if vague second answer is accepted.

---

### Persona C — Sophisticated Fundraise (Q5 Public Sale Test)

**Input:**
> "We're building a DEX aggregator. Token captures 40% of protocol fees via weekly distribution to stakers. We've done a seed round ($2M at $10M valuation), planning a strategic round at $20M, and considering a public sale before TGE."

**Expected behavior:**
- Q1 → full session (product-embedded)
- Q2: specific mechanism already stated → skill accepts, moves on (does NOT re-push unnecessarily)
- Q5: skill correctly explains public sale = additive allocation, NOT a reshuffle of seed/strategic terms
- Q5: skill flags that seed and strategic round terms are locked per round
- Handoff CTA fires at fundraise structuring complexity (multiple rounds + public sale = project-specific)

**Pass criteria:** Score 12–14. Fail if public sale is described as reshuffling existing investor allocations, or if handoff fires before Q5.

---

### Persona D — Gate Logic (Unreadiness Test)

**Input:**
> "I want to launch a token for my app. I'm not sure how value flows into it. I've thought about it but can't pin it down. It's not a meme coin — I want real fundamentals."

**Follow-up when pushed:**
> "I don't know. Maybe governance? But I'm not sure that creates value either."

**Expected behavior:**
- Q1 → full session (product-embedded motivation stated)
- Q2: skill forces — asks for mechanism, does NOT lecture first
- Founder admits they can't articulate it → skill pushes once more
- Founder still can't articulate → gate logic fires: "not ready yet" — clear statement, specific instruction to come back when mechanism is defined
- Handoff CTA does NOT fire here (gate ≠ handoff — founder is unready, not complex)

**Pass criteria:** Score 12–14. Fail if gate logic fires too early (before two genuine pushes), if handoff CTA fires instead of gate, or if "likely not ready" (hedged) wording is used instead of "not ready yet" (direct).

---

## Baseline Scores

| Version | Round | Score | Notes |
|---|---|---|---|
| v1.0.0 (V0.1.1) | 0 | 50/56 | Initial baseline |
| v1.0.1 (V0.1.2) | 15 | 55/56 | Post-autoresearch convergence |

---

## Running a New Autoresearch Pass

Before running more rounds, update the personas if real founder sessions have
revealed new failure modes. A persona that always scores 14/14 is no longer
useful — replace it with a harder variant.

**Suggested next persona upgrades (post real-session feedback):**
- Founder who argues back: "but Uniswap didn't do it that way"
- Founder who answers every question with "it depends"
- Founder who jumps straight to Q5 without completing Q1
