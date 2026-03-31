---
name: tokenomics
description: |
  Token allocation and vesting schedule builder. Walks founders through
  allocation design, vesting schedules, and generates a professional Excel
  token release schedule with supply/demand simulation chart.
  Use when a founder says "tokenomics", "allocation", "vesting schedule",
  "token release", "how do I structure my token supply", or after /why-token.
version: 2.0.20
tags: ["token", "tokenomics", "vesting", "allocation", "excel", "TGE", "schedule", "chart"]
metadata:
  openclaw:
    emoji: "📊"
    alwaysApplicable: false
---

# /tokenomics — Token Allocation & Vesting Schedule Builder

Created by **Chase Wang** (https://x.com/ChaseWang) — ex-Binance listing team,
reviewed over 1,000 projects, launched ~100 tokens in 2025.

This skill picks up where `/why-token` leaves off. You have a token thesis.
Now design the allocation and vesting that makes it credible.

**What this produces:**
1. A professional Excel token release schedule (`tokenomics-{TICKER}-{DATE}.xlsx`)
   ready for exchanges, legal counsel, and investors.
2. A supply/demand simulation chart embedded in the same workbook — gross token
   releases vs. net circulating supply after buybacks and burns.

---

## Hard Rules

- **Scan before you speak** — always read the founder's opening message for
  mode signals (reference token = Mode B), allocation data, demand inputs,
  and /why-token context before asking any questions. Extract what's there.
- One question at a time — don't dump a form at the founder
- Validate as you go — catch errors before generation, not after
- Warn on red flags — don't silently accept bad vesting designs
- Never generate until all required inputs are collected and confirmed
- Do NOT ask for information that can be computed
- Do NOT re-ask for information already provided — extract from context,
  confirm in one line, then ask ONE missing field at a time

---

## Session Flow

### Mode Select (Opening — Always First)

Ask exactly this before anything else:

> "How do you want to start?
> **A** — Build from scratch (I'll walk you through every field)
> **B** — Start from a real token's structure and modify it
>
> If B: tell me the ticker and I'll load their allocation as your starting point."

**Auto-detect before asking:** If the founder's opening message already
mentions a reference token ("similar to X", "like $JUP", "based on Uniswap"),
skip the mode select question and go directly to Mode B, confirming:
> "Looks like you want to start from $[X]'s structure — jumping to Mode B."
Similarly, if they provide a full allocation breakdown in their first message,
skip to Mode A Block 3 extraction.

Otherwise wait for response. Then branch:
- **A** → Go to Block 1: Project Basics
- **B** → Go to Mode B: Historical Reference Loader

---

### Mode B: Historical Reference Loader

1. Use the Read tool to load:
   `/Users/chasewang/.claude/skills/why-token/data/reference-tokens.json`

2. Find tokens where `tokenomics.type` is `"structured"` or `"low-confidence"`.
   Display a DYNAMIC numbered list built from the JSON file — do NOT
   hardcode any token names. Format each entry as:
   `[N]. $[ticker] — [name] · [chain] · [type label] [[confidence] confidence]`
   where type label = "structured" → "structured [high confidence]",
   "low-confidence" → "partial data [low confidence]"

   > "Available reference tokens:
   > [dynamically generated list]
   >
   > Which token do you want to start from? (number or ticker)"

3. If the founder named a token NOT in the JSON file:
   > "$[X] isn't in my reference library yet. Here are the tokens I have
   > available — want to pick the closest one, or start from scratch (Mode A)?"
   Show the dynamic list and wait for response.

   After user selects, load that token's `tokenomics` block. If
   `confidence: "low"`, warn upfront:
   > "⚠️ Note: [TOKEN]'s tokenomics aren't fully documented publicly.
   > The data below includes estimates — treat it as a starting template,
   > not ground truth. Verify any category before sharing with investors."

4. Display the loaded structure:

   > "Here's $[TICKER]'s tokenomics as your starting point:
   >
   > Total Supply: [X]
   > TGE Date: [date]
   >
   > | # | Category | % | TGE% | Cliff | Vest |
   > |---|---|---|---|---|---|
   > | 1 | [name] | [pct]% | [tge]% | [cliff]mo | [vest]mo |
   > ...
   >
   > What do you want to change? Or say 'keep as-is' to proceed with these values."

5. Apply any changes the founder specifies. Re-display the updated table.
   When they confirm, pre-fill all session variables from the loaded data
   and skip to: **Ask for Project Basics** (name, ticker, total supply,
   TGE date, vest day) — but first extract any of these already provided
   in the founder's opening message. Only ask for what is missing. Confirm
   extracted values in one line before proceeding.
   Then jump to **Block 4: Smart Validation**.

---

### Block 1: Project Basics (Mode A)

Collect in order, one at a time:

1. **Project name** — "What's the project name?"
2. **Token ticker** — "What's your token ticker? (e.g., $TOKEN)"
3. **TGE date** — "When is your TGE? (DD.MM.YYYY or YYYY-MM-DD)"
4. **Vesting day** — "On which day of each month do tokens vest?
   (e.g., 1st, 15th, last day of month. Default: 1st)"

---

### Block 2: Supply Design (Mode A)

5. **Total supply** — "What is your total token supply?"

6. **Max supply** — Only ask this if the founder's message mentions
   staking rewards, inflation, minting, or an uncapped supply model.
   Otherwise default max_supply = total_supply silently and confirm in
   the Block 6 summary as "Max Supply: [X] (same as total supply)".
   If needed: "Is your max supply the same as total supply, or does
   your protocol have a hard cap that differs? (Most projects: same number.
   Inflationary protocols: max supply may be uncapped or higher)"

   **Teach if they don't know the difference:**
   > - **Total supply** = tokens created minus tokens burned to date
   > - **Max supply** = hard cap on tokens that will ever exist
   > For most fixed-supply tokens these are the same number.

---

### Block 3: Allocation Categories (Mode A)

**Before asking anything:** Scan the founder's message for allocation data
already provided (category names, percentages, cliffs, vesting periods).
Extract and confirm in one line: "Got it — I see [N] categories: [list].
Let me validate these." Then skip directly to those specific fields that
are missing, rather than re-asking what was already given.

7. **Number of categories** — "How many allocation categories does your
   token have? (Max 9. Typical: 5-8)"

   Common categories for reference (don't suggest unless asked):
   Public Sale, Private Sale, Seed Round, Strategic Round, Team, Advisors,
   Investors, Ecosystem Fund, Community, Liquidity/Market Making,
   Foundation/Treasury, Marketing, Reserve

   For each category (repeat N times, one at a time):

   **a. Label** — "Category [N] name?"

   **b. Purpose** — "One sentence: what is this allocation for?"
      Self-explanatory categories (Team, Community, Investors, Ecosystem,
      Liquidity, Treasury, Advisors, Public Sale, etc.) — auto-fill the
      purpose with a standard one-line description and include it in the
      Block 6 confirm summary without asking. Only ask if the category name
      is ambiguous or non-standard.

   **c. Percentage** — "What % of total supply goes to [label]?"
      Show running total after each answer. If bulk-extracting from the
      founder's opening message, show a single total after all categories
      are extracted rather than one per category.

   **d. TGE unlock %** — "What % of [label]'s allocation unlocks at TGE?"
      (This is a percentage of the category's allocation, not a token count.
      If founder gives a token count, compute: tge_pct = tokens ÷ category_tokens × 100)

   **e. Cliff** — "Is there a cliff period? (Months of 0 releases after TGE.
      0 = no cliff)"
      Note if team/investor cliff < 12 months.

   **f. Linear vest duration** — "After the cliff, how many months does
      [label] vest linearly? (0 = no linear vest)"

   **g. Token price** — "What is the token price for [label]? ($USD.
      N/A if not applicable)"
      If price given, also ask:
   **h. Amount raised** — "How much did you raise in this round? ($USD.
      N/A if not applicable)"
      Valuation = price × token_amount. Do NOT ask for valuation.

   After all categories: silently compute total %. If it equals 100%,
   proceed without comment. Only raise an issue if total ≠ 100%:
   > "Your allocations sum to [X]% — need to adjust to reach 100%.
   > Which category should absorb the difference?"

