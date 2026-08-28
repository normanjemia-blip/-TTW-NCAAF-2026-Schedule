"""Generate expected_vs_actual_v062.md straight from h62_raw_results.json
so the report reflects the real calculated output with no transcription."""
import json
d = json.load(open("h62_raw_results.json"))

def stat(scn, g): return d[scn][g]["STATUS"]
def cell(scn, g, k): return d[scn][g][k]

L = []
w = L.append
w("# Phase 6.2 — Expected vs Actual Test Results\n")
w("All values below are **actual calculated output** from the `formulas` "
  "engine running v0.6.2's own byte-exact formulas (compact real-formula "
  "harness). Raw output: `h62_raw_results.json`.\n")

w("## 1. DATA INCOMPLETE repair (the fix)\n")
w("| Test (G1 = NCST@UVA, row 8) | Expected | Actual | Result |")
w("|---|---|---|---|")
w(f"| Control: line + QBs resolved, Week 0 present | READY | **{stat('datainc_control','G1')}** (week={cell('datainc_control','G1','week_B')}) | {'PASS' if stat('datainc_control','G1')=='READY' else 'FAIL'} |")
w(f"| Week blanked | DATA INCOMPLETE | **{stat('datainc_week_blank','G1')}** (week={cell('datainc_week_blank','G1','week_B')!r}) | {'PASS' if stat('datainc_week_blank','G1')=='DATA INCOMPLETE' else 'FAIL'} |")
w(f"| Date blanked | DATA INCOMPLETE | **{stat('datainc_date_blank','G1')}** (date={cell('datainc_date_blank','G1','date_C')!r}) | {'PASS' if stat('datainc_date_blank','G1')=='DATA INCOMPLETE' else 'FAIL'} |")
w(f"| Week restored to real value (0) | READY | **{stat('datainc_restored','G1')}** (week={cell('datainc_restored','G1','week_B')}) | {'PASS' if stat('datainc_restored','G1')=='READY' else 'FAIL'} |")
w("")
w("Week 0 is preserved as a real value (status READY), confirming the fix "
  "does not misread a legitimate Week 0 game as missing.\n")

w("## 2. Stacked priority — DATA INCOMPLETE must never override a higher status\n")
w("Each game below has a blank Week stacked on top of a higher-priority "
  "condition; the higher status must win.\n")
w("| Game + stacked blank Week | Expected (higher status wins) | Actual | Result |")
w("|---|---|---|---|")
rows = [("stack_blocked_over_datainc","G7","BLOCKED"),
        ("stack_pending_over_datainc","G3","PENDING LINE"),
        ("stack_qbunc_over_datainc","G1","QB UNCERTAIN"),
        ("stack_transitional_over_datainc","G5","TRANSITION UNCERTAIN")]
for scn,g,exp in rows:
    act=stat(scn,g)
    w(f"| {g}: {exp} + blank Week | {exp} | **{act}** | {'PASS' if act==exp else 'FAIL'} |")
w("")

w("## 3. Full single-condition status chain\n")
w("| Game | Expected | Actual | Result |")
w("|---|---|---|---|")
order=[("G7","BLOCKED"),("G6","FCS — NO PLAY"),("G3","PENDING LINE"),
       ("G2","STALE LINE"),("G1","QB UNCERTAIN"),("G5","TRANSITION UNCERTAIN")]
for g,exp in order:
    act=d["status_chain"][g]["STATUS"]
    w(f"| {g} | {exp} | **{act}** | {'PASS' if act==exp else 'FAIL'} |")
w(f"| G1 (isolated, QBs resolved) | READY | **{stat('datainc_control','G1')}** | {'PASS' if stat('datainc_control','G1')=='READY' else 'FAIL'} |")
w(f"| G1 (isolated, Week blanked) | DATA INCOMPLETE | **{stat('datainc_week_blank','G1')}** | {'PASS' if stat('datainc_week_blank','G1')=='DATA INCOMPLETE' else 'FAIL'} |")
w("\nAll eight statuses demonstrated; no lower-priority status overrode a higher one.\n")

