# TTW NCAAF Power Ratings 2026

Google Sheets–first college-football power-rating workbook: CFBD data in,
opponent-adjusted ratings out, your own market lines for edges. No picks
sold — just process.

## Current authoritative version: **v0.6.2** ✅

| | |
|---|---|
| **Title** | `TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE` |
| **Status** | APPROVED — current authoritative production workbook |
| **Native Google Sheet** | [`1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc`](https://docs.google.com/spreadsheets/d/1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc) |
| **Source SHA-256** | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` |
| **Promotion date** | 2026-07-21 |
| **Round-trip verification** | PASS (`workbook_v0.6.2_deliverables/promotion/`) |
| **Deliverables** | [`workbook_v0.6.2_deliverables/`](workbook_v0.6.2_deliverables/) |

v0.6.2 repaired the DATA INCOMPLETE pathway defect — `CLEAN!C6:C1005` and
`CLEAN!D6:D1005` now preserve genuinely blank Week/Date inputs as blank
(nested blank-guard) so the DATA INCOMPLETE status is reachable. Exactly
2,005 cell-level changes vs v0.6.1 (2,000 CLEAN formulas + banner + one
CHANGELOG row); nothing else was touched.

## Rollback version: v0.6.1 (preserved, unmodified)

| | |
|---|---|
| **Title** | `TTW_NCAAF_Power_Ratings_2026_v0.6.1_AUTHORITATIVE` |
| **Status** | PRESERVED — rollback version |
| **Native Google Sheet** | [`1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo`](https://docs.google.com/spreadsheets/d/1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo) |
| **Deliverables** | [`workbook_v0.6.1_deliverables/`](workbook_v0.6.1_deliverables/) |

The v0.6.1 Google Sheet was **not** modified during the v0.6.2 promotion.

## Production state (v0.6.2, clean preseason)

21 sheets · 123,011 formula cells · 888 games (761 FBS-vs-FBS,
127 FCS — NO PLAY) · 0 BLOCKED · 0 DATA INCOMPLETE · 0 audit failures ·
0 market lines · 0 adjustments · 0 in-season stats · BET toggle = N.

## Phase status

- **Phase 6.2:** CLOSED — approved, promoted to a native Google Sheet, and
  round-trip verified.
- **Phase 7 (repository closeout & authoritative-version promotion):**
  COMPLETE.
- **Phase 8.x (QB VALUES working track — NOT authoritative):** in progress on
  branch `claude/2026-ncaaf-schedule-build-by6j5n`. Deviation-only QB
  methodology; latest working checkpoint **v0.7.2 candidate** (105 OK / 33
  UNCERTAIN / 0 nonzero). **Nothing QB-related is promoted; no Google Sheet was
  edited; v0.6.2 remains the authoritative production workbook.**
- No market-line entry or preseason activation has been started.

## QB working track (not authoritative)

The deviation-only QB initialization, the 33-team exception system, and the
fall-camp monitoring + candidate-build automation live outside the authoritative
deliverables and change **no** production workbook or Google Sheet:

- [`workbook_v0.7.2_QB_values_candidate/`](workbook_v0.7.2_QB_values_candidate/)
  — latest QB working checkpoint (candidate), methodology, rubric, exception
  tracker, and review log.
- [`phase8_4_qb_monitoring/`](phase8_4_qb_monitoring/) — fall-camp monitoring
  plan, the `pending_qb_resolutions` ledger, and the **QB resolution → candidate
  build pipeline** (`apply_pending_qb_resolutions.py`, `verify_qb_candidate.py`,
  `build_qb_candidate.py`, `test_pipeline.py`). See
  [`phase8_4_qb_monitoring/qb_resolution_pipeline_readme.md`](phase8_4_qb_monitoring/qb_resolution_pipeline_readme.md).
  The pipeline turns human-**approved** resolutions into a **verified** workbook
  candidate; it never modifies the source workbook (its SHA is asserted
  unchanged) and never runs the memory-heavy full-formula engine.

See [`PROJECT_MANIFEST.json`](PROJECT_MANIFEST.json) for the
machine-readable version registry and
[`workbook_v0.6.2_deliverables/promotion/`](workbook_v0.6.2_deliverables/promotion/)
for the promotion + round-trip verification artifacts.

## Repository layout

- `workbook_v0.6.2_deliverables/` — current authoritative deliverables,
  including `promotion/` (native-sheet promotion manifest and round-trip
  verification).
- `workbook_v0.6.1_deliverables/` … `workbook_v0.3.1_deliverables/` —
  prior version deliverables (historical record).
- `workbook_v0.7.1_QB_values_working/`, `workbook_v0.7.2_QB_values_candidate/`,
  `phase8_4_qb_monitoring/` — the QB VALUES working track (deviation-only
  methodology, exception system, and the resolution→candidate pipeline). **Not
  authoritative.**
- `TTW_2026_Verified_Schedule_ESPN_v1.0.csv`,
  `TTW_2026_Schedule_Reconciliation_Report.md`, `raw_espn/`, `scripts/`,
  `validate_schedule.py` — the Phase 3 schedule build and its provenance.