---

### Block 4: Smart Validation

After categories are collected (both modes), surface red flags one at a time.
Require explicit acknowledgement before proceeding.

**Red Flag Checks:**

0. **Fully liquid insider (tge_pct=100, cliff=0, vest=0 on any insider category):**
   This is the most severe flag — check BEFORE the aggregate TGE unlock check.
   > "Your [label] allocation is fully liquid at TGE — 100% unlocks on day one
   > with no cliff and no vesting. This is a near-automatic disqualifier for
   > major exchange listings and signals to investors that insiders can dump
   > immediately. Is this a mistake or intentional?"
   Wait for response before continuing.

1. **High TGE unlock (>50% of total supply liquid at TGE):**
   > "Your TGE circulating supply is [X]% of total supply. Heavy early selling
   > pressure is one of the most common ways token launches fail in the first
   > 72 hours. Is this intentional?"

2. **No liquidity allocation:**
   > "I don't see a dedicated liquidity or market-making allocation.
   > Without committed liquidity at launch, your token will have wide spreads
   > and poor price discovery. Standard is 3-10% for liquidity. Covered another way?"

3. **Insider cliff < 12 months (team OR investors):**
   Check ALL insider categories (team, founders, investors, seed, private,
   strategic, advisors, angels, VCs). Flag any with cliff < 12 months.
   > "Your [label] allocation has a [X]-month cliff. Major exchanges (Binance,
   > OKX, Coinbase) treat a sub-12-month cliff on insider allocations as a
   > credibility red flag — this will come up in listing due diligence.
   > Intentional choice?"
   Issue one flag per offending category, wait for response on each.

