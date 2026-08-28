# Phase 7D — v0.7.2 Candidate Validation & Promotion Decision

**Date:** 2026-08-03 (America/New_York) · **Both source files unmodified** ·
**Google Sheet never accessed** · **Candidate NOT promoted.**

## Recommendation: **OPTION B — REPAIR CANDIDATE, THEN REVALIDATE**

The candidate's **structure is sound and its provenance is fully explained** —
zero formula changes, zero unauthorized differences, regression-neutral. It is
**not** promotable as-is for one owner-approved reason: **Texas Tech is coded
`L`, but the approved analytical conclusion is `M`.** That is a limited input
correction with no broader workbook defect — the exact definition of Option B.

---

## 1. Complete cell diff (v0.6.2 → v0.7.2)

**1,181 changed cells across exactly 3 sheets. Every one is explained.**

| Sheet | Cells | Columns | Classification |
|---|---:|---|---|
| QB VALUES | **1,144** | E,H,I,J,K,L ×138; C ×106; D,F ×105 | **QB DATA** |
| CHANGELOG | **36** | A–D × 9 new rows (58–66) | **VERSION OR CHANGELOG** |
| START HERE | **1** | A1 (version banner) | **VERSION OR CHANGELOG** |

**UNRELATED: 0 · UNAUTHORIZED: 0 · UNKNOWN: 0.**

Sheets with **zero** changes (18): ENGINE, TEAM RATINGS, PRESEASON, SETTINGS,
MARKET LINES, ADJUSTMENTS, IMPORT SCHEDULE, IMPORT STATS, CLEAN, CALC, DASHBOARD,
DATA QUALITY, TEAM MAP, FCS TIERS, HISTORY, BACKTEST, AUDIT, DICTIONARY.
**No ratings, HFA, weights, thresholds, schedule, or status logic touched.**

## 2. Formula diff

| Check | Result |
|---|---|
| Formula count | **123,011 → 123,011 (delta 0)** ✔ |
| Formula cells changed | **0** ✔ |
| Formulas added / removed | **0 / 0** ✔ |
| Sheets / order / visibility | 21 / identical / identical ✔ |
| Formula columns (A,B,G,M) touched | **No** — all 1,144 QB edits are in input columns only ✔ |

## 3. QB dataset inventory

| Field | Col | Populated | Type |
|---|---|---:|---|
| Baseline QB | C | 106/138 | constant |
| Baseline value | D | 105/138 (all `0`) | constant |
| Active QB | E | 138/138 | constant |
| Active value | F | 105/138 (all `0`) | constant |
| Confidence | H | **138/138** | constant |
| Source | I | 138/138 | constant |
| Reviewed for season | J | 138/138 (all `2026`) | constant |
| Last update | K | 138/138 (`2026-07-21`) | constant |
| Notes | L | 138/138 | constant |

## 4. 138-team confidence-code audit

| Check | Result |
|---|---|
| Distribution | **61 H / 45 M / 32 L = 138** ✔ (matches the stated inventory) |
| Invalid codes | **None** — every value is exactly H, M, or L ✔ |
| Header | `Confidence (H/M/L)` ✔ |
| Teams missing | 0 ✔ |
| Teams duplicated | 0 (138 unique abbrevs) ✔ |
| Row shift | None — TEAM MAP ↔ QB VALUES aligned on every spot-check ✔ |
| Wrong-team data | None detected ✔ |
| Formula cells intact | A,B,G,M all formulas on all 138 rows ✔ |
| Input cells constants only | C,D,E,F,H,I,J,K,L — no formulas ✔ |
| `Reviewed for season` | 2026 for all 138, matching `SETTINGS!B3` ✔ |

**Code interpretation verified against actual workbook behavior.** The only
formula consuming column H is `QB VALUES!M`:
`=IF(OR($G="",$H="L",$J<>SETTINGS!$B$3),"UNCERTAIN","OK")`. **Only `L` is
special-cased** — it forces UNCERTAIN. H and M behave identically to the status
formula. This confirms H = settled, M = likely, **L = the uncertainty gate**,
exactly as documented. No codes renamed; system not rebuilt.

**Cross-tab (confidence × computed status):**

| | OK | UNCERTAIN |
|---|---:|---:|
| H | 61 | 0 |
| M | 44 | **1** |
| L | 0 | 32 |

The single **M/UNCERTAIN** is **North Carolina** (row 65) — baseline QB named
(Billy Edwards Jr.) but D/F deliberately left blank as the documented PCL-injury
exception. **This is intentional and correct**, and it explains the C=106 vs
D=105 asymmetry.

## 5. Numerical QB-value audit

**The candidate does contain numerical values — but only `0` and blank.**

