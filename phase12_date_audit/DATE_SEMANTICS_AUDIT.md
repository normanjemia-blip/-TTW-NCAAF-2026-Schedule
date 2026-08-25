# DATE-SEMANTICS AUDIT — ALL 888 GAMES

**Status:** **READ-ONLY.** The workbook, the schedule CSV and the live Sheet are all **untouched**.
**Date:** 2026-08-24 · **Base:** v0.8.6 frozen at `c6bc5f8` (`bb76901a…67f9`)
**Reproduce:** `python3 phase12_date_audit/date_semantics_audit.py`
**Exact diff:** `phase12_date_audit/proposed_date_diff.csv` — **133 rows**

---

## 1. Verdict

> **The schedule stores each game's UTC calendar date, not its local date.**
> Confirmed on **888 of 888 games** — every single row matches ESPN's UTC date exactly.
> **133 games (15.0%)** therefore carry a date one day later than the game is actually played.
> **All 133 discrepancies are exactly +1 day. There are no other offsets.**

**No game changes week. No game crosses the Week 0 boundary. No rating or model output is affected.**

---

## 2. Method

Every row was joined to ESPN by its own `id` — the same event id already stored in the file, so the
match is exact, not fuzzy. **888 of 888 matched.** For each game four dates were derived from one
kickoff instant:

