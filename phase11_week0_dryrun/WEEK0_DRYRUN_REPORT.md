# WEEK 0 FULL-CARD DRY RUN

**Date:** 2026-08-15 (America/New_York)
**Workbook:** `promotion_v0.8.1/TTW_College_Football_Power_Ratings_v0.8.1_AUTHORITATIVE.xlsx`
**SHA-256:** `e2da9a4c28bd5c0f094ab06a2a85d3e31b37c2aba894f97f3415e15f799cdfd6` — asserted before **and** after the run
**Harness:** `phase11_week0_dryrun/week0_dryrun.py` — read-only
**Result: 29 checks, 0 failures.**

---

## 1. What this run is, and why it is not a re-run of Phase 10

Phase 10 validated the Week 0 card by reading the workbook. This run **rebuilds
the card from the workbook's raw inputs** — SP+, FPI and TeamRankings raw values,
the source weights in `SETTINGS!B28:B32`, the alias table, the QB codes and the
schedule flags — following the formula chain transcribed cell-by-cell from v0.8.1,
and then reconciles the result against the Phase 10 checkpoint.

That makes it an **independent reproduction**, not a re-read. If the Phase 10
numbers had been wrong, or had drifted, this run would disagree with them.

**It does not.** All eight model spreads reproduce exactly.

---

## 2. The checkpoint is preserved, not replaced

`phase10_operational_validation/week0_card.json` is **unchanged**. The harness
reads it, compares, and reports differences. It never writes to it.

**Differences found: none.**

| Game | Checkpoint | Rebuilt | Match |
|---|---|---|:--:|
| UNC @ TCU *(Dublin, neutral)* | TCU -4.2 | TCU -4.2 | ✅ |
| HAW @ STAN | STAN -3.7 | STAN -3.7 | ✅ |
| NCST @ UVA | UVA -5.3 | UVA -5.3 | ✅ |
| SJSU @ USC | USC -35.2 | USC -35.2 | ✅ |
| NMSU @ FSU | FSU -27.7 | FSU -27.7 | ✅ |
| JVST @ NDSU | NDSU -7.0 | NDSU -7.0 | ✅ |
| SAC @ EMU | EMU -4.8 | EMU -4.8 | ✅ |
| MEM @ UNLV | UNLV -5.6 | UNLV -5.6 | ✅ |

Status and, where a line exists, edge / side / label also match.

**The verified Week 0 checkpoint stands: neutral HFA 0, TCU -4.2.**
Unrounded, the rebuild gives **4.16**, which prints as `TCU -4.2`.

---

## 3. The seven operating gates

### Gate 1 — FCS — NO PLAY
- **127** FCS games on the card; **127** resolve to `FCS — NO PLAY`.
- **0** carry any playable label.
- **761** FBS-v-FBS games. 127 + 761 = 888. ✅

### Gate 2 — neutral-site HFA, including Dublin
- **11** neutral-site games on the full-season card. **All 11** take `SETTINGS!B7 = 0`. None takes a home HFA.
- **UNC @ TCU, Aviva Stadium, Dublin** — `neutral_site = True`, `ENGINE!L = 0`, model **TCU -4.2** is a pure rating differential.
- **Counterfactual proved, not asserted:** flipping the neutral flag moves the line by exactly `SETTINGS!B6 = 2.5`, to **TCU -6.7**. The 2.8-point edge on UNC would have all but vanished. The flag is load-bearing and it is set correctly.

### Gate 3 — QB uncertainty gating
- **39** teams QB UNCERTAIN.
- **5 of 8** Week 0 games inherit it (UNC, STAN, SJSU, NMSU, MEM, UNLV are the L-coded teams involved).
- **No** QB UNCERTAIN game can reach `BET` anywhere on the 888-game card.
- **Proved independent of the toggle:** with `B11` forced to `Y` and a fabricated 7.8-point edge, the Dublin game still returns `INVESTIGATE`, because status ≠ READY. QB gating binds on its own.

### Gate 4 — market-line staleness
- `B13` stale threshold = **5 days**. ✅
- `STALE LINE` count = **0** — **and the harness records *why*: `SETTINGS!B5` is blank, so `CALC!Q` short-circuits to 0.** A clean `0` here is *not* evidence that lines are fresh. It is evidence that the check is switched off.
- **This remains the single most dangerous live-operation gap.** See §4.

### Gate 5 — spread sign conventions
| Case | Expected | Observed |
|---|---|---|
| Home favorite (TCU -7) | market home spread **negative** | `T = -7.0` ✅ |
| Edge arithmetic | `4.2 + (-7.0) = -2.8` | `V = -2.84` ✅ |
| Negative edge | value on **away** | `UNC` ✅ |
| Away favorite (UNC -3) | market home spread **positive** | `T = +3.0` ✅ |
| Edge arithmetic | `4.2 + 3.0 = 7.2` | `V = 7.16` ✅ |
| Positive edge | value on **home** | `TCU` ✅ |

Both directions tested. The convention matches the START HERE worked example.

### Gate 6 — BET toggle OFF
- `B11 = N`. **0** games produce `BET` anywhere on the card.
- Toggle proved to be a real constraint, not a vacuous pass — see Gate 3.

### Gate 7 — totals disabled
- `B22` blank, `B23` blank. Totals stay off for 2026 by decision. ✅

---

## 4. Live-operation blockers

Ranked by what they cost if ignored.

