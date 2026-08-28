# v0.8.9 — PROMOTION CERTIFICATE

> **PROMOTED. v0.8.9 is the current authoritative production workbook.**
> The live Google Sheet was **NOT** written and its Drive title was **NOT** renamed.
> The accepted live-sync candidate is **untouched** — its rebase is Phase 2, not yet begun.

| | |
|---|---|
| **Workbook** | `promotion_v0.8.9/TTW_College_Football_Power_Ratings_v0.8.9_AUTHORITATIVE.xlsx` |
| **SHA-256** | `334050660deb970f23cd9761490fb47e1f2b606b61d00a20c864cec529395cbb` |
| **Promoted from** | v0.8.9 **REV 2** candidate · `fcb4d6e63c7ab260b17ffbc47081a14def59bdbd81b4f9cff2194ea1fca18298` |
| **Supersedes** | v0.8.8 · `b2a920feddc0f49f0647957334db0ecd0e922fe6a3933fc6a11af31587b56450` — **frozen, immediate rollback** |
| **Promotion date** | **2026-08-27** (America/New_York) |
| **Certificate** | `verify_v089.py` — **60 passed, 0 failed** |
| **Cells changed** | **1,024** — computed independently |
| **Diff artifact** | `diff_v088_to_v089.csv` |
| **Regression log** | `regression_log_v089.txt` |

---

## 1. Scope — exactly 1,024 cells

The permitted difference from v0.8.8 was the certified 1,023 REV 2 cells plus the single
administrative promotion banner cell. The build recomputed the full workbook diff from scratch
rather than trusting the candidate's count:

```
independent diff v0.8.8 -> v0.8.9: 1024 cells
count reconciles: 1023 REV 2 cells + 1 banner = 1024
```

| Sheet | Cells |
|---|:--:|
| `ENGINE` (`AB6:AB1005`) | 1,000 |
| `SETTINGS` | 15 |
| `AUDIT` | 4 |
| `CHANGELOG` | 4 |
| `START HERE` (banner) | 1 |
| **Total** | **1,024** |

v0.8.9 differs from the certified REV 2 candidate by **exactly `START HERE!A1`** — asserted
cell-by-cell across all 21 sheets, not inferred.

## 2. Banner

Two substitutions and nothing else:

| | Before | After |
|---|---|---|
| Version | `v0.8.8 AUTHORITATIVE` | `v0.8.9 AUTHORITATIVE` |
| Promotion date | `promotion complete 2026-08-04` | `promotion complete 2026-08-27` |
| Market lines | `0 market lines loaded` | **retained verbatim** |

The stale `2026-08-04` clause is gone. `"0 market lines loaded"` is retained **and verified
truthful** — check 2.7 confirms `MARKET LINES` is in fact blank in the repository artifact.
Check 2.6 reverses both substitutions and reproduces the v0.8.8 banner string exactly, proving no
other character moved.

## 3. What v0.8.9 changes

**Spread BET rule.** `SETTINGS!B10` 3.0 → **1.5**; `SETTINGS!B11` `N` → **Y** (spreads only).
`|ATS edge| ≥ 1.50` now qualifies as **BET**; ±1.49 does not.

**Totals separated and preserved.** Totals thresholds moved onto dedicated `B49`/`B50`/`B51` and
**preserved at 2.0 / 3.0 / 6.0**; the totals BET toggle moved onto dedicated `B52` and **retained
at `N`**. `ENGINE!AB` no longer references `B10` or `B11`; `ENGINE!X` was never edited. Totals
remain disabled — `B22`/`B23` blank.

This closes the REV 1 regression, where `ENGINE!AB` read `B8*2`/`B9*2`/`B10*2` and the **same**
toggle `B11` as spreads, so enabling spread BET labels silently turned on totals BET labels.

### The only four label changes

| Game | Edge | v0.8.8 | **v0.8.9** | Gate |
|---|---:|---|---|---|
| SAC @ EMU | −4.67 | INVESTIGATE | **BET** | READY |
| UNC @ TCU | −3.34 | INVESTIGATE | **BET** | READY |
| SJSU @ USC | −3.31 | INVESTIGATE | **BET** | READY |
| NMSU @ FSU | −2.76 | INVESTIGATE | **BET** | READY |
| MEM @ UNLV | +1.14 | LEAN | **LEAN** | **QB UNCERTAIN** |
| JVST@NDSU · HAW@STAN · NCST@UVA | <1.0 | *(blank)* | *(blank)* | READY |

## 4. Certificate — 60 proofs, 0 failures

