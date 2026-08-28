# Phase 6.2 — Exact Before-and-After Formula Report

## The repair (2 formula ranges, 2000 cells)

The DATA INCOMPLETE pathway defect was that blank Week and Date inputs
passed through `CLEAN!C` / `CLEAN!D` as numeric **0 / epoch date**, because
the formulas fell through to a **bare source reference**. A bare reference
to a blank cell evaluates to `0` (not `""`) in Excel/Google Sheets, so the
downstream check `OR($B6="",$C6="")` in `ENGINE!AI` could never recognise a
missing Week or Date, making DATA INCOMPLETE unreachable.

The repair wraps each source reference in an explicit blank guard so a
genuinely blank input propagates as blank `""` instead of `0`.

### CLEAN!C6:C1005 (Week)

**Before (all 1000 rows, byte-exact):**
```
=IF($A6="","",'IMPORT SCHEDULE'!C6)
```

**After (all 1000 rows):**
```
=IF($A6="","",IF('IMPORT SCHEDULE'!C6="","",'IMPORT SCHEDULE'!C6))
```

### CLEAN!D6:D1005 (Date)

**Before (all 1000 rows, byte-exact):**
```
=IF($A6="","",'IMPORT SCHEDULE'!D6)
```

**After (all 1000 rows):**
```
=IF($A6="","",IF('IMPORT SCHEDULE'!D6="","",'IMPORT SCHEDULE'!D6))
```

(Row 6 shown; every row 6→1005 is identical except the row number. The
build asserted each old formula byte-for-byte before overwriting;
`validate_v062.py` re-confirms every new formula.)

## Why this is the smallest safe correction

- The change is confined to the **fallthrough value** of the existing
  `IF($A6="",...)` guard. The outer guard, the referenced cells, and the
  cell's number format are all unchanged.
- The `="" ` test is not subject to the bare-reference-to-blank→0 quirk:
  comparing a blank cell to `""` reliably yields `TRUE` in both Excel and
  Google Sheets, while comparing a real value (including **Week 0**, since
  `0=""` is `FALSE`) yields `FALSE`. So blank → `""`, and every valid value
  (including 0) passes through untouched.
- A formula-produced `""` is preserved through a bare reference (unlike a
  physically blank cell), so it flows correctly through the two — and only
  two — downstream consumers, `ENGINE!B6:B1005` (`=IF($A6="","",CLEAN!$C6)`)
  and `ENGINE!C6:C1005` (`=IF($A6="","",CLEAN!$D6)`), which therefore did
  **not** need to change.

## Downstream logic (unchanged, shown for context)

```
ENGINE!B6  =IF($A6="","",CLEAN!$C6)                     (Week)
ENGINE!C6  =IF($A6="","",CLEAN!$D6)                     (Date)
ENGINE!AI6 =IF($A6="","",IF($AH6<>"","BLOCKED",
             IF($AG6<>"","FCS — NO PLAY",
             IF(CALC!$S6=1,"PENDING LINE",
             IF(CALC!$Q6=1,"STALE LINE",
             IF($AE6="QB UNCERTAIN","QB UNCERTAIN",
             IF($AF6<>"","TRANSITION UNCERTAIN",
             IF(OR($B6="",$C6=""),"DATA INCOMPLETE","READY")))))))))
```

No change was made to `ENGINE!B`, `ENGINE!C`, `ENGINE!AI`, or any other
formula.

## Dependency audit

A workbook-wide search found the **only** consumers of `CLEAN!C` and
`CLEAN!D` are `ENGINE!B` and `ENGINE!C` respectively (1000 cells each), both
already blank-safe passthroughs. No other sheet references these columns,
so no dependent formula required a change.

## Non-formula changes

| Change | Cell(s) | Before | After |
|---|---|---|---|
| Version banner | `START HERE!A1` | `...(v0.6.1 PHASE 6 CORRECTION + TEST-COMPLETION BUILD — PENDING APPROVAL)` | `...(v0.6.2 PHASE 6.2 DATA-INCOMPLETE PATHWAY REPAIR — PENDING APPROVAL)` |
| CHANGELOG | `CHANGELOG!A57:D57` | (empty) | one new `v0.6.2` row describing the repair |

## Total change set vs authoritative v0.6.1

2000 (CLEAN C+D) + 1 (banner) + 4 (CHANGELOG row A:D) = **2005 cell-level
changes**, with **0** number-format changes and **0** changes to sheet
count, sheet states, or the recalc-on-open setting. Proof:
`v0.6.2_vs_v0.6.1_cell_diff.tsv` and `validation_report_v062.txt`.
