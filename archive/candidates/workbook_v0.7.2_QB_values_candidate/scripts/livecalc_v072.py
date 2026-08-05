#!/usr/bin/env python3
"""Live-calc QB VALUES!M (status) for all 138 rows of the v0.7.2 candidate.

The QB-status formula chain is fully self-contained — QB VALUES!M depends only
on cells this script reads directly:

  G (delta)  = IF(OR($D="",$F=""), "", $F-$D)              [same sheet]
  M (status) = IF($A="", "",
                  IF(OR($G="", $H="L", $J<>SETTINGS!$B$3), "UNCERTAIN", "OK"))

Inputs: A (team, present for all 138 rows — verified in verify_v072.py),
D/F (Baseline/Active value), H (confidence), J (reviewed year), and the single
cross-sheet reference SETTINGS!$B$3 (the season). This evaluator applies the
exact formula logic to the real cell values, so it is a faithful live
evaluation of the status — equivalent to a full-engine recalc for this chain,
which has no volatile or indirect dependencies. (A full `formulas`-engine
recalc of all 123,011 formulas was attempted but is impractical here — it
exceeded available memory; the v0.7.1 engine recalc used identical calc inputs
and returned the same 105 OK / 33 UNCERTAIN.)
"""
import os, openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.dirname(HERE)
WB   = os.path.join(OUT, "TTW_NCAAF_Power_Ratings_2026_v0.7.2_QB_VALUES_CANDIDATE.xlsx")

wb = openpyxl.load_workbook(WB)
qb = wb["QB VALUES"]
season = wb["SETTINGS"]["B3"].value  # SETTINGS!$B$3

def blank(v):
    return v is None or v == ""

ok = unc = nonzero = 0
for r in range(6, 144):                 # 138 team rows (6..143)
    D = qb.cell(row=r, column=4).value   # Baseline value
    F = qb.cell(row=r, column=6).value   # Active value
    H = qb.cell(row=r, column=8).value   # Confidence
    J = qb.cell(row=r, column=10).value  # Reviewed for season
    # G = delta
    if blank(D) or blank(F):
        G = ""
    else:
        G = F - D
        if G != 0:
            nonzero += 1
    # M = status  (A is present for all 138 rows)
    if G == "" or H == "L" or J != season:
        unc += 1
    else:
        ok += 1

print(f"season (SETTINGS!B3) = {season}")
print(f"status OK: {ok} | UNCERTAIN: {unc} | nonzero deltas: {nonzero}")
assert ok + unc == 138, f"row total != 138: {ok+unc}"
