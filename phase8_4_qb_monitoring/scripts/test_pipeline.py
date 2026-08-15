#!/usr/bin/env python3
"""Phase 8.4A pipeline test harness — 12 scenarios.

Uses TEMPORARY workbook copies only (a temp dir under the system temp or
--tmp); never writes into the repo and never commits generated workbooks.
Confirms invalid scenarios fail safely and leave the source workbook unchanged
(SHA compared before/after each scenario).

Run:  python3 test_pipeline.py [--source SRC.xlsx] [--tmp DIR] [--keep]
Exit code 0 iff every scenario matched its expected outcome.
"""
import argparse, os, sys, csv, shutil, tempfile
import openpyxl
import pipeline_lib as L
import apply_pending_qb_resolutions as APP
import verify_qb_candidate as VER

_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
# Default to the current authoritative master; fall back to the v0.7.2 candidate
# the harness was originally written against (now under archive/candidates/).
# The harness copies the source into a temp dir and asserts it is unchanged, so
# pointing at the authoritative workbook is read-only and safe.
_SRC_CANDIDATES = [
    os.path.join(_ROOT, "promotion_v0.8.1",
                 "TTW_College_Football_Power_Ratings_v0.8.1_AUTHORITATIVE.xlsx"),
    os.path.join(_ROOT, "archive", "candidates", "workbook_v0.7.2_QB_values_candidate",
                 "TTW_NCAAF_Power_Ratings_2026_v0.7.2_QB_VALUES_CANDIDATE.xlsx"),
    os.path.join(_ROOT, "workbook_v0.7.2_QB_values_candidate",
                 "TTW_NCAAF_Power_Ratings_2026_v0.7.2_QB_VALUES_CANDIDATE.xlsx"),
]
DEFAULT_SRC = next((p for p in _SRC_CANDIDATES if os.path.exists(p)),
                   _SRC_CANDIDATES[0])

PEND_COLS = ["abbrev", "team", "resolution_status", "confidence", "baseline_qb",
             "baseline_value", "active_qb", "active_value", "source",
             "source_date", "last_update", "notes", "reviewed_season"]
RLOG_COLS = ["Abbrev", "Active QB", "Applied deviation", "Revised deviation",
             "Review action", "Reviewer", "Review date", "Status"]


def write_pending(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PEND_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in PEND_COLS})

def write_rlog(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=RLOG_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in RLOG_COLS})

