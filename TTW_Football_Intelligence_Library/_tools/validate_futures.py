#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 8 (Futures) validation
=================================================================

Twelve gates. Any failure exits 1.

The gate that carries the most weight is check 2. Phase 8's central claim
is that each of the 374 p. 4 cells belongs to a *named person*, and a
single dropped or shifted cell would misattribute picks to real people
for the rest of a row without changing any count. So the grid is re-read
from the PDF and compared against Phase 2's independent reading-order
extraction, cell for cell, in every category.
"""

import json
import os
import re
import subprocess
import sys

from futures_lib import (NA, bet_key, load_best_bets, load_heisman,
                         load_notes, load_predictions, load_team_prices)

OUT = "07_Futures"
INDEXES = ["README.md", "00_PREDICTIONS.md", "00_CONSENSUS.md",
           "00_BEST_BETS.md", "00_BY_CONTRIBUTOR.md", "00_HEISMAN.md",
           "00_TEAM_FUTURES.md", "00_WINTOTAL_OVERLAP.md",
           "00_DISAGREEMENT.md", "00_SOURCE_CONFLICTS.md"]
PASS, FAIL = [], []


def check(ok, msg, detail=""):
    (PASS if ok else FAIL).append(msg + (f" — {detail}" if detail and not ok else ""))


def main():
    preds, real, anomalies = load_predictions()
    roster = preds["roster"]
    bb = load_best_bets()
    bets = bb["bets"]
    heis = load_heisman()
    prices = load_team_prices()
    notes = load_notes()
    text = {f: open(os.path.join(OUT, f)).read() for f in INDEXES
            if os.path.exists(os.path.join(OUT, f))}
    every = "\n".join(text.values())

    # 1 -- the grid is complete and rectangular
    sizes = {len(c["picks"]) for c in preds["categories"]}
    check(len(roster) == 22 and len(real) == 17 and len(anomalies) == 1
          and sizes == {22},
          f"p. 4 grid complete: {len(real)} categories × {len(roster)} "
          f"contributors = {len(real) * len(roster)} attributed cells, "
          f"plus 1 anomaly row",
          f"roster={len(roster)} real={len(real)} sizes={sizes}")

    # 2 -- attribution survives a fresh parse AND agrees with Phase 2
    r = subprocess.run([sys.executable, "_tools/extract_futures.py"],
                       capture_output=True, text=True,
                       env=dict(os.environ, PYTHONPATH="_tools"))
    fresh, freal, _ = load_predictions()
    same = [[k["pick"] for k in c["picks"]] for c in freal] == \
           [[k["pick"] for k in c["picks"]] for c in real]
    p2 = json.load(open("_source/data/phase2_predictions.json"))
    agree = all([k["pick"] for k in c["picks"]] == p2.get(c["category"])
                for c in real)
    names_ok = all(k["contributor"] == roster[i]
                   for c in real for i, k in enumerate(c["picks"]))
    check(r.returncode == 0 and same and agree and names_ok,
          "every cell reproduces from p. 4 and matches Phase 2's independent "
          "reading-order extraction, in every category",
          f"reparse={same} phase2={agree} columns_aligned={names_ok}")

    # 3 -- best bets: count, roster, and reasoning all present
    noprose = [b["headline"] for b in bets if b["words"] < 15]
    check(len(bets) == 62 and len(bb["roster"]) == 20 and not noprose,
          f"{len(bets)} best bets by {len(bb['roster'])} contributors, every "
          f"one carrying its reasoning ({sum(b['words'] for b in bets):,} words)",
          f"missing_prose={noprose[:3]}")

    # 4 -- every bet and every Heisman pick has an authored note
    keys = {bet_key(b) for b in bets} | {f"heisman|{p['player']}"
                                         for p in heis["picks"]}
    missing = sorted(keys - set(notes))
    thin = [k for k in keys if len((notes.get(k, {}).get("summary") or "")
                                   .split()) < 25]
    check(not missing and not thin,
          f"all {len(keys)} recommendations carry authored TTW reference "
          f"notes (+2 framing notes)",
          f"missing={missing[:2]} thin={thin[:2]}")

    # 5 -- no price invented, and genuine absences recorded as absences
    printed = sum(1 for v in prices.values() for r_ in v["rows"] if r_["price"])
    absent = sorted(t for t, v in prices.items()
                    if any(r_["no_price_printed"] for r_ in v["rows"]))
    labelled = all(r_["market"] for v in prices.values() for r_ in v["rows"])
    check(len(prices) == 138 and printed == 412 and labelled
          and absent == ["Connecticut Huskies", "Notre Dame Fighting Irish"],
          f"138 teams × 3 markets = 414 rows, {printed} prices printed; the "
          f"2 without one are Independents and are recorded as absences",
          f"printed={printed} absent={absent}")

    # 6 -- team prices agree with what Phase 3 already stored
    td = {t["team"]: t["futures"]
          for t in json.load(open("_source/data/team_details.json"))}
    dis = []
    for t, v in prices.items():
        a = [(r_["market"], r_["price"]) for r_ in v["rows"] if r_["price"]]
        b = [(x["market"], x["price"].replace("−", "-"))
             for x in td[t]]
        if a != b:
            dis.append(t)
    check(not dis,
          "all 138 coordinate-read futures boards agree with the prices "
          "Phase 3 stored independently", f"differ={dis[:4]}")

    # 7 -- the SUN BELT CHAMP anomaly is preserved, not corrected
    a = anomalies[0]
    nfl = {"Falcons", "Panthers", "Bucs", "Saints"}
    kept = nfl & {k["pick"] for k in a["picks"]}
    conf = text.get("00_SOURCE_CONFLICTS.md", "")
    check(a["category"] == "SUN BELT CHAMP" and kept == nfl
          and "SUN BELT CHAMP" in conf and "not corrected" in conf.lower(),
          "the SUN BELT CHAMP row is reproduced with its NFL names intact and "
          "flagged, not corrected", f"kept={sorted(kept)}")

    # 8 -- disagreement preserved and not adjudicated
    dis_txt = text.get("00_DISAGREEMENT.md", "")
    resolved = re.search(r"\b(the correct pick is|we side with|the right "
                         r"answer is|resolved in favou?r of|house (?:pick|view))\b",
                         dis_txt, re.I)
    honest = "field is larger than four" in dis_txt
    check(not resolved and honest and "not resolved" in dis_txt.lower(),
          "contributor disagreement preserved unresolved, and the 12-team "
          "playoff is not misreported as a contradiction with a 4-slot grid",
          f"resolved={bool(resolved)} playoff_caveat={honest}")

    # 9 -- consensus is labelled derived and disclaimed everywhere it appears
    cons = text.get("00_CONSENSUS.md", "")
    check("TTW DERIVED" in cons
          and "not a probability" in cons
          and "not a confidence grade" in cons
          and "not a model input" in cons,
          "consensus counts labelled TTW DERIVED and explicitly disclaimed as "
          "not a probability, confidence grade or model input")

    # 10 -- no implied-probability or vig arithmetic anywhere.
    # The README's own disclaimer names the things the database refuses to do
    # and so matches this guard. It is stripped by exact match before the
    # scan, and its presence is required rather than merely tolerated -- a
    # validator artefact, not a finding.
    DISCLAIMER = ("It does not convert a price into an implied probability, "
                  "remove vig, rank contributors by past accuracy, or derive "
                  "a house position from a staff vote.")
    banned = re.compile(r"\b(implied probability|remove the vig|no-vig|"
                        r"devig|fair odds|expected value|edge of \d|"
                        r"\d+(?:\.\d+)?% implied)\b", re.I)
    hits = [fn for fn, b in text.items()
            if banned.search(b.replace(DISCLAIMER, ""))]
    check(not hits and DISCLAIMER in text.get("README.md", ""),
          "no implied-probability, vig-removal or expected-value arithmetic, "
          "and the README states the refusal explicitly",
          str(hits[:3]))

    # 11 -- no post-publication or outside research
    outside = re.compile(r"\b(as of (?:today|now)|since the guide (?:was )?"
                         r"published|latest reports|current odds now|has since"
                         r"|this season's actual)\b", re.I)
    hits = [fn for fn, b in text.items() if outside.search(b)]
    check(not hits, "no post-publication or outside-research language",
          str(hits[:3]))

    # 12 -- earlier phases still validate, workbook untouched
    prior = []
    for tool in ("validate_qb.py", "validate_coaching.py", "validate_power.py",
                 "validate_phase7.py", "validate_wintotals.py"):
        rr = subprocess.run([sys.executable, f"_tools/{tool}"],
                            capture_output=True, text=True,
                            env=dict(os.environ, PYTHONPATH="_tools"))
        if rr.returncode != 0:
            prior.append(tool)
    tracked = subprocess.run(["git", "ls-files"], capture_output=True,
                             text=True).stdout.split()
    xl = [fn for fn in tracked if fn.lower().endswith((".xlsx", ".xlsm", ".xls"))]
    check(not prior and not xl,
          "Phases 4–7 and the calibration study still validate; no workbook "
          "file tracked", f"failing={prior} xlsx={xl}")

    print("PHASE 8 — FUTURES VALIDATION")
    print("=" * 66)
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
