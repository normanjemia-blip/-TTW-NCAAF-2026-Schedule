#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 7 extraction
=======================================================

Steve Makinen's win-total feature, pp. 22-27: "2026 college football win
totals I'm betting now". Twenty-nine bets, fourteen Overs and fifteen
Unders, each with its own argument.

Two things this extractor does that the Phase 2 pass did not:

  * It keeps each entry's **page**, so provenance survives to the rendered
    record rather than being attributed to the whole 22-27 range.
  * It keeps each entry's **prose**, so Phase 7 can author reference notes
    from the argument rather than from the heading alone.

It also re-derives the pick list from the page text rather than trusting
the stored Phase 2 file, which is how the Memphis / South Florida / UTSA
defect in that file came to light.

Outputs
    _source/data/wintotals_feature.json

Usage:  python3 _tools/extract_wintotals.py
"""

import json
import os
import re
import sys

import pymupdf

from coach_lib import load_details

PDF = "_source/2026-VSiN-CFB-Betting-Guide.pdf"
FIRST, LAST = 22, 27          # 1-based, as printed

HEADING = re.compile(
    r"([A-Z][A-Z&'.\- ]{2,30}?)\s*[–-]\s*\n?\s*(OVER|UNDER)\s+([0-9]+\.[05])\s+WINS")

# The feature prints short all-caps names. Every one is stated explicitly
# rather than resolved by fuzzy match — the defect this phase found in the
# Phase 2 artefact was a resolution failure, and the fix is not a better
# heuristic but an enumerated table that a human can check against p. 22-27.
FEATURE_TO_TEAM = {
    "BOISE STATE": "Boise State Broncos",
    "FRESNO STATE": "Fresno State Bulldogs",
    "FLORIDA ATLANTIC": "Florida Atlantic Owls",
    "HOUSTON": "Houston Cougars",
    "ILLINOIS": "Illinois Fighting Illini",
    "KANSAS STATE": "Kansas State Wildcats",
    "SOUTH ALABAMA": "South Alabama Jaguars",
    "SOUTH CAROLINA": "South Carolina Gamecocks",
    "SYRACUSE": "Syracuse Orange",
    "TEXAS": "Texas Longhorns",
    "TEXAS A&M": "Texas A&M Aggies",
    "UCLA": "UCLA Bruins",
    "UNLV": "UNLV Rebels",
    "VIRGINIA TECH": "Virginia Tech Hokies",
    "COASTAL CAROLINA": "Coastal Carolina Chanticleers",
    "CONNECTICUT": "Connecticut Huskies",
    "IOWA STATE": "Iowa State Cyclones",
    "KENTUCKY": "Kentucky Wildcats",
    "LIBERTY": "Liberty Flames",
    "MEMPHIS": "Memphis Tigers",
    "MISSOURI STATE": "Missouri State Bears",
    "NEBRASKA": "Nebraska Cornhuskers",
    "NORTHERN ILLINOIS": "Northern Illinois Huskies",
    "NORTH TEXAS": "North Texas Eagles",
    "OHIO U": "Ohio U Bobcats",
    "SACRAMENTO STATE": "Sacramento State Hornets",
    "SAN JOSE STATE": "San Jose State Spartans",
    "SOUTH FLORIDA": "South Florida Bulls",
    "TOLEDO": "Toledo Rockets",
}


def main():
    doc = pymupdf.open(PDF)
    details = load_details()

    pages = {p: doc[p - 1].get_text() for p in range(FIRST, LAST + 1)}
    joined, offsets = "", {}
    for p in range(FIRST, LAST + 1):
        offsets[len(joined)] = p
        joined += pages[p]

    def page_of(pos):
        return max((s for s in offsets if s <= pos), key=lambda s: s)

    marks = []
    for m in HEADING.finditer(joined):
        name = m.group(1).strip()
        # Leading bleed: the heading may be preceded on the same line by the
        # running header. Keep only the longest known key the text ends with.
        key = next((k for k in sorted(FEATURE_TO_TEAM, key=len, reverse=True)
                    if name.endswith(k)), None)
        if key is None:
            sys.exit(f"unmapped feature heading: {name!r}")
        marks.append((m.start(), m.end(), key, m.group(2), m.group(3)))

    entries = []
    for i, (start, end, key, side, number) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(joined)
        body = joined[end:stop]
        body = re.sub(r"\n?\d{1,3}\n2026 VSiN COLLEGE FOOTBALL BETTING GUIDE\n",
                      "\n", body)
        body = re.sub(r"\s+", " ", body).strip()
        team = FEATURE_TO_TEAM[key]
        entries.append({
            "team": team, "printed_name": key,
            "conference": details[team]["conference"],
            "side": side, "number": float(number),
            "page": offsets[page_of(start)],
            "team_pages": details[team]["pages"],
            "words": len(body.split()), "text": body,
        })

    overs = [e for e in entries if e["side"] == "OVER"]
    unders = [e for e in entries if e["side"] == "UNDER"]
    if len(FEATURE_TO_TEAM) != 29 or len(entries) != 29:
        sys.exit(f"expected 29 entries, parsed {len(entries)}")
    if len(set(e["team"] for e in entries)) != 29:
        sys.exit("duplicate team in the feature list")

    intro = re.sub(r"\s+", " ", pages[FIRST]).strip()
    rec = re.search(r"overall four-year record is now ([\d-]+) for ([\d.]+%)"
                    r".*?(\d+-\d+(?:-\d+)?) \(([\d.]+%)\) on Unders", intro)

    out = {
        "feature_title": "2026 college football win totals I'm betting now",
        "author": "Steve Makinen",
        "pages": [FIRST, LAST],
        "stated_method": ("going back through the coaching changes, the "
                          "Stability Scores, the transitional systems, the "
                          "recruiting rankings, and playing out the schedule "
                          "by his power ratings"),
        "stated_record_overall": rec.group(1) if rec else None,
        "stated_record_overall_pct": rec.group(2) if rec else None,
        "stated_record_unders": rec.group(3) if rec else None,
        "stated_record_unders_pct": rec.group(4) if rec else None,
        "market_named": "DraftKings",
        "prices_printed": False,
        "counts": {"total": len(entries), "over": len(overs),
                   "under": len(unders)},
        "entries": entries,
    }
    with open("_source/data/wintotals_feature.json", "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)

    print(f"feature entries   {len(entries)}  "
          f"({len(overs)} over / {len(unders)} under)")
    print(f"pages             {FIRST}-{LAST}")
    print(f"stated record     {out['stated_record_overall']} "
          f"({out['stated_record_overall_pct']}), unders "
          f"{out['stated_record_unders']} ({out['stated_record_unders_pct']})")
    print(f"prose captured    {sum(e['words'] for e in entries)} words, "
          f"median {sorted(e['words'] for e in entries)[len(entries)//2]} per entry")
    print(f"prices printed    {out['prices_printed']}")


if __name__ == "__main__":
    main()
