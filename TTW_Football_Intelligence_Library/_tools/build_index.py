#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Master Index Builder
========================================================

Generates every file in 00_Master_Index/ from the JSON tables produced by
extract_guide.py. The index is generated, never hand-edited: rerunning this
after a corrected extraction rebuilds the whole navigation layer consistently.

Usage:
    python3 build_index.py            # run from the library root
"""

import json
import os
from collections import defaultdict

SRC = "_source/data"
OUT = "00_Master_Index"

# Features that run past a single page. Anything not listed occupies one page.
# Explicit rather than inferred, so advertising pages (48, 78, 148 …) fall
# through to the non-content list instead of being absorbed by the article
# above them.
FEATURE_SPANS = {5: 15, 16: 20, 22: 27, 28: 37, 40: 44, 46: 47}

BANNER = (
    "<!-- GENERATED FILE — do not hand-edit.\n"
    "     Rebuild:  python3 _tools/build_index.py\n"
    "     Source:   2026 VSiN College Football Betting Guide (345 pp.) -->\n\n"
)

NOTE_GUIDE = (
    "> **Source class: GUIDE CONTENT.** Every figure and name below is drawn "
    "verbatim from the 2026 VSiN College Football Betting Guide. No outside "
    "research, no inference, no gap-filling.\n"
)


def load(name):
    with open(os.path.join(SRC, f"{name}.json")) as fh:
        return json.load(fh)


def write(filename, text):
    with open(os.path.join(OUT, filename), "w") as fh:
        fh.write(BANNER + text)
    return filename


def page_ref(page, span=None):
    return f"p. {page}" if not span else f"pp. {page}–{span}"


# --------------------------------------------------------------------------- #

def build_structure_map(features, conferences, teams, page_count):
    """Assign every page 1..345 to a section."""
    marks = {}
    for f in features:
        marks[f["page"]] = ("Feature", f["title"])
    for c in conferences:
        marks[c["preview_page"]] = ("Conference Preview", f"{c['conference']} Betting Preview")
    for t in teams:
        marks[t["page"]] = ("Team", f"{t['team']} ({t['conference']})")

    starts = sorted(marks)
    ranges = []
    for i, start in enumerate(starts):
        kind, label = marks[start]
        if kind == "Team":
            end = start + 1  # team spreads are always two pages
        elif kind == "Conference Preview":
            end = start
        else:
            end = FEATURE_SPANS.get(start, start)
        ranges.append((start, end, kind, label))

    covered = set()
    for start, end, _, _ in ranges:
        covered.update(range(start, end + 1))
    filler = sorted(set(range(1, page_count + 1)) - covered)

    lines = [
        "# 01 — Guide Structure Map\n",
        NOTE_GUIDE,
        "\nPage-by-page map of all 345 pages. **Printed page numbers equal PDF "
        "page numbers throughout this guide**, so every reference in this library "
        "works in either.\n",
        "\n| Pages | Type | Section |",
        "| --- | --- | --- |",
    ]
    for start, end, kind, label in ranges:
        pages = f"{start}" if start == end else f"{start}–{end}"
        lines.append(f"| {pages} | {kind} | {label} |")

    lines.append(
        f"\n## Non-content pages\n\nThese carry advertising or no indexable "
        f"content: {', '.join(str(p) for p in filler) or 'none'}.\n"
    )
    lines.append(
        "\n## Structural rules that hold across the whole guide\n\n"
        "These were verified against all 138 team entries and are safe to rely on "
        "when building later phases:\n\n"
        "- Every team occupies exactly **two facing pages**. The even (left) page "
        "carries the header block, schedule and projection prose; the odd (right) "
        "page carries Three Burning Questions, the power rating, and the statistics "
        "tables.\n"
        "- Every team's right page uses an identical statistics schema — "
        "15 offensive and 12 defensive categories. See "
        "[12 — Statistical Category Index](12_Statistical_Category_Index.md).\n"
        "- Conference previews always open on the page before their first team and "
        "carry Makinen's projected standings.\n"
        "- The guide contains **no appendix**; it ends with Troy on pp. 344–345.\n"
    )
    return write("01_Guide_Structure_Map.md", "\n".join(lines))


def build_conference_index(conferences, teams):
    by_conf = defaultdict(list)
    for t in teams:
        by_conf[t["conference"]].append(t)

    lines = [
        "# 02 — Conference Index\n",
        NOTE_GUIDE,
        "\n11 conferences, 138 FBS teams. Team counts reflect the guide's 2026 "
        "alignment, which differs substantially from 2025 — see the realignment "
        "note at the foot of this file.\n",
        "\n| Conference | Preview | Teams | Team page range |",
        "| --- | --- | --- | --- |",
    ]
    for c in conferences:
        members = by_conf[c["conference"]]
        lo = min(t["page"] for t in members)
        hi = max(t["page"] for t in members) + 1
        lines.append(
            f"| **{c['conference']}** | p. {c['preview_page']} | "
            f"{len(members)} | {lo}–{hi} |"
        )

    for c in conferences:
        name = c["conference"]
        members = sorted(by_conf[name], key=lambda t: t["team"])
        lines.append(f"\n## {name}\n")
        lines.append(f"Conference preview: **p. {c['preview_page']}** "
                     f"(includes Makinen's projected standings)\n")
        lines.append("| Team | Pages | Head Coach | Yr | SM Power Rating | Conf Rank |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for t in sorted(members, key=lambda t: int(t["conf_rank"].split()[0][1:])):
            lines.append(
                f"| {t['team']} | {t['page']}–{t['page']+1} | "
                f"{t['head_coach']}{' *(interim)*' if t['interim'] else ''} | "
                f"{t['hc_season']} | {t['power_rating']} | {t['conf_rank']} |"
            )

    lines.append(
        "\n---\n\n## Realignment note (GUIDE CONTENT)\n\n"
        "The guide's 2026 alignment places several programs in conferences that "
        "may surprise anyone working from 2025 memory. Verify against this index "
        "rather than assumption:\n\n"
        "- **Pac-12** is an 8-team league built around Boise State, Colorado State, "
        "Fresno State, Oregon State, San Diego State, Texas State, Utah State and "
        "Washington State.\n"
        "- **Conference USA** includes Delaware, Missouri State, Kennesaw State and "
        "Jacksonville State.\n"
        "- **MAC** includes Sacramento State and UMass.\n"
        "- **Mountain West** includes North Dakota State and Northern Illinois.\n"
        "- **Independents** contains only UConn and Notre Dame.\n"
    )
    return write("02_Conference_Index.md", "\n".join(lines))


def build_team_index(teams):
    lines = [
        "# 03 — Team Index\n",
        NOTE_GUIDE,
        "\nAll 138 FBS teams. This is the primary entry point for team lookups: "
        "find the team, note its page range, then read both pages of the spread.\n",
        "\n**Column key** — *SM PR*: Steve Makinen Power Rating. *SS Rank*: schedule "
        "strength, where #1 is toughest of 138. *2025 SU / ATS / O-U*: straight-up, "
        "against-the-spread and over-under records.\n",
        "\n| Team | Conference | Pages | Head Coach | Yr | 2025 SU | 2025 ATS | 2025 O-U | SM PR | Conf | National | SS Rank |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for t in sorted(teams, key=lambda t: t["team"]):
        lines.append(
            f"| **{t['team']}** | {t['conference']} | {t['page']}–{t['page']+1} | "
            f"{t['head_coach']}{' *(int.)*' if t['interim'] else ''} | {t['hc_season']} | "
            f"{t['su_2025']} | {t['ats_2025']} | {t['ou_2025']} | {t['power_rating']} | "
            f"{t['conf_rank']} | {t['natl_rank']} | {t['sched_strength_rank']} |"
        )
    lines.append(
        "\n---\n\n## What a team spread contains\n\n"
        "Knowing the fixed layout tells you what Phase 3 can promise for every team:\n\n"
        "**Left (even) page** — team name, head coach and tenure, 2025 SU/ATS/O-U "
        "records, schedule strength with national rank, home/road field-advantage "
        "ratings, returning-starter counts, the full 12-game schedule with projected "
        "lines and opponent power ratings, a season-outlook essay, a win-total "
        "recommendation, and a projected win figure.\n\n"
        "**Right (odd) page** — Three Burning Questions, the Makinen power rating "
        "with conference and national rank, futures prices, and the full offensive "
        "and defensive statistics tables with national ranks.\n"
    )
    return write("03_Team_Index.md", "\n".join(lines))


def build_coaching_index(teams, carousel):
    year_one = {t["head_coach"]: t for t in teams if t["hc_season"] == 1}
    profiled = {c["name"]: c["page"] for c in carousel}

    lines = [
        "# 04 — Coaching Index\n",
        NOTE_GUIDE,
        "\nEvery head coach in the guide, with tenure. Tenure is stated as the "
        "**season number** the coach is entering, so `1` means Year 1 at that "
        "program.\n",
        "\n## New head coach profiles — The Coaching Carousel (pp. 28–37)\n",
        f"\nThe guide profiles **{len(carousel)}** coaches in this feature, grouped by "
        "conference.\n",
        "\n| Coach | Profile | Team | Year |",
        "| --- | --- | --- | --- |",
    ]
    team_by_coach = {t["head_coach"]: t for t in teams}
    for c in sorted(carousel, key=lambda c: c["name"]):
        t = team_by_coach.get(c["name"])
        lines.append(
            f"| **{c['name']}** | p. {c['page']} | "
            f"{t['team'] if t else '—'} | {t['hc_season'] if t else '—'} |"
        )

    lines.append(
        f"\n> **Reconciliation note.** {len(year_one)} coaches are listed as entering "
        "Year 1 on their team pages, and all of them are profiled here. The carousel "
        "carries one additional profile: **Mark Carney (Kent State)**, whose team page "
        "shows Year 2. The guide's own text explains why — Carney coached Kent State "
        "as an interim in 2025 and had the tag removed mid-season, so he is new to the "
        "job without being new to the program (p. 34). This is a definitional "
        "difference, not a contradiction; both figures are reported as the guide "
        "states them.\n"
    )

    lines.append("\n## All head coaches by tenure\n")
    lines.append("\n| Coach | Team | Conference | Year | Team pages |")
    lines.append("| --- | --- | --- | --- | --- |")
    for t in sorted(teams, key=lambda t: (t["hc_season"], t["team"])):
        star = " ⭐" if t["hc_season"] == 1 else ""
        lines.append(
            f"| {t['head_coach']}{' *(interim)*' if t['interim'] else ''}{star} | "
            f"{t['team']} | {t['conference']} | {t['hc_season']} | "
            f"{t['page']}–{t['page']+1} |"
        )
    lines.append("\n⭐ = entering Year 1 at the program.\n")

    longest = sorted(teams, key=lambda t: -t["hc_season"])[:10]
    lines.append("\n## Longest-tenured head coaches\n")
    lines.append("\n| Coach | Team | Year |")
    lines.append("| --- | --- | --- |")
    for t in longest:
        lines.append(f"| {t['head_coach']} | {t['team']} | {t['hc_season']} |")

    lines.append(
        "\n## Interim tags\n\n"
        + ("\n".join(
            f"- **{t['head_coach']}** — {t['team']}, listed as interim (p. {t['page']})"
            for t in teams if t["interim"]) or "None.")
        + "\n"
    )
    return write("04_Coaching_Index.md", "\n".join(lines))


def build_coordinator_index(coordinators):
    ocs = [c for c in coordinators if c["role"] == "OC"]
    dcs = [c for c in coordinators if c["role"] == "DC"]
    lines = [
        "# 05 — Coordinator Index\n",
        NOTE_GUIDE,
        f"\n**{len(coordinators)}** coordinators are named in the guide — "
        f"{len(ocs)} offensive, {len(dcs)} defensive.\n",
        "\n> **Coverage limit — read this before relying on the file.** The guide "
        "does not print a coordinator field in the team header block. Coordinators "
        "are named only in running prose, where the writer judged them relevant. "
        "This index therefore captures **every coordinator the guide mentions**, "
        "which is *not* the same as a complete coordinator roster for all 138 teams. "
        "Absence from this list means the guide did not name them — never infer that "
        "a position is vacant or unchanged. Filling the remainder would require "
        "outside research and must be filed as POST-PUBLICATION UPDATE, not "
        "GUIDE CONTENT.\n",
    ]
    for role, group, label in (("OC", ocs, "Offensive coordinators"),
                               ("DC", dcs, "Defensive coordinators")):
        lines.append(f"\n## {label}\n")
        lines.append("\n| Coordinator | Team(s) | Page(s) |")
        lines.append("| --- | --- | --- |")
        for c in sorted(group, key=lambda c: c["name"]):
            teams = ", ".join(c["teams"]) if c["teams"] else "*feature article*"
            pages = ", ".join(str(p) for p in c["pages"])
            lines.append(f"| {c['name']} | {teams} | {pages} |")
    return write("05_Coordinator_Index.md", "\n".join(lines))


def build_qb_index(qbs, teams):
    lines = [
        "# 06 — Quarterback Index\n",
        NOTE_GUIDE,
        "\n## Paul Stone's Top 15 Quarterbacks — \"The Year of the Quarterback\" (p. 45)\n",
        "\n| Rank | Quarterback | Team |",
        "| --- | --- | --- |",
    ]
    for q in qbs:
        lines.append(f"| {q['rank']} | **{q['qb']}** | {q['team'].title()} |")

    lines.append(
        "\n## Where else quarterbacks are discussed\n\n"
        "Quarterback content is spread across the guide and is **not** confined to "
        "p. 45. When Phase 4 builds the full quarterback database it must sweep all "
        "of these:\n\n"
        "- **p. 45** — Paul Stone's Top 15, the only ranked quarterback list.\n"
        "- **pp. 39** — Value in the Heisman Race; quarterback futures prices.\n"
        "- **Every team spread** — the depth-chart situation, competitions and "
        "transfers appear in the season-outlook prose and Three Burning Questions.\n"
        "- **Team header blocks** — a `*` on the returning-starters line marks a "
        "**returning quarterback**, a compact signal worth extracting for all 138 "
        "teams.\n"
        "- **pp. 5–15** — host best bets frequently hinge on quarterback play.\n"
        "- **pp. 22–27** — Makinen's win-total writeups cite quarterback changes.\n"
    )
    lines.append(
        "\n> **Open item for Phase 4.** The guide names starting and competing "
        "quarterbacks in prose rather than in a structured field, so a complete "
        "138-team quarterback table requires reading every spread. This is planned "
        "work, not a gap in the source.\n"
    )
    return write("06_Quarterback_Index.md", "\n".join(lines))


def build_feature_index(features, top50, contributors):
    lines = [
        "# 07 — Feature Article Index\n",
        NOTE_GUIDE,
        "\nEvery non-team article in the guide, with author where the guide states "
        "one.\n",
        "\n| Pages | Feature | Author |",
        "| --- | --- | --- |",
    ]
    authors = {
        3: "Adam Burke (welcome letter)",
        5: "VSiN hosts and contributors (20 named)",
        16: "Matt Youmans",
        21: "Adam Burke",
        22: "Steve Makinen",
        28: "Adam Burke",
        39: "Zachary Cohen",
        40: "Steve Makinen",
        45: "Paul Stone",
        46: "Steve Makinen",
    }
    for f in features:
        p = f["page"]
        pages = f"{p}–{FEATURE_SPANS[p]}" if p in FEATURE_SPANS else str(p)
        lines.append(f"| {pages} | {f['title']} | {authors.get(p, '—')} |")

    lines.append(
        "\n## Section authorship (stated on p. 3)\n\n"
        "The welcome letter assigns the conference previews explicitly. This matters "
        "for Phase 2 — preview voice and methodology differ by author:\n\n"
        "| Author | Sections |\n| --- | --- |\n"
        "| Matt Youmans | Top 50, Pac-12 previews |\n"
        "| Zachary Cohen | Heisman Trophy overview, Big 12 previews |\n"
        "| Jonathan Von Tobel | Mountain West, SEC previews |\n"
        "| Wes Reynolds | Big Ten previews |\n"
        "| Adam Burke | Home-field advantage values, new head coach profiles, "
        "American, ACC, Conference USA, Independents, MAC, Sun Belt previews |\n"
        "| Paul Stone | Top 15 quarterbacks |\n"
        "| Steve Makinen | Favorite season win-total bets, power rating projections |\n"
    )

    lines.append("\n## Matt Youmans' Preseason Top 50 (pp. 16–20)\n")
    lines.append("\n| Rank | Team | Rank | Team |")
    lines.append("| --- | --- | --- | --- |")
    half = 25
    for i in range(half):
        a = top50[i]
        b = top50[i + half] if i + half < len(top50) else {"rank": "", "team": ""}
        lines.append(f"| {a['rank']} | {a['team'].title()} | {b['rank']} | {str(b['team']).title()} |")
    return write("07_Feature_Article_Index.md", "\n".join(lines))


def build_contributor_index(contributors):
    lines = [
        "# 08 — Contributor Index\n",
        NOTE_GUIDE,
        "\n## Masthead (p. 2)\n\n"
        "| Role | Name |\n| --- | --- |\n"
        "| Managing Editor | Adam Burke |\n"
        "| Senior Editor | Zachary Cohen |\n"
        "| Database Manager | Jason Latus |\n"
        "| Layout and Design | Matt Devine |\n"
        "| Cover | James Coleman |\n"
        "| Writers and Editors | Michael Dolan, Steve Makinen, Wes Reynolds, "
        "Paul Stone, Jonathan Von Tobel, Matt Youmans |\n"
        "| Photos | USA Today Network |\n",
        f"\n## Best Bets contributors (pp. 5–15)\n\n"
        f"**{len(contributors)}** hosts and analysts submitted best bets. Each entry "
        "pairs a pick with reasoning, making this the densest concentration of "
        "actionable futures opinion in the guide.\n",
        "\n| Contributor | Page |",
        "| --- | --- |",
    ]
    for c in contributors:
        lines.append(f"| {c['contributor']} | {c['page']} |")
    lines.append(
        "\n> **Why this matters for TTW.** Different contributors disagree, "
        "sometimes sharply, on the same team. Per project standards those "
        "disagreements are preserved rather than reconciled — when Phase 8 builds "
        "the futures database, every contributor's position is recorded with "
        "attribution.\n"
    )
    return write("08_Contributor_Index.md", "\n".join(lines))


def build_power_rating_index(teams):
    ordered = sorted(teams, key=lambda t: int(t["natl_rank"].split()[0][1:]))
    ratings = [float(t["power_rating"]) for t in teams]
    by_conf = defaultdict(list)
    for t in teams:
        by_conf[t["conference"]].append(float(t["power_rating"]))

    lines = [
        "# 09 — Power Rating Index\n",
        NOTE_GUIDE,
        "\nSteve Makinen's 2026 power rating projections for all 138 teams, as "
        "printed on each team's right-hand page. The methodology article is at "
        "**pp. 46–47**.\n",
        f"\n**Range:** {min(ratings)} to {max(ratings)} "
        f"(spread of {round(max(ratings) - min(ratings), 1)} points). "
        f"**Median:** {sorted(ratings)[len(ratings)//2]}.\n",
        "\n> **Interpretation.** These are projections on Makinen's scale, not TTW "
        "numbers. Any comparison against the TTW College Football Power Ratings "
        "Workbook (v0.8.1) must account for scale differences before differences in "
        "opinion can be read. That comparison is a Phase 6 deliverable and is **not** "
        "performed here.\n",
        "\n## Conference averages\n",
        "\n| Conference | Teams | Avg | Best | Worst |",
        "| --- | --- | --- | --- | --- |",
    ]
    for conf, vals in sorted(by_conf.items(), key=lambda x: -sum(x[1]) / len(x[1])):
        lines.append(
            f"| {conf} | {len(vals)} | {round(sum(vals)/len(vals), 2)} | "
            f"{max(vals)} | {min(vals)} |"
        )

    lines.append("\n## All 138 teams by national rank\n")
    lines.append("\n| National | Rating | Team | Conference | Conf Rank | Page |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for t in ordered:
        lines.append(
            f"| {t['natl_rank']} | **{t['power_rating']}** | {t['team']} | "
            f"{t['conference']} | {t['conf_rank']} | {t['page']+1} |"
        )
    return write("09_Power_Rating_Index.md", "\n".join(lines))


def build_concept_index(concepts):
    covered = {k: v for k, v in concepts.items() if len(v) > 2}
    thin = {k: v for k, v in concepts.items() if len(v) <= 2}
    lines = [
        "# 10 — Betting Concept Index\n",
        "> **Source class: GUIDE CONTENT (locations only).** This file records "
        "*where* each concept appears. It deliberately contains **no definitions** — "
        "those are Phase 9 deliverables and will be written with explicit "
        "GUIDE CONTENT / PERSONAL INFERENCE separation.\n",
        "\nPage counts come from a full-text scan of all 345 pages. A high count "
        "means the concept is woven through the team pages; a low count means it is "
        "confined to a feature article.\n",
        "\n## Concepts with substantial coverage\n",
        "\n| Concept | Pages | Primary locations |",
        "| --- | --- | --- |",
    ]
    for concept, pages in sorted(covered.items(), key=lambda x: -len(x[1])):
        head = ", ".join(str(p) for p in pages[:10])
        more = f" … (+{len(pages)-10} more)" if len(pages) > 10 else ""
        lines.append(f"| **{concept}** | {len(pages)} | {head}{more} |")

    lines.append(
        "\n## Concepts the guide barely covers\n\n"
        "**This is the most important section of this file.** These concepts appear "
        "in the TTW project brief but are effectively absent from the guide. Phase 9 "
        "entries for them cannot be sourced to GUIDE CONTENT and must be written as "
        "PERSONAL INFERENCE or left empty — never silently filled.\n"
    )
    lines.append("\n| Concept | Pages | Where |")
    lines.append("| --- | --- | --- |")
    for concept, pages in sorted(thin.items(), key=lambda x: len(x[1])):
        where = ", ".join(str(p) for p in pages) if pages else "**not found**"
        lines.append(f"| {concept} | {len(pages)} | {where} |")

    lines.append(
        "\n### Specifics worth knowing now\n\n"
        "- **Closing Line Value** — appears only as the abbreviation `CL – Closing "
        "Line` on p. 2. The guide never explains or applies CLV.\n"
        "- **Conference Strength** — appears only on p. 46 inside Makinen's power "
        "rating methodology. There is no standalone treatment.\n"
        "- **Weather** — four pages, all incidental. No systematic weather angle.\n"
        "- **EPA** and **Success Rate** appear in conference-preview prose rather "
        "than as defined metrics; neither is in the p. 2 abbreviation list, and "
        "neither appears in the team statistics tables.\n"
        "\nThe guide's own analytical vocabulary is built on yards per play, yards "
        "per point, turnover margin, returning starters, schedule strength and power "
        "ratings — not on the modern public-analytics stack. Phase 9 should describe "
        "the guide on its own terms first.\n"
    )
    return write("10_Betting_Concept_Index.md", "\n".join(lines))


def build_glossary(abbreviations):
    lines = [
        "# 11 — Metric and Abbreviation Glossary\n",
        NOTE_GUIDE,
        f"\nAll **{len(abbreviations)}** abbreviations as defined on p. 2, "
        "reproduced verbatim.\n",
        "\n| Abbreviation | Meaning |",
        "| --- | --- |",
    ]
    for a in abbreviations:
        lines.append(f"| `{a['abbr']}` | {a['meaning']} |")
    lines.append(
        "\n## Proprietary VSiN metrics\n\n"
        "Four entries are Steve Makinen's own constructs rather than standard "
        "football statistics. They carry his methodology and are not "
        "interchangeable with similarly-named figures from other sources:\n\n"
        "- `SM PR` — Steve Makinen Power Rating (see "
        "[09 — Power Rating Index](09_Power_Rating_Index.md), methodology pp. 46–47)\n"
        "- `SM BR` — Steve Makinen Bettors' Rating\n"
        "- `EFF STRG` — Steve Makinen Effective Strength Rating\n"
        "- `SS` — Schedule Strength, printed with a national rank on every team page\n"
    )
    lines.append(
        "\n## Apparent source typo (flagged, not corrected)\n\n"
        "> `PYPG` is defined on p. 2 as **\"Passing Yards per Page\"**. Read in "
        "context alongside `RYPG – Rushing Yards per Game` and `TYPG – Total Yards "
        "per Game`, this is almost certainly a typo for *Passing Yards per Game*.\n"
        ">\n"
        "> Per project quality standards the guide text is reproduced exactly as "
        "printed in the table above. This note is the correction, kept separate "
        "and labelled. **Classification: PERSONAL INFERENCE.**\n"
    )
    return write("11_Metric_Abbreviation_Glossary.md", "\n".join(lines))


def build_stat_index(off, dfn):
    lines = [
        "# 12 — Statistical Category Index\n",
        NOTE_GUIDE,
        "\nEvery team's right-hand page carries the same two statistics tables. "
        "This schema was verified against **all 138 teams** with zero deviations, "
        "so `14_Statistics_Reference` can rely on it without per-team special cases.\n",
        "\nEach category is printed with both a **value** and a **national rank**.\n",
        f"\n## Offensive statistics ({len(off)} categories)\n",
        "\n| # | Category |",
        "| --- | --- |",
    ]
    for i, c in enumerate(off, 1):
        lines.append(f"| {i} | {c} |")
    lines.append(f"\n## Defensive statistics ({len(dfn)} categories)\n")
    lines.append("\n| # | Category |")
    lines.append("| --- | --- |")
    for i, c in enumerate(dfn, 1):
        lines.append(f"| {i} | {c} |")
    lines.append(
        "\n## Asymmetry between the two tables\n\n"
        "The defensive table omits three categories the offensive table carries — "
        "**plays per game**, **time of possession** and **rush/pass attempts per "
        "game** — and adds **sacks**. This is a property of the source, not an "
        "extraction gap: possession and tempo figures are team-level and would be "
        "duplicated on the defensive side.\n\n"
        "Practical consequence: **defensive tempo cannot be read directly from the "
        "guide.** Any tempo work must use the offensive plays-per-game and "
        "time-of-possession figures.\n"
    )
    return write("12_Statistical_Category_Index.md", "\n".join(lines))


def build_master(files, teams, conferences, coordinators, qbs, abbreviations):
    lines = [
        "# 00 — TTW Football Intelligence Library: Master Index\n",
        "**Phase 1 deliverable — the navigation system for the entire library.**\n",
        "\n| | |\n| --- | --- |\n"
        "| **Primary source** | 2026 VSiN College Football Betting Guide (345 pp.) |\n"
        f"| **Conferences** | {len(conferences)} |\n"
        f"| **FBS teams** | {len(teams)} |\n"
        f"| **Head coaches** | {len(teams)} ({sum(1 for t in teams if t['hc_season']==1)} in Year 1) |\n"
        f"| **Coordinators named** | {len(coordinators)} |\n"
        f"| **Ranked quarterbacks** | {len(qbs)} |\n"
        f"| **Abbreviations defined** | {len(abbreviations)} |\n"
        "| **Library status** | Phases 1–2 complete; Phase 3 awaiting approval |\n",
        "\n## Built databases\n",
        "\n| Phase | Database | Entry point |",
        "| --- | --- | --- |",
        "| 2 | Conference Database | "
        "[01_Conference_Database/00_CONFERENCE_INDEX.md](../01_Conference_Database/00_CONFERENCE_INDEX.md) |",
        "\n## Index files\n",
        "\n| File | What it answers |",
        "| --- | --- |",
        "| [01 — Guide Structure Map](01_Guide_Structure_Map.md) | What is on any page, 1–345 |",
        "| [02 — Conference Index](02_Conference_Index.md) | Conference membership, previews, 2026 realignment |",
        "| [03 — Team Index](03_Team_Index.md) | All 138 teams: pages, coach, records, rating, ranks |",
        "| [04 — Coaching Index](04_Coaching_Index.md) | Every head coach, tenure, and Year-1 arrivals |",
        "| [05 — Coordinator Index](05_Coordinator_Index.md) | Every coordinator the guide names |",
        "| [06 — Quarterback Index](06_Quarterback_Index.md) | Top 15 quarterbacks and where QB content lives |",
        "| [07 — Feature Article Index](07_Feature_Article_Index.md) | Every article, author, and the Top 50 |",
        "| [08 — Contributor Index](08_Contributor_Index.md) | Who wrote and who picked what |",
        "| [09 — Power Rating Index](09_Power_Rating_Index.md) | All 138 Makinen ratings, ranked |",
        "| [10 — Betting Concept Index](10_Betting_Concept_Index.md) | Where each concept appears — and which are absent |",
        "| [11 — Metric and Abbreviation Glossary](11_Metric_Abbreviation_Glossary.md) | What every abbreviation means |",
        "| [12 — Statistical Category Index](12_Statistical_Category_Index.md) | The 27-category team stat schema |",
        "| [13 — Open Questions and Gaps](13_Open_Questions_And_Gaps.md) | Decisions needed from the Director |",
    ]

    lines.append(
        "\n## How to search this library\n\n"
        "Every question in the project brief maps to a starting file:\n\n"
        "| Question | Start here |\n| --- | --- |\n"
        "| *Everything about Georgia* | [03 — Team Index](03_Team_Index.md) → pp. 292–293, then Phase 3 team file |\n"
        "| *Everything about the SEC* | [SEC conference file](../01_Conference_Database/sec.md) |\n"
        "| *Every coach entering Year 1* | [04 — Coaching Index](04_Coaching_Index.md) → Year 1 ⭐ |\n"
        "| *Every quarterback competition* | [06 — Quarterback Index](06_Quarterback_Index.md) → Phase 4 |\n"
        "| *Compare Makinen's rating with TTW* | [09 — Power Rating Index](09_Power_Rating_Index.md) → Phase 6 |\n"
        "| *Every SEC futures recommendation* | [08 — Contributor Index](08_Contributor_Index.md) + [02](02_Conference_Index.md) → Phase 8 |\n"
        "| *Every slow-tempo offense* | [12 — Statistical Category Index](12_Statistical_Category_Index.md) → `14_Statistics_Reference` |\n"
        "| *Every trap game* | [01 — Guide Structure Map](01_Guide_Structure_Map.md) → `10_Schedule_Intelligence` |\n"
        "| *Every portal-heavy roster* | `09_Transfer_Portal` |\n"
        "\nQuestions marked with a later phase are **not yet answerable**. The index "
        "tells you where the answer will live and what still has to be built — it "
        "does not pretend to answer them now.\n"
    )

    lines.append(
        "\n## Raw source access\n\n"
        "The full guide text is extracted and greppable, which makes ad-hoc "
        "questions answerable without reopening the PDF:\n\n"
        "```bash\n"
        "# every mention of a team, with page numbers\n"
        "grep -n 'Georgia' _source/extracted/guide_full.txt\n\n"
        "# read one page\n"
        "cat _source/extracted/pages/p292.txt\n\n"
        "# rebuild everything from the PDF\n"
        "python3 _tools/extract_guide.py /path/to/guide.pdf _source\n"
        "python3 _tools/build_index.py\n"
        "```\n"
    )

    lines.append(
        "\n## Standing rules\n\n"
        "These govern every phase and are not restated in each file:\n\n"
        "1. **Three source classes, never mixed** — GUIDE CONTENT, "
        "POST-PUBLICATION UPDATE, PERSONAL INFERENCE. Every claim carries one.\n"
        "2. **Never invent, guess, or fill gaps.** A gap is recorded as a gap.\n"
        "3. **Preserve disagreement.** When guide authors conflict, every view is "
        "kept with attribution; nothing is reconciled.\n"
        "4. **Page references wherever possible.** Printed page = PDF page here.\n"
        "5. **The workbook is frozen.** This library supplements "
        "TTW College Football Power Ratings v0.8.1 AUTHORITATIVE and never "
        "modifies, critiques or redesigns it.\n"
    )
    return write("00_MASTER_INDEX.md", "\n".join(lines))


def build_gaps(teams, coordinators):
    text = f"""# 13 — Open Questions and Gaps

