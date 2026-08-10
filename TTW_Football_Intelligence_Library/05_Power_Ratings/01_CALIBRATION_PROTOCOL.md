<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_protocol.py <workbook.xlsx>
     Source:   TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->

# Pre-Registered Calibration Protocol — VSiN in the preseason blend

> **Source class: TTW DERIVED.** Arithmetic over the workbook's stored schedule and preseason inputs. Not a workbook output.

> **v0.8.1 AUTHORITATIVE remains frozen.** This protocol reads it and changes nothing in it. Executing the protocol later will also change nothing in it.

> **Registered before any 2026 result exists.** As of the build date, 0 of 888 games in the workbook's 2026 schedule are complete. The comparison below is fixed now precisely so that it cannot later be shaped by the answer it produces.

## What is being tested

Two configurations, both fixed in advance, neither fitted to any 2026 data:

| | BASELINE | VSIN-INCLUDED |
| --- | --- | --- |
| Sources | SP+, FPI, TeamRankings | SP+, FPI, TeamRankings, VSiN |
| VSiN weight | — | 0.10, the workbook's own reserved value |
| Renormalisation | workbook rule, missing is never zero | same |
| Parameters estimated from 2026 | **none** | **none** |

Because neither configuration estimates anything from 2026, every 2026 game is out-of-sample for both. That is what makes a single-season test legitimate here — the walk-forward property comes from the parameters being frozen, not from splitting the sample.

## The decision point, and how look-ahead is prevented

- The prediction for a game is formed from the **preseason prior only**, faded by the workbook's own effective-games rule, using information available before kickoff.
- No closing line, no in-season rating, no result, and no post-game information may enter the prediction. The scorer refuses to read the result column until after the prediction column is written.
- Market lines are recorded at the stated line date and are used as a **benchmark**, never as an input.
- Games are scored in schedule order. Nothing is re-scored after later weeks are seen.

## Metrics

| Rank | Metric | Role |
| --- | --- | --- |
| Primary | Mean absolute error of predicted margin against actual margin | decides the question |
| Primary | Root mean squared error of the same | penalises the large misses MAE hides |
| Secondary | Paired per-game difference in absolute error, with a 95% interval | the only form in which a small effect is legible |
| Descriptive | Error against the closing spread | context only — **never a success criterion** |
| Descriptive | ATS record at the workbook's own edge thresholds, with interval | reported, **never sufficient on its own** |
| Diagnostic | Error by week bucket, by edge bucket, by favourite size | where any difference lives |

Success is defined as a **reduction in out-of-sample prediction error against actual results**, significant at the stated interval and stable across week buckets. Agreement with closing lines, with another rating system, or with the current consensus is explicitly not success.

## How large is the effect that could possibly be detected

This is the part worth reading before committing a season to the question. The difference between the two configurations' predictions for a single game is the whole effect under test:

| | Points |
| --- | --- |
| Games matched (FBS vs FBS, 2026) | 761 |
| Standard deviation of the per-game prediction difference | **0.198** |
| Root mean square of the same | 0.198 |
| Mean absolute prediction difference | 0.156 |
| Largest prediction difference in the season | 0.665 |
| Games where the two configurations differ by 0.5 pts or more | 14 |
| Games where they differ by a full point or more | 0 |

### What the paired design can and cannot resolve

The scored quantity per game is the difference in absolute error between the two configurations. Because both predictions sit within a fraction of a point of each other, the large shared margin error cancels almost exactly, and the comparison is far better powered than setting two MAE figures side by side would suggest.

| | Points of MAE |
| --- | --- |
| Largest improvement arithmetically possible | **0.156** |
| Minimum detectable effect, full season (761 games) | 0.014 |
| Minimum detectable effect, weeks 0–4 (215 games) | 0.026 |

| True improvement in MAE | Games needed (two-sided, 95%) |
| --- | --- |
| 0.02 pts | 377 |
| 0.05 pts | 61 |
| 0.10 pts | 16 |
| 0.15 pts | 7 |

The upper bound is the number that matters. Even if **every** VSiN adjustment moved its prediction in the right direction — which no rating source achieves — the improvement would be 0.16 points of mean absolute error, against margin errors that routinely run to double figures. A realistic share of that upper bound is smaller again.

So the honest statement is not that the season is underpowered. It is that the season is **well powered to measure an effect that is very small by construction**. A statistically detectable result here would still be a practically negligible one, and the report must say both things rather than one.

**This is a limitation stated before the test, not after it.** If the 2026 result comes back indistinguishable, that is the expected outcome rather than a disappointment, and it must not be met by widening the search until something reaches significance.

## Stopping rules

- The comparison is run **once**, at season end, on the full matched sample, plus the pre-declared week-bucket breakdown.
- No mid-season peeking is used to decide whether to continue.
- The alternative-weight sweep stays diagnostic. It is never used to select a production weight, and it is not re-run against the holdout to find a winner.
- If BASELINE and VSIN-INCLUDED are statistically or practically indistinguishable, the recorded result is **no evidence of improvement**. That outcome is acceptable and final for the season.

## What executing this protocol may change

Nothing, by itself. The scorer writes a report. Any production change remains an owner decision taken separately, on the evidence the report contains.

## Cross-links

- [Diagnostics](01_VSIN_DIAGNOSTICS.md) · [Phase 7 report](01_PHASE7_REPORT.md) · [import candidate](00_VSIN_IMPORT_CANDIDATE.md)
