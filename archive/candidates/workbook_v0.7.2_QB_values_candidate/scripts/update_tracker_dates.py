#!/usr/bin/env python3
"""Phase 8.3: add ISO date fields to the exception tracker and record the
Vanderbilt re-verification result.

- Reads the v0.7.1 tracker JSON (source of truth for the 33 records).
- Adds 4 machine-readable ISO (YYYY-MM-DD) fields per record:
    last_checked_date, most_recent_source_date, next_research_date, resolution_date
- Does NOT invent publication dates: most_recent_source_date is blank unless a
  precise date is actually known (only Vanderbilt, whose fresh sources are
  dated SEC Media Days 2026-07-21). Existing descriptive source text is kept.
- Updates ONLY the Vanderbilt record's descriptive fields to reflect the
  Phase 8.3 re-verification (genuine Curtis/Berlowitz competition -> stays L).
  All other 32 records keep their existing data verbatim; only the 4 date
  fields are appended.
- Writes updated CSV + JSON into the v0.7.2 folder.
"""
import json, csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
SRC = os.path.join(OUT, "..", "workbook_v0.7.1_QB_values_working",
                   "qb_exception_resolution_tracker.json")

data = json.load(open(SRC))
records = data["records"]

# ---- date logic -----------------------------------------------------------
RESEARCH_DATE = "2026-07-21"   # when the Phase 8/8.1 tracker research was done
EARLY_FALL_CAMP = "2026-08-03" # early fall camp / first depth-chart week
# per-team medical checkpoints for injury cases
INJURY_NEXT = {
    "UNC":  "2026-08-03",  # Edwards PCL: fall-camp injury clearance / first depth chart
    "TTU":  "2026-08-21",  # Hammond ACL medical clearance checkpoint (~Aug 21)
    "STAN": "2026-08-03",  # Warren ACL recovery update at fall camp
    "SYR":  "2026-08-03",  # Angeli Achilles recovery update at fall camp
}

def next_research_date(r):
    ab = r["abbrev"]
    cat = r["current_category"]
    if cat == "injury/availability":
        return INJURY_NEXT.get(ab, EARLY_FALL_CAMP)
    # open competition + conflicting/insufficient sourcing both first resolve
    # at early fall camp / first official depth chart / next coach availability
    return EARLY_FALL_CAMP

for r in records:
    # last checked = tracker research date (Vanderbilt overridden below)
    r["last_checked_date"] = RESEARCH_DATE
    # exact source date unavailable for the "(2026 offseason)" previews -> blank
    r["most_recent_source_date"] = ""
    r["next_research_date"] = next_research_date(r)
    # nothing is resolved yet
    r["resolution_date"] = ""

# ---- Vanderbilt Phase 8.3 re-verification (FAILED) ------------------------
for r in records:
    if r["abbrev"] != "VAN":
        continue
    r["current_leader"] = ""  # HC has not named a starter (undecided)
    r["current_candidates"] = ("Jared Curtis (five-star true Fr) | "
                               "Blaze Berlowitz (2 yrs in OC Tim Beck's system; Pavia's 2025 backup)")
    r["baseline_qb_assumption"] = ("Not established — genuine open competition (Curtis vs Berlowitz); "
                                   "HC has not named a starter")
    r["condition_to_clear"] = ("Official depth chart or HC naming of QB1 (Curtis or Berlowitz), "
                               "or a clear 2+ source consensus once camp resolves")
    r["next_research_checkpoint"] = ("Fall camp early-Aug 2026; HC availability; game-week depth chart "
                                     "(competition may run to the opener vs Austin Peay)")
    r["most_recent_source"] = "WSMV / Yahoo Sports / Saturday Down South (Vanderbilt SEC Media Days)"
    r["most_recent_source_url"] = ("https://www.wsmv.com/2026/07/21/"
                                   "vanderbilt-qb-competition-headlines-commodores-sec-media-days-session/")
    r["eligible_for_zero_init"] = ("N — stays L / UNCERTAIN; Phase 8.3 re-verification found a genuine "
                                   "competition, not an uncontested projected starter")
    r["requires_proposed_nonzero_deviation"] = ("TBD once resolved — likely 0 if the winner is the "
                                                "priced-in projected starter")
    r["notes"] = ("PHASE 8.3 RE-VERIFICATION (2026-07-22): the Phase 8.2 recommendation to reclassify "
                  "VAN to Medium and zero-init was REJECTED. Fresh sourcing (Clark Lea at Vanderbilt's "
                  "SEC Media Days session, 2026-07-21) confirms an ongoing Curtis vs Berlowitz "
                  "competition that may not be decided before the opener; Berlowitz is a genuine veteran "
                  "competitor (two seasons in OC Tim Beck's system, Diego Pavia's backup), not a mere "
                  "backup, and Lea declined to name a starter. Fails both 'uncontested by a genuine equal "
                  "competitor' and 'consistently projected Day-1 starter.' Vanderbilt stays L / UNCERTAIN "
                  "— NOT reclassified, NOT initialized. See vanderbilt_verification_note.md.")
    r["last_checked_date"] = "2026-07-22"      # re-verified today
    r["most_recent_source_date"] = "2026-07-21"  # SEC Media Days (precise date known)
    r["next_research_date"] = EARLY_FALL_CAMP
    r["resolution_date"] = ""

# ---- column order (date fields next to their descriptive counterparts) -----
COLS = ["team","abbrev","conference","current_category","current_confidence",
        "current_candidates","current_leader","baseline_qb_assumption",
        "condition_to_clear","best_source_types",
        "most_recent_source","most_recent_source_url","most_recent_source_date",
        "next_research_checkpoint","next_research_date","last_checked_date",
        "final_resolution","resolution_source","resolution_date",
        "confidence_after_resolution","eligible_for_zero_init",
        "requires_proposed_nonzero_deviation","notes"]

# sanity: every record has exactly these keys
for r in records:
    missing = set(COLS) - set(r.keys()); extra = set(r.keys()) - set(COLS)
    assert not missing and not extra, f"{r['abbrev']}: missing={missing} extra={extra}"

csv_path = os.path.join(OUT, "qb_exception_resolution_tracker.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    for r in records:
        w.writerow({k: r[k] for k in COLS})

data["generated"] = "2026-07-22"
data["date_fields_added"] = ["last_checked_date","most_recent_source_date",
                             "next_research_date","resolution_date"]
data["date_field_notes"] = ("ISO YYYY-MM-DD. most_recent_source_date is blank where the exact "
                            "publication date was unavailable (descriptive source text retained). "
                            "next_research_date: open competition & conflicting sourcing -> early fall "
                            "camp / first depth chart (2026-08-03); injury -> medical checkpoint "
                            "(TTU 2026-08-21; others 2026-08-03). resolution_date blank until resolved.")
data["records"] = records
json_path = os.path.join(OUT, "qb_exception_resolution_tracker.json")
json.dump(data, open(json_path, "w"), indent=1, ensure_ascii=False)

# ---- report ---------------------------------------------------------------
from collections import Counter
print("records:", len(records))
print("columns:", len(COLS))
print("by category:", dict(Counter(r["current_category"] for r in records)))
print("next_research_date distribution:", dict(Counter(r["next_research_date"] for r in records)))
print("most_recent_source_date non-blank:",
      [r["abbrev"] for r in records if r["most_recent_source_date"]])
print("last_checked 2026-07-22:", [r["abbrev"] for r in records if r["last_checked_date"]=="2026-07-22"])
print("VAN confidence:", next(r["current_confidence"] for r in records if r["abbrev"]=="VAN"))
