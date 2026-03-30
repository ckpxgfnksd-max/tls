---
name: tokenomics
description: |
  Token allocation and vesting schedule builder. Walks founders through
  allocation design, vesting schedules, and generates a professional Excel
  token release schedule ready for exchanges, legal counsel, and investors.
  Use when a founder says "tokenomics", "allocation", "vesting schedule",
  "token release", "how do I structure my token supply", or after /why-token.
version: 1.0.0
tags: ["token", "tokenomics", "vesting", "allocation", "excel", "TGE", "schedule"]
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

**What this produces:** A professional Excel token release schedule
(`tokenomics-{TICKER}-{DATE}.xlsx`) that can be submitted directly to
exchanges, shared with legal counsel, and used to brief investors.

---

## Hard Rules

- One question at a time — don't dump a form at the founder
- Validate as you go — catch errors before generation, not after
- Warn on red flags — don't silently accept bad vesting designs
- Never generate until all required inputs are collected and confirmed
- Do NOT ask for information that can be computed (e.g., don't ask for
  token amounts if you have % and total supply — calculate it)

---

## Session Flow

### Block 1: Project Basics

Collect in order, one at a time:

1. **Project name** — "What's the project name?"
2. **Token ticker** — "What's your token ticker? (e.g., $TOKEN)"
3. **TGE date** — "When is your TGE? (DD.MM.YYYY or YYYY-MM-DD)"
4. **Vesting day** — "On which day of each month do tokens vest?
   (e.g., 1st, 15th, last day of month)"

---

### Block 2: Supply Design

5. **Total supply** — "What is your total token supply?
   (This is the total number of tokens that will ever exist)"

   After they answer, ask:

6. **Max supply** — "Is your max supply the same as total supply, or does
   your protocol have a hard cap that differs? (Most projects: same number.
   Inflationary protocols: max supply may be uncapped or higher)"

   **Teach if they don't know the difference:**
   > - **Total supply** = tokens created minus tokens burned to date
   > - **Max supply** = hard cap on tokens that will ever exist
   > For most fixed-supply tokens these are the same number.

---

### Block 3: Allocation Categories

7. **Number of categories** — "How many allocation categories does your
   token have? (Max 9. Typical: 5-8)"

   Common categories for reference (don't suggest unless asked):
   Public Sale, Private Sale, Seed Round, Strategic Round, Team, Advisors,
   Investors, Ecosystem Fund, Community, Liquidity/Market Making,
   Foundation/Treasury, Marketing, Reserve

   For each category (repeat N times, one at a time):

   **a. Label** — "Category [N] name?"

   **b. Purpose** — "One sentence: what is this allocation for?"

   **c. Percentage** — "What % of total supply goes to [label]?"
      Track running total. If running total > 100%, flag immediately:
      "That puts you at X% total — you only have Y% left to allocate."

   **d. TGE unlock %** — "What % of [label]'s allocation unlocks at TGE?
      (0% = fully locked at launch, 100% = fully liquid at launch)"

   **e. Cliff** — "Is there a cliff period before vesting begins?
      (Months of 0 releases after TGE before any tokens unlock.
      0 = no cliff)"

      **Warn if team or investor cliff < 12:**
      > "Standard for team and investor allocations is a 12-month cliff
      > minimum. Exchanges and investors use this as a credibility signal.
      > Are you intentionally setting a shorter cliff?"

   **f. Linear vest duration** — "After the cliff, how many months does
      [label] vest linearly? (0 = no linear vest, fully liquid at TGE)"

   **g. Token price** — "What is the token price for [label]? (USD.
      If not applicable — e.g., ecosystem fund — answer N/A)"

      If they give a price, also ask:
      **h. Amount raised** — "How much did you raise in this round? ($USD)"
      **i. Valuation** — "What is the implied valuation? ($USD.
         Can be calculated as: token price × total supply)"

   After all categories are collected, validate:
   - **Total % must equal 100%** — if not, stop and resolve before continuing
   - If total < 100%: "You have [X]% unallocated. What happens to those tokens?"
   - If total > 100%: "Your allocations sum to [X]% — that's [X-100]% over. Adjust before we continue."

