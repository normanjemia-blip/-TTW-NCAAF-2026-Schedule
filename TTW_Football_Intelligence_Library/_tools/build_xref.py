#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 11 derived cross-reference views
===========================================================================

Populates the three directories the Director folded into Phases 2-3:

  08_Returning_Production   138 teams, counts as Phase 3 extracted them
  09_Transfer_Portal        where the approved library already discusses
                            the portal, quoted and linked
  10_Schedule_Intelligence  1,657 games as Phase 3 extracted them

These are **views, not new extractions**. No PDF is opened, no outside
source is consulted, no field is invented, and no score, grade or ranking
is created. Where an approved artifact does not support a field, the
absence marker is used or the reader is pointed at the source.
"""

import os
import re

from coach_lib import slug
from xref_lib import (NA, PORTAL_TERMS, ROOT, markdown_files, portal_mentions,
                      returning_production, schedule_rows, sentences_with,
                      stability_notes, teams)

RP = os.path.join(ROOT, "08_Returning_Production")
TP = os.path.join(ROOT, "09_Transfer_Portal")
SI = os.path.join(ROOT, "10_Schedule_Intelligence")

HEAD = ("<!-- GENERATED FILE — do not hand-edit.\n"
        "     Rebuild:  python3 _tools/build_xref.py\n"
        "     Source:   derived from approved Phases 1–10 — no new extraction -->\n")

DERIVED = (
    "> **Source class: GUIDE CONTENT, presented as a derived view.** Every "
    "figure on this page was extracted, validated and approved in an earlier "
    "phase; this directory re-presents it for retrieval and adds no new "
    "information. **Grouping and linking are TTW DERIVED.** No new score, "
    "grade, ranking or betting recommendation is created here, and no field "
    "is filled that an approved artifact does not support.")


def write(d, name, body):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w") as fh:
        fh.write(HEAD + "\n" + body.rstrip() + "\n")
    return f"{os.path.basename(d)}/{name}"


def tlink(t, pre="../02_Team_Database/"):
    return f"[{t}]({pre}{slug(t)})"


# ------------------------------------------------------- 08 returning prod

def build_returning(team_list):
    rp = returning_production(team_list)
    files = []
    L = ["# 08 Returning Production\n", DERIVED, "",
         "**Status: ✅ Built — Phase 11 derived view.** Returning-starter "
         "counts for all **138** teams, exactly as Phase 3 extracted them "
         "from each team's page.", "",
         "Returning production is the guide's most mechanised input: "
         "Makinen's Stability material on pp. 40–44 turns these counts into "
         "thresholds, and 21 of the 29 win-total bets on pp. 22–27 rest on "
         "them. The *Stability relevance* column below reports which of the "
         "guide's own printed thresholds a team meets. **It is not a score, "
         "and teams are not ranked by it.**", "",
         "| Team | Conf | Total | Off | Def | Returning QB | Stability relevance | pp. |",
         "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for t in sorted(rp):
        r = rp[t]
        notes = stability_notes(r)
        qb = ("yes" if r["returning_qb"] else "no") if r["returning_qb"] is not None else NA
        L.append(f"| {tlink(t)} | {r['conference']} | "
                 f"{r['total'] if r['total'] is not None else NA} | "
                 f"{r['offense'] if r['offense'] is not None else NA} | "
                 f"{r['defense'] if r['defense'] is not None else NA} | {qb} | "
                 f"{'; '.join(n.split(' — ')[0] for n in notes) or '—'} | "
                 f"{r['pages'][0]}–{r['pages'][1]} |")
    L.append("")
    L.append("## The guide's own thresholds\n")
    L.append("Quoted from pp. 40–44 so a team can be read against them. "
             "Records are the guide's, over the first four weeks since 2021, "
             "and are **not** independently backtested by TTW — see "
             "[`12_Historical_Trends`](../12_Historical_Trends/00_STABILITY_SYSTEM.md), "
             "where the long-run figures always travel with last season's "
             "30-36 ATS.\n")
    seen = []
    for t in sorted(rp):
        for n in stability_notes(rp[t]):
            if n not in seen:
                seen.append(n)
    for n in seen:
        L.append(f"- {n}")
    L.append("")
    L.append("## Source conflicts\n")
    L.append("Different contributors count returning production differently. "
             "On **North Texas**, one writes that zero starters return while "
             "another writes that eight percent of snaps do; both are printed "
             "in the guide and both are preserved in "
             "[`06_Win_Totals`](../06_Win_Totals/00_SOURCE_CONFLICTS.md). "
             "Nothing here adjudicates that.\n")
    L.append("Two teams — **North Dakota State** and **Sacramento State** — "
             "carry no 2025 statistics at all, because the guide prints "
             "`PARTICIPATED IN FCS IN 2025` in place of both tables. Their "
             "returning-starter counts are printed and appear above; the "
             "statistical context does not exist. See "
             "[`14_Statistics_Reference`](../14_Statistics_Reference/README.md).\n")
    L.append("## Cross-links\n")
    L.append("- Per team: [Team Database](../02_Team_Database/README.md) · "
             "[Quarterback Database](../04_Quarterback_Database/README.md) · "
             "[Coaching Database](../03_Coaching_Database/README.md)\n"
             "- Systems: [Historical Trends](../12_Historical_Trends/00_STABILITY_SYSTEM.md) "
             "· [Betting Concepts → Returning Production]"
             "(../11_Betting_Concepts/returning_production.md)\n"
             "- Applied: [Win Totals](../06_Win_Totals/00_DEPENDENCY_INDEX.md)")
    files.append(write(RP, "README.md", "\n".join(L)))
    return files


# ------------------------------------------------------------- 09 portal

def build_portal(team_list, files_md):
    mentions = portal_mentions(files_md)
    by_team = {}
    for t in team_list:
        name = t["team"]
        s = slug(name)
        hits = []
        for d, label in (("02_Team_Database", "team outlook"),
                         ("04_Quarterback_Database", "quarterback"),
                         ("03_Coaching_Database", "coaching"),
                         ("06_Win_Totals", "win total"),
                         ("07_Futures", "futures")):
            path = f"{d}/{s}"
            body = files_md.get(path)
            if not body:
                continue
            quotes = sentences_with(body, PORTAL_TERMS, 1)
            # A layer counts only if it carries portal PROSE, not merely an
            # empty field whose heading contains the word.
            if quotes:
                hits.append((label, path, quotes))
        if hits:
            by_team[name] = hits

    L = ["# 09 Transfer Portal\n", DERIVED, "",
         "**Status: ✅ Built — Phase 11 derived view.** A retrieval layer over "
         "portal material the approved library already holds. It records "
         "**where** the guide discusses the portal for a team and quotes the "
         "library's own approved wording; it does not decide that a transfer "
         "is important, and it consults no outside portal database.", "",
         f"**{len(by_team)} of {len(team_list)} teams** have portal material "
         f"in at least one approved layer.", "",
         "> **What this cannot tell you.** The guide prints no portal class "
         "ranking, no arrivals/departures table and no transfer count. Where "
         "contributors cite an outside service they name it (247Sports most "
         "often) without reproducing it. So *outgoing* transfers are recorded "
         "only where the guide happens to mention them, and the absence of a "
         "team below means the approved layers carry no portal language for "
         "it — not that its roster was unchanged.", "",
         "| Team | Layers with portal material | First approved mention |",
         "| --- | --- | --- |"]
    for name in sorted(by_team):
        hits = by_team[name]
        labels = ", ".join(f"[{lab}](../{path})" for lab, path, _ in hits)
        quote = next((q[0] for _, _, q in hits if q), NA)
        if len(quote) > 190:
            quote = quote[:190].rstrip() + "…"
        L.append(f"| {tlink(name)} | {labels} | {quote} |")
    L.append("")
    L.append("## Quarterback transfers\n")
    L.append("The portal's clearest footprint in this guide is at "
             "quarterback, and the Quarterback Database is the authoritative "
             "record. Two things live there that must not be confused: the "
             "guide's own preseason inventory, and **post-publication QB "
             "updates, which Phase 4 keeps in a separate layer and which are "
             "never merged into GUIDE CONTENT**. Start at "
             "[`04_Quarterback_Database`](../04_Quarterback_Database/README.md).\n")
    L.append("## Where the portal drives a stated position\n")
    L.append("- **Win totals** — portal and recruiting carry three of the 29 "
             "bets outright; see the *Portal / recruiting dependent* section "
             "of [00_DEPENDENCY_INDEX.md](../06_Win_Totals/00_DEPENDENCY_INDEX.md).\n"
             "- **Futures** — John McKechnie's national-title bet on Miami "
             "rests on the claim that roster continuity is overrated and "
             "elite teams reload through the portal, an argument other "
             "contributors reject. Both positions are preserved in "
             "[`07_Futures`](../07_Futures/00_DISAGREEMENT.md).\n"
             "- **Concepts** — the idea itself, and the disagreement inside "
             "the guide about whether continuity still predicts anything: "
             "[Transfer Portal](../11_Betting_Concepts/transfer_portal.md).\n")
    L.append("## Cross-links\n")
    L.append("- [Team Database](../02_Team_Database/README.md) · "
             "[Quarterback Database](../04_Quarterback_Database/README.md) · "
             "[Coaching Database](../03_Coaching_Database/README.md) · "
             "[Returning Production](../08_Returning_Production/README.md)")
    return [write(TP, "README.md", "\n".join(L))]


# ----------------------------------------------------------- 10 schedule

def build_schedule(team_list):
    rows = schedule_rows(team_list)
    files = []
    neutral = [r for r in rows if r["location"] == "neutral"]

    L = ["# 10 Schedule Intelligence\n", DERIVED, "",
         "**Status: ✅ Built — Phase 11 derived view.** All "
         f"**{len(rows):,} scheduled games** for 138 teams, exactly as Phase "
         "3 extracted them: date, opponent, home/away/neutral, Makinen's "
         "projected line, and the opponent's power rating.", "",
         "> **No new schedule-difficulty measure is created here.** The guide "
         "prints its own schedule strength with a national rank for every "
         "team, and that figure lives in the conference tables. **Projected "
         "lines are Makinen's projections, not betting recommendations**, and "
         "nothing on these pages converts one into the other.", "",
         "## Files\n",
         "| File | Content |", "| --- | --- |",
         "| [00_BY_TEAM.md](00_BY_TEAM.md) | every team's full slate |",
         "| [00_NEUTRAL_SITE.md](00_NEUTRAL_SITE.md) | "
         f"the {len(neutral)} neutral-site games |",
         "| [00_SCHEDULE_STRENGTH.md](00_SCHEDULE_STRENGTH.md) | the guide's "
         "own printed schedule strength and rank |",
         "",
         "## Where schedule drives a stated position\n",
         "- **Win totals** — 17 of the 29 bets on pp. 22–27 rest on the "
         "schedule; see the *Schedule-dependent* section of "
         "[00_DEPENDENCY_INDEX.md](../06_Win_Totals/00_DEPENDENCY_INDEX.md).\n"
         "- **Situational angles** — trap games, look-ahead and letdown "
         "spots, short weeks and travel, argued game by game with **no "
         "printed hit rate anywhere**: "
         "[`13_Situational_Angles`](../13_Situational_Angles/README.md).\n"
         "- **Home-field advantage** — the per-team home and road field "
         "ratings that turn a rating difference into a projected line: "
         "[`05_Power_Ratings`](../05_Power_Ratings/00_MAKINEN_RATINGS.md).\n",
         "## Cross-links\n",
         "- [Team Database](../02_Team_Database/README.md) · "
         "[Conference Database](../01_Conference_Database/00_CONFERENCE_INDEX.md) "
         "· [Power Ratings](../05_Power_Ratings/00_MAKINEN_RATINGS.md)"]
    files.append(write(SI, "README.md", "\n".join(L)))

    by_team = {}
    for r in rows:
        by_team.setdefault(r["team"], []).append(r)
    L = ["# Every Team's Schedule\n", DERIVED, "",
         f"{len(rows):,} games. *Line* is Makinen's projected line for the "
         f"listed team; *Opp PR* is the opponent's Makinen power rating. "
         f"Both are printed in the guide.", ""]
    for t in sorted(by_team):
        L.append(f"## {tlink(t)}\n")
        L.append("| Date | Opponent | Site | Line | Opp PR |")
        L.append("| --- | --- | --- | --- | --- |")
        for g in by_team[t]:
            L.append(f"| {g['date'] or NA} | {g['opponent'] or NA} | "
                     f"{g['location'] or NA} | {g['projected_line'] or NA} | "
                     f"{g['opponent_power_rating'] or NA} |")
        L.append("")
    L.append("## Cross-links\n")
    L.append("- [Schedule Intelligence](README.md) · "
             "[neutral-site games](00_NEUTRAL_SITE.md)")
    files.append(write(SI, "00_BY_TEAM.md", "\n".join(L)))

    L = ["# Neutral-Site Games\n", DERIVED, "",
         f"**{len(neutral)} games** the guide marks as neutral-site. These "
         f"matter because Phase 6 established that Makinen does not model "
         f"them as a bare rating difference: he puts **both teams on their "
         f"road field ratings** for almost all of them.", "",
         "| Team | Date | Opponent | Line | Opp PR |",
         "| --- | --- | --- | --- | --- |"]
    for g in sorted(neutral, key=lambda g: (g["team"], g["date"] or "")):
        L.append(f"| {tlink(g['team'])} | {g['date'] or NA} | "
                 f"{g['opponent'] or NA} | {g['projected_line'] or NA} | "
                 f"{g['opponent_power_rating'] or NA} |")
    L.append("\n## Cross-links\n")
    L.append("- [Power Ratings — line model verification]"
             "(../05_Power_Ratings/00_LINE_MODEL_VERIFICATION.md)")
    files.append(write(SI, "00_NEUTRAL_SITE.md", "\n".join(L)))

    L = ["# Schedule Strength — the guide's own figures\n", DERIVED, "",
         "Printed in every conference preview table: a schedule strength "
         "figure and a national rank out of 138. **TTW computes nothing "
         "here** — no alternative strength measure and no re-ranking.", "",
         "| Team | Conf | Schedule strength | Rank |",
         "| --- | --- | --- | --- |"]
    from xref_lib import conferences
    rowsc = []
    for c in conferences():
        for row in c["standings"]:
            rowsc.append((row["team"], c["conference"],
                          row.get("schedule_strength"), row.get("schedule_rank")))
    for team, conf, ss, rank in sorted(rowsc, key=lambda x: int(x[3] or 999)):
        L.append(f"| {tlink(team)} | {conf} | {ss if ss is not None else NA} | "
                 f"#{rank} of 138 |")
    L.append("\n## Cross-links\n")
    L.append("- [Conference Database](../01_Conference_Database/00_CONFERENCE_INDEX.md) "
             "· [Betting Concepts → Schedule Difficulty]"
             "(../11_Betting_Concepts/schedule_difficulty.md)")
    files.append(write(SI, "00_SCHEDULE_STRENGTH.md", "\n".join(L)))
    return files


def main():
    team_list = teams()
    md = markdown_files()
    f1 = build_returning(team_list)
    f2 = build_portal(team_list, md)
    f3 = build_schedule(team_list)
    rp = returning_production(team_list)
    print(f"08_Returning_Production  {len(f1)} file, {len(rp)} teams")
    print(f"09_Transfer_Portal       {len(f2)} file")
    print(f"10_Schedule_Intelligence {len(f3)} files, "
          f"{len(schedule_rows(team_list)):,} games")


if __name__ == "__main__":
    main()
