# TTW Football Intelligence Library

**Version 1.3 — Phases 1–4 complete**

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
| 2 | Conference Database | `01_Conference_Database` | ✅ **Complete** |
| 3 | Team Database | `02_Team_Database` | ✅ **Complete** |
| 3A | Team Database paraphrase pass | `02_Team_Database` | ✅ **Complete — 138/138** |
| 4 | Quarterback Database | `04_Quarterback_Database` | ✅ **Complete** |
| 5 | Coaching Database | `03_Coaching_Database` | ⏸ Pending |
| 6 | Power Ratings | `05_Power_Ratings` | ⏸ Pending |
| 7 | Win Totals | `06_Win_Totals` | ⏸ Pending |
| 8 | Futures | `07_Futures` | ⏸ Pending |
| 9 | Betting Concepts | `11_Betting_Concepts` | ⏸ Pending |
| 10 | Historical Trends | `12_Historical_Trends` | ⏸ Pending |
| 11 | Search Optimization | `99_Search_Index` | ⏸ Pending |

### Folded directories (Director decision, 2026-08-08)

No Phases 12–16 are created. These five directories are filled by existing
phases rather than getting phases of their own:

| Directory | Filled by |
| --- | --- |
| `08_Returning_Production` | Phase 3 — **resolved**, extracted by coordinate in Phase 3 |
| `09_Transfer_Portal` | Phase 3, with conference-level summaries in Phase 2 |
| `10_Schedule_Intelligence` | Phase 2 and Phase 3 |
| `13_Situational_Angles` | Phase 9 if conceptual, Phase 10 if historical or system-based |
| `14_Statistics_Reference` | Phase 9 — team-level values **resolved** in Phase 3; concept material still pending |

Phase numbers and directory numbers deliberately differ (`05_Power_Ratings` is
Phase 6, `07_Futures` is Phase 8), so this library refers to **directory names,
never bare phase numbers**, wherever ambiguity is possible.

### Team file schema (Director decision, 2026-08-08)

Every FBS team file in Phase 3 carries the **full standardised 24-heading
schema**. Where the guide does not address a heading, the file states
`Not addressed in guide.` Headings are never dropped for source silence, so all
138 files stay structurally identical and searchable.

---

## Phase 3A — paraphrase pass

Phase 3 built the team files by reproducing VSiN's prose. Phase 3A rewrites that
prose into TTW reference notes so the library carries the guide's **information
and reasoning** without reproducing substantial portions of its text.

**Status: 138 of 138 teams converted.** Every team file now carries the heading
*"Season outlook — VSiN's analysis in reference form"*; no file renders guide
prose any more. (The renderer keeps its automatic fallback to guide prose, so a
future team added without notes still produces a coherent file.)

The pass did not shorten the database. Measured against the committed Phase 3
baseline, the 138 files went from 559,007 to 583,080 words (**+4.3%**) — the
reference notes carry more of the guide's reasoning explicitly than the
reproduced prose did implicitly.

Paraphrases live in `_source/paraphrase/*.json`, 32 batch files covering all
138 teams, and are authored rather than generated. Numbers, tables, page
references, source conflicts and cross-links are never touched by this pass — a
machine comparison enforces that, and reports **0 regressions** across all 138
files:

```bash
python3 _tools/snapshot_fields.py _source/data/fields_before.json --compare
```

---

## Phase 4 — Quarterback Intelligence Database

Two layers that are never merged, one file per team in
`04_Quarterback_Database/`:

- **Layer 1 — VSiN preseason QB intelligence.** `GUIDE CONTENT`: 23 fields
  per team from the 2026 guide, via Phases 1–3A.
- **Layer 2 — Current verified QB state.** `POST-PUBLICATION UPDATE`: the
  TTW Power Ratings QB verification project (Phases 7A–7D.5 / 8.x), read
  verbatim from `_source/verified/` and never recomputed.

Each team file then classifies the relationship between them as
**ALIGNED**, **PARTIALLY ALIGNED**, **STALE**, **UNRESOLVED** or
**NO VSIN POSITION**. The classification adjudicates nothing: it does not
decide which layer is right, and it never changes an H/M/L code or a
workbook value.

```bash
PYTHONPATH=_tools python3 _tools/validate_qb.py    # 12 checks
```

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
├── 01_Conference_Database/   11 conference files + index (Phase 2)
├── 02_Team_Database/         138 team files + index (Phase 3)
├── 01_…14_                   phase databases, each with a README stating scope
├── 99_Search_Index/          cross-reference layer (Phase 11)
├── _source/
│   ├── SOURCE_MANIFEST.md    provenance, integrity, extraction method
│   ├── extracted/            full guide text, whole and per page
│   ├── data/                 machine-readable entity tables (JSON)
│   ├── paraphrase/           authored Phase 3A reference notes
│   ├── qb/                   authored Phase 4A VSiN QB records
│   └── verified/             READ-ONLY copy of the TTW QB verification project
└── _tools/
    ├── extract_guide.py      PDF → JSON + text, with validation
    ├── build_index.py        JSON → the Master Index
    ├── extract_conferences.py  conference previews + projected standings
    ├── extract_phase2.py     predictions, win totals, best bets, new coaches
    ├── build_conferences.py  JSON → the Conference Database
    ├── extract_teams.py      coordinate-based extraction of all 138 spreads
    ├── extract_stability.py  Stability Scores (pp. 41–44)
    ├── extract_mentions.py   cross-guide mention index
    ├── build_teams.py        JSON → the Team Database
    ├── validate_teams.py     Phase 3 completion checks
    ├── qb_lib.py             Phase 4 canonical identity map + loaders
    ├── build_qb.py           two-layer Quarterback Database renderer
    ├── build_qb_reports.py   discrepancy index + monitoring queue
    └── validate_qb.py        Phase 4 layer-separation and reproduction checks
```

## Rebuilding

The index is generated, never hand-edited. Extraction fixes are made once in
`_tools/` and flow through everything:

```bash
pip install pymupdf
python3 _tools/extract_guide.py _source/2026-VSiN-CFB-Betting-Guide.pdf _source
python3 _tools/build_index.py
python3 _tools/extract_conferences.py
python3 _tools/extract_phase2.py
python3 _tools/build_conferences.py
python3 _tools/extract_teams.py
python3 _tools/extract_stability.py
python3 _tools/extract_mentions.py
python3 _tools/build_teams.py
python3 _tools/validate_teams.py
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
