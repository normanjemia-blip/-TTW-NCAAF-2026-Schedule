#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 2 Conference Extraction
=================================================================

Parses the eleven conference preview pages into structured JSON:

  * the preview essay (prose), with its stated author
  * Makinen's projected standings table, matched to canonical team names

Each standings row carries the DraftKings win total, Makinen power rating,
home/road field-advantage values, schedule strength with national rank, and
projected wins/losses for all games and for conference games.

Rows are matched to teams from Phase 1 by power rating within the conference,
falling back to name-token overlap. Every match is verified against the team
pages, so a mis-parsed table cannot quietly become a conference file.

Usage:
    python3 _tools/extract_conferences.py      # run from the library root
"""

import json
import os
import re
import sys

SRC = "_source/data"
PAGES = "_source/extracted/pages"

NUMERIC = re.compile(r"^-?\d+\.?\d*$")
SCHEDULE = re.compile(r"^([\d.]+)\s*\((\d+)\)$")
AUTHOR = re.compile(r"previews?\s+by\s+([A-Z][A-Za-z.\' ]+)", re.I)

# Known duplicate printings in the source. Charlotte's row is printed in both
# the American (p. 49) and Conference USA (p. 187) standings tables with
# identical values. Three independent signals place Charlotte in the American:
# the contents page, its own team page (p. 52, "#14 of 14"), and the fact that
# every Conference USA team page reads "of 10". The Conference USA row is
# therefore a source error. It is recorded, not silently dropped.
KNOWN_DUPLICATES = {
    ("Conference USA", "CHARLOTTE"): {
        "belongs_to": "American",
        "note": (
            "Charlotte is printed in both the American (p. 49) and Conference "
            "USA (p. 187) projected standings tables with identical figures. "
            "The contents page, Charlotte's own team page (p. 52, ranked "
            "#14 of 14 in the American) and the '#N of 10' conference ranks on "
            "every Conference USA team page all place Charlotte in the "
            "American. Treated as a duplicate printing in the Conference USA "
            "table."
        ),
    }
}


def load(name):
    with open(os.path.join(SRC, f"{name}.json")) as fh:
        return json.load(fh)


def page_lines(page):
    with open(os.path.join(PAGES, f"p{page:03d}.txt")) as fh:
        return [ln.strip() for ln in fh if ln.strip()]


def parse_standings(page):
    """Rows run: team name, then nine values; the fifth is 'strength (rank)'."""
    lines = page_lines(page)
    start = max(i for i, ln in enumerate(lines) if ln == "PRJL")
    body = lines[start + 1:]

    rows, i = [], 0
    while i < len(body):
        name = body[i]
        if NUMERIC.match(name) or SCHEDULE.match(name):
            i += 1
            continue
        values = body[i + 1:i + 10]
        if len(values) < 9:
            break
        schedule = SCHEDULE.match(values[4])
        if not schedule:
            i += 1
            continue
        rows.append({
            "table_name": name,
            "dk_win_total": values[0],
            "sm_power_rating": values[1],
            "home_field": values[2],
            "road_field": values[3],
            "schedule_strength": schedule.group(1),
            "schedule_rank": int(schedule.group(2)),
            "proj_wins_all": values[5],
            "proj_losses_all": values[6],
            "proj_wins_conf": values[7],
            "proj_losses_conf": values[8],
        })
        i += 10
    return rows


def parse_prose(page):
    """Everything above the standings table, minus running headers."""
    lines = page_lines(page)
    stop = min(
        [i for i, ln in enumerate(lines)
         if ln.lower().startswith("2026 makinen projected standings")]
        or [len(lines)]
    )
    body = []
    for ln in lines[:stop]:
        if ln == str(page) or "VSiN COLLEGE FOOTBALL BETTING GUIDE" in ln:
            continue
        if AUTHOR.search(ln) or ln.lower() in ("preview", "previews"):
            continue
        body.append(ln)
    # Drop the display-type conference name, which repeats the heading.
    while body and body[-1].isupper() is False and len(body[-1]) < 24 and body[-1].istitle():
        body.pop()
    text = " ".join(body)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_author(page):
    for ln in page_lines(page):
        m = AUTHOR.search(ln)
        if m:
            return m.group(1).strip()
    return None


def match_rows(conference, rows, members):
    """Match standings rows to canonical teams; report anything unresolved."""
    # Ratings print as "44" in standings tables and "44.0" on team pages, so
    # they are keyed numerically rather than by string.
    by_rating = {}
    for team in members:
        by_rating.setdefault(float(team["power_rating"]), []).append(team)

    matched, duplicates, unmatched = [], [], []
    used = set()

    for row in rows:
        key = (conference, row["table_name"])
        if key in KNOWN_DUPLICATES:
            duplicates.append({**row, **KNOWN_DUPLICATES[key]})
            continue

        candidates = [t for t in by_rating.get(float(row["sm_power_rating"]), [])
                      if t["team"] not in used]
        if len(candidates) > 1:
            tokens = set(re.findall(r"[A-Z]+", row["table_name"].upper()))
            candidates.sort(
                key=lambda t: -len(tokens & set(re.findall(r"[A-Z]+", t["team"].upper()))))
            best = candidates[0]
        elif candidates:
            best = candidates[0]
        else:
            unmatched.append(row)
            continue

        used.add(best["team"])
        matched.append({**row, "team": best["team"], "page": best["page"],
                        "head_coach": best["head_coach"],
                        "hc_season": best["hc_season"],
                        "conf_rank": best["conf_rank"],
                        "natl_rank": best["natl_rank"],
                        "su_2025": best["su_2025"], "ats_2025": best["ats_2025"],
                        "ou_2025": best["ou_2025"]})

    missing = [t["team"] for t in members if t["team"] not in used]
    return matched, duplicates, unmatched, missing


def main():
    conferences = load("conferences")
    teams = load("teams")

    out, problems = [], []
    for conf in conferences:
        name = conf["conference"]
        page = conf["preview_page"]
        members = [t for t in teams if t["conference"] == name]
        rows = parse_standings(page)
        matched, duplicates, unmatched, missing = match_rows(name, rows, members)

        if unmatched:
            problems.append(f"{name}: unmatched rows {[r['table_name'] for r in unmatched]}")
        if missing:
            problems.append(f"{name}: teams with no standings row {missing}")

        # The standings rating must equal the team page rating for every team.
        by_team = {t["team"]: t for t in members}
        for row in matched:
            if float(row["sm_power_rating"]) != float(by_team[row["team"]]["power_rating"]):
                problems.append(
                    f"{name}: {row['team']} rating {row['sm_power_rating']} in "
                    f"standings vs {by_team[row['team']]['power_rating']} on team page")

        out.append({
            "conference": name,
            "preview_page": page,
            "author": parse_author(page),
            "prose": parse_prose(page),
            "standings": matched,
            "duplicate_rows": duplicates,
            "team_count": len(members),
        })

    with open(os.path.join(SRC, "conference_previews.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    for c in out:
        flag = f"  ⚠ {len(c['duplicate_rows'])} duplicate row(s)" if c["duplicate_rows"] else ""
        print(f"  {c['conference']:<16} p{c['preview_page']:<4} "
              f"{len(c['standings']):>2} teams  author={c['author']}{flag}")

    if problems:
        print("\nVALIDATION FAILED")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("\nvalidation passed — every standings row matches its team page rating")


if __name__ == "__main__":
    main()
