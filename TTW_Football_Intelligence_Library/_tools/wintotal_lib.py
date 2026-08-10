#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 7 shared library
============================================================

Loaders and the join for the Win Totals layer.

The guide states a win total three separate ways, and Phase 7 keeps all
three apart rather than collapsing them into one "the guide says":

  CONFERENCE TABLE   Every conference preview prints, per team, the
                     DraftKings win total, Makinen's power rating, home and
                     road field ratings, schedule strength with national
                     rank, and his projected overall and conference records.
                     All 138 teams. Author: the conference preview's author.

  TEAM PAGE          Each team's left-hand page carries a standalone
                     recommendation, printed as "Over 7.5" or "Under 7.5".
                     All 138 teams.

  FEATURE            pp. 22-27, Steve Makinen, "2026 college football win
                     totals I'm betting now" — 29 bets he is actually
                     making, with an argument for each.

These disagree with one another in places. That is content, not error, and
none of it is reconciled here.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NA = "Not addressed in guide."


def _load(name):
    with open(os.path.join(ROOT, "_source", "data", name)) as fh:
        return json.load(fh)


def load_conference_rows():
    """The conference-table layer: 138 rows, one per team."""
    out = {}
    for conf in _load("conference_previews.json"):
        for row in conf["standings"]:
            out[row["team"]] = dict(row, preview_page=conf["preview_page"],
                                    preview_author=conf.get("author"))
    if len(out) != 138:
        raise SystemExit(f"conference rows: {len(out)}")
    return out


def load_team_picks():
    """The team-page layer: the standalone Over/Under line, 138 teams."""
    out = {}
    for t in _load("team_details.json"):
        out[t["team"]] = {"pick": t.get("win_total_pick"),
                          "projected_wins": t.get("projected_wins"),
                          "pages": t["pages"], "conference": t["conference"]}
    return out


def load_feature():
    """The pp. 22-27 layer: Makinen's 29 bets."""
    f = _load("wintotals_feature.json")
    return f, {e["team"]: e for e in f["entries"]}


def load_notes():
    """Authored Phase 7 reference notes, merged across _source/wintotals/*.json."""
    out = {}
    d = os.path.join(ROOT, "_source", "wintotals")
    if not os.path.isdir(d):
        return out
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(d, name)) as fh:
            batch = json.load(fh)
        for team, rec in batch.items():
            if team in out:
                raise SystemExit(f"duplicate win-total note for {team} in {name}")
            out[team] = rec
    return out


def implied_side(proj_wins, total):
    """Which side the guide's own projected-wins figure implies.

    Reported, never used to overrule a printed recommendation. A projection
    of 8.04 against a total of 7.5 implies Over; if the printed pick is
    Under, that is a disagreement inside the guide and is recorded as one.
    """
    try:
        return "OVER" if float(proj_wins) > float(total) else "UNDER"
    except (TypeError, ValueError):
        return None


def margin(proj_wins, total):
    try:
        return float(proj_wins) - float(total)
    except (TypeError, ValueError):
        return None