| § | Proves | Result |
|:--:|---|:--:|
| 0 | v0.8.8 frozen at its exact SHA; REV 2 unmodified; 21 sheets preserved | ✅ |
| 1 | Exactly 1,024 cells; per-sheet census; differs from REV 2 by only `A1` | ✅ |
| 2 | Banner correct, truthful, and minimally edited | ✅ |
| 3 | Spread BET threshold **exactly 1.5**; ±1.50 **is** BET; ±1.49 is not; QB gate still binds | ✅ |
| 4 | Totals remain **2.0 / 3.0 / 6.0**, toggle **N**, disabled, and classify identically to v0.8.8 **at each build's own production config** | ✅ |
| 5 | Spread and totals controls **fully independent** in both directions | ✅ |
| 6 | **Both** audit guards return **OK**; each still CHECKs on deliberate drift | ✅ |
| 7 | Model spread, edge, side and gate identical across all **761** FBS-v-FBS games; exactly **four** label changes | ✅ |
| 8 | 10 sheets byte-identical; QB census 117 OK / 21 UNCERTAIN; confidence 76 H / 43 M / 19 L; 234 QB zeros | ✅ |
| 9 | Production pointers repointed; v0.8.8 preserved as immediate rollback; v0.6.2 and v0.8.0 rollback hashes intact | ✅ |

No projection, rating, spread, total, edge, side, gate, QB value or schedule value changed.
No intentional non-OK audit result was left in production.

## 5. Validators — complete chain, all green

| Suite | Result |
|---|---|
| `promotion_v0.8.9/verify_v089.py` | **60 / 0** |
| `candidate_v0.8.9_rev2/verify_v089_rev2.py` | 58 / 0 |
| `verify_v088` · `v087` · `v086` | 72 / 89 / 56 — 0 failed |
| `verify_v085` · `v084` · `v083` · `v082` | 53 / 49 / 42 / 33 — 0 failed |
| `verify_v081.py` | 0 failures |
| `live_sync_v0.8.8/verify_live_sync_candidate.py` | 36 / 0 |
| `schedule_candidate_v1/verify_schedule_candidate.py` | 53 / 0 |
| `phase11_week0_dryrun/week0_dryrun.py` | 31 / 0 |
| `validate_schedule.py` | ALL HARD-FAIL CHECKS PASSED |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | 15 / 15 |
| `git diff --check` | clean |

### Validator changes this promotion required — disclosed in full

Three validator edits were necessary, none of which weakens a proof:

1. **`verify_v088.py` §18 is now supersession-aware.** Six of its checks asserted that the
   production pointers name v0.8.8 as *current* — assertions logically incompatible with any
   approved successor. While v0.8.8 is current the original assertions run **verbatim and
   unweakened**; once superseded the same section asserts the obligation that actually binds —
   v0.8.8 preserved as the immediate rollback at its exact SHA, its artifact still byte-exact,
   and the dry run advanced off it. Forward pointer assertions live in §9 here.

2. **`week0_dryrun.py` pinned `SETTINGS!B11 = N`.** That is a v0.8.8-era production constant that
   v0.8.9 changes to `Y` with approval. It now asserts the v0.8.9 configuration (`B10 = 1.5`,
   `B11 = Y`). This is config movement, not a regression: no game, spread, edge, side or label
   moved in the dry run.

3. **A mislabeled dry-run check was corrected.** Its text claimed "QB UNCERTAIN forces
   INVESTIGATE", but the gate actually firing on that fixture is `DATA INCOMPLETE`. The check now
   asserts `AI != "READY"` and says so. A first attempt to also restate the ±1.50 boundary here
   was **removed rather than tuned into a pass** — the Dublin fixture cannot reach `READY`, so the
   check could not have proven what its name claimed. The boundary is proven on real READY rows in
   §3 of this certificate.

**A defect this caught:** the first pass of the README pointer edit dropped v0.8.8's full SHA,
leaving only an abbreviated `b2a920fe…6450`. Check 18.6s failed, and the README now carries
v0.8.8's complete 64-character hash as the named immediate rollback.

## 6. REV 1 — superseded

`candidate_v0.8.9_spread_threshold/` (REV 1, `58c6f525…8989`) is **preserved unchanged as
superseded evidence**. Its **58 / 0 result must not be cited as current production evidence** —
its certificate pinned the BET toggle to `N` on both sides of its comparison, which masked the
totals regression at ±6.00 and never tested ±6.01. Production evidence for v0.8.9 is this
certificate and `candidate_v0.8.9_rev2/verify_v089_rev2.py`.

## 7. Rollback

| Tier | Version | SHA-256 |
|---|---|---|
| **Immediate** | **v0.8.8** | `b2a920feddc0f49f0647957334db0ecd0e922fe6a3933fc6a11af31587b56450` |
| Intermediate | v0.8.0 | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` |
| Base | v0.6.2 | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` |

All three verified present and byte-exact.

## 8. Scope confirmations

| | |
|---|:--:|
| Google Sheet written | **NO** |
| Live Drive title renamed | **NO** |
| Live-sync candidate modified | **No** — `474490c8…26de` |
| REV 1 modified | **No** — preserved as superseded evidence |
| Schedule candidate modified | **No** — `5416ffcb…2a84` |
| Totals enabled | **No** — `B22`/`B23` blank, totals toggle `N` |
| QB, schedule, ratings, adjustments, market lines altered | **No** |

**Phase 1 complete. Phase 2 — rebasing the accepted live-sync candidate onto v0.8.9 — follows.**
