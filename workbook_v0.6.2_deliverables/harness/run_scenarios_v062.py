"""
Live-calculate every Phase 6.2 scenario variant with the `formulas` engine
and dump raw results to h62_raw_results.json (incremental checkpoint, so a
timeout resumes where it left off). Extracts real ENGINE/ADJUSTMENTS/
TEAM RATINGS outputs - no manual traces.
"""
import formulas, json, os

OUT = "h62_raw_results.json"
results = json.load(open(OUT)) if os.path.exists(OUT) else {}
def save(): json.dump(results, open(OUT, "w"), indent=1)

def g(sol, sheet, cell):
    tgt = f"{sheet.upper()}'!{cell.upper()}"
    for k, v in sol.items():
        if k.upper().endswith(tgt):
            try: return v.value[0, 0]
            except Exception: return v.value
    return "NOTFOUND"

def eng(sol, row):
    return {
        "STATUS": str(g(sol, "ENGINE", f"AI{row}")),
        "spread_edge": str(g(sol, "ENGINE", f"V{row}")),
        "spread_label": str(g(sol, "ENGINE", f"X{row}")),
        "final_margin": str(g(sol, "ENGINE", f"R{row}")),
        "manual_adj": str(g(sol, "ENGINE", f"O{row}")),
        "block_reasons": str(g(sol, "ENGINE", f"AH{row}")),
        "transitional": str(g(sol, "ENGINE", f"AF{row}")),
        "fcs_flag": str(g(sol, "ENGINE", f"AG{row}")),
        "qb_status": str(g(sol, "ENGINE", f"AE{row}")),
        "week_B": str(g(sol, "ENGINE", f"B{row}")),
        "date_C": str(g(sol, "ENGINE", f"C{row}")),
    }

def adjJK(sol, row):
    return {"J_effective": str(g(sol, "ADJUSTMENTS", f"J{row}")),
            "K_flags": str(g(sol, "ADJUSTMENTS", f"K{row}"))}

# scenario -> (file, extractor)
def run(name, fn):
    if name in results:
        print("skip", name); return
    print("running", name, flush=True)
    results[name] = fn()
    save()

GROW = {"G1": 8, "G2": 6, "G3": 9, "G4": 10, "G5": 11, "G6": 14, "G7": 15}

def calc(f):
    return formulas.ExcelModel().loads(f).finish().calculate()

# 1. DATA INCOMPLETE sequence (G1 = row 8)
run("datainc_control",     lambda: {"G1": eng(calc("h62_datainc_control.xlsx"), 8)})
run("datainc_week_blank",  lambda: {"G1": eng(calc("h62_datainc_week_blank.xlsx"), 8)})
run("datainc_date_blank",  lambda: {"G1": eng(calc("h62_datainc_date_blank.xlsx"), 8)})
run("datainc_restored",    lambda: {"G1": eng(calc("h62_datainc_restored.xlsx"), 8)})

# 2. Stacked priority
run("stack_transitional_over_datainc", lambda: {"G5": eng(calc("h62_stack_transitional_over_datainc.xlsx"), 11)})
run("stack_qbunc_over_datainc",        lambda: {"G1": eng(calc("h62_stack_qbunc_over_datainc.xlsx"), 8)})
run("stack_pending_over_datainc",      lambda: {"G3": eng(calc("h62_stack_pending_over_datainc.xlsx"), 9)})
run("stack_blocked_over_datainc",      lambda: {"G7": eng(calc("h62_stack_blocked_over_datainc.xlsx"), 15)})

# 3. Full status chain
def _chain():
    sol = calc("h62_status_chain.xlsx")
    return {k: eng(sol, GROW[k]) for k in ("G1","G2","G3","G5","G6","G7")}
run("status_chain", _chain)

# 4. ADJUSTMENTS (G4 = row 10, adj row 6)
def _adj(f):
    sol = calc(f)
    return {"G4": eng(sol, 10), "adj6": adjJK(sol, 6)}
run("adj_valid",      lambda: _adj("h62_adj_valid.xlsx"))
run("adj_oversized",  lambda: _adj("h62_adj_oversized.xlsx"))
run("adj_nonnumeric", lambda: _adj("h62_adj_nonnumeric.xlsx"))
run("adj_override",   lambda: _adj("h62_adj_override.xlsx"))
run("adj_noreason",   lambda: _adj("h62_adj_noreason.xlsx"))

# 5. BET toggle (G1 = row 8)
run("bet_N", lambda: {"G1": eng(calc("h62_bet_N.xlsx"), 8), "toggle": str(g(calc("h62_bet_N.xlsx"), "SETTINGS", "B11"))})
run("bet_Y", lambda: {"G1": eng(calc("h62_bet_Y.xlsx"), 8), "toggle": str(g(calc("h62_bet_Y.xlsx"), "SETTINGS", "B11"))})

# 6. NDSU functional (G5 = row 11, NDSU = TEAM RATINGS row 122)
def _ndsu():
    sol = calc("h62_ndsu_functional.xlsx")
    return {"G5": eng(sol, 11),
            "NDSU_F_games": str(g(sol, "TEAM RATINGS", "F122")),
            "NDSU_X_reviewcleared": str(g(sol, "TEAM RATINGS", "X122"))}
run("ndsu_functional", _ndsu)

# 7. FCS protection (G6 = row 14)
run("fcs_protection", lambda: {"G6": eng(calc("h62_fcs_protection.xlsx"), 14)})

# 8. Prior-fade table
def _fade():
    sol = calc("h62_fade_table.xlsx")
    return {str(f): str(g(sol, "TEST", f"G{6+f}")) for f in range(11)}
run("fade_table", _fade)

print("\nAll scenarios complete.")
save()