4. **Team + insider allocation > 40%:**
   Count as "insider": team, founders, core contributors, employees, investors,
   seed, private, strategic, advisors, angels, VCs, early backers.
   Exclude: public sale, ecosystem, community, liquidity, treasury, foundation, marketing.
   > "Team + investor + advisor allocations total [X]% — above 40% is often
   > flagged in exchange due diligence as too insider-heavy. Worth revisiting?"

5. **Implied FDV check (if any price provided):**
   Compute:
   - FDV = launch_price × total_supply
   - circ_at_tge = sum of (category_pct × tge_pct) across all categories
   - launch_mc = launch_price × (circ_at_tge / 100) × total_supply
   > "At your TGE price of $[X], your FDV is $[Y]. Circulating at TGE is [Z]%,
   > implying a launch market cap of $[W]. Does that match your expectations?"

For each flag: wait for response before proceeding. If they want to adjust,
loop back to relevant category, then restart Block 4 from check #1.

**Cumulative flag tone:** If 3+ flags triggered and all were "intentional",
add a candid closing note after the last flag:
> "Just want to flag that this design has [N] significant red flags that
> will come up in exchange due diligence. You can proceed — just go in
> with eyes open. Want to revisit any of them before we generate?"
This is said ONCE, at the end. Do not repeat it per flag.

---

### Block 5: Value Accrual Bridge

After validation, collect demand-side inputs for the supply/demand chart.

**Auto-detect before asking:** If the founder's message already mentions
/why-token, revenue figures, buyback %, or burn mechanics, extract those
values directly without asking the bridge question. Confirm in one line:
> "Picking up your demand data from /why-token: [summary of extracted values]."

Otherwise ask:
> "Now for the chart — I'll simulate how your token release schedule
> interacts with demand-side forces like buybacks and burns.
>
> Did you run /why-token before this? If yes, share your value accrual
> type and any numbers you have. If no, I'll ask a few quick questions."

**If they share /why-token output or provide demand data, extract:**
- Monthly protocol revenue (USD)
- % of revenue used for token buyback
- Token price assumption for buyback quantity calculation
- Any fixed burn per month (tokens)

**If no /why-token context, ask in order:**

a. "Does your protocol generate revenue? If yes, roughly how much per month
   in USD? (Estimate is fine — this is for the simulation, not the spreadsheet)"

b. "What % of that revenue is used to buy back tokens? (0 if none)"

c. "What token price are you assuming for the buyback calculation?
   (Use your TGE price or your target price — this affects how many tokens
   get bought back per dollar)"

d. "Are there any burn mechanics that remove tokens from circulation on a
   fixed schedule? (e.g., 1% of supply per year. Say 'none' if not applicable)"

**If they explicitly skip this block** (say "skip" or "no buybacks/burns"):
Set all demand inputs to 0 — chart will show gross supply only with a note.

Store as:
```
DEMAND_SINKS = {
  "revenue_monthly_usd": [value or 0],
  "buyback_pct": [value or 0],
  "token_price_assumption": [value or 0],
  "burn_monthly_tokens": [value or 0],
  "note": "[description of mechanism, or 'Not modeled']"
}
```

**Immediately after collecting demand inputs, compute and store:**
- Monthly buyback qty = (revenue_monthly_usd × buyback_pct/100) ÷ token_price_assumption
  (set to 0 if token_price_assumption = 0)
- This computed value must appear in the Block 6 confirm summary as
  "Monthly buyback qty: ~[N] tokens"

