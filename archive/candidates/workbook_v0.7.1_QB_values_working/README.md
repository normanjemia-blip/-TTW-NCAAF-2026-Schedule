# Phase 8.1 — Deviation-Only QB Initialization & Baseline Audit (WORKING)

**Status: WORKING FILE — NOT AUTHORITATIVE. Zero-init applied (Option A);
future nonzero adjustments proposed but NOT approved/entered.**

- **Working workbook:** `TTW_NCAAF_Power_Ratings_2026_v0.7.1_QB_VALUES_WORKING.xlsx`
- **Source:** `TTW_NCAAF_Power_Ratings_2026_v0.7.0_QB_WORKING.xlsx` (research
  checkpoint, preserved unmodified).
- **v0.7.1 SHA-256:** `608068e51c53d100280f85a092b2c1776bcc9947906f213e18ab9289faf88ef9`
- **Untouched:** authoritative v0.6.2 XLSX; v0.6.2 Google Sheet
  (`1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc`); v0.6.1 rollback sheet
  (`1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo`).

## What was done

Applied the approved **deviation-only** framework: the preseason QB is the
neutral reference, so `Baseline value = 0`, `Active value = 0`,
`QB delta = 0` — no double-count of QB quality already in TEAM RATINGS.

A **baseline-identity audit** first established the preseason-rating
snapshot dates from the PRESEASON sheet — **SP+ = 2026-03-27**, **FPI =
2026-07-19**, **TeamRankings = 2026-07-19** — and confirmed that each
initialized team's Active QB was the projected starter priced into all
three (winter-portal transfers + returning starters; no unresolved issue).
Two borderline cases were verified by targeted search (Ole Miss's Chambliss
eligibility — final, priced in → initialized; UNC's Edwards — PCL still
recovering, unsettled → exception).

## Results

- **Initialized at 0/0 (delta 0, status OK): 105 teams.**
- **Left blank / QB UNCERTAIN (exceptions): 33 teams** — 27 open
  competitions, 4 injury/availability (Stanford, Syracuse, Texas Tech,
  North Carolina), 2 conflicting sourcing (Tennessee, Nebraska).
- **Live-calc confirmed: 105 status OK, 33 UNCERTAIN, 0 nonzero deltas.**
- **Baseline mismatches: 0. Post-3/27 QB changes on initialized teams: 0.**
- **No nonzero QB value exists anywhere.**

## Change-set vs v0.7.0

Only `QB VALUES!D`/`F` for the 105 initialized teams (210 cells),
`START HERE!A1` (banner), and 3 new `CHANGELOG` rows. 21 sheets, formula
count unchanged (123,011), all formulas/formatting/states/ratings/HFA/
settings/thresholds unchanged. D and F contain **only 0 or blank**.

## Files

| File | Purpose |
|---|---|
| `TTW_NCAAF_Power_Ratings_2026_v0.7.1_QB_VALUES_WORKING.xlsx` | The working workbook (105 teams zero-initialized). |
| `baseline_identity_audit.md` / `baseline_audit.json` | Snapshot dates, method, and per-team disposition. |
| `teams_initialized.md` | The 105 teams initialized at 0/0. |
| `teams_uncertain.md` | The 33 exceptions with category + reason. |
| `post_rating_changes.md` | Post-snapshot changes / baseline-mismatch review (0 found). |
| `valuation_methodology_report.md` | **CORRECTED (Phase 8.2)** — permanently deviation-only; no absolute cross-team tier scale; Baseline value fixed at 0. |
| `future_qb_deviation_rubric.md` | **NEW (Phase 8.2)** — proposed quarter-point deviation bands (−4.0 / +2.0 bounds), evidence framework, no-arbitrary-decay review rule. |
| `qb_exception_resolution_tracker.csv` / `.json` | **NEW (Phase 8.2)** — 33-team structured resolution tracker, grouped by category. |
| `qb_exception_resolution_playbook.md` | **NEW (Phase 8.2)** — how to clear each exception + per-team treatment + Vanderbilt correction. |
| `phase8_2_review_note.md` | **NEW (Phase 8.2)** — every substantive change vs the Phase 8.1 proposal + internal-consistency findings. |
| `workbook_verification_report_v071.txt` | Full verification (all checks pass) + live-calc status counts. |
| `changed_cells_v071.csv` / `.json` | Exact changed-cell list (210 D/F + banner + 12 CHANGELOG). |
| `qb_research.csv` / `qb_research.json` / `source_audit.md` | Carried-forward research + sources. |
| `teams_initialized.md` / `teams_uncertain.md` / `post_rating_changes.md` | Init/exception lists + baseline-mismatch review. |
| `scripts/` | `classify_and_populate.py`, `verify_v071.py`, `build_tracker.py`. |

## Phase 8.2 (documentation only — no workbook/sheet edit)

The methodology is finalized as **permanently deviation-only**: Baseline
value stays 0 and is never rewritten; Active value is only the deviation vs
a team's own preseason baseline QB; **no absolute cross-team tier scale**.
The withdrawn "absolute tier" option and the arbitrary midseason-decay rule
were removed; the proposed future deviation bands are now quarter-point with
bounds **−4.0 / +2.0**. A 33-team exception-resolution tracker and playbook
were added. **One classification inconsistency flagged: Vanderbilt** (L /
"open competition") is really a consistently-projected young starter and is
**recommended for reclassification to Medium + zero-init** — documented
only, **not applied**. The v0.7.1 workbook is byte-unchanged this phase
(SHA `608068e5…`).

## Next step (requires approval)

Approve (or amend) `future_qb_deviation_rubric.md` before any nonzero QB
value is entered; optionally approve the Vanderbilt reclassification; and
resolve the 33 exceptions via the tracker as camps settle. Nothing nonzero
is written and v0.7.1 is not promoted until you approve. No Google Sheet was
modified.
