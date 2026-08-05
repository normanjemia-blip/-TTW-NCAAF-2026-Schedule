# PHASE 9A — PRODUCTION CONFIGURATION CLOSEOUT

**Date:** 2026-08-05 (America/New_York)
**Authoritative file:** TTW College Football Power Ratings v0.8.1 AUTHORITATIVE · SHA-256 `e2da9a4c…cdfd6` — **not modified**
**Native Google Sheet:** `1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA` — **read-only access only; no write performed**

---

# PART 1 — RECLASSIFICATION OF THE THREE QA FINDINGS

## Finding 1 — Totals pipeline blank (SETTINGS!B22, B23 unconfigured)

### Classification: **INTENTIONAL UNCONFIGURED FEATURE**
### Not a defect. Not a calculation error.

The formula chain is correct. `ENGINE!Y` opens with a guard —
`IF(OR(...,SETTINGS!$B$22="",SETTINGS!$B$23="",...),"",…)` — that deliberately
returns blank when the two calibration parameters are absent. That is a feature
gate working exactly as written.

**I am correcting my own Phase 9 QA report on one point.** I wrote that this state
is *"silent"* and that a user *"could reasonably think totals are working but no
edges."* **That was wrong, and reading the live Google Sheet disproved it.** The
DASHBOARD renders an explicit string:

> `Model total = NOT AVAILABLE`

— 90 occurrences in the portion of the DASHBOARD I read. The workbook clearly
distinguishes *switched off* from *broken*. My QA report over-stated this finding
and the MAJOR severity I assigned it was too high.

**Correct severity: documentation item, not an issue.** The only real risk is that
no on-sheet text explains *why* it is unavailable or that it is permanent for 2026.

---

## Finding 2 — Stale-line protection requires SETTINGS!B5

### Classification: **REQUIRED WEEKLY OPERATING STEP** (primary)
### with a genuine, secondary **USER-ERROR RISK**

`CALC!Q` reads `IF(OR($L6="",$P6="",SETTINGS!$B$5=""),0,…)`. With `B5` blank the
staleness test short-circuits to 0 and **STALE LINE can never fire** — verified in
simulation, where a line 99 days old still resolved to READY, and verified as
firing correctly the moment `B5` is populated.

This is **not a defect**: a date comparison cannot function without a reference
date. It is an input the operator supplies weekly.

**But the failure mode is genuinely dangerous and deserves to stay on the register.**
`DATA QUALITY` currently reports `STALE LINE = 0`. That reads identically whether
(a) every line is fresh, or (b) the check is switched off. **A user cannot
distinguish "protected and clean" from "unprotected."** START HERE step 1 shows
`— set week + as-of date` until both are filled, and that is the *only* warning
anywhere in the workbook.

**Confirmed live in the production master:** `SETTINGS!B4` and `B5` are **both
blank right now**, so stale-line protection is currently inactive.

**Control:** the one-minute preflight checklist (Deliverable 2), mandatory before
any market line is entered.

---

## Finding 3 — Formula ranges have no protection or data validation

### Classification: **USER-ERROR RISK** (primary) + **OPTIONAL QUALITY IMPROVEMENT**
### Not a defect.

Confirmed: **0 data-validation rules and 0 protected sheets** across all 21 tabs.
The workbook's own legend states *"Plain cells = formulas — never type into them"* —
a convention with nothing enforcing it.

**This was never an `.xlsx` problem to solve.** Excel sheet protection does not
survive import into Google Sheets in a usable form. Protection is a **Sheets-side
configuration task**, which is why Deliverable 3 is a protection map rather than a
workbook change.

**Why it matters:** the workbook stores no cached formula results, so an accidental
paste over a formula column leaves no stale-value artifact to notice. The damage is
silent until a number looks wrong.

---

## Summary table