---

### Block 6: Confirm & Generate

Show a clean summary table:

```
PROJECT: [name] ($TICKER)
TGE: [date] | Vesting day: [day] of each month
Total Supply: [number] | Max Supply: [number]

ALLOCATIONS:
#  Label              %      TGE%   Cliff  Vest    Price
1  [label]           XX%    XX%    XX mo  XX mo   $X.XXX
...
Total:              100%

CIRCULATING AT TGE: [X tokens] ([Y]% of total supply)
LAUNCH MARKET CAP:  $[W] (if price provided)
FULLY DILUTED VALUATION: $[Z] (if price provided)

DEMAND SIMULATION:
{If all demand inputs are 0: "(Not modeled — chart shows gross supply only)"}
{If demand inputs provided:
Revenue/mo: $[X] | Buyback: [Y]% | Price assumption: $[Z]
Monthly buyback qty: ~[N] tokens | Fixed burn: [B] tokens/mo}
```

Ask: "Does this look correct? Type 'yes' to generate, or tell me what to change."

---

### Block 7: Generate Excel

Once confirmed, generate using Python/openpyxl + matplotlib.

**Output filename:** `tokenomics-{TICKER}-{YYYYMMDD}.xlsx`
**Save location:** Current working directory

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from datetime import datetime
import calendar, io, math
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── DATA (filled from session) ─────────────────────────────────────────
PROJECT_NAME   = "{project_name}"
TICKER         = "{ticker}"
TGE_DATE       = datetime({tge_year}, {tge_month}, {tge_day})
VEST_DAY       = "{vest_day}"
REPORT_DATE    = datetime.today()
MAX_SUPPLY     = {max_supply}
TOTAL_SUPPLY   = {total_supply}

# Each category: label, purpose, vesting_desc, pct, tge_pct, cliff, vest,
#                price (float or "N/A"), raised (float or None),
#                valuation (float or None)
CATEGORIES = {categories_list}

# Demand sinks for supply/demand simulation chart
DEMAND_SINKS = {demand_sinks}
# Format:
# {
#   "revenue_monthly_usd": 5_000_000,
#   "buyback_pct": 50,                  # percentage (0-100)
#   "token_price_assumption": 2.50,
#   "burn_monthly_tokens": 0,
#   "note": "50% of $5M/mo revenue used for buyback at $2.50/token"
# }
# If no demand modeling, set all numeric values to 0.
# ───────────────────────────────────────────────────────────────────────

# ── STYLE HELPERS ──────────────────────────────────────────────────────
BLUE        = "FF0000FF"
BLACK       = "FF000000"
BOLD_FILL   = PatternFill("solid", fgColor="FFD9D9D9")
HEADER_FILL = PatternFill("solid", fgColor="FF1F4E79")
WHITE_FILL  = PatternFill("solid", fgColor="FFFFFFFF")

thin = Side(style='thin', color="FF000000")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

def input_font(bold=False):
    return Font(name="Arial", color=BLUE, bold=bold, size=10)

def formula_font(bold=False):
    return Font(name="Arial", color=BLACK, bold=bold, size=10)

def header_font():
    return Font(name="Arial", color="FFFFFFFF", bold=True, size=10)

def label_font():
    return Font(name="Arial", color=BLACK, bold=True, size=10)

def style_input(cell, bold=False):
    cell.font = input_font(bold)
    cell.border = BORDER

def style_formula(cell, bold=False):
    cell.font = formula_font(bold)
    cell.border = BORDER

def style_header(cell):
    cell.font = header_font()
    cell.fill = HEADER_FILL
    cell.border = BORDER
    cell.alignment = Alignment(horizontal="center", vertical="center",
                                wrap_text=True)

def style_label(cell):
    cell.font = label_font()
    cell.border = BORDER

def fmt_num(cell):
    cell.number_format = '" "* #,##0" ";" "* (#,##0);" "* "- "'

def fmt_pct_total(cell):
    cell.number_format = '0.00%'

def fmt_price(cell):
    cell.number_format = '"[$$-409]* #,##0.000 ";"[$$-409]* (#,##0.000);"[$$-409]* "-"??.0 "'

def fmt_usd(cell):
    cell.number_format = '"[$$-409]* #,##0.00 ";"[$$-409]* (#,##0.00);"[$$-409]* "-"?? "'

