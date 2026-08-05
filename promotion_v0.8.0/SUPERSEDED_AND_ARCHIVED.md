# FILES SUPERSEDED AND ARCHIVED — v0.8.0 promotion

Nothing is deleted. Every file below stays in the repository and in git history.
"Superseded" and "archived" describe **role**, not disposition.

## Superseded

| File | SHA-256 | New role |
|---|---|---|
| `workbook_v0.6.2_deliverables/TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx` | `bbb17b50…a838efd` | **SUPERSEDED as authoritative — RETAINED AS THE ROLLBACK TARGET. Do not delete, move or modify.** |
| `PROJECT_MANIFEST.json` (v0.6.2 pointer) | — | Updated to point at v0.8.0; the v0.6.2 entry is retained for rollback |

## Archived — candidate line, superseded by v0.8.0

All are intermediate QB-dataset candidates. Each retains its own MANIFEST.md,
phase report, build script and verification log, so any step is reproducible.

| Directory | Version | SHA-256 | Contribution |
|---|---|---|---|
| `archive/candidates/workbook_v0.7.2_QB_values_candidate/` | v0.7.2 | `82ee5b3d…f151a183` | First 138/138 codes (61 H / 45 M / 32 L) |
| `archive/candidates/workbook_v0.7.3_candidate/` | v0.7.3 | `07bed6de…5dc8d7a72d` | Texas Tech L→M; **Akron defect** corrected |
| `archive/candidates/workbook_v0.7.4_candidate/` | v0.7.4 | `57cd6d20…` | Akron zeros cleared; MAC/CUSA batch 1 |
| `archive/candidates/workbook_v0.7.5_candidate/` | v0.7.5 | `8c273c2e…` | Power-conference batch 2 (partial) |
| `archive/candidates/workbook_v0.7.6_candidate/` | v0.7.6 | `080986dd…4c3cae30d7a5bb` | Batch 2 complete |
| `archive/candidates/workbook_v0.7.7_candidate/` | v0.7.7 | `3da33d0c…5670d02a73` | Final G5 batch; backlog 31 → 5 |
| `archive/candidates/workbook_v0.7.8_candidate/` | v0.7.8 | `8f655e5e…b4b3c389cb` | Final five resolved; backlog → 0; **finding F-7 raised** |
| `archive/candidates/workbook_v0.7.9_candidate/` | v0.7.9 | `661f8ab0…3cef97c7` | **Promotion basis** — F-7 closed, 3 defects corrected |

Earlier deliverable sets (`workbook_v0.3.1` … `workbook_v0.6.1`, and the
`v0.4.2` / `v0.6.1` / `v0.6.2` zips) remain archived as the pre-QB-project lineage.

## Active — not superseded, still in use

| Path | Role |
|---|---|
| `promotion_v0.8.0/` | **The new authoritative workbook and its promotion package** |
| `phase8_4_qb_monitoring/scripts/` | QB monitoring and candidate-build pipeline — **run the first sweep right after promotion** |
| `phase7_preseason_calibration/` | Override standard, deferred-trigger register, source-conflict log — governs future rating changes |
| `TTW_2026_Verified_Schedule_ESPN_v1.0.csv` | Verified 2026 schedule source |
| `scripts/`, `validate_schedule.py`, `raw_espn/` | Schedule acquisition and validation |

## Not touched by this promotion

- Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` — **never accessed in any phase**
- Rollback sheet `1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo` — **never accessed**
- VSiN guide and `TTW_2026_VSiN_Reference_Database_v1.xlsx` — **not accessed; VSiN work remains paused**