---

### Block 4: Smart Validation (Run Before Generating)

After collecting all categories, surface any red flags — one at a time,
not as a dump. Require the founder to consciously acknowledge each.

**Red Flag Checks:**

1. **High TGE unlock (>50% of total supply liquid at TGE):**
   > "Your TGE circulating supply is [X]% of total supply. That's high —
   > heavy early selling pressure is one of the most common ways token
   > launches fail in the first 72 hours. Is this intentional?"

2. **No liquidity allocation:**
   > "I don't see a dedicated liquidity or market-making allocation.
   > Without committed liquidity at launch, your token will have wide
   > spreads and poor price discovery. Standard is 3-10% for liquidity.
   > Do you have this covered another way?"

3. **Team cliff < 12 months:**
   > "Your team allocation has a [X]-month cliff. Major exchanges (Binance,
   > OKX, Coinbase) treat a sub-12-month team cliff as a credibility signal.
   > This will come up in listing due diligence. Intentional choice?"

4. **Team + insider allocation > 40% of total supply:**
   > "Team + investor + advisor allocations total [X]% — above 40% is
   > often flagged in exchange due diligence as too insider-heavy.
   > Community and ecosystem should typically dominate. Worth revisiting?"

5. **Implied FDV check (if token price provided):**
   Calculate: FDV = token_price × total_supply
   > "At your token price of $[X], your fully diluted valuation (FDV) is
   > $[Y]. Your circulating supply at TGE is [Z]%, implying a launch market
   > cap of $[W]. Does that match your expectations for where this trades?"

For each flag: if the founder confirms it's intentional, proceed. If they
want to adjust, loop back to the relevant category.

---

### Block 5: Confirm & Generate

Before generating, show a clean summary table:

```
PROJECT: [name] ($TICKER)
TGE: [date] | Vesting day: [day] of each month
Total Supply: [number] | Max Supply: [number]

ALLOCATIONS:
#  Label              %      TGE%   Cliff  Vest    Price
1  [label]           XX%    XX%    XX mo  XX mo   $X.XXX
2  [label]           XX%    XX%    ...
...
Total:              100%

CIRCULATING AT TGE: [X tokens] ([Y]% of total supply)
FULLY DILUTED VALUATION: $[Z] (if price provided)
```

Ask: "Does this look correct? Type 'yes' to generate the Excel, or tell
me what to change."

---

### Block 6: Generate Excel

Once confirmed, generate the Excel file using Python/openpyxl.

**Output filename:** `tokenomics-{TICKER}-{YYYYMMDD}.xlsx`
**Save location:** Current working directory

Use this Python script template — fill in all variables from the
collected session data:

