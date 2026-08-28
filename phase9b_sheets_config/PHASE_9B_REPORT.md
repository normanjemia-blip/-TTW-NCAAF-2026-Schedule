# PHASE 9B — GOOGLE SHEETS PRODUCTION CONFIGURATION

**Date:** 2026-08-06 (America/New_York)
**Target sheet:** `1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA`
**Outcome: 1 of 8 authorized changes completed. 4 are impossible through this connector.**

---

## PRE-WRITE CONFIRMATION (required before any write)

| Item | Confirmed |
|---|---|
| **Sheet ID** | `1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA` ✅ |
| **Title** | `TTW_College_Football_Power_Ratings_v0.8.1_AUTHORITATIVE 4` ✅ |
| **Sheet count** | **21** ✅ |
| **START HERE banner** | exact v0.8.1 text — "v0.8.1 AUTHORITATIVE — promotion complete 2026-08-04 … all 73 Tier-1 records … 65 H / 40 M / 33 L" ✅ |
| **Last modified** | `2026-08-05T07:41:59Z` — **unchanged since the Phase 9A read**, so that verification is still current |

---

## 1. EXACT LIST OF GOOGLE SHEET CHANGES MADE

### One change. Nothing else was written.

| # | Change | Status |
|---|---|:--:|
| 8 | **Backup copy created** | ✅ **DONE** |

**No other write occurred.** The production master is byte-for-byte as Phase 9A left
it. No rename, no timezone change, no protection, no cell edit.

---

## 2. THE FOUR ITEMS I COULD NOT DO — connector limitation

The Google Drive connector exposes **eight tools**, of which only two write:
`copy_file` and `create_file`. Both operate at **Drive file level**. There is **no
Sheets API access** — no `spreadsheets.batchUpdate`, no cell write, no range
protection, no spreadsheet-properties tool.

| # | Authorized change | Result | Why |
|---|---|:--:|---|
| **1** | Rename to `…— PRODUCTION MASTER` | ❌ **NOT DONE** | No rename/update tool. `copy_file` can title a *new* file; nothing can retitle an existing one. |
| **2** | Set timezone to America/New_York | ❌ **NOT DONE** | **I cannot even read it.** Timezone is a spreadsheet property, exposed only via the Sheets API. |
| **3** | Apply protection | ❌ **NOT DONE** | Protected ranges are a Sheets API object. Not reachable. |
| **5** | Add visible owner note for B4/B5 | ❌ **NOT DONE** | Requires a cell write. Not reachable. |

**Per your instruction, I am not claiming any of these were completed. They were not.**
All four remain owner actions in the Sheets UI. Instructions are in §7 below.

---

## 3. BACKUP — CREATED AND VERIFIED

| Field | Value |
|---|---|
| **Title** | `TTW College Football Power Ratings v0.8.1 — PRE-CONFIG BACKUP` |
| **File ID** | `1o-oZRsVpqsRzWX6h6Q7etdS7qt3nsfcYfOsjD1PYJoU` |
| **Link** | https://docs.google.com/spreadsheets/d/1o-oZRsVpqsRzWX6h6Q7etdS7qt3nsfcYfOsjD1PYJoU/edit |
| **Created** | 2026-08-06T07:31:47Z |
| **Size** | **258,625 bytes — identical to the source** |

**Verification performed, not assumed.** The first metadata read immediately after
creation reported `fileSize: 1`, which is the same symptom as a failed upload. I
re-read it rather than reporting success. The second read returned the correct
258,625 bytes plus content confirming an exact copy: identical START HERE banner,
identical live counters (**888 games loaded · 39 teams QB UNCERTAIN · Missing: 761
lines · OK — all invariants pass**), and identical DASHBOARD rows with matching
GameIDs and model spreads (TCU -4.2, STAN -3.7). The `1` was a read-race — the
metadata call landed ~3 ms after creation.

**The backup is valid and is your restore point before manual configuration.**

---

## 4. IMPORT STATS COLUMN K — DEFINITIVE ANALYSIS

You said do not guess. I did not. Every figure below is read from the workbook.

| Question | Answer |
|---|---|
| Which cells in column K contain formulas? | **K6:K205 — exactly 200 formulas.** These are the **only 200 formulas on the entire IMPORT STATS sheet.** Formula: `=IF($A6="","",IF(ISNA(MATCH($A6,'TEAM MAP'!$K$6:$K$605,0)),"UNMATCHED",INDEX('TEAM MAP'!$L$6:$L$605,MATCH(…))))` |
| Does the weekly stats paste include column K? | **No.** |
| Would a paste at A6 overwrite K? | **No — it stops two columns short.** |
| Does the documented CFBD file have ten columns or more? | **No — it has NINE.** |

**The documented column order, verbatim from `IMPORT STATS!A2`:**

> *"Column order FIXED: team, games, off_epa_play, def_epa_play, off_success_rate, def_success_rate, off_ppp, def_ppp, pace."*

That is **9 fields → columns A–I**. **Column J is an empty spacer.** Column K
(`Abbrev (auto)`) sits at position 11. A correctly-formed 9-column paste beginning
at `A6` occupies A–I and never reaches K, with **one full spare column as buffer**.

### Both requirements are preservable with NO change to the import procedure.

**This corrects my Phase 9A recommendation.** There I hedged toward WARNING-only
protection on K because I had not yet verified the column count. Now that the
9-column/A–I fact is established, the safer implementation is available:

| Range | Protection | Rationale |
|---|---|---|
| `IMPORT STATS!A6:J205` | **editable** | The 9 documented columns plus the J buffer |
| `IMPORT STATS!K6:K205` | **RESTRICTED** | The correct paste never reaches K, so hard protection costs nothing and blocks the corruption path outright |
| `IMPORT STATS!1:5` | **RESTRICTED** | Headers |

