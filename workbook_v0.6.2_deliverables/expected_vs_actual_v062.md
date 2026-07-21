# Phase 6.2 — Expected vs Actual Test Results

All values below are **actual calculated output** from the `formulas` engine running v0.6.2's own byte-exact formulas (compact real-formula harness). Raw output: `h62_raw_results.json`.

## 1. DATA INCOMPLETE repair (the fix)

| Test (G1 = NCST@UVA, row 8) | Expected | Actual | Result |
|---|---|---|---|
| Control: line + QBs resolved, Week 0 present | READY | **READY** (week=0) | PASS |
| Week blanked | DATA INCOMPLETE | **DATA INCOMPLETE** (week='') | PASS |
| Date blanked | DATA INCOMPLETE | **DATA INCOMPLETE** (date='') | PASS |
| Week restored to real value (0) | READY | **READY** (week=0) | PASS |

Week 0 is preserved as a real value (status READY), confirming the fix does not misread a legitimate Week 0 game as missing.

## 2. Stacked priority — DATA INCOMPLETE must never override a higher status

Each game below has a blank Week stacked on top of a higher-priority condition; the higher status must win.

| Game + stacked blank Week | Expected (higher status wins) | Actual | Result |
|---|---|---|---|
| G7: BLOCKED + blank Week | BLOCKED | **BLOCKED** | PASS |
| G3: PENDING LINE + blank Week | PENDING LINE | **PENDING LINE** | PASS |
| G1: QB UNCERTAIN + blank Week | QB UNCERTAIN | **QB UNCERTAIN** | PASS |
| G5: TRANSITION UNCERTAIN + blank Week | TRANSITION UNCERTAIN | **TRANSITION UNCERTAIN** | PASS |

## 3. Full single-condition status chain

| Game | Expected | Actual | Result |
|---|---|---|---|
| G7 | BLOCKED | **BLOCKED** | PASS |
| G6 | FCS — NO PLAY | **FCS — NO PLAY** | PASS |
| G3 | PENDING LINE | **PENDING LINE** | PASS |
| G2 | STALE LINE | **STALE LINE** | PASS |
| G1 | QB UNCERTAIN | **QB UNCERTAIN** | PASS |
| G5 | TRANSITION UNCERTAIN | **TRANSITION UNCERTAIN** | PASS |
| G1 (isolated, QBs resolved) | READY | **READY** | PASS |
| G1 (isolated, Week blanked) | DATA INCOMPLETE | **DATA INCOMPLETE** | PASS |

All eight statuses demonstrated; no lower-priority status overrode a higher one.

## 4. ADJUSTMENTS (no formula changed; v0.6.1 safety logic intact)

| Adjustment on G4 | Expected | Actual (Effective J / Flag K / margin O) | Result |
|---|---|---|---|
| valid +1.5 | no flag, Eff=1, margin=1.5 | J=1 / K='' / O=1.5 | PASS |
| oversized +999 | LARGE ADJ (>4), Eff=0, margin=0.0 | J=0 / K='LARGE ADJ (>4); ' / O=0.0 | PASS |
| non-numeric "abc" | VALUE NOT NUMERIC, Eff=0, margin=0.0 | J=0 / K='VALUE NOT NUMERIC; ' / O=0.0 | PASS |
| missing reason | REASON MISSING, Eff=0, margin=0.0 | J=0 / K='REASON MISSING; ' / O=0.0 | PASS |
| MARGIN OVERRIDE +15 (exempt) | no LARGE-ADJ flag, Eff=1, applies | J=1 / K='' / margin(R)/O=0.0 | PASS |

## 5. BET toggle (same READY fixture, qualifying edge)

| Toggle | Expected | Actual (status / edge / label) | Result |
|---|---|---|---|
| N | READY, INVESTIGATE | READY / edge=4.328571428571427 / INVESTIGATE | PASS |
| Y | READY, BET | READY / edge=4.328571428571427 / BET | PASS |

Only the toggle differs between the two; the edge is identical.

## 6. Transitional restriction (NDSU) — cannot BET while restriction active

| Check | Expected | Actual |
|---|---|---|
| NDSU effective games (F) | >4 (threshold exceeded) | 5.0 |
| NDSU review-cleared (TEAM RATINGS!X) | blank (nothing auto-sets it) | 'NOTFOUND' |
| G5 transitional flag | TRANSITIONAL | TRANSITIONAL |
| G5 status (line + QBs + toggle=Y) | TRANSITION UNCERTAIN | TRANSITION UNCERTAIN |
| G5 edge | large | 11.45614078674948 |
| G5 label | INVESTIGATE (never BET) | INVESTIGATE |

With 5 completed games, a large edge, a market line, and BET toggle = Y, NDSU still cannot reach BET — the restriction holds functionally.

## 7. FCS protection (market line on an FCS game)

| Check | Expected | Actual |
|---|---|---|
| G6 status (FCS game WITH a test line) | FCS — NO PLAY | FCS — NO PLAY |
| FCS flag | FCS OPP | FCS OPP |
| Spread edge | blank (no actionable number) | '' |
| Spread label | blank | '' |

A market line cannot override FCS — NO PLAY, and no actionable spread/edge/label is produced.

## 8. Prior-fade table (unchanged; all values + clamp)

| Effective games F | Expected weight | Actual | Result |
|---|---|---|---|
| 0 | 1.0 | 1.0 | PASS |
| 1 | 0.8 | 0.8 | PASS |
| 2 | 0.65 | 0.65 | PASS |
| 3 | 0.5 | 0.5 | PASS |
| 4 | 0.4 | 0.4 | PASS |
| 5 | 0.3 | 0.3 | PASS |
| 6 | 0.225 | 0.225 | PASS |
| 7 | 0.175 | 0.175 | PASS |
| 8 | 0.125 | 0.125 | PASS |
| 9 | 0.1 | 0.1 | PASS |
| 10 (beyond table) | clamps to F=9 (0.1) | 0.1 | PASS |

