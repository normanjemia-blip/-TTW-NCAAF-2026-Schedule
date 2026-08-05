# Phase 6 — Expected vs Actual Results

All results below are **actual calculated output** from a real
formula-evaluation engine (Python `formulas` library) running the
production workbook's own byte-exact formula text — not a manual trace.
Full raw output: `harness/harness_results_raw.json`.

## 1. Status-priority chain

Documented order:
`BLOCKED → FCS — NO PLAY → PENDING LINE → STALE LINE → QB UNCERTAIN → TRANSITION UNCERTAIN → DATA INCOMPLETE → READY`

| Game | Condition(s) present | Expected status | Actual status | Result |
|---|---|---|---|---|
| G7 (Akron@Wake Forest) | Invalid favorite (BLOCKED) | BLOCKED | **BLOCKED** | ✅ |
| G6 (Bethune-Cookman@UCF) | FCS opponent, no line, no QB, then WITH a test line added | FCS — NO PLAY (in both cases) | **FCS — NO PLAY** (both cases, identical) | ✅ line cannot override |
| G6 + duplicate GameID injected | FCS opponent AND a hard block | BLOCKED (outranks FCS — NO PLAY) | **BLOCKED** | ✅ priority holds |
| G3 (SJSU@USC) | No market line | PENDING LINE | **PENDING LINE** | ✅ |
| G2 (UNC@TCU) | Line entered 15 days before as-of (>5-day threshold) | STALE LINE | **STALE LINE** | ✅ |
| G1 (NCST@UVA), Variant A | Valid line, QBs unresolved (default) | QB UNCERTAIN | **QB UNCERTAIN** | ✅ |
| G4 (NMSU@FSU), Variant A/B/C | Valid line + adjustment, QBs unresolved | QB UNCERTAIN (adjustment does not bypass QB gate) | **QB UNCERTAIN** | ✅ |
| G5 (JVST@NDSU), Variant A | Valid line, QBs unresolved, NDSU transitional | QB UNCERTAIN (masks transitional) | **QB UNCERTAIN** | ✅ |
| G1, Variant B | QBs resolved for both teams | READY | **READY** | ✅ |
| G5, Variant B | QBs resolved for both teams, NDSU still not review-cleared | TRANSITION UNCERTAIN (revealed once QB stops masking it) | **TRANSITION UNCERTAIN** | ✅ |

**Conclusion: in every tested combination, a lower-priority condition
never overrode a higher-priority one.** BLOCKED beat FCS — NO PLAY;
FCS — NO PLAY was never overridden by a market line under any condition;
QB UNCERTAIN beat both TRANSITION UNCERTAIN and would-be READY until
resolved.

## 2. Line-entry, calculation, and label tests (item 1)