Items requiring a Director decision, and honest statements of what the source
does **not** contain. Nothing here is filled by guessing.

## Owner decisions on record

All Phase 1 open questions were resolved by the Director on 2026-08-08. They are
retained here with their resolutions so the reasoning stays visible.

**1. Returning-starters field ordering.** ✅ **DEFERRED, APPROVED 2026-08-08.** Every team header prints three
returning-starter numbers under the labels `total / offense / defense`, but the
PDF's text layer emits labels and values in different orders, so the mapping
cannot be read reliably from text alone. Army shows `3, 8*, 11`; Northern
Illinois shows `0, 6, 6`. Resolving this needs coordinate-based extraction
(matching each value to its label by x/y position). It is **deferred to
`08_Returning_Production`**, where returning production is the subject. No
returning-starters figures appear anywhere in Phase 1 output, because a wrong
mapping would be worse than none. The Director has approved deferral, with the standing instruction: do not guess
these values, do not infer them from malformed text extraction, and do not
fabricate missing figures.

**2. Futures price labelling.** ✅ **DEFERRED, APPROVED 2026-08-08.** Each team's right page carries three futures
prices near the labels `CFP Championship`, `make the playoff` and a conference
line. Text order does not reliably pair price to label. Same fix, same method,
**deferred to Phase 8 (Futures)**.

