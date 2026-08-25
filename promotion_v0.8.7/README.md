# v0.8.7 AUTHORITATIVE — SEVEN ACTIVATIONS + OREGON STATE OPTION B

**Promotion date:** 2026-08-25 (America/New_York)
**Predecessor:** v0.8.6 AUTHORITATIVE — **frozen and unmodified**
**Authorising document:** `TTW_v087_Approval_Packet_20260825.md` (`6cf7393`), plus the owner's
Week 0 reconciliation of UNLV and Memphis

| | |
|---|---|
| **Workbook** | `promotion_v0.8.7/TTW_College_Football_Power_Ratings_v0.8.7_AUTHORITATIVE.xlsx` |
| **SHA-256** | `46671deeaaa94d98c63cb32d0e94af9907e76e7e2638de431b918987df2e15cd` |
| **Predecessor SHA-256** | `bb76901a96a3fa63e14f0cc582891de82846c12fa5f7ce41d182c8addab967f9` (frozen) |
| **Certificate** | `verify_v087.py` — **89 passed, 0 failed** |
| **Change** | **69 cells** · **14 zeros** · **zero formula changes** · **zero model-output changes** |

---

## 1. What was applied

### Activations — 7 rows, 14 zeros, every one a BASELINE MATCH

| Team | Row | Conf | Starter | Provenance | Date |
|---|:--:|:--:|---|---|:--:|
| **Tulane** | 91 | `L → M` | Zeon Chriss-Gremillion | ESPN / Thamel "Sources:" | 2026-08-24 |
| **Arkansas** | 7 | `L → H` | KJ Jackson | **Team announcement** + Silverfield on the record | 2026-08-23 |
| **Florida** | 9 | `L → H` | Aaron Philo | **Official athletics release** + HC Sumrall | 2026-08-24 |
| **Nebraska** | 29 | `L → H` | Anthony Colandrea | **HC Matt Rhule announcement** | 2026-08-22 |
| **Ohio** | 113 | `M` *(unchanged)* | Nick Poulos | ESPN / Thamel | 2026-08-22 |
| **South Florida** | 89 | `L → M` | Michael Van Buren Jr. | ESPN / Thamel "Sources:" | 2026-08-24 |
| **UNLV** | 125 | `L → M` | Jackson Arnold | **OWNER-CONFIRMED — not an official announcement** | 2026-08-25 |

### Record-only, no zeros — Oregon State Option B

| Team | Row | Treatment |
|---|:--:|---|
| **Oregon State** | 76 | `C76` **preserves Maalik Murphy** as the preseason baseline · `E76` records **Braden Atkinson** as active · **`D76`/`F76` left BLANK** · `M` retained · **stays UNCERTAIN** |

### Text corrections — 3 rows, no numerics, all stay `L` / UNCERTAIN

| Team | Row | Corrected field |
|---|:--:|---|
| **Memphis** | 85 | `Marcus Stokes / Air Noland; decision withheld until kickoff.` |
| **Vanderbilt** | 21 | `Open (Jared Curtis / Blaze Berlowitz / Whit Muschamp)` |
| **Kansas** | 48 | `Open (Cole Ballard / Isaiah Marshall)` |

Plus `START HERE!A1` — version identifier and confidence census.

---

## 2. The exact diff — 69 cells

| Team | Class | Cells |
|---|---|:--:|
| South Florida · Tulane | ACTIVATION | 8 each |
| Arkansas · Florida · Nebraska · Ohio · UNLV | ACTIVATION | 7 each |
| Oregon State | RECORD ONLY (no zeros) | 5 |
| Memphis · Vanderbilt · Kansas | TEXT CORRECTION | 4 each |
| `START HERE!A1` | BANNER | 1 |
| **TOTAL** | | **69** |

Arkansas and UNLV write 7 rather than 8 because **`C` already held the correct baseline and was not
rewritten.** Ohio writes 7 because its confidence was already `M`. Florida's and Nebraska's `E` cells
already held the exact starter string, so those writes are not diffs.

Full row-level detail: `diff_v086_to_v087.csv`.

---

## 3. UNLV — the baseline-match test, and honest provenance

**UNLV PASSED the baseline-match test.** `C125` already read **`Jackson Arnold`** in v0.8.6, set on
2026-08-04. The operative starter and the preseason assumption are therefore the same player, the
deviation is **literally zero**, and `C125` was **not rewritten** — certificate check 5.x asserts it
is byte-identical to v0.8.6.

**Provenance is recorded as OWNER-CONFIRMED, not "officially announced."** The note states plainly
that **HC Dan Mullen has not formally named a starter** — he says Arnold and Alex Orji will both play
and has declined to name a front-runner throughout camp. Confidence is `M`, **not** `H`, precisely
because no team or coach naming exists. **Alex Orji is expected to play** and that is preserved in
the note, along with his 2025 LCL/hamstring recovery.

---

## 4. Memphis — deliberately unresolved, and why the Week 0 gate holds

Memphis is **not** activated. No qualifying public source has named a starter; the live competition
remains **Marcus Stokes vs Air Noland**; and HC Charles Huff intends to keep the decision private
until kickoff — *"The team will know before you guys do. You guys won't know until they flip the
coin."*

**Unofficial depth charts placing Stokes first are inference only** and do not satisfy the activation
rule. Stokes was **not** activated merely because he is the current best inference. `D85`/`F85` stay
blank; Memphis stays `L` / UNCERTAIN.

**Consequence, asserted by the certificate (7.4–7.6): UNLV is now OK, Memphis is still UNCERTAIN, and
Memphis at UNLV therefore remains QB-gated.** Recheck trigger: an official announcement, an official
game-day depth chart, or the first offensive snap.