# ── VESTING CALC ───────────────────────────────────────────────────────
def calc_schedule(total, tge_pct, cliff, vest, max_months):
    """Index 0 = TGE release, 1..N = monthly releases.
    Cliff = lockup (zero releases). Linear vest begins AFTER cliff."""
    s = [0.0] * (max_months + 1)
    tge_amt = total * tge_pct / 100
    remaining = total - tge_amt
    s[0] = tge_amt
    if remaining <= 0 or (cliff == 0 and vest == 0):
        return s
    if vest == 0:
        if cliff <= max_months:
            s[cliff] += remaining
    else:
        monthly = remaining / vest
        for m in range(cliff + 1, cliff + vest + 1):
            if m <= max_months:
                s[m] += monthly
    return s

def calc_demand_sinks(sinks, max_months):
    """Returns tokens removed from circulation per month (buyback + burn).
    Month 0 (TGE) has no sinks."""
    result = [0.0] * (max_months + 1)
    revenue = sinks.get("revenue_monthly_usd", 0)
    buyback_pct = sinks.get("buyback_pct", 0) / 100
    price = sinks.get("token_price_assumption", 0)
    burn = sinks.get("burn_monthly_tokens", 0)
    for m in range(1, max_months + 1):
        buyback_qty = (revenue * buyback_pct / price) if price > 0 else 0
        result[m] = buyback_qty + burn
    return result

# ── DATE HELPERS ───────────────────────────────────────────────────────
def month_end_date(base_date, months_offset):
    y = base_date.year + (base_date.month - 1 + months_offset) // 12
    m = (base_date.month - 1 + months_offset) % 12 + 1
    d = calendar.monthrange(y, m)[1]
    return datetime(y, m, d)

# ── PRE-COMPUTE ────────────────────────────────────────────────────────
max_months = 0
for cat in CATEGORIES:
    horizon = cat["cliff"] + cat["vest"]
    if horizon > max_months:
        max_months = horizon
max_months = max(max_months, 48)

schedules = []
for cat in CATEGORIES:
    total_tokens = TOTAL_SUPPLY * cat["pct"] / 100
    s = calc_schedule(total_tokens, cat["tge_pct"], cat["cliff"],
                      cat["vest"], max_months)
    schedules.append(s)

months = list(range(max_months + 1))
gross = [sum(sched[m] for sched in schedules) for m in months]
gross_cum = [sum(gross[:m+1]) for m in months]

sink_schedule = calc_demand_sinks(DEMAND_SINKS, max_months)
sink_cum = [sum(sink_schedule[:m+1]) for m in months]
net_circ_cum = [max(0.0, gross_cum[m] - sink_cum[m]) for m in months]

# ── BUILD WORKBOOK ─────────────────────────────────────────────────────
wb = Workbook()
ws = wb.active
ws.title = "3-1. Token Allocation Breakdown"

# Column widths
ws.column_dimensions["A"].width = 6.5
ws.column_dimensions["B"].width = 22
ws.column_dimensions["C"].width = 19.5
for col in ["D","E","F","G","H","I","J","K","L"]:
    ws.column_dimensions[col].width = 16
ws.column_dimensions["M"].width = 20

# ── NOTES (rows 1-7) ───────────────────────────────────────────────────
notes = [
    "*Note",
    "- Fill in all the blue cells. Do not touch cells with formulas.",
    "- Up to 9 allocation categories (columns D–L).",
    "- Token Release Schedule auto-calculates from allocations above.",
    "- Circulating supply = cumulative tokens unlocked month-by-month.",
    "- All token amounts in absolute numbers (not thousands or millions).",
]
for i, note in enumerate(notes, 1):
    cell = ws.cell(row=i, column=2, value=note)
    cell.font = Font(name="Arial", bold=(i == 1), size=9,
                     color="FF595959" if i > 1 else BLACK)

# ── PROJECT METADATA (rows 9-17) ──────────────────────────────────────
circ_at_tge = sum(s[0] for s in schedules)

meta = [
    (9,  "Date of Report",                REPORT_DATE.strftime("%d.%m.%Y"), True),
    (10, "Project Name",                   PROJECT_NAME,                     True),
    (11, "Token Ticker",                   f"${TICKER.lstrip('$')}",         True),
    (12, "Max Supply",                     MAX_SUPPLY,                       True),
    (13, "Total Supply",                   TOTAL_SUPPLY,                     True),
    (14, "Circulating Supply at Genesis",  None,                             False),
    (15, "TGE",                            TGE_DATE,                         True),
    (16, "Date of token vested each month", VEST_DAY,                        True),
]

