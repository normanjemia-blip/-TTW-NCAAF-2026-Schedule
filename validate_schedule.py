#!/usr/bin/env python3
"""
Validate TTW_2026_Verified_Schedule_ESPN_v1.0.csv against the TTW NCAAF
2026 schedule build requirements.

Runs 18 base checks plus a placeholder-team hard-fail and a Week 0
normalization check added in the phase-3 amendment:
  1.  Duplicate GameIDs
  2.  Blank GameIDs
  3.  Invalid season values
  4.  Missing week values
  5.  Missing or invalid dates
  6.  Missing away teams
  7.  Missing home teams
  8.  Same-team matchups
  9.  Invalid neutral-site values
  10. Invalid completed values
  11. Exact duplicate matchup/date combinations
  12. Miami vs Miami (OH) identity separation
  13. North Dakota State inclusion and routing
  14. Sacramento State inclusion and routing
  15. Team schedule counts (flags unusually low/high counts)
  16. Weeks successfully retrieved (from retrieval_log.csv)
  17. Unexpected gaps in the weekly retrieval sequence
  18. Rows excluded from the final file (from raw_espn/build_log.json)
  19. Retained placeholder teams (hard failure - no exception for
      championship-labeled rows; placeholder teams also count toward the
      unresolved-team total) and unresolved team identities in general
  20. Week 0 normalization: every retained 2026-08-29 / 2026-08-30 game must
      have week=0, every retained game on/after 2026-09-03 must not, and a
      named set of known opening-weekend games is explicitly checked

Also performs a provenance check (every retained row traces back to a raw
ESPN response file) as the operational proxy for "0 manually transcribed
rows / 0 fabricated games".

Exit code is 0 only if every hard-fail check (1-10, provenance, 19, 20)
passes. Checks 11-18 are diagnostic/reporting checks (they surface findings
such as low/high game counts rather than pass/fail on their own).
"""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(REPO_ROOT, "TTW_2026_Verified_Schedule_ESPN_v1.0.csv")
LOG_PATH = os.path.join(REPO_ROOT, "retrieval_log.csv")
BUILD_LOG_PATH = os.path.join(REPO_ROOT, "raw_espn", "build_log.json")
RAW_SCOREBOARD_DIR = os.path.join(REPO_ROOT, "raw_espn", "scoreboard")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_BOOL = {"TRUE", "FALSE"}
PLACEHOLDER_NAME_RE = re.compile(r"^\s*(TBD|To Be Determined|Unknown)\b", re.IGNORECASE)

WEEK_ZERO_DATES = {"2026-08-29", "2026-08-30"}
WEEK_ZERO_CUTOFF_DATE = "2026-09-03"

# Explicit opening-weekend examples named in the phase-3 amendment request,
# each (away_team_substring, home_team_substring).
WEEK_ZERO_EXAMPLES = [
    ("North Carolina", "TCU"),
    ("NC State", "Virginia"),
    ("Jacksonville State", "North Dakota State"),
    ("Sacramento State", "Eastern Michigan"),
    ("Hawai", "Stanford"),
    ("Memphis", "UNLV"),
    ("San Jos", "USC"),
    ("New Mexico State", "Florida State"),
]

HARD_FAILS = []
DIAGNOSTICS = []


def hard_fail(check, count, detail=""):
    HARD_FAILS.append((check, count, detail))


def diagnostic(check, message):
    DIAGNOSTICS.append((check, message))


def load_rows():
    with open(CSV_PATH, newline="") as f:
        return list(csv.DictReader(f))


def load_raw_event_ids():
    ids = set()
    for fn in os.listdir(RAW_SCOREBOARD_DIR):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(RAW_SCOREBOARD_DIR, fn)) as f:
            data = json.load(f)
        for e in data.get("events", []):
            ids.add(e["id"])
    return ids


