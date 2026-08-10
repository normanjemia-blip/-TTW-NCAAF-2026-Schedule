<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_futures.py
     Source:   2026 VSiN College Football Betting Guide -->

# 07 Futures

> **Source class: GUIDE CONTENT.** Every price, pick, prediction and contributor name below is printed in the 2026 VSiN College Football Betting Guide. TTW reference notes paraphrase each argument; the judgement is the contributor's. No outside research, no post-publication updates.

Every futures market, price and recommendation the guide prints, with each position attributed to the person who holds it.

## The four layers

| Layer | Source | Coverage | What it gives you |
| --- | --- | --- | --- |
| Season predictions | p. 4 | 17 categories × 22 contributors = **374** picks | a name in a box — no price, no reasoning |
| Best bets | pp. 5–15 | **62** picks by 20 contributors | priced recommendations with an argument |
| Heisman | p. 39 | **4** picks by Zach Cohen | priced player futures |
| Team prices | 138 right-hand pages | **414** markets, 412 printed prices | the board for every team |

## Files

| File | Content |
| --- | --- |
| [00_PREDICTIONS.md](00_PREDICTIONS.md) | the attributed p. 4 grid |
| [00_CONSENSUS.md](00_CONSENSUS.md) | **TTW DERIVED** counts — agreement and splits |
| [00_BEST_BETS.md](00_BEST_BETS.md) | all priced host picks |
| [00_BY_CONTRIBUTOR.md](00_BY_CONTRIBUTOR.md) | one page per person |
| [00_HEISMAN.md](00_HEISMAN.md) | p. 39 |
| [00_TEAM_FUTURES.md](00_TEAM_FUTURES.md) | all 138 boards |
| [00_WINTOTAL_OVERLAP.md](00_WINTOTAL_OVERLAP.md) | overlap with Phase 7 |
| [00_DISAGREEMENT.md](00_DISAGREEMENT.md) | disagreement, preserved |
| [00_SOURCE_CONFLICTS.md](00_SOURCE_CONFLICTS.md) | conflicts and anomalies |

## What this database does not do

It does not convert a price into an implied probability, remove vig, rank contributors by past accuracy, or derive a house position from a staff vote. The consensus counts are arithmetic over printed cells and are labelled TTW DERIVED wherever they appear. Where the guide contradicts itself — or where one person answers two questions differently — both answers are printed and neither is resolved.

## Rebuild

```bash
python3 _tools/extract_futures.py
python3 _tools/build_futures.py
python3 _tools/validate_futures.py
```
