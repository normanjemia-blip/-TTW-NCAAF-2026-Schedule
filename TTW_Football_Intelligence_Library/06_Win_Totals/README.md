<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_wintotals.py
     Source:   2026 VSiN College Football Betting Guide -->

# 06 Win Totals

> **Source class: GUIDE CONTENT.** Every number and argument is printed in the 2026 VSiN College Football Betting Guide. TTW reference notes paraphrase the reasoning; the judgement is the guide's. No outside research, no post-publication updates.

Every win-total number, recommendation and projected-win figure in the guide, with the reasoning attached and the guide's three separate statements of each kept apart.

## Files

| File | Content |
| --- | --- |
| [00_FEATURE_PICKS.md](00_FEATURE_PICKS.md) | Makinen's 29 bets, pp. 22–27 |
| [00_ALL_TEAMS.md](00_ALL_TEAMS.md) | all 138 teams, three layers side by side |
| [00_OVER_INDEX.md](00_OVER_INDEX.md) | the 14 Overs |
| [00_UNDER_INDEX.md](00_UNDER_INDEX.md) | the 15 Unders |
| [00_DEPENDENCY_INDEX.md](00_DEPENDENCY_INDEX.md) | what each recommendation rests on |
| [00_AGREEMENT_INDEX.md](00_AGREEMENT_INDEX.md) | multiple signals agree |
| [00_DISAGREEMENT_INDEX.md](00_DISAGREEMENT_INDEX.md) | internal disagreement, preserved |
| [00_WINTOTAL_VS_POWER.md](00_WINTOTAL_VS_POWER.md) | TTW DERIVED consistency check |
| [00_SOURCE_CONFLICTS.md](00_SOURCE_CONFLICTS.md) | conflicts and one artefact defect |
| *team files* | 29 records, 26 fields each |

## The three layers

| Layer | Coverage | Author |
| --- | --- | --- |
| Conference table — total, rating, schedule strength, projected record | 138 | conference preview author |
| Team page — standalone Over/Under line | 138 | team page |
| Feature pp. 22–27 — the bets, with arguments | 29 | Steve Makinen |

No Over or Under **price** is printed anywhere in the guide's win-total material, so fields 4 and 5 of every record read `Not addressed in guide.` That is a property of the source, not a gap in this phase.

## Rebuild

```bash
python3 _tools/extract_wintotals.py
python3 _tools/build_wintotals.py
python3 _tools/validate_wintotals.py
```
