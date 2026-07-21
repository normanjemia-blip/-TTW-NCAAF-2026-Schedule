# DATA INCOMPLETE — Second Genuine Formula Defect Found During Testing

While completing the isolated DATA INCOMPLETE test you requested (item 3),
building it exposed a **second genuine formula defect**, distinct from
the ADJUSTMENTS!K one fixed in this build. Documented per your standing
instruction ("if a genuine formula defect is discovered... document...
then stop" — this was NOT authorized for repair this round, and was not
repaired; only the ADJUSTMENTS!K/J fixes you explicitly authorized were
applied).

## What the test did

Using G1 (NC State @ Virginia, GameID `401858202`, IMPORT SCHEDULE row
8), with a valid market line entered and both teams' QBs temporarily
resolved (so no higher-priority status could mask the result):
1. **Control run**: unmodified row → confirmed **READY** (as expected;
   this also re-confirms the fix didn't disturb the READY path).
2. **Test run**: `IMPORT SCHEDULE!C8` (week) temporarily set to blank —
   expected **DATA INCOMPLETE** per `ENGINE!AI`'s documented logic
   (`OR($B6="",$C6="")`).
3. **Restore**: `C8` set back to its exact original value, `0` (Week 0 —
   confirmed via direct inspection before the test, not assumed).

## What actually happened

The test run still returned **READY**, not DATA INCOMPLETE.

## Root cause (confirmed with isolated formula probes, matching standard
   Excel/Google Sheets semantics — not a verification-tool artifact)

**Cell range:** `CLEAN!C6:C1005` (week) and `CLEAN!D6:D1005` (date)

**Current formula (unchanged in this build):**
```
CLEAN!C6: =IF($A6="","",'IMPORT SCHEDULE'!C6)
CLEAN!D6: =IF($A6="","",'IMPORT SCHEDULE'!D6)
```

**Expected behavior:** if the source cell (`IMPORT SCHEDULE!C6` or `D6`)
is blank, `CLEAN!C6`/`D6` should propagate as blank/`""`, so
`ENGINE!AI`'s `OR($B6="",$C6="")` check correctly detects it.

**Actual behavior:** when `$A6` (GameID) is non-blank, the formula falls
through to a **bare cell reference** (`'IMPORT SCHEDULE'!C6`, not wrapped
in its own blank check). In Excel/Google Sheets, a direct reference to a
blank cell evaluates to **`0`**, not `""` — confirmed with two isolated
probes reproducing this exact pattern outside the production file. Since
`0 <> ""`, `ENGINE!AI`'s `OR($B6="",$C6="")` check can **never** be
satisfied for a row with a valid GameID. **DATA INCOMPLETE is
unreachable dead code for a missing week or missing date field.** A row
with a genuinely missing week silently displays `Week 0` — indistinguishable
from a real Week 0 game — and a missing date silently displays the spreadsheet
epoch date, instead of being flagged.

**Proposed correction (documented only — not applied to any file):**
```
CLEAN!C6: =IF($A6="","",IF('IMPORT SCHEDULE'!C6="","",'IMPORT SCHEDULE'!C6))
CLEAN!D6: =IF($A6="","",IF('IMPORT SCHEDULE'!D6="","",'IMPORT SCHEDULE'!D6))
```
Nesting an explicit blank check around the source reference lets a
genuinely blank field propagate as `""`, which is all `ENGINE!AI`'s
existing (unchanged) DATA INCOMPLETE check needs to work correctly — no
change to `ENGINE!AI` itself would be required.

## Consequence for the status-priority-chain revalidation (item 3)

All 7 other statuses were re-confirmed against this build's formulas
(unchanged from v0.6 except ADJUSTMENTS): BLOCKED, FCS — NO PLAY,
PENDING LINE, STALE LINE, QB UNCERTAIN, TRANSITION UNCERTAIN, READY — see
`expected_vs_actual_results_v061.md`. **DATA INCOMPLETE could not be
positively demonstrated**, because doing so surfaced the defect above
rather than the intended status. This is reported honestly rather than
fabricated. The restore step was still completed and verified exact.
