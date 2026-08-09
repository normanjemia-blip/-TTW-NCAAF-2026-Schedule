#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 4C and 4D
====================================================

Derives the discrepancy index and the monitoring queue from the join
written by build_qb.py. Nothing here is authored: both files are a
rendering of the comparison, so they cannot drift from the two layers.

The monitoring queue orders teams for future research. It does not
change, recompute or reinterpret any H/M/L confidence code — those are
reproduced exactly as stored in the verified dataset, and the priority
score is a separate ordering field that sits beside them.

Usage:
    python3 _tools/build_qb_reports.py
"""

import json
import os

from qb_lib import load_qb_notes, load_verified

OUT = "04_Quarterback_Database"

ORDER = {"STALE": 0, "PARTIALLY ALIGNED": 1, "UNRESOLVED": 2,
         "NO VSIN POSITION": 3, "ALIGNED": 4}


def load():
    with open("_source/data/qb_crossref.json") as fh:
        return json.load(fh)


def esc(s):
    return (s or "—").replace("|", "\\|").replace("\n", " ")


def discrepancy_index(rows, meta):
    """Phase 4C — every team whose layers do not simply agree."""
    disc = [r for r in rows if r["relationship"] != "ALIGNED"]
    disc.sort(key=lambda r: (ORDER[r["relationship"]], -r["priority"], r["team"]))

    L = []
    A = L.append
    A("<!-- GENERATED FILE — do not hand-edit. Rebuild: python3 _tools/build_qb_reports.py -->")
    A("")
    A("# QB Discrepancy Index — VSiN preseason vs current verified state")
    A("")
    A("**Phase 4C.** Every team where the VSiN guide's preseason quarterback "
      "expectation and the independently verified current state do not simply "
      "agree. Teams classified ALIGNED are omitted here and listed in the "
      "coverage summary instead.")
    A("")
    A("> Two layers, never merged. The VSiN column is GUIDE CONTENT as printed. "
      "The verified column is POST-PUBLICATION UPDATE from the TTW Power Ratings "
      "QB verification project, reproduced verbatim. **The H/M/L code is the "
      "existing classification, reproduced exactly — nothing in this phase "
      "recalculates it.**")
    A("")
    A("A discrepancy is not a betting edge. The market has had the same "
      "months the verification project did. The **QB-dependent** column marks "
      "the teams where VSiN itself said its handicap leans heavily on "
      "quarterback play — that is where a discrepancy is most likely to matter, "
      "and it is the only betting-relevance claim this index makes.")
    A("")
    A(f"| # | Team | Conf | VSiN preseason expectation | VSiN pp. | Current verified state | H/M/L | Verified | Relationship | Why they differ | QB-dependent |")
    A("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for i, r in enumerate(disc, 1):
        A(f"| {i} | {esc(r['team'])} | {esc(r['conference'])} | "
          f"{esc(r['vsin_starter'])} | {esc(r['vsin_pages'])} | "
          f"{esc(r['verified_starter'])} | **{r['confidence']}** | "
          f"{esc(r['verification_date'])} | {r['relationship']} | "
          f"{esc(r['reason'])} | {'**yes**' if r['qb_dependent'] else 'no'} |")
    A("")
    A("## Counts")
    A("")
    A("| Relationship | Teams |")
    A("| --- | --- |")
    for k in ["ALIGNED", "PARTIALLY ALIGNED", "STALE", "UNRESOLVED",
              "NO VSIN POSITION"]:
        A(f"| {k} | {sum(1 for r in rows if r['relationship'] == k)} |")
    A(f"| **Total** | **{len(rows)}** |")
    A("")
    A("## Verified-state provenance")
    A("")
    A("Every row's verified column and H/M/L code come from a single "
      "committed artifact, unmodified by this library:")
    A("")
    A("```")
    A(json.dumps(meta["layer2"], indent=1))
    A("```")
    A("")
    with open(os.path.join(OUT, "00_QB_DISCREPANCY_INDEX.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    return disc


def monitoring_queue(rows):
    """Phase 4D — research order, not a workbook change."""
    q = sorted(rows, key=lambda r: (-r["priority"], r["team"]))
    L = []
    A = L.append
    A("<!-- GENERATED FILE — do not hand-edit. Rebuild: python3 _tools/build_qb_reports.py -->")
    A("")
    A("# QB Monitoring Queue — preseason")
    A("")
    A("**Phase 4D.** Research order for the teams whose quarterback situation "
      "is least settled. This queue exists to direct future work.")
    A("")
    A("> **It changes nothing.** No H/M/L confidence code is altered, "
      "recalculated or proposed for alteration here. No workbook value is "
      "touched. The priority score is an ordering device created by this phase "
      "and has no standing in the TTW Power Ratings workbook.")
    A("")
    A("Priority is built from the five drivers the owner specified: an "
      "unresolved QB competition, VSiN/current-state disagreement, a VSiN "
      "handicap that depends heavily on QB play, recent transfer or injury "
      "uncertainty already documented in the verification note, and a "
      "low-confidence existing verification.")
    A("")
    A("| Rank | Team | Conf | Priority | H/M/L | Relationship | Verified starter | Drivers |")
    A("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for i, r in enumerate(q, 1):
        if r["priority"] == 0:
            continue
        A(f"| {i} | {esc(r['team'])} | {esc(r['conference'])} | {r['priority']} | "
          f"**{r['confidence']}** | {r['relationship']} | "
          f"{esc(r['verified_starter'])} | {esc('; '.join(r['priority_drivers']))} |")
    A("")
    zero = [r for r in q if r["priority"] == 0]
    A(f"**{len(zero)} teams score zero** and are not queued: an H-confidence "
      "verification, a settled job, agreement between the layers, and no VSiN "
      "statement that the handicap turns on the quarterback. They are "
      f"{', '.join(sorted(r['team'] for r in zero))}.")
    A("")
    with open(os.path.join(OUT, "00_QB_MONITORING_QUEUE.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    return q


def index(rows, meta):
    from collections import Counter
    conf = Counter(r["conference"] for r in rows)
    rel = Counter(r["relationship"] for r in rows)
    hml = Counter(r["confidence"] for r in rows)
    notes = load_qb_notes()
    NA = "Not addressed in guide."
    # Field-level VSiN coverage across the 19 authored fields.
    from build_qb import FIELDS
    cover = {}
    for key, label in FIELDS:
        filled = sum(1 for t in notes if notes[t].get(key) and notes[t][key] != NA)
        cover[label] = filled

    L = []
    A = L.append
    A("<!-- GENERATED FILE — do not hand-edit. Rebuild: python3 _tools/build_qb_reports.py -->")
    A("")
    A("# 04 — Quarterback Intelligence Database")
    A("")
    A("**Phase 4.** One file per FBS team, each carrying three sections that "
      "never mix:")
    A("")
    A("- **A. VSiN preseason QB intelligence** — GUIDE CONTENT, 23 fields, from "
      "the 2026 VSiN College Football Betting Guide via this library's Phase "
      "1–3A extractions. `Not addressed in guide.` wherever the guide is silent.")
    A("- **B. Current verified state** — POST-PUBLICATION UPDATE, read verbatim "
      "from the TTW Power Ratings QB verification project (Phases 7A–7D.5 / "
      "8.x). Never recomputed.")
    A("- **C. Relationship** — the comparison between them, which adjudicates "
      "nothing and changes nothing.")
    A("")
    A("| | |")
    A("| --- | --- |")
    A(f"| Teams | {len(rows)} |")
    A(f"| VSiN QB records authored | {len(notes)} |")
    A(f"| Verified records read | {len(rows)} |")
    A("")
    A("## Relationship counts")
    A("")
    A("| Relationship | Teams |")
    A("| --- | --- |")
    for k in ["ALIGNED", "PARTIALLY ALIGNED", "STALE", "UNRESOLVED",
              "NO VSIN POSITION"]:
        A(f"| {k} | {rel.get(k, 0)} |")
    A("")
    A("## Existing H/M/L confidence — reproduced, not recalculated")
    A("")
    A("| Code | Teams |")
    A("| --- | --- |")
    for k in ["H", "M", "L"]:
        A(f"| {k} | {hml.get(k, 0)} |")
    A("")
    A("## VSiN field coverage")
    A("")
    A("How often the guide actually supplied each field, across 138 teams. A "
      "low number is a fact about the guide, not a gap in this database.")
    A("")
    A("| Field | Teams with content | % |")
    A("| --- | --- | --- |")
    for label, n in cover.items():
        A(f"| {label} | {n} | {n * 100 // len(rows)}% |")
    A("")
    A("## Reports")
    A("")
    A("- [QB Discrepancy Index](00_QB_DISCREPANCY_INDEX.md) — Phase 4C")
    A("- [QB Monitoring Queue](00_QB_MONITORING_QUEUE.md) — Phase 4D")
    A("")
    A("## Teams by conference")
    A("")
    A("| Conference | Teams |")
    A("| --- | --- |")
    for c in sorted(conf):
        A(f"| {c} | {conf[c]} |")
    A("")
    with open(os.path.join(OUT, "00_QUARTERBACK_INDEX.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")


def main():
    data = load()
    rows, meta = data["records"], data["generated_from"]
    disc = discrepancy_index(rows, meta)
    q = monitoring_queue(rows)
    index(rows, meta)
    print(f"discrepancy index   {len(disc)} teams")
    print(f"monitoring queue    {sum(1 for r in q if r['priority'] > 0)} queued, "
          f"{sum(1 for r in q if r['priority'] == 0)} clear")
    print("index written")


if __name__ == "__main__":
    main()