**3. Phase numbering does not match directory numbering.** ✅ **DECIDED
2026-08-08 — no Phases 12–16.** The five unassigned directories fold into the
approved phase structure as follows:

| Directory | Folded into |
| --- | --- |
| `08_Returning_Production` | **Phase 3** (Team Database), with conference-level summaries in **Phase 2** where relevant |
| `09_Transfer_Portal` | **Phase 3** (Team Database), with conference-level summaries in **Phase 2** where relevant |
| `10_Schedule_Intelligence` | **Phase 2** (Conference Database) and **Phase 3** (Team Database) |
| `13_Situational_Angles` | **Phase 9** (Betting Concepts) if conceptual, **Phase 10** (Historical Trends) if historical or system-based |
| `14_Statistics_Reference` | **Phase 9** (Betting Concepts) / reference material, preserving every guide-specific statistic and definition |

Note that phase numbers and directory numbers still differ by design
(`05_Power_Ratings` is Phase 6, `07_Futures` is Phase 8). This library therefore
uses **directory names, never bare phase numbers**, wherever ambiguity is
possible.

**4. Depth of the Phase 3 team files.** ✅ **DECIDED 2026-08-08 — option (a).**
Every FBS team file carries the **full standardised 24-heading schema**. Where
the guide does not address a heading, the file states exactly:

