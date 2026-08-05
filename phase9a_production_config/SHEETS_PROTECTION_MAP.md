# GOOGLE SHEETS PROTECTION MAP

**Status: PLAN ONLY. No protection has been applied.** Apply via
Data → Protect sheets and ranges, in the production master, after import verification.

**Principle:** yellow input cells editable · import paste zones editable · formula
ranges protected · hidden pipeline sheets protected · owner retains full access.

**Two protection modes:**
- **WARNING** — Google shows *"You're editing a protected cell"* and you may continue. Catches accidents, never blocks you.
- **RESTRICTED** — only listed editors may write. As sole owner you always retain access; the restriction protects against your own mis-aimed paste, not against other people.

---

## VISIBLE SHEETS

### 1. START HERE — **RESTRICTED, whole sheet**
Pure documentation and status formulas. Nothing here is ever edited by hand.
- Editable: **none**
- Protect: `A1:Z100`
- Formulas: `C7:C15` (live status indicators)

### 2. DASHBOARD — **RESTRICTED, whole sheet**
Entirely derived. Filters and sorting still work under protection.
- Editable: **none** (header filter dropdowns are unaffected)
- Protect: `A1:AA1005`

### 3. ENGINE — **RESTRICTED with one exception**
- **Editable: `AL6:AL1005`** — *Notes (input)*, the only input column on the sheet
- Protect: `A1:AK1005` and `AM1:BZ1005`
- ⚠️ 36,000 formulas — the highest-value range in the workbook

### 4. MARKET LINES — **WARNING, with input columns open**
Your heaviest weekly input surface.
- **Editable: `A6:A1005`** (GameID), **`C6:C1005`** (Favorite), **`D6:D1005`** (Spread), **`E6:E1005`** (Total), **`G6:G1005`** (Line date)
- Protect: **`B6:B1005`** (game lookup), **`F`**, **`H:N`**, **`O6:P1005`** (alias resolution + validation)
- Mode: **WARNING** — you paste and correct here constantly; a hard block will cost you more than it saves
- Header rows `1:5`: **RESTRICTED**

### 5. ADJUSTMENTS — **WARNING, with input columns open**
- **Editable: `A6:J255`** — Type, GameID/Team, Value, Reason, dates, Active flag
- Protect: **`K6:K255`** (Flags — computed) and everything right of it
- Mode: **WARNING**

### 6. QB VALUES — **WARNING, with input columns open**
Weekly maintenance surface; second-heaviest input load.
- **Editable: `C6:F143`** (Baseline QB, Baseline value, Active QB, Active value), **`H6:L143`** (Confidence, Source, Reviewed-for-season, Last update, Notes)
- Protect: **`A6:B143`** (team identity), **`G6:G143`** (QB delta), **`M6:M143`** (QB status)
- ⚠️ `G` and `M` are the **only two columns the ENGINE reads**. Protecting them is the single highest-value action on this sheet.

### 7. TEAM RATINGS — **WARNING, with override columns open**
- **Editable: the override column and transition-review columns only** — identify the yellow-filled cells visually and open exactly those
- Protect: `A:H` (identity, effective ratings, fade) and every other computed column
- ⚠️ Do **not** open the effective-rating columns. Ratings are engine output, not input.

### 8. DATA QUALITY — **RESTRICTED, whole sheet**
- Protect: `A1:Z50`

### 9. SETTINGS — **WARNING, weekly cells open**
- **Editable: `B4`** (Current week), **`B5`** (As-of date), **`B11`** (BET toggle)
- Protect: **`B3`** (Season), **`B6:B10`** (HFA, neutral, thresholds), **`B12:B31`** (caps, weights, EPA scales, source weights), and the fade table `C37:C46`
- ⚠️ **`B22`/`B23` must stay protected and empty** — totals are disabled for 2026 by decision. Protecting them is what prevents an accidental guess.
- Mode: **WARNING** on `B4`/`B5`/`B11`; **RESTRICTED** on everything else

### 10. IMPORT SCHEDULE — **fully editable paste zone**
- **Editable: `A6:Z1005`** — *see the paste exception below*
- Protect: header rows `1:5` only

### 11. IMPORT STATS — **fully editable paste zone**
- **Editable: `A6:Z205`** — *see the paste exception below*
- Protect: **`K6:K205`** (team-match lookup — computed) and header rows `1:5`
- ⚠️ Column `K` sits **inside** the paste block. See below.

---

## HIDDEN PIPELINE SHEETS — **RESTRICTED, whole sheet, all of them**

`TEAM MAP` · `CLEAN` · `CALC` · `PRESEASON` · `FCS TIERS` · `HISTORY` ·
`BACKTEST` · `AUDIT` · `DICTIONARY` · `CHANGELOG`

The START HERE tab map already says *"unhide to audit, never edit."* These carry
**~81,000 formulas** — roughly two-thirds of the workbook. Protect every one at
sheet level. `TEAM MAP` deserves particular care: its alias table is what resolves
`Miami` → `MIA` vs `M-OH`, and corrupting it silently mis-maps games.

---

## ⚠️ THE PASTE EXCEPTION — read before protecting

**Yes, pasting a whole import file requires an exception, and it needs handling.**

`IMPORT STATS` column `K` is a **formula column inside the paste target**. Paste a
CFBD stats file wider than 10 columns starting at `A6` and you overwrite `K`,
destroying the team-match lookup for every row.

**Three workable options, in order of preference:**

1. **Protect `K6:K205` as WARNING, not RESTRICTED.** You will get a confirm prompt on every paste. Annoying weekly, but it makes the collision visible instead of silent. **Recommended.**
2. **Paste into `A6` with a file trimmed to columns A–J.** Cleanest, if your CFBD export can be trimmed reliably.
3. **RESTRICTED on `K`** — Google will refuse the paste outright. Safest, most disruptive; you must paste column-by-column.

`IMPORT SCHEDULE` has **no formulas** and needs no exception — paste freely.

**Do not protect any import zone as RESTRICTED without testing a full paste first.**

---

## APPLICATION ORDER

1. Verify the import (Part 6) — **done**
2. Rename the file, drop the trailing ` 4`
3. Apply hidden-sheet protection first (highest value, zero friction)
4. Apply RESTRICTED on START HERE, DASHBOARD, DATA QUALITY, ENGINE
5. Apply WARNING on MARKET LINES, ADJUSTMENTS, QB VALUES, TEAM RATINGS, SETTINGS
6. **Test a full IMPORT STATS paste** before trusting the setup
7. Confirm `AUDIT` still reads 0 failing invariants

**Protection is a safety net, not a substitute for the dated weekly working copy.**