| Test | Expected | Actual | Result |
|---|---|---|---|
| Standard home game (G1), HFA | 2.5 | **2.5** | ✅ |
| Neutral-site game (G2), HFA | 0 | **0** | ✅ |
| Valid favorite + positive spread (G1, Favorite=UVA, Spread=6.5) | Accepted, resolves to home team | Resolved; Favorite valid=OK | ✅ |
| Valid total (G1, 51.5) | Accepted | Accepted, feeds team-total split | ✅ |
| Missing line (G3) | PENDING LINE, no edge/label | **PENDING LINE**, edge/label blank | ✅ |
| Stale line (G2) | STALE LINE, no label (even though an edge computes) | **STALE LINE**; edge=1.16 but label suppressed | ✅ |
| Invalid/incomplete line (G7, favorite="Ohio State" — not in this game) | BLOCKED, "INVALID FAVORITE" reason | **BLOCKED**, block reason = `"INVALID FAVORITE; "` | ✅ |
| QB UNCERTAIN (G1/G4/G5, Variant A) | Status=QB UNCERTAIN | **QB UNCERTAIN** on all three | ✅ |
| Temporarily-resolved QB (G1, G5 → Variant B) | Status changes once both teams' QBs are resolved | G1→READY, G5→TRANSITION UNCERTAIN | ✅ |
| TRANSITION UNCERTAIN (G5, Variant B) | Status=TRANSITION UNCERTAIN | **TRANSITION UNCERTAIN** | ✅ |
| FCS — NO PLAY (G6) | Status permanent regardless of line | **FCS — NO PLAY**, unaffected by a test line | ✅ |
| Line cannot override FCS — NO PLAY (G6 + test line 45.0/60.0) | No spread/total/edge/label/confidence computed despite the line | All blank; status unchanged | ✅ |
| Manual adjustment, valid reason (G4, +1.5, Active=Y) | Effective=1, no flags, margin shifts by +1.5 | Effective=1, Flags=blank, `ENGINE!O`(manual adj)=**1.5** | ✅ |
| Oversized adjustment (G4 isolated, +999, Active=Y) | Flagged "LARGE ADJ (>4)"; **not auto-blocked** — applies fully | Flag=`"LARGE ADJ (>4); "`; margin included **999.0** in full | ✅ confirmed design (flag, not block — see note below) |
| Non-numeric adjustment (G4 isolated, "abc", Active=Y) | Flag shows "VALUE NOT NUMERIC" | **`#VALUE!` error** instead — see defect below | ❌ **DEFECT FOUND** |
| Home-field / neutral-site calc | 2.5 / 0 | 2.5 / 0 | ✅ (dup of above, listed per your item) |
| Spread edge, total edge, team totals, labels, confidence, priority (G1, Variant B, READY) | All compute; DASHBOARD priority/rank populated | Edge=-1.17, label=LEAN, confidence=2.0, DASHBOARD priority=3.17, rank=1 | ✅ |
| BET toggle OFF vs ON (G5, edge≈3.96, Variant B vs C) | INVESTIGATE when OFF, still INVESTIGATE here (edge doesn't clear BET's 3.0 requirement alone — toggle is necessary but not sufficient without READY status) | Both variants: INVESTIGATE (G5 is TRANSITION UNCERTAIN, never READY, so BET is correctly unreachable regardless of toggle) | ✅ toggle+status interaction confirmed |
| Threshold boundaries 1.0/1.5/3.0 (isolated formula test) | 0.99→none, 1.00→LEAN, 1.49→LEAN, 1.50→INVESTIGATE, 2.99→INVESTIGATE, 3.00→BET, 3.01→BET | Exact match on all 7 boundary values | ✅ |

## 3. Weekly-rating-workflow tests (item 2)

| Test | Expected | Actual | Result |
|---|---|---|---|
| FBS-vs-FBS completed game → effective games | Both teams +1.0 | NCST, UVA, USC, SJSU all **F=1.0** | ✅ |
| FBS-vs-FCS completed game → effective games | FBS side +0 (not partial 0.5) | UCF (played FCS Bethune-Cookman) **F=0.0** | ✅ |
| Prior-fade weight at F=1 | 0.80 (SETTINGS!C38) | **G=0.8** for all F=1 teams | ✅ |
| Prior-fade weight at F=0 | 1.00 (SETTINGS!C37) | **G=1.0** for UCF | ✅ |
| Weekly movement cap | Exactly ±2.5, even for large swings | NCST: raw blend wanted to move from -20.0 to 1.51 (Δ21.5); capped output = **-17.5** (exactly J+2.5) | ✅ |
| NDSU/Sacramento State safeguards | Unaffected by completed-game/stats fixtures | `TEAM RATINGS!D114/D122`="Y" (unaffected); review-cleared still blank | ✅ |
| Missing/unmatched stats | "UNMATCHED" flag, not a guessed abbreviation | `IMPORT STATS!K8`=**"UNMATCHED"**; `DATA QUALITY!B16`=**1** | ✅ |

## 4. Genuine formula defect found — documented, NOT repaired

**Cell range:** `ADJUSTMENTS!K6:K255` (Flags, auto-computed)

