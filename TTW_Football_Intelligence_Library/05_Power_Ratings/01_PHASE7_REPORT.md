<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_report.py
     Source:   2026 VSiN College Football Betting Guide;
               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->

# Phase 7 — VSiN Preseason Calibration: Owner Report

> **Source classes.** GUIDE CONTENT: Makinen's ratings (p. 47). WORKBOOK READ: v0.8.1 stored inputs, SETTINGS, schedule, alias table. TTW DERIVED: every statistic in this report. The classes are labelled throughout and never merged.

> **v0.8.1 AUTHORITATIVE is unchanged.** No weight, SETTING, formula, VSiN cell or version was written. Confirmed by hash against the recorded blob: `e2da9a4c28bd5c0f094ab06a2a85d3e3…`

## Headline

**RECOMMENDATION: INSUFFICIENT EVIDENCE — RETEST AFTER MORE DATA.**

Not because the analysis was inconclusive, but because the analysis that would settle it cannot be run yet: no season in this project pairs a VSiN preseason rating with played games. What could be established without results has been, and it points the same way — the decision is unusually low-stakes in either direction.

---

## 1. Calibration and backtest methodology

The intended design is a paired, pre-registered, out-of-sample comparison of two fixed configurations over a full season of games, specified in full in [01_CALIBRATION_PROTOCOL.md](01_CALIBRATION_PROTOCOL.md) and implemented in `_tools/score_calibration.py`. Neither configuration estimates any parameter from the test season, so every game is out-of-sample for both and the walk-forward property comes from the parameters being frozen rather than from splitting a sample.

**It has not been executed, because there is nothing to execute it on.** The scorer refuses to run below 200 completed games and currently exits with that refusal.

## 2. Data inventory

| Dataset | Location | Content | Usable for calibration |
| --- | --- | --- | --- |
| Makinen 2026 preseason ratings | guide p. 47 + 138 team pages | 138 ratings, both printings reconciled | as an **input**, not as history |
| Workbook PRESEASON inputs | v0.8.1, read-only | SP+, FPI, TeamRankings raw + dates + citations | as an **input** |
| Workbook SETTINGS | v0.8.1, read-only | all weights, thresholds, fade table | as **method** |
| Workbook IMPORT SCHEDULE | v0.8.1, read-only | 888 games, season 2026, **0 completed, no scores** | as a **schedule**, not as results |
| Workbook HISTORY | v0.8.1, read-only | **empty — headers only** | no |
| Workbook BACKTEST | v0.8.1, read-only | **empty — headers only** | no |
| Workbook MARKET LINES | v0.8.1, read-only | **0 lines entered** | no |
| Workbook IMPORT STATS | v0.8.1, read-only | **0 team rows** | no |
| Workbook QB VALUES | v0.8.1, read-only | **0 rows** | no |
| `raw_espn/` scoreboard scrape | verification branch | 2026 schedule only, retrieved 2026-07-19, **no pre-2026 requests in the retrieval log** | no |
| Guide 2025 team records | team pages | `su_2025`, `ats_2025`, `ou_2025` season **aggregates** | no — no matching 2025 preseason VSiN ratings exist |

### What is missing, stated plainly

A calibration of "does adding VSiN improve the preseason blend" requires, for at least one season: a VSiN **preseason** rating, the other sources' preseason ratings, and the games that followed. **This project holds zero such seasons.** Only the 2026 VSiN guide is present, and the 2026 season has not begun.

No proxy was constructed. Testing 2026 preseason ratings against 2025 outcomes would be backwards; testing Makinen's ratings against the 2025 aggregates the guide prints would compare a projection with a season it did not project; and both would be presented as evidence when they are not.

## 3. Sample sizes

| | N |
| --- | --- |
| Seasons with VSiN preseason ratings **and** results | **0** |
| Teams with a 2026 VSiN rating | 138 |
| 2026 scheduled games in the workbook | 888 |
| 2026 games completed as of this build | **0** |
| FBS-vs-FBS games matched for future scoring | 761 |
| Of those, weeks 0–4 | 215 |
| Labels not matched (FCS opponents, correctly excluded) | 100 |

## 4. Baseline results

BASELINE is the configuration in the frozen workbook today: VSiN blank, the three populated sources renormalised by the workbook's own rule.

| Source | Configured weight | Effective weight |
| --- | --- | --- |
| SP+ | 0.3 | **0.4286** |
| FPI | 0.25 | **0.3571** |
| TeamRankings | 0.15 | **0.2143** |
| VSiN | 0.10 (reserved) | — (column blank) |