| Check | Result |
|---|---|
| Distinct D values | `0` (×105), blank (×33) |
| Distinct F values | `0` (×105), blank (×33) |
| **Any nonzero value anywhere** | **NONE** ✔ |
| Values outside ±4.0 | None (none exist to test) ✔ |
| Computed deltas | **0 nonzero** across all 138 ✔ |
| Double-counting | **None possible** — a 0 delta cannot double-count |
| Methodology | Deviation-only: prior assumes the expected starter → preseason delta correctly 0 ✔ |
| Moves team ratings in pristine state? | **No** — `ENGINE!M` consumes G; 0 and blank both contribute 0 |

**Conclusion:** the numerical layer is a **zero-initialization**, not a
valuation. It asserts "the priced starter is starting," which is exactly what
the methodology requires. There is no starter-to-backup contingency value in the
workbook, and none should be entered preseason.

**On separating confidence from values:** the workbook does **not** cleanly
support promoting confidence metadata alone. Status depends on **G** (from D/F)
*and* H jointly — with D/F blank, every team would read UNCERTAIN regardless of
its code, making the confidence dataset inert. **The two layers must promote
together**, which is what the candidate does.

## 6. Texas Tech verification

| Item | Candidate value |
|---|---|
| Row | **52** = TTU / Texas Tech ✔ (TEAM MAP aligned) |
| Active QB (E52) | **Will Hammond** ✔ |
| Baseline QB (C52) | blank (injury exception) |
| **Confidence (H52)** | **`L`** ← **discrepancy** |
| Baseline / Active value | blank / blank (not zero-initialized) |
| Reviewed season (J52) | 2026 ✔ |
| Last update (K52) | 2026-07-21 |
| Computed status (M52) | **UNCERTAIN** |
| Medical status | Surgeon cleared (late July); **training staff retains final say**; ~Aug 21 nine-month mark |
| Backup | Behind Hammond, unproven (Morton/Rodriguez/Bailey to NFL) |

**DISCREPANCY DOCUMENTED, NOT CHANGED.** The candidate holds `L`; the approved
conclusion is `M` (LIKELY — not H, not L). Per instruction I have **not**
silently corrected it. Proposed repair in §11.

**Note on downstream effect:** even after repair, `M52` stays **UNCERTAIN**,
because D52/F52 are blank → G52 blank → the `$G=""` branch fires regardless of
H. The repair is metadata-only unless Texas Tech is also zero-initialized —
which the deferred-trigger register correctly gates on the ~Aug 21 clearance.

## 7. Full QB factual validation — honest scope statement

**Tier 1 (full live verification) was NOT completed for all qualifying teams in
this pass.** The tier-1 population is ~77 teams (45 M + 32 L) plus H-coded
injury risks. Across Phases 7A–7D I have individually live-verified roughly
**30** of them (all SEC candidates, the AAC trio, Southern Miss, Texas Tech,
Michigan, Penn State, Clemson, Miami, Indiana, Stanford/Syracuse/UNC/Nebraska
carried from July research). **~47 remain unverified against current sources** —
predominantly G5 teams in the MAC, CUSA, Sun Belt, and rebuilt Pac-12.

I am reporting this as a **limitation, not completed work.** It is the single
largest open item in this audit.

**Tier 2 (confirmation review)** for stable returning starters is satisfied
indirectly: the July research is internally consistent, and no league-wide
starter announcements have occurred (verified for the SEC), so H-coded returning
starters remain reasonable.

**Currency caveat:** all `Last update` values read **2026-07-21** — **13 days
stale** as of 2026-08-03, and **fall camps have since opened**. Nothing found in
Phases 7B–7D contradicts any code, but the dataset has not been refreshed since
camp began.

## 8. Regression-test results

Tested by direct formula tracing on the real workbooks (no heavy engine run).

| # | Test | Result |
|---|---|---|
| 1 | H + populated (0) values | status **OK** ✔ (61 teams) |
| 2 | M + populated (0) values | status **OK** ✔ (44 teams) |
| 3 | L + populated values | **N/A** — no L team is zero-initialized (by design); L forces UNCERTAIN regardless ✔ |
| 4 | Blank QB values | status **UNCERTAIN** ✔ (33 teams) |
| 5 | Starter-to-backup delta | **0 nonzero deltas** ✔ |
| 6 | QB status output | **105 OK / 33 UNCERTAIN** ✔ |
| 7 | **Interaction with PENDING LINE** | **PENDING LINE outranks QB UNCERTAIN** in `ENGINE!AI`. **0 market spreads are loaded**, so `CALC!S=1` for every game → **every game reads PENDING LINE in both files**. The QB status change is **completely masked** ✔ |
| 8 | Interaction with FCS — NO PLAY | FCS gate (`AG`) outranks QB gate; unaffected ✔ |
| 9 | Interaction with TRANSITION UNCERTAIN | `AF` ranks *below* QB UNCERTAIN; unchanged since both are masked by PENDING LINE ✔ |
| 10 | BET-toggle behavior | `SETTINGS!B11 = "N"` (off) and unchanged; BET requires READY + edge ≥ 3.0, unreachable with no lines ✔ |
| 11 | **No unexpected team-rating movement** | `TEAM RATINGS` **byte-identical**; `ENGINE!M` = 0 in both (blank→0 and 0→0) ✔ |
| 12 | **No unexpected projected-spread movement** | `ENGINE` sheet **unchanged**; model spread inputs identical ✔ |