| # | Finding | Classification | Defect? | Owner action |
|---|---|---|:--:|---|
| 1 | Totals blank | **Intentional unconfigured feature** | No | Document as permanently unavailable for 2026 |
| 2 | Stale-line needs B5 | **Required weekly operating step** + user-error risk | No | Preflight checklist, every week |
| 3 | No protection / validation | **User-error risk** + optional quality improvement | No | Apply the Sheets protection map |

**Zero genuine calculation defects. The Phase 9 engine verdict stands unchanged.**

---

# PART 2 — TOTALS DECISION

## Recommendation: **A — Keep totals disabled for 2026 and document all total columns as intentionally unavailable.**

**Reasoning.**

`SETTINGS!B22` (league average total) and `B23` (total EPA scale) are model
parameters, not preferences. Guessing either one produces a totals number that
looks authoritative and is unvalidated — the single most dangerous failure mode for
a workbook used to place bets. A wrong spread is visibly wrong; a plausible-looking
wrong total is not.

Nothing in this project has ever calibrated a totals model. There is no historical
scoring dataset loaded, no backtest, and no validation methodology for totals. The
`BACKTEST` tab is empty. Enabling the feature would import an unvalidated model
input into production, which Phase 9A explicitly exists to prevent.

**The cost of choosing A is low.** Spread edges are unaffected — they are a wholly
separate chain. The DASHBOARD already prints `NOT AVAILABLE`, so the state is
self-documenting.

**Option B is the correct follow-on if totals are ever wanted** — a separate
calibration project, on historical data, with its own validation and its own
promotion audit. It is not a 2026 activity and must not be attempted mid-season.

**Affected columns, all intentionally unavailable for 2026:** `ENGINE!Y` (model
total), `AA` (total edge), `AB` (total label), `AC`/`AD` (home/away team totals),
and the DASHBOARD's Model total, Total edge, Total label, Home TT, Away TT columns.
`Mkt total` still records what you enter; it simply has nothing to compare against.

**No workbook edits made in this phase.**

---

# PART 6 — GOOGLE SHEETS IMPORT VERIFICATION

Access: Drive connector, **read-only**. No write, no edit, no protection applied.

## A. DIRECTLY VERIFIED — read from the live Google Sheet

| # | Item | Required | Observed | Result |
|---|---|---|---|:--:|
| 1 | Sheet count | 21 | **21 exported blocks** | ✅ |
| 2 | Sheet order | workbook order | matches expected sequence exactly | ✅ |
| 3 | START HERE banner | v0.8.1 text | **exact match**, incl. "73 Tier-1", "65 H / 40 M / 33 L" | ✅ |
| 4 | Games loaded | 888 | **888** (DATA QUALITY, live) | ✅ |
| 5 | 138 teams | 138 | **AUDIT: "138 teams in master list — OK"** | ✅ |
| 6 | QB H / M / L | 65 / 40 / 33 | **65 / 40 / 33** (counted from QB VALUES) | ✅ |
| 7 | QB UNCERTAIN | 39 | **"39 teams QB UNCERTAIN"** (START HERE, live) | ✅ |
| 8 | Market lines | 0 | **AUDIT: "No market lines entered — OK — clean"**; PENDING LINE = **761** | ✅ |
| 9 | BET toggle | N | **AUDIT: "BET toggle default OFF — OK (OFF)"**; SETTINGS = `N` | ✅ |
| 10 | Formula errors | none | **0** `#REF!` `#VALUE!` `#N/A` `#DIV/0!` `#NAME?` `#NUM!` `#ERROR!` across 331,173 exported characters | ✅ |
| 11 | Week 0 spreads | computing | TCU -4.2 · STAN -3.7 · UVA -5.3 · USC -35.2 · FSU -27.7 · NDSU -7.0 · EMU -4.8 · UNLV -5.6 | ✅ |
| 12 | Week 1 spreads | computing | OHST -55.2 · OU -40.2 · TAMU -39.0 · IND -36.7 · CAL -1.1 · WASH -19.8 · LSU -10.3 | ✅ |
| 13 | BLOCKED | 0 | **0** (DATA QUALITY) | ✅ |
| 14 | Structural audit | pass | **"Failing invariants → 0"**, every invariant OK | ✅ |
| 15 | SETTINGS constants | 2026 / 2.5 / 0 / 1 / 1.5 / 3 / N | all exact | ✅ |
| 16 | FCS handling | no model spread | every FCS game: blank spread + `FCS — NO PLAY` | ✅ |
| 17 | QB gate live | gating | UNC @ TCU shows `QB UNCERTAIN` — UNC was downgraded to L in 7D.5 | ✅ |