| Date | Definition |
|---|---|
| `stored` | what the CSV holds today |
| `utc` | UTC calendar date of the kickoff instant (ESPN's raw `date` field) |
| `et` | kickoff converted to `America/New_York` — ESPN's US display date |
| `local` | kickoff converted to the **venue's own** zone — the official local date |

Venue zones came from ESPN's venue address: state → zone, with city overrides for the five
split-zone venues actually present (Memphis, Nashville, Murfreesboro, Bowling Green, El Paso), plus
three non-US venues — **Dublin, Ireland** (`Europe/Dublin`), **England** (`Europe/London`) and
**Puerto Rico**.

### Two traps this audit had to avoid

**(a) Placeholder kickoff times.** ESPN encodes an unannounced kickoff as **midnight US/Eastern**.
Blindly converting those into a venue zone fabricates a "23:00 kickoff on the previous day." A first
pass did exactly that and produced **180 impossible 00:00 kickoffs** and a nonsense weekday
distribution. Rows are now partitioned by ESPN's `timeValid` flag:

| Partition | n | `stored == utc` | `stored == et` | `stored == local` |
|---|:--:|:--:|:--:|:--:|
| kickoff **confirmed** | 485 | 485 | 352 | 352 |
| kickoff **unannounced** | 403 | 403 | **403** | 198 |

Only the 485 confirmed rows may be zone-converted. **The 403 unannounced rows are already correct as
stored** (`stored == et` for all 403) and **no change is proposed for any of them.**

**(b) Mapping errors.** Sanity check: after partitioning, **0 of 485** confirmed kickoffs fall
outside 10:00–23:59 local, across 31 distinct kickoff times. A materially wrong zone would show up
here immediately.

---

## 3. Quantification

| Measure | Value |
|---|:--:|
| Games in file | 888 |
| Matched to ESPN by event id | **888** |
| `stored == ESPN UTC date` | **888 / 888** |
| `stored == venue local date` | 550 / 888 |
| **Games needing correction** | **133** |
| Offset distribution (stored − local) | **`{+1 day: 133}`** — nothing else |

### The mismatches are exactly the late kickoffs

| | UTC hours observed |
|---|---|
| **Mismatched** (133) | 00 (59), 01 (23), 02 (37), 03 (12), 04 (2) — **all ≤ 04:00 UTC** |
| **Matched** (352) | 15–23 UTC only |

The two populations are **perfectly separated** with no overlap. A kickoff at or before ~04:00 UTC is
the previous evening everywhere in the United States; that is the entire mechanism.

---

## 4. Sunday games — genuine vs artifact

| | Count |
|---|:--:|
| Games **stored** on a Sunday | **70** |
| Games **actually played** on a Sunday | **3** |
| → genuine | **3** |
| → UTC rollovers, really Saturday | **67** |

### The three genuine Sunday games — all Labor Day weekend 2026

| Local date | Kickoff | Wk | Game |
|---|---|:--:|---|
| 2026-09-06 | 18:30 | 1 | Louisville @ Ole Miss |
| 2026-09-06 | 13:00 | 1 | **Washington State @ Washington** (Apple Cup) |
| 2026-09-06 | 18:30 | 1 | Wisconsin @ Notre Dame *(Lambeau Field)* |

These are real: Labor Day 2026 is **Monday, September 7**, so Sunday the 6th is a genuine television
window. Independent confirmation for the Apple Cup came from the Spokesman-Review's own "Sunday Apple
Cup" kickoff-times report. The file's lone **Monday** game — SMU @ Florida State, 2026-09-07 — is a
real Labor Day game and is also correct as stored.

### Weekday distribution — before and after

| Weekday | As stored | **True local** |
|---|:--:|:--:|
| Saturday | 720 | **751** |
| Friday | 45 | **66** |
| Thursday | 22 | 34 |
| Wednesday | 24 | 15 |
| Tuesday | 6 | 18 |
| **Sunday** | **70** | **3** |
| Monday | 1 | 1 |

The corrected distribution is what a college-football season actually looks like. The stored one —
70 Sundays including late November — is not.

---

## 5. Downstream effects

| Effect | Result |
|---|:--:|
| Games crossing the **Week 0 / Week 1 boundary** | **0** |
| Week 0 slate size, stored → corrected | **8 → 8** |
| Games changing their **week label** | **0** |
| Weeks whose corrected span overlaps the previous week | **0** |
| Ratings, spreads, edges, sides, labels | **unaffected** — dates do not enter the rating chain |
| Team/game censuses | **unaffected** — 138 / 888 / 761 / 127 / 0 BLOCK all hold |

Every correction shifts a date **within its existing week bucket**. Week spans move cleanly:

| Wk | Stored span | Corrected span | Rows moved |
|:--:|---|---|:--:|
| 0 | 2026-08-29 .. 08-30 | 2026-08-29 .. **08-29** | 1 |
| 1 | 09-03 .. 09-07 | 09-03 .. 09-07 | 23 |
| 2 | 09-11 .. 09-13 | 09-10 .. 09-12 | 11 |
| 3 | 09-17 .. 09-20 | 09-17 .. 09-19 | 13 |
| 4 | 09-24 .. 09-27 | 09-24 .. 09-26 | 6 |
| 5 | 10-02 .. 10-04 | 10-01 .. 10-03 | 7 |
| 6 | 10-07 .. 10-11 | 10-06 .. 10-10 | 6 |
| 7 | 10-13 .. 10-18 | 10-13 .. 10-17 | 7 |
| 8 | 10-20 .. 10-25 | 10-20 .. 10-24 | 5 |
| 9 | 10-27 .. 11-01 | 10-27 .. **10-31** | 5 |
| 10 | 11-04 .. 11-08 | 11-03 .. 11-07 | 15 |
| 11 | 11-11 .. 11-15 | 11-10 .. 11-14 | 13 |
| 12 | 11-18 .. 11-22 | 11-17 .. 11-21 | 14 |
| 13 | 11-24 .. 11-29 | 11-24 .. 11-28 | 7 |
| 15 | 12-12 | 12-12 | 0 |

### The Week 0 slate — the operationally important case

| Stored | → Corrected | Kickoff | Game |
|---|---|---|---|
| 2026-08-29 | 2026-08-29 | 17:00 | North Carolina @ TCU *(Dublin, Ireland)* |
| 2026-08-29 | 2026-08-29 | 16:00 | Hawai'i @ Stanford |
| 2026-08-29 | 2026-08-29 | 15:30 | NC State @ Virginia |
| 2026-08-29 | 2026-08-29 | 12:00 | San José State @ USC |
| 2026-08-29 | 2026-08-29 | 19:00 | New Mexico State @ Florida State |
| 2026-08-29 | 2026-08-29 | 16:30 | Jacksonville State @ North Dakota State |
| 2026-08-29 | 2026-08-29 | 18:30 | Sacramento State @ Eastern Michigan |
| **2026-08-30** | **2026-08-29** | **19:00** | **Memphis @ UNLV** ← the only Week 0 change |

ESPN's own record for event `401862693` is **`2026-08-30T02:00Z`** — 02:00 UTC, which is **19:00 PDT
Saturday, August 29** at Allegiant Stadium. Independent beat reporting for both Memphis and UNLV
describes an **August 29** kickoff. **The entire Week 0 slate is a single Saturday**, not a
Saturday-plus-Sunday split.

**Practical consequence:** the QB-gated Week 0 game is **one day earlier than the file says**. Any
go-live timing, line-staleness window (`SETTINGS!B13` = 5 days) or Sunday-night operational
assumption keyed to 2026-08-30 is off by a day.

---

## 6. Proposed deterministic correction rule

```
start_date := ESPN kickoff instant (UTC)
                .astimezone(ZoneInfo(venue_time_zone))
                .date()
              -- applied ONLY where competitions[0].timeValid is true

              where timeValid is false, ESPN's value is a midnight-Eastern
              placeholder: keep the stored date unchanged (it already equals
              the Eastern date for all 403 such rows)

venue_time_zone := non-US country  -> that country's zone
                   US state        -> state zone, with city overrides for
                                      Memphis, Nashville, Murfreesboro,
                                      Bowling Green and El Paso
```

**Properties:** total (all 888 resolve) · deterministic (no hour thresholds, no heuristics) ·
idempotent (re-running changes nothing) · reproduces the stored value for all 755 already-correct
rows · touches only `start_date`.

**Re-derivation note:** when kickoff times for the 403 unannounced games are published, those rows
must be re-derived under the same rule. Some will move by a day at that point — this correction is
not one-and-done for the season.

---

## 7. The exact diff

`phase12_date_audit/proposed_date_diff.csv` — **133 rows**, columns:

`id, week, away_team, home_team, venue, venue_tz, stored_start_date, proposed_start_date,
delta_days, espn_utc, local_kickoff, stored_weekday, proposed_weekday`

Every row has `delta_days = -1`. Sample:

| id | stored | → proposed | kickoff | game |
|---|---|---|---|---|
| 401862693 | 2026-08-30 | **2026-08-29** | 19:00 PDT | Memphis @ UNLV |
| 401864530 | 2026-11-01 | **2026-10-31** | 19:30 PDT | Northern Illinois @ UNLV |

---

## 8. Recommendation

The defect is **real, systematic, fully characterised and safely bounded**: it touches one column,
shifts 133 dates by exactly one day, moves no game between weeks, and changes no rating.

I recommend correcting it — **but not as part of any QB promotion.** It belongs in its own change
with its own certificate, because it edits the schedule source rather than `QB VALUES`, and because
the 403 unannounced games will need re-deriving later.

**Nothing has been changed. Awaiting your approval.**
