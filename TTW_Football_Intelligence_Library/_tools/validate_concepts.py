#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 9 (Betting Concepts) validation
==========================================================================

Twelve gates. Any failure exits 1.

The gate that matters most here is check 3. Phase 9's characteristic
failure mode is not a wrong number -- it is writing a confident,
well-known definition of a concept the guide never covers, which would put
EXTERNAL RESEARCH inside a GUIDE CONTENT layer and would look entirely
plausible on the page. So the two concepts Phase 1 singled out are checked
to carry the sentinel in every substantive field, and the corpus is
scanned for the outside authorities a general betting textbook would cite.
"""

import json
import os
import re
import subprocess
import sys

from concept_lib import (BARELY_COVERED, NA, SITUATIONAL, abbrev_index,
                         load_abbreviations, load_concept_pages, load_entries,
                         load_stat_schema, load_team_stats)

CONCEPTS, STATS, SITU = "11_Betting_Concepts", "14_Statistics_Reference", \
                        "13_Situational_Angles"
PASS, FAIL = [], []


def check(ok, msg, detail=""):
    (PASS if ok else FAIL).append(msg + (f" — {detail}" if detail and not ok else ""))


def read(d):
    return {fn: open(os.path.join(d, fn)).read()
            for fn in sorted(os.listdir(d)) if fn.endswith(".md")}


def main():
    entries = load_entries()
    pages = load_concept_pages()
    abbr = load_abbreviations()
    stats = load_team_stats()
    off, deff = load_stat_schema()
    ctext, stext, qtext = read(CONCEPTS), read(STATS), read(SITU)
    every = {**ctext, **stext, **qtext}

    FIELDS = ("guide_definition", "guide_usage", "working_definition",
              "why_it_matters", "how_used", "key_locations")

    # 1 -- exactly the indexed concepts, none invented, none dropped
    extra, missing = set(entries) - set(pages), set(pages) - set(entries)
    check(len(entries) == 29 and not extra and not missing,
          f"{len(entries)} entries, exactly the {len(pages)} concepts in the "
          f"Phase 1 index — none invented, none dropped",
          f"extra={sorted(extra)} missing={sorted(missing)}")

    # 2 -- every entry complete, every concept has a rendered page
    thin = [f"{n}.{k}" for n in entries for k in FIELDS
            if not (entries[n].get(k) or "").strip()]
    nopage = [n for n in entries
              if re.sub(r"[^a-z0-9]+", "_", n.lower()).strip("_") + ".md"
              not in ctext]
    check(not thin and not nopage,
          f"all {len(entries)} entries carry every field and render a page",
          f"thin={thin[:3]} nopage={nopage[:3]}")

    # 3 -- the barely-covered concepts are NOT filled from outside knowledge.
    # This is the gate this phase exists to pass.
    leaked = []
    for n in BARELY_COVERED:
        for k in ("guide_definition", "guide_usage", "working_definition",
                  "why_it_matters", "how_used"):
            if entries[n][k] != NA:
                leaked.append(f"{n}.{k}")
    AUTHORITIES = re.compile(
        r"\b(Pinnacle|Kelly criterion|sharp book|steam move|closing line "
        r"value is|CLV is|according to (?:most|many) bettors|industry "
        r"standard|it is widely (?:known|accepted))\b", re.I)
    cited = [fn for fn, b in every.items() if AUTHORITIES.search(b)]
    check(not leaked and not cited,
          f"the {len(BARELY_COVERED)} barely-covered concepts carry the "
          f"sentinel throughout; no outside betting authority cited anywhere",
          f"leaked={leaked} cited={cited[:3]}")

    # 4 -- gaps reported as gaps, with the count stated
    undefined = [n for n in entries if entries[n]["guide_definition"] == NA]
    gaps = ctext.get("00_GAPS.md", "")
    check(len(undefined) == 21 and str(len(undefined)) in gaps
          and all(n in gaps for n in BARELY_COVERED),
          f"{len(undefined)} of {len(entries)} concepts are never defined by "
          f"the guide, and 00_GAPS.md reports that rather than filling it",
          f"undefined={len(undefined)} in_gaps={str(len(undefined)) in gaps}")

    # 5 -- source classes labelled and never blended in one claim
    # 00_GLOSSARY.md reproduces the guide's p. 2 list and nothing else, so it
    # is wholly GUIDE CONTENT and correctly does NOT claim a derived section.
    PURE_GUIDE = {"00_GLOSSARY.md"}
    unlabelled = [fn for fn in ctext if fn not in PURE_GUIDE
                  and ("GUIDE CONTENT" not in ctext[fn]
                       or "TTW DERIVED" not in ctext[fn])]
    mislabelled = [fn for fn in PURE_GUIDE
                   if "TTW DERIVED" in ctext.get(fn, "")]
    check(not unlabelled and not mislabelled,
          "every concept page names both source classes and separates them by "
          "heading; the p. 2 glossary stays wholly GUIDE CONTENT",
          f"unlabelled={unlabelled[:3]} mislabelled={mislabelled}")

    # 6 -- page citations resolve to pages the concept map actually records
    # The Phase 1 map is a keyword scan. It records where a concept's NAME
    # appears, which is not the same as where the guide reasons about it: the
    # win-total feature on pp. 22-27 argues schedule difficulty on nearly
    # every page without using the phrase. So the gate asserts what is
    # actually true -- every cited page exists in the guide, and each entry is
    # anchored to at least one page the map does record -- rather than
    # treating a keyword scan as the authority on where a concept lives.
    outside_guide, unanchored = [], []
    for n, rec in entries.items():
        cited_pages = {int(x) for x in re.findall(r"\bp{1,2}\. ?(\d{1,3})",
                                                  rec["key_locations"])}
        outside_guide += [f"{n}:p{p}" for p in cited_pages
                          if not 1 <= p <= 345]
        if cited_pages and not (cited_pages & set(pages[n])):
            unanchored.append(n)
    check(not outside_guide and not unanchored,
          "every page cited in a concept's key locations exists in the guide, "
          "and every entry is anchored to at least one page the Phase 1 map "
          "records for it",
          f"outside={outside_guide[:4]} unanchored={unanchored[:4]}")

    # 7 -- the glossary reproduces all 45, typo intact
    gl = ctext.get("00_GLOSSARY.md", "")
    printed = [a for a in abbr if f"`{a['abbr']}`" in gl]
    typo = "Passing Yards per Page" in gl and "not** \nsilently" not in gl
    check(len(printed) == len(abbr) == 45 and typo
          and "silently corrected" in gl,
          f"all {len(abbr)} p. 2 abbreviations reproduced as printed, "
          f"including the guide's `PYPG – Passing Yards per Page` typo",
          f"printed={len(printed)} typo_kept={typo}")

    # 8 -- statistics reconcile against Phase 3
    # Sacramento State and North Dakota State carry the table headings with
    # PARTICIPATED IN FCS IN 2025 printed in place of both sides. That is an
    # explicit, reasoned absence in the source, not an extraction gap.
    fcs = sorted(t for t, v in stats.items()
                 if not v["stats"].get("offense") and not v["stats"].get("defense"))
    o_bad = [t for t, v in stats.items() if t not in fcs
             and [r["category"] for r in v["stats"].get("offense", [])] != off]
    d_bad = [t for t, v in stats.items() if t not in fcs
             and [r["category"] for r in v["stats"].get("defense", [])] != deff]
    total = sum(len(v["stats"].get(s, [])) for v in stats.values()
                for s in ("offense", "defense"))
    documented = "PARTICIPATED IN FCS IN 2025" in stext.get("README.md", "")
    check(len(stats) == 138 and not o_bad and not d_bad
          and fcs == ["North Dakota State Bison", "Sacramento State Hornets"]
          and total == 136 * 27 and documented,
          f"{len(stats) - len(fcs)} teams × {len(off)} offensive + "
          f"{len(deff)} defensive = {total:,} figures with an identical "
          f"schema; the 2 FCS promotions carry the guide's printed notice "
          f"instead of values",
          f"off_bad={o_bad[:2]} def_bad={d_bad[:2]} fcs={fcs} "
          f"total={total} documented={documented}")

    # 9 -- the table asymmetry is documented, not normalised
    sr = stext.get("README.md", "")
    documented = "defensive tempo cannot be read" in sr.lower()
    real = ("SACKS" in deff and "PLAYS PER GAME" not in deff
            and "PLAYS PER GAME" in off and "TIME OF POSSESSION" not in deff)
    withdrawn = "blocked on coordinate" not in sr.lower()
    check(documented and real and withdrawn,
          "the offensive/defensive asymmetry is real, documented, and the "
          "stale 'blocked on coordinate-based extraction' status is withdrawn",
          f"documented={documented} schema_matches={real} "
          f"withdrawn={withdrawn}")

    # 10 -- situational split stated so Phase 10 inherits a clear line
    sq = qtext.get("README.md", "")
    check("Phase 10" in sq and "conceptual" in sq.lower()
          and all(n in sq for n in SITUATIONAL),
          "13_Situational_Angles states the Phase 9 / Phase 10 boundary and "
          "routes all 5 situational concepts",
          f"phase10={'Phase 10' in sq}")

    # 11 -- no post-publication material, no scores or model inputs
    outside = re.compile(r"\b(as of (?:today|now)|since the guide (?:was )?"
                         r"published|latest reports|current odds now|"
                         r"has since|this season's actual)\b", re.I)
    scored = re.compile(r"\b(implied probability|remove the vig|no-vig|"
                        r"expected value of|confidence (?:score|grade) of|"
                        r"weight of \d|model input of)\b", re.I)
    # The Futures entry states what the guide never does, and so names the
    # very arithmetic this gate forbids. Stripped by exact match, and its
    # presence is required rather than merely tolerated.
    REFUSAL = ("No implied probability, no vig removal, and no expected-value "
               "figure appears anywhere in it, and none is supplied by this "
               "library.")
    hits = [fn for fn, b in every.items()
            if outside.search(b.replace(REFUSAL, ""))
            or scored.search(b.replace(REFUSAL, ""))]
    check(not hits and REFUSAL in ctext.get("futures.md", ""),
          "no post-publication language, and no betting score, weight or "
          "implied probability introduced — with the refusal stated "
          "explicitly in the Futures entry", str(hits[:3]))

    # 12 -- earlier phases still validate, workbook untouched
    prior = []
    for tool in ("validate_qb.py", "validate_coaching.py", "validate_power.py",
                 "validate_phase7.py", "validate_wintotals.py",
                 "validate_futures.py"):
        rr = subprocess.run([sys.executable, f"_tools/{tool}"],
                            capture_output=True, text=True,
                            env=dict(os.environ, PYTHONPATH="_tools"))
        if rr.returncode != 0:
            prior.append(tool)
    tracked = subprocess.run(["git", "ls-files"], capture_output=True,
                             text=True).stdout.split()
    xl = [fn for fn in tracked if fn.lower().endswith((".xlsx", ".xlsm", ".xls"))]
    check(not prior and not xl,
          "Phases 4–8 and the calibration study still validate; no workbook "
          "file tracked", f"failing={prior} xlsx={xl}")

    print("PHASE 9 — BETTING CONCEPTS VALIDATION")
    print("=" * 70)
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
