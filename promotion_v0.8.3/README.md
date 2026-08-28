# v0.8.3 AUTHORITATIVE — GO-LIVE GUARDRAIL PATCH

**Promotion date:** 2026-08-18 (America/New_York)
**Predecessor:** v0.8.2 AUTHORITATIVE — **frozen and unmodified**
**Change class:** AUDIT invariant replacement + version identifier

| | |
|---|---|
| **Workbook** | `promotion_v0.8.3/TTW_College_Football_Power_Ratings_v0.8.3_AUTHORITATIVE.xlsx` |
| **SHA-256** | `ff55782586ef1adb662eba59710e824dc382769a24579e48917b101fbcdd96b8` |
| **Predecessor SHA-256** | `225085449b5a1db5903a3998cb909be1f7ae0037782ea65d412bcb4d9d9490d0` (frozen) |
| **Certificate** | `verify_v083.py` — **42 passed, 0 failed** |

---

## 1. The problem

`AUDIT!B16` asserted that **MARKET LINES must be empty**:

```
=IF(COUNTIF('MARKET LINES'!$A$6:$A$1005,"?*")+COUNT('MARKET LINES'!$A$6:$A$1005)=0,
    "OK — clean","REMOVE TEST LINES")
```

That was correct for a preseason deliverable that had to ship clean. It is
**backwards for go-live**: the moment real Week 0 lines are entered, the workbook's
own structural audit reports a failure. An audit that fails when the system is used
correctly trains its operator to ignore it, which is worse than having no audit.

## 2. The replacement

The invariant now checks that every populated market row is *operationally valid*,
and passes when there are none.

A row is **valid** when:

| Requirement | Enforced by |
|---|---|
| resolves to a scheduled GameID | `P = "OK"` |
| favorite is one of that game's two teams | `P = "OK"` |
| spread is numeric **and strictly positive** | `ISNUMBER(D)` and `D > 0` |
| total is numeric | `ISNUMBER(E)` |
| source present | `Q = ""` |
| line date present | `Q = ""` |
| no duplicate GameID | `Q = ""` |
| no flag of any kind | `Q = ""` |

**Why it anchors on `P = "OK"` and not on `Q` alone.** Column `Q` never flags a
**blank favorite**: `P` short-circuits to `""` when `O` is empty, so `Q`'s
`INVALID FAVORITE` and `GAMEID NOT IN SCHEDULE` branches never fire. A row with a
GameID, spread, total, source and date but **no favorite at all** would sail past a
`Q = ""` check. Requiring `P = "OK"` closes that hole. The fixture
`3.x defect caught: favorite blank` exists specifically to hold that closed.

`Q` alone also cannot enforce **positive numeric** spread or **numeric** total — it
only tests for blankness, so `-7.5`, `0` and the text `"7.5"` would all pass.

## 3. Exactly three cells

Full detail in `diff_v082_to_v083.csv`. **One formula change, by design: `AUDIT!B16`.**

| Sheet | Cell | Class |
|---|---|---|
| START HERE | `A1` | documentation — version identifier only |
| AUDIT | `A16` | label — renamed to its operational meaning |
| AUDIT | `B16` | **formula** — the invariant itself |

`AUDIT!E1`, the failing-invariant count, is **unchanged**. It counts
`"FAIL*"`, `"REMOVE TEST LINES"` and `"CHANGED*"`; the new B16 emits `FAIL — …` on
failure, which `"FAIL*"` already matches. The `"REMOVE TEST LINES"` term is now dead
but harmless, and leaving it keeps the diff to three cells.

## 4. What is deliberately NOT here

**The eight live Week 0 Circa rows are not in this workbook.** They are transient
working-copy data. The repository artifact ships with `MARKET LINES` **blank**, and
`verify_v083.py` check 2.4 enforces that so a future build cannot quietly commit a
week's lines into the archive.

Every model formula, rating, QB value, setting and safeguard is preserved:
ENGINE, QB VALUES, TEAM RATINGS, PRESEASON, CALC and MARKET LINES formulas are
identical to v0.8.2; QB census 38 UNCERTAIN / 100 OK; confidence 65 H / 41 M / 32 L;
nonzero QB values 0; BET toggle `N`; totals unavailable; NDSU and Sacramento State
transitional.

## 5. The guardrail is tested, not just asserted

A guardrail that has only ever returned OK has not been tested. `verify_v083.py`
re-implements the `P`/`Q`/`R`/`B16` chain and drives it with fixtures:

- zero rows → **OK**
- eight valid Week 0 Circa rows → **OK — 8 line(s) valid**
- thirteen defect fixtures, each → **FAIL**: GameID not in schedule · favorite blank ·
  favorite not in that game · spread negative · spread zero · spread non-numeric ·
  spread missing · total missing · total non-numeric · source missing · date missing ·
  duplicate GameID · stale line
- a fresh line inside the stale window → **OK**

## 6. Files

| File | Role |
|---|---|
| `TTW_College_Football_Power_Ratings_v0.8.3_AUTHORITATIVE.xlsx` | the workbook |
| `build_v083.py` | deterministic build from frozen v0.8.2 |
| `verify_v083.py` | promotion certificate — **read-only**, with defect fixtures |
| `make_v083_artifacts.py` | generates the diff CSV and regression log explicitly |
| `diff_v082_to_v083.csv` | the three-cell diff |
| `regression_log_v083.txt` | captured verifier output |

## 7. Rollback

Point current-state references back at
`promotion_v0.8.2/…v0.8.2_AUTHORITATIVE.xlsx` (`22508544…90d0`). The old invariant
returns, and the workbook will again report a failing audit as soon as any market
line exists. No model output is affected either way — this patch changes one audit
formula and touches nothing the engine reads.