Distribution standard deviation: **12.533 points**.

No predictive baseline error can be reported. There are no results to score against.

## 5. VSiN-included results

| Source | Effective weight |
| --- | --- |
| SP+ | **0.3750** |
| FPI | **0.3125** |
| TeamRankings | **0.1875** |
| VSiN | **0.1250** |

Distribution standard deviation: **12.519 points** — against 12.533 for baseline.

Effect on the prior:

| Measure | Points |
| --- | --- |
| Mean absolute change per team | **0.117** |
| Median absolute change | 0.104 |
| Largest change for any team | 0.414 |
| Teams moving 1.0 point or more | **0 of 138** |
| Teams whose rank is unchanged | 100 of 138 |
| Largest rank move | 3 places |

Again: **no predictive result**, because there is nothing to predict against yet. These are structural effects only.

## 6. Diagnostic alternative-weight experiments

Run as sensitivity analysis, not as a search for a good weight. None is proposed for production and none was chosen by minimising anything — there is no error surface to minimise on.

| VSiN weight | Effective | Mean abs Δ | Max abs Δ | Teams ≥1 pt | Max rank move |
| --- | --- | --- | --- | --- | --- |
| 0.05 | 0.0667 | 0.062 | 0.221 | 0 | 2 |
| 0.1 | 0.1250 | 0.117 | 0.414 | 0 | 3 |
| 0.15 | 0.1765 | 0.165 | 0.585 | 0 | 4 |
| 0.2 | 0.2222 | 0.208 | 0.737 | 0 | 5 |
| 0.3 | 0.3000 | 0.281 | 0.994 | 0 | 5 |

Even at triple the reserved weight the average team moves less than half a point. Full detail in [01_VSIN_DIAGNOSTICS.md](01_VSIN_DIAGNOSTICS.md).

## 7. Prediction-error comparison

**Not available.** No games have been played. The comparison is specified and implemented; it awaits data.

## 8. Market/spread-error comparison

**Not available, and doubly so.** No results exist, and the workbook's MARKET LINES sheet holds **0 entered lines**. Under the protocol, line agreement would in any case be descriptive context and never a success criterion.

## 9. Betting-performance comparison

**Not legitimately testable.** No results, no stored lines, and the workbook's BET labels are switched off by default in SETTINGS with edges of 3.0+ held at INVESTIGATE. An ATS figure produced today would be fabricated.

## 10. Walk-forward / out-of-sample results

**None yet.** The design is genuinely out-of-sample by construction — no parameter is fitted to the test season — so when 2026 completes, the whole season is a clean holdout for both configurations. That property is preserved by registering the test before the data exists, which is what this phase did.

## 11. Sensitivity analysis

Two were possible without results and both were run:

- **Weight sensitivity** (§6): the response is close to linear and small throughout.
- **Information sensitivity**: how much of Makinen is already inside the live consensus.

| | Value |
| --- | --- |
| R² of VSiN on SP+, FPI and TeamRankings | **0.9930** |
| Residual standard deviation | **1.040 points** |
| Baseline distribution SD, for scale | 12.533 points |

**99.3% of the variance in Makinen's ratings is already carried by the three sources the workbook blends today.** The independent remainder is about 1.04 points of standard deviation. That is not nothing — it is where his genuine disagreement lives — but it enters the blend at an effective weight of 0.125, which is why the prior barely moves.

## 12. Overfitting: evidence and safeguards

The strongest safeguard available is that **no fitting occurred**. Nothing in this phase was estimated from outcome data, because there is no outcome data. Beyond that:

- Both configurations were fixed from the workbook's own stored weights, not selected.
- The weight sweep is reported in full, including the values that look least favourable, and no value is recommended.
- The scoring rule is registered in code before any result exists and hashes into the repository history.
- The scorer refuses partial seasons, which removes the temptation to peek and stop at a favourable point.
- The protocol states a single scoring run and a fixed segment breakdown declared in advance.

## 13. Material limitations

1. **No historical data pairs VSiN preseason ratings with results.** This is the binding limitation and no analysis overcomes it.
2. **The workbook stores no cached formula values**, so every TTW figure is a reimplementation of its printed formulas, labelled TTW DERIVED. Carried forward from Phase 6.
3. **Two of five preseason sources are empty** — the TTW independent 2025 prior as well as VSiN — so BASELINE is a third-party consensus rather than a distinctively TTW view.
4. **The effect under test is tiny by construction.** The largest MAE improvement arithmetically possible is 0.156 points.
5. **One season will remain one season.** Even a clean 2026 result is a single sample of a noisy process.
6. **No market lines are stored**, so the betting-usefulness question cannot be approached even once results exist, unless lines are captured going forward.

