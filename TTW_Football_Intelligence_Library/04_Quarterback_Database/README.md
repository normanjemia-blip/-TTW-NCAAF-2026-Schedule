# 04 Quarterback Database

**Status:** ✅ **Phase 4 complete** — 138 teams, two layers, never merged.

## Scope

One file per FBS team. Each carries three sections that are kept strictly
apart, because they answer different questions and come from different
places:

| Section | Source class | What it is |
| --- | --- | --- |
| **A. VSiN preseason QB intelligence** | `GUIDE CONTENT` | The 23-field record of what the 2026 VSiN College Football Betting Guide said at publication, built from this library's Phase 1–3A extractions. `Not addressed in guide.` wherever the guide is silent. |
| **B. Current verified state** | `POST-PUBLICATION UPDATE` | Read verbatim from the TTW Power Ratings QB verification project (Phases 7A–7D.5 / 8.x). Never recomputed. |
| **C. Relationship** | derived | The comparison between them. Adjudicates nothing; changes nothing. |

**Start here → [00_QUARTERBACK_INDEX.md](00_QUARTERBACK_INDEX.md)**

- [QB Discrepancy Index](00_QB_DISCREPANCY_INDEX.md) — Phase 4C
- [QB Monitoring Queue](00_QB_MONITORING_QUEUE.md) — Phase 4D

## What this phase does not do

- It does not modify the **v0.8.1 AUTHORITATIVE** workbook, or read it for
  anything other than verification of the committed inventory.
- It does not change, recalculate or propose changes to any **H/M/L
  confidence code**. Those are reproduced exactly as stored.
- It does not merge current information into VSiN's preseason opinion, in
  either direction. A machine check enforces that on every build.

## Layer 2 provenance

`_source/verified/` holds a read-only copy of the verification artifacts,
taken from the TTW Power Ratings branch:

| File | What it is |
| --- | --- |
| `qb_inventory_v079.json` / `.csv` | The Phase 7D.5 QB inventory, 138 records, generated 2026-08-04. Reproduces the QB VALUES sheet of v0.8.1 AUTHORITATIVE exactly — verified field by field against the workbook, 0 mismatches. |
| `MAINTENANCE_CERTIFICATE_v0.8.1.md` | Establishes that v0.8.1 changed exactly one cell (`START HERE!A1`) versus v0.8.0, so no QB value or code moved at promotion. |
| `pending_qb_resolutions.json` | The Phase 8.4 monitoring ledger — **empty**, confirming no verified QB state supersedes the inventory. |

## Rebuilding

```bash
PYTHONPATH=_tools python3 _tools/build_qb.py          # 138 team files + crossref
PYTHONPATH=_tools python3 _tools/build_qb_reports.py  # Phase 4C + 4D
PYTHONPATH=_tools python3 _tools/validate_qb.py       # 12 checks, exits non-zero on failure
```

Layer 1 is authored in `_source/qb/*.json`; Layer 2 is read-only. The
renderer is the only thing that ever sees both.
