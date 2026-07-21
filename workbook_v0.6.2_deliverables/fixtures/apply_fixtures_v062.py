"""
Phase 6.2 full-scale fixture application. Writes a representative test
fixture set into a COPY of the authoritative v0.6.2 workbook
(v0.6.2_test_applied.xlsx) so the cleanup + zero-diff proof exercises
every fixture zone: SETTINGS, MARKET LINES, ADJUSTMENTS, QB VALUES,
IMPORT STATS, synthetic schedule games, and the DATA INCOMPLETE
remove/restore demo.

FIXTURE DISCIPLINE (per Phase 6.2 instructions):
  * Synthetic games go on GENUINELY UNUSED schedule rows 894-898 (the 888
    real games occupy rows 6-893; 894+ are blank - verified before use).
  * The ONLY real (non-blank in pristine) cell altered is IMPORT
    SCHEDULE!C8 (G1 week = 0), temporarily blanked for the DATA INCOMPLETE
    demo. Its exact original value (0) is recorded in
    ORIGINAL_REAL_CELLS below and restored precisely by cleanup.
  * Every other fixture writes into a cell that is blank in the pristine
    workbook (market lines, adjustments, QB manual columns, stats,
    unused schedule rows, SETTINGS week/as-of), so cleanup simply clears
    them.
  * Every synthetic value carries the TEST_TAG marker.
"""
import datetime, json, openpyxl

TAG = "TEST ONLY — NOT REAL DATA"
SRC = "TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx"
OUT = "v0.6.2_test_applied.xlsx"

# Exact original contents of every REAL (pristine-non-blank) cell this
# script alters, for precise restoration by the cleanup script.
ORIGINAL_REAL_CELLS = {
    ("IMPORT SCHEDULE", 8, 3): 0,   # G1 week = Week 0 (real value)
}

wb = openpyxl.load_workbook(SRC, data_only=False)

# --- SETTINGS ---
st = wb["SETTINGS"]
st["B4"] = 2
st["B5"] = datetime.date(2026, 9, 4)
st["B11"] = "N"   # BET toggle stays at approved default

# --- MARKET LINES (all target rows blank in pristine) ---
ml = wb["MARKET LINES"]
def line(row, gid, fav, spread, total, ldate, note=""):
    ml.cell(row=row, column=1, value=gid)
    ml.cell(row=row, column=3, value=fav)
    ml.cell(row=row, column=4, value=spread)
    ml.cell(row=row, column=5, value=total)
    ml.cell(row=row, column=6, value=TAG)
    ml.cell(row=row, column=7, value=ldate)
    ml.cell(row=row, column=8, value=f"{TAG}{': '+note if note else ''}")
line(8,  "401858202", "UVA", 6.5, 51.5, datetime.date(2026, 9, 3))              # G1
line(10, "401864570", "FSU", 24.5, 58.5, datetime.date(2026, 9, 3))            # G4
line(11, "401864577", "NDSU", 3.0, 45.0, datetime.date(2026, 9, 3))           # G5
line(14, "401856767", "UCF", 45.0, 60.0, datetime.date(2026, 9, 3),
     "on an FCS game to prove a line cannot override FCS — NO PLAY")            # G6 (FCS)

# --- ADJUSTMENTS (rows 6,7 blank in pristine) ---
adj = wb["ADJUSTMENTS"]
def setadj(row, typ, target, value, reason):
    adj.cell(row=row, column=1, value=typ)
    adj.cell(row=row, column=2, value=target)
    adj.cell(row=row, column=3, value=value)
    adj.cell(row=row, column=4, value=reason)
    adj.cell(row=row, column=5, value=TAG)
    adj.cell(row=row, column=6, value=datetime.date(2026, 9, 1))
    adj.cell(row=row, column=8, value="Y")
    adj.cell(row=row, column=9, value=TAG)
setadj(6, "GAME", "401864570", 1.5, f"{TAG}: valid adjustment")
setadj(7, "GAME", "401856766", 999, f"{TAG}: oversized - v0.6.1 safety logic forces Effective=0")

