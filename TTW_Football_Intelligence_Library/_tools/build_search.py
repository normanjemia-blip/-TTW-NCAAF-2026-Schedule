#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 11 search layer
==========================================================

Builds 99_Search_Index: twelve files that let a reader start from one
entity and reach every approved part of the library without knowing which
phase produced it.

    THE SEARCH LAYER MAY POINT. IT MAY NOT ASSERT.

Every line here is a pointer or a count of pointers. No football claim is
made, no number is recomputed, no team is ranked and no conflict is
resolved. The two registers that look like judgements -- the conflict
roll-up and the gap register -- are deliberately built as *taxonomies*,
because flattening either into a single category would itself be an
assertion: that all conflicts are the same kind of problem, and that every
absence is a deficiency. Neither is true.
"""

import json
import os
import re
import subprocess
from collections import Counter

from coach_lib import slug
from xref_lib import (INDEXED_DIRS, NA, PHASE_DIRS, ROOT, conferences,
                      entity_registry, markdown_files, returning_production,
                      schedule_rows, teams)

OUT = os.path.join(ROOT, "99_Search_Index")

HEAD = ("<!-- GENERATED FILE — do not hand-edit.\n"
        "     Rebuild:  python3 _tools/build_search.py\n"
        "     Source:   derived from approved Phases 1–10 — pointers only -->\n")

POINTER = (
    "> **Source class: TTW DERIVED — navigation only.** This page contains "
    "**no football information**. Every fact it points at was extracted, "
    "authored, validated and approved in an earlier phase, and lives in the "
    "file linked. The search layer may point; it may not assert. It creates "
    "no score, grade, probability, ranking or betting recommendation, and it "
    "resolves no source conflict.")


def write(name, body):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(HEAD + "\n" + body.rstrip() + "\n")
    return name


def link(path, label=None):
    return f"[{label or path}](../{path})"


# ------------------------------------------------------------------ 1 & 2

def build_reverse(reg):
    kinds = Counter(v["kind"] for v in reg.values())
    L = ["# 1 — Reverse Entity Index\n", POINTER, "",
         f"**{len(reg)} entities** — {kinds['team']} teams, "
         f"{kinds['conference']} conferences, {kinds['coach']} head coaches — "
         f"each with every approved file that mentions it.", "",
         "Entities are matched on their **full canonical name only**. "
         "Substring matching on a short name would put every *Miami* mention "
         "on both Miami Hurricanes and Miami (Ohio) RedHawks, which is the "
         "alias drift ten phases of enumerated bijections exist to prevent.", ""]
    for kind, title in (("team", "Teams"), ("conference", "Conferences"),
                        ("coach", "Head coaches")):
        rows = sorted(n for n, v in reg.items() if v["kind"] == kind)
        L.append(f"## {title} — {len(rows)}\n")
        L.append("| Entity | Files | Where |")
        L.append("| --- | --- | --- |")
        for n in rows:
            fs = reg[n]["files"]
            dirs = sorted({f.split("/")[0] for f in fs})
            L.append(f"| {n} | {len(fs)} | {', '.join(f'`{d}`' for d in dirs) or '—'} |")
        L.append("")
    L.append("## Cross-links\n")
    L.append("- [Team lookup](02_TEAM_LOOKUP.md) · "
             "[conference lookup](03_CONFERENCE_LOOKUP.md) · "
             "[coach lookup](04_COACH_LOOKUP.md)")
    return write("01_REVERSE_ENTITY_INDEX.md", "\n".join(L))


def build_team_lookup(team_list, rp):
    L = ["# 2 — Team Master Lookup\n", POINTER, "",
         f"One row per team, **{len(team_list)}** of them. Every cell is a "
         f"link into the phase that owns the answer.", "",
         "| Team | Conf | Team | Coach | QB | Rating | Schedule | Win total | Futures | Ret. prod |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for t in sorted(team_list, key=lambda t: t["team"]):
        n, s = t["team"], slug(t["team"])
        wt = (f"[pick](../06_Win_Totals/{s})"
              if os.path.exists(os.path.join(ROOT, "06_Win_Totals", s))
              else "[table](../06_Win_Totals/00_ALL_TEAMS.md)")
        L.append(
            f"| **{n}** | {t['conference']} "
            f"| {link(f'02_Team_Database/{s}', 'file')} "
            f"| {link(f'03_Coaching_Database/{s}', 'coach')} "
            f"| {link(f'04_Quarterback_Database/{s}', 'QB')} "
            f"| {link('05_Power_Ratings/00_MAKINEN_RATINGS.md', 'PR')} "
            f"| {link('10_Schedule_Intelligence/00_BY_TEAM.md', 'games')} "
            f"| {wt} "
            f"| {link('07_Futures/00_TEAM_FUTURES.md', 'board')} "
            f"| {link('08_Returning_Production/README.md', 'starters')} |")
    L.append("\n## Cross-links\n")
    L.append("- [Reverse index](01_REVERSE_ENTITY_INDEX.md) · "
             "[query recipes](12_QUERY_RECIPES.md)")
    return write("02_TEAM_LOOKUP.md", "\n".join(L))


def build_conf_lookup(conf_list):
    L = ["# 3 — Conference Lookup\n", POINTER, "",
         f"**{len(conf_list)} conferences.** The guide's 2026 alignment "
         f"differs substantially from 2025 — verify membership against the "
         f"Conference Index rather than from memory.", "",
         "| Conference | Teams | Preview | Database | Standings & totals |",
         "| --- | --- | --- | --- | --- |"]
    for c in sorted(conf_list, key=lambda c: c["conference"]):
        name = c["conference"]
        f = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") + ".md"
        p = f"01_Conference_Database/{f}"
        exists = os.path.exists(os.path.join(ROOT, p))
        L.append(f"| **{name}** | {len(c['standings'])} | p. {c['preview_page']} "
                 f"| {link(p, 'file') if exists else link('01_Conference_Database/00_CONFERENCE_INDEX.md', 'index')} "
                 f"| {link('06_Win_Totals/00_ALL_TEAMS.md', 'win totals')} |")
    L.append("\n## Cross-links\n")
    L.append("- [02 — Conference Index](../00_Master_Index/02_Conference_Index.md) "
             "· [team lookup](02_TEAM_LOOKUP.md)")
    return write("03_CONFERENCE_LOOKUP.md", "\n".join(L))


def build_coach_lookup(team_list):
    L = ["# 4 — Coach Lookup\n", POINTER, "",
         f"**{len(team_list)} head coaches**, one per programme. *Yr* is the "
         f"season number the guide prints for that coach at that school.", "",
         "| Coach | Team | Yr | Coaching record | Team file | Historical context |",
         "| --- | --- | --- | --- | --- | --- |"]
    for t in sorted(team_list, key=lambda t: (t.get("head_coach") or "")):
        n, s = t.get("head_coach") or NA, slug(t["team"])
        interim = " *(interim)*" if t.get("interim") else ""
        L.append(f"| **{n}**{interim} | {t['team']} | {t.get('hc_season', NA)} "
                 f"| {link(f'03_Coaching_Database/{s}', 'record')} "
                 f"| {link(f'02_Team_Database/{s}', 'team')} "
                 f"| {link('12_Historical_Trends/00_STABILITY_SYSTEM.md', 'stability')} |")
    L.append("\n## Cross-links\n")
    L.append("- [Coaching Database](../03_Coaching_Database/README.md) · "
             "[04 — Coaching Index](../00_Master_Index/04_Coaching_Index.md)")
    return write("04_COACH_LOOKUP.md", "\n".join(L))


def build_qb_lookup(team_list):
    L = ["# 5 — Quarterback Lookup\n", POINTER, "",
         f"One entry per programme, **{len(team_list)}**. The Quarterback "
         f"Database keeps two layers apart and this index does not merge "
         f"them: the guide's preseason inventory, and **post-publication QB "
         f"updates**, which are never folded into GUIDE CONTENT.", "",
         "| Team | QB record | Returning QB | Team file | Win-total dependency |",
         "| --- | --- | --- | --- | --- |"]
    rp = returning_production(team_list)
    for t in sorted(team_list, key=lambda t: t["team"]):
        n, s = t["team"], slug(t["team"])
        r = rp[n]
        qb = ("yes" if r["returning_qb"] else "no") if r["returning_qb"] is not None else NA
        L.append(f"| **{n}** | {link(f'04_Quarterback_Database/{s}', 'QB file')} "
                 f"| {qb} | {link(f'02_Team_Database/{s}', 'team')} "
                 f"| {link('06_Win_Totals/00_DEPENDENCY_INDEX.md', 'QB-dependent totals')} |")
    L.append("\n## Cross-links\n")
    L.append("- [Quarterback Database](../04_Quarterback_Database/README.md) · "
             "[06 — Quarterback Index](../00_Master_Index/06_Quarterback_Index.md) "
             "· [Betting Concepts → Quarterback Play]"
             "(../11_Betting_Concepts/quarterback_play.md)")
    return write("05_QB_LOOKUP.md", "\n".join(L))


def build_contributor_lookup():
    preds = json.load(open(os.path.join(ROOT, "_source/data/futures_predictions.json")))
    bets = json.load(open(os.path.join(ROOT, "_source/data/futures_best_bets.json")))
    grid = set(preds["roster"])
    bb = set(bets["roster"])
    everyone = sorted(grid | bb)
    L = ["# 6 — Contributor Lookup\n", POINTER, "",
         f"**{len(everyone)} people** state a position somewhere in the guide. "
         f"The two rosters are not the same — **{len(grid)}** fill in the "
         f"p. 4 prediction grid and **{len(bb)}** write best bets — and "
         f"neither is treated as the canonical staff list.", "",
         "> Contributors are **never merged into a house opinion**. The same "
         "person can hold what look like two views in two places because "
         "they are answering two different questions.", "",
         "| Contributor | p. 4 grid | Best bets | Their page |",
         "| --- | --- | --- | --- |"]
    for n in everyone:
        f = re.sub(r"[^a-z0-9]+", "_", n.lower()).strip("_") + ".md"
        p = f"07_Futures/{f}"
        ok = os.path.exists(os.path.join(ROOT, p))
        L.append(f"| **{n}** | {'yes' if n in grid else '—'} "
                 f"| {'yes' if n in bb else '—'} "
                 f"| {link(p, 'positions') if ok else NA} |")
    L.append("\n## Cross-links\n")
    L.append("- [Futures by contributor](../07_Futures/00_BY_CONTRIBUTOR.md) · "
             "[disagreement](../07_Futures/00_DISAGREEMENT.md) · "
             "[08 — Contributor Index](../00_Master_Index/08_Contributor_Index.md)")
    return write("06_CONTRIBUTOR_LOOKUP.md", "\n".join(L))


def build_market_lookup():
    L = ["# 7 — Market and Bet Lookup\n", POINTER, "",
         "Every market the guide prices, and where each lives.", "",
         "| Market | Coverage | Where |",
         "| --- | --- | --- |",
         "| Season win total | 138 posted totals; 29 feature bets; 27 host best bets "
         f"| {link('06_Win_Totals/README.md', 'Win Totals')} · "
         f"{link('07_Futures/00_WINTOTAL_OVERLAP.md', 'overlap')} |",
         "| Conference championship | 10 best bets, plus every team's board "
         f"| {link('07_Futures/00_BEST_BETS.md', 'best bets')} |",
         "| Conference title game | 5 best bets "
         f"| {link('07_Futures/00_BEST_BETS.md', 'best bets')} |",
         "| College Football Playoff | 9 best bets; 138 team prices "
         f"| {link('07_Futures/00_TEAM_FUTURES.md', 'boards')} |",
         "| National championship | 3 best bets; 138 team prices "
         f"| {link('07_Futures/00_TEAM_FUTURES.md', 'boards')} |",
         "| Heisman | 4 on p. 39 plus 4 in best bets "
         f"| {link('07_Futures/00_HEISMAN.md', 'Heisman')} |",
         "| Conference wins | 2 best bets "
         f"| {link('07_Futures/00_BEST_BETS.md', 'best bets')} |",
         "| Pointspread | 1 (BYU +3 vs Utah) "
         f"| {link('07_Futures/00_BEST_BETS.md', 'best bets')} |",
         "| Parlay | 1 (three-team CFP) "
         f"| {link('07_Futures/00_BEST_BETS.md', 'best bets')} |",
         "| Projected game lines | 1,657 games "
         f"| {link('10_Schedule_Intelligence/00_BY_TEAM.md', 'schedules')} |",
         "",
         "> **No price is converted.** The guide prints no implied "
         "probability, removes no vig and states no expected value, and "
         "neither does this library. Projected lines are Makinen's "
         "projections, not recommendations.", "",
         "## Cross-links\n",
         "- [Futures](../07_Futures/README.md) · "
         "[Win Totals](../06_Win_Totals/README.md) · "
         "[Betting Concepts](../11_Betting_Concepts/README.md)"]
    return write("07_MARKET_LOOKUP.md", "\n".join(L))


def build_angle_lookup():
    angles = {}
    d = os.path.join(ROOT, "_source", "trends")
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".json"):
            angles.update(json.load(open(os.path.join(d, fn))))
    L = ["# 8 — Historical Angle Lookup\n", POINTER, "",
         f"**{len(angles)} angles**, all of them the guide's own records.", "",
         "> ⚠️ **TTW has not independently backtested any of these.** The "
         "library holds no game-level historical data, so no hit rate is "
         "recomputed and no span extended. A historical record is not a "
         "current edge. The Stability System's long-run figures never appear "
         "without last season's **30-36 ATS** beside them.", "",
         "| Angle | Author | Span | Sample | Where |",
         "| --- | --- | --- | --- | --- |"]
    for k, a in sorted(angles.items(),
                       key=lambda kv: -(kv[1].get("denominator") or 0)):
        den = a.get("denominator")
        where = ("12_Historical_Trends/00_STABILITY_SYSTEM.md"
                 if k == "stability_system" else
                 "12_Historical_Trends/00_BY_ANGLE.md")
        L.append(f"| {a['title']} | {a['author']} | "
                 f"{a.get('span', NA)} | {den if den else '*not printed*'} "
                 f"| {link(where, 'record')} |")
    L.append("\n## Cross-links\n")
    L.append("- [Historical Trends](../12_Historical_Trends/README.md) · "
             "[by team](../12_Historical_Trends/00_BY_TEAM.md) · "
             "[Situational Angles](../13_Situational_Angles/README.md)")
    return write("08_HISTORICAL_ANGLE_LOOKUP.md", "\n".join(L))


# --------------------------------------------------- 9 conflicts, 10 gaps

CONFLICT_KINDS = [
    ("Actual source contradiction",
     "The guide says two incompatible things about the same fact.",
     [("16 coaching-fact conflicts between the carousel feature and team pages",
       "03_Coaching_Database/00_SOURCE_CONFLICTS.md"),
      ("11 teams where the win-total feature and the team page recommend "
       "OPPOSITE sides", "06_Win_Totals/00_SOURCE_CONFLICTS.md")]),
    ("Different numbers that are not logically contradictory",
     "Two figures that can both be true because they describe different "
     "things, different books or different moments.",
     [("21 teams where the team page and the conference table print different "
       "win totals — the guide acknowledges this itself on Houston's page",
       "06_Win_Totals/00_SOURCE_CONFLICTS.md"),
      ("Three contributors on North Dakota State at two different numbers",
       "06_Win_Totals/00_SOURCE_CONFLICTS.md")]),
    ("Differing contributor opinions",
     "Not a conflict at all: two people disagreeing is the normal state of a "
     "staff room, and one person answering two different questions "
     "differently is not a contradiction.",
     [("Cohen bets Michigan OVER 8.5 while Youmans bets UNDER 8.5, on largely "
       "the same facts", "07_Futures/00_DISAGREEMENT.md"),
      ("7 contributors bet a team to make the 12-team playoff that is not in "
       "their own p. 4 final four — consistent, and listed as context",
       "07_Futures/00_DISAGREEMENT.md"),
      ("Four contributors back four different Mountain West champions",
       "07_Futures/00_BEST_BETS.md")]),
    ("Guide typos and printed slips",
     "Reproduced exactly as printed and flagged. Never silently corrected.",
     [("p. 2 prints `PYPG – Passing Yards per Page`",
       "11_Betting_Concepts/00_GLOSSARY.md"),
      ("p. 40 compares new starting quarterbacks against *returning defensive "
       "coordinators*", "12_Historical_Trends/00_STABILITY_SYSTEM.md"),
      ("p. 5 prints `ALT OVER 7.5 WINS (+120` with no closing bracket",
       "07_Futures/00_SOURCE_CONFLICTS.md"),
      ("A record printed at 45.4% that rounds to 45.5%",
       "12_Historical_Trends/00_STABILITY_SYSTEM.md"),
      ("p. 4's `MWC CCHAMPION` heading",
       "07_Futures/00_PREDICTIONS.md")]),
    ("Printed anomalies",
     "Content the guide prints under a label that does not describe it.",
     [("A `SUN BELT CHAMP` row containing NFL team names — reproduced with "
       "its contents intact", "07_Futures/00_SOURCE_CONFLICTS.md")]),
    ("Genuine source absences",
     "The guide prints a label and no value, for a stated or evident reason.",
     [("North Dakota State and Sacramento State: `PARTICIPATED IN FCS IN "
       "2025` in place of both statistics tables",
       "14_Statistics_Reference/README.md"),
      ("Connecticut and Notre Dame: a conference futures row with a label and "
       "no price, both being Independents",
       "07_Futures/00_SOURCE_CONFLICTS.md"),
      ("No Over/Under price is printed anywhere in the win-total material",
       "06_Win_Totals/README.md")]),
    ("Printed-name inconsistencies",
     "Almost certainly the same person, recorded as each page prints them.",
     [("`Zach Cohen` (p. 39) vs `Zachary Cohen` (pp. 4, 8); `Pauly Howard` "
       "(p. 7) vs `Paul Howard` (p. 4)",
       "07_Futures/00_SOURCE_CONFLICTS.md")]),
    ("Extraction or tooling defects, already repaired",
     "TTW's own errors, found and fixed. Listed separately because they are "
     "**not** guide problems and must never be read as such.",
     [("A stale Phase 2 win-total artefact: Memphis missing, South Florida at "
       "the wrong number, UTSA present though absent from the feature — "
       "regenerated from its own committed generator",
       "06_Win_Totals/00_SOURCE_CONFLICTS.md"),
      ("A Phase 4 quarterback record naming *Matt Klein* for Kansas State, "
       "where the coach is Collin Klein — repaired",
       "04_Quarterback_Database/README.md"),
      ("A column-alignment defect that split *Virginia Tech* across two "
       "contributors on the p. 4 grid — repaired before publication",
       "07_Futures/00_PREDICTIONS.md")]),
    ("Post-publication updates, held separately",
     "Never merged into GUIDE CONTENT. The guide's position at publication "
     "is preserved as the guide's position.",
     [("Phase 4's post-publication quarterback layer, kept apart from the "
       "preseason inventory", "04_Quarterback_Database/README.md")]),
]


def build_conflicts():
    n = sum(len(items) for _, _, items in CONFLICT_KINDS)
    L = ["# 9 — Source Conflict Roll-Up\n", POINTER, "",
         f"**{n} entries in {len(CONFLICT_KINDS)} kinds.** This page points "
         f"at conflicts recorded elsewhere. **It adjudicates none of them.**", "",
         "> **The kinds are the point.** Flattening these into one generic "
         "*conflict* category would itself be an assertion — that a guide "
         "typo, two contributors disagreeing, a genuine absence and a TTW "
         "tooling defect are the same kind of problem. They are not, and the "
         "difference is usually the most useful thing on this page.", ""]
    for kind, gloss, items in CONFLICT_KINDS:
        L.append(f"## {kind} — {len(items)}\n")
        L.append(f"*{gloss}*\n")
        for desc, path in items:
            L.append(f"- {desc} → {link(path, 'record')}")
        L.append("")
    L.append("## Cross-links\n")
    L.append("- [Gap register](10_GAP_REGISTER.md) · "
             "[13 — Open Questions and Gaps](../00_Master_Index/13_Open_Questions_And_Gaps.md)")
    return write("09_SOURCE_CONFLICT_ROLLUP.md", "\n".join(L))


GAP_KINDS = [
    ("The guide genuinely does not provide it",
     "The commonest kind, and not a deficiency. A preseason publication is "
     "not obliged to carry everything.",
     ["No Over/Under **price** anywhere in the win-total material — fields 4 "
      "and 5 of all 29 records",
      "No systematic **weather** angle: four incidental mentions in 345 pages",
      "No measured **travel** figure — no mileage, time zone or rest "
      "differential",
      "No printed hit rate for any classic situational spot",
      "No portal class ranking, arrivals/departures table or transfer count"]),
    ("Information the guide uses but never defines",
     "Vocabulary without a glossary entry. Working definitions exist in the "
     "library but are labelled **TTW DERIVED**, never presented as the "
     "guide's.",
     ["**21 of 29** betting concepts are never defined by the guide — tempo, "
      "regression, explosiveness and situational betting among them",
      "The guide's only glossary is the 45-entry abbreviation list on p. 2"]),
    ("Unavailable because of source structure",
     "The guide's own layout makes it unobtainable, not its editorial choice.",
     ["**Defensive tempo cannot be read at all**: plays per game and time of "
      "possession appear only on the offensive table",
      "North Dakota State and Sacramento State carry no statistics, the guide "
      "printing `PARTICIPATED IN FCS IN 2025` instead",
      "Independents have no conference-title market, so that row prints a "
      "label and no price"]),
    ("Intentionally deferred to another layer",
     "Present in the library, just not where you first looked.",
     ["Team statistics values live in `14_Statistics_Reference`, not in the "
      "concept entries",
      "Win-total reasoning lives in `06_Win_Totals`, not repeated in `07_Futures`",
      "Historical and system-based situational material is in "
      "`12_Historical_Trends`, not in `13_Situational_Angles`"]),
    ("Would require outside research",
     "Deliberately **not** filled. Filling these would move EXTERNAL RESEARCH "
     "into a GUIDE CONTENT layer.",
     ["**Closing Line Value** — one page, an abbreviation only",
      "**Conference Strength** — one page, inside the power-rating method; no "
      "conference-strength measure is printed anywhere",
      "EPA and success rate: cited by contributors, never defined or "
      "tabulated by the guide"]),
    ("Intentionally not derived by TTW",
     "Could have been computed and deliberately was not.",
     ["No implied probability, no vig removal, no expected value",
      "No backtest, re-derived hit rate or extended sample",
      "No VSiN weight promoted into the workbook: the auxiliary calibration "
      "study found the historical paired data do not exist",
      "No consensus count converted into a probability or confidence grade",
      "No new schedule-difficulty or returning-production score"]),
]


def build_gaps(files):
    counts = {}
    for path, body in files.items():
        n = body.count(NA)
        if n:
            counts[path.split("/")[0]] = counts.get(path.split("/")[0], 0) + n
    total = sum(counts.values())
    L = ["# 10 — Gap and Absence Register\n", POINTER, "",
         f"The absence marker `{NA}` appears **{total:,} times** across the "
         f"library.", "",
         "> **A high count is not a deficiency — it is the library working.** "
         "Every one of these is a place where the guide was silent and the "
         "library said so instead of filling the space. The alternative to a "
         "large number here is not a better library; it is a library that "
         "invented things.\n>\n"
         "> **This register is metadata, not a to-do list.** Nothing below is "
         "a request to fill a gap.", "",
         "## By kind\n"]
    for kind, gloss, items in GAP_KINDS:
        L.append(f"### {kind}\n")
        L.append(f"*{gloss}*\n")
        for it in items:
            L.append(f"- {it}")
        L.append("")
    L.append("## Where the marker appears\n")
    L.append("| Directory | Uses |\n| --- | --- |")
    for d in sorted(counts, key=lambda d: -counts[d]):
        L.append(f"| `{d}` | {counts[d]:,} |")
    L.append(f"| **Total** | **{total:,}** |")
    L.append("\n## Cross-links\n")
    L.append("- [Conflict roll-up](09_SOURCE_CONFLICT_ROLLUP.md) · "
             "[Betting Concepts → gaps](../11_Betting_Concepts/00_GAPS.md) · "
             "[13 — Open Questions and Gaps](../00_Master_Index/13_Open_Questions_And_Gaps.md)")
    return write("10_GAP_REGISTER.md", "\n".join(L)), total, counts


# ------------------------------------------------------- 11 link integrity

def check_links():
    """Every relative markdown link in the library, resolved."""
    broken, total = [], 0
    for d in INDEXED_DIRS + ["99_Search_Index"]:
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
                resolved = os.path.normpath(os.path.join(p, target.split("#")[0]))
                if not os.path.exists(resolved):
                    broken.append((f"{d}/{fn}", target))
    return total, broken


def build_link_map(total, broken):
    L = ["# 11 — Link Integrity Map\n", POINTER, "",
         f"Every relative markdown link in the library, resolved against the "
         f"filesystem. **{total:,} links checked.**", "",
         f"## Result: {'✅ all resolve' if not broken else f'❌ {len(broken)} broken'}\n"]
    if broken:
        L.append("| File | Broken target |\n| --- | --- |")
        for f, t in broken[:80]:
            L.append(f"| `{f}` | `{t}` |")
    else:
        L.append("No broken relative link anywhere in the library. This is "
                 "the first repository-wide check — Phases 7–10 each verified "
                 "only their own directory.\n")
    L.append("## Directories covered\n")
    L.append("| Directory | Built by | Files |\n| --- | --- | --- |")
    for d, phase, label in PHASE_DIRS:
        p = os.path.join(ROOT, d)
        n = len([f for f in os.listdir(p) if f.endswith(".md")]) \
            if os.path.isdir(p) else 0
        L.append(f"| `{d}` | Phase {phase} — {label} | {n} |")
    L.append("\n## Cross-links\n")
    L.append("- [Reverse index](01_REVERSE_ENTITY_INDEX.md)")
    return write("11_LINK_INTEGRITY_MAP.md", "\n".join(L))


# ------------------------------------------------------------ 12 recipes

def build_recipes():
    L = ["# 12 — Query Recipes\n", POINTER, "",
         "The questions the project brief asked, and where each is answered "
         "now that the library is built.", "",
         "| Question | Start here |", "| --- | --- |",
         f"| *Everything about one team* | {link('99_Search_Index/02_TEAM_LOOKUP.md', 'team lookup')} — one row, every phase |",
         f"| *Everything about a conference* | {link('99_Search_Index/03_CONFERENCE_LOOKUP.md', 'conference lookup')} |",
         f"| *Every coach entering Year 1* | {link('00_Master_Index/04_Coaching_Index.md', '04 — Coaching Index')} |",
         f"| *Every quarterback competition* | {link('04_Quarterback_Database/README.md', 'Quarterback Database')} |",
         f"| *Compare Makinen with TTW* | {link('05_Power_Ratings/00_TTW_VS_MAKINEN.md', 'Power Ratings')} |",
         f"| *Every win total VSiN bets* | {link('06_Win_Totals/00_FEATURE_PICKS.md', '29 feature picks')} |",
         f"| *Every SEC futures recommendation* | {link('07_Futures/00_BEST_BETS.md', 'best bets')} + {link('99_Search_Index/03_CONFERENCE_LOOKUP.md', 'conference')} |",
         f"| *One contributor's whole position* | {link('99_Search_Index/06_CONTRIBUTOR_LOOKUP.md', 'contributor lookup')} |",
         f"| *Every slow-tempo offense* | {link('14_Statistics_Reference/00_OFFENSE.md', 'offensive statistics')} — plays per game |",
         f"| *Every trap game* | {link('13_Situational_Angles/README.md', 'Situational Angles')} — argued case by case, **no printed hit rate** |",
         f"| *Every portal-heavy roster* | {link('09_Transfer_Portal/README.md', 'Transfer Portal')} — 91 of 138 teams |",
         f"| *Teams meeting a stability threshold* | {link('08_Returning_Production/README.md', 'Returning Production')} |",
         f"| *Does this angle have a track record?* | {link('99_Search_Index/08_HISTORICAL_ANGLE_LOOKUP.md', 'angle lookup')} — **guide records, not TTW backtests** |",
         f"| *What does the guide mean by X?* | {link('11_Betting_Concepts/README.md', 'Betting Concepts')} |",
         f"| *Where does the guide contradict itself?* | {link('99_Search_Index/09_SOURCE_CONFLICT_ROLLUP.md', 'conflict roll-up')} |",
         f"| *What is missing, and why* | {link('99_Search_Index/10_GAP_REGISTER.md', 'gap register')} |",
         "",
         "## Searching the raw guide\n",
         "The full text is extracted and greppable when a question is not "
         "yet indexed:\n",
         "```bash",
         "grep -n 'Georgia' _source/extracted/guide_full.txt   # with page numbers",
         "cat _source/extracted/pages/p292.txt                 # one page",
         "```\n",
         "## Cross-links\n",
         "- [Search Index](README.md) · "
         "[00 — Master Index](../00_Master_Index/00_MASTER_INDEX.md)"]
    return write("12_QUERY_RECIPES.md", "\n".join(L))


def build_readme(reg, total_links, broken, gap_total):
    kinds = Counter(v["kind"] for v in reg.values())
    L = ["# 99 Search Index\n", POINTER, "",
         "**Status: ✅ Built — Phase 11.** The cross-reference layer tying "
         "every entity to every other: team ↔ conference ↔ coach ↔ QB ↔ power "
         "rating ↔ schedule ↔ win total ↔ futures ↔ returning production ↔ "
         "portal ↔ historical trend ↔ betting concept ↔ contributor.", "",
         "Start from any entity you already have in mind and reach every "
         "approved part of the library without knowing which phase built it.", "",
         "## The twelve indexes\n",
         "| # | File | What it does |", "| --- | --- | --- |",
         f"| 1 | [01_REVERSE_ENTITY_INDEX.md](01_REVERSE_ENTITY_INDEX.md) | {len(reg)} entities → every file mentioning them |",
         "| 2 | [02_TEAM_LOOKUP.md](02_TEAM_LOOKUP.md) | 138 teams, one row each, every phase |",
         f"| 3 | [03_CONFERENCE_LOOKUP.md](03_CONFERENCE_LOOKUP.md) | {kinds['conference']} conferences |",
         f"| 4 | [04_COACH_LOOKUP.md](04_COACH_LOOKUP.md) | {kinds['coach']} head coaches |",
         "| 5 | [05_QB_LOOKUP.md](05_QB_LOOKUP.md) | quarterbacks, both layers kept apart |",
         "| 6 | [06_CONTRIBUTOR_LOOKUP.md](06_CONTRIBUTOR_LOOKUP.md) | who says what, never merged |",
         "| 7 | [07_MARKET_LOOKUP.md](07_MARKET_LOOKUP.md) | every market the guide prices |",
         "| 8 | [08_HISTORICAL_ANGLE_LOOKUP.md](08_HISTORICAL_ANGLE_LOOKUP.md) | angles — **guide records, not TTW backtests** |",
         "| 9 | [09_SOURCE_CONFLICT_ROLLUP.md](09_SOURCE_CONFLICT_ROLLUP.md) | conflicts by **kind**, none adjudicated |",
         f"| 10 | [10_GAP_REGISTER.md](10_GAP_REGISTER.md) | {gap_total:,} absences, by why they exist |",
         f"| 11 | [11_LINK_INTEGRITY_MAP.md](11_LINK_INTEGRITY_MAP.md) | {total_links:,} links, {len(broken)} broken |",
         "| 12 | [12_QUERY_RECIPES.md](12_QUERY_RECIPES.md) | the brief's questions, answered |",
         "",
         "## What this layer is not\n",
         "It holds **no football information**. Every fact it points at was "
         "extracted, authored, validated and approved in an earlier phase. It "
         "creates no score, grade, probability, ranking or betting "
         "recommendation; it resolves no source conflict; and it fills no "
         "gap. Where an approved artifact does not support a field, it says "
         "so or points at the source.\n",
         "Two of its registers deliberately refuse to simplify. Conflicts are "
         "sorted into **kinds**, because a guide typo, two contributors "
         "disagreeing, a genuine absence and a repaired TTW tooling defect "
         "are not the same thing. Absences are sorted by **why they exist**, "
         "because a high count is the library working rather than failing.\n",
         "## Cross-links\n",
         "- [00 — Master Index](../00_Master_Index/00_MASTER_INDEX.md) · "
         "[library README](../README.md)"]
    return write("README.md", "\n".join(L))


def main():
    team_list, conf_list = teams(), conferences()
    files = markdown_files()
    reg = entity_registry(files, team_list, conf_list)
    rp = returning_production(team_list)

    out = [build_reverse(reg), build_team_lookup(team_list, rp),
           build_conf_lookup(conf_list), build_coach_lookup(team_list),
           build_qb_lookup(team_list), build_contributor_lookup(),
           build_market_lookup(), build_angle_lookup(), build_conflicts()]
    gap_file, gap_total, gap_counts = build_gaps(files)
    out.append(gap_file)
    total_links, broken = check_links()
    out.append(build_link_map(total_links, broken))
    out.append(build_recipes())
    out.append(build_readme(reg, total_links, broken, gap_total))

    print(f"99_Search_Index  {len(out)} files")
    print(f"  entities       {len(reg)} "
          f"({Counter(v['kind'] for v in reg.values())})")
    print(f"  links checked  {total_links:,}  broken {len(broken)}")
    print(f"  absence marker {gap_total:,} uses across {len(gap_counts)} directories")
    if broken:
        for f, t in broken[:8]:
            print(f"    BROKEN {f} -> {t}")


if __name__ == "__main__":
    main()