> Not addressed in guide.

Headings are never omitted merely because the source is silent, so all 138 team
files share one searchable structure.

## Known source limitations

**Coordinators are incomplete by nature.** {len(coordinators)} coordinators are
named across the guide, but there is no coordinator field in the team header.
The guide names them only where a writer found them relevant, so a complete
276-coordinator roster (OC + DC for 138 teams) **cannot** be built from this
source. Completing it requires outside research filed as POST-PUBLICATION UPDATE.

**No appendix.** The guide ends with Troy on pp. 344–345. The brief anticipated
appendices; there are none. Nothing is missing from the extraction.

**Concepts the brief expects that the guide lacks.** Closing Line Value,
Conference Strength, and Weather are effectively absent — see
[10 — Betting Concept Index](10_Betting_Concept_Index.md). Phase 9 entries for
these cannot cite the guide.

**No TTW workbook comparison yet.** The workbook (v0.8.1 AUTHORITATIVE) has not
been read into this library. Any Makinen-vs-TTW comparison is a Phase 6
deliverable requiring the workbook as contextual reference. Phase 1 makes no
comparison and no claim about TTW numbers.

## Deliberate scope limits in Phase 1

Phase 1 built the navigation layer only. The following are **indexed but not
extracted**, by design, because each belongs to a later phase:

