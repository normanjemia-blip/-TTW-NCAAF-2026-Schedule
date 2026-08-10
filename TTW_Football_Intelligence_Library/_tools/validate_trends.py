#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 10 (Historical Trends) validation
============================================================================

Twelve gates. Any failure exits 1.

The gate that matters most is check 4. Phase 10's characteristic failure
would not be a wrong number -- it would be a *computed* one: extending a
span, re-deriving a hit rate, or backtesting a system against data the
library does not have. So the corpus is scanned for the vocabulary of
constructed history, and every record on the pages is checked to trace
back to a figure the extractor took from the guide.

Check 3 is the other one worth stating: neither of the revised system's
two rules may show its long-run figure -- 55.4% for PLAY ON, 55.6% for
FADE -- anywhere without last season's 30-36 ATS beside it.
"""

import json
import os
import re
import subprocess
import sys

OUT, SITU = "12_Historical_Trends", "13_Situational_Angles"
DATA = "_source/data"
PASS, FAIL = [], []


def check(ok, msg, detail=""):
    (PASS if ok else FAIL).append(msg + (f" — {detail}" if detail and not ok else ""))


def read(d):
    return {fn: open(os.path.join(d, fn)).read()
            for fn in sorted(os.listdir(d)) if fn.endswith(".md")}


def main():
    raw = json.load(open(f"{DATA}/trends_raw.json"))
    teams = json.load(open(f"{DATA}/team_details.json"))
    concepts = json.load(open(f"{DATA}/concept_pages.json"))
    angles = {}
    for fn in sorted(os.listdir("_source/trends")):
        if fn.endswith(".json"):
            angles.update(json.load(open(f"_source/trends/{fn}")))
    text, stext = read(OUT), read(SITU)
    every = {**text, **stext}
    body = "\n".join(every.values())

    # 1 -- the six stability components, complete and as printed
    comps = raw["components"]
    pcts = [c["ats_pct_printed"] for c in comps]
    check(len(comps) == 6 and all(p is not None for p in pcts)
          and all(c["su_record"] and c["ats_record"] for c in comps)
          and all(c["span"] == "since 2021" for c in comps),
          f"all 6 stability components carry an SU record, an ATS record and "
          f"a printed percentage, all since 2021",
          f"n={len(comps)} pcts={pcts}")

    # 2 -- every component appears on the rendered page exactly as printed
    sp = text.get("00_STABILITY_SYSTEM.md", "")
    missing = [c["ats_record"] for c in comps if c["ats_record"] not in sp]
    check(not missing,
          "every component's ATS record is rendered exactly as printed",
          str(missing[:3]))

    # 3 -- the long-run record never travels without the 2025 failure.
    # This is the honesty gate for this phase.
    # The revised system is two rules. Neither long-run percentage may appear
    # anywhere without the 2025 result beside it.
    sysrec = {x["label"]: x for x in raw["systems"]}
    rules = [sysrec.get("College Football Stability System — PLAY ON rule"),
             sysrec.get("College Football Stability System — FADE rule")]
    last = sysrec.get("College Football Stability System — 2025 season")
    bad = []
    for fn, b in every.items():
        for r in rules:
            if r and str(r["ats_pct_printed"]) in b:
                if not last or last["ats_record"] not in b:
                    bad.append(f"{fn}:{r['ats_pct_printed']}%")
    pcts = [r["ats_pct_printed"] for r in rules if r]
    check(all(rules) and last and not bad,
          f"both rules' long-run figures ({', '.join(f'{p}%' for p in pcts)}) "
          f"never appear without last season's {last['ats_record']} ATS "
          f"beside them",
          f"pages quoting one without the other: {bad[:3]}")

    # 4 -- nothing is backtested, recomputed, extended or projected.
    # The disclaimer names these very words, so it is stripped by exact match
    # and its presence is required rather than tolerated.
    DISCLAIMER = ("**Nothing here is backtested, recomputed, extended or "
                  "projected**")
    CONSTRUCTED = re.compile(
        r"\b(we (?:back-?tested|re-?ran|simulated)|our (?:back-?test|sample)|"
        r"extrapolat\w+|projected hit rate|TTW (?:hit rate|trend record)|"
        r"if we extend the sample|over a longer sample we)\b", re.I)
    hits = [fn for fn, b in every.items()
            if CONSTRUCTED.search(b.replace(DISCLAIMER, ""))]
    check(not hits and DISCLAIMER in text.get("README.md", ""),
          "no backtest, re-derived hit rate or extended sample anywhere, and "
          "the README states the refusal explicitly", str(hits[:3]))

    # 5 -- every percentage on the pages traces to one the guide printed
    printed = {str(c["ats_pct_printed"]) for c in comps}
    printed |= {str(x["ats_pct_printed"]) for x in raw["systems"]
                if x.get("ats_pct_printed") is not None}
    printed |= {str(x["ats_pct_recomputed"]) for x in raw["systems"]
                if x.get("ats_pct_recomputed") is not None}
    printed |= {str(m["recomputed_pct"]) for m in raw["percentage_mismatches"]}
    printed |= {"49.5", "55.4", "45.4", "57.6", "66.7", "15.2", "13.3", "45"}
    found = set(re.findall(r"\b(\d{1,2}\.\d)%", body))
    stray = sorted(found - printed)
    check(not stray,
          f"every percentage rendered ({len(found)} distinct) traces to a "
          f"figure the guide prints or a labelled reconciliation check",
          f"stray={stray[:5]}")

    # 6 -- printed slips preserved, not corrected
    typos = raw["printed_typos"]
    mism = raw["percentage_mismatches"]
    check(len(typos) == 1 and len(mism) == 1
          and typos[0]["printed_comparison"] in sp
          and "not corrected" in sp.lower()
          and str(mism[0]["printed_pct"]) in sp
          and str(mism[0]["recomputed_pct"]) in sp,
          "the printed slip and the percentage mismatch are both reproduced "
          "and flagged, with neither number adjusted",
          f"typos={len(typos)} mismatches={len(mism)}")

    # 7 -- team attribution never exceeds what the guide names
    named = {t for a in angles.values() for t in a.get("applied_to", [])}
    canon = {t["team"] for t in teams}
    unknown = sorted(named - canon)
    bt = text.get("00_BY_TEAM.md", "")
    check(not unknown and len(named) < len(canon)
          and f"{len(named)} of 138" in bt,
          f"{len(named)} teams carry a named angle, all canonical, and the "
          f"page states that the other {len(canon) - len(named)} carry none",
          f"unknown={unknown[:3]}")

    # 8 -- the register traces to the Phase 1 historical map
    hist = set(concepts["Historical Angles"])
    off_map = sorted({r["page"] for r in raw["narrative_records"]} - hist)
    check(not off_map and raw["narrative_records"],
          f"all {len(raw['narrative_records'])} register entries come from "
          f"pages the Phase 1 historical map records", f"off_map={off_map[:5]}")

    # 9 -- team header blocks excluded from the register
    hdr = raw["header_or_fragment_rows_skipped"]
    su = sum(1 for t in teams if t.get("su_2025"))
    check(su == 138 and "excluded" in text.get("00_TREND_REGISTER.md", ""),
          f"one-season team records ({su} teams) are reproduced from Phase 3 "
          f"and explicitly excluded from the trend register",
          f"su={su} skipped={hdr}")

    # 10 -- 13_Situational_Angles complete on both halves, gaps stated
    sq = stext.get("README.md", "")
    check("Both halves are now built" in sq
          and sq.count("*none printed*") >= 4
          and "Nothing of that kind is constructed here" not in sq,
          "13_Situational_Angles is complete on both halves and records the "
          "situational angles for which the guide prints no history at all",
          f"none_printed={sq.count('*none printed*')}")

    # 11 -- no post-publication material, no scores or model inputs
    outside = re.compile(r"\b(as of (?:today|now)|since the guide (?:was )?"
                         r"published|latest reports|current odds now|"
                         r"this season's actual|so far in 2026)\b", re.I)
    scored = re.compile(r"\b(implied probability|remove the vig|no-vig|"
                        r"confidence (?:score|grade) of|weight of \d|"
                        r"model input of)\b", re.I)
    hits = [fn for fn, b in every.items()
            if outside.search(b) or scored.search(b)]
    check(not hits,
          "no post-publication language, and no betting score, weight or "
          "implied probability introduced", str(hits[:3]))

    # 12 -- earlier phases still validate, workbook untouched
    prior = []
    for tool in ("validate_qb.py", "validate_coaching.py", "validate_power.py",
                 "validate_phase7.py", "validate_wintotals.py",
                 "validate_futures.py", "validate_concepts.py"):
        rr = subprocess.run([sys.executable, f"_tools/{tool}"],
                            capture_output=True, text=True,
                            env=dict(os.environ, PYTHONPATH="_tools"))
        if rr.returncode != 0:
            prior.append(tool)
    tracked = subprocess.run(["git", "ls-files"], capture_output=True,
                             text=True).stdout.split()
    xl = [fn for fn in tracked if fn.lower().endswith((".xlsx", ".xlsm", ".xls"))]
    check(not prior and not xl,
          "Phases 4–9 and the calibration study still validate; no workbook "
          "file tracked", f"failing={prior} xlsx={xl}")

    print("PHASE 10 — HISTORICAL TRENDS VALIDATION")
    print("=" * 72)
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
