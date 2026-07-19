"""
Parse the raw ESPN scoreboard responses saved under raw_espn/scoreboard/ into
TTW_2026_Verified_Schedule_ESPN_v1.0.csv.

Inclusion / exclusion rules (see TTW_2026_Schedule_Reconciliation_Report.md for
full accounting):

  1. Every event was retrieved with ESPN's structured FBS grouping (group 80),
     which ESPN associates with any game involving at least one FBS team -
     including FBS-vs-FCS games and North Dakota State / Sacramento State,
     both of which ESPN already places under FBS conference groups for 2026.
  2. Placeholder ("TBD") participants:
       - If the event is an officially scheduled conference championship game
         (identified by ESPN's own event notes headline containing
         "Championship"), it is RETAINED with both team columns marked
         "TBD (Home)" / "TBD (Away)" - per project instructions these games
         must be retained even though the two participants are not yet known.
       - Any other placeholder-participant game (bowl games, CFP games, or any
         other not-yet-determined-opponent regular-season game) is EXCLUDED,
         because the participating teams are not yet known and the project
         instructions explicitly forbid fabricating or including such
         placeholders outside the conference-championship exception.
  3. North Dakota State (ESPN team id 2449) and Sacramento State (ESPN team id
     16) have their conference column forced to the approved 2026 assignments
     (Mountain West / Mid-American) regardless of what ESPN reports, with the
     original ESPN-reported value logged to Notes and the reconciliation
     report whenever it differs.
  4. Events are de-duplicated by ESPN event id across all retrieved files.
"""
import csv
import json
import glob
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
SEASON = 2026

# Approved 2026 conference assignments for FCS-to-FBS reclassifying teams.
RECLASSIFIER_OVERRIDES = {
    "2449": {"team_name": "North Dakota State", "conference": "Mountain West Conference"},
    "16": {"team_name": "Sacramento State", "conference": "Mid-American Conference"},
}

# Slug aliases needed to resolve conference-championship headline text
# ("SEC Championship", "Conference USA Championship", ...) to the conference
# names ESPN itself returned in raw_espn/conference_map.json.
HEADLINE_SLUG_ALIASES = {
    "conference usa": "cusa",
}