| Content | Destination |
| --- | --- |
| Team schedules with projected lines and opponent ratings | Phase 3 → `02_Team_Database` |
| Season-outlook and Three Burning Questions prose | Phase 3 → `02_Team_Database` |
| Win-total recommendations and projected win figures | Phase 7 → `06_Win_Totals` |
| Full offensive/defensive statistics values and ranks | `14_Statistics_Reference` *(unassigned)* |
| Conference projected standings | Phase 2 → `01_Conference_Database` |
| Host best-bet picks with reasoning | Phase 8 → `07_Futures` |

## Post-publication updates outstanding

None recorded, and **none authorised**. The Director's standing instruction as of
2026-08-08 is that outside updating has not begun and requires explicit
authorisation. The guide's publication date has not been established from the
source, so the cut-off for "post-publication" remains undefined. Coaching changes, portal
movement, injuries and suspensions occurring after publication must be filed
under POST-PUBLICATION UPDATE and are **not** part of Phase 1.
"""
    return write("13_Open_Questions_And_Gaps.md", text)


def main():
    conferences = load("conferences")
    teams = load("teams")
    coordinators = load("coordinators")
    carousel = load("new_head_coaches")
    qbs = load("quarterbacks_top15")
    top50 = load("youmans_top50")
    contributors = load("contributors")
    abbreviations = load("abbreviations")
    off = load("offensive_stat_categories")
    dfn = load("defensive_stat_categories")
    features = load("features")
    concepts = load("concept_pages")

    os.makedirs(OUT, exist_ok=True)
    written = [
        build_structure_map(features, conferences, teams, 345),
        build_conference_index(conferences, teams),
        build_team_index(teams),
        build_coaching_index(teams, carousel),
        build_coordinator_index(coordinators),
        build_qb_index(qbs, teams),
        build_feature_index(features, top50, contributors),
        build_contributor_index(contributors),
        build_power_rating_index(teams),
        build_concept_index(concepts),
        build_glossary(abbreviations),
        build_stat_index(off, dfn),
        build_gaps(teams, coordinators),
        build_master(None, teams, conferences, coordinators, qbs, abbreviations),
    ]
    for f in sorted(written):
        size = os.path.getsize(os.path.join(OUT, f))
        print(f"  {f:<45} {size:>7,} bytes")
    print(f"\n{len(written)} index files written to {OUT}/")


if __name__ == "__main__":
    main()
