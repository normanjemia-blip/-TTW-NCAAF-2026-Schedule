#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 6 validation
=======================================================

Ten gates. Any failure exits 1.

The gate that matters most is check 4. Phase 6 is the first phase allowed
to open the frozen v0.8.1 workbook, and the only guarantee worth anything
is that the file is byte-identical to the blob recorded in its provenance.
That is checked against the git object, not against a hash this phase
wrote down itself.

Check 6 is the second: it independently re-derives the workbook's
preseason prior from the stored inputs and compares it against the
rendered comparison table, so a renderer that quietly changed the blend
would be caught rather than believed.
"""

import csv
import hashlib
import json
import os
import re
import statistics as stats
import subprocess
import sys

from coach_lib import load_details, slug
from qb_lib import ABBREV_TO_VSIN

OUT = "05_Power_Ratings"
FILES = ["README.md", "00_MAKINEN_METHODOLOGY.md", "00_MAKINEN_RATINGS.md",
         "00_LINE_MODEL_VERIFICATION.md", "00_SCALE_RECONCILIATION.md",
         "00_TTW_VS_MAKINEN.md", "00_DISAGREEMENT_INDEX.md",
         "00_HOME_FIELD_COMPARISON.md", "00_VSIN_IMPORT_CANDIDATE.md",
         "00_WORKBOOK_PROVENANCE.md", "00_SOURCE_CONFLICTS.md"]

PASS, FAIL = [], []


def check(ok, msg, detail=""):
    (PASS if ok else FAIL).append(msg + (f" — {detail}" if detail and not ok else ""))


def main():
    p47 = {r["team"]: r for r in json.load(open("_source/data/makinen_ratings_p47.json"))}
    details = load_details()
    wb = json.load(open("_source/verified/workbook_preseason_v081.json"))
    lm = json.load(open("_source/data/line_model_check.json"))
    conflicts = json.load(open("_source/data/power_rating_conflicts.json"))
    text = {f: open(os.path.join(OUT, f)).read() for f in FILES
            if os.path.exists(os.path.join(OUT, f))}

    # 1 -- both printings of every rating extracted and reconciled
    check(len(p47) == 138 and all(r["agree"] for r in p47.values())
          and not conflicts,
          f"all 138 ratings reconciled across both printings "
          f"(p. 47 and team pages), {len(conflicts)} conflicts",
          f"{sum(1 for r in p47.values() if not r['agree'])} disagree")

    # 2 -- ratings rendered are the ratings extracted
    body = text.get("00_MAKINEN_RATINGS.md", "")
    bad = [t for t, r in p47.items()
           if f"| **{r['p47_rating']:g}** | [{t}]" not in body]
    check(len(bad) == 0, "every printed rating rendered verbatim", str(bad[:5]))

    # 3 -- the canonical join is total and is the Phase 4 bijection
    joined = {ABBREV_TO_VSIN.get(r["abbrev"]) for r in wb["rows"]}
    check(None not in joined and len(joined) == 138
          and joined == set(p47) == set(details),
          "workbook joins to all 138 canonical teams via the Phase 4 map",
          f"{len(joined)} joined")

    # 4 -- the frozen workbook is byte-identical to its recorded blob
    try:
        blob = subprocess.run(["git", "cat-file", "-p", wb["git_blob"]],
                              capture_output=True, check=True).stdout
        live = hashlib.sha256(blob).hexdigest()
    except Exception as e:                       # pragma: no cover
        live = f"unavailable: {e}"
    check(live == wb["sha256"],
          f"frozen workbook byte-identical to git blob {wb['git_blob'][:12]}… "
          f"(sha256 {wb['sha256'][:16]}…)",
          f"git says {live}")

    # 5 -- nothing in the tracked tree is a copy of the workbook
    stray = subprocess.run(["git", "ls-files"], capture_output=True,
                           text=True).stdout.split()
    xl = [f for f in stray if f.lower().endswith((".xlsx", ".xlsm", ".xls"))]
    check(not xl, "no workbook copy committed to the library tree", str(xl))

    # 6 -- the derived prior is reproducible and matches what was rendered
    keys = {"sp_raw": "SP+ 2026 preseason", "fpi_raw": "FPI 2026 preseason",
            "ttw25_raw": "TTW independent 2025 regressed prior",
            "tr_raw": "TeamRankings predictive", "vsin_raw": "VSiN (user-supplied)"}
    rows = {ABBREV_TO_VSIN[r["abbrev"]]: r for r in wb["rows"]}
    present = [k for k in keys
               if all(isinstance(r[k], (int, float)) for r in rows.values())]
    means = {k: stats.fmean(r[k] for r in rows.values()) for k in present}
    wsum = sum(wb["settings"][keys[k]] for k in present)
    prior = {t: sum(wb["settings"][keys[k]] * (r[k] - means[k])
                    for k in present) / wsum for t, r in rows.items()}
    cmp_body = text.get("00_TTW_VS_MAKINEN.md", "")
    mismatch = [t for t in p47
                if f"| {prior[t]:+.2f} |" not in cmp_body.split(f"[{t}]")[-1][:120]]
    check(len(present) == 3 and not mismatch,
          f"derived prior independently reproducible on {len(present)} live "
          f"sources; all 138 rows match the rendered table",
          f"{len(mismatch)} mismatched")

    # 7 -- the scale claim is backed by the line model, not asserted
    ok_rate = lm["exact"] / lm["checked"] if lm["checked"] else 0
    lmv = text.get("00_LINE_MODEL_VERIFICATION.md", "")
    check(lm["checked"] >= 1500 and ok_rate >= 0.99
          and f"{lm['exact']}" in lmv and f"{lm['checked']}" in lmv,
          f"scale claim evidenced: {lm['exact']}/{lm['checked']} printed lines "
          f"reconstructed ({ok_rate*100:.2f}%)",
          f"checked {lm['checked']} rate {ok_rate:.4f}")

    # 8 -- no rescaling was applied anywhere; translation only
    rescale = re.compile(r"\b(z-score|standard[- ]deviation rescal|rescaled to|"
                         r"normalised to unit variance|scaled by sd)\b", re.I)
    bad = [f for f, b in text.items()
           if rescale.search(b) and "would have been" not in b[
               max(0, rescale.search(b).start() - 120):rescale.search(b).end() + 120]]
    mean_m = stats.fmean(r["p47_rating"] for r in p47.values())
    centred_ok = all(
        f"| {r['p47_rating'] - mean_m:+.2f} |" in cmp_body.split(f"[{t}]")[-1][:120]
        for t, r in p47.items())
    check(not bad and centred_ok,
          "comparison uses mean-centering only — no rescaling applied",
          str(bad[:3]) + (" centred values mismatch" if not centred_ok else ""))

    # 9 -- source classes labelled and never merged
    unlabelled = [f for f, b in text.items()
                  if f != "README.md"
                  and "Source class:" not in b
                  and "workbook is frozen" not in b]
    derived_files = ("00_LINE_MODEL_VERIFICATION.md", "00_SCALE_RECONCILIATION.md",
                     "00_TTW_VS_MAKINEN.md", "00_DISAGREEMENT_INDEX.md",
                     "00_HOME_FIELD_COMPARISON.md")
    mislabelled = [f for f in derived_files
                   if "TTW DERIVED" not in text.get(f, "")]
    guide_files = ("00_MAKINEN_METHODOLOGY.md", "00_MAKINEN_RATINGS.md",
                   "00_SOURCE_CONFLICTS.md")
    mis2 = [f for f in guide_files if "GUIDE CONTENT" not in text.get(f, "")]
    check(not unlabelled and not mislabelled and not mis2,
          "every file declares its source class; guide and derived never merged",
          str(unlabelled + mislabelled + mis2))

    # 10 -- the import candidate is prepared, complete, and not applied
    imp = list(csv.DictReader(open("_source/data/vsin_preseason_import.csv")))
    abbrs = {r["abbrev"] for r in imp}
    raw_ok = all(abs(float(r["vsin_raw"]) - p47[r["team_vsin"]]["p47_rating"]) < 1e-9
                 for r in imp)
    vc = text.get("00_VSIN_IMPORT_CANDIDATE.md", "")
    says_unapplied = ("not applied" in vc.lower()
                      and "has **not** been opened for writing" in vc)
    workbook_still_blank = wb["coverage"]["vsin_raw"] == 0
    check(len(imp) == 138 and abbrs == set(ABBREV_TO_VSIN) and raw_ok
          and says_unapplied and workbook_still_blank,
          "VSiN import candidate complete (138 rows), verbatim, and unapplied",
          f"rows {len(imp)} raw_ok {raw_ok} unapplied {says_unapplied} "
          f"workbook vsin col {wb['coverage']['vsin_raw']}")

    print("PHASE 6 VALIDATION")
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
