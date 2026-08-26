# v0.8.8 AUTHORITATIVE — SCHEDULE-DATE CORRECTION

**Promotion date:** 2026-08-25 (America/New_York)
**Predecessor:** v0.8.7 AUTHORITATIVE — **frozen and unmodified**
**Authorising documents:** `schedule_candidate_v1/V088_SCHEDULE_CANDIDATE_APPROVAL.md` (candidate
certified 53/0 at commit `6f3f646`), plus the owner's conditional banner instruction

| | |
|---|---|
| **Workbook** | `promotion_v0.8.8/TTW_College_Football_Power_Ratings_v0.8.8_AUTHORITATIVE.xlsx` |
| **SHA-256** | `b2a920feddc0f49f0647957334db0ecd0e922fe6a3933fc6a11af31587b56450` |
| **Predecessor SHA-256** | `46671deeaaa94d98c63cb32d0e94af9907e76e7e2638de431b918987df2e15cd` (frozen) |
| **Certificate** | `verify_v088.py` — **72 passed, 0 failed** |
| **Change** | **134 cells** = 133 schedule dates + 1 banner · **zero formula changes** · **zero model-output changes** · **zero QB changes** |

---

## 1. The banner required changing — stated plainly

The certified candidate (`5416ffcb…2a84`) was verified 53/0 **while still carrying the v0.8.7
banner.** Under the conditional banner rule, `START HERE!A1` was therefore updated in the promotion
copy.

> **The authoritative v0.8.8 workbook is NOT byte-identical to the certified candidate.**
> It differs by exactly one cell — `START HERE!A1` — and its SHA-256 is a new value,
> `b2a920fe…6450`, computed from the final file.

**The promotion diff against v0.8.7 is therefore 134 cells, not 133:**

| | Cells |
|---|:--:|
| Certified schedule dates — `IMPORT SCHEDULE!D` | **133** |
| Administrative banner — `START HERE!A1` | **1** |
| **Total** | **134** |

### The banner edit is the version token and nothing else

| | |
|---|---|
| Before | `…TTW COLLEGE FOOTBALL POWER RATINGS (**v0.8.7 AUTHORITATIVE** — promotion complete 2026-08-04. … 76 H / 43 M / 19 L; 0 nonzero QB values. …)` |
| After | `…TTW COLLEGE FOOTBALL POWER RATINGS (**v0.8.8 AUTHORITATIVE** — promotion complete 2026-08-04. … 76 H / 43 M / 19 L; 0 nonzero QB values. …)` |

The confidence census in the banner was **already correct** at `76 H / 43 M / 19 L` — this promotion
makes no QB change — so it was not touched. Certificate check **1.6** proves the edit is reversible
to the exact v0.8.7 string, i.e. nothing else in the banner moved.

> **Carried-forward artifact, deliberately left alone:** the banner's `promotion complete 2026-08-04`
> clause has been inherited unchanged since v0.8.0 and is stale. Correcting it was **not** in scope
> here and would have exceeded the authorised single-token edit. Flagged, not fixed.

---

## 2. Preflight — all six checks cleared before promotion

| Check | Result |
|---|:--:|
| HEAD is `6f3f646` | ✅ |
| Branch synchronised (0 ahead / 0 behind), worktree clean | ✅ |
| Candidate SHA `5416ffcb…2a84` · predecessor SHA `46671dee…15cd` | ✅ both matched |
| Schedule certificate | ✅ **53 / 0** |
| `verify_v087` | ✅ **89 / 0** |
| Candidate differs from v0.8.7 by exactly 133 cells, all `IMPORT SCHEDULE!D` | ✅ verified **before** the banner edit |

---

## 3. What changed — and what did not

### Changed

**133 venue-local date corrections**, every one exactly **−1 calendar day**, confined to
`IMPORT SCHEDULE` column **D**. Plus the one banner cell.

### Explicitly unchanged

| | Evidence |
|---|---|
| **The entire `QB VALUES` sheet** — byte-identical to v0.8.7 | check 13.1 |
| Formulas — anywhere in the workbook | check 6.1 |
| Event IDs, season, week, neutral_site, teams, venue, notes | checks 5.1, 5.2, 5.x |
| **The 403 placeholder-time rows** | checks 4.1, 4.2 |
| No newly announced kickoff time incorporated | check 4.3 |
| Ratings, spreads, edges, sides, labels, market lines, gates | checks 14.x, 15.1–15.8 |
| Historical reports and rollback artifacts | untouched; hashes preserved, check 18.5 |

---

## 4. Certificate — all 19 required proofs

**Result: 72 passed, 0 failed.**

| # | Required proof | Check | Result |
|:--:|---|---|---|
| 1 | 133 schedule cells + at most one banner cell | 1.1, 1.2, 1.3 | 134 total |
| 2 | Schedule changes confined to `IMPORT SCHEDULE!D` | 2.1 | column D only |
| 3 | Every schedule delta exactly −1 day | 3.1, 3.2 | `{-1: 133}` |
| 4 | 403 placeholder-time rows unchanged | 4.1, 4.2, 4.3 | `[]` |
| 5 | 888 event IDs present and unique | 5.1, 5.2 | `n=888 unique=888` |
| 6 | No formula changed | 6.1 | `[]` |
| 7 | No game changes week or crosses Week 0 | 7.1, 7.2, 7.3, 7.4 | 0 crossed |
| 8 | Memphis at UNLV is Saturday 2026-08-29 | 8.1 | `2026-08-30 → 2026-08-29` |
| 9 | Sunday games remain 3 | 9.1, 9.2 | `70 → 3` |
| 10 | QB census remains 117 / 21 | 10.1 | ✅ |
| 11 | Confidence census remains 76 / 43 / 19 | 11.1 | ✅ |
| 12 | QB zero count remains 234 | 12.1, 12.2 | `234` |
| 13 | No QB value or status changed | **13.1** | whole sheet byte-identical |
| 14 | Five reference spreads unchanged | 14.x | all five |
| 15 | Every model output, edge, side, label and gate unchanged | 15.1–15.8 | ✅ |
| 16 | Date rule remains idempotent | 16.1, 16.2 | `[]` |
| 17 | Guard detects all 133 predecessor UTC defects | 17.1 | flagged **133** |
| 18 | All production pointers identify only v0.8.8 | 18.1–18.9 | ✅ |
| 19 | Superseded candidate not referenced as current | 19.x, 19.5, 19.6 | ✅ |