| # | Blocker | Consequence | Owner action |
|:--:|---|---|---|
| **1** | **`SETTINGS!B5` blank ⇒ stale-line protection inactive**, and it reports a clean `0` while inactive | A five-week-old line reads `READY`. This is a money risk the moment lines are entered. | Set `B5` to today's date **before** entering any market line |
| **2** | **`SETTINGS!B4` blank** (current week) | `START HERE!C7` prompts; status logic cannot reach `READY` | Set `B4` to the week being priced |
| **3** | **Google Sheet timezone unset and unverifiable** | Dates entered in the Sheet may land on the wrong day; lost on every re-import | File → Settings → Time zone → America/New_York |
| **4** | **No cell protection applied** | A mis-aimed paste silently overwrites formulas; the workbook stores **no cached results**, so nothing looks stale and nothing errors — a number is just wrong | Apply `phase9a_production_config/SHEETS_PROTECTION_MAP.md`, amended by Phase 9B §4 (IMPORT STATS `K6:K205` **RESTRICTED**, `A6:J205` editable) |
| **5** | **Production master still titled `… AUTHORITATIVE 4`** | Sibling copies `1`/`2`/`3` can be confused for the master | Rename to `… — PRODUCTION MASTER`; park or delete siblings |
| **6** | **32 of 33 QB exception records are overdue** as of 2026-08-15 (all stamped due 2026-08-03) | 39 teams stay `QB UNCERTAIN`, suppressing every edge they touch — including 5 of the 8 Week 0 games | Run the sweep (§5) |

**Blockers 1–5 are all owner actions in the Sheets UI. None can be done through
the available connector** — the Google Drive connector exposes no Sheets API, so
there is no way to write a cell, set a timezone, rename a file, or apply a
protected range. That limitation is unchanged since Phase 9B.

---

## 5. The August 22–24 dry-run window — exact tasks

Wagers are placed Tuesday–Thursday for CLV; Week 0 kicks off **Saturday
2026-08-29** (two games slip to 8/30). The 22nd is a Saturday and the 24th a
Monday, so this window is **preparation, not pricing** — no line should be bet
out of it.

### Saturday 22 August — configuration
1. Confirm the archive SHA is still `e2da9a4c…cdfd6`. If it is not, stop.
2. **Rename** the production master, dropping the trailing ` 4`. Confirm no ` 1` / ` 2` / ` 3` siblings survive.
3. **Set the timezone** to America/New_York (File → Settings). Do this *before* entering any date.
4. **Apply the protection map** — hidden sheets first, then RESTRICTED on START HERE / DASHBOARD / DATA QUALITY / ENGINE, then WARNING on the input sheets.
5. **Test one full IMPORT STATS paste** before trusting the protection. Confirm `AUDIT` still reads **0 failing invariants**.

### Sunday 23 August — QB sweep
6. Run `python3 phase8_4_qb_monitoring/scripts/due_this_sweep.py 2026-08-23`. Expect **33 records due** — 27 open competition, 3 injury/availability, 2 conflicting sourcing, plus TTU.
7. Work the backlog team-by-team against **primary sources only** — official depth charts, named-coach statements, verified beat reporting. Do **not** infer a starter from a preseason projection, and do **not** treat absence of evidence as proof a competition is closed.
8. Record resolutions in the pending ledger. **H = confirmed starter · M = clear leader not officially named · L = genuine competition or unverifiable.**
9. Build any candidate through `build_qb_candidate.py --source <v0.8.1> …`. It refuses to write when no approved resolution exists, and deletes the candidate if verification fails. **Do not hand-edit `QB VALUES`.**

### Monday 24 August — dry run proper
10. **Make the working copy first:** File → Make a copy → `TTW WORKING 2026-08-24 Wk0`. Everything below happens in the copy.
11. Set `SETTINGS!B4 = 0` and `SETTINGS!B5 = 2026-08-24`. **Both, before any line.**
12. Enter the Week 0 market lines available. Confirm `DATA QUALITY` moves off `PENDING LINE` only for the games actually priced.
13. Re-run `python3 phase11_week0_dryrun/week0_dryrun.py`. It must stay **29/0**.
14. Confirm the neutral-site handling on **UNC @ TCU** by eye: `ENGINE!L` = 0, model **TCU -4.2**.
15. **Leave `B11 = N`.** The 2026 season has no BET authorisation yet. Every edge should read `LEAN` or `INVESTIGATE`.
16. Confirm `B22` / `B23` are still blank and `Model total` reads `NOT AVAILABLE`.

### Do not, during this window
- Do not bet out of the dry run. It is a rehearsal.
- Do not set `B11 = Y`.
- Do not populate `B22` / `B23` to "switch totals on" — totals are disabled by decision, not by oversight.
- Do not edit the archive `.xlsx`, and do not type into the production master.

---

## 6. Reproducibility notes

- The harness derives priors from **SP+, FPI and TeamRankings only**. `PRESEASON!L` (TTW 2025) and `PRESEASON!U` (VSiN) are blank by decision, so available weight is `0.30 + 0.25 + 0.15 = 0.70` and the blend renormalises by its own rule. **No substitute was invented for the missing TTW prior, and VSiN was not blended in.**
- Effective games = 0 across the board, so `TEAM RATINGS!I` collapses to the prior and the fade table is not exercised. That is correct for preseason and will change the first time results load.
- `CALC!Q` (stale) is hard-coded to 0 in the harness **because that is what the formula does while `B5` is blank** — not because staleness was skipped. When `B5` is set, this path needs re-testing with a live line.
