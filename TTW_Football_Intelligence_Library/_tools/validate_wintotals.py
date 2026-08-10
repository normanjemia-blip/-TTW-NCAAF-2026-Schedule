#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 7 (Win Totals) validation
====================================================================

Ten gates. Any failure exits 1.

Check 2 is the one that matters most. The defect this phase found in the
Phase 2 artefact passed its original validation because the *counts* were
right — 14 Overs and 15 Unders — while two teams were mis-seated and a
third was missing. So this harness checks membership against a re-parse of
pp. 22-27, not just the totals.
"""

import json
import os
import re
import subprocess
import sys

from coach_lib import slug
from wintotal_lib import load_conference_rows, load_feature, load_notes, load_team_picks

OUT = "06_Win_Totals"
INDEXES = ["README.md", "00_FEATURE_PICKS.md", "00_ALL_TEAMS.md",
           "00_OVER_INDEX.md", "00_UNDER_INDEX.md", "00_DEPENDENCY_INDEX.md",
           "00_AGREEMENT_INDEX.md", "00_DISAGREEMENT_INDEX.md",
           "00_WINTOTAL_VS_POWER.md", "00_SOURCE_CONFLICTS.md"]
PASS, FAIL = [], []


def check(ok, msg, detail=""):
    (PASS if ok else FAIL).append(msg + (f" — {detail}" if detail and not ok else ""))


def main():
    feature, feat = load_feature()
    rows = load_conference_rows()
    picks = load_team_picks()
    notes = load_notes()
    text = {f: open(os.path.join(OUT, f)).read() for f in INDEXES
            if os.path.exists(os.path.join(OUT, f))}
    teamfiles = {t: open(os.path.join(OUT, slug(t))).read() for t in feat
                 if os.path.exists(os.path.join(OUT, slug(t)))}

    # 1 -- counts reconcile to the previously validated 14 / 15
    c = feature["counts"]
    check(c["total"] == 29 and c["over"] == 14 and c["under"] == 15,
          f"feature counts reconcile: {c['over']} Overs, {c['under']} Unders",
          str(c))

    # 2 -- membership, not just counts, matches a fresh parse of pp. 22-27
    r = subprocess.run([sys.executable, "_tools/extract_wintotals.py"],
                       capture_output=True, text=True,
                       env=dict(os.environ, PYTHONPATH="_tools"))
    fresh, ffeat = load_feature()
    same = {(t, e["side"], e["number"]) for t, e in ffeat.items()} == \
           {(t, e["side"], e["number"]) for t, e in feat.items()}
    p2 = {(w["team"], w["side"], float(w["number"]))
          for w in json.load(open("_source/data/phase2_win_totals.json"))}
    now = {(t, e["side"], e["number"]) for t, e in feat.items()}
    check(r.returncode == 0 and same and p2 == now,
          "every pick reproduces from pp. 22–27 by team, side and number; "
          "the repaired Phase 2 artefact now agrees",
          f"reparse_ok={same} phase2_matches={p2 == now} "
          f"diff={sorted(p2 ^ now)[:4]}")

    # 2b -- Makinen's printed records reconcile with his printed percentages.
    # p. 22 breaks "34- 17-1" across a line; an earlier parse dropped the 34
    # and stored "17-1", which reconciles to 94.4%, not the printed 66.7%.
    def reconciles(rec, pct):
        try:
            w, l = [int(x) for x in rec.split("-")[:2]]
            return abs(round(100 * w / (w + l), 1) - float(pct.strip("%"))) <= 0.1
        except (AttributeError, ValueError, ZeroDivisionError):
            return False
    ov = reconciles(feature["stated_record_overall"],
                    feature["stated_record_overall_pct"])
    un = reconciles(feature["stated_record_unders"],
                    feature["stated_record_unders_pct"])
    check(ov and un,
          f"stated records reconcile with stated percentages: "
          f"{feature['stated_record_overall']} = "
          f"{feature['stated_record_overall_pct']}, "
          f"{feature['stated_record_unders']} = "
          f"{feature['stated_record_unders_pct']} on Unders",
          f"overall={ov} unders={un}")

    # 3 -- one record per feature team, all 26 fields
    bad = []
    for t, body in teamfiles.items():
        nums = [int(n) for n in re.findall(r"^\| (\d+) \| ", body, re.M)]
        if nums != list(range(1, 27)):
            bad.append(f"{t}:{nums}")
    check(len(teamfiles) == 29 and not bad,
          "29 records rendered, fields 1–26 present and in order",
          str(bad[:2]))

    # 4 -- prices are recorded as absent, never invented
    invented = [t for t, b in teamfiles.items()
                if re.search(r"\| [45] \| (?:Over|Under) price \| (?!Not addressed)",
                             b)]
    check(not invented and feature["prices_printed"] is False,
          "no Over/Under price invented — the guide prints none",
          str(invented[:5]))

    # 5 -- every authored note carries the sentinel where unsupported
    missing = [t for t in feat if t not in notes]
    fields = ("over_argument", "under_argument", "schedule_argument",
              "qb_argument", "coaching_argument", "roster_argument",
              "key_games", "floor_case", "ceiling_case", "risks",
              "futures_interaction", "best_bet_interaction",
              "other_opinions", "internal_disagreement", "conflicts")
    incomplete = [f"{t}.{k}" for t in notes for k in fields
                  if not (notes[t].get(k) or "").strip()]
    check(not missing and not incomplete,
          f"all 29 notes authored with every field populated "
          f"({sum(1 for t in notes for k in fields if notes[t][k] == 'Not addressed in guide.')} "
          f"sentinel uses)",
          str((missing + incomplete)[:5]))

    # 6 -- team mappings are canonical and page provenance survives
    canon = set(rows) == set(picks) and len(rows) == 138
    pages = [t for t, e in feat.items()
             if f"p. {e['page']}" not in teamfiles.get(t, "")]
    check(canon and not pages,
          "canonical 138-team mapping intact; feature page cited on every record",
          f"canonical={canon} missing_page={pages[:4]}")

    # 7 -- contributor attribution correct
    attr = feature["author"] == "Steve Makinen"
    wrong = [t for t, b in teamfiles.items() if "Steve Makinen" not in b]
    check(attr and not wrong,
          "feature attributed to Steve Makinen on every record", str(wrong[:4]))

    # 8 -- disagreement preserved, never resolved
    dis = text.get("00_DISAGREEMENT_INDEX.md", "")
    resolved = re.search(r"\b(the correct (?:pick|side) is|we side with|"
                         r"the right number is|resolved in favou?r of)\b", dis, re.I)
    sidediff = [t for t in feat if picks[t]["pick"]
                and picks[t]["pick"]["side"] != feat[t]["side"]]
    listed = all(t in dis for t in sidediff)
    check(not resolved and listed and "Nothing here is resolved" in dis,
          f"all {len(sidediff)} opposite-side contradictions preserved, none resolved",
          f"resolved={bool(resolved)} listed={listed}")

    # 9 -- no post-publication or outside research
    BANNER = "No outside research, no post-publication updates."
    outside = re.compile(r"\b(as of (?:today|now)|since the guide (?:was )?published"
                         r"|latest reports|current odds|has since)\b", re.I)
    hits = [f for f, b in {**text, **teamfiles}.items()
            if outside.search(b.replace(BANNER, ""))]
    check(not hits, "no post-publication or outside-research language",
          str(hits[:4]))

    # 10 -- earlier phases untouched, workbook untouched
    prior = []
    for tool in ("validate_qb.py", "validate_coaching.py", "validate_power.py",
                 "validate_phase7.py"):
        rr = subprocess.run([sys.executable, f"_tools/{tool}"],
                            capture_output=True, text=True,
                            env=dict(os.environ, PYTHONPATH="_tools"))
        if rr.returncode != 0:
            prior.append(tool)
    tracked = subprocess.run(["git", "ls-files"], capture_output=True,
                             text=True).stdout.split()
    xl = [f for f in tracked if f.lower().endswith((".xlsx", ".xlsm", ".xls"))]
    check(not prior and not xl,
          "Phases 4–6 and the calibration study still validate; no workbook "
          "touched", f"failing={prior} xlsx={xl}")

    print("PHASE 7 — WIN TOTALS VALIDATION")
    print("=" * 64)
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
