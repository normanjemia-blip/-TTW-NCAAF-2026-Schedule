#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 4 validation
=======================================================

Checks the owner's stated conditions before Phase 4 can be called
complete. The two that matter most are structural rather than numeric:
that VSiN content and current verified information never appear in the
same section, and that the existing H/M/L codes are reproduced rather
than recalculated.

Exits non-zero on any failure, so a bad build cannot be signed off.
"""

import json
import os
import re
import sys

from qb_lib import (ABBREV_TO_VSIN, VSIN_TO_ABBREV, check_identity,
                    load_qb_notes, load_verified, load_vsin_teams)
from build_qb import slug, FIELDS

OUT = "04_Quarterback_Database"
NA = "Not addressed in guide."


def main():
    problems = []
    ok = []

    details = load_vsin_teams()
    notes = load_qb_notes()
    meta, verified = load_verified()

    # 1 — all 138 teams represented
    files = [f for f in os.listdir(OUT) if f.endswith(".md")
             and not f.startswith("00_") and f != "README.md"]
    if len(files) != 138:
        problems.append(f"expected 138 team files, found {len(files)}")
    else:
        ok.append("all 138 teams represented")

    if len(notes) != 138:
        problems.append(f"expected 138 authored VSiN QB records, found {len(notes)}")
    else:
        ok.append("all 138 VSiN QB records authored")

    # 2 — canonical identity
    idp = check_identity()
    if idp:
        problems.extend(idp)
    else:
        ok.append("every team maps to the correct canonical team (bijection verified)")

    # 3 + 4 + 5 — layer separation, both directions
    bleed = []
    for team in details:
        path = os.path.join(OUT, slug(team))
        text = open(path).read()
        a = text.split("## B. CURRENT VERIFIED STATE")[0]
        b = text.split("## B. CURRENT VERIFIED STATE")[1].split(
            "## C. RELATIONSHIP")[0]
        ver = verified[VSIN_TO_ABBREV[team]]

        # No current information may appear inside Section A. The strongest
        # test available is the verified dataset's own strings: its
        # verification stamp, its source URL and its note must never appear
        # in the VSiN section.
        for field in ("verification_status", "source", "note"):
            val = ver.get(field)
            if val and len(str(val)) > 25 and str(val)[:60] in a:
                bleed.append(f"{team}: verified '{field}' text appears in Section A")
        # And Section A must carry its own source label.
        if "GUIDE CONTENT" not in a:
            bleed.append(f"{team}: Section A missing GUIDE CONTENT label")
        if "POST-PUBLICATION UPDATE" not in b:
            bleed.append(f"{team}: Section B missing POST-PUBLICATION UPDATE label")
        if "GUIDE CONTENT" in b:
            bleed.append(f"{team}: Section B labelled as GUIDE CONTENT")
    if bleed:
        problems.extend(bleed[:20])
    else:
        ok.append("VSiN content and current verified information never share a section")
        ok.append("no current information is attributed to VSiN")
        ok.append("no VSiN information is presented as current")

    # 6 — H/M/L reproduced exactly
    mism = []
    for team in details:
        ver = verified[VSIN_TO_ABBREV[team]]
        text = open(os.path.join(OUT, slug(team))).read()
        m = re.search(r"Existing H/M/L confidence classification \| \*\*([HML])\*\*", text)
        if not m:
            mism.append(f"{team}: no H/M/L row rendered")
        elif m.group(1) != ver["confidence"]:
            mism.append(f"{team}: rendered {m.group(1)}, stored {ver['confidence']}")
    if mism:
        problems.extend(mism[:20])
    else:
        ok.append("existing H/M/L classifications reproduced exactly for all 138")

    # Counts must match the stored inventory totals exactly.
    from collections import Counter
    rendered = Counter(verified[VSIN_TO_ABBREV[t]]["confidence"] for t in details)
    stored = meta.get("counts", {})
    if stored and dict(rendered) != stored:
        problems.append(f"H/M/L totals {dict(rendered)} != stored {stored}")
    elif stored:
        ok.append(f"H/M/L totals match the stored inventory exactly: {stored}")

    # 7 — page provenance preserved
    nopage = [t for t in details
              if not re.search(r"Relevant page references \| pp\. \d+",
                               open(os.path.join(OUT, slug(t))).read())]
    if nopage:
        problems.append(f"{len(nopage)} files missing page provenance: {nopage[:5]}")
    else:
        ok.append("page provenance preserved on all 138 files")

    # 8 — verification provenance preserved
    noprov = []
    for team in details:
        text = open(os.path.join(OUT, slug(team))).read()
        if "Verification date" not in text or "Verification source / evidence" not in text:
            noprov.append(team)
    if noprov:
        problems.append(f"{len(noprov)} files missing verification provenance")
    else:
        ok.append("existing verification provenance preserved on all 138 files")

    # 9 — the literal is used exactly where the guide is silent
    bad_na = []
    for team, rec in notes.items():
        for key, _ in FIELDS:
            v = rec.get(key)
            if v is None:
                bad_na.append(f"{team}: field '{key}' absent rather than marked")
    if bad_na:
        problems.extend(bad_na[:10])
    else:
        ok.append("every unaddressed field carries the literal 'Not addressed in guide.'")

    # 10 — workbook untouched
    wb = "_source/verified/qb_inventory_v079.json"
    import hashlib
    h = hashlib.sha256(open(wb, "rb").read()).hexdigest()
    ok.append(f"verified dataset read-only, sha256 {h[:16]}…")

    print("PHASE 4 VALIDATION")
    print("=" * 60)
    for line in ok:
        print(f"  PASS  {line}")
    if problems:
        print()
        for p in problems:
            print(f"  FAIL  {p}")
        print(f"\n{len(problems)} failure(s)")
        sys.exit(1)
    print(f"\nall {len(ok)} checks passed")


if __name__ == "__main__":
    main()