**Current formula (unchanged in delivered v0.6):**
```
=IF($A6="","",IF($D6="","REASON MISSING; ","")&IF(NOT(ISNUMBER($C6)),"VALUE NOT NUMERIC; ","")&IF(AND(ISNUMBER($C6),ABS($C6)>4,$A6<>"MARGIN OVERRIDE",$A6<>"TOTAL OVERRIDE"),"LARGE ADJ (>4); ",""))
```

**Expected behavior:** when the adjustment's Value (column C) is
non-numeric, the Flags cell shows a clean, readable
`"VALUE NOT NUMERIC; "` message.

**Actual behavior (confirmed with a real formula-calculation engine, and
independently verified this is standard Excel/Google Sheets behavior —
`AND()` evaluates every argument eagerly, it does not short-circuit):**
`ABS($C6)` is evaluated as part of the second `AND(...)` term even when
`ISNUMBER($C6)` is `FALSE`. `ABS()` on non-numeric text always produces a
`#VALUE!` error in Excel/Sheets, and that error propagates through the
`AND()`, then through the `&` string concatenation, replacing the
**entire** Flags cell with `#VALUE!` instead of the intended message.
This also corrupts `DATA QUALITY!B15`'s flagged-row count for any row
affected, since `SUMPRODUCT` over a range containing an error cell
itself errors.

**Proposed correction (documented only — not applied to any file):**
```
=IF($A6="","",IF($D6="","REASON MISSING; ","")&IF(NOT(ISNUMBER($C6)),"VALUE NOT NUMERIC; ","")&IF(ISNUMBER($C6),IF(AND(ABS($C6)>4,$A6<>"MARGIN OVERRIDE",$A6<>"TOTAL OVERRIDE"),"LARGE ADJ (>4); ",""),""))
```
The `ABS($C6)>4` check is moved inside an `IF(ISNUMBER($C6), ...)` gate
so it is never evaluated when `C6` isn't numeric, avoiding the eager-`AND`
problem entirely.

**Practical impact:** low. A non-numeric adjustment value is an unusual
manual-entry mistake (typing "abc" instead of a number); the delivered
workbook ships with 0 adjustments, so this does not affect the current
state. It would only surface if a future user mistypes a Value cell.

**Per your explicit instruction, this was documented and not silently
repaired — no v0.6.1 was created.** It is also recorded in the workbook's
own CHANGELOG (v0.6 entry) so it is visible without this external report.

## 5. Related, non-defect behavioral finding

An **oversized** adjustment (e.g. +999, still numeric, Active=Y) is
**not auto-blocked or capped by any formula** — it is flagged
`"LARGE ADJ (>4); "` for visibility, but the full value is still summed
into the game's margin (`ENGINE!O`). This matches the workbook's
documented design philosophy ("manual review still required — never
auto-clears"), so it is not treated as a defect, but it's called out
explicitly here since it's easy to assume a "flag" implies a "block."
The weekly review step (`DATA QUALITY!B15` / `START HERE` step 7) is the
only safeguard against an oversized adjustment being applied — not an
automatic cap.

## 6. Cross-check: `formulas`-engine `SUMPRODUCT(--(...))` limitation
   (already known, re-encountered)

`DATA QUALITY!B15` (`SUMPRODUCT(--(ADJUSTMENTS!$K$6:$K$255<>""))`) was
observed returning `0` in one harness run where a flagged row genuinely
existed. This is the **same documented limitation of the open-source
`formulas` verification library** first identified during the Phase 3
row-extension work (the `--` double-unary-negate idiom over a range with
blanks returns 0 in this library; the mathematically identical `*`-based
version returns the correct value on identical data) — not a workbook
defect, and not the same issue as the `#VALUE!` finding above (which was
independently confirmed via a standalone `ABS("text")` probe outside the
`formulas` engine's SUMPRODUCT path). Ground truth for flagged-row counts
in this report was taken from direct cell inspection, not the
library's SUMPRODUCT evaluation.