**Why RESTRICTED beats WARNING here:** if the CFBD export ever changes shape to ≥11
columns, RESTRICTED makes the paste **fail loudly** instead of silently destroying
200 lookup formulas. A loud failure is the correct behaviour — you would want to
know the export format changed.

**`IMPORT SCHEDULE` needs no exception at all.** It contains **zero formulas**, and
its documented format is 14 columns (A–N: id, season, week, start_date,
neutral_site, away_team, away_conference, home_team, home_conference, away_points,
home_points, completed, venue, notes). Protect rows 1–5 only; leave `A6:Z1005` fully
editable.

---

## 5. SETTINGS VERIFICATION (read-only)

| Item | Required | Observed | Result |
|---|---|---|:--:|
| **B4** Current week | blank, editable | **blank** | ✅ correct for this phase |
| **B5** As-of date | blank, editable | **blank** | ✅ correct for this phase |
| **B11** BET toggle | `N` | **`N`** — AUDIT confirms *"BET toggle default OFF — OK (OFF)"* | ✅ |
| **B22** League avg total | blank | **blank** | ✅ totals stay disabled |
| **B23** Total EPA scale | blank | **blank** | ✅ totals stay disabled |

**On "verify they remain editable":** since **no protection exists anywhere in the
sheet**, every cell including B4 and B5 is editable by definition. That will remain
true after you apply the protection map, which places B4/B5/B11 in the editable set.

---

## 6. POST-CONFIGURATION VERIFICATION

**No configuration was applied, so there is no post-configuration state to verify.**
What follows re-confirms the pre-existing state is intact and untouched by this phase.

| Check | Required | Observed | Result |
|---|---|---|:--:|
| 21 sheets | 21 | 21 | ✅ |
| Sheet order | unchanged | unchanged | ✅ |
| Formulas intact | intact | all live counters computing | ✅ |
| 138 teams | 138 | AUDIT: *"138 teams in master list — OK"* | ✅ |
| 888 games | 888 | DATA QUALITY: **888** | ✅ |
| 65 H / 40 M / 33 L | exact | **65 / 40 / 33** | ✅ |
| 99 OK / 39 UNCERTAIN | exact | **39 UNCERTAIN** (⇒ 99 OK of 138) | ✅ |
| Zero nonzero QB values | 0 | 0 | ✅ |
| Zero market lines | 0 | AUDIT: *"No market lines entered — OK — clean"*; 761 PENDING | ✅ |
| BET toggle N | N | N | ✅ |
| B22 / B23 blank | blank | blank | ✅ |
| No formula errors | none | **0** errors across 331,173 exported chars | ✅ |
| Week 0 spreads | unchanged | TCU -4.2 · STAN -3.7 · UVA -5.3 · USC -35.2 | ✅ |
| Week 1 spreads | unchanged | OHST -55.2 · OU -40.2 · CAL -1.1 · WASH -19.8 | ✅ |
| Imports pasteable | yes | analysis in §4 confirms the 9-column paste is safe | ✅ |
| Structural audit | pass | **"Failing invariants → 0"** | ✅ |

**The sheet's `modifiedTime` is unchanged from Phase 9A** — proof this phase wrote
nothing to it.

---

## 7. OWNER INSTRUCTIONS — the four manual steps

All in the Sheets UI, roughly 10–15 minutes.

### Step 1 — Rename (30 seconds)
File → Rename → **`TTW College Football Power Ratings v0.8.1 — PRODUCTION MASTER`**
Then check Drive for sibling copies (`… 1`, `… 2`, `… 3`) and delete or clearly park them.

### Step 2 — Timezone (30 seconds)
File → Settings → Time zone → **America/New_York** → Save settings.
**Do this before entering any date.** It is lost on every re-import.

### Step 3 — Owner note for B4/B5 (1 minute)
Put this somewhere visible and **outside any formula range** — the SETTINGS sheet,
a few rows below the last setting (e.g. `A33`), is ideal:

> **WEEKLY REQUIRED:** B4 = current week · B5 = today's date.
> **Stale-line protection is INACTIVE while B5 is blank** — a five-week-old line will
> still read READY, and DATA QUALITY will show `STALE LINE = 0` either way.
> Set both before entering any market line.

Do **not** place it in `B22`/`B23`, anywhere in column B rows 3–31, or on any sheet
other than SETTINGS.

### Step 4 — Protection (10 minutes)
Apply `phase9a_production_config/SHEETS_PROTECTION_MAP.md`, **amended by §4 above**:
IMPORT STATS `K6:K205` should be **RESTRICTED**, not WARNING, and `A6:J205` editable.

Then **test one full stats paste** before trusting it, and confirm AUDIT still reads
0 failing invariants.

---

## 8. FINAL CERTIFICATION

# NOT READY FOR WEEKLY USE

**This is a configuration status, not a verdict on the workbook.** The engine passed
Phase 9 acceptance with zero calculation defects, and the Sheets import is verified
clean — zero formula errors, all structural invariants passing, every count exact,
spreads computing correctly across Week 0 and Week 1.

**It is NOT READY for exactly one reason: the required configuration has not been
applied, and I could not apply it.** Specifically:

1. **`SETTINGS!B5` is blank, so stale-line protection is inactive** — and it reports a clean `0` while inactive. That is a live money risk the moment lines are entered.
2. The timezone is unset and unverifiable.
3. No protection is applied, so any mis-aimed paste silently overwrites formulas.

**None of these can be fixed through the connector available to me.** Claiming
otherwise, or certifying READY on the assumption you will do the steps, would be the
wrong call for a tool that places real bets.

**It becomes READY FOR WEEKLY USE the moment Steps 1–4 in §7 are done.** The backup
is in place, so those steps are now safe to attempt.
