# 1.5-POINT SPREAD THRESHOLD AUDIT — READ-ONLY

> **No formula and no setting was altered.** This is an audit plus a cell-level proposal.
> Reproduce with `python3 live_sync_v0.8.8/threshold_audit.py` against authoritative v0.8.8.

**Owner's intended rule:** SPREADS ONLY — absolute ATS edge **≥ 1.5 = BET**, below 1.5 = not BET.
Totals are **not** covered and no totals threshold has been approved.

---

## 1. Verdict

> **The intended rule is NOT implemented — and it cannot be implemented by changing one cell,
> because the spread thresholds are shared with the totals market.**

Two independent reasons an edge of exactly **±1.50 does not return BET today**:

1. `ABS(1.50) < SETTINGS!B10` (3.0) → **INVESTIGATE**
2. `SETTINGS!B11` is `"N"`, not `"Y"` → **INVESTIGATE regardless of edge**

**With the toggle at `N`, `BET` is currently unreachable at any edge whatsoever.** Verified: no value
in {±1.5, 3, 10, 50} produces `BET`.

---

## 2. Every cell controlling spread classification

| Cell / range | Role | Current |
|---|---|:--:|
| `SETTINGS!B8` | LEAN threshold (abs edge) | **1.0** |
| `SETTINGS!B9` | INVESTIGATE threshold (abs edge) | **1.5** |
| `SETTINGS!B10` | **BET threshold (abs edge)** | **3.0** |
| `SETTINGS!B11` | BET labels toggle (Y/N) | **`N`** |
| `ENGINE!V6:V1005` | Spread EDGE `= R + T` | — |
| `ENGINE!W6:W1005` | Side (sign of V) | — |
| `ENGINE!X6:X1005` | **Spread label** — consumes B8, B9, B10, B11 | — |
| `ENGINE!AI6:AI1005` | STATUS gate (BLOCKED / PENDING LINE / STALE LINE / QB UNCERTAIN / …) | — |
| `ENGINE!AF`, `AG` | transitional flag, FCS flag — force INVESTIGATE | — |
| `DASHBOARD!K6:K1005` | visible spread label ← `ENGINE!X` | — |
| `DASHBOARD!J6:J1005` | side ← `ENGINE!W` | — |

**`ENGINE!X6` verbatim:**

```
=IF(OR($V6="",$AI6="BLOCKED",$AI6="PENDING LINE",$AI6="STALE LINE"),"",
 IF(ABS($V6)<SETTINGS!$B$8,"",
  IF(ABS($V6)<SETTINGS!$B$9,"LEAN",
   IF(OR(ABS($V6)<SETTINGS!$B$10,SETTINGS!$B$11<>"Y",$AI6<>"READY",$AF6<>"",$AG6<>""),
      "INVESTIGATE","BET"))))
```

**Absolute edge is used correctly** — `ABS($V6)` in all three comparisons, sign-symmetric, with
direction preserved separately in `ENGINE!W`.

---

## 3. ⚠️ The threshold cells are SHARED with totals

**`ENGINE!AB6` (totals label) verbatim:**

```
=IF($AA6="","",
 IF(ABS($AA6)<SETTINGS!$B$8*2,"",
  IF(ABS($AA6)<SETTINGS!$B$9*2,"LEAN",
   IF(OR(SETTINGS!$B$11<>"Y",$AI6<>"READY",ABS($AA6)<SETTINGS!$B$10*2,$AF6<>"",$AG6<>""),
      "INVESTIGATE","BET"))))
```

| Threshold | Spread (`ENGINE!X`) | Totals (`ENGINE!AB`) |
|---|:--:|:--:|
| `B8` | 1.0 | **2.0** (`B8×2`) |
| `B9` | 1.5 | **3.0** (`B9×2`) |
| `B10` | 3.0 | **6.0** (`B10×2`) |

**Setting `B10 = 1.5` would silently redefine the totals BET threshold from 6.0 to 3.0.**

**Today that is latent, not visible:** `SETTINGS!B22` (league average total) and `B23` (total EPA
scale) are **blank**, so `ENGINE!Y` is blank for every game → `AA` blank → `AB` blank workbook-wide.
Totals are inert. But the redefinition would take effect the moment totals are enabled — an
unapproved totals change arriving with no further review. **That is why this needs decoupling, not a
one-cell edit.**

---

## 4. Test matrix — current behaviour

READY status, non-transitional, non-FCS:

| Edge | \|Edge\| | Current label | Intended | |
|---:|---:|---|---|:--:|
| +1.49 | 1.49 | LEAN | not BET | OK |
| **+1.50** | 1.50 | **INVESTIGATE** | **BET** | ❌ |
| **+1.51** | 1.51 | **INVESTIGATE** | **BET** | ❌ |
| −1.49 | 1.49 | LEAN | not BET | OK |
| **−1.50** | 1.50 | **INVESTIGATE** | **BET** | ❌ |
| **−1.51** | 1.51 | **INVESTIGATE** | **BET** | ❌ |
| 0.00 | 0.00 | *(blank)* | not BET | OK |
| blank line | — | *(blank)* | *(blank)* | OK |
| +0.99 | 0.99 | *(blank)* | not BET | OK |
| +1.00 | 1.00 | LEAN | not BET | OK |
| **+2.99** | 2.99 | **INVESTIGATE** | **BET** | ❌ |
| **+3.00** | 3.00 | **INVESTIGATE** | **BET** | ❌ |

**6 of 12 rows disagree with the intended rule.** Sign symmetry is correct throughout.

