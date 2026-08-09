#!/usr/bin/env python3
"""Dump the guide's coaching material for one conference, for authoring.

Pulls together everything the library already holds that bears on a
program's staff: the Coaching Carousel assessment where there is one,
the Phase 3A reference notes tagged coaching/offense/defense/portal, the
Phase 4 scheme-fit and QB-development fields, and the printed Stability
Score components.

Usage: python3 _tools/dump_coaching_source.py "SEC" [start] [end]
"""

import glob
import json
import sys

from coach_lib import load_carousel, load_details, load_stability, load_teams

TAGS = {"coaching", "offense", "defense", "portal", "quarterback"}


def main():
    conf = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    end = int(sys.argv[3]) if len(sys.argv) > 3 else 999

    details, teams = load_details(), load_teams()
    stab, car = load_stability(), load_carousel()

    para = {}
    for f in glob.glob("_source/paraphrase/*.json"):
        para.update(json.load(open(f)))
    qb = {}
    for f in glob.glob("_source/qb/*.json"):
        qb.update(json.load(open(f)))

    names = [t for t in sorted(details) if details[t]["conference"] == conf]
    for team in names[start:end]:
        d, s, t = details[team], stab[team], teams[team]
        print("=" * 74)
        print(f"### {team} | pp.{d['pages'][0]}-{d['pages'][-1]} | "
              f"HC {t['head_coach']} ({t['hc_season']}) interim={t['interim']}")
        print(f"    STABILITY p{s['page']}: HC={s['hc_returns']} OC={s['oc_returns']} "
              f"DC={s['dc_returns']} QB={s['qb_returns']} RS={s['returning_starters_points']}"
              f"({s['returning_starters_count']}) TOTAL={s['stability_score']} "
              f"rec={s['record_2025']}")
        if team in car:
            print(f"    CAROUSEL p{car[team]['page']}: {car[team]['assessment']}")
        v = para.get(team, {})
        for n in v.get("outlook", []):
            if TAGS & set(n["t"]):
                print(f"    [O] {n['n']}")
        for q in v.get("questions", []):
            print(f"    [Q] {q['q']}")
            print(f"        {q['n']}")
        r = qb.get(team, {})
        for k in ("scheme_fit", "qb_development"):
            if r.get(k):
                print(f"    [QB:{k}] {r[k]}")
        print()


if __name__ == "__main__":
    main()
