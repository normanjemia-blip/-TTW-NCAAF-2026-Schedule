# TTW Football Intelligence Library

**Version 1.0 — Phase 1 (Master Index) complete**

TTW's permanent football research encyclopedia, built from the 2026 VSiN College
Football Betting Guide. The goal is that the 345-page guide never has to be
searched by hand again.

This library **supplements** the TTW College Football Power Ratings Workbook
(v0.8.1 AUTHORITATIVE). It never replaces, modifies, critiques or redesigns it.
The workbook is frozen production software; the two are separate projects.

---

## Start here

**→ [00_Master_Index/00_MASTER_INDEX.md](00_Master_Index/00_MASTER_INDEX.md)**

That file is the navigation system for everything else.

---

## Phase status

| Phase | Deliverable | Directory | Status |
| --- | --- | --- | --- |
| 1 | Master Index | `00_Master_Index` | ✅ **Complete** |
| 2 | Conference Database | `01_Conference_Database` | ⏸ Awaiting approval |
| 3 | Team Database | `02_Team_Database` | ⏸ Pending |
| 4 | Quarterback Database | `04_Quarterback_Database` | ⏸ Pending |
| 5 | Coaching Database | `03_Coaching_Database` | ⏸ Pending |
| 6 | Power Ratings | `05_Power_Ratings` | ⏸ Pending |
| 7 | Win Totals | `06_Win_Totals` | ⏸ Pending |
| 8 | Futures | `07_Futures` | ⏸ Pending |
| 9 | Betting Concepts | `11_Betting_Concepts` | ⏸ Pending |
| 10 | Historical Trends | `12_Historical_Trends` | ⏸ Pending |
| 11 | Search Optimization | `99_Search_Index` | ⏸ Pending |
| — | Returning Production | `08_Returning_Production` | ⚠️ No phase assigned |
| — | Transfer Portal | `09_Transfer_Portal` | ⚠️ No phase assigned |
| — | Schedule Intelligence | `10_Schedule_Intelligence` | ⚠️ No phase assigned |
| — | Situational Angles | `13_Situational_Angles` | ⚠️ No phase assigned |
| — | Statistics Reference | `14_Statistics_Reference` | ⚠️ No phase assigned |

Phase numbers and directory numbers **do not correspond**. Five directories have
no phase in the workflow — see
[13 — Open Questions and Gaps](00_Master_Index/13_Open_Questions_And_Gaps.md),
item 3, which needs a Director decision.

---

## Standing rules

1. **Three source classes, never mixed.**
   - `GUIDE CONTENT` — from the VSiN guide, with a page reference
   - `POST-PUBLICATION UPDATE` — outside research, permitted only for coaching
     changes, injuries, portal movement, roster changes, suspensions,
     conference changes and corrected factual errors
   - `PERSONAL INFERENCE` — TTW judgement
2. **Never invent, guess, or fill gaps.** A gap is recorded as a gap.
3. **Preserve disagreement.** Where guide authors conflict, every view is kept
   with attribution. Uncertainty is maintained, not resolved.
4. **Page references wherever possible.** Printed page numbers equal PDF page
   numbers throughout this guide.
5. **One phase at a time**, stopping for approval after each.

---

## Repository layout

```
TTW_Football_Intelligence_Library/
├── 00_Master_Index/          14 index files — the navigation layer (Phase 1)
├── 01_…14_                   phase databases, each with a README stating scope
├── 99_Search_Index/          cross-reference layer (Phase 11)
├── _source/
│   ├── SOURCE_MANIFEST.md    provenance, integrity, extraction method
│   ├── extracted/            full guide text, whole and per page
│   └── data/                 machine-readable entity tables (JSON)
└── _tools/
    ├── extract_guide.py      PDF → JSON + text, with validation
    └── build_index.py        JSON → the Master Index
```

## Rebuilding

The index is generated, never hand-edited. Extraction fixes are made once in
`_tools/` and flow through everything:

```bash
pip install pymupdf
python3 _tools/extract_guide.py _source/2026-VSiN-CFB-Betting-Guide.pdf _source
python3 _tools/build_index.py
```

The guide PDF is committed under `_source/`, so this runs with no external
retrieval. Verified 2026-08-08: a full re-run reproduces the committed index
byte-for-byte.

`extract_guide.py` exits non-zero if validation fails, so a bad extraction can
never silently produce a plausible-looking library.

## Ad-hoc research

The full guide text is extracted and greppable:

```bash
grep -n 'Kirby Smart' _source/extracted/guide_full.txt   # page-marked
cat _source/extracted/pages/p292.txt                     # a single page
```