### Gated cases

| Case | Label | Why |
|---|---|---|
| Blank line, `PENDING LINE` | *(blank)* | outer `IF` short-circuits |
| Zero edge | *(blank)* | below the LEAN threshold |
| **QB-gated game, \|edge\| = 4.0** | **INVESTIGATE** | `AI <> "READY"` forces it |
| Transitional team, \|edge\| = 4.0 | INVESTIGATE | `AF <> ""` forces it |
| FCS opponent, \|edge\| = 4.0 | INVESTIGATE | `AG <> ""` and `FCS — NO PLAY` |

These gates are **correct and should be preserved** — a QB-gated game must never emit BET.

---

## 5. Cell-level proposal — NOT APPLIED

To implement the rule for spreads **while leaving totals numerically untouched**, three changes are
required. One cell alone is not sufficient and one cell alone is not safe.

### 5.1 Decouple totals first (prerequisite)

| Cell | Current | Proposed | Rationale |
|---|---|---|---|
| `SETTINGS!A26` | *(empty)* | `TOTALS thresholds (abs edge) — LEAN / INVESTIGATE / BET` | new label row |
| `SETTINGS!B33` | *(empty)* | `2` | totals LEAN — **equals today's `B8×2`** |
| `SETTINGS!B34` | *(empty)* | `3` | totals INVESTIGATE — **equals today's `B9×2`** |
| `SETTINGS!B26` | *(empty)* | `6` | totals BET — **equals today's `B10×2`** |

Rows 26, 33 and 34 are the only free `SETTINGS` rows; none is referenced by any formula today.

**Downstream formula affected — `ENGINE!AB6:AB1005` (1,000 cells):**

```
current:  ...ABS($AA6)<SETTINGS!$B$8*2 ... SETTINGS!$B$9*2 ... SETTINGS!$B$10*2 ...
proposed: ...ABS($AA6)<SETTINGS!$B$33  ... SETTINGS!$B$34  ... SETTINGS!$B$26   ...
```

**Totals behaviour is numerically identical** — 2.0 / 3.0 / 6.0 before and after — and totals remain
inert while `B22`/`B23` are blank. This change exists solely to stop the spread threshold from
dragging totals with it.

### 5.2 Then set the spread BET threshold

| Cell | Current | Proposed | Effect |
|---|:--:|:--:|---|
| `SETTINGS!B10` | **3.0** | **1.5** | `|edge| ≥ 1.5` → BET for spreads |

### 5.3 And enable BET labels

| Cell | Current | Proposed | Effect |
|---|:--:|:--:|---|
| `SETTINGS!B11` | **`N`** | **`Y`** | without this, BET stays unreachable at any edge |

> `SETTINGS!B11` also appears in `AUDIT!B12`, which reports
> `=IF(SETTINGS!$B$11="N","OK (OFF)","CHECK — toggle is "&SETTINGS!$B$11)`.
> Flipping to `Y` changes that audit line from `OK (OFF)` to `CHECK — toggle is Y` **by design** —
> it is an advisory, not a failure. Flagged so it is not mistaken for a regression.

### 5.4 What `B9` becomes

With `B10 = 1.5` and `B9 = 1.5`, the INVESTIGATE *band* `[B9, B10)` is empty. INVESTIGATE would then
appear only via the safety conditions — toggle off, status not READY, transitional, FCS — which is
the desired behaviour. **`B9` is proposed unchanged**; leaving it at 1.5 keeps the LEAN band at
`[1.0, 1.5)`, matching the rule exactly.

### 5.5 Expected classification changes on the 8 live-lined games

| Game | \|Edge\| | Now | After the proposal |
|---|:--:|---|---|
| SAC @ EMU | 4.67 | INVESTIGATE | **BET** |
| UNC @ TCU | 3.34 | INVESTIGATE | **BET** |
| SJSU @ USC | 3.31 | INVESTIGATE | **BET** |
| NMSU @ FSU | 2.76 | INVESTIGATE | **BET** |
| MEM @ UNLV | 1.14 | LEAN | LEAN *(and QB-gated regardless)* |
| JVST @ NDSU | 0.54 | *(blank)* | *(blank)* |
| HAW @ STAN | 0.24 | *(blank)* | *(blank)* |
| NCST @ UVA | 0.17 | *(blank)* | *(blank)* |

**Four games would move INVESTIGATE → BET.** Memphis @ UNLV stays LEAN and remains QB-gated, so it
could not emit BET even at a larger edge.

### 5.6 Totals — confirmation

| | Before | After |
|---|:--:|:--:|
| Totals LEAN | 2.0 | **2.0** |
| Totals INVESTIGATE | 3.0 | **3.0** |
| Totals BET | 6.0 | **6.0** |
| Totals labels produced today | none (`B22`/`B23` blank) | **none** |

**Totals remain untouched, numerically and operationally.** No totals threshold is being approved —
the proposal only pins the existing effective values in place so the spread change cannot move them.

---

## 6. Risk if only `SETTINGS!B10` is changed

Setting `B10 = 1.5` without §5.1 would:

- implement the spread rule correctly **today**, and
- silently halve every latent totals threshold — totals BET 6.0 → 3.0 — which would surface without
  review the first time `B22`/`B23` are populated.

**I recommend against the one-cell change** for that reason.

---

## 7. Nothing was altered

No formula, setting or threshold was modified. The 1.5 INVESTIGATE threshold, the BET toggle and all
weights are exactly as found. **Stopped for approval.**
