# v0.8.9 REV 2 — CANDIDATE CERTIFICATE

> **CANDIDATE ONLY. NOT PROMOTED.** Production remains **v0.8.8**. No pointer repointed, no Google
> Sheet written. Authoritative v0.8.8 and the accepted live-sync candidate are untouched.
> **REV 1 (`2963afe`) is preserved unchanged as superseded evidence.**

| | |
|---|---|
| **Candidate** | `candidate_v0.8.9_rev2/TTW_College_Football_Power_Ratings_v0.8.9_REV2_CANDIDATE.xlsx` |
| **SHA-256** | `fcb4d6e63c7ab260b17ffbc47081a14def59bdbd81b4f9cff2194ea1fca18298` |
| **Built from** | authoritative v0.8.8 · `b2a920fe…6450` — **not from REV 1** |
| **Certificate** | `verify_v089_rev2.py` — **58 passed, 0 failed** |
| **Cells changed** | **1,023** |

---

## 1. The REV 1 conflict — reproduced and confirmed

Fixture: real Week 0 game `401864577` Jacksonville State @ North Dakota State — both teams resolve,
`AI = READY`, `AF` and `AG` empty, market total 46.5 populated, model total populated, so
`ENGINE!AA = Y − Z` is a real number.

| \|Total edge\| | v0.8.8 (`B11=N`) | REV 1 (`B11=Y`, shared) | |
|---:|---|---|:--:|
| ±5.99 | INVESTIGATE | INVESTIGATE | — |
| **±6.00** | **INVESTIGATE** | **BET** | ⚠️ |
| **±6.01** | **INVESTIGATE** | **BET** | ⚠️ |

**CONFIRMED — 4 of 6 fixtures change.** REV 1 preserved the totals thresholds at exactly 2.0/3.0/6.0;
the regression came **entirely from the shared toggle**.

### Why REV 1's "byte-for-byte equivalent" check failed to expose it

`verify_v089.py` check 9.1 built its "after" settings as:

```python
S_old_hold = dict(S9); S_old_hold['B11'] = S8['B11']   # toggle pinned to the v0.8.8 value
```

It **deliberately held the toggle at `N` on both sides** to isolate the threshold repointing. Three
consequences:

1. It compared **"decoupling alone"**, not **"v0.8.8 shipped config vs REV 1 shipped config"**. The
   claim it proved was *true but narrower than its wording implied* — the thresholds were equivalent;
   the shipped configurations were not.
2. At exactly ±6.00 the difference was **masked**: the pinned `N` forced INVESTIGATE on both sides.
3. It never tested **±6.01**, just past the BET boundary.

**Fix in REV 2:** every fixture is evaluated **at each build's own production settings**, ±6.01 is in
the matrix, and totals get a dedicated toggle so the spread toggle cannot reach them at all.

---

## 2. Exact diff — 1,023 cells

| Sheet | Cells |
|---|:--:|
| `SETTINGS` | 15 |
| `ENGINE` | 1,000 (`AB6:AB1005`) |
| `AUDIT` | 4 |
| `CHANGELOG` | 4 |

Per-cell listing: `diff_v088_to_v089rev2.csv`.

### SETTINGS — 15 cells

| Cell | Before | After |
|---|---|---|
| `A8` | `LEAN threshold (abs edge)` | `SPREAD LEAN threshold (abs edge)` |
| `A9` | `INVESTIGATE threshold (abs edge)` | `SPREAD INVESTIGATE threshold (abs edge)` |
| `A10` | `BET threshold (abs edge)` | `SPREAD BET threshold (abs edge)` |
| **`B10`** | **`3`** | **`1.5`** |
| `A11` | `BET labels toggle (Y/N)` | `Enable SPREAD BET labels? (Y/N) — spreads only` |
| **`B11`** | **`N`** | **`Y`** |
| `A48` | *(empty)* | `TOTALS MARKET CONTROLS — independent of the spread controls above` |
| `A49` / **`B49`** | *(empty)* | `TOTALS LEAN threshold (abs edge)` / **`2`** |
| `A50` / **`B50`** | *(empty)* | `TOTALS INVESTIGATE threshold (abs edge)` / **`3`** |
| `A51` / **`B51`** | *(empty)* | `TOTALS BET threshold (abs edge)` / **`6`** |
| `A52` / **`B52`** | *(empty)* | **`Enable totals BET labels? (Y/N)`** / **`N`** |

Rows 48–52 were fully empty and referenced by no formula. REV 1's split layout (26/33/34) was
abandoned — REV 2 is built fresh, so the totals block is contiguous and self-documenting.

### ENGINE!AB6:AB1005 — 1,000 cells

```
before: IF(ABS($AA6)<SETTINGS!$B$8*2 … SETTINGS!$B$9*2 … SETTINGS!$B$11<>"Y" … SETTINGS!$B$10*2 …
after:  IF(ABS($AA6)<SETTINGS!$B$49  … SETTINGS!$B$50  … SETTINGS!$B$52<>"Y" … SETTINGS!$B$51  …
```

**No reference to `B10` or `B11` survives.** The build asserts this per cell and verifies that
substituting the four control tokens back reproduces the original string exactly — so nothing else in
any of the 1,000 formulas moved. **`ENGINE!X` was never edited** and still reads `B10`/`B11`.

### AUDIT — 4 cells