# --- QB VALUES (manual columns blank in pristine) ---
qb = wb["QB VALUES"]
for r in (64, 70, 97, 122):   # NCST, UVA, JVST, NDSU
    qb.cell(row=r, column=3, value=f"{TAG}: base QB")
    qb.cell(row=r, column=4, value=0.0)
    qb.cell(row=r, column=5, value=f"{TAG}: active QB")
    qb.cell(row=r, column=6, value=0.0)
    qb.cell(row=r, column=8, value="M")
    qb.cell(row=r, column=9, value=TAG)
    qb.cell(row=r, column=10, value=2026)
    qb.cell(row=r, column=11, value=datetime.date(2026, 9, 1))
    qb.cell(row=r, column=12, value=TAG)

# --- IMPORT STATS (rows 6-8 blank in pristine): 2 matched + 1 unmatched ---
ist = wb["IMPORT STATS"]
for i, vals in enumerate([
        ("NC State", 1, 0.15, -0.05, 0.44, 0.38, 0.35, 0.28, 68.0),
        ("Virginia", 1, 0.08, -0.02, 0.41, 0.40, 0.30, 0.29, 70.0),
        (f"{TAG}: Nonexistent Fictional University", 1, 0.10, -0.10, 0.40, 0.40, 0.30, 0.30, 69.0)]):
    for c, v in enumerate(vals, start=1):
        ist.cell(row=6 + i, column=c, value=v)

# --- NDSU 5 synthetic completed FBS games on GENUINELY UNUSED rows 894-898 ---
sched = wb["IMPORT SCHEDULE"]
opps = [("Air Force Falcons", "American Conference"),
        ("UNLV Rebels", "Mountain West Conference"),
        ("New Mexico Lobos", "Mountain West Conference"),
        ("San José State Spartans", "Mountain West Conference"),
        ("UTEP Miners", "Conference USA")]
for i, (opp, conf) in enumerate(opps):
    r = 894 + i
    sched.cell(row=r, column=1, value=f"9900000{i}")
    sched.cell(row=r, column=2, value=2026)
    sched.cell(row=r, column=3, value=1 + i)
    sched.cell(row=r, column=4, value=datetime.date(2026, 9, 5 + i))
    sched.cell(row=r, column=5, value=False)
    sched.cell(row=r, column=6, value="North Dakota State Bison")
    sched.cell(row=r, column=7, value="Missouri Valley Football Conference")
    sched.cell(row=r, column=8, value=opp)
    sched.cell(row=r, column=9, value=conf)
    sched.cell(row=r, column=10, value=17)
    sched.cell(row=r, column=11, value=24)
    sched.cell(row=r, column=12, value=True)
    sched.cell(row=r, column=14, value=f"{TAG}: synthetic NDSU completed game (unused row)")

# --- DATA INCOMPLETE demo: temporarily blank G1 (row 8) week (real value 0) ---
assert sched.cell(row=8, column=3).value == ORIGINAL_REAL_CELLS[("IMPORT SCHEDULE", 8, 3)]
sched.cell(row=8, column=3).value = None

# --- Banner marker ---
sh = wb["START HERE"]
sh["A1"] = ("TO THE WINDOW — NCAAF POWER RATINGS 2026 "
            "(v0.6.2 — TEST FIXTURES APPLIED — DO NOT USE FOR REAL PICKS)")

wb.save(OUT)
json.dump({f"{s}!{openpyxl.utils.get_column_letter(c)}{r}": v
           for (s, r, c), v in ORIGINAL_REAL_CELLS.items()},
          open("original_real_cells_v062.json", "w"), indent=1, default=str)

tagged = sum(1 for name in wb.sheetnames for row in wb[name].iter_rows()
             for cell in row if isinstance(cell.value, str) and TAG in cell.value)
print("Saved", OUT)
print("TEST_TAG cells applied:", tagged)
print("Real cells altered (recorded for restore):", list(ORIGINAL_REAL_CELLS))
