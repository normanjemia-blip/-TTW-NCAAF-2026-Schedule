#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 7 scorer (executes the protocol)
===========================================================================

Runs the comparison registered in 05_Power_Ratings/01_CALIBRATION_PROTOCOL.md
once 2026 results exist. It is written now, before any result exists, so
that the scoring rule cannot be shaped by the answer.

It refuses to run on an empty or partial season rather than reporting a
number that would invite over-reading. It reports uncertainty on every
comparison. It never writes to the workbook.

Usage:  python3 _tools/score_calibration.py <workbook.xlsx> [--min-games 200]
"""

import json
import math
import statistics as stats
import sys

from build_protocol import read_schedule
from qb_lib import ABBREV_TO_VSIN

HFA_DEFAULT_KEY = "Default home-field advantage (pts)"


def ci95(vals):
    """Mean with a 95% interval. Reported on every comparison, always."""
    n = len(vals)
    if n < 2:
        return (float("nan"), float("nan"), float("nan"))
    m = stats.fmean(vals)
    se = stats.stdev(vals) / math.sqrt(n)
    return (m, m - 1.96 * se, m + 1.96 * se)


def main():
    path = sys.argv[1]
    min_games = 200
    if "--min-games" in sys.argv:
        min_games = int(sys.argv[sys.argv.index("--min-games") + 1])

    diag = json.load(open("_source/calibration/vsin_diagnostics.json"))
    wbp = json.load(open("_source/verified/workbook_preseason_v081.json"))
    base = {r["team"]: r["baseline"] for r in diag["per_team"]}
    withv = {r["team"]: r["vsin_included"] for r in diag["per_team"]}
    hfa = wbp["settings"][HFA_DEFAULT_KEY]

    games, alias = read_schedule(path)

    def resolve(name):
        ab = alias.get(str(name).strip().lower())
        return ABBREV_TO_VSIN.get(ab) if ab else None

    scored = []
    for g in games:
        if not g["completed"] or g["home_pts"] is None or g["away_pts"] is None:
            continue
        h, a = resolve(g["home"]), resolve(g["away"])
        if h is None or a is None:
            continue                                   # FCS opponent
        edge = 0 if g["neutral"] else hfa
        actual = g["home_pts"] - g["away_pts"]
        pb = base[h] - base[a] + edge
        pv = withv[h] - withv[a] + edge
        scored.append({"week": g["week"], "home": h, "away": a,
                       "actual": actual, "pred_base": pb, "pred_vsin": pv,
                       "err_base": pb - actual, "err_vsin": pv - actual})

    if len(scored) < min_games:
        print(f"REFUSING TO SCORE: {len(scored)} completed FBS-vs-FBS games "
              f"available, protocol requires at least {min_games}.")
        print("A partial season is not scored, because a number reported here "
              "would be read as a result. Re-run at season end.")
        sys.exit(2)

    def block(rows, label):
        eb = [abs(r["err_base"]) for r in rows]
        ev = [abs(r["err_vsin"]) for r in rows]
        paired = [b - v for b, v in zip(eb, ev)]
        m, lo, hi = ci95(paired)
        return {"segment": label, "n": len(rows),
                "mae_baseline": stats.fmean(eb), "mae_vsin": stats.fmean(ev),
                "rmse_baseline": math.sqrt(stats.fmean(x * x for x in eb)),
                "rmse_vsin": math.sqrt(stats.fmean(x * x for x in ev)),
                "paired_mean_gain": m, "ci95_low": lo, "ci95_high": hi,
                "significant": not (lo <= 0 <= hi)}

    out = [block(scored, "full season")]
    for lo_w, hi_w, name in ((0, 4, "weeks 0-4"), (5, 9, "weeks 5-9"),
                             (10, 20, "weeks 10+")):
        seg = [r for r in scored
               if isinstance(r["week"], int) and lo_w <= r["week"] <= hi_w]
        if len(seg) >= 30:
            out.append(block(seg, name))

    with open("_source/calibration/scored_results.json", "w") as fh:
        json.dump({"games_scored": len(scored), "segments": out}, fh, indent=1)

    print(f"games scored: {len(scored)}")
    print(f"{'segment':<14} {'n':>5} {'MAE base':>9} {'MAE vsin':>9} "
          f"{'gain':>8} {'95% CI':>20}  verdict")
    for b in out:
        verdict = ("improvement" if b["significant"] and b["paired_mean_gain"] > 0
                   else "degradation" if b["significant"]
                   else "indistinguishable")
        print(f"{b['segment']:<14} {b['n']:>5} {b['mae_baseline']:>9.3f} "
              f"{b['mae_vsin']:>9.3f} {b['paired_mean_gain']:>+8.4f} "
              f"[{b['ci95_low']:+.4f}, {b['ci95_high']:+.4f}]  {verdict}")
    print()
    print("Reminder from the protocol: a statistically detectable effect here "
          "is still practically negligible. Report both.")


if __name__ == "__main__":
    main()