for row, label, val, is_input in meta:
    lbl = ws.cell(row=row, column=2, value=label)
    style_label(lbl)
    if row == 14:
        val_cell = ws.cell(row=row, column=3, value=circ_at_tge)
        style_formula(val_cell)
    else:
        val_cell = ws.cell(row=row, column=3, value=val)
        if is_input:
            style_input(val_cell)
        else:
            style_formula(val_cell)
    if row == 12:
        ws.cell(row=row, column=4,
                value="* The maximum amount of coins that will ever exist").font = \
            Font(name="Arial", size=9, italic=True, color="FF595959")
    if row == 13:
        ws.cell(row=row, column=4,
                value="* Total supply = Total coins created - coins that have been burned").font = \
            Font(name="Arial", size=9, italic=True, color="FF595959")
    if isinstance(val, datetime):
        val_cell.number_format = "DD.MM.YYYY"
    elif isinstance(val, (int, float)) and row in (12, 13):
        val_cell.number_format = '#,##0'

# ── ALLOCATION TABLE (rows 18-27) ─────────────────────────────────────
n_cats = len(CATEGORIES)
cat_cols = [get_column_letter(4 + i) for i in range(n_cats)]
total_col = get_column_letter(4 + n_cats)

# Row 18: header
ws.cell(row=18, column=2, value="Allocation No.").font = label_font()
for i in range(n_cats):
    c = ws.cell(row=18, column=4+i, value=i+1)
    style_header(c)
ws.cell(row=18, column=4+n_cats, value="Total").font = Font(
    name="Arial", bold=True, color=BLACK, size=10)

# Rows 19-21: Label, Purpose, Vesting Schedule
row_labels = [(19, "Label"), (20, "Purpose of Allocation"),
              (21, "Vesting Schedule")]
cat_fields = ["label", "purpose", "vesting_desc"]

for (row, lbl), field in zip(row_labels, cat_fields):
    l = ws.cell(row=row, column=2, value=lbl)
    style_label(l)
    ws.merge_cells(f"B{row}:C{row}")
    for i, cat in enumerate(CATEGORIES):
        val = cat.get(field, "")
        c = ws.cell(row=row, column=4+i, value=val)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        style_input(c)

# Row 22: Token Amount header
ws.cell(row=22, column=2, value="Token Amount").font = label_font()
ws.merge_cells("B22:C22")

# Row 23: Checker
ws.cell(row=23, column=2, value="Checker").font = label_font()
ws.merge_cells("B23:C23")
for i, cat in enumerate(CATEGORIES):
    token_amt = round(TOTAL_SUPPLY * cat["pct"] / 100)
    c = ws.cell(row=23, column=4+i, value=token_amt)
    style_formula(c)
    fmt_num(c)
tc = ws.cell(row=23, column=4+n_cats,
             value=f"=SUM({cat_cols[0]}23:{cat_cols[-1]}23)")
style_formula(tc, bold=True)
fmt_num(tc)

# Row 24: % of Total Supply
ws.cell(row=24, column=2, value="% of Total Supply").font = label_font()
ws.merge_cells("B24:C24")
for i, cat in enumerate(CATEGORIES):
    c = ws.cell(row=24, column=4+i, value=cat["pct"])
    style_input(c)
    c.number_format = "General"
tc = ws.cell(row=24, column=4+n_cats,
             value=f"=SUM({cat_cols[0]}24:{cat_cols[-1]}24)/100")
style_formula(tc, bold=True)
fmt_pct_total(tc)

# Row 25: Token Price
ws.cell(row=25, column=2, value="Token Price ($)").font = label_font()
ws.merge_cells("B25:C25")
for i, cat in enumerate(CATEGORIES):
    price = cat.get("price", "N/A")
    c = ws.cell(row=25, column=4+i, value=price)
    style_input(c, bold=True)
    if isinstance(price, (int, float)):
        fmt_price(c)

# Row 26: Amount Raised
ws.cell(row=26, column=2, value="Amount Raised ($)").font = label_font()
ws.merge_cells("B26:C26")
for i, cat in enumerate(CATEGORIES):
    raised = cat.get("raised", "")
    c = ws.cell(row=26, column=4+i, value=raised if raised else None)
    style_input(c, bold=True)
    if isinstance(raised, (int, float)):
        fmt_usd(c)
tc = ws.cell(row=26, column=4+n_cats,
             value=f"=SUM({cat_cols[0]}26:{cat_cols[-1]}26)")