| Cell | After |
|---|---|
| `A12` | `SPREAD config: BET threshold 1.5, spread toggle Y, formula independent of totals` |
| `B12` | OK only when `B10=1.5`, `B11="Y"`, `ENGINE!X` uses `B10`/`B11` and **not** `B51`/`B52` |
| `A13` | `TOTALS config: thresholds 2.0/3.0/6.0, totals toggle N, formula independent of spreads` |
| `B13` | OK only when `B49=2`, `B50=3`, `B51=6`, `B52="N"`, `ENGINE!AB` uses `B49–B52` and **not** `B10`/`B11` |

Both wrap every `FORMULATEXT` clause in `IFERROR(…,FALSE)` so an unsupported function fails to
**CHECK**, never to a false OK.

### CHANGELOG — row 87

`v0.8.9 · 2026-08-26` recording: spread BET threshold 3.0 → 1.5 · spread BET labels enabled · totals
thresholds separated and preserved at 2.0/3.0/6.0 · totals BET toggle separated and retained at `N` ·
no projection, rating, edge, side or totals output changed · REV 1 superseded.

---

## 3. Certificate — all 17 proofs

| # | Proof | Result |
|:--:|---|:--:|
| 1 | v0.8.8 remains byte-exact source | ✅ |
| 2 | Every changed cell enumerated | 1,023; SETTINGS 15 / ENGINE 1000 / AUDIT 4 / CHANGELOG 4 |
| 3 | ±1.49 not BET | LEAN ✅ |
| 4 | ±1.50 and ±1.51 BET | ✅ |
| 5 | `B11` affects spreads only | `X` uses it; `AB` does not ✅ |
| 6 | Flipping `B11` → **zero** totals-label changes (15 fixtures) | ✅ |
| 7 | Dedicated totals toggle affects totals only | ✅ |
| 8 | Flipping the totals toggle → **zero** spread-label changes | ✅ |
| 9 | Totals match v0.8.8 at ±1.99/±2.00/±2.99/±3.00/±5.99/±6.00/**±6.01** | ✅ each at its own config |
| 10 | Harness-only `B52="Y"` makes BET reachable at ±6 without touching spreads | ✅ |
| 11 | Totals remain inert in the workbook | `B22`/`B23` blank ✅ |
| 12 | **Both** AUDIT rows OK in approved production | ✅ |
| 13 | Both guards catch deliberate drift | 8 drift cases + 2 fail-safe ✅ |
| 14 | Only the four expected lined games change | ✅ |
| 15 | Memphis at UNLV remains LEAN and QB UNCERTAIN | ✅ |
| 16 | No projection, rating, spread, total, edge, side, QB or schedule change | 11 sheets byte-identical ✅ |
| 17 | Complete historical validator chain green | ✅ §5 |

### Proof 9 — the regression is closed

| \|AA\| | v0.8.8 | **REV 2** |
|---:|---|---|
| ±1.99 | *(blank)* | *(blank)* |
| ±2.00 / ±2.99 | LEAN | LEAN |
| ±3.00 / ±5.99 | INVESTIGATE | INVESTIGATE |
| **±6.00** | INVESTIGATE | **INVESTIGATE** |
| **±6.01** | INVESTIGATE | **INVESTIGATE** |
| blank | *(blank)* | *(blank)* |

**Identical at every fixture, each build evaluated at its own production configuration** — the exact
comparison REV 1's certificate did not make.

---

## 4. Before / after — the eight lined games

| Game | Edge | v0.8.8 | **REV 2** | Gate |
|---|---:|---|---|---|
| SAC @ EMU | −4.67 | INVESTIGATE | **BET** | READY |
| UNC @ TCU | −3.34 | INVESTIGATE | **BET** | READY |
| SJSU @ USC | −3.31 | INVESTIGATE | **BET** | READY |
| NMSU @ FSU | −2.76 | INVESTIGATE | **BET** | READY |
| **MEM @ UNLV** | +1.14 | LEAN | **LEAN** | **QB UNCERTAIN** |
| JVST @ NDSU · HAW @ STAN · NCST @ UVA | <1.0 | *(blank)* | *(blank)* | READY |

Exactly four changes. Every model spread, edge, side and gate identical across all 761 FBS-v-FBS games.

---

## 5. Validators — all green

| Suite | Result |
|---|---|
| `verify_v089_rev2.py` | **58 / 0** |
| `verify_v089.py` *(REV 1, preserved)* | 58 / 0 |
| `verify_v088` · `v087` · `v086` | 72 / 89 / 56, all 0 failed |
| `verify_v085` · `v084` · `v083` · `v082` | 53 / 49 / 42 / 33, all 0 failed |
| `verify_v081.py` | 0 failures |
| `live_sync_v0.8.8/verify_live_sync_candidate.py` | 36 / 0 |
| `schedule_candidate_v1/verify_schedule_candidate.py` | 53 / 0 |
| `phase11_week0_dryrun/week0_dryrun.py` | 30 / 0 |
| `validate_schedule.py` | ALL HARD-FAIL CHECKS PASSED |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | 15 / 15 |
| `git diff --check` | clean |

---

## 6. Scope confirmations

| | |
|---|:--:|
| Authoritative v0.8.8 modified | **No** — `b2a920fe…6450` |
| Accepted live-sync candidate modified | **No** — `474490c8…26de` |
| REV 1 modified | **No** — `58c6f525…8989`, preserved as superseded evidence |
| Production pointers repointed | **No** |
| Totals enabled | **No** — `B22`/`B23` blank, totals toggle `N` |
| QB, schedule, ratings, adjustments, market lines altered | **No** |
| Intentional non-OK audit result left in production | **No** — both rows OK |
| Google Sheets written | **NO** |

**Stopped for approval. v0.8.9 REV 2 is not promoted.**