```python
from openpyxl import Workbook
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side,
                              numbers)
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta
import calendar

# ── DATA (filled from session) ─────────────────────────────────────────
PROJECT_NAME   = "{project_name}"
TICKER         = "{ticker}"
TGE_DATE       = datetime({tge_year}, {tge_month}, {tge_day})
VEST_DAY       = "{vest_day}"   # e.g. "1st", "15th", "Last"
REPORT_DATE    = datetime.today()
MAX_SUPPLY     = {max_supply}
TOTAL_SUPPLY   = {total_supply}

# Each category: dict with keys:
#   label, purpose, pct, tge_pct, cliff, vest, price, raised, valuation
CATEGORIES = {categories_list}
# ───────────────────────────────────────────────────────────────────────

# ── STYLE HELPERS ──────────────────────────────────────────────────────
BLUE   = "FF0000FF"   # Input cells (blue text)
BLACK  = "FF000000"   # Formula/calculated cells
BOLD_FILL   = PatternFill("solid", fgColor="FFD9D9D9")  # Header rows
HEADER_FILL = PatternFill("solid", fgColor="FF1F4E79")  # Dark blue header
WHITE_FILL  = PatternFill("solid", fgColor="FFFFFFFF")
YELLOW_FILL = PatternFill("solid", fgColor="FFFFFF00")  # Key assumptions

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
    cell.number_format = '#,##0;(#,##0);"-"'

def fmt_pct(cell):
    cell.number_format = '0.0%;(0.0%);"-"'

# ── VESTING CALC ───────────────────────────────────────────────────────
def calc_schedule(total, tge_pct, cliff, vest, max_months):
    """Returns list: index 0 = TGE release, 1..N = monthly releases."""
    s = [0.0] * (max_months + 1)
    tge_amt = total * tge_pct / 100
    remaining = total - tge_amt
    s[0] = tge_amt

    if remaining <= 0 or (cliff == 0 and vest == 0):
        return s  # fully liquid at TGE

    if cliff == 0:
        monthly = remaining / vest
        for m in range(1, vest + 1):
            if m <= max_months:
                s[m] += monthly
    else:
        total_months = cliff + vest
        rate = remaining / total_months
        if cliff <= max_months:
            s[cliff] += rate * cliff        # accumulated cliff release
        for m in range(cliff + 1, cliff + vest + 1):
            if m <= max_months:
                s[m] += rate

    return s

# ── DATE HELPERS ───────────────────────────────────────────────────────
def month_end_date(base_date, months_offset):
    """Return the last day of (base_date + months_offset months)."""
    y = base_date.year + (base_date.month - 1 + months_offset) // 12
    m = (base_date.month - 1 + months_offset) % 12 + 1
    d = calendar.monthrange(y, m)[1]
    return datetime(y, m, d)

# Determine max vesting horizon
max_months = 0
for cat in CATEGORIES:
    horizon = cat["cliff"] + cat["vest"]
    if horizon > max_months:
        max_months = horizon
max_months = max(max_months, 48)  # minimum 48 months shown

# Pre-compute all schedules
schedules = []
for cat in CATEGORIES:
    total_tokens = TOTAL_SUPPLY * cat["pct"] / 100
    s = calc_schedule(total_tokens, cat["tge_pct"], cat["cliff"],
                      cat["vest"], max_months)
    schedules.append(s)

# ── BUILD WORKBOOK ─────────────────────────────────────────────────────
wb = Workbook()
ws = wb.active
ws.title = "Token Allocation Breakdown"

# Column widths (match template)
ws.column_dimensions["A"].width = 6.5
ws.column_dimensions["B"].width = 22
ws.column_dimensions["C"].width = 19.5
for i, col in enumerate(["D","E","F","G","H","I","J","K","L"]):
    ws.column_dimensions[col].width = 16
ws.column_dimensions["M"].width = 20

# ── NOTES SECTION (rows 1-7) ───────────────────────────────────────────
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
meta = [
    (9,  "Date of Report",               REPORT_DATE.strftime("%d.%m.%Y"), True),
    (10, "Project Name",                  PROJECT_NAME,                     True),
    (11, "Token Ticker",                  f"${TICKER.lstrip('$')}",         True),
    (12, "Max Supply",                    MAX_SUPPLY,                       True),
    (13, "Total Supply",                  TOTAL_SUPPLY,                     True),
    (14, "Circulating Supply at Genesis", None,                             False),
    (15, "TGE",                           TGE_DATE,                         True),
    (16, "Date of token vested each month", VEST_DAY,                       True),
]

# Circulating at TGE = sum of TGE releases across all categories
circ_at_tge = sum(s[0] for s in schedules)

for row, label, val, is_input in meta:
    lbl = ws.cell(row=row, column=2, value=label)
    style_label(lbl)
    if row == 14:
        val_cell = ws.cell(row=row, column=3,
                           value=f"=SUM(D{28+2}:{get_column_letter(3+len(CATEGORIES))}{28+2})")
        # We'll fix this reference after schedule rows are known
        val_cell.value = circ_at_tge
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

# ── ALLOCATION TABLE (rows 18-30) ──────────────────────────────────────
n_cats = len(CATEGORIES)
cat_cols = [get_column_letter(4 + i) for i in range(n_cats)]  # D, E, F...
total_col = get_column_letter(4 + n_cats)  # column after last category

# Row 18: header
ws.cell(row=18, column=2, value="Allocation No.").font = label_font()
ws.cell(row=18, column=3, value="").font = label_font()
for i, col in enumerate(cat_cols):
    c = ws.cell(row=18, column=4+i, value=i+1)
    style_header(c)
ws.cell(row=18, column=4+n_cats, value="Total").font = Font(
    name="Arial", bold=True, color=BLACK, size=10)

# Rows 19-21: Label, Purpose, Vesting Schedule
row_labels = [(19, "Label"), (20, "Purpose of Allocation"),
              (21, "Vesting Schedule")]
cat_fields = [("label", True), ("purpose", True), ("vesting_desc", True)]

for (row, lbl), (field, is_input) in zip(row_labels, cat_fields):
    l = ws.cell(row=row, column=2, value=lbl)
    style_label(l)
    ws.merge_cells(f"B{row}:C{row}")
    for i, cat in enumerate(CATEGORIES):
        val = cat.get(field, "")
        c = ws.cell(row=row, column=4+i, value=val)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if is_input:
            style_input(c)
        else:
            style_formula(c)

# Row 22: Token Amount (header only)
ws.cell(row=22, column=2, value="Token Amount").font = label_font()
ws.merge_cells("B22:C22")

# Row 23: Token amounts (calculated from % × total supply)
ws.cell(row=23, column=2, value="Amount").font = label_font()
ws.merge_cells("B23:C23")
for i, cat in enumerate(CATEGORIES):
    token_amt = TOTAL_SUPPLY * cat["pct"] / 100
    c = ws.cell(row=23, column=4+i, value=token_amt)
    style_formula(c)
    fmt_num(c)
# Total
tc = ws.cell(row=23, column=4+n_cats,
             value=f"=SUM({cat_cols[0]}23:{cat_cols[-1]}23)")
style_formula(tc, bold=True)
fmt_num(tc)

# Row 24: % of Total Supply
ws.cell(row=24, column=2, value="% of Total Supply").font = label_font()
ws.merge_cells("B24:C24")
for i, cat in enumerate(CATEGORIES):
    c = ws.cell(row=24, column=4+i, value=cat["pct"] / 100)
    style_input(c)
    fmt_pct(c)
tc = ws.cell(row=24, column=4+n_cats,
             value=f"=SUM({cat_cols[0]}24:{cat_cols[-1]}24)")
style_formula(tc, bold=True)
fmt_pct(tc)

# Row 25: Token Price
ws.cell(row=25, column=2, value="Token Price ($)").font = label_font()
ws.merge_cells("B25:C25")
for i, cat in enumerate(CATEGORIES):
    price = cat.get("price", "N/A")
    c = ws.cell(row=25, column=4+i, value=price)
    style_input(c, bold=True)
    if isinstance(price, (int, float)):
        c.number_format = '$#,##0.0000'

# Row 26: Amount Raised
ws.cell(row=26, column=2, value="Amount Raised ($)").font = label_font()
ws.merge_cells("B26:C26")
for i, cat in enumerate(CATEGORIES):
    raised = cat.get("raised", "")
    c = ws.cell(row=26, column=4+i, value=raised if raised else None)
    style_input(c, bold=True)
    if isinstance(raised, (int, float)):
        c.number_format = '$#,##0'
tc = ws.cell(row=26, column=4+n_cats,
             value=f"=SUM({cat_cols[0]}26:{cat_cols[-1]}26)")
style_formula(tc, bold=True)
tc.number_format = '$#,##0'

# Row 27: Valuation
ws.cell(row=27, column=2, value="Valuation ($)").font = label_font()
ws.merge_cells("B27:C27")
for i, cat in enumerate(CATEGORIES):
    val = cat.get("valuation", "")
    c = ws.cell(row=27, column=4+i, value=val if val else None)
    style_input(c, bold=True)
    if isinstance(val, (int, float)):
        c.number_format = '$#,##0'

# Row 29: Vesting Schedule section header
header_row = 29
ws.cell(row=header_row, column=2, value="Token Release Schedule").font = \
    Font(name="Arial", bold=True, size=11, color=BLACK)
ws.merge_cells(f"B{header_row}:M{header_row}")

# Row 30: Column headers for schedule
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

    if month_idx == 0:
        label = "TGE"
        date_val = TGE_DATE
    else:
        label = f"{month_idx}M"
        date_val = month_end_date(TGE_DATE, month_idx)

    ws.cell(row=row, column=2, value=label).font = formula_font(bold=True)
    date_cell = ws.cell(row=row, column=3, value=date_val)
    date_cell.number_format = "DD.MM.YYYY"
    style_formula(date_cell)

    row_total = 0
    for i, (cat, sched) in enumerate(zip(CATEGORIES, schedules)):
        release = sched[month_idx] if month_idx < len(sched) else 0
        c = ws.cell(row=row, column=4+i, value=release if release != 0 else None)
        style_formula(c)
        fmt_num(c)
        row_total += release

    # Circulating supply = SUM of all releases up to and including this row
    circ_col = 4 + n_cats
    circ_cell = ws.cell(row=row, column=circ_col,
                         value=f"=SUM({cat_cols[0]}{data_start}:{cat_cols[-1]}{row})")
    style_formula(circ_cell, bold=True)
    fmt_num(circ_cell)

# Freeze top rows and first 2 cols
ws.freeze_panes = ws.cell(row=data_start, column=4)

# ── SAVE ──────────────────────────────────────────────────────────────
filename = f"tokenomics-{TICKER.upper().lstrip('$')}-{REPORT_DATE.strftime('%Y%m%d')}.xlsx"
wb.save(filename)
print(f"Saved: {filename}")
```

