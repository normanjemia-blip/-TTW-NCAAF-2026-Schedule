# v0.8.2 AUTHORITATIVE — PROMOTION REPORT

**Promotion date:** 2026-08-18 (America/New_York)
**Predecessor:** v0.8.1 AUTHORITATIVE, which remains **frozen and unmodified**
**Change class:** QB data — one team record activated, plus the banner census it makes stale

| | |
|---|---|
| **Workbook** | `promotion_v0.8.2/TTW_College_Football_Power_Ratings_v0.8.2_AUTHORITATIVE.xlsx` |
| **SHA-256** | `225085449b5a1db5903a3998cb909be1f7ae0037782ea65d412bcb4d9d9490d0` |
| **Predecessor SHA-256** | `e2da9a4c28bd5c0f094ab06a2a85d3e31b37c2aba894f97f3415e15f799cdfd6` (frozen) |
| **Certificate** | `verify_v082.py` — **33 passed, 0 failed** |

---

## 1. Why v0.8.2 exists rather than an edit to v0.8.1

v0.8.1's promotion certificate asserts a specific identity: **v0.8.1 = v0.8.0 plus
exactly one documentation cell** (`START HERE!A1`), with 20 of 21 worksheet XML
parts byte-identical. Applying the NMSU activation inside v0.8.1 would have made
that identity false and destroyed the only artifact able to prove what v0.8.1
contained at promotion.

**v0.8.1 is therefore untouched.** Its workbook, verifier, diff CSV and regression
log are byte-identical to the promoted originals, and `verify_v081.py` still passes
unchanged. v0.8.2 carries the change forward under its own certificate.

---

## 2. The change

New Mexico State's quarterback record was coded `L / "Open competition"` on
2026-08-03, cited to a projection aggregator. A dated head-coach confirmation had
been published **five days earlier**:

> **KVIA ABC-7 El Paso, 2026-07-29** — head coach Tony Sanchez confirmed
> *"quarterback Trey Hedden will be the team's starter going into week one."*

The 2026-08-03 review missed it. The defect direction is **under-confident** — the
workbook was more uncertain than the evidence supported, the same class as the
earlier Missouri finding and the opposite of the more common over-confidence
pattern.

Confidence is set to **M, not H**. The Sanchez statement is definitive enough to
justify H, but no Week 0 official depth chart or game notes have been published and
at least one outlet still lists Adam Damante in the mix. **M clears the UNCERTAIN
gate identically to H**, so the activation is achieved without overstating the
evidence.

**Source discipline:** KVIA is the sole starter-designation source recorded in the
workbook. Corroborating material (KTSM, 247Sports, Sports Illustrated) informed the
decision but is not cited in the cell, because those pages were either undated or
not directly retrievable.

---

## 3. Exactly nine cells

Full detail in `diff_v081_to_v082.csv`. **Zero formula differences.**

| Sheet | Cell | Class | Old | New |
|---|---|---|---|---|
| START HERE | `A1` | documentation | `v0.8.1 …65 H / 40 M / 33 L…` | `v0.8.2 …65 H / 41 M / 32 L…` |
| QB VALUES | `C102` | QB data | *(blank)* | `Trey Hedden` |
| QB VALUES | `D102` | QB data | *(blank)* | `0` |
| QB VALUES | `E102` | QB data | `Open competition` | `Trey Hedden` |
| QB VALUES | `F102` | QB data | *(blank)* | `0` |
| QB VALUES | `H102` | QB data | `L` | `M` |
| QB VALUES | `I102` | QB data | Underdog Dynasty | KVIA ABC-7 El Paso |
| QB VALUES | `K102` | QB data | `2026-08-03` | `2026-08-18` |
| QB VALUES | `L102` | QB data | prior note | replacement note |

`G102` (QB delta) and `M102` (QB status) remain the original formulas.
`J102` (Reviewed for season) remains `2026`.

The banner change is confined to two substitutions: the version identifier and the
confidence census. The **73 Tier-1** statement is preserved and remains correct —
41 M + 32 L = 73.

---

## 4. Effect

**No model output moved.** `ENGINE!M` already coerces a blank QB delta to 0, so a
blank delta and a 0 delta are numerically identical. NMSU at FSU is **FSU -27.7**
before and after.

What changed is the **gate**:

| | v0.8.1 | v0.8.2 |
|---|---|---|
| QB status census | 39 UNCERTAIN / 99 OK | **38 UNCERTAIN / 100 OK** |
| Confidence census | 65 H / 40 M / 33 L | **65 H / 41 M / 32 L** |
| Tier-1 population | 73 | 73 *(unchanged)* |
| Nonzero QB values | 0 | **0** |
| Week 0 games blocked by QB | 5 of 8 | **4 of 8** |

`NMSU @ FSU` is the game that cleared. The four still blocked are `UNC @ TCU`
(UNC), `HAW @ STAN` (STAN), `SJSU @ USC` (SJSU) and `MEM @ UNLV` (both sides).

---

## 5. Unchanged and verified

Market lines 0 · BET toggle `N` · `B22`/`B23` blank so totals remain `NOT AVAILABLE`
· `SETTINGS!B4` and `B5` still blank · NDSU and Sacramento State retain transitional
safeguards · 888 games / 761 FBS-v-FBS / 127 FCS — NO PLAY · 21 sheets in identical
order with identical visibility · named ranges preserved · all 14 AUDIT structural
invariants pass.

---

## 6. Files

| File | Role |
|---|---|
| `TTW_College_Football_Power_Ratings_v0.8.2_AUTHORITATIVE.xlsx` | the workbook |
| `build_v082.py` | deterministic build from frozen v0.8.1; asserts every precondition |
| `verify_v082.py` | promotion certificate — **read-only, writes nothing** |
| `make_v082_artifacts.py` | generates the diff CSV and regression log explicitly |
| `diff_v081_to_v082.csv` | the nine-cell diff, accurately classified |
| `regression_log_v082.txt` | captured verifier output |

**Design note.** `verify_v081.py` rewrote `diff_v080_to_v081.csv` and
`regression_log_v081.txt` as a side effect of running, so verifying a modified
workbook silently overwrote promotion history. v0.8.2 separates the two: the
verifier only reads, and artifacts are produced by an explicit generator.

---

## 7. Rollback

v0.8.2 is numerically inert relative to v0.8.1, so rollback carries no model risk.

1. **Level 1** — point the current-state references back at
   `promotion_v0.8.1/…v0.8.1_AUTHORITATIVE.xlsx` (`e2da9a4c…cdfd6`). NMSU returns
   to `L / UNCERTAIN` and Week 0 blocked games return to five.
2. **Level 2** — v0.8.1 is frozen in this repository and needs no restoration.
3. **Level 3** — full model rollback to v0.6.2 (`bbb17b50…a838efd`) per
   `promotion_v0.8.0/ROLLBACK.md`. Not warranted by anything in this promotion.

**Recheck trigger:** publication of an official NMSU Week 0 depth chart or FSU game
notes. If they name a different starter, revisit `H102` before the 2026-08-29
kickoff.
