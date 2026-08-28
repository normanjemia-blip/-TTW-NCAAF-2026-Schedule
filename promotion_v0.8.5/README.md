# v0.8.5 AUTHORITATIVE — REV 2 ITEMS 1–5

**Promotion date:** 2026-08-24 (America/New_York)
**Predecessor:** v0.8.4 AUTHORITATIVE — **frozen and unmodified**
**Authorising document:** `TTW_v084_QB_Closeout_20260824_REV2.md`, items 1–5, approved by the owner

| | |
|---|---|
| **Workbook** | `promotion_v0.8.5/TTW_College_Football_Power_Ratings_v0.8.5_AUTHORITATIVE.xlsx` |
| **SHA-256** | `0676aa1a05d661ca0d99c917c8dc471c0030128cc42ea8fd1bd2f17dcea767be` |
| **Predecessor SHA-256** | `ed5d3b3d9aa3dd4f845e91688216a28276aaa0b3e4bd68ba09a9ceb96a8adaff` (frozen) |
| **Certificate** | `verify_v085.py` — **53 passed, 0 failed** |
| **Change** | 33 cells · **8 zeros** · **zero formula changes** · **zero model-output changes** |

---

## 1. What was applied — approved scope only

### Activations (4 rows)

| Team | Row | Confidence | Starter | Evidence |
|---|:--:|:--:|---|---|
| **Syracuse** | 69 | `L → H` | Steve Angeli | Official Syracuse Athletics camp preview 2026-08-04 + position review 2026-08-17; retained-incumbent clause |
| **Alabama** | 6 | `L → H` | Keelon Russell | Kalen DeBoer's decision over Austin Mack, confirmed 2026-08-22 |
| **Tennessee** | 18 | `L → H` | Faizon Brandon | Josh Heupel, team meeting, 2026-08-24 |
| **Georgia Southern** | 131 | `M` *(unchanged)* | Max Johnson | ESPN + Pete Thamel, 2026-08-23 |

### Record correction (1 row)

| Team | Row | Change |
|---|:--:|---|
| **Fresno State** | 75 | candidate field → `Open (Khristian Martin / Jayden Mandal)`. **Confidence stays `L`, status stays UNCERTAIN.** Braden Atkinson confirmed carried on Oregon State row 76, never present here. |

Plus `START HERE!A1` — version identifier and confidence census.

### Deliberately NOT applied

| Item | Row | Why |
|---|:--:|---|
| **Rutgers** | 35 | Awaiting approval. Supplemental packet issued separately. |
| **Colorado State** | 74 | The owner ruled the field should read `Hauss Hejny vs. K'saan Farrar`, but the same instruction said **"apply only those approved cells"** and Colorado State was not among items 1–5. Held with Rutgers rather than assumed. |

Certificate checks 6.x assert Colorado State, Rutgers, Texas Tech, Stanford, Northern
Illinois and Tulane are **byte-identical to v0.8.4**.

---

## 2. The eight zeros — justification

**Eight numerical values were written. All eight are the integer `0`**, two on each
activated row (`D` and `F`).

`QB VALUES!G = F − D`, so `0 − 0 = 0` — the QB delta is **exactly zero** and `ENGINE!M`
contributes **nothing** to any game.

The zeros are **not a rating of the quarterback.** They record that the confirmed active
starter **is** the quarterback the preseason blend already assumed, so **no deviation
applies**. A blank leaves `G` blank, which forces status UNCERTAIN; a zero clears the
gate while moving no number. **That is why activation is numerically inert.**

Certificate checks 2.1–2.x assert exactly eight zeros on exactly the four activated rows,
and **zero nonzero QB values anywhere in the workbook**.

---

## 3. Censuses

| | v0.8.4 | **v0.8.5** | Target |
|---|:--:|:--:|:--:|
| QB status | 104 OK / 34 UNCERTAIN | **108 OK / 30 UNCERTAIN** | ✅ exact |
| Confidence | 69 H / 40 M / 29 L | **72 H / 40 M / 26 L** | ✅ exact |
| Total | 138 | **138** | ✅ |
| Nonzero QB values | 0 | **0** | ✅ |

Derivation: Syracuse, Alabama and Tennessee each `L → H` (−3 L, +3 H); Georgia Southern
stays `M`. All four move UNCERTAIN → OK. Texas Tech and Fresno State remain UNCERTAIN.

---

## 4. Model outputs — unchanged

The certificate re-derives five spreads from the workbook's own inputs and asserts each
is unchanged:

`MEM at UNLV -5.6` · `UNC at TCU -4.2` · `NMSU at FSU -27.7` ·
`SJSU at USC -35.2` · `HAW at STAN -3.7`

It also asserts **every QB delta in the workbook is 0 or blank**, so `ENGINE!M`
contributes nothing anywhere.

Baseline preserved: **138 teams · 888 games · 761 FBS-v-FBS · 127 FCS-involved · 0 BLOCK.**
Market lines blank in the repo artifact · BET toggle `N` · `B22`/`B23` blank ·
NDSU and Sacramento State transitional.

Week 0 QB gating is unaffected — none of the four activated teams plays in Week 0.
**Memphis at UNLV remains the single QB-gated Week 0 game.**

---

## 5. Validation

| Suite | Result |
|---|---|
| `promotion_v0.8.5/verify_v085.py` | **53 passed, 0 failed** |
| `promotion_v0.8.4/verify_v084.py` | 49 passed, 0 failed |
| `promotion_v0.8.3/verify_v083.py` | 42 passed, 0 failed |
| `promotion_v0.8.2/verify_v082.py` | 33 passed, 0 failed |
| `promotion_v0.8.1/verify_v081.py` | 0 failures |
| `phase11_week0_dryrun/week0_dryrun.py` | 30 passed, 0 failed |
| `validate_schedule.py` | ALL HARD-FAIL CHECKS PASSED |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | 15/15 |
| `git diff --check` | clean |

---

## 6. Files

| File | Role |
|---|---|
| `TTW_College_Football_Power_Ratings_v0.8.5_AUTHORITATIVE.xlsx` | the workbook |
| `build_v085.py` | deterministic build from frozen v0.8.4; asserts exactly 8 zeros and the untouched rows |
| `verify_v085.py` | promotion certificate — **read-only** |
| `make_v085_artifacts.py` | generates the diff CSV and regression log explicitly |
| `diff_v084_to_v085.csv` | the 33-cell diff, classified ACTIVATION vs RECORD CORRECTION |
| `regression_log_v085.txt` | captured verifier output |

## 7. Rollback

Point current-state references back at `promotion_v0.8.4/…v0.8.4_AUTHORITATIVE.xlsx`
(`ed5d3b3d…a892`). The census returns to 104 OK / 34 UNCERTAIN and 69 H / 40 M / 29 L.

**No model output is affected either way.** This promotion changes QB record text, three
confidence codes, eight zeros and the banner — and touches nothing the engine reads
numerically.

## 8. Not complete

The QB closeout is **not** declared complete. Outstanding at promotion time: Rutgers
(pending approval), Colorado State (ruled but not applied), Texas Tech (medically gated),
Washington State (decision promised 2026-08-24, unpublished at 10:49 EDT), and the
live-Sheet application of Northern Illinois and Tulane.
