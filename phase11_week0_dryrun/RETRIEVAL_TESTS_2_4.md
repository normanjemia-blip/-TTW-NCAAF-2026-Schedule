# LIVE RETRIEVAL TESTS #2–#4 — UNLV, Arizona, New Mexico State

**Date:** 2026-08-15 (America/New_York)
**Library under test:** `claude/ttw-football-intelligence-lib-7zt8m0` @ `d7a9d45`
**Method:** follow the documented retrieval path (`99_Search_Index/12_QUERY_RECIPES.md` → team lookup → team file), then adversarially re-verify every checkable claim against the raw guide text in `_source/extracted/pages/`.
**No bets were derived from any of this.**

---

## Summary

| Test | Team | Verdict | New defects |
|:--:|---|---|:--:|
| #2 | **UNLV Rebels** | Retrieval accurate; **one new defect class found** | 1 |
| #3 | **Arizona Wildcats** | Clean — conflict handling exemplary | 0 |
| #4 | **New Mexico State Aggies** | Clean | 0 |

**One new defect, N-3.** It is a *visibility* defect, not a correctness one: no
fact is wrong, and both disagreeing numbers are reproduced faithfully. What is
missing is the notice that they disagree.

---

## The prefix-collision regression (F-1) — the headline result

F-1 was the worst defect from Test #1: `"GEORGIA SOUTHERN"` collided with
`"GEORGIA"` and put Adam Burke's bet on the wrong team's page. The repair
replaced substring matching with longest-prefix matching against an enumerated
bijection.

**Arizona / Arizona State and New Mexico / New Mexico State are exactly that
collision shape.** They were chosen for this round for that reason.

| Check | Result |
|---|:--:|
| Two `NEW MEXICO` best bets (Ben Stevens +265 MW, Stormy Buonantony 20-1 CFP) resolve to **New Mexico Lobos** | ✅ |
| Neither leaks onto **New Mexico State** — its best-bet table is correctly absent | ✅ |
| Guide contains **zero** Arizona / Arizona State best bets; Arizona's empty table is therefore correct, not a missing-bets defect | ✅ |

**F-1 does not regress.** The empty sections on Arizona and NMSU are *true
absences*, which is the distinction Test #1's F-4 repair was built to make.

---

## N-3 — table-vs-prose returning-starter conflicts are not detected

### What the library already does

Arizona demonstrates the existing detector working exactly as designed:

> **SOURCE CONFLICT.** The team page (p. 116) prints 12 returning starters; the
> Stability Score table (p. 42) prints 14 for the same team. The team page is
> internally consistent — offence 4 plus defence 8 equals its own total — so both
> figures are reproduced as printed and neither is corrected.

That is a **table-vs-table** comparison, and it is good work — it even reasons
about internal consistency without adjudicating.

### What it misses

The guide also states returning-starter counts **in prose**, and those are never
compared against the printed tables. A scan of all 138 teams across their own
guide pages found **five** genuine table-vs-prose disagreements:

| Team | Structured (team page) | Prose | Page | Both in the team file? |
|---|:--:|:--:|:--:|:--:|
| **UNLV** | defence **3** | "install his defense, but only **four** starters return" | 259 | ✅ both shown, unflagged |
| **Iowa** | defence **4** | "just **three** starters return" (of the stop unit) | 155 | ✅ both shown, unflagged |
| **San Diego State** | defence **5** | "only **two** starters return" (scoring-defence unit) | 275 | ✅ both shown, unflagged |
| **Indiana** | total **16**, defence **9** | "returns **10** starters (**six** on defense)" | 152 | ✅ both shown, unflagged |
| **USC** | total **17** | "with **14** starters returning" | 180 | ❌ prose figure not surfaced at all |

For the first four, a reader of the team file sees both numbers and is given no
notice they conflict. For USC the guide's alternate figure never reaches the
reader.

None of these appears in `99_Search_Index/09_SOURCE_CONFLICT_ROLLUP.md`
(**21 entries in 9 kinds**), and none appears in the affected teams' §27.

### Four cases I checked and rejected

My first scan flagged nine. **Four were my own scanner's fault**, and asserting
them would have repeated the Test #1 failure mode of reporting a tooling bug as a
library defect:

| Team | Prose | Why it is not a conflict |
|---|---|---|
| Michigan | "an offensive line that returns four starters" | **offensive-line** sub-unit, not whole-offence |
| Minnesota | "the offensive line, which returns three starters" | same |
| Nevada | "a strong offensive line … Three starters return" | same |
| Washington | "offensive line to run behind as four starters return" | same |

