#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Coaching Carousel extraction
=================================================================

Extracts the per-coach entries from "The Coaching Carousel Never Stops"
(pp. 28-37), Adam Burke's feature on every new head coach. This is the
guide's primary coaching-assessment source and the only place it states
a view on most of the 35 hires.

Each entry is a bold "Coach Name  School" line followed by a paragraph,
grouped under a conference heading. Bold is detected from the font name,
the same way Phase 3 found the Burning Question headers, because the
plain text stream gives no reliable way to tell a heading from a
sentence that happens to start with a name.

The extractor validates against the feature's own claim — the article
states 35 schools have new head coaches — and exits non-zero if the
count does not match.

Usage:
    python3 _tools/extract_carousel.py
"""

import json
import re
import sys

import pymupdf

PDF = "_source/2026-VSiN-CFB-Betting-Guide.pdf"
FIRST, LAST = 28, 37

# Conference headings sit alone in caps. They are section markers, not
# entries, and the school names underneath are what map to teams.
CONFERENCES = {
    "AMERICAN": "American", "ACC": "ACC", "BIG TEN": "Big Ten",
    "BIG 12": "Big 12", "CONFERENCE USA": "Conference USA",
    "C-USA": "Conference USA", "MAC": "MAC",
    # The banner is set with irregular internal spacing, so both the
    # hyphenated and spaced forms of Pac-12 have to be recognised.
    "MOUNTAIN WEST": "Mountain West", "PAC-12": "Pac-12", "PAC 12": "Pac-12",
    "SEC": "SEC", "SUN BELT": "Sun Belt",
    "INDEPENDENT": "Independents", "INDEPENDENTS": "Independents",
}

# The feature names schools its own way. Map to canonical VSiN team names.
SCHOOL_TO_TEAM = {
    "Memphis": "Memphis Tigers", "North Texas": "North Texas Eagles",
    "Tulane": "Tulane Green Wave", "USF": "South Florida Bulls",
    "California": "California Golden Bears", "Stanford": "Stanford Cardinal",
    "Virginia Tech": "Virginia Tech Hokies", "Wake Forest": "Wake Forest Demon Deacons",
    "Michigan": "Michigan Wolverines", "Michigan State": "Michigan State Spartans",
    "Penn State": "Penn State Nittany Lions", "UCLA": "UCLA Bruins",
    "Arizona State": "Arizona State Sun Devils", "Baylor": "Baylor Bears",
    "Iowa State": "Iowa State Cyclones", "Kansas": "Kansas Jayhawks",
    "Oklahoma State": "Oklahoma State Cowboys", "TCU": "TCU Horned Frogs",
    "UCF": "UCF Golden Knights", "Utah": "Utah Utes",
    "Kennesaw State": "Kennesaw State Owls", "Missouri State": "Missouri State Bears",
    "Sam Houston": "Sam Houston State Bearkats",
    "Sam Houston State": "Sam Houston State Bearkats",
    "Bowling Green": "Bowling Green Falcons", "Kent State": "Kent State Golden Flashes",
    "Northern Illinois": "Northern Illinois Huskies", "Toledo": "Toledo Rockets",
    "UAB": "UAB Blazers",
    "Colorado State": "Colorado State Rams", "Nevada": "Nevada Wolf Pack",
    "Sacramento State": "Sacramento State Hornets",
    "UNLV": "UNLV Rebels", "Oregon State": "Oregon State Beavers",
    "Washington State": "Washington State Cougars",
    "Arkansas": "Arkansas Razorbacks", "Auburn": "Auburn Tigers",
    "Florida": "Florida Gators", "Kentucky": "Kentucky Wildcats",
    "LSU": "LSU Tigers", "Ole Miss": "Ole Miss Rebels",
    "Coastal Carolina": "Coastal Carolina Chanticleers",
    "Southern Miss": "Southern Miss Golden Eagles",
    "Charlotte": "Charlotte 49ers", "UConn": "Connecticut Huskies",
    "Connecticut": "Connecticut Huskies",
    "Temple": "Temple Owls", "Louisiana Tech": "Louisiana Tech Bulldogs",
    "Marshall": "Marshall Thundering Herd",
    "Delaware": "Delaware Fightin’ Blue Hens",
    "Middle Tennessee": "Middle Tennessee Blue Raiders",
    "New Mexico State": "New Mexico State Aggies",
    "Old Dominion": "Old Dominion Monarchs", "Rice": "Rice Owls",
    "Purdue": "Purdue Boilermakers", "West Virginia": "West Virginia Mountaineers",
    "Fresno State": "Fresno State Bulldogs", "San Jose State": "San Jose State Spartans",
    "Hawaii": "Hawaii Rainbow Warriors", "Air Force": "Air Force Falcons",
    "Kansas State": "Kansas State Wildcats", "James Madison": "James Madison Dukes",
    # The guide writes Ole Miss as "Mississippi" here, and Ohio U as "Ohio",
    # the same short forms its standings tables use.
    "Mississippi": "Ole Miss Rebels", "Ohio": "Ohio U Bobcats",
}


def spans(page):
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for s in line["spans"]:
                t = s["text"].strip()
                if t:
                    yield t, s["font"], round(s["size"], 1), s["bbox"]


# The feature is typeset in three distinct display faces, which is the
# only reliable way to tell its parts apart: the plain text stream gives
# no clue that "Memphis" is a heading rather than a word in a sentence.
COACH_FONT, COACH_SIZE = "BebasNeueLight", 36.0     # coach name
SCHOOL_FONT, SCHOOL_SIZE = "BebasNeueBold", 24.0    # school beside it
CONF_FONT, CONF_SIZE = "BebasNeueBook", 72.0        # conference banner
BODY_FONT = "SourceSerif4"                          # assessment prose


def main():
    doc = pymupdf.open(PDF)
    teams_conf = {t["team"]: t["conference"]
                  for t in json.load(open("_source/data/teams.json"))}
    entries = []
    validation = []
    conflicts = []

    for pno in range(FIRST, LAST + 1):
        page = doc[pno - 1]
        items = list(spans(page))

        # The conference banner is decorative: it is set vertically in the
        # margin, uses irregular internal spacing, and a single span can
        # carry two banners when a section changes mid-page. So the
        # conference is taken from the canonical team table instead, and
        # the banner is parsed only as a cross-check that this feature is
        # being read in the right place.
        banners = []
        for text, font, size, bbox in items:
            if font == CONF_FONT and abs(size - CONF_SIZE) < 1:
                raw = re.sub(r"\s+", " ", text.upper()).strip()
                hit = [v for k, v in CONFERENCES.items() if k in raw]
                if hit:
                    banners.extend(hit)
                else:
                    validation.append(f"p{pno}: unreadable conference banner {text!r}")

        # Headings pair a coach-name span with the school span printed to
        # its right on the same baseline. Match them by vertical proximity
        # rather than by order, since the two use different fonts and
        # sizes and so are not guaranteed to be adjacent in the stream.
        names = [(t, b) for t, f, sz, b in items
                 if f == COACH_FONT and abs(sz - COACH_SIZE) < 1]
        schools = [(t, b) for t, f, sz, b in items
                   if f == SCHOOL_FONT and abs(sz - SCHOOL_SIZE) < 1]
        body = [(t, b) for t, f, sz, b in items if f.startswith(BODY_FONT)]

        heads = []
        for coach, cb in names:
            best, bestd = None, 99
            for school, sb in schools:
                d = abs(cb[1] - sb[1])
                if d < bestd and sb[0] > cb[0]:
                    best, bestd = school, d
            if best is None or bestd > 20:
                validation.append(f"p{pno}: no school found for {coach!r}")
                continue
            heads.append((cb[1], coach, best))
        heads.sort()

        # Assessment prose is whatever sits below a heading and above the
        # next one.
        for i, (y, coach, school) in enumerate(heads):
            nexty = heads[i + 1][0] if i + 1 < len(heads) else 1e9
            text = " ".join(t for t, b in sorted(body, key=lambda x: x[1][1])
                            if y < b[1] < nexty)
            if school not in SCHOOL_TO_TEAM:
                validation.append(f"p{pno}: school {school!r} not mapped to a team")
                continue
            team = SCHOOL_TO_TEAM[school]
            conference = teams_conf[team]
            if banners and conference not in banners:
                # A rotated banner span can carry two conference labels, so
                # this only fires when the team's conference is absent from
                # the page entirely. That is a real inconsistency in the
                # guide, not an extraction artifact, and is recorded rather
                # than corrected.
                conflicts.append({
                    "team": team,
                    "field": "conference placement in the Coaching Carousel",
                    "detail": (
                        f"The Coaching Carousel (p. {pno}) places {school} in "
                        f"the {' / '.join(banners)} section, while the team "
                        f"page and the projected standings place the programme "
                        f"in the {conference}. Both are reproduced as printed "
                        f"and neither is corrected."),
                })
            entries.append({
                "coach": coach,
                "school": school,
                "team": team,
                "conference": conference,
                "page": pno,
                "assessment": re.sub(r"\s+", " ", text).strip(),
            })

    clean = entries

    # ---- validation ----
    if len(clean) != 35:
        validation.append(f"expected 35 new head coaches, extracted {len(clean)}")
    thin = [e["coach"] for e in clean if len(e["assessment"]) < 200]
    if thin:
        validation.append(f"assessment text too short for: {thin}")
    dupes = [t for t in {e["team"] for e in clean}
             if sum(1 for e in clean if e["team"] == t) > 1]
    if dupes:
        validation.append(f"a team appears twice: {dupes}")

    with open("_source/data/coaching_carousel.json", "w") as fh:
        json.dump(clean, fh, indent=1, ensure_ascii=False)
    with open("_source/data/carousel_conflicts.json", "w") as fh:
        json.dump(conflicts, fh, indent=1, ensure_ascii=False)

    print(f"coaching carousel entries: {len(clean)} (pp. {FIRST}-{LAST})")
    from collections import Counter
    for c, n in sorted(Counter(e["conference"] for e in clean).items()):
        print(f"  {c}: {n}")
    for c in conflicts:
        print(f"  SOURCE CONFLICT recorded: {c['team']}")
    if validation:
        print("\nVALIDATION FAILED")
        for v in validation:
            print("  -", v)
        sys.exit(1)
    print("\nvalidation passed")


if __name__ == "__main__":
    main()
