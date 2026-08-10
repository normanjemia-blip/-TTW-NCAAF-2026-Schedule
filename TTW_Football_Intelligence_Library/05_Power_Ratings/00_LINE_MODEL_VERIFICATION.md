<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_power.py
     Source:   2026 VSiN College Football Betting Guide;
               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->

# Line-Model Verification — what one Makinen point is worth

> **Source class: TTW DERIVED.** The arithmetic below is this library's, performed over numbers printed in the guide and read from the workbook. It is not VSiN's claim and not a workbook output.

The Master Index deferred one question to this phase: whether Makinen's ratings can be compared with the TTW workbook's ratings at all, given that the two run on different scales — his from 16 to 71, the workbook's centred on zero as points better or worse than an average FBS team on a neutral field.

That question is answerable from the guide's own numbers rather than by assumption. Every team page prints a projected line for every game, and every team page prints home and road field ratings. If the printed lines are reconstructible from the printed ratings, the unit is fixed by arithmetic.

## The model tested

```
home / away:   line = (home rating + home team's HOME field rating)
                    − (away rating + away team's ROAD field rating)

neutral site:  line = (team A rating + A's ROAD field rating)
                    − (team B rating + B's ROAD field rating)
```

The neutral-site form is worth stating separately, because it is not a bare difference of ratings. Makinen puts **both** teams on their road field ratings for almost every neutral game, which matches the off-campus reality of most of them. Two pairings fit the bare rating difference instead. Both forms were tried and the outcome is reported rather than smoothed over by a wider tolerance.

## Result

| Games checked | Reconstructed to within 0.05 pts | Rate |
| --- | --- | --- |
| 1530 | 1528 | **99.87%** |

Of those, 24 are neutral-site games, tested against the neutral form above.

### The 2 that do not reconstruct

| Team | Opponent | Site | Printed | Model |
| --- | --- | --- | --- | --- |
| [Cincinnati Bearcats](../02_Team_Database/cincinnati_bearcats.md) | [Miami (Ohio) RedHawks](../02_Team_Database/miami_ohio_redhawks.md) | neutral | -8.8 | +8.5 |
| [Miami (Ohio) RedHawks](../02_Team_Database/miami_ohio_redhawks.md) | [Cincinnati Bearcats](../02_Team_Database/cincinnati_bearcats.md) | neutral | +8.8 | -8.5 |

These are mirror rows of the same fixture and they agree with each other, so this is one disagreement rather than several. It fits neither neutral form, by 0.3 points. It is recorded in [source conflicts](00_SOURCE_CONFLICTS.md) and left uncorrected; the full list lives in `_source/data/line_model_check.json`.

100 opponent labels did not resolve to one of the 138 and were skipped rather than guessed at. They are FCS opponents, which Makinen rates but which have no field ratings and no team page.

## What follows from it

**One Makinen power-rating point is one point of projected point spread.** That is the same unit the workbook uses. The two rating sets are therefore directly comparable after mean-centering alone, and any remaining difference in spread between the two distributions is a difference of football opinion about game margins — not an artefact of scale.

This matters for what Phase 6 is allowed to do. A z-score or standard-deviation rescale would have been a *reinterpretation* of Makinen's numbers; mean-centering is a *translation* of them. Only the translation is performed anywhere in this phase.

> The guide never states this relationship. It is demonstrated here from printed figures, and is labelled TTW DERIVED wherever it is relied upon.

## Cross-links

- [Scale reconciliation](00_SCALE_RECONCILIATION.md) · [TTW comparison](00_TTW_VS_MAKINEN.md)
