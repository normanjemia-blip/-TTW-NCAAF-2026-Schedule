<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_power.py
     Source:   2026 VSiN College Football Betting Guide;
               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->

# Workbook Provenance — what was read, and what could not be

> **The v0.8.1 AUTHORITATIVE workbook is frozen and was opened read-only.** Nothing in Phase 6 writes to it, recalculates it or proposes a change to it.

| | |
| --- | --- |
| File | `TTW_College_Football_Power_Ratings_v0.8.1_AUTHORITATIVE.xlsx` |
| Git branch | `claude/2026-ncaaf-schedule-build-by6j5n` |
| Git path | `promotion_v0.8.1/` |
| Git blob | `06d817cdaa2814aa71630c5637d90af978c17b98` |
| SHA-256 | `e2da9a4c28bd5c0f094ab06a2a85d3e31b37c2aba894f97f3415e15f799cdfd6` |
| Opened | read-only, never re-saved |
| Sheets | 21 |
| Team rows read | 138 |

## What could not be read, and why it matters

`TEAM RATINGS!EFFECTIVE RATING` holds a cached value for **0 of 138** teams. The workbook was written programmatically and has never been recalculated by a spreadsheet application, so every computed cell is a formula with no stored result.

The consequence is stated rather than worked around: **no TTW rating exists to be read.** Every TTW figure in Phase 6 is derived by reimplementing the workbook's own printed formulas over its stored inputs, and is labelled TTW DERIVED wherever it appears. A reader who wants the workbook's own numbers must open and recalculate the workbook, which this phase does not do.

## What was read

| Sheet | Read |
| --- | --- |
| `TEAM MAP` | abbreviation, canonical name, conference, status |
| `PRESEASON` | stored source inputs with dates and citation URLs |
| `SETTINGS` | every weight and threshold |
| `TEAM RATINGS` | checked for cached values; none present |

## Source coverage found

| Column | Numeric rows |
| --- | --- |
| `sp_raw` | 138/138 |
| `fpi_raw` | 138/138 |
| `ttw25_raw` | 0/138 |
| `tr_raw` | 138/138 |
| `vsin_raw` | 0/138 |

## Canonical identity

The join between the workbook and this library reuses the Phase 4 abbreviation bijection rather than matching on names — the two artefacts spell teams differently (`UConn` against `Connecticut Huskies`, `Ole Miss` against `Mississippi`), and a name-matched join is exactly the failure mode that map exists to prevent. The join is asserted to cover all 138 at build time.

## Cross-links

- [Scale reconciliation](00_SCALE_RECONCILIATION.md) · [VSiN import candidate](00_VSIN_IMPORT_CANDIDATE.md)
