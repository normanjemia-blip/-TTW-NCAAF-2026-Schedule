#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 11 shared library
=============================================================

The cross-reference layer's loaders and entity registry.

Phase 11 introduces **no football knowledge**. Every fact it surfaces was
extracted, authored, validated and approved in Phases 1-10; this layer only
makes those facts reachable from an entity a reader already has in mind.
The rule that follows from that, and which the validator enforces, is:

    THE SEARCH LAYER MAY POINT. IT MAY NOT ASSERT.

So the registry below stores *locations* -- which approved file mentions
which entity -- and never a new claim about the entity. Where a field is
not supported by an approved artifact, the absence marker is used or the
reader is pointed at the source, rather than the field being manufactured.

Three directories the Director folded into Phases 2-3 are built here as
derived views over that same approved data: returning production, transfer
portal and schedule intelligence. None of them re-reads the PDF.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "_source", "data")

NA = "Not addressed in guide."

# Every directory holding approved, rendered library content.
PHASE_DIRS = [
    ("00_Master_Index", 1, "Master Index"),
    ("01_Conference_Database", 2, "Conference Database"),
    ("02_Team_Database", 3, "Team Database"),
    ("03_Coaching_Database", 5, "Coaching Database"),
    ("04_Quarterback_Database", 4, "Quarterback Database"),
    ("05_Power_Ratings", 6, "Power Ratings"),
    ("06_Win_Totals", 7, "Win Totals"),
    ("07_Futures", 8, "Futures"),
    ("08_Returning_Production", 11, "Returning Production (derived view)"),
    ("09_Transfer_Portal", 11, "Transfer Portal (derived view)"),
    ("10_Schedule_Intelligence", 11, "Schedule Intelligence (derived view)"),
    ("11_Betting_Concepts", 9, "Betting Concepts"),
    ("12_Historical_Trends", 10, "Historical Trends"),
    ("13_Situational_Angles", 9, "Situational Angles"),
    ("14_Statistics_Reference", 9, "Statistics Reference"),
    ("99_Search_Index", 11, "Search Index"),
]

# Directories the search layer indexes. It never indexes itself: doing so
# would let a pointer count as evidence that the thing pointed at exists.
INDEXED_DIRS = [d for d, _, _ in PHASE_DIRS if d != "99_Search_Index"]


def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


def teams():
    return load("team_details.json")


def conferences():
    return load("conference_previews.json")


def markdown_files(dirs=None):
    """Every rendered markdown file in the approved library, by directory."""
    out = {}
    for d in (dirs or INDEXED_DIRS):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for fn in sorted(os.listdir(p)):
            if fn.endswith(".md"):
                with open(os.path.join(p, fn)) as fh:
                    out[f"{d}/{fn}"] = fh.read()
    return out


# --------------------------------------------------------------- entities

def entity_registry(files, team_list, conf_list):
    """entity -> {kind, files[]}.

    A team is matched on its full canonical name only. Substring matching
    on a short name would put every "Miami" mention on both Miami
    Hurricanes and Miami (Ohio) RedHawks, which is exactly the alias drift
    ten phases of enumerated bijections exist to prevent.
    """
    reg = {}

    def add(name, kind, path):
        e = reg.setdefault(name, {"kind": kind, "files": []})
        if path not in e["files"]:
            e["files"].append(path)

    names = {t["team"]: "team" for t in team_list}
    for c in conf_list:
        names[c["conference"]] = "conference"
    coaches = {t["head_coach"]: "coach" for t in team_list if t.get("head_coach")}
    names.update(coaches)

    for path, body in files.items():
        for name, kind in names.items():
            if name in body:
                add(name, kind, path)
    for name, kind in names.items():
        reg.setdefault(name, {"kind": kind, "files": []})
    return reg


# ----------------------------------------------------- returning production

def returning_production(team_list):
    """Phase 3's structured returning-starter counts, unchanged."""
    out = {}
    for t in team_list:
        rs = t.get("returning_starters") or {}
        out[t["team"]] = {
            "total": (rs.get("total") or {}).get("value"),
            "offense": (rs.get("offense") or {}).get("value"),
            "defense": (rs.get("defense") or {}).get("value"),
            "returning_qb": (rs.get("offense") or {}).get("returning_qb"),
            "pages": t["pages"],
            "conference": t["conference"],
        }
    return out