**761 PENDING LINE reconciles exactly: 888 games − 127 FCS — NO PLAY = 761.** The
FCS exclusion is working in production.

**Live AUDIT invariants, all OK:** 138 teams · no duplicate abbreviations · no
duplicate manual aliases · preseason prior mean **0.00** · no BLOCK-typed team
resolves to READY · **no recommendation without a valid line** · BET toggle OFF ·
thresholds 1.0/1.5/3.0 · HFA 2.5 / neutral 0 · movement cap 2.5 · no market lines ·
no duplicate GameIDs.

## B. STATIC-ANALYSIS CONCLUSIONS — inferred, not directly observed

- **Formula equivalence.** The connector returns *values*, not formulas. That every spread, status and audit invariant computes to the expected figure is strong evidence the formulas imported correctly, but I did not read a single formula string out of the Sheet.
- **Hidden/visible states.** All 21 tabs appear in the export. Google's export includes hidden tabs, so **presence does not prove the hidden ones are still hidden.** Unverified — check visually.
- **Array formulas.** 28,893 single-cell array formulas were the flagged import risk. They evidently evaluate correctly (spreads are right), but I could not inspect their converted form.

## C. COULD NOT BE VERIFIED THROUGH THE CONNECTOR

1. **Formula text** — no read path exposes it.
2. **Tab hidden/visible state** — requires the Sheets API or a visual check.
3. **Conditional formatting / protection / validation** — not exposed; expected to be absent.
4. **Full 888-row DASHBOARD and ENGINE** — the export truncates long tabs. I read roughly the first 90 DASHBOARD rows. The **live counters** (888 / 761 / 39 / 0 blocked) are computed over the full dataset, so those figures are trustworthy.
5. **Timezone setting** — not exposed. **Must be confirmed manually.**
6. **SHA / byte identity** — meaningless for a native Sheet; conversion necessarily changes bytes.

## D. One observation for the owner

The file is titled **`TTW_College_Football_Power_Ratings_v0.8.1_AUTHORITATIVE 4`** —
the trailing ` 4` indicates a repeated upload. Rename it before it becomes the
production master, and confirm no sibling copies (` 1`, ` 2`, ` 3`) are still in
Drive to be confused with it later.

---

# PART 7 — FINAL RECOMMENDATION

## **READY AFTER OWNER CONFIGURATION**

Not "ready for weekly use" — and the gap is small, specific and entirely on the
configuration side.

**What is already proven.** The engine passed Phase 9 acceptance with zero
calculation defects, and the Google Sheets import is **cleaner than I expected**:
zero formula errors, all structural invariants passing, 888 games, 138 teams,
QB codes exact, spreads computing sensibly across Week 0 and Week 1, FCS
exclusion working, BET toggle off, zero market lines. There is nothing wrong with
the model or the import.

**What the owner must do first — three items, under ten minutes total:**

1. **Set the timezone** to America/New_York (one time). Unverifiable through the connector; the `.xlsx` cannot carry it.
2. **Populate `SETTINGS!B4` and `B5`** before entering any market line. Both are blank right now, which means stale-line protection is currently inactive and reports a clean `0` while inactive.
3. **Apply the Sheets protection map** (Deliverable 3) before live data goes in — or consciously accept the paste-over risk and rely on the weekly working copy instead.

**Then it is ready for weekly use.**

**Standing constraint for the season:** totals remain disabled. Every total column
is intentionally unavailable, and no one should populate `B22`/`B23` without a
completed calibration project.
