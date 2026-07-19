# v0.3.1 Extended Ranges — Exact Inventory

**v0.3.1 note:** Sections 1-4 below describe the original v0.3 build. Section
5 documents three corrections made on top of it for v0.3.1. IMPORT SCHEDULE
is **no longer** "untouched" as of v0.3.1 — see Section 5.1.

## 1. Row-range extension (840 games -> 1000 games, rows 6:845 -> 6:1005)

### Fully re-tiled game-anchored sheets (formulas filled for rows 846-1005, using
validated relative-row-shift of the row-845 template; all internal `845` boundary
references corrected to `1005`)
- **ENGINE** — columns A:AL (38 columns)
- **CLEAN** — columns A:AG (33 columns)
- **DASHBOARD** — columns A:Z (26 columns)
- **MARKET LINES** — formula columns B, O, P, Q, R (user-input columns A, C:N
  extended with matching cell style only, no formulas needed)
- **CALC** — game-side helper columns K:Z (16 columns; columns A:J are the
  per-team block and were not row-extended)

### Absolute range-boundary fixes (`...$845` -> `...$1005`), applied to every
existing row (6-845) and every newly-filled row (846-1005) in these specific
cells only:
| Sheet | Column | What it bounds |
|---|---|---|
| DASHBOARD | G | Market-line INDEX lookup |
| DASHBOARD | W | Priority RANK range |
| MARKET LINES | B | Matchup auto-lookup vs CLEAN |
| MARKET LINES | P | Favorite-valid check vs CLEAN |
| MARKET LINES | R | Duplicate-GameID-row counter |
| CLEAN | M | Self dup-count (`COUNTIF($A$6:$A$1005,...)`) |
| CALC | L | Market-line row MATCH |
| CALC | M | Favorite-resolved INDEX |
| CALC | N | Home-spread-signed INDEX |
| CALC | O | Market-total INDEX |
| CALC | P | Line-date INDEX |
| CALC | R | Duplicate-market-row flag |
| CALC | S | Pending-line flag |

### Team-anchored aggregation formulas (own row range 6:143 untouched — these
sum/count across all *games*, not across teams, so only their internal
boundary changes)
| Sheet | Column | Purpose |
|---|---|---|
| TEAM RATINGS | F | Effective-games-played sum across CLEAN |
| TEAM RATINGS | W | FBS-games-completed sum across CLEAN |
| CALC | B | perf_w_sum across CLEAN |
| CALC | C | w_sum across CLEAN |

### Fixed-row summary/counter formulas (own row position untouched — these are
single checklist rows, not per-game rows)
| Sheet | Column | Rows |
|---|---|---|
| DATA QUALITY | B | 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18 |
| AUDIT | B | 10, 11, 16, 19 |
| START HERE | C | 10, 12, 14 |

### Filters
- DASHBOARD autofilter: `$A$5:$Z$845` -> `$A$5:$Z$1005`

### Explicitly NOT touched in the original v0.3 build (confirmed via
full-workbook diff, 0 cell differences outside the zones above)
IMPORT SCHEDULE (pure paste zone, no formulas — **its own row dimension was
left at 1000 in v0.3; this was a defect, corrected in v0.3.1 Section 5.1
below**), IMPORT STATS, ADJUSTMENTS, QB VALUES, SETTINGS, PRESEASON,
FCS TIERS, HISTORY, BACKTEST, DICTIONARY — plus every non-boundary
formula/range on every touched sheet. IMPORT STATS, ADJUSTMENTS, QB VALUES,
SETTINGS, PRESEASON, FCS TIERS, HISTORY, BACKTEST, DICTIONARY remain
untouched as of v0.3.1 too.

## 2. TEAM MAP additions

### K:L — IMPORT alias table (rows 281-418, 138 new rows)
Every one of the 138 canonical FBS/FBS-reclassifying teams gets its exact
ESPN full display name mapped to its existing canonical abbreviation. No
abbreviation was created, renamed, or altered — see `alias_additions_report.tsv`
for the full 138-row list. Verified: 0 case-insensitive duplicates against
the existing 275 rows, 0 duplicates within the new 138, 0 conference
mismatches against each team's canonical conference.

### N — FBS conference-string list (rows 20-28, 9 new rows)
```
Atlantic Coast Conference
Big Ten Conference
Big 12 Conference
Southeastern Conference
Pac-12 Conference
American Conference
Mid-American Conference
Mountain West Conference
Sun Belt Conference
```
(Conference USA and FBS Independents already matched ESPN's exact strings
and needed no addition.)

