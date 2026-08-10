#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 7 (VSiN preseason calibration)
=========================================================================

What this phase was asked to decide: whether adding Makinen/VSiN to the
workbook's preseason consensus improves out-of-sample football prediction
enough to justify including it.

What this phase can actually decide, given the data that exists: nothing
about predictive value. Zero seasons in this project pair a VSiN preseason
rating with played games. The 2026 season has not begun. That is stated in
the report and is not worked around with a proxy.

So this tool does the two honest things that remain:

  1. **Diagnostics that need no results.** How far the preseason prior
     would move if VSiN were included at its reserved weight; how much
     genuinely new information VSiN carries once the three live sources
     are accounted for; how sensitive all of that is to the weight chosen.
     None of this is evidence of predictive value and every output says so.

  2. **A pre-registered scoring protocol.** The comparison is specified in
     code now, before any 2026 result exists, so that when results arrive
     the test cannot be tuned to its own answer.

Nothing is written to the workbook.

Usage:  python3 _tools/build_calibration.py
"""

import json
import os
import statistics as stats

from coach_lib import slug
from qb_lib import ABBREV_TO_VSIN

OUT = "05_Power_Ratings"
HEADER = ("<!-- GENERATED FILE — do not hand-edit.\n"
          "     Rebuild:  python3 _tools/build_calibration.py\n"
          "     Source:   2026 VSiN College Football Betting Guide;\n"
          "               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->\n")

DERIVED = ("> **Source class: TTW DERIVED.** Every number below is this "
           "library's arithmetic over guide figures and workbook inputs. It "
           "is not a workbook output and not VSiN's claim.")
FROZEN = ("> **v0.8.1 AUTHORITATIVE remains frozen.** This phase reads it and "
          "writes nothing to it: no weights, no SETTINGS, no formulas, no "
          "VSiN column, no new version.")
NOTPRED = ("> **This is not predictive validation.** Nothing on this page "
           "measures whether VSiN improves prediction. It measures how the "
           "blend would move and how much independent information VSiN "
           "carries. Those are decision-relevant, and they are not evidence "
           "of forecasting skill.")

SRC = {"sp_raw": "SP+ 2026 preseason",
       "fpi_raw": "FPI 2026 preseason",
       "tr_raw": "TeamRankings predictive",
       "vsin_raw": "VSiN (user-supplied)"}
LABEL = {"sp_raw": "SP+", "fpi_raw": "FPI", "tr_raw": "TeamRankings",
         "vsin_raw": "VSiN"}


def write(name, lines):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(HEADER + "\n" + "\n".join(lines) + "\n")


def tlink(team):
    return f"[{team}](../02_Team_Database/{slug(team)})"


def ols(y, xs):
    """Least squares with intercept, by normal equations. No numpy here.

    Returns (coefficients, r_squared, residuals). Written out rather than
    imported so the arithmetic is auditable alongside everything else.
    """
    n = len(y)
    cols = [[1.0] * n] + [list(x) for x in xs]
    k = len(cols)
    a = [[sum(cols[i][t] * cols[j][t] for t in range(n)) for j in range(k)]
         + [sum(cols[i][t] * y[t] for t in range(n))] for i in range(k)]
    for i in range(k):                                   # Gaussian elimination
        p = max(range(i, k), key=lambda r: abs(a[r][i]))
        a[i], a[p] = a[p], a[i]
        piv = a[i][i]
        a[i] = [v / piv for v in a[i]]
        for r in range(k):
            if r != i and a[r][i]:
                f = a[r][i]
                a[r] = [v - f * w for v, w in zip(a[r], a[i])]
    beta = [row[-1] for row in a]
    fit = [sum(beta[j] * cols[j][t] for j in range(k)) for t in range(n)]
    resid = [y[t] - fit[t] for t in range(n)]
    ybar = stats.fmean(y)
    ss_tot = sum((v - ybar) ** 2 for v in y)
    ss_res = sum(v * v for v in resid)
    return beta, 1 - ss_res / ss_tot, resid


def blend(norm, weights, keys):
    wsum = sum(weights[SRC[k]] for k in keys)
    return {t: sum(weights[SRC[k]] * norm[k][t] for k in keys) / wsum
            for t in norm[keys[0]]}


def main():
    wb = json.load(open("_source/verified/workbook_preseason_v081.json"))
    p47 = {r["team"]: r["p47_rating"]
           for r in json.load(open("_source/data/makinen_ratings_p47.json"))}
    rows = {ABBREV_TO_VSIN[r["abbrev"]]: r for r in wb["rows"]}
    teams = sorted(rows)
    conf = {t: rows[t]["conference"] for t in teams}
    W = wb["settings"]

    # Normalised sources. The three live ones come from the workbook's stored
    # inputs; VSiN comes from p. 47, mean-centred — the same convention the
    # sheet uses, and the transformation Phase 6 established as the correct
    # one for this scale.
    raw = {k: {t: rows[t][k] for t in teams} for k in ("sp_raw", "fpi_raw", "tr_raw")}
    raw["vsin_raw"] = {t: p47[t] for t in teams}
    norm = {k: {t: v - stats.fmean(raw[k].values()) for t, v in raw[k].items()}
            for k in raw}

    live = ["sp_raw", "fpi_raw", "tr_raw"]
    base = blend(norm, W, live)
    withv = blend(norm, W, live + ["vsin_raw"])
    delta = {t: withv[t] - base[t] for t in teams}

    def ranks(d):
        o = sorted(teams, key=lambda t: -d[t])
        return {t: i + 1 for i, t in enumerate(o)}
    rb, rw = ranks(base), ranks(withv)
    rank_move = {t: rb[t] - rw[t] for t in teams}

    # How much of VSiN is already in the three live sources?
    beta, r2, resid = ols([norm["vsin_raw"][t] for t in teams],
                          [[norm[k][t] for t in teams] for k in live])
    resid_sd = stats.pstdev(resid)

    pair = {}
    for i, a in enumerate(list(norm)):
        for b in list(norm)[i + 1:]:
            pair[(a, b)] = stats.correlation([norm[a][t] for t in teams],
                                             [norm[b][t] for t in teams])

    # Weight sensitivity. Diagnostic only: these are not candidate
    # configurations and none is being proposed for production.
    sweep = []
    for w in (0.05, 0.10, 0.15, 0.20, 0.30):
        Wx = dict(W, **{SRC["vsin_raw"]: w})
        b = blend(norm, Wx, live + ["vsin_raw"])
        d = {t: b[t] - base[t] for t in teams}
        r = ranks(b)
        sweep.append({"w": w,
                      "eff": w / (sum(W[SRC[k]] for k in live) + w),
                      "max_abs": max(abs(v) for v in d.values()),
                      "mean_abs": stats.fmean(abs(v) for v in d.values()),
                      "sd": stats.pstdev(b.values()),
                      "max_rank": max(abs(rb[t] - r[t]) for t in teams),
                      "n_over_1pt": sum(1 for v in d.values() if abs(v) >= 1.0)})

    out = {
        "generated": "phase 7 — VSiN preseason calibration (diagnostics only)",
        "predictive_validation_possible": False,
        "reason": ("no season in this project pairs a VSiN preseason rating "
                   "with played games; the 2026 season has not begun"),
        "baseline_effective_weights": {
            LABEL[k]: W[SRC[k]] / sum(W[SRC[x]] for x in live) for k in live},
        "vsin_included_effective_weights": {
            LABEL[k]: W[SRC[k]] / sum(W[SRC[x]] for x in live + ["vsin_raw"])
            for k in live + ["vsin_raw"]},
        "delta": {"mean_abs": stats.fmean(abs(v) for v in delta.values()),
                  "median_abs": stats.median(sorted(abs(v) for v in delta.values())),
                  "max_abs": max(abs(v) for v in delta.values()),
                  "n_over_0_5": sum(1 for v in delta.values() if abs(v) >= 0.5),
                  "n_over_1_0": sum(1 for v in delta.values() if abs(v) >= 1.0)},
        "rank": {"unchanged": sum(1 for t in teams if rank_move[t] == 0),
                 "max_move": max(abs(v) for v in rank_move.values())},
        "vsin_information": {"r_squared_on_live_sources": r2,
                             "residual_sd_pts": resid_sd,
                             "coefficients": dict(zip(["intercept"] + [LABEL[k] for k in live], beta))},
        "pairwise_correlation": {f"{LABEL[a]}~{LABEL[b]}": v for (a, b), v in pair.items()},
        "weight_sweep": sweep,
        "sd": {"baseline": stats.pstdev(base.values()),
               "vsin_included": stats.pstdev(withv.values())},
        "per_team": [{"team": t, "conference": conf[t], "baseline": base[t],
                      "vsin_included": withv[t], "delta": delta[t],
                      "rank_baseline": rb[t], "rank_vsin": rw[t],
                      "vsin_residual": resid[teams.index(t)]} for t in teams],
    }
    os.makedirs("_source/calibration", exist_ok=True)
    with open("_source/calibration/vsin_diagnostics.json", "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)

    # ---------------- rendered diagnostics ----------------
    L = ["# VSiN Inclusion — Diagnostics Without Results", "", DERIVED, "",
         FROZEN, "", NOTPRED, "",
         "## The two configurations compared", "",
         "| | BASELINE | VSIN-INCLUDED |", "| --- | --- | --- |",
         "| Sources blended | SP+, FPI, TeamRankings | SP+, FPI, "
         "TeamRankings, VSiN |",
         "| VSiN weight | — (column blank) | "
         f"{W[SRC['vsin_raw']]:g}, the workbook's own reserved weight |"]
    for k in live:
        L.append(f"| {LABEL[k]} effective weight | "
                 f"{out['baseline_effective_weights'][LABEL[k]]:.4f} | "
                 f"{out['vsin_included_effective_weights'][LABEL[k]]:.4f} |")
    L += [f"| VSiN effective weight | — | "
          f"{out['vsin_included_effective_weights']['VSiN']:.4f} |",
          f"| Distribution SD | {out['sd']['baseline']:.3f} | "
          f"{out['sd']['vsin_included']:.3f} |", "",
          "Both configurations use the workbook's own renormalisation rule — "
          "weights spread across whatever sources are present, missing is "
          "never zero. Neither changes any stored weight.", "",
          "## How far the prior would actually move", "",
          "| Measure | Points |", "| --- | --- |",
          f"| Mean absolute change | {out['delta']['mean_abs']:.3f} |",
          f"| Median absolute change | {out['delta']['median_abs']:.3f} |",
          f"| Largest change | {out['delta']['max_abs']:.3f} |",
          f"| Teams moving 0.5 pts or more | {out['delta']['n_over_0_5']} of 138 |",
          f"| Teams moving 1.0 pt or more | {out['delta']['n_over_1_0']} of 138 |",
          f"| Teams whose rank does not change | {out['rank']['unchanged']} of 138 |",
          f"| Largest rank move | {out['rank']['max_move']} places |", "",
          "## How much new information VSiN carries", "",
          "The question is not whether VSiN agrees with the existing "
          "sources — Phase 6 already showed it does. It is whether VSiN says "
          "anything the three live sources do not already say. Regressing "
          "the VSiN column on the other three answers that directly.", "",
          "| | Value |", "| --- | --- |",
          f"| R² of VSiN on SP+, FPI and TeamRankings | **{r2:.4f}** |",
          f"| Residual standard deviation | **{resid_sd:.3f} points** |", "",
          f"{r2*100:.1f}% of the variance in Makinen's ratings is already "
          f"explained by the three sources the workbook blends today. What "
          f"remains is about {resid_sd:.2f} points of standard deviation of "
          f"genuinely independent opinion — real, but small against a "
          f"distribution whose own SD is {out['sd']['baseline']:.1f} points.", "",
          "Whether that independent component is *skilful* or merely "
          "*different* is exactly the question no data in this project can "
          "currently answer.", "",
          "### Pairwise correlations between normalised sources", "",
          "| Pair | r |", "| --- | --- |"]
    for k, v in out["pairwise_correlation"].items():
        L.append(f"| {k} | {v:.4f} |")
    L += ["", "## Weight sensitivity — diagnostic only", "", NOTPRED, "",
          "These are experiments, not candidate configurations. No weight "
          "below is proposed for production, and none was selected by "
          "minimising anything.", "",
          "| VSiN weight | Effective | Mean abs Δ | Max abs Δ | Teams ≥1 pt | "
          "Max rank move | Blend SD |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for s in sweep:
        L.append(f"| {s['w']:g} | {s['eff']:.4f} | {s['mean_abs']:.3f} | "
                 f"{s['max_abs']:.3f} | {s['n_over_1pt']} | {s['max_rank']} | "
                 f"{s['sd']:.3f} |")
    L += ["",
          "The relationship is close to linear and the magnitudes stay "
          "small throughout: even at triple its reserved weight, VSiN moves "
          "the average team by well under a point. That is a useful thing "
          "to know before spending effort on the decision — but it cuts "
          "both ways, since a change too small to matter is also a change "
          "too small to be worth risking.", "",
          "## Teams the inclusion would move most", "",
          "| Team | Conference | Baseline | VSiN-included | Δ | Rank move |",
          "| --- | --- | --- | --- | --- | --- |"]
    for t in sorted(teams, key=lambda x: -abs(delta[x]))[:20]:
        L.append(f"| {tlink(t)} | {conf[t]} | {base[t]:+.2f} | {withv[t]:+.2f} "
                 f"| **{delta[t]:+.3f}** | {rank_move[t]:+d} |")
    L += ["", "## Where Makinen most disagrees with the live consensus", "",
          "The regression residual is the part of Makinen's rating that the "
          "three live sources cannot explain. A large residual is where his "
          "independent opinion actually lives.", "",
          "| Team | Conference | VSiN residual | Makinen | Baseline prior |",
          "| --- | --- | --- | --- | --- |"]
    ridx = {t: resid[teams.index(t)] for t in teams}
    for t in sorted(teams, key=lambda x: -abs(ridx[x]))[:20]:
        L.append(f"| {tlink(t)} | {conf[t]} | **{ridx[t]:+.2f}** | "
                 f"{p47[t]:g} | {base[t]:+.2f} |")
    L += ["", "## Cross-links", "",
          "- [Pre-registered test protocol](01_CALIBRATION_PROTOCOL.md)",
          "- [Phase 7 report](01_PHASE7_REPORT.md)",
          "- [VSiN import candidate](00_VSIN_IMPORT_CANDIDATE.md)",
          "- [Scale reconciliation](00_SCALE_RECONCILIATION.md)"]
    write("01_VSIN_DIAGNOSTICS.md", L)

    print("calibration diagnostics written")
    print(f"  baseline eff weights   { {k: round(v,4) for k,v in out['baseline_effective_weights'].items()} }")
    print(f"  vsin-incl eff weights  { {k: round(v,4) for k,v in out['vsin_included_effective_weights'].items()} }")
    print(f"  mean |delta|           {out['delta']['mean_abs']:.4f} pts")
    print(f"  max |delta|            {out['delta']['max_abs']:.4f} pts")
    print(f"  teams >=1pt move       {out['delta']['n_over_1_0']}")
    print(f"  ranks unchanged        {out['rank']['unchanged']}/138  max move {out['rank']['max_move']}")
    print(f"  VSiN R^2 on live srcs  {r2:.4f}   residual sd {resid_sd:.3f}")
    return out


if __name__ == "__main__":
    main()
