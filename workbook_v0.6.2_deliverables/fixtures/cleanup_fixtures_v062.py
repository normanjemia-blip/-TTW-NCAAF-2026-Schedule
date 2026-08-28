"""
Phase 6.2 cleanup: reverse every fixture written by
apply_fixtures_v062.py, producing v0.6.2_test_cleaned.xlsx. Only
manual-input cells are cleared (never a formula column); the single real
cell that was altered (IMPORT SCHEDULE!C8 = Week 0) is restored to its
exact recorded original. Proven zero-diff vs the pristine authoritative
v0.6.2 by prove_zero_diff_v062.py.
"""
import json, openpyxl

SRC = "v0.6.2_test_applied.xlsx"
OUT = "v0.6.2_test_cleaned.xlsx"
ORIG = json.load(open("original_real_cells_v062.json"))  # {"IMPORT SCHEDULE!C8": "0"}

wb = openpyxl.load_workbook(SRC, data_only=False)

# --- SETTINGS -> pristine (B4/B5 blank, B11 default N) ---
st = wb["SETTINGS"]
st["B4"] = None
st["B5"] = None
st["B11"] = "N"

# --- MARKET LINES: clear manual cols A,C,D,E,F,G,H on the 4 test rows ---
ml = wb["MARKET LINES"]
for row in (8, 10, 11, 14):
    for c in (1, 3, 4, 5, 6, 7, 8):
        ml.cell(row=row, column=c).value = None

# --- ADJUSTMENTS: clear A:I on rows 6,7 (J,K are formulas, untouched) ---
adj = wb["ADJUSTMENTS"]
for row in (6, 7):
    for c in range(1, 10):
        adj.cell(row=row, column=c).value = None

# --- QB VALUES: clear manual cols on the 4 test rows ---
qb = wb["QB VALUES"]
for row in (64, 70, 97, 122):
    for c in (3, 4, 5, 6, 8, 9, 10, 11, 12):
        qb.cell(row=row, column=c).value = None

# --- IMPORT STATS: clear the 3 test rows (all blank in pristine) ---
ist = wb["IMPORT STATS"]
for row in (6, 7, 8):
    for c in range(1, 10):
        ist.cell(row=row, column=c).value = None

# --- IMPORT SCHEDULE: clear synthetic rows 894-898 (genuinely unused),
#     then restore the one real altered cell (G1 week) precisely ---
sched = wb["IMPORT SCHEDULE"]
for row in range(894, 899):
    for c in range(1, 15):
        sched.cell(row=row, column=c).value = None
for key, val in ORIG.items():
    sheet, coord = key.split("!")
    cell = wb[sheet][coord]
    # original value recorded as JSON (Week 0 -> int 0)
    cell.value = int(val) if str(val).lstrip("-").isdigit() else val

# --- Reset number_format to pristine 'General' on the date-input cells
#     that openpyxl auto-formatted when a datetime value was written
#     (writing a date into a blank 'General' cell stamps 'yyyy-mm-dd';
#     clearing the value leaves that format behind). Every one of these is
#     'General' in the pristine authoritative v0.6.2. ---
for coord in ("G8", "G10", "G11", "G14"):
    ml[coord].number_format = "General"
for coord in ("F6", "F7"):
    adj[coord].number_format = "General"
for coord in ("K64", "K70", "K97", "K122"):
    qb[coord].number_format = "General"
st["B5"].number_format = "General"

# --- START HERE: restore the pristine v0.6.2 banner ---
sh = wb["START HERE"]
sh["A1"] = ("TO THE WINDOW — NCAAF POWER RATINGS 2026 "
            "(v0.6.2 PHASE 6.2 DATA-INCOMPLETE PATHWAY REPAIR — PENDING APPROVAL)")

wb.save(OUT)

TAG = "TEST ONLY — NOT REAL DATA"
remaining = [(name, cell.coordinate) for name in wb.sheetnames
             for row in wb[name].iter_rows() for cell in row
             if isinstance(cell.value, str) and TAG in cell.value]
print("Saved", OUT)
print("Remaining TEST_TAG cells:", len(remaining), remaining[:5])
