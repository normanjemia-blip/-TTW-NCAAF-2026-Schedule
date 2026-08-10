#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 8 shared library
============================================================

Loaders and the identity joins for the Futures layer.

The guide states a futures position in four separate places, and Phase 8
keeps them apart rather than collapsing them into "the guide likes":

  PREDICTIONS   p. 4. A 17-category grid in which each of 22 named
                contributors picks a winner. No price, no reasoning --
                just a name in a box. 374 attributed cells.

  BEST BETS     pp. 5-15. 62 priced recommendations by 20 contributors,
                each with an argument. These are bets people are making.

  HEISMAN       p. 39. Zach Cohen's four priced player picks.

  TEAM PRICES   Each team's right-hand page: CFP Championship, make the
                playoff, and the conference title. 414 markets, 412
                printed prices.

A contributor picking Miami on p. 4 while betting Notre Dame on p. 9 is
not a contradiction to fix. It is two different questions, and both are
recorded.

Every team identity here is an enumerated bijection asserted at import.
Nothing is matched by prefix, substring or fuzz: "Miami" and "Miami (OH)"
are different programmes, and so are Georgia, Georgia Southern, Georgia
State and Georgia Tech.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "_source", "data")

NA = "Not addressed in guide."


def _load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


# --------------------------------------------------------------- identity

# p. 4 prints short programme names. 45 of the 49 distinct cell values are
# college teams; the other four are NFL clubs printed in the anomaly row.
PRED_TO_TEAM = {
    "Air Force": "Air Force Falcons",
    "Alabama": "Alabama Crimson Tide",
    "Arkansas State": "Arkansas State Red Wolves",
    "BYU": "BYU Cougars",
    "Boise State": "Boise State Broncos",
    "Clemson": "Clemson Tigers",
    "Delaware": "Delaware Fightin’ Blue Hens",
    "East Carolina": "East Carolina Pirates",
    "Fresno State": "Fresno State Bulldogs",
    "Georgia": "Georgia Bulldogs",
    "Hawaii": "Hawaii Rainbow Warriors",
    "Indiana": "Indiana Hoosiers",
    "Jacksonville State": "Jacksonville State Gamecocks",
    "James Madison": "James Madison Dukes",
    "Kansas State": "Kansas State Wildcats",
    "LSU": "LSU Tigers",
    "Liberty": "Liberty Flames",
    "Louisville": "Louisville Cardinals",
    "Marshall": "Marshall Thundering Herd",
    "Memphis": "Memphis Tigers",
    "Miami": "Miami Hurricanes",
    "Miami (OH)": "Miami (Ohio) RedHawks",
    "Navy": "Navy Midshipmen",
    "New Mexico": "New Mexico Lobos",
    "North Dakota State": "North Dakota State Bison",
    "Notre Dame": "Notre Dame Fighting Irish",
    "Ohio State": "Ohio State Buckeyes",
    "Old Dominion": "Old Dominion Monarchs",
    "Oregon": "Oregon Ducks",
    "Penn State": "Penn State Nittany Lions",
    "SMU": "SMU Mustangs",
    "San Diego State": "San Diego State Aztecs",
    "South Florida": "South Florida Bulls",
    "Texas": "Texas Longhorns",
    "Texas A&M": "Texas A&M Aggies",
    "Texas State": "Texas State Bobcats",
    "Texas Tech": "Texas Tech Red Raiders",
    "Toledo": "Toledo Rockets",
    "Troy": "Troy Trojans",
    "UMass": "Massachusetts Minutemen",
    "UNLV": "UNLV Rebels",
    "UTSA": "UTSA Roadrunners",
    "Virginia Tech": "Virginia Tech Hokies",
    "Western Kentucky": "Western Kentucky Hilltoppers",
    "Western Michigan": "Western Michigan Broncos",
}

# The SUN BELT CHAMP row prints NFL clubs. They are never mapped to a
# college programme; they are reproduced as printed and flagged.
NFL_ANOMALY = {"Bucs", "Falcons", "Panthers", "Saints"}

