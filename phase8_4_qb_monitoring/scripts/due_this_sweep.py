#!/usr/bin/env python3
"""List exception-tracker rows due for a sweep on/before a given date.

Usage: python3 due_this_sweep.py 2026-08-03
Reads the v0.7.2 tracker (source of truth) and prints the still-UNCERTAIN rows
whose next_research_date <= the sweep date, grouped by category, so each sweep
touches only the teams that are actually due. Read-only; changes nothing.
"""
import sys, os, json, signal
from collections import defaultdict

# tolerate `| head` and other truncated pipes cleanly
try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
TRACKER = os.path.join(HERE, "..", "..", "workbook_v0.7.2_QB_values_candidate",
                       "qb_exception_resolution_tracker.json")

def main():
    if len(sys.argv) != 2:
        print("usage: due_this_sweep.py YYYY-MM-DD"); sys.exit(2)
    sweep = sys.argv[1]
    data = json.load(open(TRACKER))
    due = defaultdict(list)
    for r in data["records"]:
        nrd = r.get("next_research_date", "")
        if nrd and nrd <= sweep:
            due[r["current_category"]].append((r["abbrev"], r["team"], nrd))
    total = sum(len(v) for v in due.values())
    print(f"Sweep date: {sweep}")
    print(f"Exceptions due (next_research_date <= {sweep}): {total}")
    for cat in ["open competition", "injury/availability", "conflicting/insufficient sourcing"]:
        rows = sorted(due.get(cat, []))
        if rows:
            print(f"\n  [{cat}] {len(rows)}")
            for ab, team, nrd in rows:
                print(f"    {ab:5s} {team:22s} due {nrd}")
    not_due = [r["abbrev"] for r in data["records"]
               if r.get("next_research_date", "") and r["next_research_date"] > sweep]
    if not_due:
        print(f"\n  Not yet due (> {sweep}): {', '.join(sorted(not_due))}")

if __name__ == "__main__":
    main()