style_formula(tc, bold=True)
fmt_usd(tc)

# Row 27: Valuation
ws.cell(row=27, column=2, value="Valuation ($)").font = label_font()
ws.merge_cells("B27:C27")
for i, cat in enumerate(CATEGORIES):
    val = cat.get("valuation", "")
    c = ws.cell(row=27, column=4+i, value=val if val else None)
    style_input(c, bold=True)
    if isinstance(val, (int, float)):
        fmt_usd(c)

# ── VESTING SCHEDULE SECTION ───────────────────────────────────────────
header_row = 29
ws.cell(row=header_row, column=2, value="Token Release Schedule").font = \
    Font(name="Arial", bold=True, size=11, color=BLACK)
ws.merge_cells(f"B{header_row}:M{header_row}")

hdr = 30
ws.cell(row=hdr, column=2, value="Timeline").font = label_font()
ws.cell(row=hdr, column=3, value="Date").font = label_font()
for i, cat in enumerate(CATEGORIES):
    c = ws.cell(row=hdr, column=4+i, value=cat["label"])
    style_header(c)
circ_hdr = ws.cell(row=hdr, column=4+n_cats, value="Circulating Supply")
style_header(circ_hdr)

# ── MONTHLY RELEASE ROWS ───────────────────────────────────────────────
data_start = 31

for month_idx in range(max_months + 1):
    row = data_start + month_idx
    label = "TGE" if month_idx == 0 else f"{month_idx}M"
    date_formula = "=C15" if month_idx == 0 else f"=EOMONTH(C{row-1},1)"

    ws.cell(row=row, column=2, value=label).font = formula_font(bold=True)
    date_cell = ws.cell(row=row, column=3, value=date_formula)
    date_cell.number_format = "DD.MM.YYYY"
    style_formula(date_cell)

    for i, (cat, sched) in enumerate(zip(CATEGORIES, schedules)):
        release = sched[month_idx] if month_idx < len(sched) else 0
        c = ws.cell(row=row, column=4+i,
                    value=round(release) if release != 0 else None)
        style_formula(c)
        fmt_num(c)

    circ_col = 4 + n_cats
    circ_col_letter = get_column_letter(circ_col)
    if month_idx == 0:
        circ_formula = f"=SUM({cat_cols[0]}{row}:{cat_cols[-1]}{row})"
    else:
        circ_formula = (f"=SUM({cat_cols[0]}{row}:{cat_cols[-1]}{row})"
                        f"+{circ_col_letter}{row-1}")
    circ_cell = ws.cell(row=row, column=circ_col, value=circ_formula)
    style_formula(circ_cell, bold=True)
    fmt_num(circ_cell)

ws.freeze_panes = ws.cell(row=data_start, column=4)

# ── CHART SHEET ────────────────────────────────────────────────────────
has_demand = (DEMAND_SINKS.get("revenue_monthly_usd", 0) > 0 or
              DEMAND_SINKS.get("burn_monthly_tokens", 0) > 0)

palette = ["#4472C4", "#ED7D31", "#A9D18E", "#FFC000", "#9E480E",
           "#5A5A5A", "#7030A0", "#00B0F0", "#FF0000"]

fig, ax1 = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#FAFAFA')
ax1.set_facecolor('#FAFAFA')

# Stacked bar: monthly unlocks per category
bottom = [0.0] * len(months)
for i, (cat, sched) in enumerate(zip(CATEGORIES, schedules)):
    vals = [sched[m] / 1e6 for m in months]
    ax1.bar(months, vals, bottom=bottom,
            color=palette[i % len(palette)],
            label=cat["label"], width=0.85, linewidth=0)
    bottom = [bottom[m] + vals[m] for m in range(len(months))]

ax1.set_xlabel("Month Post-TGE", fontsize=11)
ax1.set_ylabel("Monthly Unlocks (M tokens)", fontsize=11)
ax1.set_xlim(-0.5, max_months + 0.5)
ax1.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{x:.1f}M"))
ax1.tick_params(axis='both', labelsize=10)

# Right axis: cumulative lines
ax2 = ax1.twinx()
ax2.plot(months, [v / 1e6 for v in gross_cum],
         color="#595959", linewidth=1.6, linestyle="--",
         label="Gross Circulating", zorder=4)
if has_demand:
    ax2.plot(months, [v / 1e6 for v in net_circ_cum],
             color="#C00000", linewidth=2.2,
             label=f"Net Circulating (after {DEMAND_SINKS.get('note', 'buybacks/burns')})",
             zorder=5)