**Headline regression finding:** promoting the candidate flips 105 teams'
QB status from UNCERTAIN to OK — but because **PENDING LINE outranks QB
UNCERTAIN** and no market lines exist, **not one visible game status changes in
the pristine preseason state.** `ENGINE!AJ` (confidence) is likewise blank for
PENDING LINE games, so no confidence score moves either. The QB dataset becomes
behaviorally visible only once market lines are loaded — which is the intended
design.

## 9. Candidate defect list

| # | Severity | Defect | Effect |
|---|---|---|---|
| **D-1** | **Blocking** | **Texas Tech `H52` = `L`; approved conclusion is `M`** | Metadata only (status stays UNCERTAIN either way) |
| D-2 | Moderate | **~47 tier-1 teams not live-verified** against current sources | Unknown factual currency, mostly G5 |
| D-3 | Minor | `Last update` = 2026-07-21 for all 138 (13 days stale; camps have opened) | Documentation currency |
| D-4 | Informational | UNC coded `M` but not zero-initialized → the lone M/UNCERTAIN | **Intentional** injury exception; no action |

No structural, formula, alignment, or unauthorized-change defects were found.

## 10. Source & conflict log (Phase 7D)

| # | Claim | Source 1 | Source 2 | Resolution | Residual |
|---|---|---|---|---|---|
| D7-1 | Candidate is "v0.7.2 vs v0.6.2, QB-only" | Project docs | Direct diff: 1,181 cells, 3 sheets, 0 formula changes | **Confirmed** | None |
| D7-2 | "138/138 codes, 61H/45M/32L" | Owner statement | Direct count | **Confirmed exactly** | None |
| D7-3 | Texas Tech should be M | Approved 7C.1 conclusion | Candidate holds `L` | **Genuine discrepancy** → repair D-1 | None |
| D7-4 | Promotion might move ratings/spreads | Reasonable concern | ENGINE/TEAM RATINGS byte-identical; deltas all 0 | **Refuted — no movement** | None |
| D7-5 | Promotion would un-gate 105 teams' game status | Plausible inference | PENDING LINE outranks QB UNCERTAIN; 0 lines loaded | **Masked — no visible status change now** | Becomes visible when lines load |

## 11. Exact repair plan (Option B)

**Single edit, in the candidate only:**

1. `QB VALUES!H52` (Texas Tech): **`L` → `M`**
2. `QB VALUES!K52` (Last update): `2026-07-21` → **`2026-08-03`**
3. `QB VALUES!L52` (Notes): append the clearance basis — surgeon cleared;
   training staff retains final medical decision; ~Aug 21 nine-month mark;
   LIKELY not KNOWN pending official naming
4. CHANGELOG: one new row (67) recording the reclassification, reason, date
5. Banner: version increment if you want a distinct artifact (e.g. v0.7.3);
   otherwise leave as-is

**Do NOT** zero-initialize D52/F52 — Texas Tech stays UNCERTAIN until the
Aug 21 clearance trigger fires, per the deferred-trigger register.

**Revalidation after repair:** re-run this exact audit and confirm — 123,011
formulas, 0 formula changes, diff limited to `H52`/`K52`/`L52` + CHANGELOG
(+ banner), codes still 61 H / **46 M** / **31 L**, and status counts unchanged
at **105 OK / 33 UNCERTAIN**.

**Recommended sequencing:** address **D-2** (the ~47 unverified tier-1 teams)
*before* promotion, or accept it explicitly as a known limitation. My
recommendation is to resolve D-1 and D-2 together in one pass, then promote —
promoting a dataset whose factual currency is one-third unverified would import
that uncertainty into production.

## 12. Zero-changes confirmation — both source files

| File | SHA-256 | Status |
|---|---|---|
| v0.6.2 AUTHORITATIVE | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` | **Unchanged** — identical to `PROJECT_MANIFEST.json` ✔ |
| v0.7.2 CANDIDATE | `82ee5b3d4731c18a2deb3288d63c9b6eb8e1dae4bc5c28bb6be0cdebf151a183` | **Unchanged** — identical to its build-time manifest ✔ |

Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` — **never accessed.**
No promotion, no new authoritative version, no rating/HFA/formula change, no
market-line loading, no weekly simulation, no silent defect fixes.
