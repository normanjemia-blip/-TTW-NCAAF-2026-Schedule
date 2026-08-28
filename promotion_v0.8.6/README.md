# v0.8.6 AUTHORITATIVE — SUPPLEMENTAL PACKET ITEMS 1–3

**Promotion date:** 2026-08-24 (America/New_York)
**Predecessor:** v0.8.5 AUTHORITATIVE — **frozen and unmodified**
**Authorising document:** `TTW_Supplemental_Approval_Packet_20260824.md`, items 1–3, approved by the owner

| | |
|---|---|
| **Workbook** | `promotion_v0.8.6/TTW_College_Football_Power_Ratings_v0.8.6_AUTHORITATIVE.xlsx` |
| **SHA-256** | `bb76901a96a3fa63e14f0cc582891de82846c12fa5f7ce41d182c8addab967f9` |
| **Predecessor SHA-256** | `0676aa1a05d661ca0d99c917c8dc471c0030128cc42ea8fd1bd2f17dcea767be` (frozen) |
| **Certificate** | `verify_v086.py` — **56 passed, 0 failed** |
| **Change** | 18 cells · **4 zeros** · **zero formula changes** · **zero model-output changes** |

---

## 1. What was applied — approved scope only

### Activations (2 rows)

| Team | Row | Confidence | Starter | Evidence |
|---|:--:|:--:|---|---|
| **Rutgers** | 35 | `M` *(unchanged)* | Dylan Lonergan | ESPN / Pete Thamel, 2026-08-24, via On3 The Knight Report + 247Sports |
| **Washington State** | 80 | `L → H` | Caden Pinnick | **Washington State's own announcement** (`@WSUCougarFB`), 2026-08-24, reported by the Spokesman-Review |

### Record correction (1 row)

| Team | Row | Change |
|---|:--:|---|
| **Colorado State** | 74 | active field → `Hauss Hejny vs. K'saan Farrar`. **Confidence stays `L`, status stays UNCERTAIN, no numerical entry.** The prior 2026-08-03 note is retained verbatim with the ruling appended. |

Plus `START HERE!A1` — version identifier and confidence census.

### Why the two confidence tiers differ

Washington State is `H` because **the program itself announced it**; Rutgers is `M` because the
naming is **reporter-sourced**, matching the precedent set for North Carolina and Georgia Southern.
The distinction is provenance, not conviction.

---

## 2. Three constraints the build enforces mechanically

| Constraint | How it is enforced |
|---|---|
| **`C80` must not be rewritten** | Pinnick was **already** the recorded baseline QB. The build asserts `C80 == "Caden Pinnick"` *before* writing and never touches it; the 18-cell diff confirms `C80` is absent. Certificate check 5.3. |
| **Darius Curry must not be added anywhere** | The build scans every cell of every sheet and **raises** if the string appears. It caught a violation on the first run — the ruling note I had drafted *named* him — and the note was rewritten. Certificate check 5.7. |
| **`H35` must stay `M`** | Rutgers already carried `M`, so no confidence write occurs. `H35` is absent from the diff. |

---

## 3. The four zeros — justification

**Four numerical values were written. All four are the integer `0`**, two on each activated row
(`D` and `F`).

`QB VALUES!G = F − D`, so `0 − 0 = 0` — the QB delta is **exactly zero** and `ENGINE!M` contributes
**nothing** to any game. The zeros are **not a rating of the quarterback.** They record that the
confirmed active starter **is** the quarterback the preseason blend already assumed, so **no
deviation applies.**

**Washington State is the strongest possible case of this.** The workbook's 2026-08-04 entry recorded
Pinnick as the baseline *while explicitly refusing to call him the starter* — correctly, at `L`, since
camp was wide open. The announcement confirms that baseline rather than departing from it, so the
zero is **literally** true, not merely conventional.

Workbook-wide zero count: **216 → 220**, exactly `+4`, and `220 = 2 × 110 OK rows` — every OK row
carries exactly one `0/0` pair and nothing else is numeric. Certificate check 2.3.

---

## 4. The baseline-QB invariant

Every one of v0.8.5's **108 OK rows carried a populated baseline quarterback in column `C` — 108 of
108, no exceptions.** Blank `C` occurred only on UNCERTAIN rows.

Rutgers row 35 had `C` **blank**. Activating with only the two zeros would have made it the first OK
row in the workbook with no baseline quarterback — an unauditable zero, since nothing would record
*deviation from whom*. `C35 = Dylan Lonergan` was therefore approved and applied; the SI source the
prior entry cited names him as the projected starter, so he is the quarterback the preseason blend
assumed.