def base_row(**kw):
    r = {"abbrev": "IOWA", "team": "Iowa", "resolution_status": "APPROVED",
         "confidence": "M", "baseline_qb": "Test Starter", "baseline_value": 0,
         "active_qb": "Test Starter", "active_value": 0, "source": "Official depth chart",
         "source_date": "2026-08-04", "last_update": "2026-08-04",
         "notes": "camp resolved (fixture)", "reviewed_season": 2026}
    r.update(kw); return r


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULT_SRC)
    ap.add_argument("--tmp", default="")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args(argv)
    SRC = os.path.abspath(a.source)
    src_sha0 = L.sha256(SRC)
    tmp = a.tmp or tempfile.mkdtemp(prefix="qbpipe_test_")
    os.makedirs(tmp, exist_ok=True)
    results = []

    def record(name, expected, actual, ok, note=""):
        results.append((name, expected, actual, ok, note))

    def out(n): return os.path.join(tmp, f"cand_{n}.xlsx")

    def apply_expect(name, pending_rows, rlog_rows=None, source=SRC,
                     expect_written=False):
        """Run apply in APPLY mode; assert written/not and source unchanged."""
        pf = os.path.join(tmp, f"pend_{name}.csv"); write_pending(pf, pending_rows)
        rf = ""
        if rlog_rows is not None:
            rf = os.path.join(tmp, f"rlog_{name}.csv"); write_rlog(rf, rlog_rows)
        sha_before = L.sha256(source)
        res = APP.run(source, pf, rf, out(name), "v0.7.3-TEST",
                      apply_mode=True, build_date="2026-08-11")
        sha_after = L.sha256(source)
        src_ok = (sha_before == sha_after)
        written = res["written"] and os.path.exists(out(name))
        ok = (written == expect_written) and src_ok
        note = "" if src_ok else "SOURCE CHANGED!"
        if not expect_written and res["errors"]:
            note = (note + " | " if note else "") + f"{len(res['errors'])} err: {res['errors'][0][:60]}"
        record(name, f"written={expect_written}", f"written={written}", ok, note)
        return res

    # ---- 1. valid zero initialization -> candidate + verify passes ---------
    r1 = apply_expect("01_zero_init", [base_row()], expect_written=True)
    if r1["written"]:
        rep = VER.verify(SRC, out("01_zero_init"),
                         os.path.join(tmp, "pend_01_zero_init.csv"), "")
        record("01_zero_init_verify", "verify=PASS", f"verify={'PASS' if rep['pass'] else 'FAIL'}",
               rep["pass"], f"{rep['counts']['candidate_ok']}/{rep['counts']['candidate_uncertain']}")

    # ---- 2. valid approved nonzero deviation -------------------------------
    dev_pend = [base_row(abbrev="STAN", team="Stanford", confidence="M",
                         baseline_qb="Baseline Starter", active_qb="Replacement QB",
                         active_value=-1.50, source_date="2026-08-11",
                         last_update="2026-08-11", notes="starter out; replacement named")]
    dev_rlog = [{"Abbrev": "STAN", "Active QB": "Replacement QB",
                 "Applied deviation": -1.50, "Revised deviation": -1.50,
                 "Review action": "entered", "Reviewer": "JN",
                 "Review date": "2026-08-11", "Status": "active"}]
    r2 = apply_expect("02_nonzero_ok", dev_pend, dev_rlog, expect_written=True)
    if r2["written"]:
        rep = VER.verify(SRC, out("02_nonzero_ok"),
                         os.path.join(tmp, "pend_02_nonzero_ok.csv"),
                         os.path.join(tmp, "rlog_02_nonzero_ok.csv"))
        record("02_nonzero_verify",
               "verify=PASS,1 nonzero",
               f"verify={'PASS' if rep['pass'] else 'FAIL'},{rep['counts']['candidate_nonzero_delta']} nonzero",
               rep["pass"] and rep["counts"]["candidate_nonzero_delta"] == 1)

    # ---- 3. missing source -------------------------------------------------
    apply_expect("03_missing_source", [base_row(source="")], expect_written=False)
    # ---- 4. invalid date ---------------------------------------------------
    apply_expect("04_invalid_date", [base_row(source_date="08/04/2026")], expect_written=False)
    # ---- 5. duplicate team -------------------------------------------------
    apply_expect("05_duplicate", [base_row(), base_row(notes="dup")], expect_written=False)
    # ---- 6. unknown abbreviation -------------------------------------------
    apply_expect("06_unknown_abbrev", [base_row(abbrev="ZZZ", team="Nowhere")], expect_written=False)
    # ---- 7. low-confidence row ---------------------------------------------
    apply_expect("07_low_conf", [base_row(confidence="L")], expect_written=False)
    # ---- 8. baseline mismatch without approval -----------------------------
    apply_expect("08_mismatch_noapproval",
                 [base_row(baseline_qb="A Starter", active_qb="B Replacement", active_value=-1.00)],
                 rlog_rows=[], expect_written=False)
    # ---- 9. out-of-bounds deviation (with a matching approved rlog) --------
    oob_rlog = [{"Abbrev": "STAN", "Active QB": "B Replacement",
                 "Applied deviation": -5.00, "Revised deviation": -5.00,
                 "Review action": "entered", "Reviewer": "JN",
                 "Review date": "2026-08-11", "Status": "active"}]
    apply_expect("09_out_of_bounds",
                 [base_row(abbrev="STAN", team="Stanford", baseline_qb="A Starter",
                          active_qb="B Replacement", active_value=-5.00)],
                 rlog_rows=oob_rlog, expect_written=False)

    # ---- 10. attempt to overwrite a formula (mutated temp source) ----------
    mut_src = os.path.join(tmp, "src_formula_injected.xlsx")
    shutil.copyfile(SRC, mut_src)
    wbm = L.load_wb(mut_src)
    # IOWA is row 24; inject a formula into its Baseline value (D24) input cell
    wbm["QB VALUES"].cell(row=24, column=L.COL["baseline_value"]).value = "=1+1"
    wbm.save(mut_src)
    apply_expect("10_formula_overwrite", [base_row()], source=mut_src, expect_written=False)

    # ---- 11. unexpected unrelated-cell change (verifier must catch) --------
    # build a valid candidate, then mutate an unrelated cell, then verify.
    ok_out = out("01_zero_init")
    if os.path.exists(ok_out):
        tampered = os.path.join(tmp, "cand_11_tampered.xlsx")
        shutil.copyfile(ok_out, tampered)
        wbt = L.load_wb(tampered)
        old = wbt["SETTINGS"]["C5"].value
        wbt["SETTINGS"]["C5"].value = ("__TAMPER__" if not isinstance(old, (int, float)) else (old or 0) + 999)
        wbt.save(tampered)
        rep = VER.verify(SRC, tampered, os.path.join(tmp, "pend_01_zero_init.csv"), "")
        record("11_unrelated_change", "verify=FAIL", f"verify={'PASS' if rep['pass'] else 'FAIL'}",
               rep["pass"] is False, "verifier must reject unrelated change")
    else:
        record("11_unrelated_change", "verify=FAIL", "SKIPPED (no base candidate)", False)

    # ---- 12. empty pending ledger -> no candidate --------------------------
    apply_expect("12_empty_ledger", [], expect_written=False)

    # ---- source workbook unchanged overall ---------------------------------
    src_sha1 = L.sha256(SRC)
    record("source_unchanged_overall", src_sha0[:12], src_sha1[:12], src_sha0 == src_sha1)

    # ---- report ------------------------------------------------------------
    print("\n" + "=" * 78)
    print(f"{'SCENARIO':30s} {'EXPECTED':22s} {'ACTUAL':22s} RESULT")
    print("-" * 78)
    allok = True
    for name, exp, act, ok, note in results:
        allok = allok and ok
        print(f"{name:30s} {exp:22s} {act:22s} {'PASS' if ok else 'FAIL'}"
              + (f"  ({note})" if note else ""))
    print("=" * 78)
    print(f"{'ALL SCENARIOS PASSED' if allok else 'SOME SCENARIOS FAILED'} "
          f"({sum(1 for *_, ok, _ in results if ok)}/{len(results)})")

    if not a.keep:
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"cleaned temp dir {tmp}")
    else:
        print(f"kept temp dir {tmp}")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