def slugify(label):
    s = label.lower().strip()
    s = HEADLINE_SLUG_ALIASES.get(s, s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def load_conference_map():
    with open(os.path.join(REPO_ROOT, "raw_espn", "conference_map.json")) as f:
        return json.load(f)


def build_championship_conference_lookup(conference_map):
    """slug -> full conference name, for resolving championship headlines."""
    lookup = {}
    for conf_id, info in conference_map.items():
        if info["division"] != "FBS":
            continue
        lookup[info["slug"]] = info["name"]
    return lookup


def resolve_headline_conference(headline, champ_lookup):
    label = headline.replace(" Championship", "").strip()
    slug = slugify(label)
    return champ_lookup.get(slug)


def team_conference(team, conference_map):
    team_id = str(team.get("id"))
    if team_id in RECLASSIFIER_OVERRIDES:
        override = RECLASSIFIER_OVERRIDES[team_id]
        espn_conf_id = team.get("conferenceId")
        espn_conf_name = conference_map.get(str(espn_conf_id), {}).get("name") if espn_conf_id is not None else None
        if espn_conf_name == override["conference"]:
            note = f"{override['team_name']}: ESPN structured conferenceId already matches approved 2026 assignment ({override['conference']})."
        else:
            note = (
                f"{override['team_name']}: approved 2026 assignment ({override['conference']}) applied; "
                f"ESPN reported conferenceId={espn_conf_id} ({espn_conf_name or 'unresolved'})."
            )
        return override["conference"], note

    conf_id = team.get("conferenceId")
    if conf_id is None:
        return "", f"UNRESOLVED CONFERENCE: {team.get('displayName')} has no ESPN conferenceId."
    conf = conference_map.get(str(conf_id))
    if conf is None:
        return "", f"UNRESOLVED CONFERENCE: {team.get('displayName')} conferenceId={conf_id} not found in ESPN conference map."
    return conf["name"], ""


def main():
    conference_map = load_conference_map()
    champ_lookup = build_championship_conference_lookup(conference_map)

    seen_event_ids = set()
    rows = []
    excluded = []  # (event_id, reason_category, detail)
    duplicate_source_files = []

    files = sorted(glob.glob(os.path.join(REPO_ROOT, "raw_espn", "scoreboard", "type*_week*.json")))

    for fn in files:
        with open(fn) as f:
            data = json.load(f)
        for event in data.get("events", []):
            event_id = event["id"]

            if event_id in seen_event_ids:
                duplicate_source_files.append((event_id, fn))
                continue
            seen_event_ids.add(event_id)

            season_year = event.get("season", {}).get("year")
            if season_year != SEASON:
                excluded.append((event_id, "wrong_season", f"season.year={season_year}"))
                continue

            week_number = event.get("week", {}).get("number")
            comp = event["competitions"][0]

            competitors = {c["homeAway"]: c for c in comp["competitors"]}
            if "home" not in competitors or "away" not in competitors:
                excluded.append((event_id, "malformed_competitors", "missing home/away competitor"))
                continue

            home_team = competitors["home"]["team"]
            away_team = competitors["away"]["team"]

            home_is_placeholder = str(home_team.get("id")).startswith("-")
            away_is_placeholder = str(away_team.get("id")).startswith("-")

            notes_list = comp.get("notes") or []
            headline = notes_list[0]["headline"] if notes_list else ""
            # A genuine conference championship headline resolves to one of
            # ESPN's own FBS conference names (e.g. "SEC Championship" ->
            # "Southeastern Conference"). CFP / bowl headlines also contain
            # the word "Championship" (e.g. "College Football Playoff
            # National Championship") but do not resolve to a conference,
            # so they correctly fall through to the bowl/playoff exclusion.
            is_championship = (
                "Championship" in headline
                and "College Football Playoff" not in headline
                and resolve_headline_conference(headline, champ_lookup) is not None
            )

            if (home_is_placeholder or away_is_placeholder):
                if not is_championship:
                    excluded.append((
                        event_id, "placeholder_participant_non_championship",
                        f"headline='{headline}' date={event.get('date')} "
                        f"home={home_team.get('displayName')} away={away_team.get('displayName')}"
                    ))
                    continue

            row_notes = []

            if is_championship and home_is_placeholder and away_is_placeholder:
                champ_conf_name = resolve_headline_conference(headline, champ_lookup)
                away_team_name = "TBD (Away)"
                home_team_name = "TBD (Home)"
                away_conf = champ_conf_name or ""
                home_conf = champ_conf_name or ""
                if not champ_conf_name:
                    row_notes.append(f"UNRESOLVED CHAMPIONSHIP CONFERENCE for headline '{headline}'")
                row_notes.append(
                    f"Officially scheduled conference championship game; participating teams not yet "
                    f"determined (to be decided by regular-season standings). ESPN headline: '{headline}'."
                )
            else:
                away_team_name = away_team.get("displayName")
                home_team_name = home_team.get("displayName")
                away_conf, away_note = team_conference(away_team, conference_map)
                home_conf, home_note = team_conference(home_team, conference_map)
                if away_note:
                    row_notes.append(away_note)
                if home_note:
                    row_notes.append(home_note)
                if headline:
                    row_notes.append(f"ESPN event note: {headline}")

            if not away_team_name or not home_team_name:
                excluded.append((event_id, "missing_team_name", f"away={away_team_name} home={home_team_name}"))
                continue

            if away_team_name == home_team_name and not is_championship:
                excluded.append((event_id, "same_team_matchup", f"{away_team_name} vs {home_team_name}"))
                continue

            start_date_raw = event.get("date", "")
            if len(start_date_raw) < 10:
                excluded.append((event_id, "missing_or_invalid_date", f"date={start_date_raw}"))
                continue
            start_date = start_date_raw[:10]

            status = comp.get("status", {}).get("type", {})
            completed = bool(status.get("completed", False))

            away_points = ""
            home_points = ""
            if completed:
                away_points = competitors["away"].get("score", "")
                home_points = competitors["home"].get("score", "")

            neutral_site = comp.get("neutralSite")
            if neutral_site is None:
                excluded.append((event_id, "missing_neutral_site_flag", ""))
                continue

            venue = comp.get("venue", {}).get("fullName", "") if comp.get("venue") else ""

            rows.append({
                "id": event_id,
                "season": SEASON,
                "week": week_number,
                "start_date": start_date,
                "neutral_site": "TRUE" if neutral_site else "FALSE",
                "away_team": away_team_name,
                "away_conference": away_conf,
                "home_team": home_team_name,
                "home_conference": home_conf,
                "away_points": away_points,
                "home_points": home_points,
                "completed": "TRUE" if completed else "FALSE",
                "venue": venue,
                "notes": " | ".join(row_notes),
            })

    # Sort for stable, readable output.
    rows.sort(key=lambda r: (r["season"], r["week"], r["start_date"], r["id"]))

    out_path = os.path.join(REPO_ROOT, "TTW_2026_Verified_Schedule_ESPN_v1.0.csv")
    columns = ["id", "season", "week", "start_date", "neutral_site", "away_team", "away_conference",
               "home_team", "home_conference", "away_points", "home_points", "completed", "venue", "notes"]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    # Write an exclusion / build log for the reconciliation report + validator.
    build_log = {
        "total_raw_events_scanned": len(seen_event_ids) + sum(1 for _ in duplicate_source_files),
        "unique_events_scanned": len(seen_event_ids),
        "retained_rows": len(rows),
        "excluded_count": len(excluded),
        "excluded_by_category": {},
        "excluded_events": [
            {"event_id": e[0], "category": e[1], "detail": e[2]} for e in excluded
        ],
        "duplicate_source_occurrences": duplicate_source_files,
    }
    for _, cat, _ in excluded:
        build_log["excluded_by_category"][cat] = build_log["excluded_by_category"].get(cat, 0) + 1

    with open(os.path.join(REPO_ROOT, "raw_espn", "build_log.json"), "w") as f:
        json.dump(build_log, f, indent=2)

    print(f"Wrote {len(rows)} rows to {out_path}")
    print(f"Excluded {len(excluded)} events:")
    for cat, count in build_log["excluded_by_category"].items():
        print(f"  {cat}: {count}")
    if duplicate_source_files:
        print(f"Duplicate event-id occurrences across source files: {len(duplicate_source_files)}")


if __name__ == "__main__":
    main()
