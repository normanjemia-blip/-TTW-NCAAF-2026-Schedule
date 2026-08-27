# v0.8.9 SPREAD-THRESHOLD CANDIDATE — CERTIFICATE

> **CANDIDATE ONLY. NOT PROMOTED.** Production remains **v0.8.8**. No pointer repointed, no Google
> Sheet written, and the accepted live-sync candidate is untouched.

**Built:** 2026-08-26 · from authoritative v0.8.8 at commit `936fef1`

| | |
|---|---|
| **Candidate** | `candidate_v0.8.9_spread_threshold/TTW_College_Football_Power_Ratings_v0.8.9_THRESHOLD_CANDIDATE.xlsx` |
| **Candidate SHA-256** | `58c6f525d07f3d3ee08eed5028b9235e8db52cd5a139e57e98d2d260bfc88989` |
| **Source** | v0.8.8 · `b2a920fe…6450` — verified unmodified |
| **Certificate** | `verify_v089.py` — **58 passed, 0 failed** |
| **Cells changed** | **1,008** |

---

## 1. Exact diff — 1,008 cells

| Sheet | Cells | What |
|---|:--:|---|
| `SETTINGS` | 6 | thresholds, toggle, dedicated totals settings |
| `ENGINE` | 1,000 | `AB6:AB1005` — totals classification repointed |
| `AUDIT` | 2 | `A12` / `B12` config guard |

Full per-cell listing: `diff_v088_to_v089.csv`.

### The 8 discrete cells

