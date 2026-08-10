#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 9 renderer
======================================================

Writes three directories:

  11_Betting_Concepts   29 concept entries, one per indexed concept.
  14_Statistics_Reference   the 27-category schema with definitions, and
                        all 138 teams' values and national ranks.
  13_Situational_Angles the conceptual half only; historical and
                        system-based material is Phase 10's.

Every file is generated. Fixes belong here or in _source/concepts/*.json.

The entries deliberately read "what does the guide say, and where does it
stop" rather than "what is this concept". 21 of the 29 are never defined by
the guide at all, and two are barely present in it -- writing those up from
general betting knowledge would put EXTERNAL RESEARCH inside a GUIDE
CONTENT layer, so they carry the sentinel and the gap is reported as the
finding.
"""

import json
import os
import re

from coach_lib import slug
from concept_lib import (BARELY_COVERED, NA, OWNED_BY, SITUATIONAL,
                         abbrev_index, leaders, load_abbreviations,
                         load_concept_pages, load_entries, load_stat_schema,
                         load_team_stats, page_summary)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONCEPTS = os.path.join(ROOT, "11_Betting_Concepts")
STATS = os.path.join(ROOT, "14_Statistics_Reference")
SITU = os.path.join(ROOT, "13_Situational_Angles")

HEAD = ("<!-- GENERATED FILE — do not hand-edit.\n"
        "     Rebuild:  python3 _tools/build_concepts.py\n"
        "     Source:   2026 VSiN College Football Betting Guide -->\n")

MIXED = ("> **Two source classes on this page, never mixed in one claim.** "
         "*How the guide defines it*, *how the guide uses it* and every page "
         "reference are **GUIDE CONTENT**. *Working definition*, *why it "
         "matters* and any arithmetic over printed figures are **TTW "
         "DERIVED** — this library's words, supplied because the guide "
         "supplies none. Where the guide neither defines nor develops a "
         "concept, the field reads `Not addressed in guide.` and is not "
         "padded out.")

GUIDE = ("> **Source class: GUIDE CONTENT.** Every category, value, rank and "
         "abbreviation below is printed in the 2026 VSiN College Football "
         "Betting Guide. No outside research, no post-publication updates.")


def write(d, name, body):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w") as fh:
        fh.write(HEAD + "\n" + body.rstrip() + "\n")
    return name


def cslug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") + ".md"


def f(rec, key):
    return (rec or {}).get(key) or NA


# ------------------------------------------------------------ 11_Betting_Concepts

def concept_page(name, rec, pages, entries, abbr):
    n = len(pages)
    L = [f"# {name}\n", MIXED, "",
         "> Appears on **{} page{}** of 345.{}".format(
             n, "s" if n != 1 else "",
             " A high count usually means the concept is woven through the "
             "138 team tables, not that the guide discusses it that often — "
             "this is a count of locations, not of emphasis." if n > 100
             else ""),
         ""]
    if name in BARELY_COVERED:
        L.append("> ⚠️ **The guide barely covers this.** Phase 1 flagged it as "
                 "present in the TTW brief and effectively absent from the "
                 "guide. The fields below carry the sentinel rather than a "
                 "definition written from outside knowledge. **The gap is the "
                 "finding.**\n")
    L.append("## How the guide defines it\n")
    L.append(f(rec, "guide_definition"))
    L.append("")
    L.append("## How the guide uses it\n")
    L.append(f(rec, "guide_usage"))
    L.append("")
    L.append("## Working definition — TTW DERIVED\n")
    L.append(f(rec, "working_definition"))
    L.append("")
    L.append("## Why it matters — TTW DERIVED\n")
    L.append(f(rec, "why_it_matters"))
    L.append("")
    L.append("## How bettors use it in this guide\n")
    L.append(f(rec, "how_used"))
    L.append("")
    L.append("## Where it appears\n")
    L.append(f"{f(rec, 'key_locations')}\n")
    L.append(f"*Full page list ({n}):* {page_summary(pages)}\n")
    mine = [a for a in rec.get("abbrev", []) if a in abbr]
    if mine:
        L.append("### Abbreviations the guide glosses on p. 2\n")
        L.append("| Abbr | As printed |")
        L.append("| --- | --- |")
        for a in mine:
            L.append(f"| `{a}` | {abbr[a]} |")
        L.append("")
    if f(rec, "caution") != NA:
        L.append("## Caution\n")
        L.append(f(rec, "caution"))
        L.append("")
    L.append("## Related concepts\n")
    rel = []
    for r in rec.get("related", []):
        rel.append(f"[{r}]({cslug(r)})" if r in entries else f"{r}")
    L.append(" · ".join(rel) or NA)
    L.append("")
    if name in OWNED_BY:
        d, fn = OWNED_BY[name]
        L.append("## The database that holds the data\n")
        L.append(f"This entry explains the idea. The figures live in "
                 f"[`{d}`](../{d}/{fn}).\n")
    L.append("## Cross-links\n")
    L.append("- [All concepts](README.md) · "
             "[what the guide never defines](00_GAPS.md) · "
             "[01 — Guide Structure Map](../00_Master_Index/01_Guide_Structure_Map.md)")
    return write(CONCEPTS, cslug(name), "\n".join(L))


def build_concepts(entries, pages, abbr):
    files = [concept_page(n, entries[n], pages[n], entries, abbr)
             for n in sorted(entries)]

    ranked = sorted(pages.items(), key=lambda kv: -len(kv[1]))
    undefined = [n for n in sorted(entries)
                 if f(entries[n], "guide_definition") == NA]
    L = ["# 11 Betting Concepts\n", MIXED, "",
         f"One entry per concept the guide actually contains — "
         f"**{len(entries)}** of them, taken from the Phase 1 concept-to-page "
         f"map and neither added to nor trimmed.", "",
         "## The finding that shapes this directory\n",
         f"**The guide uses far more vocabulary than it defines.** Its only "
         f"glossary is the {len(load_abbreviations())}-entry abbreviation "
         f"list on p. 2, and **{len(undefined)} of the {len(entries)} "
         f"concepts here are never defined by the guide at all** — including "
         f"tempo, regression, explosiveness and situational betting, which it "
         f"nonetheless uses constantly. Each entry therefore keeps *what the "
         f"guide says* apart from *what the term means*, and the second is "
         f"labelled TTW DERIVED wherever it appears.\n",
         "The guide's own analytical vocabulary is built on yards per play, "
         "yards per point, turnover margin, returning starters, schedule "
         "strength and power ratings — not on the modern public-analytics "
         "stack. EPA and success rate appear only in contributor prose, in "
         "neither the glossary nor the statistics tables.\n",
         "## Every concept\n",
         "| Concept | Pages | Guide defines it? | Owned by |",
         "| --- | --- | --- | --- |"]
    for n, ps in ranked:
        d = "yes" if f(entries[n], "guide_definition") != NA else "**no**"
        own = f"`{OWNED_BY[n][0]}`" if n in OWNED_BY else "—"
        flag = " ⚠️" if n in BARELY_COVERED else ""
        L.append(f"| [{n}]({cslug(n)}){flag} | {len(ps)} | {d} | {own} |")
    L.append("\n⚠️ marks the two concepts Phase 1 flagged as effectively "
             "absent from the guide. Their entries carry the sentinel rather "
             "than a definition imported from outside.\n")
    L.append("## Files\n")
    L.append("| File | Content |\n| --- | --- |")
    L.append("| [00_GAPS.md](00_GAPS.md) | what the guide never defines, and "
             "what it barely covers |")
    L.append("| [00_GLOSSARY.md](00_GLOSSARY.md) | all 45 p. 2 abbreviations, "
             "as printed |")
    L.append("\n## Cross-links\n")
    L.append("- [10 — Betting Concept Index](../00_Master_Index/10_Betting_Concept_Index.md) "
             "(locations) · [14 — Statistics Reference](../14_Statistics_Reference/README.md) "
             "· [13 — Situational Angles](../13_Situational_Angles/README.md)")
    files.append(write(CONCEPTS, "README.md", "\n".join(L)))

    L = ["# What the Guide Never Defines\n", MIXED, "",
         "A gap recorded as a gap. This page exists so that a reader never "
         "mistakes this library's working definitions for the guide's, and "
         "never assumes a concept is supported here because it is familiar "
         "elsewhere.", "",
         f"## Used constantly, never defined — {len(undefined)} concepts\n",
         "The guide deploys each of these and explains none of them. The "
         "working definitions in their entries are **TTW DERIVED**.\n",
         "| Concept | Pages | What the guide gives you instead |",
         "| --- | --- | --- |"]
    for n in sorted(undefined, key=lambda n: -len(pages[n])):
        L.append(f"| [{n}]({cslug(n)}) | {len(pages[n])} | "
                 f"{f(entries[n], 'guide_usage')[:150].rstrip()}… |")
    L.append(f"\n## Barely present at all — {len(BARELY_COVERED)} concepts\n")
    L.append("These appear in the TTW project brief and on **one page each** "
             "of the guide. Their entries carry `Not addressed in guide.` "
             "throughout. Filling them from general betting knowledge would "
             "move EXTERNAL RESEARCH into a GUIDE CONTENT layer, which is "
             "precisely what Phase 1 instructed against.\n")
    for n in sorted(BARELY_COVERED):
        L.append(f"- **[{n}]({cslug(n)})** — {f(entries[n], 'key_locations')}")
    L.append("\n## Present in the tables but absent from the glossary\n")
    L.append("**EPA** and **Success Rate** appear in conference-preview prose "
             "only. Neither is in the p. 2 abbreviation list and neither is a "
             "statistics-table category, so neither may be presented as a "
             "guide-defined metric. **Explosiveness** is prose-only too, with "
             "no column, rate or rank anywhere.\n")
    L.append("## A gap in the tables themselves\n")
    L.append("The defensive statistics table omits **plays per game**, **time "
             "of possession** and **rush/pass attempts per game**, which the "
             "offensive table carries, and adds **sacks**. The practical "
             "consequence is that **defensive tempo cannot be read from this "
             "guide at all**.\n")
    L.append("## Cross-links\n")
    L.append("- [All concepts](README.md) · "
             "[glossary](00_GLOSSARY.md) · "
             "[14 — Statistics Reference](../14_Statistics_Reference/README.md)")
    files.append(write(CONCEPTS, "00_GAPS.md", "\n".join(L)))

    L = ["# The Guide's Glossary — p. 2, as printed\n", GUIDE, "",
         f"All **{len(load_abbreviations())}** abbreviations the guide "
         f"defines, in the order printed. This is the guide's *only* "
         f"glossary; every other term in the book is used without "
         f"definition.", "",
         "| Abbr | Meaning as printed |", "| --- | --- |"]
    for a in load_abbreviations():
        note = ""
        if a["abbr"] == "PYPG":
            note = " ⚠️"
        L.append(f"| `{a['abbr']}` | {a['meaning']}{note} |")
    L.append("\n⚠️ The guide prints **`PYPG – Passing Yards per Page`**. "
             "Read in context with `RYPG – Rushing Yards per Game` and "
             "`TYPG – Total Yards per Game`, this is plainly a typo for "
             "*Game*. It is reproduced exactly as printed and is **not** "
             "silently corrected.\n")
    L.append("## Cross-links\n")
    L.append("- [All concepts](README.md) · "
             "[11 — Metric and Abbreviation Glossary](../00_Master_Index/11_Metric_Abbreviation_Glossary.md)")
    files.append(write(CONCEPTS, "00_GLOSSARY.md", "\n".join(L)))
    return files, undefined


# --------------------------------------------------------- 14_Statistics_Reference

def build_statistics(stats, abbr):
    off, deff = load_stat_schema()
    notes = json.load(open(os.path.join(ROOT, "_source", "statistics",
                                        "category_notes.json")))
    files = []
    L = ["# 14 Statistics Reference\n", GUIDE, "",
         f"The guide's team statistics: **{len(off)} offensive** and "
         f"**{len(deff)} defensive** categories, each with a value and a "
         f"national rank out of {len(stats)}, for **136** of the "
         f"**{len(stats)}** teams — **{136 * (len(off) + len(deff)):,}** "
         f"printed figures. The two teams promoted from FCS carry the "
         f"headings and an explicit notice instead of values; see below.", "",
         "> **Status corrected.** This directory long carried a note saying "
         "the values could not yet be extracted. Phase 3 resolved them; the "
         "schema and the values are both verified, and that stale status is "
         "withdrawn.", "",
         "## The schema\n",
         "| # | Offensive category | Defensive category |",
         "| --- | --- | --- |"]
    for i in range(max(len(off), len(deff))):
        a = off[i] if i < len(off) else "—"
        b = deff[i] if i < len(deff) else "—"
        L.append(f"| {i + 1} | {a} | {b} |")
    L.append("\n## The asymmetry between the two tables\n")
    L.append("The defensive table omits three categories the offensive table "
             "carries — **plays per game**, **time of possession** and "
             "**rush/pass attempts per game** — and adds **sacks**. This is a "
             "property of the source, not an extraction gap: possession and "
             "tempo figures are team-level and would simply be duplicated on "
             "the defensive side.\n")
    L.append("**Practical consequence: defensive tempo cannot be read "
             "directly from this guide.** Any tempo work has to use the "
             "offensive plays-per-game and time-of-possession figures.\n")
    L.append("## Categories the guide defines\n")
    L.append("| Category | p. 2 abbreviation | As printed |")
    L.append("| --- | --- | --- |")
    pairs = [("POINTS PER GAME", "PPG"), ("YARDS PER PLAY", "YPP"),
             ("YARDS PER POINT", "YPPT"), ("TOTAL YARDS PER GAME", "TYPG"),
             ("PASSING YARDS PER GAME", "PYPG"),
             ("RUSH YARDS PER GAME", "RYPG"),
             ("YARDS PER RUSH ATTEMPT", "YPR"), ("TURNOVERS", "TO")]
    for cat, ab in pairs:
        L.append(f"| {cat} | `{ab}` | {abbr.get(ab, NA)} |")
    L.append(f"\nThe remaining categories are printed as column headings and "
             f"never glossed.\n")
    fcs = sorted(t for t, v in stats.items()
                 if not v["stats"].get("offense") and not v["stats"].get("defense"))
    L.append("## Two teams with no statistics, and the guide says why\n")
    L.append(f"**{' and '.join(fcs)}** carry the table headings with no "
             f"values. In place of both tables the guide prints "
             f"**`PARTICIPATED IN FCS IN 2025`** — twice, once for each side "
             f"of the ball. Both programmes moved up for 2026, so there are "
             f"no FBS figures to print.\n")
    L.append(f"This is an explicit, reasoned absence in the source, not an "
             f"extraction gap. It is recorded as printed and never filled "
             f"from FCS statistics or from anywhere else. The printed total "
             f"is therefore "
             f"**{(len(stats) - len(fcs)) * (len(off) + len(deff)):,}** "
             f"figures across {len(stats) - len(fcs)} teams, not "
             f"{len(stats) * (len(off) + len(deff)):,}.\n")
    L.append("## A note on yards per point\n")
    L.append(f(notes.get("YARDS PER POINT"), "working_definition"))
    L.append("")
    L.append(f(notes.get("YARDS PER POINT"), "caution"))
    L.append("")
    L.append("## Files\n")
    L.append("| File | Content |\n| --- | --- |")
    L.append("| [00_OFFENSE.md](00_OFFENSE.md) | all 138 teams × 15 offensive categories |")
    L.append("| [00_DEFENSE.md](00_DEFENSE.md) | all 138 teams × 12 defensive categories |")
    L.append("| [00_LEADERS.md](00_LEADERS.md) | who the guide ranks first in each category |")
    L.append("\n## Cross-links\n")
    L.append("- [12 — Statistical Category Index](../00_Master_Index/12_Statistical_Category_Index.md) "
             "· [11 — Betting Concepts](../11_Betting_Concepts/README.md) "
             "· team files in [`02_Team_Database`](../02_Team_Database/README.md)")
    files.append(write(STATS, "README.md", "\n".join(L)))

    for side, cats, fn, label in (("offense", off, "00_OFFENSE.md", "Offensive"),
                                  ("defense", deff, "00_DEFENSE.md", "Defensive")):
        L = [f"# {label} Statistics — all 138 teams\n", GUIDE, "",
             f"{len(cats)} categories, value and national rank as printed on "
             f"each team's right-hand page.", "",
             "| Team | " + " | ".join(c.title() for c in cats) + " |",
             "| --- | " + " | ".join("---" for _ in cats) + " |"]
        for team in sorted(stats):
            row = {r["category"]: r for r in stats[team]["stats"].get(side, [])}
            if not row:
                # The guide prints this in place of both tables for the two
                # programmes promoted from FCS. Reproduced, never filled in.
                L.append(f"| [{team}](../02_Team_Database/{slug(team)}) | "
                         + " | ".join(["*PARTICIPATED IN FCS IN 2025*"]
                                      + ["—"] * (len(cats) - 1)) + " |")
                continue
            cells = []
            for c in cats:
                r = row.get(c)
                cells.append(f"{r['value']} (#{r['rank']})" if r and r.get("rank")
                             else (r["value"] if r else "—"))
            L.append(f"| [{team}](../02_Team_Database/{slug(team)}) | "
                     + " | ".join(cells) + " |")
        L.append("\n## Cross-links\n")
        L.append("- [Statistics Reference](README.md) · [leaders](00_LEADERS.md)")
        files.append(write(STATS, fn, "\n".join(L)))

    L = ["# Category Leaders — as the guide ranks them\n", GUIDE, "",
         "> The ranks below are **the guide's own printed national ranks**, "
         "not a TTW re-derivation. This page is a lookup over figures the "
         "guide prints, and rank #1 means whatever the guide meant by it — "
         "note that for yards per point a low value is good on offense, so "
         "the printed rank, not the raw value, is the thing to read.", ""]
    for side, cats, label in (("offense", off, "Offense"),
                              ("defense", deff, "Defense")):
        L.append(f"## {label}\n")
        L.append("| Category | #1 | #2 | #3 |")
        L.append("| --- | --- | --- | --- |")
        for c in cats:
            top = leaders(stats, side, c, 3)
            cells = [f"{t} — {v}" for _, t, v in top]
            while len(cells) < 3:
                cells.append("—")
            L.append(f"| {c.title()} | " + " | ".join(cells) + " |")
        L.append("")
    L.append("## Cross-links\n")
    L.append("- [Statistics Reference](README.md) · [offense](00_OFFENSE.md) "
             "· [defense](00_DEFENSE.md)")
    files.append(write(STATS, "00_LEADERS.md", "\n".join(L)))
    return files


# ---------------------------------------------------------- 13_Situational_Angles

def build_situational(entries, pages):
    L = ["# 13 Situational Angles\n", MIXED, "",
         "The **conceptual half only.** The standing decision for this "
         "directory splits it: conceptual material is Phase 9, and historical "
         "or system-based material — hit rates, backtested spots, trend "
         "records — is Phase 10. Nothing of that kind is constructed here.", "",
         "## What the guide actually has\n",
         "| Concept | Pages | Status in the guide |",
         "| --- | --- | --- |"]
    for n in SITUATIONAL:
        d = "defined on p. 2" if f(entries[n], "guide_definition") != NA \
            else "**used but never defined**"
        L.append(f"| [{n}](../11_Betting_Concepts/{cslug(n)}) | "
                 f"{len(pages[n])} | {d} |")
    L.append("\n## How the guide reasons situationally\n")
    L.append(f(entries["Situational Betting"], "how_used"))
    L.append("")
    L.append(f(entries["Situational Betting"], "guide_usage"))
    L.append("")
    L.append("## The two things that are genuinely missing\n")
    L.append("**Weather.** Four incidental mentions across 345 pages. There "
             "is no systematic weather angle in this guide, and none is "
             "constructed here.\n")
    L.append("**Any measured travel figure.** Travel is named as a factor "
             "feeding home-field advantage on p. 21 and argued in prose where "
             "realignment bites, but no mileage, time-zone count or rest "
             "differential is printed anywhere.\n")
    L.append("## Where the measurable part lives\n")
    L.append("The one situational factor the guide does quantify is "
             "home-field advantage, and it does so per team rather than as a "
             "league constant — a home field rating and a road field rating "
             "for all 138 teams, which is what converts a power rating into a "
             "projected line. Those figures live in "
             "[`05_Power_Ratings`](../05_Power_Ratings/00_MAKINEN_RATINGS.md) "
             "and in every conference table.\n")
    L.append("## Cross-links\n")
    L.append("- [Situational Betting](../11_Betting_Concepts/situational_betting.md) "
             "· [Travel](../11_Betting_Concepts/travel.md) "
             "· [Weather](../11_Betting_Concepts/weather.md) "
             "· [Home-Field Advantage](../11_Betting_Concepts/home_field_advantage.md)")
    return [write(SITU, "README.md", "\n".join(L))]


def main():
    entries = load_entries()
    pages = load_concept_pages()
    abbr = abbrev_index()
    stats = load_team_stats()

    cfiles, undefined = build_concepts(entries, pages, abbr)
    sfiles = build_statistics(stats, abbr)
    qfiles = build_situational(entries, pages)

    off, deff = load_stat_schema()
    print(f"11_Betting_Concepts    {len(cfiles)} files, {len(entries)} concepts")
    print(f"  never defined by the guide   {len(undefined)}")
    print(f"  barely covered (sentinel)    {len(BARELY_COVERED)}")
    print(f"14_Statistics_Reference {len(sfiles)} files, "
          f"{len(stats)} teams x {len(off) + len(deff)} categories = "
          f"{len(stats) * (len(off) + len(deff)):,} figures")
    print(f"13_Situational_Angles   {len(qfiles)} file, "
          f"{len(SITUATIONAL)} concepts routed")


if __name__ == "__main__":
    main()
