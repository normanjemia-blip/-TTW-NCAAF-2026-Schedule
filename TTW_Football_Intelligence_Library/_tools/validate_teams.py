#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 3 Validation
=======================================================

Checks the built team database against the Phase 3 completion requirements:

  * 138 team files exist, one per FBS team, none duplicated, none missing
  * every file carries all 29 standardised headings in the correct order
  * every team maps to exactly one canonical conference
  * every printed Makinen rating reconciles to the Phase 1 / Phase 2 figures
  * every file carries page provenance
  * deferred values are explicitly marked

Exits non-zero if any check fails.

Usage:
    python3 _tools/validate_teams.py
"""

import json
import os
import re
import sys
from collections import Counter

SRC = "_source/data"
OUT = "02_Team_Database"

SCHEMA = [
    "Program Snapshot", "Conference", "VSiN Team Rank / Conference Rank",
    "Steve Makinen Power Rating", "Home-Field Advantage Reference",
    "Head Coach", "Coordinator Notes", "Coaching Continuity / Changes",
    "Quarterback Situation", "Returning Production", "Transfer Portal",
    "Recruiting / Roster Notes", "Offensive Identity", "Defensive Identity",
    "Key Strengths", "Key Weaknesses", "Schedule Overview",
    "Difficult Stretches / Trap Spots", "Win Total Discussion",
    "Futures / Conference / Playoff Discussion", "Betting Notes / Best Bets",
    "Historical / Situational Trends", "Important Statistics", "Bull Case",
    "Bear Case", "Open Questions / Risks", "Source Conflicts",
    "Relevant Page References", "Cross-Links",
]


def load(name):
    with open(os.path.join(SRC, f"{name}.json")) as fh:
        return json.load(fh)


def slug(name):
    # Matches coach_lib.slug and build_teams.slug. All three diverged on
    # "&" until Phase 11's repository-wide link check exposed it.
    s = name.lower().replace("\u2019", "").replace("'", "").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def main():
    teams = load("teams")
    details = {t["team"]: t for t in load("team_details")}
    previews = load("conference_previews")
    standings = {r["team"]: r for c in previews for r in c["standings"]}

    failures, notes = [], []

    files = {f for f in os.listdir(OUT) if f.endswith(".md") and f != "README.md"}
    expected = {f"{slug(t['team'])}.md" for t in teams}

    if len(teams) != 138:
        failures.append(f"expected 138 teams, source lists {len(teams)}")
    missing = expected - files
    extra = files - expected
    if missing:
        failures.append(f"missing team files: {sorted(missing)[:5]}")
    if extra:
        failures.append(f"unexpected files: {sorted(extra)[:5]}")

    slugs = Counter(slug(t["team"]) for t in teams)
    dupes = [s for s, n in slugs.items() if n > 1]
    if dupes:
        failures.append(f"duplicate team slugs: {dupes}")

    conf_of = {}
    for t in teams:
        conf_of.setdefault(t["team"], set()).add(t["conference"])
    multi = [k for k, v in conf_of.items() if len(v) != 1]
    if multi:
        failures.append(f"teams mapped to more than one conference: {multi}")

    schema_ok = rating_ok = provenance_ok = 0
    deferred_marks, conflict_files = 0, 0

    for team in teams:
        path = os.path.join(OUT, f"{slug(team['team'])}.md")
        if not os.path.exists(path):
            continue
        text = open(path).read()

        headings = re.findall(r"^## \d+\. (.+)$", text, re.M)
        if headings == SCHEMA:
            schema_ok += 1
        else:
            failures.append(f"{team['team']}: schema mismatch "
                            f"({len(headings)} headings)")

        printed = details[team["team"]]["power_rating"]
        phase1 = team["power_rating"]
        phase2 = standings[team["team"]]["sm_power_rating"]
        if (float(printed) == float(phase1) == float(phase2)
                and re.search(rf"\*\*{re.escape(str(printed))}\*\* — as printed", text)):
            rating_ok += 1
        else:
            failures.append(
                f"{team['team']}: rating reconciliation failed "
                f"(file {printed}, phase1 {phase1}, phase2 {phase2})")

        if re.search(r"\(p\. \d+\)|pp\. \d+", text):
            provenance_ok += 1
        else:
            failures.append(f"{team['team']}: no page provenance found")

        deferred_marks += len(re.findall(r"DEFERRED — EXTRACTION NOT RELIABLE", text))
        if "SOURCE CONFLICT" in text:
            conflict_files += 1

    print(f"team files present                 {len(files)}/138")
    print(f"schema complete (29 headings)      {schema_ok}/138")
    print(f"power ratings reconciled           {rating_ok}/138")
    print(f"files with page provenance         {provenance_ok}/138")
    print(f"files carrying a source conflict   {conflict_files}")
    print(f"explicit deferred markers          {deferred_marks}")

    conferences = Counter(t["conference"] for t in teams)
    print("\nteams by conference:")
    for conf, n in sorted(conferences.items(), key=lambda x: -x[1]):
        built = sum(1 for t in teams if t["conference"] == conf
                    and os.path.exists(os.path.join(OUT, f"{slug(t['team'])}.md")))
        flag = "" if built == n else "  ← MISMATCH"
        print(f"  {conf:<16} {built}/{n}{flag}")

    if failures:
        print(f"\nVALIDATION FAILED ({len(failures)}):")
        for f in failures[:20]:
            print("  -", f)
        sys.exit(1)
    print("\nall Phase 3 completion checks passed")


if __name__ == "__main__":
    main()
