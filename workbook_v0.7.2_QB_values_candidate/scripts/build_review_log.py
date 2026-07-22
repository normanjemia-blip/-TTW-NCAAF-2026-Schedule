#!/usr/bin/env python3
"""Build the EMPTY QB deviation review log (headers + schema only).

No fictional adjustment records are written. This creates the header-only
CSV and a JSON that carries the schema, per-field documentation, and the
validation rules. The log is a SEPARATE future-use file from the exception
tracker (which does not contain review-log columns).
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

# 28-field schema, in the exact order supplied in the Phase 8.3 instruction.
COLUMNS = [
    "Team",
    "Abbrev",
    "Baseline QB",
    "Active QB",
    "Applied deviation",
    "Effective date",
    "Trigger",
    "Adjustment classification",
    "Evidence summary",
    "Primary source",
    "Primary source date",
    "Secondary source",
    "Secondary source date",
    "Injury confirmed for week",
    "Starts by active QB",
    "Three-start review due",
    "Three-start review completed",
    "TEAM RATINGS movement reviewed",
    "Double-counting risk",
    "Review action",
    "Previous deviation",
    "Revised deviation",
    "Review date",
    "Reviewer",
    "Reason",
    "Reset date",
    "Status",
]

# Per-field documentation + validation rules (no data rows).
FIELD_DOC = {
    "Team": "Full team name (e.g., 'Vanderbilt'). Required. Must match the workbook's QB VALUES team name.",
    "Abbrev": "Canonical abbreviation (e.g., 'VAN'). Required. Must match QB VALUES!A.",
    "Baseline QB": "The team's preseason baseline quarterback (the zero reference). Text.",
    "Active QB": "The quarterback the Active value describes. Text.",
    "Applied deviation": "The Active value entered in QB VALUES!F. Must be one of the discrete quarter-point values in future_qb_deviation_rubric.md §2 and within -4.00..+2.00.",
    "Effective date": "ISO YYYY-MM-DD the deviation takes effect (the game week / date it first applies).",
    "Trigger": "What caused the entry: e.g., 'injury', 'depth-chart change', 'competition resolved', 'transfer', 'benching'.",
    "Adjustment classification": "One of: functionally equivalent replacement | minor downgrade | clear downgrade | major downgrade | extreme elite-to-unproven downgrade | modest upgrade | clear upgrade | exceptional upgrade.",
    "Evidence summary": "One-line summary of the written baseline-vs-active comparison (see rubric §3, 9 factors).",
    "Primary source": "Primary credible source (official depth chart / HC or OC statement / established beat writer).",
    "Primary source date": "ISO YYYY-MM-DD of the primary source. Leave blank if the exact date is unavailable.",
    "Secondary source": "Second independent source (required for disputed situations per rubric §3).",
    "Secondary source date": "ISO YYYY-MM-DD of the secondary source. Leave blank if unavailable.",
    "Injury confirmed for week": "For injury deltas: 'Y'/'N' that the injury/absence is re-confirmed for the affected week (week-scoped).",
    "Starts by active QB": "Integer count of starts the active QB has made under this deviation (drives the 3-start review).",
    "Three-start review due": "ISO YYYY-MM-DD the 3-start double-counting review is due, or 'N/A' if not a lasting replacement.",
    "Three-start review completed": "ISO YYYY-MM-DD the 3-start review was completed, else blank.",
    "TEAM RATINGS movement reviewed": "'Y'/'N' — whether TEAM RATINGS was checked for absorbed performance at the review.",
    "Double-counting risk": "'None'/'Low'/'Medium'/'High' — assessed risk that the deviation duplicates TEAM RATINGS movement.",
    "Review action": "One of: 'entered' | 'continued' | 'reduced' | 'reset' | 'removed'.",
    "Previous deviation": "The Active value before this review action (blank on first entry). Quarter-point value.",
    "Revised deviation": "The Active value after this review action. Quarter-point value within -4.00..+2.00.",
    "Review date": "ISO YYYY-MM-DD this row was recorded / reviewed.",
    "Reviewer": "Who performed the review (initials or name).",
    "Reason": "Explicit reason for the action (why entered/continued/reduced/reset/removed).",
    "Reset date": "ISO YYYY-MM-DD the deviation was reset to 0 (baseline QB returned healthy), else blank.",
    "Status": "One of: 'active' | 'under review' | 'reset' | 'closed'.",
}

VALIDATION_RULES = [
    "Applied deviation, Previous deviation, and Revised deviation must each be a quarter-point value (multiple of 0.25) within the inclusive range -4.00 to +2.00; blank is allowed for Previous deviation on first entry.",
    "Adjustment classification must be one of the eight rubric classifications, and Applied/Revised deviation must fall in that classification's allowed value set (future_qb_deviation_rubric.md §2).",
    "No value may be entered that requires a backdoor via ADJUSTMENTS; anything outside -4.00..+2.00 or off the quarter-point grid requires a formal methodology amendment first.",
    "All date fields use ISO YYYY-MM-DD. Source-date fields are left blank when the exact publication date is unavailable (do not invent dates).",
    "For injury-driven deviations, 'Injury confirmed for week' must be re-set each affected week; a lasting replacement gets a 'Three-start review due' date.",
    "'Review action' = 'reset' requires a non-blank 'Reset date' and Revised deviation = 0.",
    "Every row must carry a 'Review date', 'Reviewer', and 'Reason' — no silent decay (rubric §4).",
    "'Starts by active QB' >= 3 requires 'TEAM RATINGS movement reviewed' = 'Y' and a completed 3-start review before any further continuation of a nonzero deviation.",
]

def main():
    # 1) header-only CSV (no records)
    csv_path = os.path.join(OUT, "qb_deviation_review_log.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLUMNS)
        # intentionally NO data rows
    # 2) JSON: schema + docs + validation rules, empty records list
    json_path = os.path.join(OUT, "qb_deviation_review_log.json")
    payload = {
        "log": "qb_deviation_review_log",
        "purpose": "Future-use audit trail for every nonzero QB deviation: entry, weekly injury re-confirmation, 3-start double-counting review, reduction, reset, and closure. Separate from qb_exception_resolution_tracker (which has no review-log columns).",
        "generated": "2026-07-22",
        "status": "EMPTY — headers, schema, and validation rules only; no adjustment records exist (no nonzero deviation has been approved or entered).",
        "column_order": COLUMNS,
        "field_documentation": FIELD_DOC,
        "validation_rules": VALIDATION_RULES,
        "records": [],
    }
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=1, ensure_ascii=False)
    # verify emptiness
    with open(csv_path) as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]
    assert len(lines) == 1, f"CSV must be header-only, got {len(lines)} lines"
    assert payload["records"] == [], "JSON records must be empty"
    print(f"CSV : {csv_path} ({len(COLUMNS)} columns, {len(lines)-1} data rows)")
    print(f"JSON: {json_path} ({len(payload['records'])} records, {len(VALIDATION_RULES)} validation rules)")

if __name__ == "__main__":
    main()
