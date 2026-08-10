<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_power.py
     Source:   2026 VSiN College Football Betting Guide;
               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->

# VSiN Import Candidate — prepared, not applied

> **The v0.8.1 AUTHORITATIVE workbook is frozen and was opened read-only.** Nothing in Phase 6 writes to it, recalculates it or proposes a change to it.

## Why this file exists

The workbook was built with a fifth preseason source it has never been given. `PRESEASON` reserves columns U–X for a VSiN rating, and `SETTINGS` carries a configured weight of **0.1** for *VSiN (user-supplied)*. Both the raw column and the date and citation columns are empty in v0.8.1, so the weight renormalises away and the source contributes nothing.

Phase 6 is the first phase to hold the numbers that column was designed for. So the import set is **prepared here and left unapplied**: `_source/data/vsin_preseason_import.csv`, 138 rows, keyed on the workbook's own abbreviations.

## What is in it

| Column | Class | Content |
| --- | --- | --- |
| `abbrev` | workbook | the workbook's own team key |
| `team_workbook` / `team_vsin` | join | both names, so the join is auditable rather than implicit |
| `vsin_raw` | GUIDE CONTENT | the rating exactly as printed on p. 47 |
| `vsin_norm_ttw_derived` | TTW DERIVED | the mean-centred value, matching the workbook's own normalisation convention |
| `vsin_date`, `vsin_cite` | provenance | publication date and page citation, in the form the sheet's sibling columns already use |

## What has deliberately not been done

- The workbook has **not** been opened for writing, modified, re-saved or copied into the tracked tree.
- No cell has been populated and no weight has been changed.
- No claim is made that importing this source would improve the ratings. That is an owner decision and, on the evidence of this phase, a Phase 7 calibration question.

> Applying this file would change the workbook, which is frozen. It is offered as a prepared input awaiting an explicit instruction, and for no other purpose.

## Cross-links

- [Scale reconciliation](00_SCALE_RECONCILIATION.md) · [workbook provenance](00_WORKBOOK_PROVENANCE.md)
