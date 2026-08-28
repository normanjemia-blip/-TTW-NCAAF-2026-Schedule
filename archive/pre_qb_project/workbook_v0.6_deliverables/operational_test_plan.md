# TTW NCAAF Power Ratings 2026 — Phase 6 Operational Test Plan

Base: approved **v0.5.2** (unmodified; the native Google Sheet, ID
`1U_QMDw_vpsHSTncvNVHvaiA9hjjvll2Wjvmqy8d5PS4`, was also never opened or
edited). This is controlled end-to-end testing and workflow validation
only — no new rating sources, no additional QB research, no real market
lines, no model redesign. Phase 7 not started.

## Why two separate test artifacts, not one

No spreadsheet-calculation engine is available in this session that can
recalculate the full ~1,000-row, 21-sheet production file at reasonable
cost (LibreOffice headless conversion was attempted first and confirmed
non-functional in this sandbox — fails even on a trivial one-line text
file — so a real Excel/Sheets recalculation of the full-scale workbook
was not available). Two complementary artifacts were built instead,
matching the methodology already validated and used successfully in
Phases 3 and 5:

1. **A compact real-formula test harness** (`harness/`) — every formula
   cell is extracted **byte-for-byte** from `v0.6_working.xlsx` (never
   invented or approximated) and placed at its **original row/column
   position** in a smaller workbook containing all 138 real team rows
   (so INDEX/MATCH lookups behave exactly as in production) plus the 7
   real game rows used for testing. This is run through the open-source
   `formulas` Python engine to get **actual calculated results**, not a
   manual trace.
2. **A full-scale test-applied copy** (`fixtures/v0.6_test_applied...xlsx`)
   — the same fixtures written into an actual complete copy of the
   workbook, so a human can open it (e.g. import into Google Sheets,
   which *can* fully recalculate it) and see the same behavior directly.
   This copy is **not** the delivered file — see Cleanup below.

Every synthetic value in both artifacts is tagged
`TEST ONLY — NOT REAL DATA` in a Source/Notes/Reason field.

## Fixture design (`test_fixtures.json`)

7 real schedule rows were selected (never invented GameIDs):

| Tag | Game | Row | Purpose |
|---|---|---|---|
| G1 | NC State @ Virginia | 8 | Main line-entry test: valid favorite/spread/total, HFA=2.5, edges/labels/confidence/priority, BET toggle |
| G2 | North Carolina @ TCU (neutral, Dublin) | 6 | Neutral-site HFA=0, stale-line test |
| G3 | San José State @ USC | 9 | Missing-line test (no MARKET LINES row entered) |
| G4 | New Mexico State @ Florida State | 10 | QB UNCERTAIN, temporarily-resolved QB, manual/oversized/non-numeric adjustment tests |
| G5 | Jacksonville State @ North Dakota State | 11 | TRANSITION UNCERTAIN (NDSU, reclassifier) |
| G6 | Bethune-Cookman @ UCF | 14 | FCS — NO PLAY + "a line cannot override it" proof |
| G7 | Akron @ Wake Forest | 15 | Invalid/incomplete line (bad favorite → BLOCKED) |

Five harness variants isolate independent conditions so results aren't
cross-contaminated (an early draft mixed a valid +1.5 adjustment with a
+999 "oversized" one on the same game and produced a nonsensical
1000+-point margin — caught by the results themselves looking wrong, and
fixed by isolating each adjustment test to its own variant):

- **A** — lines entered on 6 of 7 games (G3 deliberately has none), one
  valid adjustment on G4, QB VALUES completely empty (matches real
  default state).
- **B** — same as A, plus QBs temporarily resolved for G1's and G5's
  teams only (G4's teams stay unresolved on purpose).
- **C** — same as B, plus BET toggle = Y.
- **D** — G4 gets *only* an isolated oversized (999-point) adjustment.
- **E** — G4 gets *only* an isolated non-numeric ("abc") adjustment.

A sixth, separate harness (`weekly_harness.xlsx`) tests the weekly-rating
workflow: 2 completed FBS-vs-FBS games + 1 completed FBS-vs-FCS game
(synthetic scores), a 3-row IMPORT STATS paste (2 matched teams + 1
deliberately misspelled/unmatched team), and a HISTORY prior-week
snapshot set intentionally far from the new blended rating to exercise
the ±2.5 movement cap.

A seventh, isolated harness (`threshold_test.xlsx`) feeds the real
`ENGINE!X` (spread-label) formula synthetic edge values directly at the
exact boundary points (0.99/1.00/1.49/1.50/2.99/3.00/3.01), which is
more precise and reliable than trying to engineer a real market line
that happens to produce an exact boundary edge.

## What was explicitly out of scope (per your instructions) and was not
   done

No new preseason rating source was added. No QB starter research was
conducted (QB VALUES stays exactly as approved — 0/138 loaded). No real
market line was entered anywhere in the delivered file. No formula was
redesigned; the one genuine defect found (see
`expected_vs_actual_results.md`) was documented, not repaired, and no
v0.6.1 was created.

## Cleanup methodology

A scripted cleanup pass (`fixtures/cleanup_script.py`) reverses every
fixture on a copy of the test-applied file — clearing only the exact
manual-input cells that were written to (never a whole column range,
after an earlier draft's bug of clearing formula columns like
`MARKET LINES!B`, `ADJUSTMENTS!J:K`, `QB VALUES!G` was caught by the
diff proof below and fixed), and restoring — not blanking — the two
`IMPORT SCHEDULE` cells that had genuine non-blank original values
(`L`=`FALSE`, `N`=an ESPN source note) before the test fixture overwrote
them. The result, `proof_of_removal/v0.6_test_cleaned...xlsx`, is proven
**cell-by-cell identical (0 differences, all 21 sheets)** to the approved
`v0.5.2` baseline — see `proof_of_removal/cell_diff_proof.txt`.

The delivered `v0.6_working.xlsx` was never touched with test data in
the first place (confirmed identical to `v0.5.2` before the Phase 6
CHANGELOG/banner update was applied) — the cleanup proof above was
produced on the separate test-applied copy specifically to validate that
the removal *procedure* is correct and complete, in case it's needed for
a future round of operational testing against the live production file.

## Full deliverables inventory

See `README.md` in this directory for the file-by-file index.