---

## 5. Censuses — unchanged, as required

| | v0.8.7 | **v0.8.8** |
|---|:--:|:--:|
| QB status | 117 OK / 21 UNCERTAIN | **117 OK / 21 UNCERTAIN** |
| Confidence | 76 H / 43 M / 19 L | **76 H / 43 M / 19 L** |
| QB zeros | 234 | **234** |
| Nonzero QB values | 0 | **0** |
| Teams / games | 138 / 888 / 761 / 127 / 0 BLOCK | **identical** |

### Weekday distribution — the visible improvement

| Weekday | v0.8.7 | **v0.8.8** | Δ |
|---|:--:|:--:|:--:|
| Saturday | 720 | **751** | +31 |
| Friday | 45 | **66** | +21 |
| Thursday | 22 | **34** | +12 |
| Wednesday | 24 | **15** | −9 |
| Tuesday | 6 | **18** | +12 |
| **Sunday** | **70** | **3** | **−67** |
| Monday | 1 | 1 | 0 |

The three surviving Sunday games are genuine Labor Day weekend fixtures (Labor Day 2026 is Monday
Sept 7): Louisville @ Ole Miss, Washington State @ Washington, Wisconsin @ Notre Dame. **Week 0 is now
a single Saturday, 2026-08-29** — including the QB-gated Memphis @ UNLV.

---

## 6. Validation — complete chain

| Suite | Result |
|---|---|
| `promotion_v0.8.8/verify_v088.py` | **72 passed, 0 failed** |
| `schedule_candidate_v1/verify_schedule_candidate.py` | 53 passed, 0 failed |
| `promotion_v0.8.7/verify_v087.py` | 89 passed, 0 failed |
| `promotion_v0.8.6/verify_v086.py` | 56 passed, 0 failed |
| `promotion_v0.8.5/verify_v085.py` | 53 passed, 0 failed |
| `promotion_v0.8.4/verify_v084.py` | 49 passed, 0 failed |
| `promotion_v0.8.3/verify_v083.py` | 42 passed, 0 failed |
| `promotion_v0.8.2/verify_v082.py` | 33 passed, 0 failed |
| `promotion_v0.8.1/verify_v081.py` | 0 failures |
| `phase11_week0_dryrun/week0_dryrun.py` | 30 passed, 0 failed |
| `validate_schedule.py` | ALL HARD-FAIL CHECKS PASSED |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | 15/15 |
| `git diff --check` | clean |

**No assertion was weakened, removed or bypassed.**

---

## 7. Pointers updated — targeted edits, hashes recomputed from files

`README.md` · `PROJECT_MANIFEST.json` · `phase9a_production_config/MASTER_AND_WORKING_COPY_POLICY.md`
· `phase11_week0_dryrun/week0_dryrun.py` (`EXPECTED_SHA`).

Every hash was **recomputed directly from its own file** — no value was copied through a global
replacement. v0.8.7 is preserved as the immediate frozen predecessor and rollback target with its
exact SHA; all older rollback filenames and hashes are unchanged (check 18.5 re-asserts the v0.6.2
and v0.8.0 hashes). No historical promotion report was modified.

---

## 8. The superseded candidate

`schedule_candidate_v1/TTW_College_Football_Power_Ratings_SCHED1_CANDIDATE.xlsx` — the original
**v0.8.6-based** build — **remains on disk, untouched and tracked**, as instructed. It is documented
as superseded and is **referenced by no production pointer** (checks 19.x). **Do not promote it.**
Its cleanup is a separate matter.

The certified `…v0.8.8_SCHEDULE_CANDIDATE.xlsx` also remains, unmodified (check 19.6), as the
provenance record for this promotion.

---

## 9. Files

| File | Role |
|---|---|
| `TTW_College_Football_Power_Ratings_v0.8.8_AUTHORITATIVE.xlsx` | the workbook |
| `build_v088.py` | deterministic build from the certified candidate; asserts the banner edit is the version token alone |
| `verify_v088.py` | promotion certificate — **read-only**, 72 checks |
| `diff_v087_to_v088.csv` | the 134-cell diff: 133 SCHEDULE DATE rows (with event id, week, teams, −1 delta) + 1 BANNER |
| `regression_log_v088.txt` | captured verifier output |

## 10. Rollback

Point current-state references back at `promotion_v0.8.7/…v0.8.7_AUTHORITATIVE.xlsx`
(`46671dee…15cd`). Dates return to UTC semantics; **no QB value, rating or model output is affected
either way.**

## 11. Outstanding — not part of this promotion

- **403 placeholder-time rows** must be re-derived once ESPN publishes real kickoff times. Some will
  move a day then. **This correction is not one-and-done for the season.**
- **QB closeout is NOT complete** — 21 rows remain UNCERTAIN, including Texas Tech (medical gate),
  Oregon State (deferred valuation) and Memphis (deliberately unresolved until kickoff).
- **The live Google Sheet has NOT been updated.** The connector cannot write cells; applying the 133
  date changes there remains an owner action.
