# SCHEDULE DATE CANDIDATE v1 — **CANDIDATE ONLY, NOT PROMOTED**

**Built:** 2026-08-25 · **Base:** v0.8.6 AUTHORITATIVE, frozen at `c6bc5f8`
**Certificate:** `verify_schedule_candidate.py` — **41 passed, 0 failed**

| | |
|---|---|
| **Base SHA-256** | `bb76901a96a3fa63e14f0cc582891de82846c12fa5f7ce41d182c8addab967f9` *(unmodified)* |
| **Candidate SHA-256** | `d16c1d2cc725d16eeac77c3931df012d65650bc9e5beb73c647f50e5481288b1` |
| **Change** | **133 cells**, all in `IMPORT SCHEDULE` column **D** · zero formula changes · zero model-output changes |

> **This candidate is deliberately independent of the QB promotion chain.** It is not a QB version,
> it does not carry any QB proposal, and it must not be merged into one. When a QB version is
> promoted, rebase with `--source <that workbook>`; the correction is orthogonal and applies unchanged.

---

## 1. Canonical date semantics

> **`start_date` is the calendar date on which the game is played IN THE TIME ZONE OF ITS VENUE.**
> It is **not** the UTC date and **not** the US/Eastern date.

Codified once, in `espn_date_rule.py`, and imported by everything else:

```
timeValid = True    start_date = kickoff_utc.astimezone(venue_zone).date()

timeValid = False   ESPN has no announced kickoff and encodes the row as MIDNIGHT
                    US/EASTERN. That instant is a placeholder, not a kickoff;
                    converting it into a western venue zone would fabricate a
                    23:00 game on the PREVIOUS day.
                    start_date = kickoff_utc.astimezone(US/Eastern).date()
                    -> flagged by needs_rederivation() for re-derivation once a
                       real kickoff time is published
```

`venue_zone()` maps the ESPN venue address: non-US country → that country's zone; US state → state
zone, with **city overrides for split-zone states** (Memphis, Nashville, Murfreesboro, Bowling Green,
El Paso today; the table is written to cover others the schedule could reach). It **raises
`UnresolvedVenueZone` rather than falling back to UTC** — that fallback *is* the original defect.

### The defect being corrected

The extractor stored `.date()` off the UTC instant. Confirmed on **888 of 888 games**: `stored ==
ESPN UTC date`, without exception. Any kickoff after roughly 20:00 US/Eastern therefore rolled
forward a day — **133 games (15.0%)**, every one exactly **+1 day**, inventing **67 Sunday games that
are really Saturday games**.

---

## 2. Every file and cell changed

| Artifact | Change |
|---|---|
| `TTW_College_Football_Power_Ratings_SCHED1_CANDIDATE.xlsx` | **`IMPORT SCHEDULE!D6:D893` — 133 cells.** Nothing else, on any of the 21 sheets. |
| `TTW_2026_Verified_Schedule_ESPN_v1.1_LOCALDATES.csv` | **133 of 888 rows**, `start_date` field only |
| `espn_kickoff_snapshot.csv` | new evidence file — 888 rows: id, ESPN kickoff UTC, `timeValid`, venue city/state/country, resolved zone, local kickoff, canonical date, stored date, re-derivation flag |
| `espn_date_rule.py` · `build_schedule_candidate.py` · `verify_schedule_candidate.py` | new |
| **Production workbook, live Sheet, `…v1.0.csv`** | **UNTOUCHED** |

Certificate checks 1.1–1.4 assert: zero formula differences · only `IMPORT SCHEDULE` changed · only
column `D` changed · exactly 133 cells.

---

## 3. Every consumer of the date field — the full graph

Traced by scanning all 123,011 formulas:

```
IMPORT SCHEDULE!D  ──►  CLEAN!D  ──►  ENGINE!C  ──►  DASHBOARD!B
   (source)          1000 formulas  1000 formulas  1000 formulas
```

**That is the entire graph. The game date is display-only.**

| Check | Result |
|---|:--:|
| Consumers of the date column | **CLEAN, ENGINE, DASHBOARD only** |
| `CALC` formulas touching any date column — `CALC` drives every gate | **0** |
| `TODAY()` anywhere in the workbook | **0** |
| Staleness (`CALC!Q`) input | `SETTINGS!B5` − **MARKET LINES line date**, *not* the game date |

Because `CALC` never reads the game date and nothing is `TODAY()`-relative, **no gate, no status, no
edge and no rating can move.** `ENGINE!AI` status precedence is untouched.

---

## 4. Proof of invariance — certificate results