# Thresholds Makinen states on pp. 40-44 and applies on pp. 22-27. These are
# the guide's own cut points, quoted here so a team can be looked up against
# them. No score is computed and no team is ranked.
STABILITY_THRESHOLDS = [
    (lambda r: (r["total"] or 0) >= 17,
     "17+ total returning starters — the strongest stability component "
     "(108-86 ATS, 55.7% since 2021, first four weeks)"),
    (lambda r: (r["total"] or 99) <= 7,
     "0–7 total returning starters — a decline trigger "
     "(40-41 ATS, 49.4% since 2021, first four weeks)"),
    (lambda r: (r["offense"] or 0) >= 9 and bool(r["returning_qb"]),
     "9+ returning offensive starters including the quarterback — the "
     "transition system Makinen applies to Texas and South Carolina"),
    (lambda r: (r["offense"] or 99) <= 4,
     "4 or fewer returning offensive starters — a decline trigger"),
]


def stability_notes(rec):
    return [note for test, note in STABILITY_THRESHOLDS if test(rec)]


# ----------------------------------------------------------------- schedule

def schedule_rows(team_list):
    """Phase 3's 1,657 scheduled games, unchanged."""
    out = []
    for t in team_list:
        for g in (t.get("schedule") or []):
            out.append({
                "team": t["team"],
                "conference": t["conference"],
                "date": g.get("date"),
                "opponent": g.get("opponent"),
                "opponent_raw": g.get("opponent_raw"),
                "location": g.get("location"),
                "projected_line": g.get("projected_line"),
                "opponent_power_rating": g.get("opponent_power_rating"),
            })
    return out


# ------------------------------------------------------------------ portal

# Portal language as the guide's own contributors use it. This finds where
# the approved library already discusses the portal; it does not decide that
# a transfer is important, which only the guide may do.
PORTAL_TERMS = re.compile(
    r"\b(transfer portal|portal(?:-heavy)?|transferred? (?:in|from|to)|"
    r"[A-Z][a-z]+ transfer|incoming transfer|outgoing transfer)\b")


def prose_only(body):
    """Strip markdown tables, headings and quote markers.

    A rendered page is mostly table. Scanning it whole matches the
    *headings* of empty fields -- every quarterback file carries a
    "Relevant portal context" row even when its value is the absence
    marker -- which would report all 138 teams as having portal material
    and quote a table fragment as evidence. Only prose is scanned.
    """
    keep = []
    for line in body.splitlines():
        t = line.strip()
        if not t or t.startswith(("|", "#", ">", "-", "*", "<!--")):
            continue
        keep.append(t)
    return " ".join(keep)


def portal_mentions(files):
    """path -> count, over the prose of approved rendered files only."""
    out = {}
    for path, body in files.items():
        n = len(PORTAL_TERMS.findall(prose_only(body)))
        if n:
            out[path] = n
    return out


def sentences_with(body, pattern, limit=3):
    """Quoted context from an approved file. Reproduced, never rewritten.

    Sentences that are only the absence marker are not context, and a
    sentence carrying it is not evidence that the guide said anything.
    """
    hits = []
    for chunk in re.split(r"(?<=[.!?])\s+", prose_only(body)):
        chunk = chunk.strip()
        if (pattern.search(chunk) and 40 < len(chunk) < 400
                and NA not in chunk):
            hits.append(chunk)
        if len(hits) >= limit:
            break
    return hits


def _verify():
    t = teams()
    if len(t) != 138:
        raise SystemExit(f"team_details: {len(t)} teams, expected 138")
    c = conferences()
    if len(c) != 11:
        raise SystemExit(f"conference_previews: {len(c)} conferences, expected 11")
    n = sum(len(x.get("schedule") or []) for x in t)
    if n != 1657:
        raise SystemExit(f"schedule: {n} games, expected 1657")


_verify()
