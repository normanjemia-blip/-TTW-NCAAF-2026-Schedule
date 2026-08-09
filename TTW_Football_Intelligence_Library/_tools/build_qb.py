#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 4 renderer
====================================================

Builds 04_Quarterback_Database from two strictly separated layers.

Layer 1 is authored in _source/qb/*.json from the VSiN guide, through
this library's Phase 1-3A extractions. Layer 2 is read verbatim from
_source/verified/qb_inventory_v079.json and is never recomputed.

Every rendered team file states which layer each statement came from,
and the two never share a section. Phase 4C (discrepancy index) and
Phase 4D (monitoring queue) are derived from the join, not authored.

Usage:
    python3 _tools/build_qb.py            # all 138
    python3 _tools/build_qb.py SEC        # one conference
"""

import json
import os
import re
import sys

from qb_lib import (ABBREV_TO_VSIN, VSIN_TO_ABBREV, load_qb_notes,
                    load_verified, load_vsin_teams)

OUT = "04_Quarterback_Database"
NA = "Not addressed in guide."

# The 23 captured fields, in the owner's stated order. Fields 1, 2, 4 and
# 22 are machine-derived; the rest are authored from the guide.
FIELDS = [
    ("expected_starter", "3. Expected starter in VSiN guide"),
    ("status", "4. Returning starter / new starter / transfer"),
    ("previous_school", "5. Previous school"),
    ("career_experience", "6. Career experience"),
    ("previous_starts", "7. Previous starts"),
    ("passing", "8. Passing production"),
    ("rushing", "9. Rushing contribution"),
    ("efficiency", "10. Efficiency statistics"),
    ("turnovers", "11. Turnover information"),
    ("competition", "12. Competition status"),
    ("backup", "13. Backup / challenger information"),
    ("author_confidence", "14. Author's confidence in the QB situation"),
    ("positive_case", "15. Author's positive case"),
    ("concerns", "16. Author's concerns"),
    ("scheme_fit", "17. Scheme / coordinator fit"),
    ("supporting_cast", "18. Supporting-cast considerations"),
    ("portal_context", "19. Relevant portal context"),
    ("betting_implications", "20. Betting implications explicitly discussed by VSiN"),
    ("outlook_dependency", "21. VSiN team outlook dependency on QB performance"),
]

RELATIONSHIPS = ["ALIGNED", "PARTIALLY ALIGNED", "STALE", "UNRESOLVED",
                 "NO VSIN POSITION"]


def slug(team):
    s = team.lower()
    s = s.replace("’", "").replace("'", "").replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s + ".md"


# ---------------------------------------------------------------------------
# Relationship classification
#
# This compares two independently produced statements about the same
# team. It never adjudicates which is right, and never touches the H/M/L
# code, which is reproduced from Layer 2 exactly as stored.
# ---------------------------------------------------------------------------
def norm_name(s):
    """Reduce a QB name to a comparable key. Returns a set of surnames."""
    if not s:
        return set()
    s = s.replace("’", "'")
    # strip parentheticals such as "(USF transfer)" and "(Notre Dame transfer)"
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\b(open|tbd|undecided|competition|or|vs\.?|and)\b", " ", s, flags=re.I)
    parts = [p for p in re.split(r"[\s/,;|]+", s) if p]
    return {p.lower().strip(".") for p in parts if len(p) > 2}


def is_open(s):
    return bool(s) and bool(re.search(r"\bopen\b|\bundecided\b|\bcompetition\b|/", s, re.I))


def classify(note, ver):
    """Return (relationship, reason). Both inputs may be None."""
    vsin_qb = (note or {}).get("expected_starter", NA)
    has_vsin = bool(vsin_qb) and vsin_qb != NA and not vsin_qb.lower().startswith("not addressed")
    vsin_unsettled = bool((note or {}).get("competition_unsettled"))

    if not has_vsin:
        return ("NO VSIN POSITION",
                "The guide names no expected starter clearly enough to test.")

    active = ver.get("active_qb")
    conf = ver.get("confidence")

    if not active:
        return ("UNRESOLVED",
                "Verified state records no active quarterback for this team.")

    a, v = norm_name(active), norm_name(vsin_qb)
    overlap = bool(a & v)

    # Verified state is itself an unresolved competition.
    if is_open(active) or conf == "L":
        if overlap:
            return ("PARTIALLY ALIGNED",
                    "Verified state still lists this quarterback but the job is "
                    "not settled; confidence is " + str(conf) + ".")
        if vsin_unsettled:
            return ("PARTIALLY ALIGNED",
                    "Both sources describe an unsettled competition, but they "
                    "do not name the same leading quarterback.")
        return ("UNRESOLVED",
                "Verified state records an open competition that does not "
                "confirm or refute the guide's expectation.")

    if overlap:
        return ("ALIGNED",
                "Verified state names the same quarterback the guide expected.")

    if vsin_unsettled:
        return ("PARTIALLY ALIGNED",
                "The guide left the job open; verified state has since settled "
                "on a starter it did not lead with.")

    return ("STALE",
            "Verified state names a different quarterback from the guide's "
            "expected starter.")


def priority(rel, ver, note):
    """Monitoring priority. Ordering only — no H/M/L code is altered."""
    score = 0
    reasons = []
    conf = ver.get("confidence")
    if conf == "L":
        score += 40
        reasons.append("low-confidence verification (L)")
    elif conf == "M":
        score += 20
        reasons.append("medium-confidence verification (M)")
    if is_open(ver.get("active_qb") or ""):
        score += 25
        reasons.append("unresolved competition in verified state")
    if rel == "STALE":
        score += 30
        reasons.append("VSiN/current-state disagreement")
    elif rel == "PARTIALLY ALIGNED":
        score += 15
        reasons.append("partial VSiN/current-state disagreement")
    elif rel == "UNRESOLVED":
        score += 20
        reasons.append("relationship unresolved")
    elif rel == "NO VSIN POSITION":
        score += 5
        reasons.append("no VSiN preseason position")
    if (note or {}).get("qb_dependent"):
        score += 25
        reasons.append("VSiN handicap depends heavily on QB play")
    note_text = (ver.get("note") or "").lower()
    if re.search(r"injur|shoulder|acl|surgery|availability|hurt", note_text):
        score += 10
        reasons.append("injury or availability language in verification note")
    if re.search(r"transfer", note_text):
        score += 5
        reasons.append("transfer context in verification note")
    return score, reasons


def field(note, key):
    v = (note or {}).get(key)
    if v is None or v == "":
        return NA
    return v


def render(team, det, note, ver, rel, reason, score, reasons):
    ab = VSIN_TO_ABBREV[team]
    pages = det["pages"]
    ret = det.get("returning_starters", {}).get("offense", {})
    lines = []
    A = lines.append

    A("<!-- GENERATED FILE — do not hand-edit.")
    A("     Rebuild:  python3 _tools/build_qb.py")
    A("     Layer 1:  2026 VSiN College Football Betting Guide (authored notes)")
    A("     Layer 2:  TTW QB verification project, read-only -->")
    A("")
    A(f"# {team} — Quarterback Intelligence")
    A("")
    A(f"> **Two layers, never merged.** Section A is what the VSiN guide said at "
      f"publication (pp. {pages[0]}–{pages[-1]}). Section B is the independently "
      f"verified current state from the TTW Power Ratings QB verification "
      f"project. Nothing in Section B is VSiN's opinion; nothing in Section A is "
      f"a current fact.")
    A("")

    # ---------------- Section A — Layer 1 ----------------
    A("## A. VSiN PRESEASON QB INTELLIGENCE")
    A("")
    A("*Source class: GUIDE CONTENT. 2026 VSiN College Football Betting Guide, "
      "as printed. No outside research. Nothing inferred to fill a field.*")
    A("")
    A("| # | Field | Value |")
    A("| --- | --- | --- |")
    A(f"| 1 | Team | {team} |")
    A(f"| 2 | Conference | {det['conference']} |")

    n = 3
    for key, label in FIELDS:
        num = label.split(".")[0]
        name = label.split(". ", 1)[1]
        val = field(note, key)
        A(f"| {num} | {name} | {val} |")
    A(f"| 22 | Relevant page references | pp. {pages[0]}–{pages[-1]} |")
    A(f"| 23 | Source conflicts / ambiguities | {field(note, 'conflicts')} |")
    A("")

    # The returning-QB marker is a printed field on the team spread, so it
    # is reported as its own machine-read fact rather than folded into the
    # authored status line.
    mark = ret.get("returning_qb")
    A(f"**Returning-QB marker on the team spread (p. {pages[0]}):** "
      f"{'present — the guide marks this team as returning its quarterback' if mark else 'absent — the guide does not mark this team as returning its quarterback'}. "
      f"Printed offensive returning starters: {ret.get('value', 'n/a')}.")
    A("")
    A(f"Team file: [../02_Team_Database/{slug(team)}](../02_Team_Database/{slug(team)})")
    A("")

    # ---------------- Section B — Layer 2 ----------------
    A("## B. CURRENT VERIFIED STATE — EXTERNAL TO VSiN GUIDE")
    A("")
    A("*Source class: POST-PUBLICATION UPDATE. Reproduced verbatim from the TTW "
      "Power Ratings QB verification project (Phases 7A–7D.5 / 8.x). Not VSiN "
      "content. Not re-derived, not recalculated, not edited by this phase.*")
    A("")
    A("| Field | Value |")
    A("| --- | --- |")
    A(f"| Workbook team | {ver['team']} (`{ab}`, QB VALUES row {ver['row']}) |")
    A(f"| Currently verified expected starter | {ver.get('active_qb') or '—'} |")
    A(f"| Baseline QB | {ver.get('baseline_qb') or '—'} |")
    A(f"| Current competition status | "
      f"{'OPEN — competition unresolved' if is_open(ver.get('active_qb') or '') else 'Settled in the verified record'} |")
    A(f"| Existing H/M/L confidence classification | **{ver['confidence']}** "
      f"(reproduced exactly; not recalculated) |")
    A(f"| Verification date | {ver.get('last_update') or '—'} |")
    A(f"| Reviewed for season | {ver.get('reviewed_for_season') or '—'} |")
    A(f"| Verification status | {ver.get('verification_status') or '—'} |")
    A(f"| QB value in workbook | "
      f"{'blank (UNCERTAIN)' if ver.get('active_value') is None else ver.get('active_value')} "
      f"— unchanged by this phase |")
    A("")
    A("**Verification source / evidence summary**")
    A("")
    A(f"- Source: {ver.get('source') or '—'}")
    A(f"- Evidence: {ver.get('note') or '—'}")
    A("")

    # ---------------- Section C — the join ----------------
    A("## C. RELATIONSHIP BETWEEN THE LAYERS")
    A("")
    A(f"### {rel}")
    A("")
    A(reason)
    A("")
    A("| | |")
    A("| --- | --- |")
    A(f"| VSiN preseason expectation | {field(note, 'expected_starter')} |")
    A(f"| Current verified state | {ver.get('active_qb') or '—'} |")
    A(f"| Does the VSiN assumption still appear current? | {still_current(rel)} |")
    A(f"| Monitoring priority score | {score} |")
    A("")
    if reasons:
        A("Priority drivers: " + "; ".join(reasons) + ".")
        A("")
    A("> This classification compares two sources. It does not decide which is "
      "correct, and it does not change the workbook's H/M/L code or QB value.")
    A("")
    return "\n".join(lines) + "\n"


def still_current(rel):
    return {
        "ALIGNED": "Yes — verified state agrees.",
        "PARTIALLY ALIGNED": "Partly — the core expectation survives, but "
                             "certainty or personnel have moved.",
        "STALE": "No — superseded by verified information.",
        "UNRESOLVED": "Cannot be determined from existing evidence.",
        "NO VSIN POSITION": "Not applicable — the guide took no clear position.",
    }[rel]


def build():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    details = load_vsin_teams()
    notes = load_qb_notes()
    meta, verified = load_verified()

    os.makedirs(OUT, exist_ok=True)
    rows = []
    written = 0
    for team in sorted(details):
        det = details[team]
        if only and det["conference"] != only:
            continue
        ab = VSIN_TO_ABBREV[team]
        ver = verified[ab]
        note = notes.get(team)
        rel, reason = classify(note, ver)
        score, why = priority(rel, ver, note)
        with open(os.path.join(OUT, slug(team)), "w") as fh:
            fh.write(render(team, det, note, ver, rel, reason, score, why))
        written += 1
        rows.append({
            "team": team, "abbrev": ab, "conference": det["conference"],
            "vsin_starter": field(note, "expected_starter"),
            "vsin_pages": f"{det['pages'][0]}-{det['pages'][-1]}",
            "verified_starter": ver.get("active_qb"),
            "confidence": ver["confidence"],
            "verification_date": ver.get("last_update"),
            "verification_status": ver.get("verification_status"),
            "relationship": rel, "reason": reason,
            "priority": score, "priority_drivers": why,
            "qb_dependent": bool((note or {}).get("qb_dependent")),
            "has_note": note is not None,
        })

    with open("_source/data/qb_crossref.json", "w") as fh:
        json.dump({"generated_from": {
            "layer1": "2026 VSiN College Football Betting Guide (this library)",
            "layer2": meta}, "records": rows}, fh, indent=1)
    print(f"quarterback files written: {written}" + (f" ({only})" if only else ""))
    return rows


if __name__ == "__main__":
    build()
