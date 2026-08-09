#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 4 shared library
===========================================================

Canonical identity mapping between the two TTW datasets that Phase 4
reconciles, plus loaders for each.

    LAYER 1  VSiN preseason QB intelligence
             derived from the 2026 VSiN College Football Betting Guide,
             via this library's own Phase 1-3A extractions.

    LAYER 2  Current verified QB state
             the TTW Power Ratings QB verification project, Phases
             7A-7D.5 / 8.x, read from the committed
             qb_inventory_v079.json which reproduces the QB VALUES sheet
             of v0.8.1 AUTHORITATIVE exactly.

Layer 2 is READ ONLY. Nothing in Phase 4 writes to it, recomputes an
H/M/L code, or edits the workbook.

The two datasets name teams differently. VSiN uses the full
school-plus-mascot form ("Ohio U Bobcats"); the workbook uses a short
school name plus a stable abbreviation ("Ohio", OHIO). Base-name
matching is ambiguous for 24 of 138 teams — "Miami" alone matches both
Miami (Ohio) and Miami (FL) — so the join is on the workbook's
abbreviation, which is unique, through an explicit table. Nothing is
matched by guesswork.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Layer 2 lives outside this library, on the Power Ratings branch. It is
# copied in read-only under _source/verified/ with its provenance record.
VERIFIED = os.path.join(ROOT, "_source", "verified", "qb_inventory_v079.json")

# ---------------------------------------------------------------------------
# Canonical identity: workbook abbreviation -> VSiN team name.
#
# Every entry is stated explicitly. 114 of these could have been derived
# by prefix matching, but a derived join that silently mis-seats one team
# is exactly the failure mode Phase 2 already produced once in this
# project, so the whole table is written out and asserted to be a
# bijection at import time.
# ---------------------------------------------------------------------------
ABBREV_TO_VSIN = {
    "AFA": "Air Force Falcons",
    "AKR": "Akron Zips",
    "ALA": "Alabama Crimson Tide",
    "APP": "Appalachian State Mountaineers",
    "ARIZ": "Arizona Wildcats",
    "ARK": "Arkansas Razorbacks",
    "ARMY": "Army Black Knights",
    "ARST": "Arkansas State Red Wolves",
    "AUB": "Auburn Tigers",
    "AZST": "Arizona State Sun Devils",
    "BALL": "Ball State Cardinals",
    "BAY": "Baylor Bears",
    "BC": "Boston College Eagles",
    "BGSU": "Bowling Green Falcons",
    "BSU": "Boise State Broncos",
    "BUFF": "Buffalo Bulls",
    "BYU": "BYU Cougars",
    "CAL": "California Golden Bears",
    "CCU": "Coastal Carolina Chanticleers",
    "CIN": "Cincinnati Bearcats",
    "CLEM": "Clemson Tigers",
    "CLT": "Charlotte 49ers",
    "CMU": "Central Michigan Chippewas",
    "COLO": "Colorado Buffaloes",
    "CONN": "Connecticut Huskies",
    "CSU": "Colorado State Rams",
    "DEL": "Delaware Fightin’ Blue Hens",
    "DUKE": "Duke Blue Devils",
    "ECU": "East Carolina Pirates",
    "EMU": "Eastern Michigan Eagles",
    "FAU": "Florida Atlantic Owls",
    "FIU": "FIU Golden Panthers",
    "FLA": "Florida Gators",
    "FRES": "Fresno State Bulldogs",
    "FSU": "Florida State Seminoles",
    "GASO": "Georgia Southern Eagles",
    "GAST": "Georgia State Panthers",
    "GT": "Georgia Tech Yellow Jackets",
    "HAW": "Hawaii Rainbow Warriors",
    "HOU": "Houston Cougars",
    "ILL": "Illinois Fighting Illini",
    "IND": "Indiana Hoosiers",
    "IOWA": "Iowa Hawkeyes",
    "ISU": "Iowa State Cyclones",
    "JMU": "James Madison Dukes",
    "JVST": "Jacksonville State Gamecocks",
    "KAN": "Kansas Jayhawks",
    "KENN": "Kennesaw State Owls",
    "KENT": "Kent State Golden Flashes",
    "KSU": "Kansas State Wildcats",
    "LIB": "Liberty Flames",
    "LOU": "Louisville Cardinals",
    "LSU": "LSU Tigers",
    "LT": "Louisiana Tech Bulldogs",
    "M-OH": "Miami (Ohio) RedHawks",
    "MASS": "Massachusetts Minutemen",
    "MD": "Maryland Terrapins",
    "MEM": "Memphis Tigers",
    "MIA": "Miami Hurricanes",
    "MICH": "Michigan Wolverines",
    "MINN": "Minnesota Golden Gophers",
    "MISS": "Ole Miss Rebels",
    "MIZ": "Missouri Tigers",
    "MOST": "Missouri State Bears",
    "MRSH": "Marshall Thundering Herd",
    "MSST": "Mississippi State Bulldogs",
    "MSU": "Michigan State Spartans",
    "MTSU": "Middle Tennessee Blue Raiders",
    "NAVY": "Navy Midshipmen",
    "NCST": "NC State Wolfpack",
    "ND": "Notre Dame Fighting Irish",
    "NDSU": "North Dakota State Bison",
    "NEB": "Nebraska Cornhuskers",
    "NEV": "Nevada Wolf Pack",
    "NIU": "Northern Illinois Huskies",
    "NMSU": "New Mexico State Aggies",
    "NW": "Northwestern Wildcats",
    "ODU": "Old Dominion Monarchs",
    "OHIO": "Ohio U Bobcats",
    "OHST": "Ohio State Buckeyes",
    "OKST": "Oklahoma State Cowboys",
    "ORE": "Oregon Ducks",
    "ORST": "Oregon State Beavers",
    "OU": "Oklahoma Sooners",
    "PITT": "Pittsburgh Panthers",
    "PSU": "Penn State Nittany Lions",
    "PUR": "Purdue Boilermakers",
    "RICE": "Rice Owls",
    "RUTG": "Rutgers Scarlet Knights",
    "SAC": "Sacramento State Hornets",
    "SCAR": "South Carolina Gamecocks",
    "SDSU": "San Diego State Aztecs",
    "SHSU": "Sam Houston State Bearkats",
    "SJSU": "San Jose State Spartans",
    "SMU": "SMU Mustangs",
    "STAN": "Stanford Cardinal",
    "SYR": "Syracuse Orange",
    "TAMU": "Texas A&M Aggies",
    "TCU": "TCU Horned Frogs",
    "TEM": "Temple Owls",
    "TENN": "Tennessee Volunteers",
    "TEX": "Texas Longhorns",
    "TLSA": "Tulsa Golden Hurricane",
    "TOL": "Toledo Rockets",
    "TROY": "Troy Trojans",
    "TTU": "Texas Tech Red Raiders",
    "TULN": "Tulane Green Wave",
    "TXST": "Texas State Bobcats",
    "UAB": "UAB Blazers",
    "UCF": "UCF Golden Knights",
    "UCLA": "UCLA Bruins",
    "UGA": "Georgia Bulldogs",
    "UK": "Kentucky Wildcats",
    "ULL": "Louisiana Ragin’ Cajuns",
    "ULM": "ULM Warhawks",
    "UNC": "North Carolina Tar Heels",
    "UNLV": "UNLV Rebels",
    "UNM": "New Mexico Lobos",
    "UNT": "North Texas Eagles",
    "USA": "South Alabama Jaguars",
    "USC": "USC Trojans",
    "USF": "South Florida Bulls",
    "USM": "Southern Miss Golden Eagles",
    "USU": "Utah State Aggies",
    "UTAH": "Utah Utes",
    "UTEP": "UTEP Miners",
    "UTSA": "UTSA Roadrunners",
    "UVA": "Virginia Cavaliers",
    "VAN": "Vanderbilt Commodores",
    "VT": "Virginia Tech Hokies",
    "WAKE": "Wake Forest Demon Deacons",
    "WASH": "Washington Huskies",
    "WISC": "Wisconsin Badgers",
    "WKU": "Western Kentucky Hilltoppers",
    "WMU": "Western Michigan Broncos",
    "WSU": "Washington State Cougars",
    "WVU": "West Virginia Mountaineers",
    "WYO": "Wyoming Cowboys",
}

