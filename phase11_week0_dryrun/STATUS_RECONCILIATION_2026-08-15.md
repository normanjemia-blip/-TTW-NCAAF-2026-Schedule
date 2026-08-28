# PROJECT STATUS RECONCILIATION — 2026-08-15

**Checkpoint date:** 2026-08-15 (America/New_York). The container clock is UTC;
the owner's timezone governs.
**Branch:** `claude/2026-ncaaf-schedule-build-by6j5n`
**Starting commit:** `c76131805ee95c60648700c36759062ab463c69c` — *TTW College Football Operations Manual v1.0*
**Working tree at start:** clean.

---

## 1. Repository documentation

**There is no `AGENTS.md` and no `CLAUDE.md`** anywhere in the repository. Project
convention lives in the phase reports, `operations/TTW_OPERATIONS_MANUAL_v1.0.md`
and the Phase 9A/9B policy documents instead.

---

## 2. Commit `fc0b247` — located and verified

`fc0b247d7d7d946d176eaf5a66ba6d5ebbc6ba56` · 2026-08-11 07:20:41 +0000 ·
*MAINTENANCE: repair the seven defects from Live Retrieval Test #1*

- **It is not an ancestor of HEAD.** It lives only on `remotes/origin/claude/ttw-football-intelligence-lib-7zt8m0` (the Football Intelligence Library branch), which is separate from the workbook branch.
- Library branch: 82 commits, HEAD `d7a9d45` *(MAINTENANCE: repair N-2 — cross-database conflict visibility in §27)*, preceded by `80bf37e` *FREEZE: TTW Football Intelligence Library declared COMPLETE*.
- fc0b247 repairs F-1 wrong-team best bet · F-2 bull/bear misclassification · F-3 raw page furniture · F-4 empty sections · F-5/F-6 unrecorded numeric conflicts · F-7 false no-conflict claim, and adds nine maintenance gates to `validate_teams.py`.

Its claim **"All 10 validation harnesses pass"** is **confirmed correct** — see §4.

---

## 3. Authoritative master — confirmed

| | |
|---|---|
| **File** | `promotion_v0.8.1/TTW_College_Football_Power_Ratings_v0.8.1_AUTHORITATIVE.xlsx` |
| **SHA-256** | `e2da9a4c28bd5c0f094ab06a2a85d3e31b37c2aba894f97f3415e15f799cdfd6` |
| **Verified by** | `promotion_v0.8.1/verify_v081.py` — **0 failures** |
| **Invariants** | 21 sheets · 123,011 formulas · 138 teams · 888 games (761 FBS-v-FBS, 127 FCS) · 65 H / 40 M / 33 L · 99 OK / 39 UNCERTAIN · 73 Tier-1 · 0 nonzero QB values · 0 market lines |

`v0.8.0` and the `v0.6.2` rollback target are both confirmed untouched. No older
workbook was treated as authoritative, and nothing was rebuilt.

---

## 4. Validator and test baseline

### 4.1 A correction to my own earlier result

An earlier run in this session reported **3 passed / 7 failed** on the library
harnesses and flagged it as contradicting fc0b247. **That result was my harness
error, not a library defect.** Two causes, both mine:

1. I had extracted the library with `git archive`, so `/tmp/lib` had **no `.git`** — every check that shells out to `git cat-file` failed, and five further checks failed only on the cascading meta-assertion *"prior phases still validate."*
2. **`pymupdf` was not installed**, so `extract_futures.py` and `extract_wintotals.py` exited non-zero. Those two checks print their sub-conditions but not the subprocess return code, which is why they read as `FAIL` while showing `reparse=True phase2=True columns_aligned=True`.

Re-run in a real git checkout with the dependency installed:

```
[PASS] validate_coaching.py    all 10 checks passed
[PASS] validate_concepts.py    all 12 checks passed
[PASS] validate_futures.py     all 12 checks passed
[PASS] validate_phase7.py      all 10 checks passed
[PASS] validate_power.py       all 10 checks passed
[PASS] validate_qb.py          all 12 checks passed
[PASS] validate_search.py      all 16 checks passed
[PASS] validate_teams.py       all 13 maintenance gates passed
[PASS] validate_trends.py      all 12 checks passed
[PASS] validate_wintotals.py   all 11 checks passed
----  10 passed, 0 failed  ----
```

**fc0b247's claim holds.** Link integrity: **10,012** relative links, **0 broken**.

### 4.2 Repository-side suites

| Suite | Result |
|---|---|
| `validate_schedule.py` | **ALL HARD-FAIL CHECKS PASSED** — 888 rows, 138 FBS programs, 8 Week 0 games on 2026-08-29/30 |
| `promotion_v0.8.1/verify_v081.py` | **0 failures** |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | **15/15** against v0.8.1 **and** against the archived v0.7.2 |
| `phase11_week0_dryrun/week0_dryrun.py` *(new)* | **29 passed, 0 failed** |

