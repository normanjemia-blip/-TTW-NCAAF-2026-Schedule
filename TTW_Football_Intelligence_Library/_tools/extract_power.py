#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 6 extraction
=======================================================

Two independent reads, deliberately kept apart so they can be compared:

  1. p. 47, Steve Makinen's printed master ratings table (138 rows).
  2. The right-hand team pages, already extracted in Phase 3 and stored in
     team_details.json.

The guide prints every rating twice. That is a gift: cross-checking the two
lists is the only way to catch a transcription error in either, and any
disagreement is a source conflict to preserve rather than a number to
choose between.

Outputs
    _source/data/makinen_ratings_p47.json
    _source/data/power_rating_conflicts.json

Usage:  python3 _tools/extract_power.py
"""

import json
import os
import re
import sys

import pymupdf

from coach_lib import load_details

PDF = "_source/2026-VSiN-CFB-Betting-Guide.pdf"
PAGE = 47  # 1-based, as printed

# The master table prints short all-caps names. Every one of the 138 is
# stated explicitly rather than matched by prefix: base-name matching is
# ambiguous here (MIAMI, OHIO, SAN JOSE STATE all collide with something),
# and a derived join that mis-seats one team is exactly the failure this
# whole cross-check exists to catch.
P47_TO_TEAM = {
    "AIR FORCE": "Air Force Falcons", "AKRON": "Akron Zips",
    "ALABAMA": "Alabama Crimson Tide",
    "APPALACHIAN STATE": "Appalachian State Mountaineers",
    "ARIZONA": "Arizona Wildcats", "ARIZONA STATE": "Arizona State Sun Devils",
    "ARKANSAS": "Arkansas Razorbacks",
    "ARKANSAS STATE": "Arkansas State Red Wolves",
    "ARMY": "Army Black Knights", "AUBURN": "Auburn Tigers",
    "BALL STATE": "Ball State Cardinals", "BAYLOR": "Baylor Bears",
    "BOISE STATE": "Boise State Broncos",
    "BOSTON COLLEGE": "Boston College Eagles",
    "BOWLING GREEN": "Bowling Green Falcons", "BUFFALO": "Buffalo Bulls",
    "BYU": "BYU Cougars", "CENTRAL MICHIGAN": "Central Michigan Chippewas",
    "CALIFORNIA": "California Golden Bears", "CHARLOTTE": "Charlotte 49ers",
    "CINCINNATI": "Cincinnati Bearcats", "CLEMSON": "Clemson Tigers",
    "COASTAL CAROLINA": "Coastal Carolina Chanticleers",
    "COLORADO": "Colorado Buffaloes", "COLORADO STATE": "Colorado State Rams",
    "CONNECTICUT": "Connecticut Huskies", "DELAWARE": "Delaware Fightin’ Blue Hens",
    "DUKE": "Duke Blue Devils", "EAST CAROLINA": "East Carolina Pirates",
    "EASTERN MICHIGAN": "Eastern Michigan Eagles",
    "FLORIDA": "Florida Gators", "FLORIDA ATLANTIC": "Florida Atlantic Owls",
    "FLORIDA INTERNATIONAL": "FIU Golden Panthers", "FLORIDA STATE": "Florida State Seminoles",
    "FRESNO STATE": "Fresno State Bulldogs", "GEORGIA": "Georgia Bulldogs",
    "GEORGIA SOUTHERN": "Georgia Southern Eagles",
    "GEORGIA STATE": "Georgia State Panthers",
    "GEORGIA TECH": "Georgia Tech Yellow Jackets",
    "HAWAII": "Hawaii Rainbow Warriors", "HOUSTON": "Houston Cougars",
    "ILLINOIS": "Illinois Fighting Illini", "INDIANA": "Indiana Hoosiers",
    "IOWA": "Iowa Hawkeyes", "IOWA STATE": "Iowa State Cyclones",
    "JACKSONVILLE STATE": "Jacksonville State Gamecocks",
    "JAMES MADISON": "James Madison Dukes", "KANSAS": "Kansas Jayhawks",
    "KANSAS STATE": "Kansas State Wildcats", "KENNESAW STATE": "Kennesaw State Owls",
    "KENT STATE": "Kent State Golden Flashes", "KENTUCKY": "Kentucky Wildcats",
    "LOUISIANA": "Louisiana Ragin’ Cajuns", "LOUISIANA TECH": "Louisiana Tech Bulldogs",
    "LIBERTY": "Liberty Flames", "LOUISVILLE": "Louisville Cardinals", "LSU": "LSU Tigers",
    "MARSHALL": "Marshall Thundering Herd", "MARYLAND": "Maryland Terrapins",
    "MASSACHUSETTS": "Massachusetts Minutemen", "MEMPHIS": "Memphis Tigers",
    "MIAMI": "Miami Hurricanes", "MIAMI OHIO": "Miami (Ohio) RedHawks",
    "MICHIGAN": "Michigan Wolverines", "MICHIGAN STATE": "Michigan State Spartans",
    "MIDDLE TENNESSEE STATE": "Middle Tennessee Blue Raiders",
    "MINNESOTA": "Minnesota Golden Gophers",
    "OLE MISS": "Ole Miss Rebels", "MISSISSIPPI STATE": "Mississippi State Bulldogs",
    "MISSOURI": "Missouri Tigers", "MISSOURI STATE": "Missouri State Bears",
    "NAVY": "Navy Midshipmen", "NORTH CAROLINA STATE": "NC State Wolfpack",
    "NEBRASKA": "Nebraska Cornhuskers", "NEVADA": "Nevada Wolf Pack",
    "NEW MEXICO": "New Mexico Lobos", "NEW MEXICO STATE": "New Mexico State Aggies",
    "NORTH CAROLINA": "North Carolina Tar Heels",
    "NORTH DAKOTA STATE": "North Dakota State Bison",
    "NORTH TEXAS": "North Texas Eagles",
    "NORTHERN ILLINOIS": "Northern Illinois Huskies",
    "NORTHWESTERN": "Northwestern Wildcats", "NOTRE DAME": "Notre Dame Fighting Irish",
    "OHIO U": "Ohio U Bobcats", "OHIO STATE": "Ohio State Buckeyes",
    "OKLAHOMA": "Oklahoma Sooners", "OKLAHOMA STATE": "Oklahoma State Cowboys",
    "OLD DOMINION": "Old Dominion Monarchs", "OREGON": "Oregon Ducks",
    "OREGON STATE": "Oregon State Beavers", "PENN STATE": "Penn State Nittany Lions",
    "PITTSBURGH": "Pittsburgh Panthers", "PURDUE": "Purdue Boilermakers",
    "RICE": "Rice Owls", "RUTGERS": "Rutgers Scarlet Knights",
    "SACRAMENTO STATE": "Sacramento State Hornets",
    "SAM HOUSTON STATE": "Sam Houston State Bearkats",
    "SAN DIEGO STATE": "San Diego State Aztecs",
    "SAN JOSE STATE": "San Jose State Spartans", "SMU": "SMU Mustangs",
    "SOUTH ALABAMA": "South Alabama Jaguars",
    "SOUTH CAROLINA": "South Carolina Gamecocks",
    "SOUTH FLORIDA": "South Florida Bulls",
    "SOUTHERN MISS": "Southern Miss Golden Eagles",
    "STANFORD": "Stanford Cardinal", "SYRACUSE": "Syracuse Orange",
    "TCU": "TCU Horned Frogs", "TEMPLE": "Temple Owls",
    "TENNESSEE": "Tennessee Volunteers", "TEXAS": "Texas Longhorns",
    "TEXAS A&M": "Texas A&M Aggies", "TEXAS STATE": "Texas State Bobcats",
    "TEXAS TECH": "Texas Tech Red Raiders", "TOLEDO": "Toledo Rockets",
    "TROY": "Troy Trojans", "TULANE": "Tulane Green Wave",
    "TULSA": "Tulsa Golden Hurricane", "UAB": "UAB Blazers",
    "UCF": "UCF Golden Knights", "UCLA": "UCLA Bruins",
    "LOUISIANA-MONROE": "ULM Warhawks", "UNLV": "UNLV Rebels",
    "USC": "USC Trojans", "UTAH": "Utah Utes", "UTAH STATE": "Utah State Aggies",
    "UTEP": "UTEP Miners", "UTSA": "UTSA Roadrunners",
    "VANDERBILT": "Vanderbilt Commodores", "VIRGINIA": "Virginia Cavaliers",
    "VIRGINIA TECH": "Virginia Tech Hokies", "WAKE FOREST": "Wake Forest Demon Deacons",
    "WASHINGTON": "Washington Huskies", "WASHINGTON STATE": "Washington State Cougars",
    "WEST VIRGINIA": "West Virginia Mountaineers",
    "WESTERN KENTUCKY": "Western Kentucky Hilltoppers",
    "WESTERN MICHIGAN": "Western Michigan Broncos", "WISCONSIN": "Wisconsin Badgers",
    "WYOMING": "Wyoming Cowboys",
}

NUM = re.compile(r"^\d{1,2}(?:\.\d)?$")


def parse_p47():
    doc = pymupdf.open(PDF)
    lines = [x.strip() for x in doc[PAGE - 1].get_text().split("\n") if x.strip()]
    # Everything after the column headers is a strict name/number alternation.
    start = lines.index("POWER RATING") + 1
    out, i = {}, start
    unmapped = []
    while i < len(lines) - 1:
        name, val = lines[i], lines[i + 1]
        if NUM.match(val) and not NUM.match(name):
            if name in P47_TO_TEAM:
                out[P47_TO_TEAM[name]] = float(val)
            else:
                unmapped.append(name)
            i += 2
        else:
            i += 1
    return out, unmapped


def main():
    p47, unmapped = parse_p47()
    details = load_details()

    if unmapped:
        sys.exit(f"unmapped p.47 names: {unmapped}")
    assert len(P47_TO_TEAM) == 138, len(P47_TO_TEAM)
    assert len(set(P47_TO_TEAM.values())) == 138, "p.47 map is not a bijection"
    missing = sorted(set(details) - set(p47))
    if missing:
        sys.exit(f"p.47 table missing {len(missing)} teams: {missing[:5]}")

    conflicts = []
    rows = []
    for team in sorted(details):
        page_val = details[team].get("power_rating")
        page_val = float(page_val) if page_val not in (None, "") else None
        table_val = p47[team]
        agree = page_val is not None and abs(page_val - table_val) < 1e-9
        rows.append({"team": team, "conference": details[team]["conference"],
                     "p47_rating": table_val, "team_page_rating": page_val,
                     "team_pages": details[team]["pages"], "agree": agree})
        if not agree:
            conflicts.append({
                "team": team, "field": "power rating",
                "detail": (f"The master ratings table (p. 47) prints "
                           f"{table_val:g}, while the team page "
                           f"(p. {details[team]['pages'][1]}) prints "
                           f"{'nothing' if page_val is None else format(page_val, 'g')}. "
                           f"Both are reproduced as printed and neither is "
                           f"corrected.")})

    with open("_source/data/makinen_ratings_p47.json", "w") as fh:
        json.dump(rows, fh, indent=1, ensure_ascii=False)
    with open("_source/data/power_rating_conflicts.json", "w") as fh:
        json.dump(conflicts, fh, indent=1, ensure_ascii=False)

    vals = [r["p47_rating"] for r in rows]
    print(f"p.47 master table   {len(rows)} teams")
    print(f"agree with team page {sum(1 for r in rows if r['agree'])}/138")
    print(f"conflicts            {len(conflicts)}")
    print(f"range                {min(vals):g} to {max(vals):g}")


if __name__ == "__main__":
    main()
