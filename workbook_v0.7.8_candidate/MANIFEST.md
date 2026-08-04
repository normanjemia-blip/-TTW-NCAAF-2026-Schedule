# Phase 7D.4A deliverables — v0.7.8 CANDIDATE

**Built:** 2026-08-04 (America/New_York) · **Source:** v0.7.7 CANDIDATE
**Status: CANDIDATE — NOT AUTHORITATIVE, NOT PROMOTED.**

## Files

| File | Purpose |
|---|---|
| `TTW_NCAAF_Power_Ratings_2026_v0.7.8_CANDIDATE.xlsx` | The candidate workbook |
| `PHASE_7D4A_REPORT.md` | Phase report: five verifications, correction log, source & conflict log, finding F-7, regression battery, diff, recommendation |
| `build_v078.py` | Reproducible build script (v0.7.7 → v0.7.8) |
| `verify_v078.py` | Diff, 35-test regression battery, inventory, backlog ledger, manifest |
| `verification_log_v078.txt` | Full captured output of `verify_v078.py` |
| `final_five_starting_state.json` / `.csv` | The five records exactly as they stood in v0.7.7 |
| `qb_inventory_v078.json` / `.csv` | 138-team QB inventory with carried-forward verification ledger |
| `diff_v077_to_v078.csv` | Every changed cell with its classification |

## SHA-256

| File | SHA-256 | Status |
|---|---|---|
| `TTW_NCAAF_Power_Ratings_2026_v0.7.8_CANDIDATE.xlsx` | `8f655e5e369a6a8c12fdb34f3309cff13a92c9310af6186b77081be4b3c389cb` | Built this phase |
| v0.7.7 CANDIDATE | `3da33d0c10a375c6bd3e43c06f1119b1a6a72cfb49d16abff65ed9c670d02a73` | **UNCHANGED** ✔ |
| v0.6.2 AUTHORITATIVE | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` | **UNCHANGED**, matches `PROJECT_MANIFEST.json` ✔ |

## What changed

**32 cells · 0 formula changes · 0 unrelated/unauthorized/unknown.**

- **Washington State** (row 80) **M → L**, zeros cleared to blank — wide-open competition, HC declined to commit, no separation from Eshelman.
- **Georgia Southern** (row 131) **L → M**, values stay blank — stale entry omitted Max Johnson, whom HC Clay Helton says would start today.
- **Texas State** (78), **North Texas** (87), **Old Dominion** (137) — confirmed at M, entries refined to name competitors.
- All five stamped `2026-08-04`; 3 CHANGELOG rows; 1 START HERE banner.

## State

| Metric | v0.7.7 | v0.7.8 |
|---|---|---|
| H / M / L | 64 / 43 / 31 | **64 / 43 / 31** (offsetting) |
| OK / UNCERTAIN | 101 / 37 | **100 / 38** |
| Blank / zero numerical | 37 / 101 | **38 / 100** |
| Nonzero QB values | 0 | **0** |
| Formula cells | 123,011 | **123,011** |
| Sheets | 21 | **21** |
| **Ledger backlog** | 5 | **0** |
| **Tier-1 rows lacking an in-workbook verification stamp** | 21 | **21** — finding F-7 |

## Recommendation

**OPTION B — DEFER AND REPAIR.** The backlog is zero, but finding F-7 (report §9) shows 21
Tier-1 records are credited as verified while the workbook still carries their original
2026-07-21 build stamp and note. Owner decision required before a promotion audit.

## Constraints honored

v0.6.2 AUTHORITATIVE unmodified ✔ · v0.7.7 unmodified ✔ · Google Sheet
`1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` and rollback sheet
`1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo` never accessed ✔ · nothing promoted ✔ ·
no nonzero QB values created ✔ · no formula, tab, structure, settings, threshold, schedule,
source-weight or status-logic change ✔ · no market lines loaded, no simulation, no Phase 8
work ✔ · dates not refreshed for any team that remains unverified ✔.
