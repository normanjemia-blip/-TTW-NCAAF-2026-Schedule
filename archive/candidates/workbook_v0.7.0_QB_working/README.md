# Phase 8 — Automated QB Research & Controlled QB VALUES Population (WORKING)

**Status: WORKING FILE — NOT AUTHORITATIVE. Awaiting valuation-rubric
approval before any numerical QB values are entered.**

- **Working workbook:** `TTW_NCAAF_Power_Ratings_2026_v0.7.0_QB_WORKING.xlsx`
- **Built from:** authoritative v0.6.2 (`bbb17b50…838efd`), unmodified.
- **Working xlsx SHA-256:** `73aaa005bfb5e72be79dce24598a75c664003ee725435ba696ccb1ac34b4d76f`
- **Authoritative untouched:** v0.6.2 XLSX + Google Sheet
  `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc`; v0.6.1 rollback sheet
  `1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo`. No Google Sheet touched.

## What was done

Researched the 2026 starting-QB situation for **all 138 FBS teams** from
current, credible sources (official athletics releases, beat writers,
ESPN, SI, Athlon, On3/247, Underdog Dynasty, and team-focused outlets),
verifying transfer affiliations. Populated `QB VALUES` **non-numeric**
columns only:

| Col | Field | Populated? |
|---|---|---|
| C | Baseline QB | Yes for H/M teams (= projected starter); **blank for the 32 open competitions** (identity not established, flagged in Notes) |
| D | Baseline value | **BLANK** — pending rubric approval |
| E | Active QB | Yes (projected 2026 starter; "Open (…)" for toss-up competitions) |
| F | Active value | **BLANK** — pending rubric approval |
| G | QB delta | formula (stays blank while D/F blank) |
| H | Confidence (H/M/L) | Yes |
| I | Source | Yes (primary source + URL; full multi-source list in `source_audit.md`) |
| J | Reviewed for season | Yes (2026) |
| K | Last update | Yes (2026-07-21) |
| L | Notes | Yes |
| M | QB status | formula — **all 138 = UNCERTAIN** (delta blank), by design |

No numerical value was invented: the project has **no approved QB
valuation rubric** (confirmed in DICTIONARY/CHANGELOG/architecture and the
v0.4/v0.5.1 findings). A proposed rubric is in
`valuation_methodology_report.md` for approval.

## Results

- **Teams researched:** 138 / 138.
- **Confidence:** 61 H, 45 M, 32 L (see `confidence_summary.md`).
- **Unresolved competitions:** 32 (see `unresolved_competitions.md`).
- **Injury / eligibility concerns:** 10 (see `injury_eligibility.md`).
- **Rows with numerical values:** 0. **Rows awaiting valuation approval:** 138.
- **Remaining QB UNCERTAIN:** 138 (intended — status flips to OK/READY-
  eligible only after approved values are entered; verified live that the
  status formula responds correctly).

## Files

| File | Purpose |
|---|---|
| `TTW_NCAAF_Power_Ratings_2026_v0.7.0_QB_WORKING.xlsx` | The working workbook (QB VALUES non-numeric fields populated). |
| `qb_research.csv` / `qb_research.json` | Complete machine-readable research dataset (all fields + sources + research date). |
| `source_audit.md` | Every team and its supporting source links. |
| `unresolved_competitions.md` | The 32 open competitions (no starter forced). |
| `injury_eligibility.md` | Injury / eligibility / suspension concerns. |
| `valuation_methodology_report.md` | Rubric finding + **proposed rubric for approval**. |
| `confidence_summary.md` | H/M/L counts overall and by conference. |
| `workbook_verification_report.txt` | Full workbook verification (all checks pass). |
| `changed_cells.csv` / `changed_cells.json` | Exact list of changed workbook cells (934 QB VALUES + banner + 12 CHANGELOG). |
| `teams_138.json` | The 138-team canonical abbrev/name/conference list (from TEAM MAP). |
| `scripts/` | `append_records.py`, `build_audits.py`, `populate_workbook.py`, `verify_workbook.py` — reproducible pipeline. |

## Change-set vs authoritative v0.6.2

Only three sheets differ: `QB VALUES` (934 cells: C/E/H/I/J/K/L),
`START HERE!A1` (banner → v0.7.0 WORKING), and `CHANGELOG` (3 new v0.7.0
rows). No formulas, formatting, sheet states, ratings, HFA, thresholds,
market lines, adjustments, or tab structure changed. 21 sheets, recalc-on-
open preserved.

## Next step (requires your approval)

Approve a valuation rubric (Option A recommended in
`valuation_methodology_report.md`). Then, in a separate step, I will write
only `D` and `F` values using that scale, keep the 32 L teams UNCERTAIN,
and re-verify. **Nothing numerical is written until you approve. This
working file has not been promoted to authoritative and no Google Sheet
was modified.**