## 14. Source and data conflicts encountered

None new. Everything already recorded stands and none was adjudicated:

- The Cincinnati / Miami (Ohio) neutral-site line anomaly (Phase 6) — preserved, still unexplained by either neutral form.
- 16 coaching conflicts (Phase 5) — untouched.
- The Navy tenure discrepancy (Phase 2) — untouched.

## 15. Demonstrated defects discovered in prior artefacts

**None.** Phase 6's extraction, the canonical maps and the workbook read all reproduced exactly. One item worth recording that is a gap rather than a defect: the workbook's BACKTEST sheet declares a plan — *construction/calibration on pre-2025 seasons, 2025 preserved as out-of-sample holdout* — that was never executed and for which no data was ever loaded. That plan is the one this phase would have inherited.

## 16. Recommendation on whether VSiN should enter the blend

**INSUFFICIENT EVIDENCE — RETEST AFTER MORE DATA.**

The question as posed — does it improve out-of-sample prediction — has no admissible answer today. What can be said is that the decision is low-stakes in both directions: 99.3% of Makinen is already in the blend, and adding the rest at its reserved weight moves the average team 0.12 points and no team by a full point. There is no urgency to include it and no cost to waiting for the evidence.

## 17. Recommended VSiN weight

**None.** Recommending a weight would require evidence this phase does not have. If the owner later approves inclusion on other grounds — source diversity, or a judgement that Makinen's independent component is worth carrying — the workbook's own reserved 0.10 is the only defensible starting value, because it was chosen by the workbook's designer before any of this analysis existed and is therefore not fitted to it.

## 18. Confidence level

| Claim | Confidence |
| --- | --- |
| No admissible historical data exists for this test | **High** — verified directly against every candidate dataset |
| Adding VSiN at 0.10 changes the prior negligibly | **High** — arithmetic over the frozen inputs |
| Makinen is ~99% explained by the live sources | **High** — regression over all 138 |
| Whether inclusion improves prediction | **None — untested** |

## 19. Exact production changes required, if later approved

Recorded so that approval could be executed precisely, and **not executed here**:

1. Paste `_source/data/vsin_preseason_import.csv` `vsin_raw` into `PRESEASON!U6:U143`, matched on `abbrev`.
2. Paste `vsin_date` into `PRESEASON!V6:V143` and `vsin_cite` into `PRESEASON!W6:W143`.
3. Leave `PRESEASON!X` (VSiN norm) alone — it is a formula and will populate itself.
4. Change **no** SETTINGS value: the 0.10 weight is already there and the renormalisation is automatic.
5. Log the change in `CHANGELOG` with version, date, reason and authority, per the sheet's own rule that there be no silent tuning.
6. Promote as a new version with a fresh hash; v0.8.1 remains the frozen artefact it is today.

Note that step 1 alone changes the effective weights of all three existing sources, from SP+ 0.4286, FPI 0.3571, TeamRankings 0.2143 to SP+ 0.3750, FPI 0.3125, TeamRankings 0.1875. That is the workbook behaving as designed, and it should be an intended consequence rather than a surprise.

## 20. Validation results

See `_tools/validate_phase7.py`. Gates cover: the frozen hash; the absence of any workbook write; the canonical join; reproducibility of both configurations; the registration order of the protocol; the scorer's refusal on an unplayed season; source-class labelling; and the honesty gate that no predictive claim appears anywhere in the phase.

## 21. Confirmation on v0.8.1 AUTHORITATIVE

**Unchanged.** SHA-256 `e2da9a4c28bd5c0f094ab06a2a85d3e31b37c2aba894f97f3415e15f799cdfd6`, byte-identical to the git blob `06d817cdaa2814aa71630c5637d90af978c17b98` recorded in Phase 6 and to the `source_sha256` in the verification project's own `PROJECT_MANIFEST.json`. No write, no recalculation, no promotion, no new version.

## Cross-links

- [Diagnostics](01_VSIN_DIAGNOSTICS.md) · [pre-registered protocol](01_CALIBRATION_PROTOCOL.md) · [import candidate](00_VSIN_IMPORT_CANDIDATE.md) · [workbook provenance](00_WORKBOOK_PROVENANCE.md)