A sub-unit count and a unit count are different populations. Comparing them is
the error, not the guide.

### Recommended repair (not applied — the library is frozen)

Extend the existing returning-starters conflict check to also scan team-page
prose, **restricted to whole-unit statements** — excluding any sentence whose
subject is a sub-unit such as the offensive line, secondary or front seven.
Where the scan cannot tell which unit is meant, it should record the ambiguity
rather than guess a side.

**No repair was made.** The library is outside this task's scope, the branch is
frozen, and N-3 changes no fact — it changes what a reader is warned about.

---

## Test #2 — UNLV Rebels (pp. 258–259)

**Retrieval accuracy.** Every structured field reproduces the page exactly:
Dan Mullen 2nd season · `10-4 SU & 7-7 ATS, 6-8 O-U` · schedule strength
`33.36 (#97 toughest of 138)` · field ratings `3.2 / 0.9` · power rating 44.0,
#62 of 138, #1 of 10 · all 12 schedule rows with projected lines and opponent
ratings · both stat blocks with national ranks.

**Returning-production ordering — handled and disclosed.** The PDF text layer
emits the three figures in a different order than they are printed. The file says
so, out loud, and resolves by position: total 6 = offence 3 + defence 3. The same
mechanism checks out on the other two teams, where the numbers are asymmetric and
therefore diagnostic:

| Team | Raw emission order | Resolved | Internally consistent |
|---|---|---|:--:|
| Arizona | `8  4*  12` | def 8, off 4, total 12 | 4 + 8 = 12 ✅ |
| NMSU | `6  4  10` | def 6, off 4, total 10 | 4 + 6 = 10 ✅ |

The asterisk marking a returning quarterback lands on **offence** on Arizona —
the correct unit for a QB. That is strong evidence the ordering logic is right
rather than coincidentally right.

**Conflict preservation — strong.** UNLV's §27 records three win-total conflicts,
including the one that matters most: the feature (pp. 22–27) bets **Over 7.5**
while the team page bets **Under 8.5**. Opposite sides, same team, both preserved,
neither reconciled.

**Source discipline — strong.** GUIDE CONTENT and TTW DERIVED are separated
throughout; the bull/bear sections declare the selection as PERSONAL INFERENCE and
state how many statements were withheld as two-sided (4 each) rather than forcing
them onto a side — the F-2 repair visibly working.

---

## Test #3 — Arizona Wildcats (pp. 116–117)

Verified against p. 116: Brent Brennan 3rd season · `9-4 SU & 8-5 ATS, 4-9 O-U` ·
schedule strength `44.57 (#46 toughest of 138)` · field ratings `2.7 / 0.5` ·
power rating 52.5, #29 of 138, #5 of 16 · DraftKings win total 7.5.

Conflict handling is the best example in the three tests — see N-3 above. **No
defects.**

---

## Test #4 — New Mexico State Aggies (pp. 202–203)

Verified against p. 202: Tony Sanchez 3rd season · `4-8 SU & 6-6 ATS, 5-7 O-U` ·
schedule strength `29.65 (#126 toughest of 138)` · field ratings `3.9 / 0` ·
power rating 25.0, #126 of 138, #7 of 10 · win total 4.5 · returning production
10 / 4 / 6, agreeing with the Stability Score table at 10, so **correctly no
conflict recorded**.

**No defects.**

---

## Evaluation against the five criteria

| Criterion | Finding |
|---|---|
| **Retrieval accuracy** | Every structured field on all three teams reproduces the printed page. No fabricated value found. |
| **Source discipline** | Consistently strong. Guide content, TTW-derived navigation and personal inference are labelled and never merged. Page citations are specific and correct. |
| **Conflict preservation** | Strong where detected — opposite-side win-total bets preserved unreconciled, table-vs-table returning-starter conflicts recorded with reasoning. **N-3 is the gap: prose-vs-table numeric conflicts are not scanned for.** |
| **Search architecture** | The documented path works. Team lookup → team file resolved in one hop for all three; cross-links to coaching, QB, futures, win-total and conference files all valid. `validate_search.py` confirms **10,012** relative links resolve, 0 broken. |
| **Usefulness for football analysis** | High. The team file answers real questions without a second lookup, and — more valuable — it is explicit about what the guide does *not* say. UNLV's §12 "Not addressed in guide under this heading" is worth more than a filled-in guess. |

---

## Note on the fc0b247 link count

fc0b247 claimed *"9,918 links, 0 broken."* At current HEAD `d7a9d45` the count is
**10,012**, still 0 broken. That is not drift — `d7a9d45` added cross-database
conflict visibility to §27, which added links. Both figures are correct for their
commit.
