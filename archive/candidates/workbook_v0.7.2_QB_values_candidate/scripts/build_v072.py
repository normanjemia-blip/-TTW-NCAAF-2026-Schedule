#!/usr/bin/env python3
"""Phase 8.3: build the v0.7.2 CANDIDATE workbook from v0.7.1.

Vanderbilt re-verification FAILED (genuine Curtis/Berlowitz competition per
Clark Lea at SEC Media Days 2026-07-21), so NO QB VALUES data changes. The
ONLY differences vs v0.7.1 are:
  1) START HERE!A1 version banner  -> v0.7.2 CANDIDATE
  2) three appended CHANGELOG rows documenting the null result + doc cleanup

Everything else (formulas, formatting, sheet order/visibility, ratings, HFA,
settings, thresholds, imports, schedule, and all 138 QB rows) is byte-carried
from v0.7.1.
"""
import shutil, os, openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.dirname(HERE)
SRC  = os.path.join(OUT, "..", "workbook_v0.7.1_QB_values_working",
                    "TTW_NCAAF_Power_Ratings_2026_v0.7.1_QB_VALUES_WORKING.xlsx")
DST  = os.path.join(OUT, "TTW_NCAAF_Power_Ratings_2026_v0.7.2_QB_VALUES_CANDIDATE.xlsx")

NEW_BANNER = ("TO THE WINDOW — NCAAF POWER RATINGS 2026 "
              "(v0.7.2 QB VALUES CANDIDATE — DEVIATION-ONLY ZERO-INIT of 105 settled QBs; "
              "33 UNCERTAIN exceptions incl. Vanderbilt (re-verified 2026-07-22: genuine "
              "Curtis/Berlowitz competition — stays UNCERTAIN); NONZERO ADJUSTMENTS PENDING "
              "— NOT AUTHORITATIVE)")

CHANGELOG_ROWS = [
    ("v0.7.2", "2026-07-22",
     "Phase 8.3 (CANDIDATE — not authoritative): re-verified Vanderbilt's 2026 QB situation. "
     "Clark Lea at SEC Media Days (2026-07-21) confirmed a genuine, undecided Jared Curtis vs "
     "Blaze Berlowitz competition (Berlowitz a credible veteran with two years in OC Tim Beck's "
     "system, Pavia's backup — not a mere backup); Lea declined to name a starter and the battle "
     "may run to the opener. Re-verification FAILED: Vanderbilt NOT reclassified L->M and NOT "
     "initialized. QB status counts remain 105 OK / 33 UNCERTAIN (not 106/32).",
     "Phase 8.3 re-verification gate"),
    ("v0.7.2", "2026-07-22",
     "No QB VALUES data changed vs v0.7.1: Baseline value (D) and Active value (F) still contain "
     "only 0 or blank; no nonzero QB deviation exists; formula count unchanged (123,011). The only "
     "cells that differ from v0.7.1 are this version banner (START HERE!A1) and these CHANGELOG rows.",
     "Phase 8.3 (null result — no data change)"),
    ("v0.7.2", "2026-07-22",
     "Methodology cleanup (documentation only): future deviation bands replaced with discrete, "
     "non-overlapping quarter-point values (-4.00..+2.00; no backdoor QB value via ADJUSTMENTS); "
     "the review trail was moved to a SEPARATE qb_deviation_review_log (CSV/JSON) since the "
     "exception tracker has no review-log columns; the exception tracker gained ISO date fields "
     "(last_checked/most_recent_source/next_research/resolution).",
     "Phase 8.3 methodology correction"),
]

def main():
    shutil.copyfile(SRC, DST)
    wb = openpyxl.load_workbook(DST)

    # 1) banner
    sh = wb["START HERE"]
    old_banner = sh["A1"].value
    sh["A1"].value = NEW_BANNER

    # 2) CHANGELOG rows appended after the last populated row (63)
    cl = wb["CHANGELOG"]
    last = 0
    for r in range(1, cl.max_row + 1):
        if any(cl.cell(row=r, column=c).value not in (None, "") for c in range(1, 7)):
            last = r
    assert last == 63, f"expected last CHANGELOG row 63, got {last}"
    for i, (ver, date, change, reason) in enumerate(CHANGELOG_ROWS):
        rr = last + 1 + i
        cl.cell(row=rr, column=1).value = ver
        cl.cell(row=rr, column=2).value = date
        cl.cell(row=rr, column=3).value = change
        cl.cell(row=rr, column=4).value = reason

    # 3) SAFETY: assert no Vanderbilt QB data change (D/F must stay blank).
    # QB VALUES!A/B are formulas fed from TEAM RATINGS <- TEAM MAP, so the
    # constant abbrev lives in TEAM MAP!A. Locate VAN there.
    tm = wb["TEAM MAP"]
    van_row = None
    for r in range(1, tm.max_row + 1):
        if tm.cell(row=r, column=1).value == "VAN":
            van_row = r
            break
    assert van_row is not None, "VAN not found in TEAM MAP!A"
    qb = wb["QB VALUES"]
    C = qb.cell(row=van_row, column=3).value  # Baseline QB
    D = qb.cell(row=van_row, column=4).value  # Baseline value
    E = qb.cell(row=van_row, column=5).value  # Active QB
    F = qb.cell(row=van_row, column=6).value  # Active value
    H = qb.cell(row=van_row, column=8).value  # Confidence
    assert D in (None, ""), f"VAN Baseline value must stay blank, got {D!r}"
    assert F in (None, ""), f"VAN Active value must stay blank, got {F!r}"
    assert H == "L", f"VAN Confidence must stay L, got {H!r}"
    print(f"VAN at QB VALUES row {van_row}: C={C!r} D={D!r} E={E!r} F={F!r} H={H!r}  (unchanged)")

    wb.save(DST)
    print("OLD banner:", old_banner)
    print("NEW banner:", NEW_BANNER)
    print(f"Appended CHANGELOG rows {last+1}..{last+len(CHANGELOG_ROWS)}")
    print("Saved:", DST)

if __name__ == "__main__":
    main()
