"""Phase 7E.1 — documentation maintenance patch v0.8.0 -> v0.8.1.

Scope: ONE CELL. START HERE!A1 only. No formula, structure, QB data, rating,
engine, HFA, worksheet-order or formatting change.
"""
import shutil, os, openpyxl, hashlib
from openpyxl.worksheet.formula import ArrayFormula

ROOT="/home/user/-TTW-NCAAF-2026-Schedule"
SRC=f"{ROOT}/promotion_v0.8.0/TTW_College_Football_Power_Ratings_v0.8.0_AUTHORITATIVE.xlsx"
OUT=f"{ROOT}/promotion_v0.8.1"
DST=f"{OUT}/TTW_College_Football_Power_Ratings_v0.8.1_AUTHORITATIVE.xlsx"
os.makedirs(OUT, exist_ok=True)

def isf(v): return isinstance(v,ArrayFormula) or (isinstance(v,str) and v.startswith("="))

OLD_BANNER=("TO THE WINDOW — NCAAF POWER RATINGS 2026 (v0.7.9 FINAL QB-VERIFICATION CANDIDATE — backlog 0, "
 "audit-trail gap 0; all 74 Tier-1 records verified and stamped; Missouri M->H, North Carolina and UNLV M->L; "
 "NOT AUTHORITATIVE, NOT PROMOTED — awaiting owner approval)")

NEW_BANNER=("TO THE WINDOW — TTW COLLEGE FOOTBALL POWER RATINGS (v0.8.1 AUTHORITATIVE — promotion complete "
 "2026-08-04. QB verification complete: backlog 0, audit-trail gap 0, all 73 Tier-1 records verified and "
 "stamped against team-specific primary sources; 65 H / 40 M / 33 L; 0 nonzero QB values. Preseason state: "
 "0 market lines loaded, BET toggle = N.)")

shutil.copyfile(SRC, DST)
wb=openpyxl.load_workbook(DST)
sh=wb["START HERE"]
cell=sh["A1"]

# --- guards: assert exactly what we expect before touching anything ---
assert not isf(cell.value), "A1 must not be a formula"
assert cell.value==OLD_BANNER, f"A1 does not match the expected v0.8.0 banner:\n{cell.value!r}"
for bad in ("NOT PROMOTED","NOT AUTHORITATIVE","awaiting owner approval","74 Tier-1","v0.7.9"):
    assert bad in OLD_BANNER, f"guard string missing from old banner: {bad}"
    assert bad not in NEW_BANNER, f"forbidden string still present in new banner: {bad}"
for need in ("v0.8.1 AUTHORITATIVE","promotion complete","73 Tier-1"):
    assert need in NEW_BANNER, f"required string missing from new banner: {need}"

# capture the style so we can prove formatting is untouched
before_style=(cell.font.b, cell.font.sz, cell.font.color.rgb if cell.font.color else None,
              cell.fill.fgColor.rgb if cell.fill and cell.fill.fgColor else None,
              cell.alignment.horizontal, cell.alignment.wrap_text, cell.number_format)

cell.value=NEW_BANNER

after_style=(cell.font.b, cell.font.sz, cell.font.color.rgb if cell.font.color else None,
             cell.fill.fgColor.rgb if cell.fill and cell.fill.fgColor else None,
             cell.alignment.horizontal, cell.alignment.wrap_text, cell.number_format)
assert before_style==after_style, f"formatting drifted: {before_style} -> {after_style}"

wb.save(DST)

h=hashlib.sha256(open(DST,"rb").read()).hexdigest()
print("v0.8.1 built")
print(f"  OLD: {OLD_BANNER}")
print(f"  NEW: {NEW_BANNER}")
print(f"  style preserved: {before_style==after_style}  {before_style}")
print(f"  SHA-256: {h}")
