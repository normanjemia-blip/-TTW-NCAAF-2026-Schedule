#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 5 shared library
===========================================================

Loaders and continuity derivation for the Coaching Intelligence Database.

Everything numeric here comes from the guide as printed. The continuity
flags are not a TTW invention: Steve Makinen's Stability Score table
(pp. 41-44) awards points for a returning head coach, offensive
coordinator, defensive coordinator and quarterback, so a zero in one of
those columns *is* the guide stating that the position changed. This
library reads those columns and nothing more. It never recomputes a
Stability Score, never re-weights it, and never substitutes a TTW score.

    hc_returns  4 -> head coach returns      0 -> new head coach
    oc_returns  3 -> offensive coord returns 0 -> new offensive coordinator
    dc_returns  3 -> defensive coord returns 0 -> new defensive coordinator
    qb_returns  4 -> quarterback returns     0 -> new quarterback
    returning_starters_points 0-4, from the printed returning-starter count

All 138 rows were verified to sum to their own printed total.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NA = "Not addressed in guide."


def _load(name):
    with open(os.path.join(ROOT, "_source", "data", name)) as fh:
        return json.load(fh)


def load_teams():
    """Canonical team table: name -> record, including head coach and tenure."""
    return {t["team"]: t for t in _load("teams.json")}


def load_details():
    return {t["team"]: t for t in _load("team_details.json")}


def load_stability():
    """The printed Stability Score table, keyed by team."""
    return {r["team"]: r for r in _load("stability_scores.json")}


def load_carousel():
    """The Coaching Carousel feature, keyed by team (35 new head coaches)."""
    return {e["team"]: e for e in _load("coaching_carousel.json")}


def load_notes():
    """Authored Phase 5A coaching records, merged across _source/coaching/*.json."""
    out = {}
    d = os.path.join(ROOT, "_source", "coaching")
    if not os.path.isdir(d):
        return out
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(d, name)) as fh:
            batch = json.load(fh)
        for team, rec in batch.items():
            if team in out:
                raise SystemExit(f"duplicate coaching record for {team} in {name}")
            out[team] = rec
    return out


def continuity(team, stability, teams):
    """The guide's own continuity picture for one program.

    Returns a dict of flags plus the printed components. Nothing is
    inferred: each flag is a direct reading of a printed column.
    """
    s = stability[team]
    t = teams[team]
    return {
        "hc_returns": s["hc_returns"] != "0",
        "oc_returns": s["oc_returns"] != "0",
        "dc_returns": s["dc_returns"] != "0",
        "qb_returns": s["qb_returns"] != "0",
        "hc_points": s["hc_returns"],
        "oc_points": s["oc_returns"],
        "dc_points": s["dc_returns"],
        "qb_points": s["qb_returns"],
        "rs_points": s["returning_starters_points"],
        "rs_count": s["returning_starters_count"],
        "score": s["stability_score"],
        "record_2025": s["record_2025"],
        "page": s["page"],
        "hc_season": t["hc_season"],
        "interim": t["interim"],
        "head_coach": t["head_coach"],
    }


# ---------------------------------------------------------------------------
# Source conflicts carried into Phase 5.
#
# Every entry is a contradiction between two things the guide itself
# prints. None is corrected. The first is carried forward by explicit
# owner instruction; the rest were found by cross-checking the three
# independent places the guide states coaching status.
# ---------------------------------------------------------------------------
def _ordinal(n):
    """English ordinal. 11-13 take 'th' regardless of last digit."""
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return f"{n}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th') }"


def coaching_conflicts(teams, stability, carousel):
    out = []

    # Carried forward by instruction — found in Phase 2.
    out.append({
        "team": "Navy Midshipmen",
        "field": "head-coach tenure",
        "detail": (
            "The American preview (p. 49) says Brian Newberry “begins his "
            "fourth season at the helm”, while the team page (p. 60) prints "
            "“Brian Newberry - 5th season”. Both are reproduced as printed "
            "and neither is corrected."),
    })

    # Derived: the three places the guide states head-coach status disagree.
    for team in sorted(teams):
        t, s = teams[team], stability[team]
        first_season = t["hc_season"] == 1
        stab_new = s["hc_returns"] == "0"
        in_carousel = team in carousel
        if first_season == stab_new == in_carousel:
            continue
        parts = []
        parts.append(f"the team page prints “{t['head_coach']} - "
                     f"{_ordinal(t['hc_season'])} season”")
        parts.append("the Stability Score table (p. %s) awards %s points for a "
                     "returning head coach, so it treats the position as %s"
                     % (s["page"], s["hc_returns"],
                        "changed" if stab_new else "unchanged"))
        parts.append("the Coaching Carousel feature (pp. 28–37) %s the programme"
                     % ("lists" if in_carousel else "does not list"))
        out.append({
            "team": team,
            "field": "new / returning head coach",
            "detail": ("The guide states this three ways and they do not agree: "
                       + "; ".join(parts) + ". All three are reproduced as "
                       "printed and none is corrected."),
        })

    # Conflicts already recorded by earlier phases that bear on coaching.
    for name in ("stability_conflicts.json", "carousel_conflicts.json"):
        for c in _load(name):
            out.append(c)
    return out


def slug(team):
    import re
    s = team.lower().replace("’", "").replace("'", "").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_") + ".md"


if __name__ == "__main__":
    teams = load_teams()
    stab = load_stability()
    car = load_carousel()
    print(f"teams               {len(teams)}")
    print(f"stability rows      {len(stab)}")
    print(f"carousel entries    {len(car)}")
    n = sum(1 for t in teams if stab[t]["hc_returns"] == "0")
    print(f"stability: new HC   {n}")
    print(f"team pages: 1st yr  {sum(1 for t in teams if teams[t]['hc_season'] == 1)}")
    print()
    for c in coaching_conflicts(teams, stab, car):
        print(f"CONFLICT {c['team']}: {c['field']}")
