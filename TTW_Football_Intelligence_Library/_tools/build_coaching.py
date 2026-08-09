#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 5A renderer
======================================================

Builds 03_Coaching_Database: one standardised coaching record per FBS
program, 29 fields, all of it GUIDE CONTENT from the 2026 VSiN College
Football Betting Guide.

Fields 1-5, 26, 27 and 29 are machine-derived from tables this library
already extracted and validated. Fields 6-25 and 28 are authored in
_source/coaching/*.json from the Team Database, the Coaching Carousel
feature and the conference previews.

Two rules are enforced by construction rather than by care:

  * Scheme and tendency fields say `Not addressed in guide.` unless the
    guide states them. A coach's reputation is not evidence.
  * Source conflicts are rendered as their own labelled block, never
    resolved into a single value.

Usage:
    python3 _tools/build_coaching.py           # all 138
    python3 _tools/build_coaching.py SEC       # one conference
"""

import json
import os
import sys
from collections import defaultdict

from coach_lib import (NA, coaching_conflicts, continuity, load_carousel,
                       load_details, load_notes, load_stability, load_teams,
                       slug)

OUT = "03_Coaching_Database"

# Authored fields, in the owner's stated order. The numbers are the
# owner's numbering; the machine-derived fields fill the gaps.
FIELDS = [
    ("previous_hc_experience", 6, "Previous head-coaching experience"),
    ("oc", 7, "Offensive coordinator"),
    ("dc", 8, "Defensive coordinator"),
    ("oc_status", 9, "New / returning OC"),
    ("dc_status", 10, "New / returning DC"),
    ("play_caller", 11, "Play-caller identity"),
    ("offensive_scheme", 12, "Offensive scheme / philosophy"),
    ("defensive_scheme", 13, "Defensive scheme / philosophy"),
    ("tempo", 14, "Tempo tendencies"),
    ("run_pass", 15, "Run/pass tendencies"),
    ("personnel", 16, "Personnel tendencies"),
    ("qb_development", 17, "QB-development history"),
    ("continuity", 18, "Coordinator/head-coach continuity"),
    ("staff_turnover", 19, "Staff turnover"),
    ("prior_school", 20, "Prior-school relationships"),
    ("portal_recruiting", 21, "Portal/recruiting implications tied to staff"),
    ("vsin_assessment", 22, "VSiN author's assessment of coaching"),
    ("strengths", 23, "Coaching strengths"),
    ("concerns", 24, "Coaching concerns"),
    ("betting", 25, "Betting implications explicitly tied to coaching"),
]


def field(note, key):
    v = (note or {}).get(key)
    return v if v else NA


def ordinal(n):
    return f"{n}{'st' if n == 1 else 'nd' if n == 2 else 'rd' if n == 3 else 'th'}"


def render(team, det, teamrec, cont, note, car, conflicts):
    pages = det["pages"]
    L = []
    A = L.append

    A("<!-- GENERATED FILE — do not hand-edit.")
    A("     Rebuild:  python3 _tools/build_coaching.py")
    A("     Source:   2026 VSiN College Football Betting Guide -->")
    A("")
    A(f"# {team} — Coaching Intelligence")
    A("")
    A(f"> **Source: 2026 VSiN College Football Betting Guide.** Team pages "
      f"pp. {pages[0]}–{pages[-1]}; Stability Score table p. {cont['page']}"
      + (f"; Coaching Carousel p. {car['page']}" if car else "")
      + ". GUIDE CONTENT throughout. No outside research, and no "
        "post-publication updates: this record states the guide's position "
        "at publication and nothing later.")
    A("")

    # ---------------- Identity ----------------
    A("## Program and staff")
    A("")
    A("| # | Field | Value |")
    A("| --- | --- | --- |")
    A(f"| 1 | Team | {team} |")
    A(f"| 2 | Conference | {det['conference']} |")
    A(f"| 3 | Head coach | {cont['head_coach']}"
      + (" *(interim)*" if cont["interim"] else "") + " |")
    A(f"| 4 | Head-coach tenure | {ordinal(cont['hc_season'])} season |")
    new_hc = not cont["hc_returns"]
    A(f"| 5 | New / returning head coach | "
      f"{'**New**' if new_hc else 'Returning'} — the Stability Score table "
      f"(p. {cont['page']}) awards {cont['hc_points']} points for a returning "
      f"head coach |")
    for key, num, label in FIELDS:
        A(f"| {num} | {label} | {field(note, key)} |")
    A(f"| 26 | Stability Score information | **{cont['score']}** total "
      f"(p. {cont['page']}) — see the component table below |")
    A(f"| 27 | Relevant page references | team pp. {pages[0]}–{pages[-1]}; "
      f"Stability Score p. {cont['page']}"
      + (f"; Coaching Carousel p. {car['page']}" if car else "") + " |")
    A(f"| 28 | Source conflicts / ambiguities | "
      f"{'See the labelled block below.' if conflicts else field(note, 'conflicts')} |")
    A("")

    # ---------------- Stability ----------------
    A("## VSiN Stability Score — as printed")
    A("")
    A("Steve Makinen's Stability Score (pp. 41–44), reproduced exactly. This "
      "library does not recompute it, re-weight it, or substitute a TTW score.")
    A("")
    A("| Component | Points | Reading |")
    A("| --- | --- | --- |")
    A(f"| Head coach returns | {cont['hc_points']} | "
      f"{'Returning head coach' if cont['hc_returns'] else '**New head coach**'} |")
    A(f"| Offensive coordinator returns | {cont['oc_points']} | "
      f"{'Returning OC' if cont['oc_returns'] else '**New OC**'} |")
    A(f"| Defensive coordinator returns | {cont['dc_points']} | "
      f"{'Returning DC' if cont['dc_returns'] else '**New DC**'} |")
    A(f"| Quarterback returns | {cont['qb_points']} | "
      f"{'Returning QB' if cont['qb_returns'] else '**New QB**'} |")
    A(f"| Returning starters | {cont['rs_points']} | "
      f"{cont['rs_count']} returning starters as printed in the table |")
    A(f"| **Total** | **{cont['score']}** | 2025 record {cont['record_2025']} |")
    A("")
    A("> The guide's own use of this number: it plays on teams with a "
      "Stability Score edge of 6 or more in non-conference games in weeks "
      "0–3, and against teams scoring 0–6 in the same window, excluding "
      "games with a spread of 30 or more (pp. 40–41).")
    A("")

    # ---------------- Carousel ----------------
    if car:
        A("## VSiN on this hire — The Coaching Carousel Never Stops")
        A("")
        A(f"*Adam Burke, p. {car['page']}. GUIDE CONTENT — TTW reference notes "
          f"summarising the guide's assessment; the judgement is the guide's.*")
        A("")
        A(field(note, "carousel_summary"))
        A("")

    # ---------------- Conflicts ----------------
    if conflicts:
        A("## SOURCE CONFLICT")
        A("")
        for c in conflicts:
            A(f"**{c['field']}.** {c['detail']}")
            A("")

    # ---------------- Cross-links ----------------
    A("## 29. Cross-links")
    A("")
    A(f"- Team file: [../02_Team_Database/{slug(team)}](../02_Team_Database/{slug(team)})")
    A(f"- Quarterback file: [../04_Quarterback_Database/{slug(team)}](../04_Quarterback_Database/{slug(team)})")
    cslug = det["conference"].lower().replace(" ", "_").replace("-", "_")
    A(f"- Conference file: [../01_Conference_Database/{cslug}.md](../01_Conference_Database/{cslug}.md)")
    A("- Change indexes: [new head coaches](00_NEW_HEAD_COACHES.md) · "
      "[continuity matrix](00_CONTINUITY_MATRIX.md) · "
      "[QB × coaching](00_QB_COACHING_CROSSLINK.md)")
    A("")
    return "\n".join(L) + "\n"


def build():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    teams = load_teams()
    details = load_details()
    stability = load_stability()
    carousel = load_carousel()
    notes = load_notes()

    by_team = defaultdict(list)
    for c in coaching_conflicts(teams, stability, carousel):
        by_team[c["team"]].append(c)

    os.makedirs(OUT, exist_ok=True)
    rows, written = [], 0
    for team in sorted(teams):
        det = details[team]
        if only and det["conference"] != only:
            continue
        cont = continuity(team, stability, teams)
        note = notes.get(team)
        car = carousel.get(team)
        with open(os.path.join(OUT, slug(team)), "w") as fh:
            fh.write(render(team, det, teams[team], cont, note, car,
                            by_team.get(team, [])))
        written += 1
        rows.append({
            "team": team, "conference": det["conference"],
            "head_coach": cont["head_coach"], "hc_season": cont["hc_season"],
            "interim": cont["interim"],
            "new_hc": not cont["hc_returns"], "new_oc": not cont["oc_returns"],
            "new_dc": not cont["dc_returns"], "new_qb": not cont["qb_returns"],
            "hc_points": cont["hc_points"], "oc_points": cont["oc_points"],
            "dc_points": cont["dc_points"], "qb_points": cont["qb_points"],
            "rs_points": cont["rs_points"], "rs_count": cont["rs_count"],
            "stability_score": int(cont["score"]),
            "record_2025": cont["record_2025"],
            "in_carousel": team in carousel,
            "oc": field(note, "oc"), "dc": field(note, "dc"),
            "play_caller": field(note, "play_caller"),
            "scheme_change": bool((note or {}).get("scheme_change")),
            "staff_turnover_major": bool((note or {}).get("staff_turnover_major")),
            "qb_developer": bool((note or {}).get("qb_developer")),
            "pages": f"{det['pages'][0]}-{det['pages'][-1]}",
            "stability_page": cont["page"],
            "carousel_page": car["page"] if car else None,
            "conflicts": len(by_team.get(team, [])),
            "has_note": note is not None,
        })

    with open("_source/data/coaching_matrix.json", "w") as fh:
        json.dump(rows, fh, indent=1, ensure_ascii=False)
    print(f"coaching files written: {written}" + (f" ({only})" if only else ""))
    return rows


if __name__ == "__main__":
    build()
