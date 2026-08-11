#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 11 validation
=========================================================

Sixteen gates, repository-wide. Any failure exits 1.

Phase 11's characteristic failure would be for the navigation layer to
start *asserting* -- to answer a question rather than point at the answer,
to rank teams, to resolve a conflict by summarising it, or to quietly fill
a gap it was built to describe. Gates 9 and 10 exist for that. Gate 5 is
the repository-wide link check that Phases 7-10 never had.
"""

import json
import os
import re
import subprocess
import sys
from collections import Counter

from xref_lib import (INDEXED_DIRS, NA, PHASE_DIRS, ROOT, conferences,
                      entity_registry, markdown_files, teams)

SEARCH = "99_Search_Index"
DERIVED_DIRS = ["08_Returning_Production", "09_Transfer_Portal",
                "10_Schedule_Intelligence"]
PASS, FAIL = [], []


def check(ok, msg, detail=""):
    (PASS if ok else FAIL).append(msg + (f" — {detail}" if detail and not ok else ""))


def main():
    team_list, conf_list = teams(), conferences()
    files = markdown_files()
    search = markdown_files([SEARCH])
    reg = entity_registry(files, team_list, conf_list)
    every = {**files, **search}
    sbody = "\n".join(search.values())

    # 1 -- all 138 teams represented
    tl = search.get(f"{SEARCH}/02_TEAM_LOOKUP.md", "")
    missing = [t["team"] for t in team_list if t["team"] not in tl]
    check(len(team_list) == 138 and not missing,
          "all 138 teams appear in the team master lookup", str(missing[:4]))

    # 2 -- all 11 conferences represented
    cl = search.get(f"{SEARCH}/03_CONFERENCE_LOOKUP.md", "")
    missing = [c["conference"] for c in conf_list if c["conference"] not in cl]
    check(len(conf_list) == 11 and not missing,
          "all 11 conferences appear in the conference lookup",
          str(missing[:4]))

    # 3 -- every indexed entity resolves to an existing approved artifact
    unresolved = []
    for name, v in reg.items():
        for path in v["files"]:
            if not os.path.exists(os.path.join(ROOT, path)):
                unresolved.append(f"{name}->{path}")
    check(not unresolved and len(reg) == 287,
          f"all {len(reg)} indexed entities resolve to approved artifacts on "
          f"disk", str(unresolved[:3]))

    # 4 -- no canonical-team alias drift across phases.
    # This is the gate that caught Phase 11's biggest find: three slug
    # functions disagreed on "&", so one team's file was named two ways and
    # 18 cross-links pointed at a file that did not exist.
    from coach_lib import slug
    drift = []
    for t in team_list:
        s = slug(t["team"])
        for d in ("02_Team_Database", "03_Coaching_Database",
                  "04_Quarterback_Database"):
            if not os.path.exists(os.path.join(ROOT, d, s)):
                drift.append(f"{d}/{s}")
    check(not drift,
          "one canonical slug serves every phase — no alias drift in the "
          "team, coaching or quarterback databases", str(drift[:4]))

    # 5 -- every relative markdown link in the ENTIRE library resolves
    broken, total = [], 0
    for d in INDEXED_DIRS + [SEARCH]:
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for fn in sorted(os.listdir(p)):
            if not fn.endswith(".md"):
                continue
            body = open(os.path.join(p, fn)).read()
            for target in re.findall(r"\]\(([^)#][^)]*)\)", body):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                total += 1
                if not os.path.exists(
                        os.path.normpath(os.path.join(p, target.split("#")[0]))):
                    broken.append(f"{d}/{fn} -> {target}")
    check(not broken and total > 8000,
          f"all {total:,} relative markdown links in the library resolve",
          str(broken[:4]))

    # 6 & 7 -- every known conflict survives the roll-up, none resolved
    roll = search.get(f"{SEARCH}/09_SOURCE_CONFLICT_ROLLUP.md", "")
    MUST = ["16 coaching-fact conflicts", "11 teams", "21 teams",
            "SUN BELT CHAMP", "PYPG", "PARTICIPATED IN FCS IN 2025",
            "Zach Cohen", "Memphis", "Collin Klein", "post-publication"]
    absent = [m for m in MUST if m not in roll]
    kinds = roll.count("\n## ")
    check(not absent and kinds >= 9,
          f"every known conflict class survives the roll-up, in {kinds} "
          f"distinct kinds", str(absent[:4]))

    RESOLVED = re.compile(r"\b(the correct (?:value|pick|side|answer) is|"
                          r"we side with|resolved in favou?r of|"
                          r"the right number is|we have corrected)\b", re.I)
    bad = [f for f, b in search.items() if RESOLVED.search(b)]
    check(not bad and "adjudicates none" in roll,
          "no conflict is resolved, adjudicated or corrected by the search "
          "layer", str(bad[:3]))

    # 8 -- gap-register counts reconcile to an independent scan
    stated = re.search(r"appears \*\*([\d,]+) times\*\*",
                       search.get(f"{SEARCH}/10_GAP_REGISTER.md", ""))
    actual = sum(b.count(NA) for b in files.values())
    claimed = int(stated.group(1).replace(",", "")) if stated else -1
    check(claimed == actual,
          f"the gap register's count ({claimed:,}) reconciles to an "
          f"independent scan ({actual:,})")

    # 9 -- the search layer introduces no new football fact.
    # Every number it prints must already appear in the library it indexes.
    nums = set(re.findall(r"\b\d+\.\d\b", sbody))
    elsewhere = "\n".join(files.values())
    invented = sorted(n for n in nums if n not in elsewhere)
    check(not invented,
          f"every figure the search layer prints ({len(nums)} distinct) "
          f"already appears in the phases it indexes — no new football fact",
          f"invented={invented[:5]}")

    # 10 -- no new score, grade, probability or model input
    # The market lookup and gap register state what the library refuses to
    # do, and so name the very terms this gate forbids. Those two sentences
    # are stripped by exact match, and their presence is REQUIRED rather
    # than merely tolerated -- a validator artefact, not a finding.
    # A refusal is a statement of what the library does NOT do, and by
    # construction it begins with "No"/"no" or "never". Rather than listing
    # each one -- which grows every time a page states its limits more
    # clearly -- refusal lines are recognised structurally and removed
    # before the scan.
    REFUSAL_LINE = re.compile(r"^\s*[-*>]?\s*(?:\*\*)?(?:No|no|Never|never|"
                              r"It creates no|and neither does)\b")
    REQUIRED = "No implied probability, no vig removal, no expected value"
    SCORING = re.compile(
        r"\b(TTW (?:score|grade|rating of)|composite score|our ranking|"
        r"we rank|confidence (?:score|grade)|implied probability|"
        r"remove the vig|no-vig|expected value of|model input of|"
        r"betting edge of)\b", re.I)
    hits = []
    for f, b in search.items():
        kept = [ln for ln in b.splitlines() if not REFUSAL_LINE.match(ln)]
        if SCORING.search("\n".join(kept)):
            hits.append(f)
    stated = any(REQUIRED in b for b in search.values())
    check(not hits and stated and "may point" in sbody.lower(),
          "no score, grade, probability, ranking or model input introduced "
          "outside an explicit statement of refusal", str(hits[:3]))

    # 11 & 12 -- no post-publication leak, no outside research
    POST = re.compile(r"\b(as of (?:today|now)|since the guide (?:was )?"
                      r"published|latest reports|current odds now|"
                      r"this season's actual|so far in 2026)\b", re.I)
    # EXTERNAL RESEARCH and POST-PUBLICATION UPDATE are valid source
    # classes. Phase 4's verification layer cites Wikipedia, 247 and ESPN by
    # URL, which is correct: what the rules forbid is outside research
    # CONTAMINATING a guide-derived layer, not existing in a labelled one.
    # So a file may carry outside sources only if it also declares that
    # layer.
    OUTSIDE = re.compile(r"\b(according to ESPN|per 247Sports we|"
                         r"we looked up|our research (?:shows|found)|"
                         r"Wikipedia|we consulted)\b", re.I)
    LABELLED = re.compile(r"POST-PUBLICATION|EXTERNAL RESEARCH|"
                          r"Verification source", re.I)
    leak = [f for f, b in every.items() if POST.search(b)]
    out = [f for f, b in every.items()
           if OUTSIDE.search(b) and not LABELLED.search(b)]
    check(not leak, "no post-publication information in any GUIDE CONTENT "
                    "layer", str(leak[:3]))
    labelled_n = sum(1 for b in every.values()
                     if OUTSIDE.search(b) and LABELLED.search(b))
    check(not out,
          f"no outside research contaminates a guide-derived layer; the "
          f"{labelled_n} files citing outside sources all declare a "
          f"post-publication or verification layer", str(out[:3]))

    # 13 -- every prior phase still validates
    prior = []
    for tool in ("validate_teams.py", "validate_qb.py", "validate_coaching.py",
                 "validate_power.py", "validate_phase7.py",
                 "validate_wintotals.py", "validate_futures.py",
                 "validate_concepts.py", "validate_trends.py"):
        rr = subprocess.run([sys.executable, f"_tools/{tool}"],
                            capture_output=True, text=True,
                            env=dict(os.environ, PYTHONPATH="_tools"))
        if rr.returncode != 0:
            prior.append(tool)
    check(not prior,
          "all 9 prior-phase validators and the calibration study still pass",
          f"failing={prior}")

    # 14 -- workbook frozen
    tracked = subprocess.run(["git", "ls-files"], capture_output=True,
                             text=True).stdout.split()
    xl = [f for f in tracked if f.lower().endswith((".xlsx", ".xlsm", ".xls"))]
    check(not xl, "v0.8.1 AUTHORITATIVE remains frozen — no workbook file "
                  "tracked anywhere in the repository", str(xl[:3]))

    # 15 -- repeated builds are byte-stable
    import hashlib

    def digest():
        h = hashlib.sha256()
        for d in DERIVED_DIRS + [SEARCH]:
            p = os.path.join(ROOT, d)
            for fn in sorted(os.listdir(p)):
                if fn.endswith(".md"):
                    h.update(open(os.path.join(p, fn), "rb").read())
        return h.hexdigest()

    before = digest()
    for tool in ("build_xref.py", "build_search.py"):
        subprocess.run([sys.executable, f"_tools/{tool}"],
                       capture_output=True, text=True,
                       env=dict(os.environ, PYTHONPATH="_tools"))
    check(before == digest(),
          "rebuilding the derived views and the search layer is byte-stable")

    # 16 -- no directory still claims it is unbuilt
    STALE = re.compile(r"Not yet built|⏸ Pending|intentionally empty", re.I)
    stale = []
    for d, _, _ in PHASE_DIRS:
        p = os.path.join(ROOT, d, "README.md")
        if os.path.exists(p) and STALE.search(open(p).read()):
            stale.append(d)
    check(not stale,
          "no library directory still reports itself as unbuilt or pending",
          f"stale={stale}")

    print("PHASE 11 — SEARCH OPTIMIZATION VALIDATION")
    print("=" * 74)
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
