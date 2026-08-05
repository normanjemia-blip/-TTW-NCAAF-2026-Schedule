# PROMOTION MANIFEST — TTW NCAAF Power Ratings 2026

**Promotion date:** 2026-08-04 (America/New_York)
**Action:** v0.6.2 AUTHORITATIVE → **v0.8.0 AUTHORITATIVE**
**Basis:** `TTW_NCAAF_Power_Ratings_2026_v0.7.9_CANDIDATE.xlsx`, promoted **byte-for-byte**

## New authoritative version

| Field | Value |
|---|---|
| **Version** | **v0.8.0 AUTHORITATIVE** |
| **File** | `promotion_v0.8.0/TTW_NCAAF_Power_Ratings_2026_v0.8.0_AUTHORITATIVE.xlsx` |
| **SHA-256** | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` |
| Size | 3,010,398 bytes |
| Sheets | 21 |
| Formula cells | 123,011 |

**The promoted file is byte-identical to `v0.7.9_CANDIDATE` (`cmp` clean, same SHA-256).**
Promotion is a designation, not a rebuild. **No cell was changed to promote it.**

## Version lineage

| Version | SHA-256 | Role after promotion |
|---|---|---|
| v0.6.2 | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` | **SUPERSEDED** — retained as rollback target |
| v0.7.2 – v0.7.8 | see each candidate's MANIFEST.md | ARCHIVED — intermediate candidates |
| v0.7.9 | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` | ARCHIVED — promotion basis |
| **v0.8.0** | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` | **AUTHORITATIVE** |

## What changed vs v0.6.2

**1,249 cells · 0 formula changes · 3 sheets.**

| Sheet | Cells changed | XML part |
|---|---:|---|
| QB VALUES | 1,132 | `xl/worksheets/sheet6.xml` — differs |
| CHANGELOG | 116 | `xl/worksheets/sheet21.xml` — differs |
| START HERE | 1 | `xl/worksheets/sheet1.xml` — differs |
| **All other 18 sheets** | **0** | **byte-identical OOXML parts** |

Only 4 of 29 zip parts differ: the three sheets above plus `docProps/core.xml` (save
metadata). **18 of 21 worksheet XML parts are byte-identical to the authoritative
workbook** — a stronger result than cell-level equality.

## Per-sheet formula counts — identical, both workbooks

| Sheet | Formulas | | Sheet | Formulas |
|---|---:|---|---|---:|
| START HERE | 8 | | TEAM MAP | 476 |
| DASHBOARD | 26,000 | | CLEAN | 33,000 |
| ENGINE | 36,000 | | CALC | 17,104 |
| MARKET LINES | 5,000 | | AUDIT | 15 |
| ADJUSTMENTS | 500 | | SETTINGS | 0 |
| QB VALUES | 552 | | IMPORT SCHEDULE | 0 |
| TEAM RATINGS | 2,208 | | FCS TIERS | 0 |
| DATA QUALITY | 16 | | HISTORY | 0 |
| IMPORT STATS | 200 | | BACKTEST | 0 |
| PRESEASON | 1,932 | | DICTIONARY / CHANGELOG | 0 |
| | | | **TOTAL** | **123,011** |

## QB dataset state

| Metric | v0.6.2 | **v0.8.0** |
|---|---|---|
| Confidence codes populated | **0 / 138** | **138 / 138** |
| H / M / L | — | **65 / 40 / 33** |
| QB status | **138 UNCERTAIN** | **99 OK / 39 UNCERTAIN** |
| Blank / zero numerical inputs | — | 39 / 99 |
| **Nonzero QB values** | **0** | **0** |
| **Nonzero QB deltas** | **0** | **0** |
| Tier-1 records verified and stamped | 0 / 73 | **73 / 73** |

## Invariants preserved

`SETTINGS!B3` = 2026 · `SETTINGS!B6` = 2.5 HFA · `SETTINGS!B11` = "N" (BET off) ·
138 unique teams · 21 sheets, order and visibility unchanged · defined names identical ·
conditional formatting and data validation identical on every sheet ·
`ENGINE!M`, `ENGINE!AE`, `ENGINE!AI`, `QB VALUES!G`, `QB VALUES!M` byte-identical ·
0 market spreads loaded (pristine preseason state).

## Audit artifacts

`workbook_v0.7.9_candidate/promotion_audit_log.txt` (parts 1),
`promotion_audit_log3.txt` (part 3, corrected), `verification_log_v079.txt`,
`diff_v062_to_v079.csv`, `qb_inventory_v079.json`.