After running the script, report:
- The filename and full path of the generated Excel
- Circulating supply at TGE (tokens + % of total)
- Fully diluted valuation (if token price was provided)
- Total months until fully vested

---

## Vesting Description Generator

When writing the `vesting_desc` field for each category, auto-generate
a clean human-readable string:

- 100% TGE, no cliff, no vest → `"Fully liquid at TGE"`
- 0% TGE, 12mo cliff, 36mo vest → `"1-year cliff, 3-year linear vest"`
- 25% TGE, 0 cliff, 24mo vest → `"25% liquid at TGE, remainder linear over 24 months"`
- 0% TGE, 6mo cliff, 18mo vest → `"6-month cliff, 18-month linear vest"`
- X% TGE, Y cliff, Z vest → `"X% liquid at TGE, Y-month cliff, Z-month linear vest"`

---

## Skill Limits & Feedback

When this skill hits its edge (complex multi-tranche raises, non-linear
vesting, performance-based unlocks, on-chain governance-controlled
release schedules), say so directly:

> "This is where /tokenomics hits its limit — this design requires
> custom modeling. Submit feedback or get in touch:
> - GitHub: https://github.com/ckpxgfnksd-max/tls/issues
> - DM: https://x.com/ChaseWang"

---

## Output Summary (After Generation)

After the Excel is generated, show:

```
✅ Generated: tokenomics-{TICKER}-{DATE}.xlsx

SUMMARY
───────────────────────────────────────────
Total Supply:          {X} tokens
Circulating at TGE:    {X} tokens ({Y}% of total)
Fully Diluted Value:   ${Z} (at ${price}/token)
Fully Vested by:       {date} ({N} months post-TGE)

ALLOCATION BREAKDOWN
───────────────────────────────────────────
{label:<22} {pct:>6}%  TGE:{tge_pct:>4}%  Cliff:{cliff:>3}mo  Vest:{vest:>3}mo
...

⚠️  FLAGS ACKNOWLEDGED:
{list any flags the founder confirmed}

Next step: /launch-strategy to coordinate parties around this timeline.
```
