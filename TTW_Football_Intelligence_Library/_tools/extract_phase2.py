#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 2 Supporting Extraction
=================================================================

Everything Phase 2 needs that lives outside the eleven conference preview
pages, so each conference file can carry its own slice of the guide's
cross-cutting content:

  * p. 4    staff prediction matrix (conference champions, CFP picks)
  * pp. 22-27  Steve Makinen's win-total bets
  * pp. 5-15   VSiN host best bets
  * pp. 28-37  new head coaches, grouped by conference

Team names in these sections are printed in shortened upper case
("TX-SAN ANTONIO", "W KENTUCKY") and sometimes carry running-header bleed
from the PDF text layer. They are resolved against the canonical 138-team
list from Phase 1 rather than trusted as printed.

Usage:
    python3 _tools/extract_phase2.py      # run from the library root
"""

import json
import os
import re
import sys
from collections import defaultdict

import pymupdf

SRC = "_source/data"
PAGES = "_source/extracted/pages"
PDF = "_source/2026-VSiN-CFB-Betting-Guide.pdf"

# Conference labels as printed on the p. 4 prediction matrix.
PREDICTION_LABELS = {
    "ACC CHAMPION": "ACC",
    "BIG TEN CHAMPION": "Big Ten",
    "BIG 12 CHAMPION": "Big 12",
    "SEC CHAMPION": "SEC",
    "AAC CHAMPION": "American",
    "CUSA CHAMPION": "Conference USA",
    "MAC CHAMPION": "MAC",
    "MWC CCHAMPION": "Mountain West",      # typo is in the source
    "PAC-12 CHAMPION": "Pac-12",
    "SUN BELT CHAMPION": "Sun Belt",
}

CFP_LABELS = [
    "CFP FINAL FOUR #1", "CFP FINAL FOUR #2", "CFP FINAL FOUR #3",
    "CFP FINAL FOUR #4", "CFP TITLE GAME #1", "CFP TITLE GAME #2",
    "CFP CHAMPION",
]

# The row printed as "SUN BELT CHAMP" (y≈377) holds NFL team names, not Sun
# Belt teams. Its label does not describe its contents. Recorded as a source
# anomaly and excluded from prediction data rather than silently dropped.
MISLABELLED_ROW = "SUN BELT CHAMP"

# Running-header fragments that bleed into the text layer mid-sentence and
# must be stripped before a printed name can be resolved.
BLEED = re.compile(
    r"\b(?:2026\s+)?(?:VSIN\s+)?(?:COLL?EGE\s+)?(?:EGE\s+)?FOOTBALL\s+BETTING\s+GUIDE\b"
    r"|\bBETTING\s+GUIDE\b|\bATS\.?\b|\bLL\b|\bEGE\b",
    re.I,
)

# Leading initials in the standings tables stand for more than one word
# ("N ILLINOIS" is Northern, "N DAKOTA ST" is North), so every plausible
# expansion is generated and any that collides across teams is discarded.
INITIALS = {
    "N": ["NORTH", "NORTHERN"],
    "S": ["SOUTH", "SOUTHERN"],
    "E": ["EAST", "EASTERN"],
    "W": ["WEST", "WESTERN"],
    "C": ["CENTRAL"],
    "FLA": ["FLORIDA"],
    "TENN": ["TENNESSEE"],
    "MISS": ["MISSISSIPPI"],
    "LA": ["LOUISIANA"],
    "TX": ["TEXAS"],
}


def load(name):
    with open(os.path.join(SRC, f"{name}.json")) as fh:
        return json.load(fh)


def normalise(text):
    text = BLEED.sub(" ", text.upper())
    text = re.sub(r"[^A-Z0-9&\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def name_variants(printed):
    """Every spelling of a standings short name that other sections might use."""
    base = normalise(printed)
    forms = {base}
    if re.search(r"\bST\b", base):
        forms.add(re.sub(r"\bST\b", "STATE", base))
    for form in list(forms):
        parts = form.split()
        if parts and parts[0] in INITIALS:
            for expansion in INITIALS[parts[0]]:
                forms.add(" ".join([expansion] + parts[1:]))
    return forms


class TeamResolver:
    """Resolve a printed short name to a canonical team, or report failure.

    Built from the eleven projected-standings tables, which name all 138 teams
    in the guide's own shortened style and were matched to canonical teams by
    power rating. That makes the map guide-derived rather than guessed, and it
    separates the pairs that defeat token matching (Kansas / Kansas State,
    Illinois / Northern Illinois, Missouri / Missouri State).
    """

    def __init__(self, teams, previews):
        self.by_name = {t["team"]: t for t in teams}
        self.lookup = {}
        collisions = set()

        for conf in previews:
            for row in conf["standings"]:
                for form in name_variants(row["table_name"]):
                    if form in self.lookup and self.lookup[form] != row["team"]:
                        collisions.add(form)
                    self.lookup[form] = row["team"]

        # Canonical full names resolve too, minus the mascot where unambiguous.
        for team in teams:
            full = normalise(team["team"])
            if full not in self.lookup:
                self.lookup[full] = team["team"]

        for form in collisions:
            self.lookup.pop(form, None)

        self.aliases = {
            "CONNECTICUT": "Connecticut Huskies",
            "UCONN": "Connecticut Huskies",
            "OHIO U": "Ohio U Bobcats",
            "UMASS": "Massachusetts Minutemen",
            "MIAMI OH": "Miami (Ohio) RedHawks",
            "OLE MISS": "Ole Miss Rebels",
            "MISSISSIPPI": "Ole Miss Rebels",
        }

    def resolve(self, printed):
        text = normalise(printed)
        if not text:
            return None
        if text in self.aliases:
            return self.by_name[self.aliases[text]]
        if text in self.lookup:
            return self.by_name[self.lookup[text]]
        # Longest known name the printed text ends with (leading bleed such as
        # "... BETTING GUIDE UCLA") or begins with (trailing bet wording such as
        # "GEORGIA SOUTHERN OVER 3.5 CONFERENCE WINS").
        best = None
        for form, team in self.lookup.items():
            if text.endswith(" " + form) or text.startswith(form + " "):
                if best is None or len(form) > len(best[0]):
                    best = (form, team)
        return self.by_name[best[1]] if best else None


def parse_predictions(doc):
    """p. 4 is a landscape matrix: labels at x<40, picks in columns to the right."""
    page = doc[3]
    spans = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span["text"].strip()
                if text:
                    spans.append((span["bbox"][0], span["bbox"][1], text))

    labels = sorted([(y, t) for x, y, t in spans if x < 40], key=lambda r: r[0])
    values = [(x, y, t) for x, y, t in spans if x >= 40]

    out, anomalies = {}, []
    for y, label in labels:
        # Picks sit within a couple of points of their label's baseline.
        row = sorted([(x, t) for x, vy, t in values if 0 <= vy - y <= 4])
        picks = [t for x, t in row]
        if label == MISLABELLED_ROW:
            anomalies.append({
                "printed_label": label,
                "picks": picks,
                "note": (
                    "This row is printed under the label 'SUN BELT CHAMP' but "
                    "contains NFL team names (Falcons, Panthers, Bucs, Saints). "
                    "The label does not describe the contents. Excluded from "
                    "conference prediction data; recorded here as printed."
                ),
            })
            continue
        if label in PREDICTION_LABELS or label in CFP_LABELS:
            out[label] = picks
    return out, anomalies


def parse_win_totals(resolver):
    text = " ".join(
        re.sub(r"\s+", " ", open(os.path.join(PAGES, f"p{p:03d}.txt")).read())
        for p in range(22, 28)
    )
    found, seen = [], set()
    for name, side, number in re.findall(
        r"([A-Z][A-Z &'\.\-]{2,30}?)\s*[–-]\s*(OVER|UNDER)\s*([0-9]+\.5)\s*WINS", text
    ):
        key = (side, number, name.strip())
        if key in seen:
            continue
        seen.add(key)
        team = resolver.resolve(name)
        found.append({
            "printed_name": name.strip(),
            "team": team["team"] if team else None,
            "conference": team["conference"] if team else None,
            "side": side,
            "number": number,
        })
    return found


def parse_best_bets(doc, resolver):
    """Host best bets: contributor name at ~11pt, the pick headline at ~8pt."""
    bets = []
    for page_no in range(5, 16):
        page = doc[page_no - 1]
        entries = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    size = round(span["size"], 1)
                    if not text:
                        continue
                    if 10.5 <= size <= 11.5 and re.fullmatch(r"[A-Z][A-Z\.' ]{3,30}", text):
                        entries.append(("contributor", span["bbox"][1], text))
                    elif 7.5 <= size <= 8.5 and text.isupper() and len(text) > 8:
                        entries.append(("pick", span["bbox"][1], text))
        entries.sort(key=lambda e: e[1])
        current = None
        for kind, _, text in entries:
            if kind == "contributor":
                current = text.title()
            elif current:
                team = resolver.resolve(re.split(r"\s+(?:TO|OVER|UNDER|\+|\-|\d)", text)[0])
                bets.append({
                    "contributor": current,
                    "pick": text,
                    "page": page_no,
                    "team": team["team"] if team else None,
                    "conference": team["conference"] if team else None,
                })
    return bets


def parse_new_coaches(carousel, teams):
    by_name = {t["head_coach"]: t for t in teams}
    out = []
    for entry in carousel:
        team = by_name.get(entry["name"])
        out.append({
            "coach": entry["name"],
            "page": entry["page"],
            "team": team["team"] if team else None,
            "conference": team["conference"] if team else None,
            "hc_season": team["hc_season"] if team else None,
        })
    return out


def main():
    teams = load("teams")
    carousel = load("new_head_coaches")
    previews = load("conference_previews")
    resolver = TeamResolver(teams, previews)
    doc = pymupdf.open(PDF)

    predictions, anomalies = parse_predictions(doc)
    win_totals = parse_win_totals(resolver)
    best_bets = parse_best_bets(doc, resolver)
    new_coaches = parse_new_coaches(carousel, teams)

    problems = []
    for label in PREDICTION_LABELS:
        picks = predictions.get(label, [])
        if len(picks) != 22:
            problems.append(f"p4 '{label}': {len(picks)} picks, expected 22")
    overs = [w for w in win_totals if w["side"] == "OVER"]
    unders = [w for w in win_totals if w["side"] == "UNDER"]
    if len(overs) != 14:
        problems.append(f"win totals: {len(overs)} Overs, guide states 14")
    if len(unders) != 15:
        problems.append(f"win totals: {len(unders)} Unders, guide states 15")
    unresolved = [w["printed_name"] for w in win_totals if not w["team"]]
    if unresolved:
        problems.append(f"win totals unresolved to a team: {unresolved}")

    bundle = {
        "predictions": predictions,
        "prediction_anomalies": anomalies,
        "win_totals": win_totals,
        "best_bets": best_bets,
        "new_coaches": new_coaches,
    }
    for name, payload in bundle.items():
        with open(os.path.join(SRC, f"phase2_{name}.json"), "w") as fh:
            json.dump(payload, fh, indent=1)

    print(f"prediction rows   {len(predictions)} ({len(anomalies)} anomaly)")
    print(f"win total picks   {len(win_totals)}  ({len(overs)} over / {len(unders)} under)")
    print(f"best bets         {len(best_bets)}  "
          f"({sum(1 for b in best_bets if b['team'])} resolved to a team)")
    print(f"new head coaches  {len(new_coaches)}")
    if problems:
        print("\nVALIDATION FAILED")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("\nvalidation passed")


if __name__ == "__main__":
    main()
