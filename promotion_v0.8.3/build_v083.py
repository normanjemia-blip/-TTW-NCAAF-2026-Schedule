#!/usr/bin/env python3
"""Build v0.8.3 from the frozen v0.8.2 workbook.

Go-live guardrail patch. Three cells:

  AUDIT!A16   label  — the invariant's name
  AUDIT!B16   FORMULA — replaces "market lines must be empty" with an
                        operational validity check
  START HERE!A1        version identifier v0.8.2 -> v0.8.3

Nothing else changes: every model formula, rating, QB value, setting and
market row is preserved. The repository artifact keeps a BLANK MARKET LINES
sheet -- the eight live Circa rows are transient working-copy data and are
deliberately not committed.

Run:  python3 promotion_v0.8.3/build_v083.py
"""
import hashlib, os, sys
import openpyxl
from openpyxl.worksheet.formula import ArrayFormula

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "promotion_v0.8.2",
                   "TTW_College_Football_Power_Ratings_v0.8.2_AUTHORITATIVE.xlsx")
OUT = os.path.join(ROOT, "promotion_v0.8.3",
                   "TTW_College_Football_Power_Ratings_v0.8.3_AUTHORITATIVE.xlsx")
FROZEN_V082_SHA = "225085449b5a1db5903a3998cb909be1f7ae0037782ea65d412bcb4d9d9490d0"

A16_LABEL = ("Market lines valid (every populated row: in schedule, favorite valid, "
             "positive spread, numeric total, source, date, no duplicate, no flag)")

# Populated row = MARKET LINES!A non-blank.
# A row is VALID when:
#   P = "OK"        -> GameID resolves to a scheduled game AND the favorite
#                      resolves to one of that game's two teams
#                      (this also closes the gap where a BLANK favorite leaves
#                       P and Q empty, so Q alone would not flag it)
#   Q = ""          -> no flag: source, line date, duplicate GameID, staleness
#   D numeric and > 0
#   E numeric
# Passes when zero rows are populated: 0 = 0.
B16_FORMULA = (
    '=IF(SUMPRODUCT(--(\'MARKET LINES\'!$A$6:$A$1005<>""))'
    '=SUMPRODUCT(--(\'MARKET LINES\'!$A$6:$A$1005<>""),'
    '--(\'MARKET LINES\'!$P$6:$P$1005="OK"),'
    '--(\'MARKET LINES\'!$Q$6:$Q$1005=""),'
    '--ISNUMBER(\'MARKET LINES\'!$D$6:$D$1005),'
    '--(\'MARKET LINES\'!$D$6:$D$1005>0),'
    '--ISNUMBER(\'MARKET LINES\'!$E$6:$E$1005)),'
    '"OK — "&SUMPRODUCT(--(\'MARKET LINES\'!$A$6:$A$1005<>""))&" line(s) valid",'
    '"FAIL — "&SUMPRODUCT(--(\'MARKET LINES\'!$A$6:$A$1005<>""))'
    '-SUMPRODUCT(--(\'MARKET LINES\'!$A$6:$A$1005<>""),'
    '--(\'MARKET LINES\'!$P$6:$P$1005="OK"),'
    '--(\'MARKET LINES\'!$Q$6:$Q$1005=""),'
    '--ISNUMBER(\'MARKET LINES\'!$D$6:$D$1005),'
    '--(\'MARKET LINES\'!$D$6:$D$1005>0),'
    '--ISNUMBER(\'MARKET LINES\'!$E$6:$E$1005))'
    '&" line(s) invalid — see MARKET LINES column Q")'
)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def isf(v):
    return isinstance(v, ArrayFormula) or (isinstance(v, str) and v.startswith("="))


def ftext(v):
    return v.text if isinstance(v, ArrayFormula) else v


def main():
    got = sha256(SRC)
    assert got == FROZEN_V082_SHA, f"v0.8.2 is not the expected artifact: {got}"
    print(f"source v0.8.2 SHA-256 verified: {got}")

    wb = openpyxl.load_workbook(SRC)
    au, sh, ml = wb["AUDIT"], wb["START HERE"], wb["MARKET LINES"]

    # ---- preconditions ---------------------------------------------------
    assert au["A16"].value == "No market lines entered (Phase 2 deliverable must ship clean)", \
        f"A16 unexpected: {au['A16'].value!r}"
    old_b16 = ftext(au["B16"].value)
    assert isf(au["B16"].value) and "REMOVE TEST LINES" in old_b16, \
        f"B16 unexpected: {old_b16!r}"
    e1 = ftext(au["E1"].value)
    assert 'COUNTIF($B$6:$B$19,"FAIL*")' in e1, "E1 count formula unexpected"

    # the repository artifact must ship with a blank MARKET LINES sheet
    populated = [r for r in range(6, 1006) if ml.cell(row=r, column=1).value not in (None, "")]
    assert not populated, f"MARKET LINES must be blank in the repo artifact, found {populated[:5]}"
    print("preconditions verified; MARKET LINES is blank")

    banner = sh["A1"].value
    assert "v0.8.2 AUTHORITATIVE" in banner, "banner version marker missing"

    # ---- the three writes -------------------------------------------------
    au["A16"].value = A16_LABEL
    au["B16"].value = B16_FORMULA
    sh["A1"].value = banner.replace("v0.8.2 AUTHORITATIVE", "v0.8.3 AUTHORITATIVE")

    assert "v0.8.2" not in sh["A1"].value
    assert ftext(au["E1"].value) == e1, "E1 must not change"
    print("A16 label, B16 formula and banner version written; E1 unchanged")

    tmp = OUT + ".building.xlsx"
    wb.save(tmp)
    os.replace(tmp, OUT)
    print(f"written: {OUT}")
    print(f"v0.8.3 SHA-256: {sha256(OUT)}")
    assert sha256(SRC) == FROZEN_V082_SHA, "v0.8.2 was modified by the build"
    print("v0.8.2 confirmed still frozen")


if __name__ == "__main__":
    sys.exit(main())
