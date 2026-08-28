"""
Fetch ESPN structured scoreboard data for every 2026 college-football week
(Preseason/Week-0 window, full regular season, postseason/conference-championship
window) using the site.api scoreboard endpoint filtered to the FBS group (80),
which ESPN's own group tree associates with any game involving at least one
FBS team (including FBS-vs-FCS games and the FCS-to-FBS reclassifiers
North Dakota State and Sacramento State, both of which ESPN already places
under FBS conference groups for 2026 - see raw_espn/conference_map.json).

Retrieval method notes (established via live testing against the ESPN API,
recorded here for reproducibility):
  - The scoreboard endpoint's `week=` query parameter silently truncates
    results to 25 events regardless of the true weekly game count.
  - The `dates=YYYYMMDD-YYYYMMDD` range parameter returns complete results,
    but a `limit` value above ~500 also silently truncates to 25.
  - Using `dates=<week start>-<week end>` (from ESPN's own week metadata)
    together with `limit=300` (safely above any observed weekly game count,
    well below the truncation threshold) returns the full, correct event
    list, cross-validated against the core API's authoritative per-week
    event counts during manual investigation.

Every raw HTTP response is saved untouched to raw_espn/scoreboard/. Every
request is logged to retrieval_log.csv, including retries and any
short/malformed responses.
"""
import json
import os
import sys

from http_utils import fetch_json, save_raw, append_log_row, now_iso

SEASON = 2026
SITE_BASE = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
LIMIT = 300
GROUPS = 80  # ESPN structured FBS grouping

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)


def ymd(iso_str):
    # '2026-08-22T07:00Z' -> '20260822'
    return iso_str[:10].replace("-", "")


def main():
    with open(os.path.join(REPO_ROOT, "raw_espn", "season_types_weeks_summary.json")) as f:
        season_types = json.load(f)

    plan = []  # list of (season_type_id, week_number, start_date, end_date)
    for type_id_str, info in season_types.items():
        type_id = int(type_id_str)
        for w in info["weeks"]:
            plan.append((type_id, w["number"], w["startDate"], w["endDate"]))

    plan.sort(key=lambda x: (x[0], x[1]))

    results_index = []  # summary of what was retrieved, for the parser + reconciliation

    for season_type, week_num, start_date, end_date in plan:
        date_range = f"{ymd(start_date)}-{ymd(end_date)}"
        url = f"{SITE_BASE}?dates={date_range}&groups={GROUPS}&limit={LIMIT}"

        status, parsed, raw_text, retries, notes = fetch_json(
            url, season=SEASON, season_type=season_type, week=week_num
        )

        filename = f"type{season_type}_week{week_num}.json"
        save_raw("scoreboard", filename, raw_text)

        if status != 200 or parsed is None:
            append_log_row({
                "retrieved_at": now_iso(),
                "request_url": url,
                "season": SEASON,
                "season_type": season_type,
                "week": week_num,
                "http_status": status if status is not None else "ERROR",
                "raw_event_count": "",
                "parsed_event_count": "",
                "retry_count": retries,
                "notes": f"BLOCKER: {notes}",
            })
            print(f"BLOCKER: failed to retrieve season_type={season_type} week={week_num}: {notes}", file=sys.stderr)
            sys.exit(1)

        events = parsed.get("events", [])
        raw_event_count = len(events)

        # A response matching the known truncation-bug value (25) is flagged
        # for manual review rather than silently accepted.
        suspicious = raw_event_count == 25
        note_extra = ""
        if suspicious:
            note_extra = "CAUTION: raw_event_count == 25 matches known truncation-bug value; verify manually"

        append_log_row({
            "retrieved_at": now_iso(),
            "request_url": url,
            "season": SEASON,
            "season_type": season_type,
            "week": week_num,
            "http_status": status,
            "raw_event_count": raw_event_count,
            "parsed_event_count": raw_event_count,  # all well-formed events parse; malformed handled in build step
            "retry_count": retries,
            "notes": note_extra or "OK",
        })

        results_index.append({
            "season_type": season_type,
            "week": week_num,
            "date_range": date_range,
            "raw_event_count": raw_event_count,
            "file": filename,
        })

        print(f"season_type={season_type} week={week_num} range={date_range} -> {raw_event_count} events (status {status}, retries {retries})")

    with open(os.path.join(REPO_ROOT, "raw_espn", "scoreboard_retrieval_index.json"), "w") as f:
        json.dump(results_index, f, indent=2)

    print(f"\nDone. {len(results_index)} week-requests retrieved.")


if __name__ == "__main__":
    main()