ax2.set_ylabel("Cumulative Circulating (M tokens)", fontsize=11)
ax2.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{x:.0f}M"))
ax2.tick_params(axis='y', labelsize=10)

# Legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
fig.legend(h1 + h2, l1 + l2,
           loc="upper left", bbox_to_anchor=(0.08, 0.95),
           fontsize=9, framealpha=0.85, ncol=2)

title = f"{PROJECT_NAME} (${TICKER.lstrip('$')}) — Token Release Schedule"
if has_demand:
    title += f"\n{DEMAND_SINKS.get('note', '')}"
ax1.set_title(title, fontsize=12, fontweight='bold', pad=12)

plt.tight_layout()

png_buf = io.BytesIO()
fig.savefig(png_buf, format='png', dpi=150, bbox_inches='tight')
png_buf.seek(0)
plt.close()

chart_ws = wb.create_sheet("Token Release Chart")
chart_ws.column_dimensions["A"].width = 2
img = XLImage(png_buf)
img.anchor = "B2"
chart_ws.add_image(img)

# ── SAVE ──────────────────────────────────────────────────────────────
filename = (f"tokenomics-{TICKER.upper().lstrip('$')}"
            f"-{REPORT_DATE.strftime('%Y%m%d')}.xlsx")
wb.save(filename)
print(f"Saved: {filename}")
```

After running, report:
- Filename and full path
- Circulating supply at TGE (tokens + % of total)
- Fully diluted valuation (if price provided)
- Total months until fully vested
- Monthly buyback qty (if demand sinks modeled)

---

## Vesting Description Generator

Auto-generate `vesting_desc` field:

- 100% TGE, no cliff, no vest → `"Fully liquid at TGE"`
- 0% TGE, no cliff, no vest → `"Permanently locked (never vests)"`
- 0% TGE, 12mo cliff, 36mo vest → `"1-year cliff, 3-year linear vest"`
- 25% TGE, 0 cliff, 24mo vest → `"25% liquid at TGE, remainder linear over 2 years"`
- 0% TGE, 6mo cliff, 18mo vest → `"6-month cliff, 18-month linear vest"`
- X% TGE, 0 cliff, 0 vest (with remaining% unlocked at TGE) → treat as
  100% TGE if tge_pct=100, or confirm with founder if 0 < tge_pct < 100
  and vest=0 (remaining tokens would be permanently locked — ask to clarify)

**Rule:** Express durations in years when divisible by 12; months otherwise.

---

## Skill Limits & Feedback

**Trigger limits CTA when:**
- More than 9 allocation categories
- Performance-based or milestone-triggered unlocks
- Dynamic or governance-controlled release schedules
- Non-linear vesting curves (accelerating, stepped)
- Multiple tranches within one category at different terms

When triggered:
> "This is where /tokenomics hits its limit — this design requires
> custom modeling. Submit feedback or get in touch:
> - GitHub: https://github.com/ckpxgfnksd-max/tls/issues
> - DM: https://x.com/ChaseWang"

---

## Output Summary (After Generation)

```
✅ Generated: tokenomics-{TICKER}-{DATE}.xlsx
   Sheet 1: 3-1. Token Allocation Breakdown
   Sheet 2: Token Release Chart

SUMMARY
───────────────────────────────────────────
Total Supply:          {X} tokens
Circulating at TGE:    {X} tokens ({Y}% of total)
Launch Market Cap:     ${W} (if price provided)
Fully Diluted Value:   ${Z} (if price provided)
Fully Vested by:       {date} ({N} months post-TGE)

DEMAND SIMULATION (Chart):
Monthly buyback:       ~{N} tokens/mo (at ${price} assumed)
Monthly burn:          {B} tokens/mo
Net effect:            {X}M tokens removed from circulation by month {N}

ALLOCATION BREAKDOWN
───────────────────────────────────────────
{label:<22} {pct:>6}%  TGE:{tge_pct:>4}%  Cliff:{cliff:>3}mo  Vest:{vest:>3}mo
...

⚠️  VALIDATION NOTES:
{Populate from Block 4 results. For each flag raised, record:
 "⚠ [flag name] — founder confirmed intentional" or
 "✓ [flag name] — corrected to [new value]"
 If no flags triggered: "(none — design passed all checks)"}

Next step: /launch-strategy to coordinate parties around this timeline.
```