---

## 5. Oregon State — why no zeros were manufactured

Oregon State is the **first row in the project where the named starter is not the quarterback the
preseason blend assumed.** Atkinson displaced **Maalik Murphy**, the incumbent the preseason priced.

The zeros mean something specific here: *"the active starter **is** the quarterback the preseason
rating already assumed, so no deviation applies."* For Oregon State that sentence is false. Writing
`0/0` would assert the Murphy → Atkinson change is worth exactly zero — a valuation claim the
deviation-only convention was never built to carry.

So `C76` preserves Murphy as the baseline, `E76` records Atkinson as active, the numerical cells stay
blank, and the row stays UNCERTAIN pending the QB-value rubric. Certificate check **7.3** asserts
Oregon State's delta is **blank, not `0`** — deferred, not asserted.

---

## 6. Censuses — recomputed directly from rows 6–143

| | v0.8.6 | **v0.8.7** |
|---|:--:|:--:|
| QB status | 110 OK / 28 UNCERTAIN | **117 OK / 21 UNCERTAIN** |
| Confidence | 73 H / 40 M / 25 L | **76 H / 43 M / 19 L** |
| Total | 138 | **138** |
| Nonzero QB values | 0 | **0** |
| Workbook zero count | 220 = 2 × 110 | **234 = 2 × 117** |

Six confidence codes move: Arkansas, Florida, Nebraska each `L → H` (+3 `H`); Tulane, South Florida,
UNLV each `L → M` (+3 `M`); −6 `L`. Ohio was already `M` and Oregon State stays `M`, so neither moves
a code.

**Baseline-QB invariant: all 117 OK rows carry a populated baseline quarterback in column `C`** —
117/117, no exceptions (check 5.12).

---

## 7. Model outputs — unchanged

Five spreads re-derived from the workbook's own inputs and asserted identical:

`MEM at UNLV -5.6` · `UNC at TCU -4.2` · `NMSU at FSU -27.7` · `SJSU at USC -35.2` · `HAW at STAN -3.7`

Every QB delta in the workbook is **0 or blank**, so `ENGINE!M` contributes exactly nothing to any of
the 888 games. **The only thing that moved is gate status.**

Baseline preserved: **138 teams · 888 games · 761 FBS-v-FBS · 127 FCS-involved · 0 BLOCK.**
Market lines blank in the repo artifact · BET toggle `N` · `B22`/`B23` blank · NDSU and Sacramento
State transitional · AUDIT invariant unchanged · **Darius Curry appears nowhere.**

**`IMPORT SCHEDULE` is untouched** (check 8.6) — the schedule date candidate is **not** folded in.

---

## 8. Validation — complete chain

| Suite | Result |
|---|---|
| `promotion_v0.8.7/verify_v087.py` | **89 passed, 0 failed** |
| `promotion_v0.8.6/verify_v086.py` | 56 passed, 0 failed |
| `promotion_v0.8.5/verify_v085.py` | 53 passed, 0 failed |
| `promotion_v0.8.4/verify_v084.py` | 49 passed, 0 failed |
| `promotion_v0.8.3/verify_v083.py` | 42 passed, 0 failed |
| `promotion_v0.8.2/verify_v082.py` | 33 passed, 0 failed |
| `promotion_v0.8.1/verify_v081.py` | 0 failures |
| `phase11_week0_dryrun/week0_dryrun.py` | 30 passed, 0 failed |
| `validate_schedule.py` | ALL HARD-FAIL CHECKS PASSED |
| `phase8_4_qb_monitoring/scripts/test_pipeline.py` | 15/15 |
| `schedule_candidate_v1/verify_schedule_candidate.py` | 41 passed, 0 failed *(candidate, unpromoted)* |
| `git diff --check` | clean |

The Week 0 dry run's UNCERTAIN assertion moved `28 → 21` with the census. **No Week 0 game, spread,
edge, side or label changed.**

---

## 9. Files

| File | Role |
|---|---|
| `TTW_College_Football_Power_Ratings_v0.8.7_AUTHORITATIVE.xlsx` | the workbook |
| `build_v087.py` | deterministic build from frozen v0.8.6; asserts 14 zeros, the untouched baselines, Option B's blank cells and the Curry prohibition |
| `verify_v087.py` | promotion certificate — **read-only**, 89 checks |
| `make_v087_artifacts.py` | generates the diff CSV and regression log explicitly |
| `diff_v086_to_v087.csv` | the 69-cell diff, classified ACTIVATION / RECORD ONLY / TEXT CORRECTION |
| `regression_log_v087.txt` | captured verifier output |

## 10. Rollback

Point current-state references back at `promotion_v0.8.6/…v0.8.6_AUTHORITATIVE.xlsx`
(`bb76901a…67f9`). The census returns to 110 OK / 28 UNCERTAIN and 73 H / 40 M / 25 L.
**No model output is affected either way.**

## 11. Not complete

The QB closeout is **not** declared complete. **21 rows remain UNCERTAIN**, including:

- **Texas Tech** (r52) — `H`, medically gated
- **Oregon State** (r76) — `M`, valuation deferred pending the QB-value rubric
- **Memphis** (r85) — `L`, deliberately unresolved until kickoff; keeps Week 0 QB-gated
- 18 further open competitions

**The schedule date candidate is built and verified 41/0 but NOT promoted.** On approval it rebases
onto v0.8.7 via `build_schedule_candidate.py --source`, then the 41-check certificate and the full
validator chain re-run. **The 403 placeholder-time games are not altered.**

**The live Google Sheet has not been updated.** The connector cannot write cells; live application
remains an owner action.