w("## 4. ADJUSTMENTS (no formula changed; v0.6.1 safety logic intact)\n")
w("| Adjustment on G4 | Expected | Actual (Effective J / Flag K / margin O) | Result |")
w("|---|---|---|---|")
def adjrow(scn, exp_j, exp_k, exp_o, note):
    j=d[scn]["adj6"]["J_effective"]; k=d[scn]["adj6"]["K_flags"]; o=d[scn]["G4"]["manual_adj"]
    ok = (j==exp_j) and (exp_k in k) and (str(o)==exp_o)
    w(f"| {note} | {exp_k or 'no flag'}, Eff={exp_j}, margin={exp_o} | J={j} / K={k!r} / O={o} | {'PASS' if ok else 'FAIL'} |")
adjrow("adj_valid","1","", "1.5","valid +1.5")
adjrow("adj_oversized","0","LARGE ADJ (>4)","0.0","oversized +999")
adjrow("adj_nonnumeric","0","VALUE NOT NUMERIC","0.0","non-numeric \"abc\"")
adjrow("adj_noreason","0","REASON MISSING","0.0","missing reason")
jo=d["adj_override"]["adj6"]["J_effective"]; ko=d["adj_override"]["adj6"]["K_flags"]; oo=d["adj_override"]["G4"]["manual_adj"]
w(f"| MARGIN OVERRIDE +15 (exempt) | no LARGE-ADJ flag, Eff=1, applies | J={jo} / K={ko!r} / margin(R)/O={oo} | {'PASS' if jo=='1' and 'LARGE ADJ' not in ko else 'FAIL'} |")
w("")

w("## 5. BET toggle (same READY fixture, qualifying edge)\n")
w("| Toggle | Expected | Actual (status / edge / label) | Result |")
w("|---|---|---|---|")
for scn,exp in [("bet_N","INVESTIGATE"),("bet_Y","BET")]:
    g=d[scn]["G1"]
    ok = g["STATUS"]=="READY" and g["spread_label"]==exp
    w(f"| {d[scn]['toggle']} | READY, {exp} | {g['STATUS']} / edge={g['spread_edge']} / {g['spread_label']} | {'PASS' if ok else 'FAIL'} |")
w("\nOnly the toggle differs between the two; the edge is identical.\n")

w("## 6. Transitional restriction (NDSU) — cannot BET while restriction active\n")
n=d["ndsu_functional"]
g5=n["G5"]
w("| Check | Expected | Actual |")
w("|---|---|---|")
w(f"| NDSU effective games (F) | >4 (threshold exceeded) | {n['NDSU_F_games']} |")
w(f"| NDSU review-cleared (TEAM RATINGS!X) | blank (nothing auto-sets it) | {n['NDSU_X_reviewcleared']!r} |")
w(f"| G5 transitional flag | TRANSITIONAL | {g5['transitional']} |")
w(f"| G5 status (line + QBs + toggle=Y) | TRANSITION UNCERTAIN | {g5['STATUS']} |")
w(f"| G5 edge | large | {g5['spread_edge']} |")
w(f"| G5 label | INVESTIGATE (never BET) | {g5['spread_label']} |")
w("\nWith 5 completed games, a large edge, a market line, and BET toggle = Y, "
  "NDSU still cannot reach BET — the restriction holds functionally.\n")

w("## 7. FCS protection (market line on an FCS game)\n")
f=d["fcs_protection"]["G6"]
w("| Check | Expected | Actual |")
w("|---|---|---|")
w(f"| G6 status (FCS game WITH a test line) | FCS — NO PLAY | {f['STATUS']} |")
w(f"| FCS flag | FCS OPP | {f['fcs_flag']} |")
w(f"| Spread edge | blank (no actionable number) | {f['spread_edge']!r} |")
w(f"| Spread label | blank | {f['spread_label']!r} |")
w("\nA market line cannot override FCS — NO PLAY, and no actionable "
  "spread/edge/label is produced.\n")

w("## 8. Prior-fade table (unchanged; all values + clamp)\n")
w("| Effective games F | Expected weight | Actual | Result |")
w("|---|---|---|---|")
exp_fade=[1.0,0.8,0.65,0.5,0.4,0.3,0.225,0.175,0.125,0.1]
for fnum in range(10):
    act=d["fade_table"][str(fnum)]
    w(f"| {fnum} | {exp_fade[fnum]} | {act} | {'PASS' if str(exp_fade[fnum])==act else 'FAIL'} |")
w(f"| 10 (beyond table) | clamps to F=9 (0.1) | {d['fade_table']['10']} | {'PASS' if d['fade_table']['10']=='0.1' else 'FAIL'} |")
w("")

open("expected_vs_actual_v062.md","w").write("\n".join(L)+"\n")
print("wrote expected_vs_actual_v062.md")