### 4.3 A real defect found and repaired: archive path drift

Archiving the v0.7.x candidates under `archive/candidates/` broke **18 scripts**
that hardcode pre-archive paths. Sixteen are frozen historical build/verify
scripts living inside the archived candidate directories — **left untouched**, as
superseded candidates must not be edited, and an archived build script should not
be re-runnable against an archived artifact.

**Two were live operational tooling and were repaired:**

| Script | Was | Now |
|---|---|---|
| `phase8_4_qb_monitoring/scripts/due_this_sweep.py` | crashed with `FileNotFoundError` — **the weekly QB sweep tool was unrunnable** | resolves the tracker at its archived location, with a fallback to the legacy path |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | default source path missing; only runnable with an explicit `--source` | defaults to the authoritative v0.8.1, falling back to the archived v0.7.2 |

Neither change touches pipeline logic, thresholds or validation rules. The
production `build_qb_candidate.py` path was never affected — it takes `--source`
explicitly.

---

## 5. Phase status

### Complete

| Phase | Evidence |
|---|---|
| 3 — Schedule acquisition | `validate_schedule.py` all checks pass |
| 4–6 — Source loading, FCS no-play, line-level testing | v0.6.2 deliverables |
| 7A–7D.5 — QB verification | backlog reached zero; 73 Tier-1 records |
| **7B Group 2** | **`phase7_preseason_calibration/phase7b_group2_validation.md`, dated 2026-08-03 — see §6** |
| 7E / 7E.1 — Promotion to v0.8.0 → v0.8.1 | `verify_v081.py` 0 failures |
| 8.4 — QB monitoring pipeline | 15/15 scenarios |
| 9 — QA | zero calculation defects |
| 9A / 9B — Production configuration | reports complete; **4 items blocked by connector** |
| 10 — Week 0 operational validation | zero discrepancies; **independently reproduced today** |
| Operations Manual v1.0 | Sections A–I |
| Football Intelligence Library | FROZEN at `80bf37e`, maintained through `d7a9d45`; 10/10 validators pass |

### Outstanding

| Item | Status |
|---|---|
| **Google Sheets configuration** — rename, timezone, protection, owner note | **Owner action.** Not possible through the available connector — no Sheets API. |
| **QB exception sweep** | **32 of 33 records overdue** as of 2026-08-15 (all stamped due 2026-08-03); all 33 due by 08-24 |
| **VSiN integration** | Deliberately not begun. VSiN remains a benchmark and peer-review reference; it is **not** blended into TTW ratings. |
| **Phase V1 — VSiN guide indexing** | Was blocked in-session by a 1-byte upload. Superseded: the Football Intelligence Library indexes the guide in full. |

---

## 6. Phase 7B Group 2 — reconciled as COMPLETE

`phase7_preseason_calibration/phase7b_group2_validation.md` (20,509 bytes, dated
2026-08-03) carries an Executive Decision Table covering all twelve named teams:

> **Result: 0 ACCEPTED · 0 MODIFIED · 8 HOLD · 4 DEFER.**

| Verdict | Teams |
|---|---|
| **HOLD** (8) | Michigan, Penn State, Clemson, Miami, Kentucky, Auburn, Missouri, Charlotte |
| **DEFER** (4) | Tulane, Memphis, South Florida, Southern Miss — all QB-unresolved |

Two details worth carrying forward:

- The **Penn State** claim carried in the Phase 7A notes is **wrong** — Campbell, Mouser and Lynn were confirmed, and Group 2 corrected it.
- The **Charlotte** disagreement resolved as a **scale artifact**, not a rating error: SP+ has SD 13.20 against FPI's 11.33, so points are not comparable across sources — ranks are. The rank gap was 12.

**No Group 2 validation work was required or performed.** Re-running it would
have re-litigated a closed decision.

---

## 7. Files changed in this session

| File | Change |
|---|---|
| `phase8_4_qb_monitoring/scripts/due_this_sweep.py` | repaired stale tracker path (live tool was unrunnable) |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | repaired stale default source path |
| `phase11_week0_dryrun/week0_dryrun.py` | **new** — Week 0 dry-run harness, 29 checks |
| `phase11_week0_dryrun/WEEK0_DRYRUN_REPORT.md` | **new** — dry-run results, blockers, Aug 22–24 tasks |
| `phase11_week0_dryrun/RETRIEVAL_TESTS_2_4.md` | **new** — retrieval tests #2–#4 |
| `phase11_week0_dryrun/STATUS_RECONCILIATION_2026-08-15.md` | **new** — this document |

**No workbook was modified.** The v0.8.1 SHA-256 is unchanged, verified before
and after every run. `phase10_operational_validation/week0_card.json` is
unchanged — the checkpoint was reconciled against, never rewritten. No formula,
tab, threshold, schedule, source weight or status rule was altered anywhere.
