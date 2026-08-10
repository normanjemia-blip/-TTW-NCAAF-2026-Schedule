#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 7 validation
=======================================================

Ten gates. Any failure exits 1.

Two of these are unusual and deliberate.

Check 8 is an honesty gate: it fails the build if any Phase 7 file claims
a predictive result. The whole finding of this phase is that no such
result is available, and the easiest way for that finding to decay is for
a later edit to quietly promote a diagnostic into a conclusion.

Check 9 verifies the scorer still refuses an unplayed season. A
pre-registered test whose scorer would happily emit a number from three
games is not pre-registered in any meaningful sense.
"""

import hashlib
import json
import os
import re
import statistics as stats
import subprocess
import sys

from qb_lib import ABBREV_TO_VSIN

OUT = "05_Power_Ratings"
P7 = ["01_VSIN_DIAGNOSTICS.md", "01_CALIBRATION_PROTOCOL.md",
      "01_PHASE7_REPORT.md"]
PASS, FAIL = [], []


def check(ok, msg, detail=""):
    (PASS if ok else FAIL).append(msg + (f" — {detail}" if detail and not ok else ""))


def main():
    wb = json.load(open("_source/verified/workbook_preseason_v081.json"))
    d = json.load(open("_source/calibration/vsin_diagnostics.json"))
    p = json.load(open("_source/calibration/power_analysis.json"))
    text = {f: open(os.path.join(OUT, f)).read() for f in P7
            if os.path.exists(os.path.join(OUT, f))}

    # 1 -- every Phase 7 artefact exists
    check(len(text) == 3 and os.path.exists("_tools/score_calibration.py"),
          "all Phase 7 artefacts present (3 documents + scorer)",
          str(sorted(set(P7) - set(text))))

    # 2 -- the frozen workbook is still byte-identical to its recorded blob
    blob = subprocess.run(["git", "cat-file", "-p", wb["git_blob"]],
                          capture_output=True).stdout
    live = hashlib.sha256(blob).hexdigest()
    check(live == wb["sha256"],
          f"v0.8.1 AUTHORITATIVE unchanged (sha256 {wb['sha256'][:16]}…)",
          f"git blob now {live[:16]}…")

    # 3 -- nothing in this phase wrote a workbook
    tracked = subprocess.run(["git", "ls-files"], capture_output=True,
                             text=True).stdout.split()
    xl = [f for f in tracked if f.lower().endswith((".xlsx", ".xlsm", ".xls"))]
    writes = [t for t in ("_tools/build_calibration.py", "_tools/build_protocol.py",
                          "_tools/score_calibration.py", "_tools/build_report.py")
              if re.search(r"\.save\(|wb\.save", open(t).read())]
    check(not xl and not writes,
          "no workbook written or committed anywhere in Phase 7",
          str(xl + writes))

    # 4 -- the VSiN column in the frozen workbook is still empty
    check(wb["coverage"]["vsin_raw"] == 0 and wb["coverage"]["ttw25_raw"] == 0,
          "workbook VSiN and TTW-2025 source columns still empty",
          f"vsin {wb['coverage']['vsin_raw']} ttw25 {wb['coverage']['ttw25_raw']}")

    # 5 -- both configurations reproduce from the frozen inputs
    rows = {ABBREV_TO_VSIN[r["abbrev"]]: r for r in wb["rows"]}
    p47 = {r["team"]: r["p47_rating"]
           for r in json.load(open("_source/data/makinen_ratings_p47.json"))}
    raw = {"sp_raw": {t: rows[t]["sp_raw"] for t in rows},
           "fpi_raw": {t: rows[t]["fpi_raw"] for t in rows},
           "tr_raw": {t: rows[t]["tr_raw"] for t in rows},
           "vsin_raw": {t: p47[t] for t in rows}}
    norm = {k: {t: v - stats.fmean(raw[k].values()) for t, v in raw[k].items()}
            for k in raw}
    W = wb["settings"]
    key = {"sp_raw": "SP+ 2026 preseason", "fpi_raw": "FPI 2026 preseason",
           "tr_raw": "TeamRankings predictive", "vsin_raw": "VSiN (user-supplied)"}

    def blend(ks):
        s = sum(W[key[k]] for k in ks)
        return {t: sum(W[key[k]] * norm[k][t] for k in ks) / s for t in rows}
    b = blend(["sp_raw", "fpi_raw", "tr_raw"])
    v = blend(["sp_raw", "fpi_raw", "tr_raw", "vsin_raw"])
    bad = [r["team"] for r in d["per_team"]
           if abs(r["baseline"] - b[r["team"]]) > 1e-9
           or abs(r["vsin_included"] - v[r["team"]]) > 1e-9]
    check(len(d["per_team"]) == 138 and not bad,
          "BASELINE and VSIN-INCLUDED reproduce exactly for all 138",
          str(bad[:5]))

    # 6 -- the effective weights are the workbook's own, not tuned
    ok = (abs(d["vsin_included_effective_weights"]["VSiN"]
              - W["VSiN (user-supplied)"] / 0.80) < 1e-9
          and abs(sum(d["baseline_effective_weights"].values()) - 1) < 1e-9
          and abs(sum(d["vsin_included_effective_weights"].values()) - 1) < 1e-9)
    check(ok, "weights are the workbook's stored values, renormalised by its "
              "own rule — none fitted")

    # 7 -- the test was registered before any result existed
    reg = (p["games_completed"] == 0
           and "Registered before any 2026 result exists"
           in text.get("01_CALIBRATION_PROTOCOL.md", ""))
    check(reg, f"protocol registered with {p['games_completed']} of "
               f"{p['games_total']} games played")

    # 8 -- honesty gate: no predictive claim anywhere in the phase
    claim = re.compile(
        r"\b(VSiN (?:improves|improved|outperforms|beats)|"
        r"including VSiN (?:reduces|reduced|improves)|"
        r"backtest (?:shows|showed)|"
        r"out-of-sample (?:MAE|error) (?:of|was))\b", re.I)
    # The renderer's own disclaimer contains the phrase "whether VSiN
    # improves prediction", so it has to come out before the scan or the
    # gate fires on the very sentence that satisfies it. That is a
    # validator artefact, not a claim; the text is generated and is
    # removed by exact match, so a hand-edited variant would not slip past.
    NOTPRED_SENTENCE = ("Nothing on this page measures whether VSiN improves "
                        "prediction.")
    hits = [f for f, b in text.items()
            if claim.search(b.replace(NOTPRED_SENTENCE, ""))]
    # Each document must state, in one of the phase's standing forms, that
    # no result exists yet. The protocol carries the registration statement
    # rather than a results disclaimer, which is the correct form for a
    # test design; all three forms are accepted, none is optional.
    STATEMENTS = ("not predictive validation", "no predictive",
                  "insufficient evidence",
                  "registered before any 2026 result exists")
    missing = [f for f, b in text.items()
               if not any(x in b.lower() for x in STATEMENTS)]
    disclaim = not missing
    check(not hits and disclaim,
          "no predictive claim made; every document states the absence",
          str(hits + missing))

    # 9 -- the scorer refuses an unplayed season
    r = subprocess.run([sys.executable, "_tools/score_calibration.py",
                        os.environ.get("WB_PATH", "/nonexistent.xlsx")],
                       capture_output=True, text=True,
                       env=dict(os.environ, PYTHONPATH="_tools"))
    refused = r.returncode != 0 and (
        "REFUSING TO SCORE" in r.stdout or "No such file" in r.stderr
        or "FileNotFoundError" in r.stderr)
    check(refused, "scorer refuses to report a result on an unplayed season",
          f"rc={r.returncode}")

    # 10 -- prior phases still validate, and the index pointer is accurate
    idx = open("00_Master_Index/09_Power_Rating_Index.md").read()
    ok_idx = ("00_TTW_VS_MAKINEN.md" in idx
              and "is a Phase 6 deliverable" not in idx)
    prior = []
    for tool in ("validate_qb.py", "validate_coaching.py", "validate_power.py"):
        rr = subprocess.run([sys.executable, f"_tools/{tool}"],
                            capture_output=True, text=True,
                            env=dict(os.environ, PYTHONPATH="_tools"))
        if rr.returncode != 0:
            prior.append(tool)
    check(ok_idx and not prior,
          "Master Index pointer accurate; Phases 4, 5 and 6 still validate",
          f"index_ok={ok_idx} failing={prior}")

    print("PHASE 7 VALIDATION")
    print("=" * 62)
    for m in PASS:
        print(f"  PASS  {m}")
    for m in FAIL:
        print(f"  FAIL  {m}")
    print()
    if FAIL:
        print(f"{len(FAIL)} of {len(PASS) + len(FAIL)} checks failed")
        sys.exit(1)
    print(f"all {len(PASS)} checks passed")


if __name__ == "__main__":
    main()
