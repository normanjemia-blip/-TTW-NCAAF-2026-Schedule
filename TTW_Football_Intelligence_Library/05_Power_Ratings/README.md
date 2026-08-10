<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_power.py
     Source:   2026 VSiN College Football Betting Guide;
               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->

# 05 Power Ratings

Steve Makinen's 2026 power ratings in full, the methodology he states for them, and a structured comparison against the TTW College Football Power Ratings Workbook v0.8.1 AUTHORITATIVE.

> **The v0.8.1 AUTHORITATIVE workbook is frozen and was opened read-only.** Nothing in Phase 6 writes to it, recalculates it or proposes a change to it.

## Files

| File | Class | Content |
| --- | --- | --- |
| [00_MAKINEN_METHODOLOGY.md](00_MAKINEN_METHODOLOGY.md) | GUIDE | what Makinen says goes into the number, and what he does not say |
| [00_MAKINEN_RATINGS.md](00_MAKINEN_RATINGS.md) | GUIDE | all 138 ratings with field ratings, both printings reconciled |
| [00_LINE_MODEL_VERIFICATION.md](00_LINE_MODEL_VERIFICATION.md) | DERIVED | proof that one rating point equals one point of spread |
| [00_SCALE_RECONCILIATION.md](00_SCALE_RECONCILIATION.md) | DERIVED | how the two scales are made comparable, and what the workbook's prior actually contains |
| [00_TTW_VS_MAKINEN.md](00_TTW_VS_MAKINEN.md) | DERIVED | the 138-team comparison |
| [00_DISAGREEMENT_INDEX.md](00_DISAGREEMENT_INDEX.md) | DERIVED | where the two differ most |
| [00_HOME_FIELD_COMPARISON.md](00_HOME_FIELD_COMPARISON.md) | DERIVED | Makinen's per-team field ratings against the workbook's flat HFA |
| [00_VSIN_IMPORT_CANDIDATE.md](00_VSIN_IMPORT_CANDIDATE.md) | PREPARED | the import set for the workbook's empty VSiN column — not applied |
| [00_WORKBOOK_PROVENANCE.md](00_WORKBOOK_PROVENANCE.md) | PROVENANCE | what was read, its hash, and what could not be read |
| [00_SOURCE_CONFLICTS.md](00_SOURCE_CONFLICTS.md) | GUIDE | the two printings, reconciled |

## Headline findings

- The guide prints all 138 ratings twice and **all 138 agree**.
- One Makinen rating point is one point of projected spread, verified by reconstructing **1528 of 1530** printed game lines (99.87%). The two scales therefore need translation, not rescaling.
- Correlation between Makinen and the workbook's preseason prior: **0.9956**; mean absolute difference **0.94 points**.
- The workbook holds **no cached formula results**, so no TTW rating could be read; every TTW figure here is derived from its printed formulas and labelled as such.
- Two of the workbook's five preseason source columns are empty, including the VSiN column the guide would fill. The comparison is therefore against a renormalised third-party consensus.

## Rebuild

```bash
python3 _tools/extract_power.py       # p.47 table + cross-check
python3 _tools/extract_workbook.py <workbook.xlsx>   # read-only
python3 _tools/build_power.py
python3 _tools/validate_power.py
```

## Cross-links

- [Team Database](../02_Team_Database/README.md)
- [Coaching Database](../03_Coaching_Database/README.md)
- [Master Index — Power Rating Index](../00_Master_Index/09_Power_Rating_Index.md)
