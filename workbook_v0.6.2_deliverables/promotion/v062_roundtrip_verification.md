# TTW NCAAF Power Ratings v0.6.2 — Native Google Sheets Promotion Verification

**Result: PASS**  
**Promotion date:** 2026-07-21  
**Native Sheet ID:** `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc`  
**Source SHA-256:** `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd`

## Verified

- New native Google Sheet is separate from v0.6.1.
- 21 sheets preserved in the same order with identical visible/hidden states.
- 123,011 formula cells preserved at the same coordinates.
- All formula semantics match the approved source.
- `CLEAN!C6:C1005` and `CLEAN!D6:D1005` preserve all 2,000 repaired nested blank-guard formulas exactly.
- `ADJUSTMENTS!J6:J255` is exact; `K6:K255` is semantically unchanged after Google shared-formula compression.
- `START HERE!A1` contains v0.6.2 and the v0.6.2 CHANGELOG entry is exact.
- Native calculation results: 888 games, 761 PENDING LINE/FBS-vs-FBS, 127 FCS — NO PLAY, 0 BLOCKED, 0 DATA INCOMPLETE, 0 audit failures.
- Input state: 0 market lines, 0 adjustments, 0 in-season stats; BET toggle = N.
- Zero substantive constant-value differences.

## Accepted Google package-level differences

- Google represented 26,618 formula cells as followers of 40 shared-formula groups. Formula count, locations, and semantics are unchanged.
- 3,168 numeric values were normalized in XML serialization (`5` → `5.0`, floating tails → equivalent decimals); no substantive values changed.
- The exported round-trip XLSX omits the source package's `calcPr/fullCalcOnLoad` metadata. The native Google Sheet recalculated successfully and all computed audit outputs are correct.