The build asserts the invariant held in v0.8.5 before writing; the certificate asserts it holds
across all **110** OK rows afterwards. Checks 5.4 and 5.8.

---

## 5. Censuses

| | v0.8.5 | **v0.8.6** | Target |
|---|:--:|:--:|:--:|
| QB status | 108 OK / 30 UNCERTAIN | **110 OK / 28 UNCERTAIN** | ✅ exact |
| Confidence | 72 H / 40 M / 26 L | **73 H / 40 M / 25 L** | ✅ |
| Total | 138 | **138** | ✅ |
| Nonzero QB values | 0 | **0** | ✅ |

Only **one** confidence code moves: Washington State `L → H`. Rutgers was already `M`; Colorado State
stays `L`. Both activations clear UNCERTAIN → OK.

---

## 6. Model outputs — unchanged

The certificate re-derives five spreads from the workbook's own inputs and asserts each is unchanged:

`MEM at UNLV -5.6` · `UNC at TCU -4.2` · `NMSU at FSU -27.7` · `SJSU at USC -35.2` · `HAW at STAN -3.7`

It also asserts **every QB delta in the workbook is 0 or blank**, and specifically that Rutgers' and
Washington State's deltas are exactly `0`.

Baseline preserved: **138 teams · 888 games · 761 FBS-v-FBS · 127 FCS-involved · 0 BLOCK.**
Market lines blank in the repo artifact · BET toggle `N` · `B22`/`B23` blank ·
NDSU and Sacramento State transitional.

None of the three teams plays in Week 0. **Memphis at UNLV remains the single QB-gated Week 0 game.**

---

## 7. Validation

| Suite | Result |
|---|---|
| `promotion_v0.8.6/verify_v086.py` | **56 passed, 0 failed** |
| `promotion_v0.8.5/verify_v085.py` | 53 passed, 0 failed |
| `promotion_v0.8.4/verify_v084.py` | 49 passed, 0 failed |
| `promotion_v0.8.3/verify_v083.py` | 42 passed, 0 failed |
| `promotion_v0.8.2/verify_v082.py` | 33 passed, 0 failed |
| `promotion_v0.8.1/verify_v081.py` | 0 failures |
| `phase11_week0_dryrun/week0_dryrun.py` | 30 passed, 0 failed |
| `validate_schedule.py` | ALL HARD-FAIL CHECKS PASSED |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | 15/15 |
| `git diff --check` | clean |

The Week 0 dry run's UNCERTAIN-count assertion was updated `30 → 28` — the census legitimately moved
when Rutgers and Washington State cleared. No Week 0 game, spread, edge, side or label changed.

---

## 8. Manifest defect repaired alongside this promotion

`PROJECT_MANIFEST.json` recorded the **wrong SHA-256 for two rollback targets**: both
`/rollback` (v0.6.2) and `/intermediate_rollback` (v0.8.0) carried v0.8.5's hash, left behind by an
earlier blanket version-bump replace. A rollback verified against those values would have failed.

Corrected to the true hashes, recomputed from the files:

- v0.6.2 → `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd`
- v0.8.0 → `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7`

---

## 9. Files

| File | Role |
|---|---|
| `TTW_College_Football_Power_Ratings_v0.8.6_AUTHORITATIVE.xlsx` | the workbook |
| `build_v086.py` | deterministic build from frozen v0.8.5; asserts 18 cells, exactly 4 zeros, the untouched rows, and the Curry prohibition |
| `verify_v086.py` | promotion certificate — **read-only** |
| `make_v086_artifacts.py` | generates the diff CSV and regression log explicitly |
| `diff_v085_to_v086.csv` | the 18-cell diff, classified ACTIVATION vs RECORD CORRECTION |
| `regression_log_v086.txt` | captured verifier output |

## 10. Rollback

Point current-state references back at `promotion_v0.8.5/…v0.8.5_AUTHORITATIVE.xlsx`
(`0676aa1a…67be`). The census returns to 108 OK / 30 UNCERTAIN and 72 H / 40 M / 26 L.

**No model output is affected either way.**

## 11. Not complete

The QB closeout is **not** declared complete. Outstanding: **Tulane** (packet issued, awaiting
approval), **Texas Tech** (medically gated), 27 other unresolved competitions, and the live-Sheet
application of the approved changes plus the outstanding Northern Illinois and Tulane corrections.

**The live Google Sheet has not been updated.** The connector cannot write cells; live application
remains an owner action.
