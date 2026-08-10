#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 7 renderer
=====================================================

Builds 06_Win_Totals from three layers the guide keeps separate and this
library refuses to merge:

  CONFERENCE TABLE   DK win total, power rating, field ratings, schedule
                     strength and projected records — all 138 teams.
  TEAM PAGE          the standalone Over/Under recommendation — all 138.
  FEATURE            Steve Makinen's 29 bets, pp. 22-27, with reasoning.

Where the three disagree, every reading is printed and none is resolved.
The 26-field record is rendered for the 29 feature teams; the other 109
appear in the all-teams table with their two printed layers and a pointer
to the team file, because pp. 22-27 says nothing about them and this phase
will not invent an argument on the guide's behalf.

Usage:  python3 _tools/build_wintotals.py
"""

import json
import os
import statistics as stats

from coach_lib import slug
from wintotal_lib import (NA, implied_side, load_conference_rows, load_feature,
                          load_notes, load_team_picks, margin)

OUT = "06_Win_Totals"
HEADER = ("<!-- GENERATED FILE — do not hand-edit.\n"
          "     Rebuild:  python3 _tools/build_wintotals.py\n"
          "     Source:   2026 VSiN College Football Betting Guide -->\n")

GUIDE = ("> **Source class: GUIDE CONTENT.** Every number and argument is "
         "printed in the 2026 VSiN College Football Betting Guide. TTW "
         "reference notes paraphrase the reasoning; the judgement is the "
         "guide's. No outside research, no post-publication updates.")
DERIVED = ("> **Source class: TTW DERIVED.** The comparison below is this "
           "library's arithmetic over figures the guide prints. It is not a "
           "VSiN claim and not a betting model.")

FIELDS = [
    ("over_argument", 9, "Core Over argument"),
    ("under_argument", 10, "Core Under argument"),
    ("schedule_argument", 11, "Schedule argument"),
    ("qb_argument", 12, "Quarterback argument"),
    ("coaching_argument", 13, "Coaching argument"),
    ("roster_argument", 14, "Returning-production / roster argument"),
    ("key_games", 17, "Key swing games"),
    ("floor_case", 18, "Floor case"),
    ("ceiling_case", 19, "Ceiling case"),
    ("risks", 20, "Risks to recommendation"),
    ("futures_interaction", 21, "Relevant futures interaction"),
    ("best_bet_interaction", 22, "Relevant best-bet interaction"),
    ("other_opinions", 23, "Other VSiN contributor opinions"),
]


def write(name, lines):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(HEADER + "\n" + "\n".join(lines) + "\n")


def tlink(team):
    return f"[{team}](../02_Team_Database/{slug(team)})"


def f(note, key):
    v = (note or {}).get(key)
    return v if v else NA


def render_team(team, e, row, tp, note):
    L, A = [], None
    A = L.append
    A(f"# {team} — Win Total {e['side']} {e['number']:g}")
    A("")
    A(GUIDE)
    A("")
    A(f"> Feature: *2026 college football win totals I'm betting now*, "
      f"Steve Makinen, p. {e['page']}. Conference table p. "
      f"{row['preview_page']}. Team pages pp. "
      f"{tp['pages'][0]}–{tp['pages'][1]}.")
    A("")
    A("## The market and the recommendation")
    A("")
    A("| # | Field | Value |")
    A("| --- | --- | --- |")
    A(f"| 1 | Team | {team} |")
    A(f"| 2 | Conference | {row['team'] and e['conference']} |")
    A(f"| 3 | Posted win total | **{row['dk_win_total']}** "
      f"(DraftKings, conference table p. {row['preview_page']}) |")
    A(f"| 4 | Over price | {NA} |")
    A(f"| 5 | Under price | {NA} |")
    A(f"| 6 | VSiN recommendation | **{e['side']} {e['number']:g}** |")
    A(f"| 7 | Recommendation strength | {f(note, 'strength')} |")
    A(f"| 8 | Contributor | Steve Makinen (feature); team page pick printed "
      f"as **{tp['pick']['side'].title()} {tp['pick']['number']}** |")
    for key, num, label in FIELDS:
        A(f"| {num} | {label} | {f(note, key)} |")
    A(f"| 15 | Power-rating context | Makinen rates them "
      f"**{row['sm_power_rating']}**; his projected record is "
      f"{row['proj_wins_all']}–{row['proj_losses_all']} overall and "
      f"{row['proj_wins_conf']}–{row['proj_losses_conf']} in conference |")
    A(f"| 16 | Conference-strength context | schedule strength "
      f"{row['schedule_strength']}, ranked #{row['schedule_rank']} of 138 |")
    A(f"| 24 | Internal disagreement | {f(note, 'internal_disagreement')} |")
    A(f"| 25 | Page references | feature p. {e['page']}; conference table "
      f"p. {row['preview_page']}; team pp. {tp['pages'][0]}–{tp['pages'][1]} |")
    A(f"| 26 | Source conflicts / ambiguities | {f(note, 'conflicts')} |")
    A("")

    A("## What the guide's own numbers imply")
    A("")
    A(DERIVED)
    A("")
    imp = implied_side(row["proj_wins_all"], row["dk_win_total"])
    mg = margin(row["proj_wins_all"], row["dk_win_total"])
    A("| Reading | Value |")
    A("| --- | --- |")
    A(f"| Posted total | {row['dk_win_total']} |")
    A(f"| Makinen's projected wins | {row['proj_wins_all']} |")
    A(f"| Difference | {mg:+.2f} |")
    A(f"| Side that difference implies | **{imp}** |")
    A(f"| Side he actually bets | **{e['side']}** |")
    A(f"| Agreement | {'consistent' if imp == e['side'] else '**inconsistent — preserved, not resolved**'} |")
    A("")

    A("## VSiN's argument — TTW reference notes")
    A("")
    A(f(note, "summary"))
    A("")

    A("## Cross-links")
    A("")
    A(f"- Team file: [../02_Team_Database/{slug(team)}](../02_Team_Database/{slug(team)})")
    A(f"- Quarterback: [../04_Quarterback_Database/{slug(team)}](../04_Quarterback_Database/{slug(team)})")
    A(f"- Coaching: [../03_Coaching_Database/{slug(team)}](../03_Coaching_Database/{slug(team)})")
    A(f"- Power rating: [../05_Power_Ratings/00_MAKINEN_RATINGS.md](../05_Power_Ratings/00_MAKINEN_RATINGS.md)")
    A("- Indexes: [Overs](00_OVER_INDEX.md) · [Unders](00_UNDER_INDEX.md) · "
      "[agreement](00_AGREEMENT_INDEX.md) · "
      "[disagreement](00_DISAGREEMENT_INDEX.md)")
    A("")
    return "\n".join(L) + "\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = load_conference_rows()
    picks = load_team_picks()
    feature, feat = load_feature()
    notes = load_notes()

    for team, e in feat.items():
        with open(os.path.join(OUT, slug(team)), "w") as fh:
            fh.write(render_team(team, e, rows[team], picks[team],
                                 notes.get(team)))

    # ---------------- all teams ----------------
    L = ["# Win Totals — all 138 teams", "", GUIDE, "",
         "The guide states a win total three ways and this table keeps them "
         "apart. The **posted total** and **projected record** come from the "
         "conference preview tables; the **team-page pick** is the "
         "standalone Over/Under line on each team's own page; the "
         "**feature** column is Steve Makinen's pp. 22–27 bet, which covers "
         "29 teams.", "",
         "| Team | Conf | Total | PR | SoS (rank) | Projected | Team page | "
         "Feature |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for team in sorted(rows):
        r, tp = rows[team], picks[team]
        e = feat.get(team)
        pick = (f"{tp['pick']['side'].title()} {tp['pick']['number']}"
                if tp["pick"] else NA)
        fx = (f"**{e['side'].title()} {e['number']:g}**"
              if e else "—")
        L.append(f"| {tlink(team)} | {r['team'] and tp['conference']} "
                 f"| {r['dk_win_total']} | {r['sm_power_rating']} "
                 f"| {r['schedule_strength']} (#{r['schedule_rank']}) "
                 f"| {r['proj_wins_all']}–{r['proj_losses_all']} "
                 f"| {pick} | {fx} |")
    L += ["", "## Cross-links", "",
          "- [Feature picks](00_FEATURE_PICKS.md) · [Overs](00_OVER_INDEX.md) "
          "· [Unders](00_UNDER_INDEX.md) · "
          "[win total × power rating](00_WINTOTAL_VS_POWER.md)"]
    write("00_ALL_TEAMS.md", L)

    # ---------------- feature summary ----------------
    fr = feature
    L = [f"# {fr['feature_title']} — {fr['counts']['total']} bets", "",
         GUIDE, "",
         f"*{fr['author']}, pp. {fr['pages'][0]}–{fr['pages'][1]}.* He states "
         f"his method as {fr['stated_method']}, and prints his own record: "
         f"**{fr['stated_record_overall']}** overall across four years "
         f"({fr['stated_record_overall_pct']}), including "
         f"**{fr['stated_record_unders']}** on Unders "
         f"({fr['stated_record_unders_pct']}) — which is why he says he has "
         f"again opted for more Unders than Overs.", "",
         f"**{fr['counts']['over']} Overs, {fr['counts']['under']} Unders.** "
         f"The market named throughout is {fr['market_named']}. "
         f"**No Over or Under price is printed anywhere in the feature**, so "
         f"fields 4 and 5 of every record read `{NA}`", "",
         "| Team | Conf | Pick | Total | PR | Projected | Team page agrees? |",
         "| --- | --- | --- | --- | --- | --- | --- |"]
    for team in sorted(feat):
        e, r, tp = feat[team], rows[team], picks[team]
        same = tp["pick"] and tp["pick"]["side"] == e["side"]
        L.append(f"| [{team}]({slug(team)}) | {tp['conference']} "
                 f"| **{e['side'].title()} {e['number']:g}** "
                 f"| {r['dk_win_total']} | {r['sm_power_rating']} "
                 f"| {r['proj_wins_all']}–{r['proj_losses_all']} "
                 f"| {'yes' if same else '**no**'} |")
    L += ["", "## Cross-links", "",
          "- [All 138 teams](00_ALL_TEAMS.md) · "
          "[disagreement index](00_DISAGREEMENT_INDEX.md)"]
    write("00_FEATURE_PICKS.md", L)

    # ---------------- over / under indexes ----------------
    for side, fname in (("OVER", "00_OVER_INDEX.md"),
                        ("UNDER", "00_UNDER_INDEX.md")):
        sel = sorted(t for t in feat if feat[t]["side"] == side)
        L = [f"# {side.title()} Recommendations — {len(sel)} teams", "",
             GUIDE, "",
             f"Steve Makinen's {side.lower()} bets, pp. 22–27, with the "
             f"stated strength where he gives one.", "",
             "| Team | Conf | Number | Strength as stated | Core argument |",
             "| --- | --- | --- | --- | --- |"]
        for team in sel:
            n = notes.get(team) or {}
            L.append(f"| [{team}]({slug(team)}) | {picks[team]['conference']} "
                     f"| {feat[team]['number']:g} "
                     f"| {n.get('strength') or NA} "
                     f"| {n.get('headline') or NA} |")
        L += ["", "## Cross-links", "",
              "- [Feature picks](00_FEATURE_PICKS.md) · "
              "[dependency index](00_DEPENDENCY_INDEX.md)"]
        write(fname, L)

    # ---------------- dependency index ----------------
    tags = {"qb": "Quarterback-dependent", "coaching": "Coaching-dependent",
            "schedule": "Schedule-dependent", "roster": "Roster / returning-production dependent",
            "portal": "Portal / recruiting dependent"}
    L = ["# What the Recommendations Depend On", "", GUIDE, "",
         "A team appears under a heading only where the guide's own argument "
         "rests on it. These are contextual cross-links, not a scoring "
         "system, and no weight is assigned to any of them.", ""]
    for tag, label in tags.items():
        sel = sorted(t for t in feat
                     if tag in ((notes.get(t) or {}).get("depends_on") or []))
        L += [f"## {label} — {len(sel)} teams", "",
              "| Team | Pick | What the guide rests it on |",
              "| --- | --- | --- |"]
        for team in sel:
            n = notes.get(team) or {}
            key = {"qb": "qb_argument", "coaching": "coaching_argument",
                   "schedule": "schedule_argument", "roster": "roster_argument",
                   "portal": "roster_argument"}[tag]
            L.append(f"| [{team}]({slug(team)}) "
                     f"| **{feat[team]['side'].title()} {feat[team]['number']:g}** "
                     f"| {n.get(key) or NA} |")
        L.append("")
    L += ["## Cross-links", "",
          "- [Coaching Database](../03_Coaching_Database/README.md) · "
          "[Quarterback Database](../04_Quarterback_Database/README.md)"]
    write("00_DEPENDENCY_INDEX.md", L)

    # ---------------- agreement / disagreement ----------------
    agree, disagree = [], []
    for team, e in feat.items():
        r, tp = rows[team], picks[team]
        imp = implied_side(r["proj_wins_all"], r["dk_win_total"])
        sig = []
        if tp["pick"] and tp["pick"]["side"] == e["side"]:
            sig.append("team-page pick agrees")
        if imp == e["side"]:
            sig.append("his own projected record agrees")
        n = notes.get(team) or {}
        if n.get("other_opinions") and n["other_opinions"] != NA:
            sig.append("another contributor is quoted on the same side")
        conflicts = []
        if tp["pick"] and tp["pick"]["side"] != e["side"]:
            conflicts.append(f"the team page prints **{tp['pick']['side'].title()} "
                             f"{tp['pick']['number']}**, the opposite side")
        if tp["pick"] and str(tp["pick"]["number"]) != str(r["dk_win_total"]):
            conflicts.append(f"the team page uses {tp['pick']['number']} while "
                             f"the conference table prints {r['dk_win_total']}")
        if imp and imp != e["side"]:
            conflicts.append(f"his own projection of {r['proj_wins_all']} wins "
                             f"against a total of {r['dk_win_total']} implies "
                             f"**{imp}**")
        if n.get("internal_disagreement") and n["internal_disagreement"] != NA:
            conflicts.append(n["internal_disagreement"])
        (agree if len(sig) >= 2 else []).append((team, sig)) if len(sig) >= 2 else None
        if conflicts:
            disagree.append((team, conflicts))

    L = [f"# Multiple VSiN Signals Agree — {len(agree)} teams", "", GUIDE, "",
         "Teams where at least two independent parts of the guide point the "
         "same way. Agreement is recorded, not scored: the guide agreeing "
         "with itself is not evidence that it is right.", "",
         "| Team | Pick | Signals that agree |", "| --- | --- | --- |"]
    for team, sig in sorted(agree):
        L.append(f"| [{team}]({slug(team)}) | **{feat[team]['side'].title()} "
                 f"{feat[team]['number']:g}** | " + "; ".join(sig) + " |")
    L += ["", "## Cross-links", "",
          "- [Internal disagreement](00_DISAGREEMENT_INDEX.md)"]
    write("00_AGREEMENT_INDEX.md", L)

    L = [f"# Internal VSiN Disagreement — {len(disagree)} teams", "", GUIDE, "",
         "> **Nothing here is resolved.** Where the guide contradicts itself "
         "about a win total, every printed position is reproduced and the "
         "contradiction is left standing.", "",
         "Three kinds appear: the team page recommending the opposite side "
         "from the feature; the team page using a different number from the "
         "conference table; and Makinen's own projected record implying the "
         "side he does not bet.", ""]
    for team, cs in sorted(disagree):
        e = feat[team]
        L += [f"### {team} — feature says **{e['side'].title()} "
              f"{e['number']:g}**", ""]
        for c in cs:
            L.append(f"- {c}")
        L += ["", f"*Record: [{slug(team)}]({slug(team)})*", ""]
    L += ["## Cross-links", "",
          "- [Agreement index](00_AGREEMENT_INDEX.md) · "
          "[source conflicts](00_SOURCE_CONFLICTS.md)"]
    write("00_DISAGREEMENT_INDEX.md", L)

    # ---------------- win total vs power rating ----------------
    xs = [float(rows[t]["sm_power_rating"]) for t in sorted(rows)]
    ys = [float(rows[t]["dk_win_total"]) for t in sorted(rows)]
    r_pr = stats.correlation(xs, ys)
    resid = {}
    xbar, ybar = stats.fmean(xs), stats.fmean(ys)
    b = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / \
        sum((x - xbar) ** 2 for x in xs)
    a = ybar - b * xbar
    for t in sorted(rows):
        resid[t] = float(rows[t]["dk_win_total"]) - (
            a + b * float(rows[t]["sm_power_rating"]))

    L = ["# Win Total × Power Rating — consistency check", "",
         "> **Source class: TTW DERIVED — CONSISTENCY CHECK.** This compares "
         "two things the guide prints. It does **not** claim that a power "
         "rating determines a win total: schedule and the distribution of "
         "opponents matter, which is why Makinen runs his ratings against "
         "each schedule rather than reading wins off the rating. The purpose "
         "is to surface interesting inconsistencies, not to declare errors.",
         "",
         f"Across all 138 teams the posted win total and Makinen's power "
         f"rating correlate at **{r_pr:.4f}**. A least-squares line through "
         f"them gives an expected total for each rating; the residual below "
         f"is the posted total minus that expectation. A positive residual "
         f"means the market total is higher than the rating alone would "
         f"suggest — most often because the schedule is soft.", "",
         "## Largest positive residuals — total high for the rating", "",
         "| Team | Conf | Total | PR | SoS rank | Residual | Feature pick |",
         "| --- | --- | --- | --- | --- | --- | --- |"]
    for t in sorted(rows, key=lambda x: -resid[x])[:15]:
        e = feat.get(t)
        L.append(f"| {tlink(t)} | {picks[t]['conference']} "
                 f"| {rows[t]['dk_win_total']} | {rows[t]['sm_power_rating']} "
                 f"| #{rows[t]['schedule_rank']} | **{resid[t]:+.2f}** "
                 f"| {(e['side'].title() + ' ' + format(e['number'], 'g')) if e else '—'} |")
    L += ["", "## Largest negative residuals — total low for the rating", "",
          "| Team | Conf | Total | PR | SoS rank | Residual | Feature pick |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for t in sorted(rows, key=lambda x: resid[x])[:15]:
        e = feat.get(t)
        L.append(f"| {tlink(t)} | {picks[t]['conference']} "
                 f"| {rows[t]['dk_win_total']} | {rows[t]['sm_power_rating']} "
                 f"| #{rows[t]['schedule_rank']} | **{resid[t]:+.2f}** "
                 f"| {(e['side'].title() + ' ' + format(e['number'], 'g')) if e else '—'} |")
    L += ["",
          "## Reading these", "",
          "A large residual is a place where the market's number and "
          "Makinen's rating sit further apart than usual. That is often a "
          "schedule effect and sometimes a disagreement. It is never, on its "
          "own, an error — and this page does not treat it as one.", "",
          "## Cross-links", "",
          "- [Power Ratings](../05_Power_Ratings/00_MAKINEN_RATINGS.md) · "
          "[all teams](00_ALL_TEAMS.md)"]
    write("00_WINTOTAL_VS_POWER.md", L)

    # ---------------- source conflicts ----------------
    numdiff = [t for t in rows if picks[t]["pick"]
               and str(picks[t]["pick"]["number"]) != str(rows[t]["dk_win_total"])]
    sidediff = [t for t in feat if picks[t]["pick"]
                and picks[t]["pick"]["side"] != feat[t]["side"]]
    L = ["# Source Conflict Audit — win totals", "", GUIDE, "",
         "> **Nothing here is corrected.** Every printed figure is "
         "reproduced as printed.", "",
         f"## The team page and the conference table print different numbers "
         f"— {len(numdiff)} teams", "",
         "The conference tables print the DraftKings number. The team pages "
         "carry their own. The guide acknowledges this itself on Houston's "
         "page, which says the win total *is either 7.5 or 8.5 depending on "
         "where you look*. Both are reproduced.", "",
         "| Team | Conference table | Team page |", "| --- | --- | --- |"]
    for t in sorted(numdiff):
        L.append(f"| {tlink(t)} | {rows[t]['dk_win_total']} "
                 f"| {picks[t]['pick']['side'].title()} "
                 f"{picks[t]['pick']['number']} |")
    L += ["",
          f"## The team page and the feature recommend opposite sides — "
          f"{len(sidediff)} teams", "",
          "| Team | Feature (pp. 22–27) | Team page |", "| --- | --- | --- |"]
    for t in sorted(sidediff):
        L.append(f"| [{t}]({slug(t)}) | **{feat[t]['side'].title()} "
                 f"{feat[t]['number']:g}** | **{picks[t]['pick']['side'].title()} "
                 f"{picks[t]['pick']['number']}** |")
    L += ["",
          "## A defect found in a TTW artefact, not in the guide", "",
          "Phase 7 re-derived the feature list from pp. 22–27 and found that "
          "the stored Phase 2 artefact `phase2_win_totals.json` disagreed "
          "with its own generator in two rows: **Memphis** (UNDER 7.5) was "
          "missing, **South Florida** carried 7.5 instead of 8.5, and "
          "**UTSA** appeared although it is not in the feature at all. The "
          "counts still read 14 Overs and 15 Unders, which is why the "
          "original validation passed. Re-running the committed Phase 2 "
          "extractor today reproduces the correct 29, so the stored file was "
          "stale rather than the code being wrong. It has been regenerated "
          "and the American conference file rebuilt; no other phase output "
          "changed.", "",
          "## Cross-links", "",
          "- [Internal disagreement](00_DISAGREEMENT_INDEX.md) · "
          "[Phase 5 conflicts](../03_Coaching_Database/00_SOURCE_CONFLICTS.md)"]
    write("00_SOURCE_CONFLICTS.md", L)

    # ---------------- readme ----------------
    L = ["# 06 Win Totals", "", GUIDE, "",
         "Every win-total number, recommendation and projected-win figure in "
         "the guide, with the reasoning attached and the guide's three "
         "separate statements of each kept apart.", "",
         "## Files", "", "| File | Content |", "| --- | --- |",
         "| [00_FEATURE_PICKS.md](00_FEATURE_PICKS.md) | Makinen's 29 bets, "
         "pp. 22–27 |",
         "| [00_ALL_TEAMS.md](00_ALL_TEAMS.md) | all 138 teams, three layers "
         "side by side |",
         "| [00_OVER_INDEX.md](00_OVER_INDEX.md) | the "
         f"{feature['counts']['over']} Overs |",
         "| [00_UNDER_INDEX.md](00_UNDER_INDEX.md) | the "
         f"{feature['counts']['under']} Unders |",
         "| [00_DEPENDENCY_INDEX.md](00_DEPENDENCY_INDEX.md) | what each "
         "recommendation rests on |",
         "| [00_AGREEMENT_INDEX.md](00_AGREEMENT_INDEX.md) | multiple signals "
         "agree |",
         "| [00_DISAGREEMENT_INDEX.md](00_DISAGREEMENT_INDEX.md) | internal "
         "disagreement, preserved |",
         "| [00_WINTOTAL_VS_POWER.md](00_WINTOTAL_VS_POWER.md) | TTW DERIVED "
         "consistency check |",
         "| [00_SOURCE_CONFLICTS.md](00_SOURCE_CONFLICTS.md) | conflicts and "
         "one artefact defect |",
         f"| *team files* | {len(feat)} records, 26 fields each |", "",
         "## The three layers", "", "| Layer | Coverage | Author |",
         "| --- | --- | --- |",
         "| Conference table — total, rating, schedule strength, projected "
         "record | 138 | conference preview author |",
         "| Team page — standalone Over/Under line | 138 | team page |",
         "| Feature pp. 22–27 — the bets, with arguments | 29 | Steve "
         "Makinen |", "",
         "No Over or Under **price** is printed anywhere in the guide's "
         "win-total material, so fields 4 and 5 of every record read "
         f"`{NA}` That is a property of the source, not a gap in this "
         "phase.", "",
         "## Rebuild", "", "```bash",
         "python3 _tools/extract_wintotals.py",
         "python3 _tools/build_wintotals.py",
         "python3 _tools/validate_wintotals.py", "```"]
    write("README.md", L)

    print(f"win-total files written to {OUT}/")
    print(f"  feature records   {len(feat)}  "
          f"({feature['counts']['over']} over / {feature['counts']['under']} under)")
    print(f"  notes authored    {len(notes)}/{len(feat)}")
    print(f"  agreement         {len(agree)}")
    print(f"  disagreement      {len(disagree)}")
    print(f"  number conflicts  {len(numdiff)}   side conflicts {len(sidediff)}")
    print(f"  total~PR corr     {r_pr:.4f}")


if __name__ == "__main__":
    main()
