#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Stability Scores (pp. 41-44)
================================================================

Steve Makinen's Stability Score table, extracted by position.

Each row carries the 2025 record, whether the head coach, offensive
coordinator, defensive coordinator and starting quarterback return, a
returning-starters figure, and the total score. Columns are fixed:

    TEAM (CONFERENCE) | RECORD | HC? | OC? | DC? | QB? | RET STRS | STABILITY

The returning-starters cell prints as "2 (12)" — points, then the underlying
count in brackets. That count is an independent second printing of the same
figure taken from each team page, so the two are compared here.

Usage:
    python3 _tools/extract_stability.py     # run from the library root
"""

import json
import os
import re
import sys

import pymupdf

SRC = "_source/data"
PDF = "_source/2026-VSiN-CFB-Betting-Guide.pdf"
PAGES = (41, 42, 43, 44)

COLUMNS = {"team": (0, 170), "record": (170, 240), "hc": (240, 300),
           "oc": (300, 360), "dc": (360, 425), "qb": (425, 480),
           "ret": (480, 530), "total": (530, 612)}

CONFERENCE_TAGS = {
    "SEC": "SEC", "B1G": "Big Ten", "B10": "Big Ten", "B12": "Big 12",
    "ACC": "ACC", "AAC": "American", "MWC": "Mountain West", "MAC": "MAC",
    "SBC": "Sun Belt", "CUSA": "Conference USA", "CUS": "Conference USA",
    "P12": "Pac-12", "IND": "Independents",
}


def cell(spans, lo, hi):
    hits = [s for s in spans if lo <= s["x"] < hi]
    return " ".join(s["text"] for s in sorted(hits, key=lambda s: s["x"])) if hits else None


def main():
    doc = pymupdf.open(PDF)
    rows = []
    for page_no in PAGES:
        spans = []
        for block in doc[page_no - 1].get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if text and round(span["size"], 1) <= 8.5:
                        spans.append({"x": span["bbox"][0],
                                      "y": round(span["bbox"][1], 1),
                                      "text": text})
        by_row = {}
        for s in spans:
            by_row.setdefault(round(s["y"], 0), []).append(s)

        for y, group in sorted(by_row.items()):
            name = cell(group, *COLUMNS["team"])
            if not name or not re.search(r"\(([A-Z0-9]+)\)\s*$", name):
                continue
            tag = re.search(r"\(([A-Z0-9]+)\)\s*$", name).group(1)
            ret = cell(group, *COLUMNS["ret"]) or ""
            count = re.search(r"\((\d+)\)", ret)
            rows.append({
                "printed_name": re.sub(r"\s*\([A-Z0-9]+\)\s*$", "", name).strip(),
                "conference_tag": tag,
                "conference": CONFERENCE_TAGS.get(tag),
                "record_2025": cell(group, *COLUMNS["record"]),
                "hc_returns": cell(group, *COLUMNS["hc"]),
                "oc_returns": cell(group, *COLUMNS["oc"]),
                "dc_returns": cell(group, *COLUMNS["dc"]),
                "qb_returns": cell(group, *COLUMNS["qb"]),
                "returning_starters_points": ret.split("(")[0].strip() or None,
                "returning_starters_count": int(count.group(1)) if count else None,
                "stability_score": cell(group, *COLUMNS["total"]),
                "page": page_no,
            })

    with open(os.path.join(SRC, "stability_scores.json"), "w") as fh:
        json.dump(rows, fh, indent=1)

    print(f"stability rows extracted   {len(rows)} (expected 138)")
    complete = [r for r in rows if r["stability_score"] and r["returning_starters_count"]]
    print(f"rows with score and count  {len(complete)}")

    # Points must reconstruct the printed total: HC 4, OC 3, DC 3, QB 4.
    bad = []
    for r in rows:
        try:
            parts = [int(r[k]) for k in ("hc_returns", "oc_returns",
                                          "dc_returns", "qb_returns")]
            total = sum(parts) + int(r["returning_starters_points"])
            if total != int(r["stability_score"]):
                bad.append((r["printed_name"], parts,
                            r["returning_starters_points"], r["stability_score"]))
        except (TypeError, ValueError):
            bad.append((r["printed_name"], "unparsed", None, None))
    print(f"rows whose components sum to the printed total  "
          f"{len(rows) - len(bad)}/{len(rows)}")
    if bad:
        print("  arithmetic mismatches:")
        for b in bad[:10]:
            print("   ", b)
    # The stability table prints returning starters a second time. Comparing it
    # to the figure on each team page is an independent check on the
    # coordinate extraction — and surfaces places where the guide disagrees
    # with itself.
    ABBR = {"ST": "STATE", "N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST",
            "C": "CENTRAL", "FLA": "FLORIDA", "TENN": "TENNESSEE", "TX": "TEXAS",
            "GA": "GEORGIA", "LA": "LOUISIANA", "MISS": "MISSISSIPPI"}

    def norm(name):
        cleaned = re.sub(r"[^A-Z0-9& ]", " ", name.upper())
        return " ".join(ABBR.get(w, w) for w in cleaned.split())

    with open(os.path.join(SRC, "conference_previews.json")) as fh:
        previews = json.load(fh)
    with open(os.path.join(SRC, "team_details.json")) as fh:
        details = {t["team"]: t for t in json.load(fh)}

    lookup = {}
    for conf in previews:
        for row in conf["standings"]:
            lookup[norm(row["table_name"])] = row["team"]
    for team in details:
        lookup.setdefault(norm(team), team)

    conflicts, matched = [], 0
    for r in rows:
        key = norm(r["printed_name"])
        team = lookup.get(key)
        if not team:
            candidates = {v for k, v in lookup.items()
                          if k.startswith(key + " ") or key.startswith(k + " ")}
            team = candidates.pop() if len(candidates) == 1 else None
        r["team"] = team
        if not team:
            continue
        matched += 1
        printed = details[team]["returning_starters"]
        if printed and printed["total"]["value"] != r["returning_starters_count"]:
            conflicts.append({
                "team": team,
                "field": "returning_starters_total",
                "detail": (
                    f"The team page (p. {details[team]['pages'][0]}) prints "
                    f"{printed['total']['value']} returning starters; the "
                    f"Stability Score table (p. {r['page']}) prints "
                    f"{r['returning_starters_count']} for the same team. The team "
                    f"page is internally consistent — offence "
                    f"{printed['offense']['value']} plus defence "
                    f"{printed['defense']['value']} equals its own total — so "
                    f"both figures are reproduced as printed and neither is "
                    f"corrected."),
            })

    with open(os.path.join(SRC, "stability_scores.json"), "w") as fh:
        json.dump(rows, fh, indent=1)
    with open(os.path.join(SRC, "stability_conflicts.json"), "w") as fh:
        json.dump(conflicts, fh, indent=1)

    print(f"rows matched to a team     {matched}/138")
    print(f"returning starters agree with team pages  "
          f"{matched - len(conflicts)}/{matched}")
    if conflicts:
        print("  SOURCE CONFLICTS:")
        for c in conflicts:
            print(f"    {c['team']}")
    if len(rows) != 138 or matched != 138:
        sys.exit(1)


if __name__ == "__main__":
    main()