## 3. CLEAN conference-lookup range extension
`CLEAN!O` and `CLEAN!Q` (FBS/FCS/BLOCK classification fallback) range
`'TEAM MAP'!$N$6:$N$25` -> `'TEAM MAP'!$N$6:$N$40`, applied to every row
6-1005, to make room for the 9 new conference strings without truncating.

## 4. Bug caught and fixed during build
Initial boundary-fix regex blindly replaced every standalone `845` with
`1005`, which also corrupted row 845's own **relative** self-references
(`$A845` -> `$A1005`) in addition to the intended **absolute** boundary
(`$A$845` -> `$A$1005`), in exactly 13 cells (row 845 only, across
CLEAN!M / DASHBOARD!G,W / MARKET LINES!B,P,R / CALC!L,M,N,O,P,R,S). Fixed by
restricting the regex to `$`-anchored occurrences only
(`(?<=\$)845(?!\d)`); re-verified zero absolute-boundary leaks and correct
row-845 self-references afterward. The same class of bug was independently
caught in the scratch-test build (row 14 self-reference) before it was
applied to the production file.

## 5. v0.3.1 corrections

### 5.1 IMPORT SCHEDULE physical row extension (was: "IMPORT SCHEDULE ...
untouched")
The v0.3 build correctly extended every *downstream* sheet's formulas to
row 1005, but IMPORT SCHEDULE itself has no formulas — it's the paste zone
— so nothing in the row-extension loop ever ran against it, and its own
`ws.dimensions` stayed at `A1:N1000`.

Fix: rows 1001-1005, columns A:N, now physically exist as real cells,
styled to match the existing blank paste-zone row (1000, `fill=none`,
`numfmt=General` except column D — see 5.2). Confirmed post-fix:
`IMPORT SCHEDULE.dimensions == 'A1:N1005'`.

Flow-through proof: in the compact scratch model (using the *exact* real
formulas, scaled to a 20-row boundary standing in for production's 1005), a
real game (Arkansas-Pine Bluff at Missouri) was placed at the model's exact
final row (20 — the direct analog of production row 1005) and live-
calculated:
```
IMPORT SCHEDULE!A20 = 401856663
CLEAN!A20  = 401856663   (id passthrough)
CLEAN!N20  = ""          (Arkansas-Pine Bluff: no alias, conf not in FBS list -> FCS, correct)
CLEAN!O20  = FCS
CLEAN!P20  = MIZ         (Missouri: resolves via IMPORT alias)
CLEAN!Q20  = FBS
ENGINE!A20 = 401856663
ENGINE!AI20 = BLOCKED    (expected - ratings not loaded in Phase 3, same as every other row)
ENGINE!AH20 = "HOME RATING MISSING; "
DATA QUALITY!B6 (games loaded) increased to include this row
DATA QUALITY!B7 (BLOCKED) increased to include this row
```
This confirms the row at the exact boundary edge flows through CLEAN,
ENGINE, and DATA QUALITY identically to every other row; AUDIT reads the
same 1005-extended ranges (already verified by formula-text validation) and
consumes the same per-row CLEAN/ENGINE outputs already proven correct.

### 5.2 start_date: text -> native date
IMPORT SCHEDULE!D6:D893 (888 cells): Python `str` `'2026-08-29'` ->
`datetime.date(2026, 8, 29)`, `number_format = 'yyyy-mm-dd'`. Verified
lossless for all 888 rows (`date.isoformat() == original CSV text`, 0
mismatches). `number_format = 'yyyy-mm-dd'` was also applied to D894:D1005
(the still-blank remainder of the paste zone) so future pasted dates
inherit correct formatting.

### 5.3 ENGINE!AL846:AL1005 style restoration
ENGINE!AL is the sheet's one hand-edited column (Notes input). The v0.3
row-extension loop copied style only when copying a formula; AL845 has no
formula (`value is None`), so the loop's `if ft is None: continue` guard
skipped it entirely for rows 846-1005, leaving them with default
(no-fill) styling instead of the yellow `FFFFF2CC` input-cell fill used by
AL6:AL845. A parallel gap was checked for and ruled out on ENGINE!U (a
genuine blank spacer column with no header and no styling anywhere in the
original workbook, rows 6-845 alike — not a bug).

Fix: `AL846:AL1005` font/border/fill/alignment/number-format/protection
copied from `AL845`. Confirmed post-fix: `AL846`, `AL900`, `AL1005` fill =
`FFFFF2CC`, matching `AL845`; `.value is None` for all of them (no formula
written).