| Claim | Check | Result |
|---|---|:--:|
| **Event IDs unchanged** | 2.x `id` column byte-identical across all 888 rows | ✅ |
| **Kickoff timestamps unchanged** | 4.1 — the workbook stores no kickoff time, only a date; the ESPN instant is the **input** and is never written | ✅ |
| **Weeks unchanged** | 4.2 week distribution identical across 15 weeks | ✅ |
| | 4.3 no week's corrected span overlaps the previous week | ✅ |
| | 4.4 Week 0 still exactly 8 games | ✅ |
| **Formulas unchanged** | 1.1 zero formula differences workbook-wide | ✅ |
| **Ratings / model outputs unchanged** | 5.x all five reference spreads re-derived identical | ✅ |
| | 5.1 888 / 761 / 127 census intact | ✅ |
| **QB state unchanged** | 6.1–6.3 — 110 OK / 28 UNCERTAIN, 73 H / 40 M / 25 L, 0 nonzero QB values | ✅ |
| **Correction is exact** | 3.1 all 888 dates equal the canonical rule; 3.2 exactly 133 moved / 755 already correct; 3.3 every delta exactly −1 day | ✅ |
| **Other columns untouched** | 2.x season, week, neutral_site, away_team, home_team, venue, notes all byte-identical | ✅ |
| **CSV scope** | 9.1–9.3 same 888 ids; 133 rows differ; **no field other than `start_date` differs on any row** | ✅ |

### What visibly improves

| | As stored | **Corrected** |
|---|:--:|:--:|
| Saturday games | 720 | **751** |
| **Sunday games** | **70** | **3** |
| Week 0 | Sat + Sun split | **a single Saturday, 2026-08-29** |

The three surviving Sunday games are genuine, all Labor Day weekend 2026 (Labor Day is Monday
Sept 7): Louisville @ Ole Miss, **Washington State @ Washington**, Wisconsin @ Notre Dame. The lone
Monday game — SMU @ Florida State, Sept 7 — is a real Labor Day game and was already correct.

**The QB-gated Week 0 game moves:** Memphis @ UNLV is **Saturday 2026-08-29 at 19:00 PDT**, not
Sunday the 30th. ESPN's own record is `2026-08-30T02:00Z`; both teams' beat outlets say Aug 29.

---

## 5. A normal refresh cannot reintroduce UTC dates

Three independent mechanisms, all exercised by the certificate:

1. **No UTC fallback exists.** `venue_zone()` **raises `UnresolvedVenueZone`** for an unmapped venue.
   There is no code path that silently yields a UTC date, so the defect cannot recur by omission.
2. **The refresh guard.** `assert_not_utc_dates(records)` recomputes the canonical date for every row
   after ingestion and raises listing every violation. Run it at the end of every refresh.
   - Check **8.1** — guard **passes** on the candidate.
   - Check **8.2** — guard **fails on the old file and catches all 133**. The guard is *tested against
     a real regression*, not merely asserted.
3. **Idempotence.** Check **8.3** — re-applying the rule changes nothing, so repeated refreshes
   converge instead of oscillating.

### Known follow-up, not a defect

**403 of 888 rows have no announced kickoff yet** (`timeValid = false`) and currently take the
Eastern date, which is correct for a midnight-Eastern placeholder — all 403 already match. They are
flagged `needs_rederivation = True` in the snapshot and **must be re-derived once ESPN publishes real
kickoff times**; some will then move by a day. **This correction is not one-and-done for the season.**

---

## 6. Files

| File | Role |
|---|---|
| `espn_date_rule.py` | the canonical rule, zone maps, and the refresh guard — import this from any extractor |
| `build_schedule_candidate.py` | deterministic build from a frozen source workbook; `--source` rebases onto a later QB version |
| `verify_schedule_candidate.py` | certificate — **read-only**, 41 checks |
| `espn_kickoff_snapshot.csv` | 888-row evidence snapshot; makes the candidate reproducible without re-fetching ESPN |
| `TTW_2026_Verified_Schedule_ESPN_v1.1_LOCALDATES.csv` | corrected schedule file |
| `TTW_College_Football_Power_Ratings_SCHED1_CANDIDATE.xlsx` | corrected workbook |
| `../phase12_date_audit/` | the read-only audit and its 133-row diff |

## 7. If approved

1. Rebase onto the then-current QB production version: `build_schedule_candidate.py --source <that .xlsx>`.
2. Re-run `verify_schedule_candidate.py` plus the full validator chain (`verify_v0XX`, Week 0 dry run,
   `validate_schedule.py`, `test_pipeline.py`).
3. Promote as a **schedule** version with its own certificate — **not** folded into a QB promotion.
4. Wire `assert_not_utc_dates()` into the refresh job so the defect cannot return.
5. Apply the 133 date changes to the live Google Sheet **manually** — the connector cannot write cells.

**NOT PROMOTED. Awaiting approval.**
