#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 9 shared library
============================================================

Loaders and identity for the Betting Concepts layer.

Phase 1 built a concept-to-page map and deliberately stopped there,
recording *where* each concept appears and writing no definitions. This
phase writes the entries, and the reason Phase 1 held back is the same
reason the schema below is shaped the way it is: **the guide uses far
more vocabulary than it defines.**

Only 45 terms are glossed anywhere in the guide, all on p. 2. Everything
else -- tempo, regression, explosiveness, situational betting -- is used
constantly and never defined. So each entry keeps three things apart:

  guide_definition    What the guide itself says the term means. Usually
                      the p. 2 gloss, and often `Not addressed in guide.`

  guide_usage         How the guide actually deploys the concept, with
                      pages. GUIDE CONTENT.

  working_definition  What the term means, supplied by this library where
                      the guide supplies nothing. TTW DERIVED, labelled in
                      place and never blended into a guide sentence.

The two concepts Phase 1 singled out -- Closing Line Value and Conference
Strength, one page each -- are the test of whether this phase behaved.
Both are well known outside the guide and neither is developed inside it,
so both must carry the sentinel rather than a textbook paragraph.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "_source", "data")

NA = "Not addressed in guide."

# Phase 1 flagged these as present in the project brief but effectively
# absent from the guide. They may never be filled from outside knowledge.
BARELY_COVERED = {"Closing Line Value", "Conference Strength"}

# Which library directory owns the detailed treatment of a concept, where
# one exists. A concept entry explains the idea; the owning database holds
# the data.
OWNED_BY = {
    "Power Ratings": ("05_Power_Ratings", "00_MAKINEN_RATINGS.md"),
    "Quarterback Play": ("04_Quarterback_Database", "README.md"),
    "Win Totals": ("06_Win_Totals", "README.md"),
    "Futures": ("07_Futures", "README.md"),
    "CFP / Playoff": ("07_Futures", "00_BEST_BETS.md"),
    "Heisman": ("07_Futures", "00_HEISMAN.md"),
    "Coaching Carousel": ("03_Coaching_Database", "README.md"),
    "Coaching Continuity": ("03_Coaching_Database", "00_CONTINUITY_MATRIX.md"),
    "Transfer Portal": ("02_Team_Database", "README.md"),
    "Returning Production": ("02_Team_Database", "README.md"),
    "Roster Continuity": ("02_Team_Database", "README.md"),
    "Schedule Difficulty": ("01_Conference_Database", "00_CONFERENCE_INDEX.md"),
    "Recruiting": ("03_Coaching_Database", "README.md"),
}

# Concepts whose material belongs in 13_Situational_Angles. The directory's
# standing decision splits it: conceptual material is Phase 9, historical or
# system-based material is Phase 10. That line is drawn here.
SITUATIONAL = ["Situational Betting", "Travel", "Weather",
               "Home-Field Advantage", "Injuries"]

# Concepts that are statistical categories in the team tables.
STATISTICAL = ["Yards Per Play", "Turnover Margin", "Tempo", "Explosiveness",
               "Success Rate", "EPA"]


def _load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


def load_concept_pages():
    """Phase 1's concept-to-page map: 29 concepts scanned across 345 pages."""
    return _load("concept_pages.json")


def load_abbreviations():
    """The guide's only glossary, p. 2. 45 entries, reproduced as printed."""
    return _load("abbreviations.json")


def load_stat_schema():
    """15 offensive and 12 defensive categories, verified across 138 teams."""
    return (_load("offensive_stat_categories.json"),
            _load("defensive_stat_categories.json"))


def load_team_stats():
    """Phase 3's resolved values and national ranks, all 138 teams.

    The 14_Statistics_Reference README long said these were 'blocked on
    coordinate-based extraction'. Phase 3 resolved them; that status line
    is stale and is corrected by this phase.
    """
    out = {}
    for t in _load("team_details.json"):
        out[t["team"]] = {"stats": t["statistics"], "pages": t["pages"],
                          "conference": t["conference"]}
    return out


def load_entries():
    """Authored Phase 9 concept entries, merged across _source/concepts/*.json."""
    out = {}
    d = os.path.join(ROOT, "_source", "concepts")
    if not os.path.isdir(d):
        return out
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(d, name)) as fh:
            batch = json.load(fh)
        for key, rec in batch.items():
            if key in out:
                raise SystemExit(f"duplicate concept entry {key!r} in {name}")
            out[key] = rec
    return out


def page_summary(pages, n=12):
    """Locations, not emphasis.

    A concept on 287 pages is usually woven through the 138 team tables
    rather than discussed 287 times, so the count is always reported as
    'appears on N pages' and never as a measure of how much the guide has
    to say about it.
    """
    shown = ", ".join(str(p) for p in pages[:n])
    more = f" … (+{len(pages) - n} more)" if len(pages) > n else ""
    return f"{shown}{more}"


def abbrev_index():
    """abbreviation -> meaning, exactly as printed on p. 2."""
    return {a["abbr"]: a["meaning"] for a in load_abbreviations()}


def leaders(stats, side, category, n=5, best_is_low=False):
    """TTW DERIVED. Rank order over values the guide prints.

    Uses the guide's own printed national rank rather than re-deriving one,
    so this is a lookup over guide figures, not a new rating.
    """
    rows = []
    for team, v in stats.items():
        for row in v["stats"].get(side, []):
            if row["category"] == category and row.get("rank"):
                try:
                    rows.append((int(row["rank"]), team, row["value"]))
                except ValueError:
                    pass
    rows.sort()
    return rows[:n]


def _verify():
    pages = load_concept_pages()
    if len(pages) != 29:
        raise SystemExit(f"concept map: {len(pages)} concepts, expected 29")
    missing = BARELY_COVERED - set(pages)
    if missing:
        raise SystemExit(f"barely-covered concepts absent from map: {missing}")
    unknown = set(OWNED_BY) - set(pages)
    if unknown:
        raise SystemExit(f"OWNED_BY names concepts not in the map: {unknown}")
    for group in (SITUATIONAL, STATISTICAL):
        unknown = set(group) - set(pages)
        if unknown:
            raise SystemExit(f"grouping names concepts not in the map: {unknown}")


_verify()
