# Operating the frozen library for matchup analysis

**Status: FROZEN AND OPERATIONAL.** Library development is finished. This
file describes how to *read* the library for betting and matchup work. It
adds no football content and changes nothing in the library.

---

## What the library is for

The TTW Football Intelligence Library is a **frozen reference source** for
college-football betting and matchup analysis. It records the 2026 VSiN
College Football Betting Guide as published, plus the deliberately
separated post-publication quarterback verification layer.

It is **not** for team-preview shows, podcast scripts, season-preview
content, episode production, automatic picks, or automatic power-rating
changes.

Its job is to supply structured preseason context that is later reconciled
with four live things it does not contain:

1. the TTW College Football Power Ratings Workbook, v0.8.1 PRODUCTION MASTER;
2. verified current quarterback, injury, roster and depth-chart information;
3. current betting lines and market movement;
4. matchup-specific statistical analysis.

---

## The matchup-reference packet

```bash
cd TTW_Football_Intelligence_Library
python3 _tools/matchup.py "UNLV Rebels" "North Dakota State Bison"
python3 _tools/matchup.py "UNLV Rebels" "Hawaii Rainbow Warriors" -o _packets/wk0.md
```

Both arguments must be the **exact canonical team name**. A partial name is
refused with the candidate list rather than resolved by guesswork —
`"North Dakota"`, `"Miami"` and `"Ohio"` are all rejected, because
resolving them would be the substring join the library spent eleven phases
eliminating. `python3 _tools/matchup.py --help` prints usage.

The packet contains, for both teams: canonical identity and conference;
source-specific preseason expectations; head coach, coordinators and the
printed Stability Score; offensive and defensive identity; returning
production, strengths and weaknesses; the frozen preseason quarterback
outlook, labelled non-current; win totals and futures; bull and bear cases;
historical and situational trends; explicit numerical and narrative source
conflicts; `Not addressed in guide.` wherever the guide is silent; page
references and provenance; and a closing list of betting-relevant questions
that require current verification.

Every line is reproduced from an approved library file and cited back to
it. The packet introduces no football content of its own — a validator
gate proves it, line by line, against the library corpus.

### What the packet will not do

It does not recommend a wager, compute an edge from stale guide numbers,
build a depth chart, treat a preseason quarterback expectation as verified
current status, silently resolve a conflict, import anything into v0.8.1,
alter TEAM RATINGS / QB VALUES / ADJUSTMENTS / MARKET LINES / BET status,
or overwrite any part of the frozen library. `_tools/validate_matchup.py`
gates each of those prohibitions.

---

## The live betting workflow, and the boundary it must not cross

The packet is **step 1 of 7**. It is not an analysis and must never be the
last thing read before a bet.

1. **Retrieve** the frozen matchup-reference packet.
2. **Read** the current matchup numbers from the v0.8.1 workbook.
3. **Verify independently** current quarterback status, injuries, depth
   charts, roster changes, weather and venue.
4. **Obtain** current market spreads, totals and movement.
5. **Reconcile** the agreements and conflicts between those four.
6. **Only then** conduct betting analysis.
7. Any proposed workbook adjustment follows the **existing approval and
   audit process**.

> **The boundary.** Current information may read and cite the frozen
> library. It may never be written back into it, and it may never
> overwrite it. The library states what the guide said at publication;
> that record does not change because the season did.

The workbook is likewise out of scope for anything in this repository. No
spreadsheet file is tracked here, and no tool in `_tools/` opens one.

---

## Assurance

```bash
for v in _tools/validate_*.py; do PYTHONPATH=_tools python3 "$v" || break; done
```

11 harnesses, 142 gates. Any failure exits non-zero.

| Harness | Gates | Covers |
| --- | --- | --- |
| `validate_teams.py` | 13 | team schema, canonical joins, §27 conflict propagation |
| `validate_matchup.py` | 22 | the retrieval workflow's prohibitions |
| `validate_search.py` | 16 | repository-wide links, entity registry, gap register |
| `validate_qb.py` | 14 | two-layer separation, cross-reference completeness |
| `validate_concepts.py` `validate_futures.py` `validate_trends.py` | 12 each | Phases 9, 8, 10 |
| `validate_wintotals.py` | 11 | Phase 7 |
| `validate_coaching.py` `validate_phase7.py` `validate_power.py` | 10 each | Phases 5, 7-calibration, 6 |
