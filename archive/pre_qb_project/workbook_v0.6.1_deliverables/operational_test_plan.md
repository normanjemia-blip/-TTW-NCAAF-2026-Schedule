# TTW NCAAF Power Ratings 2026 — Phase 6.1 Correction & Test-Completion Plan

Base: **v0.6** (`v0.6_working.xlsx`), which was **not approved**. Neither
v0.6 nor the approved **v0.5.2** baseline was modified — both remain
exactly as they were. This build's own diffs (`v0.6.1_vs_v0.6_full_diff.tsv`,
`v0.6.1_vs_v0.5.2_full_diff.tsv`) prove that directly: every changed cell
in v0.6.1 is inside `ADJUSTMENTS!J6:J255`/`K6:K255`, the `START HERE`
banner, or new `CHANGELOG` rows — nothing else. Phase 7 was not started.

## What this build does, in the order the user authorized it

1. **Corrects the genuine ADJUSTMENTS!K formula defect** found (but left
   unrepaired) during Phase 6, using the user's exact specified formula
   text, filled through row 255.
2. **Adds a new authorized safety behavior**: `ADJUSTMENTS!J` (Effective)
   now requires `K` (Flags) to be blank, in addition to the pre-existing
   Active=Y / not-expired conditions. A flagged row — missing reason,
   non-numeric value, or an oversized non-override adjustment — can no
   longer flow into `ENGINE` calculations. `MARGIN OVERRIDE`/`TOTAL
   OVERRIDE` rows remain exempt from the ordinary 4-point large-adjustment
   warning, confirmed by a dedicated harness test.
3. **Completes the DATA INCOMPLETE status test** that Phase 6 was missing.
   Doing so surfaced a **second genuine formula defect** (documented, not
   repaired this round — see `data_incomplete_finding.md`): `DATA
   INCOMPLETE` is currently unreachable because a bare reference to a
   blank source cell evaluates to `0` in Excel/Sheets, not `""`.
4. **Completes a genuine BET-toggle test**: the Phase 6 test never
   actually reached READY status on either toggle variant, so the
   toggle's effect on the label was never really observed. This round
   drives one fixture to true READY with edge ≥ 3.0 and confirms N→
   INVESTIGATE / Y→BET on the *same* fixture.
5. **Strengthens weekly-workflow validation**: every populated prior-fade
   row (F=0 through F=9, not just 0 and 1) is now live-tested, and NDSU's
   transitional restriction is proven *functionally* (5 completed games,
   large edge, BET toggle=Y — restriction still holds) rather than only by
   checking that a label field didn't change.
6. **Corrects the iPad checklist** (QB VALUES Source/Last-update columns,
   the PENDING-LINE-masks-QB-UNCERTAIN clarification, and the spread-sign
   phrasing).
7. **Corrects the Phase 6 CHANGELOG/report entries** that overclaimed
   test coverage (both the DATA INCOMPLETE and BET-toggle claims), rather
   than leaving inaccurate history in place.

## Why the same two-artifact methodology as Phase 6

No spreadsheet engine in this sandbox can recalculate the full
~1,000-row, 21-sheet production file at reasonable cost (LibreOffice
headless remains non-functional; confirmed again this round). The same
two complementary artifacts are used:

1. **Compact real-formula harnesses** (`phase6/harness_test_*.xlsx`,
   `phase6/fade_table_test.xlsx`) — every formula extracted byte-for-byte
   from `v0.6.1_working.xlsx` at its original row/column, run through the
   open-source `formulas` Python engine for actual calculated results.
2. **A full-scale test-applied copy** (`v0.6.1_test_applied.xlsx`) — the
   consolidated fixture set written into a real, complete workbook copy so
   it can be opened directly and inspected.

Every synthetic value in both is tagged `TEST ONLY — NOT REAL DATA`.

## New fixtures this round (`test_fixtures_v061.json`)

