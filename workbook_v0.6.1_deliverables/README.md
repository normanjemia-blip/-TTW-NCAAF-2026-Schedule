# Phase 6.1 Deliverables Index

Correction + test-completion build from **v0.6** (not approved). Neither
v0.6 nor the approved **v0.5.2** baseline was modified. Phase 7 was not
started.

1. **`TTW NCAAF Power Ratings 2026 - Working v0.6.1.xlsx`** — the clean
   delivered workbook. Diffs against both v0.6 and v0.5.2 touch only
   `ADJUSTMENTS!J6:J255`/`K6:K255` (the two authorized formula
   corrections), the version banner, and new `CHANGELOG` rows.
2. **`operational_test_plan.md`** — what changed, why, the two-artifact
   test methodology, fixture design, cleanup methodology, and the
   AUDIT-invariant verification approach.
3. **`expected_vs_actual_results.md`** — every new Phase 6.1 test's
   expected vs actual result, the full status-priority-chain
   revalidation, and the second genuine formula defect found (documented,
   not repaired).
4. **`data_incomplete_finding.md`** — full root-cause write-up of the
   DATA INCOMPLETE defect surfaced while completing the test the user
   requested (`CLEAN!C`/`D` bare blank-cell-reference issue).
5. **`ipad_weekly_checklist.md`** — corrected weekly-operating checklist:
   QB VALUES Source/Last-update columns added, PENDING-LINE-masks-QB-
   UNCERTAIN clarified, "home underdog favorite" phrasing removed in favor
   of "spread is always positive regardless of home/away favorite."
6. **`test_fixtures.json`** — every fixture used this round, both carried
   over from Phase 6 and newly added (isolated oversized adjustment,
   NDSU's 5-game history, the DATA INCOMPLETE remove/restore sequence,
   the genuine BET-toggle fixture, the full prior-fade sweep).
7. **`fcs_classification_888.json`** — unchanged from Phase 6 (schedule
   composition didn't change this round); the real, calculated FBS/FCS
   classification for all 888 schedule games, proving the 761/127 split.
8. **`v0.6.1_vs_v0.6_full_diff.tsv`** and
   **`v0.6.1_vs_v0.5.2_full_diff.tsv`** — complete cell/formula diffs
   against both baselines, plus **`validate_v061.py`** and
   **`validation_report.txt`** — the full validation battery (46/46
   checks pass), including the AUDIT-invariant proof and every
   user-specified target count.
9. **`build_v061_formulas.py`** / **`build_v061_changelog.py`** — the
   scripts that produced the two authorized formula corrections and the
   CHANGELOG/banner updates, with assert-before-overwrite verification
   against the user's exact specified formula text.
10. **`harness/`** — the compact real-formula test harness for every new
    Phase 6.1 test: `build_harness.py` builds the base;
    `harness_test_D2/E2/F_override.xlsx` re-test the ADJUSTMENTS fix
    (oversized, non-numeric, and MARGIN OVERRIDE-exempt cases);
    `harness_test_G_control/G_datainc/G_datainc2/G_restored.xlsx` are the
    DATA INCOMPLETE remove/restore sequence; `harness_test_BET_N/BET_Y.xlsx`
    are the genuine BET-toggle test; `harness_test_NDSU_functional.xlsx`
    is the functional transitional-restriction proof;
    `build_fade_table_test.py`/`fade_table_test.xlsx` is the full 0-9
    prior-fade sweep; `build_audit_harness.py`/`audit_harness.xlsx` is the
    AUDIT-invariant live-calc harness; `probe_blank.xlsx`/
    `probe_blank2.xlsx`/`probe_countif.xlsx` are the isolated
    formula-semantics probes that confirmed the DATA INCOMPLETE root
    cause and the `formulas`-engine COUNTIF-wildcard-on-blank library bug.
    `harness_results_raw_v061.json` is every test's raw calculated output.
11. **`fixtures/`** — the reproducible test-fixture system applied to a
    real, full-scale workbook copy: `apply_to_real_workbook_v061.py`
    (writes the consolidated Phase 6.1 fixture set),
    `v0.6.1_test_applied.xlsx` (the resulting test-applied file, clearly
    marked TEST ONLY), and `cleanup_script_v061.py` (reverses every
    fixture, including exact restoration of 5 real schedule games that
    the NDSU fixture temporarily overwrote — see `operational_test_plan.md`).
12. **`proof_of_removal/`** — `cleanup_script_v061.py`'s output
    (`v0.6.1_test_cleaned.xlsx`) diffed cell-by-cell against the pristine
    `v0.6.1_working.xlsx`: **0 differences, all sheets**
    (`cell_diff_proof.txt`).

## What changed vs Phase 6 (v0.6, not approved)

- The genuine `ADJUSTMENTS!K` `#VALUE!`-propagation defect is now fixed
  (exact user-specified formula), not just documented.
- A new authorized safety behavior: any flagged adjustment row now has
  `Effective = 0`, so it can never reach `ENGINE`.
- The DATA INCOMPLETE status test is now actually attempted (it surfaced
  a second genuine defect, documented not repaired).
- The BET-toggle test now genuinely reaches READY and demonstrates the
  toggle's real effect — Phase 6's version never did.
- The prior-fade table is tested across all 10 populated rows, not just
  0 and 1.
- NDSU/Sacramento State's transitional restriction is proven functionally
  (games played, edge size, toggle state all insufficient to lift it),
  not just by label persistence.
- The iPad checklist and this build's own CHANGELOG correct several Phase
  6 inaccuracies.
