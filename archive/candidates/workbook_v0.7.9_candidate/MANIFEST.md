# Phase 7D.5 deliverables — v0.7.9 FINAL QB-VERIFICATION CANDIDATE

**Built:** 2026-08-04 (America/New_York) · **Source:** v0.7.8 CANDIDATE
**Status: CANDIDATE — NOT AUTHORITATIVE, NOT PROMOTED. Awaiting owner approval.**

## Files

| File | Purpose |
|---|---|
| `TTW_NCAAF_Power_Ratings_2026_v0.7.9_CANDIDATE.xlsx` | The final QB-verification candidate |
| `PHASE_7D5_REPORT.md` | Phase report: the five re-verified, 21 records closed out, 3 defects, remaining issues, promotion recommendation |
| `build_v079.py` | Reproducible build script (v0.7.8 → v0.7.9) |
| `verify_v079.py` | 38-test regression battery, both diffs, inventory, ledger, manifest |
| `verification_log_v079.txt` | Full captured output of `verify_v079.py` |
| `qb_inventory_v079.json` / `.csv` | Final 138-team QB inventory with verification ledger |
| `diff_v078_to_v079.csv` | Every changed cell this phase, classified |
| `diff_v062_to_v079.csv` | Cumulative diff against the AUTHORITATIVE workbook |

## SHA-256

| File | SHA-256 | Status |
|---|---|---|
| `TTW_NCAAF_Power_Ratings_2026_v0.7.9_CANDIDATE.xlsx` | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` | Built this phase |
| v0.7.8 CANDIDATE | `8f655e5e369a6a8c12fdb34f3309cff13a92c9310af6186b77081be4b3c389cb` | **UNCHANGED** ✔ |
| v0.6.2 AUTHORITATIVE | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` | **UNCHANGED**, matches `PROJECT_MANIFEST.json` ✔ |

## What changed

**73 cells · 0 formula changes · 0 unrelated/unauthorized/unknown.**

- **Missouri** (row 14) **M → H** — HC Eli Drinkwitz officially named Austin Simmons on 2026-03-19; the entry was stale. Zeros retained.
- **North Carolina** (row 65) **M → L** — battle "remains wide open," four candidates, Belichick has not named a starter. Values were already blank.
- **UNLV** (row 125) **M → L**, zeros cleared — coaches won't name a front-runner in the Arnold/Orji battle.
- **18 records stamped** with verification dates and evidence notes (finding F-7 closed).
- **5 final-five records** re-verified against official sources; notes refreshed with two new facts (Texas State's Shaker Reisig is the backup; North Texas replaces the national passing-yards leader).
- 3 CHANGELOG rows; 1 START HERE banner.

## State

| Metric | v0.6.2 AUTH | v0.7.8 | v0.7.9 |
|---|---|---|---|
| QB confidence codes populated | **0 / 138** | 138 / 138 | **138 / 138** |
| H / M / L | — | 64 / 43 / 31 | **65 / 40 / 33** |
| OK / UNCERTAIN | — | 100 / 38 | **99 / 39** |
| Blank / zero numerical | — | 38 / 100 | **39 / 99** |
| Nonzero QB values | 0 | 0 | **0** |
| Formula cells | 123,011 | 123,011 | **123,011** |
| Sheets | 21 | 21 | **21** |
| **QB verification backlog** | — | 0 | **0** |
| **Audit-trail gap (Tier-1 unstamped)** | — | 21 | **0** |

## Cumulative change vs the AUTHORITATIVE workbook

**1,249 cells · 0 formula changes**, confined to three sheets: QB VALUES (1,132),
CHANGELOG (116), START HERE (1). **Eighteen of twenty-one sheets are byte-identical.**

## Recommendation

**Promote v0.7.9 to AUTHORITATIVE**, subject to two conditions: (1) promote before the
openers while 0 market lines are loaded and the change is behaviorally inert; (2) pair
promotion with the first Phase 8.4 monitoring sweep, because the 33 L records are
perishable and depth charts land within three weeks. Not claimed: independent
verification of the 61 H-coded tier-2 records, which were never in scope.

## Constraints honored

v0.6.2 AUTHORITATIVE unmodified ✔ · v0.7.8 unmodified ✔ · Google Sheets never accessed ✔ ·
**nothing promoted** ✔ · no nonzero QB values created ✔ · no formula, tab, structure,
settings, threshold, schedule, source-weight or status-logic change ✔ · only QB dataset
fields updated ✔ · VSiN guide and VSiN database not accessed ✔ · no market lines,
no simulation, no Phase 8 work ✔.