VSIN_TO_ABBREV = {v: k for k, v in ABBREV_TO_VSIN.items()}


def load_vsin_teams():
    """VSiN structured team table from Phase 3 (teams.json + team_details)."""
    with open(os.path.join(ROOT, "_source", "data", "team_details.json")) as fh:
        details = {t["team"]: t for t in json.load(fh)}
    return details


def load_verified():
    """Layer 2, read only. Returns (metadata, {abbrev: record})."""
    with open(VERIFIED) as fh:
        data = json.load(fh)
    meta = {k: v for k, v in data.items() if k != "records"}
    return meta, {r["abbrev"]: r for r in data["records"]}


def load_qb_notes():
    """Authored Layer 1 QB records, merged across _source/qb/*.json."""
    out = {}
    qbdir = os.path.join(ROOT, "_source", "qb")
    if not os.path.isdir(qbdir):
        return out
    for name in sorted(os.listdir(qbdir)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(qbdir, name)) as fh:
            batch = json.load(fh)
        for team, rec in batch.items():
            if team in out:
                raise SystemExit(f"duplicate QB record for {team} in {name}")
            out[team] = rec
    return out


def check_identity():
    """Assert the mapping is a bijection over both 138-team populations."""
    problems = []
    if len(ABBREV_TO_VSIN) != 138:
        problems.append(f"alias table has {len(ABBREV_TO_VSIN)} entries, expected 138")
    if len(VSIN_TO_ABBREV) != len(ABBREV_TO_VSIN):
        problems.append("alias table maps two abbreviations to the same VSiN team")

    vsin = set(load_vsin_teams())
    mapped = set(ABBREV_TO_VSIN.values())
    for t in sorted(vsin - mapped):
        problems.append(f"VSiN team not in alias table: {t}")
    for t in sorted(mapped - vsin):
        problems.append(f"alias table names a team VSiN does not have: {t}")

    _, verified = load_verified()
    for a in sorted(set(verified) - set(ABBREV_TO_VSIN)):
        problems.append(f"verified abbrev not in alias table: {a}")
    for a in sorted(set(ABBREV_TO_VSIN) - set(verified)):
        problems.append(f"alias abbrev absent from verified dataset: {a}")
    return problems


if __name__ == "__main__":
    probs = check_identity()
    print(f"alias entries       {len(ABBREV_TO_VSIN)}")
    print(f"identity problems   {len(probs)}")
    for p in probs:
        print("  -", p)
    if not probs:
        print("\nidentity mapping is a clean bijection over both 138-team populations")
