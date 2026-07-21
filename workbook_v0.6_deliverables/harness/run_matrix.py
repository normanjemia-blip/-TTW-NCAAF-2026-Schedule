import formulas, json

def get(sol, sheet, cell):
    target = f"{sheet.upper()}'!{cell.upper()}"
    for k, v in sol.items():
        if k.upper().endswith(target):
            try:
                return v.value[0, 0]
            except Exception:
                return v.value
    return "NOT FOUND"

results = {}
for variant in ["A", "B", "C", "D", "E"]:
    xl = formulas.ExcelModel().loads(f"harness_test_{variant}.xlsx").finish()
    sol = xl.calculate()
    r = {}
    for row in [6, 8, 9, 10, 11, 14, 15]:
        r[str(row)] = {
            "STATUS": str(get(sol, "ENGINE", f"AI{row}")),
            "spread_edge": str(get(sol, "ENGINE", f"V{row}")),
            "spread_label": str(get(sol, "ENGINE", f"X{row}")),
            "total_edge": str(get(sol, "ENGINE", f"AA{row}")),
            "total_label": str(get(sol, "ENGINE", f"AB{row}")),
            "home_tt": str(get(sol, "ENGINE", f"AC{row}")),
            "away_tt": str(get(sol, "ENGINE", f"AD{row}")),
            "confidence": str(get(sol, "ENGINE", f"AJ{row}")),
            "HFA": str(get(sol, "ENGINE", f"L{row}")),
            "block_reasons": str(get(sol, "ENGINE", f"AH{row}")),
            "final_margin": str(get(sol, "ENGINE", f"R{row}")),
            "manual_adj": str(get(sol, "ENGINE", f"O{row}")),
        }
    r["DASHBOARD_priority_row8"] = str(get(sol, "DASHBOARD", "V8"))
    r["DASHBOARD_rank_row8"] = str(get(sol, "DASHBOARD", "W8"))
    for dqrow, label in [(7,"BLOCKED"),(8,"PENDING"),(9,"STALE"),(10,"QBUNC"),(11,"TRANSUNC"),(13,"READY"),(21,"FCSNOPLAY"),(15,"ADJ_FLAGS")]:
        r[f"DQ_{label}"] = str(get(sol, "DATA QUALITY", f"B{dqrow}"))
    for arow in [6,7,8]:
        r[f"ADJ_J{arow}"] = str(get(sol, "ADJUSTMENTS", f"J{arow}"))
        r[f"ADJ_K{arow}"] = str(get(sol, "ADJUSTMENTS", f"K{arow}"))
    results[variant] = r
    print(f"=== Variant {variant} ===")
    for row in [6, 8, 9, 10, 11, 14, 15]:
        print(f"  row {row}: {r[str(row)]}")
    print("  DASHBOARD:", r["DASHBOARD_priority_row8"], r["DASHBOARD_rank_row8"])
    print("  DQ:", {k:v for k,v in r.items() if k.startswith("DQ_")})
    print("  ADJ:", {k:v for k,v in r.items() if k.startswith("ADJ_")})
    print()

json.dump(results, open("harness_results_raw.json","w"), indent=1)
