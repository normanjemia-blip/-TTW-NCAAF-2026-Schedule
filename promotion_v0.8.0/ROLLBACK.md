# ROLLBACK INSTRUCTIONS — v0.8.0 → v0.6.2

**Rollback target:** `workbook_v0.6.2_deliverables/TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx`
**Target SHA-256:** `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd`

Rollback is **safe and lossless**. v0.6.2 is unmodified, committed, and its SHA-256
matches `PROJECT_MANIFEST.json`. Nothing in the promotion overwrote it.

## When to roll back

Roll back if **any** of these is observed after promotion:

- A team rating or projected spread differs from its pre-promotion value. *(Should be
  impossible — all QB deltas are 0 and `TEAM RATINGS`/`ENGINE` are byte-identical — so
  treat this as evidence of a deeper problem.)*
- The workbook fails to open, or recalculation produces `#REF!`/`#N/A` in `ENGINE`,
  `CLEAN`, `CALC` or `TEAM RATINGS`.
- Formula count on open is anything other than **123,011**.
- Any sheet is missing; sheet count is anything other than **21**.
- `SETTINGS!B3` ≠ 2026, `B6` ≠ 2.5, or `B11` ≠ "N".

**Do not roll back** merely because a QB record is out of date. That is expected during
fall camp and is handled by a monitoring sweep, not a rollback.

## Procedure — local / repository

```bash
cd /home/user/-TTW-NCAAF-2026-Schedule

# 1. Confirm the rollback target is intact BEFORE touching anything
sha256sum workbook_v0.6.2_deliverables/TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx
# must print: bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd

# 2. Restore it as the operating workbook
cp workbook_v0.6.2_deliverables/TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx \
   ./TTW_NCAAF_Power_Ratings_2026_AUTHORITATIVE.xlsx

# 3. Verify the restored copy
sha256sum ./TTW_NCAAF_Power_Ratings_2026_AUTHORITATIVE.xlsx   # same hash as step 1

# 4. Revert the manifest pointer
git checkout PROJECT_MANIFEST.json
```

The promotion is a **file designation plus a manifest pointer**. There is no migration,
no schema change and no data transformation to undo.

## Procedure — Google Sheets

The native Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` was **never
touched** by any phase of this project, and neither was the rollback sheet
`1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo`. If the owner imports v0.8.0 into
Sheets, roll back by re-importing v0.6.2 or by restoring the pre-import Sheets version
from File → Version history. **Take a Sheets version snapshot immediately before any
import** so this path stays available.

## What a rollback costs

Reverting to v0.6.2 restores an **empty QB dataset**: 0/138 confidence codes, all 138
teams computing **UNCERTAIN**. Ratings and spreads are unaffected — they are identical
in both workbooks. So the cost of rolling back is losing the verification metadata and
returning to a blanket-uncertain QB gate, not losing any computed output.

## Partial rollback

Not applicable and not recommended. The change is confined to one data sheet plus a
changelog and a banner; there is no meaningful subset to revert. If a single QB record
is wrong, correct that record in a new candidate — do not roll back the workbook.