def main():
    rows = load_rows()
    print(f"Loaded {len(rows)} rows from {CSV_PATH}\n")

    # --- 1. Duplicate GameIDs ---
    id_counts = Counter(r["id"] for r in rows)
    dupes = {k: v for k, v in id_counts.items() if v > 1}
    hard_fail("1. Duplicate GameIDs", len(dupes), list(dupes.items())[:10])

    # --- 2. Blank GameIDs ---
    blank_ids = sum(1 for r in rows if not r["id"].strip())
    hard_fail("2. Blank GameIDs", blank_ids)

    # --- 3. Invalid season values ---
    bad_season = [r["id"] for r in rows if r["season"] != "2026"]
    hard_fail("3. Invalid season values", len(bad_season), bad_season[:10])

    # --- 4. Missing week values ---
    bad_week = [r["id"] for r in rows if not r["week"].strip()]
    hard_fail("4. Missing week values", len(bad_week), bad_week[:10])

    # --- 5. Missing or invalid dates ---
    bad_date = [r["id"] for r in rows if not DATE_RE.match(r["start_date"] or "")]
    hard_fail("5. Missing or invalid dates", len(bad_date), bad_date[:10])

    # --- 6. Missing away teams ---
    bad_away = [r["id"] for r in rows if not r["away_team"].strip()]
    hard_fail("6. Missing away teams", len(bad_away), bad_away[:10])

    # --- 7. Missing home teams ---
    bad_home = [r["id"] for r in rows if not r["home_team"].strip()]
    hard_fail("7. Missing home teams", len(bad_home), bad_home[:10])

    # --- 8. Same-team matchups ---
    same_team = [r["id"] for r in rows if r["away_team"] == r["home_team"]]
    hard_fail("8. Same-team matchups", len(same_team), same_team[:10])

    # --- 9. Invalid neutral-site values ---
    bad_neutral = [r["id"] for r in rows if r["neutral_site"] not in VALID_BOOL]
    hard_fail("9. Invalid neutral-site values", len(bad_neutral), bad_neutral[:10])

    # --- 10. Invalid completed values ---
    bad_completed = [r["id"] for r in rows if r["completed"] not in VALID_BOOL]
    hard_fail("10. Invalid completed values", len(bad_completed), bad_completed[:10])

    # --- Provenance: every row must trace to a raw ESPN file ---
    raw_ids = load_raw_event_ids()
    unprovenanced = [r["id"] for r in rows if r["id"] not in raw_ids]
    hard_fail("Provenance (row id found in raw_espn/scoreboard/*.json)", len(unprovenanced), unprovenanced[:10])

    # --- 19. Retained placeholder teams (hard failure, no championship exception) ---
    # A row "labeled a championship" (via its notes text) gets no pass here -
    # the check below only looks at the team-name columns themselves.
    placeholder_rows = [
        r["id"] for r in rows
        if PLACEHOLDER_NAME_RE.match(r["away_team"] or "") or PLACEHOLDER_NAME_RE.match(r["home_team"] or "")
    ]
    hard_fail("19. Retained placeholder teams (TBD / To Be Determined / Unknown)", len(placeholder_rows), placeholder_rows[:10])

    # Unresolved team identity = placeholder team name OR unresolved (blank)
    # conference on either side. "Every retained row must have two resolvable
    # real team identities" - conference resolution is part of that identity.
    unresolved_identity_rows = [
        r["id"] for r in rows
        if PLACEHOLDER_NAME_RE.match(r["away_team"] or "")
        or PLACEHOLDER_NAME_RE.match(r["home_team"] or "")
        or not r["away_conference"].strip()
        or not r["home_conference"].strip()
    ]
    hard_fail("19b. Unresolved team identities (placeholder team OR unresolved conference)", len(unresolved_identity_rows), unresolved_identity_rows[:10])

    # --- 11. Exact duplicate matchup/date combinations ---
    matchup_date = Counter((r["away_team"], r["home_team"], r["start_date"]) for r in rows)
    exact_dupes = {k: v for k, v in matchup_date.items() if v > 1}
    diagnostic("11. Exact duplicate matchup/date combinations", f"{len(exact_dupes)} found: {list(exact_dupes.items())[:10]}")

    swapped = Counter((frozenset([r["away_team"], r["home_team"]]), r["start_date"]) for r in rows)
    swapped_dupes = {k: v for k, v in swapped.items() if v > 1}
    diagnostic("11b. Same two teams same date (regardless of home/away order)", f"{len(swapped_dupes)} found: {list(swapped_dupes.items())[:10]}")

    # --- 12. Miami vs Miami (OH) identity separation ---
    miami_names = set()
    for r in rows:
        for col in ("away_team", "home_team"):
            if r[col].startswith("Miami"):
                miami_names.add(r[col])
    bad_miami = miami_names - {"Miami Hurricanes", "Miami (OH) RedHawks"}
    miami_count = sum(1 for r in rows if "Miami Hurricanes" in (r["away_team"], r["home_team"]))
    miami_oh_count = sum(1 for r in rows if "Miami (OH) RedHawks" in (r["away_team"], r["home_team"]))
    diagnostic(
        "12. Miami vs Miami (OH) identity separation",
        f"Distinct 'Miami*' labels found: {sorted(miami_names)} | "
        f"unexpected labels: {sorted(bad_miami)} | "
        f"Miami Hurricanes games: {miami_count} | Miami (OH) RedHawks games: {miami_oh_count}",
    )
    if bad_miami:
        hard_fail("12. Miami vs Miami (OH) identity separation (unexpected label variants)", len(bad_miami), sorted(bad_miami))

    # --- 13. North Dakota State inclusion and routing ---
    ndsu_rows = [r for r in rows if "North Dakota State" in r["away_team"] or "North Dakota State" in r["home_team"]]
    ndsu_bad_conf = [
        r["id"] for r in ndsu_rows
        if (r["away_team"] == "North Dakota State Bison" and r["away_conference"] != "Mountain West Conference")
        or (r["home_team"] == "North Dakota State Bison" and r["home_conference"] != "Mountain West Conference")
    ]
    diagnostic("13. North Dakota State inclusion and routing", f"{len(ndsu_rows)} games found; {len(ndsu_bad_conf)} misrouted (expected Mountain West Conference)")
    if not ndsu_rows:
        hard_fail("13. North Dakota State inclusion (must be > 0)", 1, "no NDSU games found")
    if ndsu_bad_conf:
        hard_fail("13. North Dakota State conference routing", len(ndsu_bad_conf), ndsu_bad_conf)

    # --- 14. Sacramento State inclusion and routing ---
    sacst_rows = [r for r in rows if "Sacramento State" in r["away_team"] or "Sacramento State" in r["home_team"]]
    sacst_bad_conf = [
        r["id"] for r in sacst_rows
        if (r["away_team"] == "Sacramento State Hornets" and r["away_conference"] != "Mid-American Conference")
        or (r["home_team"] == "Sacramento State Hornets" and r["home_conference"] != "Mid-American Conference")
    ]
    diagnostic("14. Sacramento State inclusion and routing", f"{len(sacst_rows)} games found; {len(sacst_bad_conf)} misrouted (expected Mid-American Conference)")
    if not sacst_rows:
        hard_fail("14. Sacramento State inclusion (must be > 0)", 1, "no Sacramento State games found")
    if sacst_bad_conf:
        hard_fail("14. Sacramento State conference routing", len(sacst_bad_conf), sacst_bad_conf)

    # --- 15. Team schedule counts ---
    team_counts = Counter()
    for r in rows:
        team_counts[r["away_team"]] += 1
        team_counts[r["home_team"]] += 1
    counts_only = sorted(team_counts.values())
    if counts_only:
        median = counts_only[len(counts_only) // 2]
    low = {t: c for t, c in team_counts.items() if c <= 2}
    high = {t: c for t, c in team_counts.items() if c >= 13}
    diagnostic(
        "15. Team schedule counts (all teams, incl. FCS opponents)",
        f"{len(team_counts)} teams; min={min(counts_only)} max={max(counts_only)} median={median} | "
        f"low (<=2 games, mostly FCS opponents that play only one FBS team - expected): {len(low)} teams | "
        f"high (>=13 games): {high}",
    )

    # Cross-reference against ESPN's structured FBS group-80 team roster
    # (raw_espn/conferences/group_80_teams.json) to separate genuine FBS
    # programs from non-competing exhibition/all-star entities ESPN also
    # tags under the FBS group (e.g. "East All-Stars", "Team Gaither").
    fbs_teams_path = os.path.join(REPO_ROOT, "raw_espn", "conferences", "group_80_teams.json")
    if os.path.exists(fbs_teams_path):
        with open(fbs_teams_path) as f:
            fbs_teams_raw = json.load(f)
        fbs_ids = set()
        for item in fbs_teams_raw.get("items", []):
            m = re.search(r"/teams/(\d+)\?", item["$ref"])
            if m:
                fbs_ids.add(m.group(1))

        id_to_name = {}
        for fn in os.listdir(RAW_SCOREBOARD_DIR):
            with open(os.path.join(RAW_SCOREBOARD_DIR, fn)) as f:
                data = json.load(f)
            for e in data.get("events", []):
                for c in e["competitions"][0]["competitors"]:
                    tid = str(c["team"].get("id"))
                    if tid in fbs_ids:
                        id_to_name[tid] = c["team"].get("displayName")

        fbs_names = set(id_to_name.values())
        zero_game_ids = fbs_ids - set(id_to_name.keys())
        fbs_low = {n: team_counts.get(n, 0) for n in fbs_names if team_counts.get(n, 0) < 10}
        fbs_high = {n: team_counts.get(n, 0) for n in fbs_names if team_counts.get(n, 0) > 13}
        diagnostic(
            "15b. FBS-roster-verified team schedule counts",
            f"{len(fbs_ids)} entries in ESPN's FBS group-80 roster; {len(zero_game_ids)} are non-competing "
            f"exhibition/all-star placeholders with zero 2026 games (ids: {sorted(zero_game_ids)}); "
            f"{len(fbs_names)} genuine FBS programs have >=1 game in the final file; "
            f"FBS programs with <10 games: {fbs_low or 'none'}; FBS programs with >13 games: {fbs_high or 'none'}",
        )

    # --- 16 & 17: retrieval log based checks ---
    retrieval_rows = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, newline="") as f:
            retrieval_rows = list(csv.DictReader(f))

    successful = [r for r in retrieval_rows if r["http_status"] == "200" and r["week"].strip() and "scoreboard" in r["request_url"]]
    by_type = defaultdict(set)
    for r in successful:
        by_type[r["season_type"]].add(int(r["week"]))

    diagnostic("16. Weeks successfully retrieved", f"season_type -> weeks: { {k: sorted(v) for k, v in by_type.items()} }")

    gaps = {}
    for season_type, weeks in by_type.items():
        if not weeks:
            continue
        expected = set(range(min(weeks), max(weeks) + 1))
        missing = expected - weeks
        if missing:
            gaps[season_type] = sorted(missing)
    reg_weeks = by_type.get("2", set())
    if reg_weeks and reg_weeks != set(range(1, 16)):
        gaps["2_expected_1_15"] = sorted(set(range(1, 16)) - reg_weeks)
    diagnostic("17. Unexpected gaps in weekly retrieval sequence", f"{gaps if gaps else 'none - all expected weeks present'}")
    if gaps:
        hard_fail("17. Unexpected gaps in weekly retrieval sequence", sum(len(v) for v in gaps.values()), gaps)

    # --- 18. Rows excluded from the final file ---
    if os.path.exists(BUILD_LOG_PATH):
        with open(BUILD_LOG_PATH) as f:
            build_log = json.load(f)
        diagnostic(
            "18. Rows excluded from the final file",
            f"excluded_count={build_log.get('excluded_count')} by_category={build_log.get('excluded_by_category')}",
        )
    else:
        diagnostic("18. Rows excluded from the final file", "raw_espn/build_log.json not found")

    # --- 20. Week 0 normalization ---
    week_zero_rows = [r for r in rows if r["start_date"] in WEEK_ZERO_DATES]
    misrouted_to_nonzero = [r["id"] for r in week_zero_rows if r["week"] != "0"]
    hard_fail(
        "20. All 2026-08-29 / 2026-08-30 games route to Week 0",
        len(misrouted_to_nonzero), misrouted_to_nonzero,
    )

    on_or_after_cutoff_week_zero = [
        r["id"] for r in rows if r["start_date"] >= WEEK_ZERO_CUTOFF_DATE and r["week"] == "0"
    ]
    hard_fail(
        "20b. No game on/after 2026-09-03 is misrouted to Week 0",
        len(on_or_after_cutoff_week_zero), on_or_after_cutoff_week_zero,
    )

    earliest_date = min((r["start_date"] for r in rows), default=None)
    sept3_rows = [r for r in rows if r["start_date"] == WEEK_ZERO_CUTOFF_DATE]
    sept3_not_week1 = [r["id"] for r in sept3_rows if r["week"] != "1"]
    hard_fail("20c. 2026-09-03 games begin Week 1", len(sept3_not_week1), sept3_not_week1)
    diagnostic(
        "20d. Week 0 / Week 1 boundary",
        f"{len(week_zero_rows)} Week 0 rows (dates {sorted(WEEK_ZERO_DATES)}); "
        f"{len(sept3_rows)} rows on {WEEK_ZERO_CUTOFF_DATE} (first normalized Week 1 date); "
        f"earliest retained date overall: {earliest_date}.",
    )

    # Explicit named opening-weekend examples.
    example_results = []
    for away_sub, home_sub in WEEK_ZERO_EXAMPLES:
        matches = [
            r for r in rows
            if away_sub.lower() in r["away_team"].lower() and home_sub.lower() in r["home_team"].lower()
        ]
        if not matches:
            example_results.append((f"{away_sub} @ {home_sub}", "NOT FOUND", None))
        else:
            for m in matches:
                example_results.append((f"{m['away_team']} @ {m['home_team']}", m["week"], m["start_date"]))
    bad_examples = [e for e in example_results if e[1] != "0"]
    hard_fail("20e. Named Week 0 opening-weekend examples all resolve to week=0", len(bad_examples), bad_examples)
    diagnostic("20f. Named Week 0 example resolution", example_results)

    # --- Report ---
    print("=" * 70)
    print("HARD-FAIL CHECKS (must all be 0 / empty)")
    print("=" * 70)
    all_pass = True
    for check, count, detail in HARD_FAILS:
        status = "PASS" if not count else "FAIL"
        if count:
            all_pass = False
        print(f"[{status}] {check}: {count}")
        if count and detail:
            print(f"       detail: {detail}")

    print()
    print("=" * 70)
    print("DIAGNOSTIC / REPORTING CHECKS")
    print("=" * 70)
    for check, message in DIAGNOSTICS:
        print(f"- {check}: {message}")

    print()
    if all_pass:
        print("RESULT: ALL HARD-FAIL CHECKS PASSED")
    else:
        print("RESULT: ONE OR MORE HARD-FAIL CHECKS FAILED")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
