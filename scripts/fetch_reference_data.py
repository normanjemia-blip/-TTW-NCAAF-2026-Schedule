"""
Fetch ESPN structured reference data for the 2026 college-football season:
  - Season types (Preseason/Regular/Postseason) and their weeks (number, dates)
  - Conference (group) ID -> name mapping for FBS (group 80) and FCS (group 81)

All raw responses are saved untouched under raw_espn/. Output summaries are
written as JSON files consumed by fetch_schedule_data.py and build_schedule_csv.py.
"""
import json
import os
import sys

from http_utils import fetch_json, save_raw, append_log_row, now_iso

SEASON = 2026
CORE_BASE = "https://sports.core.api.espn.com/v2/sports/football/leagues/college-football"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)


def log(url, season_type, week, status, raw_count, parsed_count, retries, notes):
    append_log_row({
        "retrieved_at": now_iso(),
        "request_url": url,
        "season": SEASON,
        "season_type": season_type,
        "week": week,
        "http_status": status if status is not None else "ERROR",
        "raw_event_count": raw_count,
        "parsed_event_count": parsed_count,
        "retry_count": retries,
        "notes": notes,
    })


def fetch_and_save(url, subdir, filename, season_type="", week=""):
    status, parsed, raw_text, retries, notes = fetch_json(url, season=SEASON, season_type=season_type, week=week)
    save_raw(subdir, filename, raw_text)
    if status != 200 or parsed is None:
        log(url, season_type, week, status, "", "", retries, f"REFERENCE FETCH FAILED: {notes}")
        print(f"BLOCKER: failed to retrieve {url} -> status={status} notes={notes}", file=sys.stderr)
        sys.exit(1)
    log(url, season_type, week, status, "", "", retries, notes or "reference data OK")
    return parsed


def main():
    season_types = {}  # type_id -> {name, abbreviation, weeks: [{number, text, startDate, endDate}]}

    for type_id in (1, 2, 3):
        type_url = f"{CORE_BASE}/seasons/{SEASON}/types/{type_id}?lang=en&region=us"
        type_data = fetch_and_save(type_url, "metadata", f"season_type_{type_id}.json", season_type=type_id)

        weeks_list_url = f"{CORE_BASE}/seasons/{SEASON}/types/{type_id}/weeks?lang=en&region=us&limit=50"
        weeks_list = fetch_and_save(weeks_list_url, "metadata", f"season_type_{type_id}_weeks.json", season_type=type_id)

        weeks = []
        for item in weeks_list.get("items", []):
            week_url = item["$ref"]
            # week number is embedded at the end of the ref path
            week_num = week_url.split("/weeks/")[1].split("?")[0]
            week_filename = f"season_type_{type_id}_week_{week_num}.json"
            week_data = fetch_and_save(week_url, "metadata", week_filename, season_type=type_id, week=week_num)
            weeks.append({
                "number": week_data.get("number"),
                "text": week_data.get("text"),
                "startDate": week_data.get("startDate"),
                "endDate": week_data.get("endDate"),
            })

        season_types[type_id] = {
            "name": type_data.get("name"),
            "abbreviation": type_data.get("abbreviation"),
            "startDate": type_data.get("startDate"),
            "endDate": type_data.get("endDate"),
            "weeks": weeks,
        }

    with open(os.path.join(REPO_ROOT, "raw_espn", "season_types_weeks_summary.json"), "w") as f:
        json.dump(season_types, f, indent=2)
    print("Season types/weeks summary written.")

    # --- Conference reference map (FBS group 80 + FCS group 81) ---
    conference_map = {}  # conferenceId (str) -> {name, slug, division}

    for group_id, division in ((80, "FBS"), (81, "FCS")):
        group_url = f"{CORE_BASE}/seasons/{SEASON}/types/2/groups/{group_id}?lang=en&region=us"
        group_data = fetch_and_save(group_url, "conferences", f"group_{group_id}.json")

        children_url = f"{CORE_BASE}/seasons/{SEASON}/types/2/groups/{group_id}/children?lang=en&region=us&limit=100"
        children_list = fetch_and_save(children_url, "conferences", f"group_{group_id}_children.json")

        for item in children_list.get("items", []):
            child_url = item["$ref"]
            child_id = child_url.split("/groups/")[1].split("?")[0]
            child_filename = f"group_{group_id}_child_{child_id}.json"
            child_data = fetch_and_save(child_url, "conferences", child_filename)
            conference_map[child_id] = {
                "name": child_data.get("name"),
                "slug": child_data.get("slug"),
                "division": division,
            }

    with open(os.path.join(REPO_ROOT, "raw_espn", "conference_map.json"), "w") as f:
        json.dump(conference_map, f, indent=2)
    print(f"Conference map written with {len(conference_map)} conferences.")


if __name__ == "__main__":
    main()