# Leading team token of a best-bet headline. Longest match wins, so
# "NORTH TEXAS" is tested before "TEXAS" and "TEXAS TECH" before "TEXAS".
BET_TO_TEAM = {
    "AIR FORCE": "Air Force Falcons",
    "APPALACHIAN STATE": "Appalachian State Mountaineers",
    "ARKANSAS": "Arkansas Razorbacks",
    "AUBURN": "Auburn Tigers",
    "BOISE STATE": "Boise State Broncos",
    "BYU": "BYU Cougars",
    "CLEMSON": "Clemson Tigers",
    "FLORIDA STATE": "Florida State Seminoles",
    "FRESNO STATE": "Fresno State Bulldogs",
    "GEORGIA": "Georgia Bulldogs",
    "GEORGIA SOUTHERN": "Georgia Southern Eagles",
    "HAWAII": "Hawaii Rainbow Warriors",
    "HOUSTON": "Houston Cougars",
    "INDIANA": "Indiana Hoosiers",
    "IOWA": "Iowa Hawkeyes",
    "KENTUCKY": "Kentucky Wildcats",
    "LSU": "LSU Tigers",
    "MIAMI (FL)": "Miami Hurricanes",
    "MICHIGAN": "Michigan Wolverines",
    "NC STATE": "NC State Wolfpack",
    "NEW MEXICO": "New Mexico Lobos",
    "NORTH DAKOTA STATE": "North Dakota State Bison",
    "NORTH TEXAS": "North Texas Eagles",
    "OKLAHOMA STATE": "Oklahoma State Cowboys",
    "OLE MISS": "Ole Miss Rebels",
    "OREGON": "Oregon Ducks",
    "PENN STATE": "Penn State Nittany Lions",
    "RUTGERS": "Rutgers Scarlet Knights",
    "SMU": "SMU Mustangs",
    "SOUTHERN MISS": "Southern Miss Golden Eagles",
    "TEXAS": "Texas Longhorns",
    "TEXAS A&M": "Texas A&M Aggies",
    "TEXAS TECH": "Texas Tech Red Raiders",
    "TOLEDO": "Toledo Rockets",
    "UCLA": "UCLA Bruins",
    "UNLV": "UNLV Rebels",
    "VIRGINIA TECH": "Virginia Tech Hokies",
    "WISCONSIN": "Wisconsin Badgers",
}

# Headlines naming a player rather than a team. Each programme below is the
# one the guide's own argument names for that player, read out of the pick's
# reasoning rather than assumed: Mensah "the Miami Hurricanes", Sagapolutele
# "the starting QB at Cal", Stockton "the Georgia signal-caller". Kienholz is
# the one that punishes assumption -- he spent three seasons at Ohio State and
# the pick is explicitly about his transfer TO Louisville, under Jeff Brohm.
PLAYER_MARKETS = {
    "DARIAN MENSAH": ("Darian Mensah", "Miami Hurricanes"),
    "JARON-KEAWE SAGAPOLUTELE": ("Jaron-Keawe Sagapolutele",
                                 "California Golden Bears"),
    "GUNNER STOCKTON": ("Gunner Stockton", "Georgia Bulldogs"),
    "LINCOLN KIENHOLZ": ("Lincoln Kienholz", "Louisville Cardinals"),
}

# One headline is a three-team parlay and resolves to no single team.
PARLAY_PREFIX = "PARLAY:"

# `.title()` mangles interior capitals, so contributor names printed in
# caps are mapped explicitly rather than case-folded.
CONTRIBUTOR_FIX = {
    "John Mckechnie": "John McKechnie",
}


def canonical_contributor(name):
    return CONTRIBUTOR_FIX.get(name, name)


def resolve_prediction(cell):
    """Canonical team for a p. 4 cell, or None for the NFL anomaly row."""
    if cell in NFL_ANOMALY:
        return None
    return PRED_TO_TEAM[cell]


_BET_KEYS = sorted(BET_TO_TEAM, key=len, reverse=True)
_PLAYER_KEYS = sorted(PLAYER_MARKETS, key=len, reverse=True)


def resolve_bet(headline):
    """(team, player) for a best-bet headline; either may be None.

    Longest-prefix match against the enumerated table -- never a substring
    scan, which would find "TEXAS" inside "NORTH TEXAS" and "TEXAS TECH".
    """
    h = headline.upper().strip()
    if h.startswith(PARLAY_PREFIX):
        return None, None
    for k in _PLAYER_KEYS:
        if h.startswith(k):
            player, team = PLAYER_MARKETS[k]
            return team, player
    for k in _BET_KEYS:
        if h.startswith(k + " ") or h == k:
            return BET_TO_TEAM[k], None
    return None, None