| Cell | Before | After |
|---|---|---|
| `SETTINGS!B10` | `3` | **`1.5`** — spread BET threshold |
| `SETTINGS!B11` | `N` | **`Y`** — spread BET toggle |
| `SETTINGS!A26` | *(empty)* | `TOTALS thresholds (abs edge) — BET here; LEAN B33 / INVESTIGATE B34` |
| `SETTINGS!B26` | *(empty)* | **`6`** — totals BET (pins today's `B10×2`) |
| `SETTINGS!B33` | *(empty)* | **`2`** — totals LEAN (pins today's `B8×2`) |
| `SETTINGS!B34` | *(empty)* | **`3`** — totals INVESTIGATE (pins today's `B9×2`) |
| `AUDIT!A12` | `BET toggle default OFF` | `Approved spread config: BET 1.5 / toggle Y / totals pinned 2-3-6 and decoupled` |
| `AUDIT!B12` | `=IF(SETTINGS!$B$11="N","OK (OFF)","CHECK — toggle is "&SETTINGS!$B$11)` | full approved-configuration guard (below) |

### `ENGINE!AB6:AB1005` — totals decoupling, 1,000 cells

```
before: =IF($AA6="","",IF(ABS($AA6)<SETTINGS!$B$8*2,"",IF(ABS($AA6)<SETTINGS!$B$9*2,"LEAN",
         IF(OR(SETTINGS!$B$11<>"Y",$AI6<>"READY",ABS($AA6)<SETTINGS!$B$10*2,$AF6<>"",$AG6<>""),
            "INVESTIGATE","BET"))))

after:  =IF($AA6="","",IF(ABS($AA6)<SETTINGS!$B$33,"",IF(ABS($AA6)<SETTINGS!$B$34,"LEAN",
         IF(OR(SETTINGS!$B$11<>"Y",$AI6<>"READY",ABS($AA6)<SETTINGS!$B$26,$AF6<>"",$AG6<>""),
            "INVESTIGATE","BET"))))
```

**Only the three threshold tokens changed.** The build asserts this per cell by substituting the new
references back and requiring the original string — so no other part of any of the 1,000 formulas
moved. `ENGINE!X` (the spread classifier) is **not** edited at all; the rule change comes entirely
from `SETTINGS!B10`/`B11`.

---

## 2. Certificate — all 15 required proofs

| # | Proof | Check | Result |
|:--:|---|---|:--:|
| 1 | Source v0.8.8 hash matches | 1.1 | ✅ |
| 2 | Every changed cell listed | 2.1–2.5 | 1,008; SETTINGS 6, ENGINE 1000, AUDIT 2 |
| 3 | No QB or schedule cell changed | 3.x | QB VALUES, IMPORT SCHEDULE, TEAM MAP, PRESEASON, TEAM RATINGS, MARKET LINES, ADJUSTMENTS, CLEAN, CALC, DASHBOARD all byte-identical |
| 4 | No rating, projection, edge, direction or spread changed | 4.1–4.3 | identical across all 761 FBS-v-FBS games |
| 5 | ±1.49 not BET · ±1.50 BET · ±1.51 BET | 5.x | ✅ all six |
| 6 | Absolute-edge direction correct | 6.1, 6.2 | sign-symmetric; side still follows sign |
| 7 | QB-gated games remain gated | 7.1 | `|edge|=4.0` + QB UNCERTAIN → INVESTIGATE |
| 8 | Blank-line, FCS, transitional retain treatment | 8.1–8.6 | ✅ six cases |
| 9 | Totals equivalent before/after decoupling | 9.1–9.4 | ✅ all 13 fixtures |
| 10 | Totals remain disabled/inert | 10.1–10.3 | `B22`/`B23` still blank |
| 11 | `AUDIT!B12` OK for approved config, CHECK on drift | 11.1–11.8 | ✅ incl. fail-safe |
| 12 | Eight live fixtures retain projections and sides | 12.1 | ✅ |
| 13 | Exactly the four identified label changes | 13.1, 13.2, 13.x | ✅ |
| 14 | Memphis at UNLV stays gated, not a BET | 14.1, 14.2 | QB UNCERTAIN, LEAN |
| 15 | All established validators green | §5 | ✅ |

### Requirement 5 — the boundary

| Edge | Label | Required |
|---:|---|---|
| +1.49 / −1.49 | LEAN | not BET ✅ |
| **+1.50 / −1.50** | **BET** | **BET ✅** |
| **+1.51 / −1.51** | **BET** | **BET ✅** |

### Requirement 9 — totals equivalence across the decoupling

Toggle held at its v0.8.8 value so the decoupling is isolated:

| \|Total edge\| | Before | After | |
|---:|---|---|:--:|
| ±1.99 | *(blank)* | *(blank)* | ✅ |
| ±2.00 | LEAN | LEAN | ✅ |
| ±2.99 | LEAN | LEAN | ✅ |
| ±3.00 | INVESTIGATE | INVESTIGATE | ✅ |
| ±5.99 | INVESTIGATE | INVESTIGATE | ✅ |
| ±6.00 | INVESTIGATE | INVESTIGATE | ✅ |
| blank | *(blank)* | *(blank)* | ✅ |

**Byte-for-byte equivalent. Effective totals thresholds remain exactly 2.0 / 3.0 / 6.0.**

---

## 3. Before / after on the eight live market-line fixtures

| Game | Edge | v0.8.8 | **v0.8.9** | Gate |
|---|---:|---|---|---|
| SAC @ EMU | −4.67 | INVESTIGATE | **BET** | READY |
| UNC @ TCU | −3.34 | INVESTIGATE | **BET** | READY |
| SJSU @ USC | −3.31 | INVESTIGATE | **BET** | READY |
| NMSU @ FSU | −2.76 | INVESTIGATE | **BET** | READY |
| **MEM @ UNLV** | +1.14 | LEAN | **LEAN** | **QB UNCERTAIN** |
| JVST @ NDSU | −0.54 | *(blank)* | *(blank)* | READY |
| HAW @ STAN | +0.24 | *(blank)* | *(blank)* | READY |
| NCST @ UVA | −0.17 | *(blank)* | *(blank)* | READY |

**Exactly four labels change — the four identified in the approved audit.** Every model spread, edge
and side is identical. **Memphis at UNLV remains QB-gated and is not a certified BET.**

---

## 4. `AUDIT!B12` — the new guard

Returns **OK** only when every approved condition holds: `B10=1.5` · `B11="Y"` · `B26=6` · `B33=2` ·
`B34=3` · and `ENGINE!AB6` references `B33`/`B34`/`B26` while containing none of `$B$8*2`,
`$B$9*2`, `$B$10*2` (read via `FORMULATEXT`).

Otherwise it returns **CHECK** with a diagnostic naming what drifted. Verified CHECK on: BET
threshold back to 3 · toggle back to N · each totals threshold drifting · totals re-coupled · and —
**fail-safe** — if `FORMULATEXT` is unavailable, every clause is wrapped in `IFERROR(…,FALSE)` so the
guard fails to CHECK rather than falsely reporting OK.

---

## 5. Validators — all green

| Suite | Result |
|---|---|
| `verify_v089.py` *(this candidate)* | **58 / 0** |
| `verify_v088.py` | 72 / 0 |
| `verify_v087.py` | 89 / 0 |
| `verify_v086` · `v085` · `v084` · `v083` · `v082` | 56 / 53 / 49 / 42 / 33, all 0 failed |
| `verify_v081.py` | 0 failures |
| `live_sync_v0.8.8/verify_live_sync_candidate.py` | 36 / 0 *(accepted candidate, untouched)* |
| `schedule_candidate_v1/verify_schedule_candidate.py` | 53 / 0 |
| `phase11_week0_dryrun/week0_dryrun.py` | 30 / 0 |
| `validate_schedule.py` | ALL HARD-FAIL CHECKS PASSED |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | 15 / 15 |
| `git diff --check` | clean |

---

## 6. ⚠️ Two findings requiring a ruling — NOT applied

### 6.1 `AUDIT!B13` will display "CHANGED" under the approved configuration

`AUDIT!B13` hard-codes the old thresholds:

```
A13: "Thresholds 1.0 / 1.5 / 3.0"
B13: =IF(AND(SETTINGS!$B$8=1,SETTINGS!$B$9=1.5,SETTINGS!$B$10=3),"OK","CHANGED — log in CHANGELOG")
```

With `B10 = 1.5` it evaluates to **`CHANGED — log in CHANGELOG`**, and the `A13` label becomes stale.

Your instruction named only `B12`, so **I did not touch `B13`.** Two readings are defensible: it is
arguably *working correctly* — the thresholds did change and it is asking for a changelog entry — but
it leaves a second non-OK line on the AUDIT tab in approved production, which is the very thing the
`B12` requirement was meant to prevent.

**Proposed fix, for your approval only:**

| Cell | Current | Proposed |
|---|---|---|
| `AUDIT!A13` | `Thresholds 1.0 / 1.5 / 3.0` | `Thresholds 1.0 / 1.5 / 1.5 (LEAN / INVESTIGATE / BET)` |
| `AUDIT!B13` | `…SETTINGS!$B$10=3…` | `=IF(AND(SETTINGS!$B$8=1,SETTINGS!$B$9=1.5,SETTINGS!$B$10=1.5),"OK","CHANGED — log in CHANGELOG")` |

### 6.2 `SETTINGS!B11` remains shared with totals

The approved proposal decoupled the **thresholds**, not the **toggle**. `ENGINE!AB` still reads
`SETTINGS!$B$11<>"Y"`, so setting `B11 = "Y"` also latently enables totals BET at `|total edge| ≥ 6`.

**No live effect today:** `B22`/`B23` are blank, `ENGINE!Y` is blank workbook-wide, so every totals
label is blank and no totals BET can appear (certificate 10.1–10.3). The approved totals thresholds
stay exactly 2.0 / 3.0 / 6.0.

But this is the same class of latent coupling as the `B10` hazard that blocked the one-cell shortcut:
it would surface unreviewed the day totals are enabled. **Recommended follow-up** — a dedicated
totals toggle (e.g. `SETTINGS!B35`) with `ENGINE!AB` repointed at it, defaulted to `N`.
**Not applied; flagged for your decision.**

### 6.3 Banner

`START HERE!A1` still reads **v0.8.8** — this is a candidate, not a promotion, matching the pattern
used for the v0.8.8 schedule candidate where the banner was applied at promotion time. **Not changed.**

---

## 7. Scope confirmations

| | |
|---|:--:|
| Authoritative v0.8.8 modified | **No** — SHA re-verified |
| Accepted live-sync candidate modified | **No** — `474490c8…26de` re-verified |
| Production pointers repointed | **No** |
| MARKET LINES / QB VALUES / schedule dates / ratings / adjustments altered | **No** |
| Totals enabled or totals inputs populated | **No** |
| One-cell `B10` shortcut used | **No** — decoupled first |
| Google Sheets written | **NO** |

**Stopped for approval. v0.8.9 is not promoted.**