- An **isolated oversized adjustment** (`ADJUSTMENTS` row 7, +999 on G2's
  GameID) added to the real full-scale test copy, specifically to
  demonstrate the v0.6.1 J/K fix live (not just in the harness).
- **NDSU's 5-game simulated completed history** at `IMPORT SCHEDULE` rows
  20-24, for the functional transitional-restriction proof.
- The **DATA INCOMPLETE remove/restore** sequence — demonstrated only via
  the harness (`harness_test_G_control/G_datainc/G_datainc2/G_restored.xlsx`),
  since by definition it's a temporary single-field removal, not something
  that fits a static "applied" snapshot.
- The **genuine BET-toggle** fixture (`harness_test_BET_N/BET_Y.xlsx`).
- The **full prior-fade table** synthetic-F sweep (`fade_table_test.xlsx`).
- The **NDSU functional** harness (`harness_test_NDSU_functional.xlsx`).

## A correction made *during this round's own cleanup work*

`apply_to_real_workbook_v061.py`'s docstring described `IMPORT SCHEDULE`
rows 20-24 as "previously-unused rows." That was wrong, and was caught
while building the cleanup script: those 5 rows hold real production
schedule games (Arkansas-Pine Bluff@Missouri, Idaho@Utah, Colorado@Georgia
Tech, Eastern Illinois@Minnesota, UAB@Illinois). `cleanup_script_v061.py`
restores their exact original values (captured directly from the pristine
file, not reconstructed), and the resulting 0-diff proof
(`cell_diff_proof_v061.tsv`) confirms the restoration is exact.

## Cleanup methodology

`cleanup_script_v061.py` reverses every fixture on a copy of the
test-applied file: only the exact manual-input cells that were written to
are cleared (never a whole column, never a formula column); genuinely
non-blank original values (`IMPORT SCHEDULE!L`=`FALSE`, `N`=ESPN source
notes on rows 8/9, and the 5 real games at rows 20-24) are restored to
their true originals, not blanked. The result,
`v0.6.1_test_cleaned.xlsx`, is proven **cell-by-cell identical (0
differences, all sheets)** to the pristine `v0.6.1_working.xlsx` — see
`cell_diff_proof_v061.tsv`.

The delivered `v0.6.1_working.xlsx` was never touched with test data —
only its formula/CHANGELOG/banner content differs from v0.5.2 and v0.6,
confirmed by the full diffs. The test-applied/cleaned pair exists
specifically to prove the fixture-and-removal *procedure* is correct.

## AUDIT-invariant verification

9 of `AUDIT`'s 11 structural invariants (team-map integrity, duplicate
checks, thresholds, HFA, movement cap, BET-toggle default) were
live-calculated via a real-formula compact harness
(`audit_harness.xlsx`) against the real, full-scale `TEAM MAP` /
`PRESEASON` / `SETTINGS` / `MARKET LINES` data. One (`B16`, "no market
lines entered") came back a false failure from a confirmed `formulas`-
engine library bug — `COUNTIF(range,"?*")` incorrectly matches blank
cells — cross-verified as a false positive by direct cell inspection
(0 non-blank cells) and an isolated reproduction probe. The remaining two
(`B10`, `B19`) require the full CLEAN/ENGINE 1000-row pipeline, confirmed
too costly for full-scale recalculation; both are proven instead by direct
structural argument in `validate_v061.py`. Net result: **0 failing
invariants**, `AUDIT!F1` = 0. Full detail in
`expected_vs_actual_results_v061.md`.

## What was explicitly out of scope and was not done

No new preseason rating source, no QB starter research, no real market
line entered anywhere in the delivered file, no formula redesign beyond
the two explicitly authorized ADJUSTMENTS corrections. The second genuine
defect found (`CLEAN!C`/`D` — see `data_incomplete_finding.md`) was
documented, not repaired, per the standing instruction to stop and report
rather than silently fix. Phase 7 was not started.

## Full deliverables inventory

See `README.md` in this ZIP for the file-by-file index.