# ----------------------------------------------------------------- market

MARKETS = (
    ("Heisman", re.compile(r"HEISMAN", re.I)),
    ("National championship", re.compile(r"NATIONAL CHAMPIONSHIP", re.I)),
    ("College Football Playoff", re.compile(r"COLLEGE FOOTBALL PLAYOFF", re.I)),
    ("Conference title game", re.compile(
        r"(?:CHAMPIONSHIP|TITLE) GAME|TO REACH", re.I)),
    ("Conference championship", re.compile(
        r"TO WIN (?:THE )?(?:SEC|BIG TEN|BIG 12|ACC|PAC-12|MAC|MOUNTAIN WEST"
        r"|SUN BELT|AMERICAN|CONFERENCE USA)", re.I)),
    ("Conference wins", re.compile(r"CONFERENCE WINS", re.I)),
    ("Season win total", re.compile(r"\b(?:OVER|UNDER)\b.*\bWINS\b", re.I)),
    ("Pointspread", re.compile(r"\s[+-]\d+(?:\.\d)?\s+VS\.", re.I)),
)


def classify(headline):
    """The market a best-bet headline is in. First match wins, and the
    order above matters: 'PENN STATE OVER 8.5 WINS & TO MAKE COLLEGE
    FOOTBALL PLAYOFF' is filed under the playoff leg it is priced on."""
    if headline.upper().startswith(PARLAY_PREFIX):
        return "Parlay"
    for name, pat in MARKETS:
        if pat.search(headline):
            return name
    return "Other"


# ---------------------------------------------------------------- loaders

def load_predictions():
    p = _load("futures_predictions.json")
    real = [c for c in p["categories"] if "anomaly" not in c]
    anomalies = [c for c in p["categories"] if "anomaly" in c]
    for c in p["categories"]:
        for k in c["picks"]:
            k["contributor"] = canonical_contributor(k["contributor"])
    return p, real, anomalies


def load_best_bets():
    b = _load("futures_best_bets.json")
    for x in b["bets"]:
        x["contributor"] = canonical_contributor(x["contributor"])
        x["team"], x["player"] = resolve_bet(x["headline"])
        x["market"] = classify(x["headline"])
    b["roster"] = [canonical_contributor(n) for n in b["roster"]]
    return b


def load_heisman():
    return _load("futures_heisman.json")


def load_team_prices():
    return _load("futures_team_prices.json")


def load_notes():
    """Authored Phase 8 reference notes, merged across _source/futures/*.json."""
    out = {}
    d = os.path.join(ROOT, "_source", "futures")
    if not os.path.isdir(d):
        return out
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(d, name)) as fh:
            batch = json.load(fh)
        for key, rec in batch.items():
            if key in out:
                raise SystemExit(f"duplicate futures note {key!r} in {name}")
            out[key] = rec
    return out


def bet_key(bet):
    """Stable identifier for a best bet: contributor plus headline."""
    return f"{bet['contributor']}|{bet['headline']}"


def consensus(category_picks):
    """TTW DERIVED. How many of the 22 named a given team.

    A count of printed cells and nothing more. It is not a probability, not
    a confidence grade, and not evidence that the majority is right.
    """
    tally = {}
    for k in category_picks:
        tally[k["pick"]] = tally.get(k["pick"], 0) + 1
    return sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))


def _verify():
    teams = {t["team"] for t in _load("teams.json")}
    unknown = sorted(set(PRED_TO_TEAM.values()) - teams)
    if unknown:
        raise SystemExit(f"PRED_TO_TEAM: not canonical team names: {unknown}")
    unknown = sorted(set(BET_TO_TEAM.values()) - teams)
    if unknown:
        raise SystemExit(f"BET_TO_TEAM: not canonical team names: {unknown}")
    unknown = sorted({team for _, team in PLAYER_MARKETS.values()} - teams)
    if unknown:
        raise SystemExit(f"PLAYER_MARKETS: not canonical team names: {unknown}")
    cells = {k["pick"] for c in _load("futures_predictions.json")["categories"]
             for k in c["picks"]}
    missing = sorted(cells - set(PRED_TO_TEAM) - NFL_ANOMALY)
    if missing:
        raise SystemExit(f"p.4 cells with no canonical mapping: {missing}")


_verify()
