"""
v0.5.2 correction build from v0.5.1 (v0.4.2 and v0.5.1 untouched).

Fixes a documentation/implementation mismatch introduced in v0.5.1: the
v0.5.1 documentation (DICTIONARY, DATA QUALITY!A2/A11) was already
written to describe the transitional-reclassifier status as
"TRANSITION UNCERTAIN", but the actual formula text (ENGINE!AI) and the
DATA QUALITY!B11 counter were never updated to match - they still
returned/counted the old "FCS/TRANSITION UNCERTAIN" string. This build
makes the formulas match the docs. STATUS PRIORITY AND ALL OTHER LOGIC
ARE UNCHANGED - this is a string-literal-only correction.
"""
import openpyxl

FILE = "v0.5.2_working.xlsx"
wb = openpyxl.load_workbook(FILE, data_only=False)
engine = wb["ENGINE"]
dq = wb["DATA QUALITY"]

AI_OLD = ('=IF($A{r}="","",IF($AH{r}<>"","BLOCKED",IF($AG{r}<>"","FCS — NO PLAY",'
          'IF(CALC!$S{r}=1,"PENDING LINE",IF(CALC!$Q{r}=1,"STALE LINE",'
          'IF($AE{r}="QB UNCERTAIN","QB UNCERTAIN",IF($AF{r}<>"","FCS/TRANSITION UNCERTAIN",'
          'IF(OR($B{r}="",$C{r}=""),"DATA INCOMPLETE","READY"))))))))')
AI_NEW = ('=IF($A{r}="","",IF($AH{r}<>"","BLOCKED",IF($AG{r}<>"","FCS — NO PLAY",'
          'IF(CALC!$S{r}=1,"PENDING LINE",IF(CALC!$Q{r}=1,"STALE LINE",'
          'IF($AE{r}="QB UNCERTAIN","QB UNCERTAIN",IF($AF{r}<>"","TRANSITION UNCERTAIN",'
          'IF(OR($B{r}="",$C{r}=""),"DATA INCOMPLETE","READY"))))))))')

count = 0
mismatches = []
for r in range(6, 1006):
    c = engine.cell(row=r, column=35)
    expected = AI_OLD.format(r=r)
    if c.value != expected:
        mismatches.append((r, c.value)); continue
    c.value = AI_NEW.format(r=r)
    count += 1

print("ENGINE!AI rows corrected:", count)
if mismatches:
    print(f"*** {len(mismatches)} MISMATCHES (aborting) ***")
    for m in mismatches[:5]: print("  ", m)
    raise SystemExit(1)
assert count == 1000

DQ_B11_OLD = '=COUNTIF(ENGINE!$AI$6:$AI$1005,"FCS/TRANSITION UNCERTAIN")'
DQ_B11_NEW = '=COUNTIF(ENGINE!$AI$6:$AI$1005,"TRANSITION UNCERTAIN")'
assert dq["B11"].value == DQ_B11_OLD, dq["B11"].value
dq["B11"] = DQ_B11_NEW
print("DATA QUALITY!B11 corrected")

wb.save(FILE)
print("Saved", FILE)
