<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_power.py
     Source:   2026 VSiN College Football Betting Guide;
               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->

# Scale Reconciliation — Makinen against the workbook

> **Source class: TTW DERIVED.** The arithmetic below is this library's, performed over numbers printed in the guide and read from the workbook. It is not VSiN's claim and not a workbook output.

> **The v0.8.1 AUTHORITATIVE workbook is frozen and was opened read-only.** Nothing in Phase 6 writes to it, recalculates it or proposes a change to it.

## The two scales

| | Makinen | TTW workbook prior |
| --- | --- | --- |
| Definition | absolute rating, 1 pt = 1 pt of spread ([verified](00_LINE_MODEL_VERIFICATION.md)) | points better/worse than average FBS on a neutral field |
| Mean | 42.00 | 0.00 |
| Standard deviation | 12.46 | 12.53 |
| Range | 16 to 71 | -25.9 to 31.0 |

## The translation used everywhere in this phase

```
Makinen (centred) = printed rating − 41.9964
```

No rescaling is applied. See the line-model verification for why rescaling would be wrong rather than merely optional.

## Agreement between the two

Pearson correlation across all 138 teams: **0.9956**.

The two rating sets order the sport almost identically. The standard deviations differ (12.46 against 12.53), which on a shared unit means Makinen's ratings are less spread out — he expects smaller margins between good and bad teams than the workbook's prior does.

## What the workbook's prior actually is right now

> **The v0.8.1 AUTHORITATIVE workbook is frozen and was opened read-only.** Nothing in Phase 6 writes to it, recalculates it or proposes a change to it.

This is the finding that most constrains the comparison, and it is stated plainly rather than worked around:

- The workbook holds **no cached formula results**. It was written programmatically and has not been recalculated by a spreadsheet application, so `TEAM RATINGS!EFFECTIVE RATING` and every other computed cell reads as empty. **No TTW rating can be read out of the file.** Every TTW number in this phase is derived by reimplementing the workbook's own printed formula.
- Of the five preseason sources the workbook is designed to blend, **two are empty**: the TTW independent 2025 prior and the VSiN column. The live blend therefore runs on three third-party sources.

| Source | Configured weight | Present | Effective weight |
| --- | --- | --- | --- |
| SP+ 2026 preseason | 0.3 | 138/138 | **0.4286** |
| FPI 2026 preseason | 0.25 | 138/138 | **0.3571** |
| TTW independent 2025 regressed prior | 0.2 | 0/138 | — (absent) |
| TeamRankings predictive | 0.15 | 138/138 | **0.2143** |
| VSiN (user-supplied) | 0.1 | 0/138 | — (absent) |

> **Consequence, stated for the owner rather than buried.** The comparison in this phase is, at present, *Makinen against a renormalised SP+/FPI/TeamRankings consensus*. It is not Makinen against a distinctively TTW opinion, because the two columns that would carry TTW's own view are blank in v0.8.1. That is a fact about the frozen workbook, not a defect this phase may repair.

## Cross-links

- [Line-model verification](00_LINE_MODEL_VERIFICATION.md) · [TTW comparison](00_TTW_VS_MAKINEN.md) · [workbook provenance](00_WORKBOOK_PROVENANCE.md)
