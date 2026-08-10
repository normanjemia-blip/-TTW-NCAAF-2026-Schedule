#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 10 renderer
======================================================

Writes 12_Historical_Trends/ and completes 13_Situational_Angles/ with the
historical half Phase 9 deferred here.

Everything on these pages is a record the guide prints. Nothing is
backtested, recomputed, extended or projected: the library holds no
game-level historical data, which is exactly what the auxiliary
calibration study established. Where a printed percentage and a printed
record do not agree, both are shown and neither is adjusted.
"""

import json
import os
import re

from coach_lib import slug

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "12_Historical_Trends")
SITU = os.path.join(ROOT, "13_Situational_Angles")
DATA = os.path.join(ROOT, "_source", "data")

NA = "Not addressed in guide."

HEAD = ("<!-- GENERATED FILE — do not hand-edit.\n"
        "     Rebuild:  python3 _tools/build_trends.py\n"
        "     Source:   2026 VSiN College Football Betting Guide -->\n")

GUIDE = ("> **Source class: GUIDE CONTENT.** Every record, percentage, span "
         "and threshold below is printed in the 2026 VSiN College Football "
         "Betting Guide and is reproduced as printed. **Nothing here is "
         "backtested, recomputed, extended or projected** — this library "
         "holds no game-level historical data and does not manufacture any. "
         "Grouping trends into angles, and any check of a printed record "
         "against its printed percentage, are **TTW DERIVED** and labelled "
         "where they appear.")


def write(d, name, body):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w") as fh:
        fh.write(HEAD + "\n" + body.rstrip() + "\n")
    return name


def load():
    raw = json.load(open(os.path.join(DATA, "trends_raw.json")))
    angles = {}
    d = os.path.join(ROOT, "_source", "trends")
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".json"):
            for k, v in json.load(open(os.path.join(d, fn))).items():
                if k in angles:
                    raise SystemExit(f"duplicate angle {k!r}")
                angles[k] = v
    teams = json.load(open(os.path.join(DATA, "team_details.json")))
    return raw, angles, teams


def pp(pages):
    return f"p. {pages[0]}" if len(pages) < 2 or pages[0] == pages[1] \
        else f"pp. {pages[0]}–{pages[1]}"


def build_stability(raw, angles):
    s = angles["stability_system"]
    comps = raw["components"]
    sysrec = {x["label"]: x for x in raw["systems"]}
    play_on = sysrec["College Football Stability System — PLAY ON rule"]
    fade = sysrec["College Football Stability System — FADE rule"]
    long_run = play_on
    last = sysrec["College Football Stability System — 2025 season"]
    fade_last = sysrec.get("FADE rule — 2025 season")
    losing = sysrec.get("Revised Stability Score Edge System — losing seasons")

    L = [f"# {s['title']} — {pp(s['pages'])}\n", GUIDE, "",
         f"*{s['author']}.* The guide's only fully specified betting system, "
         f"and the one it supplies the most historical evidence for.", "",
         "## The revised system is two rules, each with its own record\n",
         "Makinen calls this his *official new College Football Stability "
         "System(s)* — plural. Both rules apply to non-conference games in "
         "the first four weeks, and both exclude games with a point spread "
         "of -30 or higher for either team.\n",
         "| Rule | Condition | Record as printed | ATS % | Span |",
         "| --- | --- | --- | --- | --- |",
         f"| **PLAY ON** | {play_on['condition']} | {play_on['su_record']} SU, "
         f"{play_on['ats_record']} ATS | {play_on['ats_pct_printed']}% | "
         f"{play_on['span']} |",
         f"| **FADE** | {fade['condition']} | {fade['su_record']} SU, "
         f"{fade['ats_record']} ATS | {fade['ats_pct_printed']}% | "
         f"{fade['span']} |", "",
         "## And what each did last season\n",
         "| | 2025 |", "| --- | --- |",
         f"| System as run in 2025 | **{last['ats_record']} ATS** |",
         f"| FADE angle | **{fade_last['ats_record']} ATS** |"
         if fade_last else "",
         (f"| Losing seasons, {losing['span']} | only two, one of them 2025 |"
          if losing else ""), "",
         f"> ⚠️ **{s['caution']}**\n",
         "## What happened in 2025, in the guide's own account\n",
         s["the_2025_result"], "",
         "## What he changed\n", s["what_he_changed"], "",
         "## The premise\n", s["premise"], "",
         f"**Window.** {s['window']}\n",
         f"**Scope.** {s['scope_limits']}\n",
         f"**Transfer quarterbacks.** {s['qb_transfer_rule']}\n",
         "## The six components — first four weeks, since 2021\n",
         "Each row compares a class of team against its opposite. FBS vs. "
         "FBS games only.\n",
         "| Class of team | SU | ATS | ATS % as printed | Compared against |",
         "| --- | --- | --- | --- | --- |"]
    for c in sorted(comps, key=lambda c: -(c["ats_pct_printed"] or 0)):
        L.append(f"| {c['subject']} | {c['su_record']} | {c['ats_record']} | "
                 f"{c['ats_pct_printed']}% | {c['comparison'] or NA} |")
    L.append("")
    L.append("Makinen's own reading of this table is that new head coaches, "
             "new defensive coordinators and many returning starters are the "
             "most impactful offseason developments.\n")
    if raw["percentage_mismatches"]:
        L.append("### A printed percentage that does not reconcile — "
                 "TTW DERIVED check\n")
        L.append("| Row | ATS record | Printed | Recomputed |")
        L.append("| --- | --- | --- | --- |")
        for m in raw["percentage_mismatches"]:
            L.append(f"| {m['subject']} | {m['ats_record']} | "
                     f"{m['printed_pct']}% | {m['recomputed_pct']}% |")
        L.append(f"\n{raw['percentage_mismatches'][0]['note']} The difference "
                 f"is a rounding direction, not a substantive disagreement, "
                 f"and the printed figure is what the guide stands behind.\n")
    if raw["printed_typos"]:
        L.append("### A printed slip, reproduced\n")
        for t in raw["printed_typos"]:
            L.append(f"The bullet for **{t['subject']}** compares them "
                     f"against *{t['printed_comparison']}*. {t['note']}\n")
    L.append("## Cross-links\n")
    L.append("- [All angles](00_BY_ANGLE.md) · "
             "[Coaching Database](../03_Coaching_Database/README.md) · "
             "[Betting Concepts → Historical Angles]"
             "(../11_Betting_Concepts/historical_angles.md)")
    return write(OUT, "00_STABILITY_SYSTEM.md", "\n".join(L))


def build_angles(angles):
    others = {k: v for k, v in angles.items() if k != "stability_system"}
    L = ["# Historical Angles — by angle\n", GUIDE, "",
         f"**{len(others)} angles** beyond the Stability System, each a "
         f"historical claim the guide argues from. Where the guide prints a "
         f"denominator it is given; where it does not, that is stated rather "
         f"than estimated.", "",
         "| Angle | Author | Span | Sample | Pages |",
         "| --- | --- | --- | --- | --- |"]
    for k, a in sorted(others.items(), key=lambda kv: -(kv[1].get("denominator") or 0)):
        den = a.get("denominator")
        L.append(f"| [{a['title']}](#{re.sub(r'[^a-z0-9]+', '-', a['title'].lower()).strip('-')}) "
                 f"| {a['author']} | {a['span']} | "
                 f"{den if den else '*not printed*'} | {pp(a['pages'])} |")
    L.append("")
    for k, a in sorted(others.items(), key=lambda kv: -(kv[1].get("denominator") or 0)):
        L.append(f"## {a['title']}\n")
        L.append(f"*{a['author']}, {pp(a['pages'])}.*\n")
        L.append("**As printed.** " + a["statement_as_printed"] + "\n")
        den = a.get("denominator")
        L.append(f"| | |\n| --- | --- |")
        L.append(f"| Span | {a['span']} |")
        L.append(f"| Sample the guide prints | {den if den else '*none printed*'} |")
        applied = a.get("applied_to") or []
        L.append(f"| Teams the guide applies it to | "
                 f"{', '.join(f'[{t}](../02_Team_Database/{slug(t)})' for t in applied) if applied else '*stated as a general angle*'} |")
        L.append("")
        if a.get("caution") and a["caution"] != NA:
            L.append(f"*Caution:* {a['caution']}\n")
    L.append("## Cross-links\n")
    L.append("- [Stability System](00_STABILITY_SYSTEM.md) · "
             "[by team](00_BY_TEAM.md) · "
             "[the register](00_TREND_REGISTER.md)")
    return write(OUT, "00_BY_ANGLE.md", "\n".join(L))


def build_by_team(angles, teams):
    applied = {}
    for k, a in angles.items():
        for t in a.get("applied_to", []):
            applied.setdefault(t, []).append(a["title"])
    L = ["# Historical Angles — by team\n", GUIDE, "",
         "Only teams the guide **explicitly** attaches an angle to appear "
         "here. A system describes a class of team; applying it to a "
         "programme the guide does not name would be inventing a claim, so "
         "this list is short by design.", "",
         "| Team | Angles the guide applies |", "| --- | --- |"]
    for t in sorted(applied):
        L.append(f"| [{t}](../02_Team_Database/{slug(t)}) | "
                 f"{'; '.join(applied[t])} |")
    L.append(f"\n**{len(applied)} of 138 teams.** The remaining "
             f"{138 - len(applied)} carry no angle the guide names them "
             f"under. That absence is recorded, not filled.\n")
    L.append("## Last-season records — all 138 teams\n")
    L.append("> These are one season's results, not trends. They come from "
             "Phase 3 and are reproduced here for reference because the "
             "guide prints them in every team's header block.\n")
    L.append("| Team | 2025 SU | 2025 ATS | 2025 O/U |")
    L.append("| --- | --- | --- | --- |")
    for t in sorted(teams, key=lambda t: t["team"]):
        L.append(f"| [{t['team']}](../02_Team_Database/{slug(t['team'])}) | "
                 f"{t.get('su_2025') or NA} | {t.get('ats_2025') or NA} | "
                 f"{t.get('ou_2025') or NA} |")
    L.append("\n## Cross-links\n")
    L.append("- [By angle](00_BY_ANGLE.md) · "
             "[Team Database](../02_Team_Database/README.md)")
    return write(OUT, "00_BY_TEAM.md", "\n".join(L))


def build_register(raw):
    recs = raw["narrative_records"]
    by_page = {}
    for r in recs:
        by_page.setdefault(r["page"], []).append(r)
    L = ["# The Trend Register — every historical claim, by page\n", GUIDE, "",
         f"**{len(recs)} historical claims** across "
         f"**{len(by_page)}** of the {len(raw['historical_pages'])} pages "
         f"Phase 1 flagged as carrying them, each captured with the span "
         f"phrase that makes it historical.", "",
         "> This is a register, not a curated list. A claim appears here "
         "because the guide makes it, whether or not it supports a bet. "
         "Team-page header blocks — one season's SU/ATS/O-U for all 138 "
         "teams — are **excluded**: they are results, not trends, and Phase "
         "3 already holds them.", ""]
    for p in sorted(by_page):
        L.append(f"### p. {p}\n")
        for r in by_page[p]:
            rec = f" **{r['record']}**" if r.get("record") else ""
            L.append(f"- *({r['span_phrase']})*{rec} {r['sentence']}")
        L.append("")
    L.append("## Cross-links\n")
    L.append("- [By angle](00_BY_ANGLE.md) · "
             "[Stability System](00_STABILITY_SYSTEM.md)")
    return write(OUT, "00_TREND_REGISTER.md", "\n".join(L))


def build_readme(raw, angles, teams):
    others = {k: v for k, v in angles.items() if k != "stability_system"}
    L = ["# 12 Historical Trends\n", GUIDE, "",
         "Every historical betting trend and long-run pattern the guide "
         "cites, indexed by angle and by team.", "",
         "## What is here\n",
         "| File | Content |", "| --- | --- |",
         "| [00_STABILITY_SYSTEM.md](00_STABILITY_SYSTEM.md) | the guide's "
         "one fully specified system, its 6 components, its long-run record "
         "**and its 2025 failure** |",
         f"| [00_BY_ANGLE.md](00_BY_ANGLE.md) | {len(others)} further angles, "
         f"with the samples the guide prints |",
         "| [00_BY_TEAM.md](00_BY_TEAM.md) | teams the guide names under an "
         "angle, plus all 138 last-season records |",
         f"| [00_TREND_REGISTER.md](00_TREND_REGISTER.md) | all "
         f"{len(raw['narrative_records'])} claims, by page |",
         "",
         "## The constraint that defines this phase\n",
         "**Nothing here is backtested.** The library has no game-level "
         "historical data — the auxiliary calibration study established that "
         "no season pairs a VSiN preseason rating with played games — so "
         "every record on these pages is one the guide printed, quoted with "
         "its span and its page. No hit rate is computed, no sample "
         "extended, no system re-run.\n",
         "The one arithmetic this phase does perform is a **reconciliation "
         "check**: does a printed record agree with its own printed "
         "percentage? That is labelled TTW DERIVED, reported where it fails, "
         "and never applied as a correction.\n",
         "## What the guide gives you, and what it does not\n",
         "It supplies denominators more often than most betting publications "
         "do — 141 teams, 33 teams, 21 teams, 43 teams — which is what makes "
         "these angles checkable in principle. What it rarely supplies is "
         "what happened to the rest of the sample, or how 'got worse' is "
         "measured.\n",
         "And it is candid about failure. The Stability System's long-run "
         "record is 55.4% since 2013; last season it went **30-36 ATS**, and "
         "the guide leads with that rather than burying it. Both figures "
         "travel together everywhere in this directory.\n",
         "## Cross-links\n",
         "- [13 — Situational Angles](../13_Situational_Angles/README.md) · "
         "[11 — Betting Concepts](../11_Betting_Concepts/historical_angles.md) "
         "· [Coaching Database](../03_Coaching_Database/README.md) · "
         "[Win Totals](../06_Win_Totals/README.md)"]
    return write(OUT, "README.md", "\n".join(L))


MARKER = "## The historical and system-based half — Phase 10"


def build_situational(raw, angles):
    """Phase 9 built the conceptual half. This completes the directory.

    Idempotent in both directions: everything from MARKER onward is
    discarded before the section is rewritten, so running this twice, or
    running it after build_concepts.py regenerates the conceptual half,
    both produce the same file.
    """
    path = os.path.join(SITU, "README.md")
    body = open(path).read()
    if MARKER in body:
        body = body[:body.index(MARKER)].rstrip()
        body = body.rstrip("-").rstrip()
    # The file is now written by two builders. Update the rebuild banner and
    # retire the Phase 9 sentence that says the historical half does not
    # exist, which Phase 10 has since made false.
    BANNER_ONE = "     Rebuild:  python3 _tools/build_concepts.py"
    BANNER_TWO = BANNER_ONE + " && python3 _tools/build_trends.py"
    if BANNER_TWO not in body:
        body = body.replace(BANNER_ONE, BANNER_TWO, 1)
    body = body.replace(
        "The **conceptual half only.** The standing decision for this "
        "directory splits it: conceptual material is Phase 9, and historical "
        "or system-based material — hit rates, backtested spots, trend "
        "records — is Phase 10. Nothing of that kind is constructed here.",
        "**Both halves are now built.** The standing decision for this "
        "directory split it: conceptual material in Phase 9, and historical "
        "or system-based material — hit rates, backtested spots, trend "
        "records — in Phase 10. The conceptual half is below; the historical "
        "half is at the foot of this page, with the detail in "
        "[`12_Historical_Trends`](../12_Historical_Trends/README.md).")
    add = [
        "", "---", "",
        MARKER + "\n",
        "Phase 9 deferred hit rates, backtested spots and trend records to "
        "Phase 10. They are now built, and the honest summary is that the "
        "guide has **far less situational history than situational prose**.\n",
        "The one situational family the guide supports with historical "
        "evidence is **offseason transition**, not game context: new head "
        "coaches, new coordinators, new quarterbacks and returning-starter "
        "counts, all measured over the first four weeks of a season since "
        "2021. Those live in "
        "[the Stability System](../12_Historical_Trends/00_STABILITY_SYSTEM.md).\n",
        "For the classic situational spots — rest advantages, look-ahead and "
        "letdown games, short weeks, travel and time zones — **the guide "
        "prints no hit rate, no sample and no historical record anywhere**. "
        "Contributors argue them game by game, as Phase 9 documented. That "
        "absence is the finding, and no rate has been constructed to fill "
        "it.\n",
        "| Situational angle | Historical evidence in the guide |",
        "| --- | --- |",
        "| Look-ahead and letdown spots | *none printed* |",
        "| Rest and short weeks | *none printed* |",
        "| Travel and time zones | *none printed* |",
        "| Weather | *none printed* |",
        "| Home-field advantage | quantified per team as a field rating, but "
        "no hit rate is printed |",
        "| Offseason transition | **yes** — six component records since 2021, "
        "plus the system's own record since 2013 |",
        "",
        "## Cross-links\n",
        "- [12 — Historical Trends](../12_Historical_Trends/README.md) · "
        "[Stability System](../12_Historical_Trends/00_STABILITY_SYSTEM.md)",
    ]
    with open(path, "w") as fh:
        fh.write(body.rstrip() + "\n" + "\n".join(add) + "\n")
    return "README.md"


def main():
    raw, angles, teams = load()
    files = [build_readme(raw, angles, teams),
             build_stability(raw, angles),
             build_angles(angles),
             build_by_team(angles, teams),
             build_register(raw)]
    build_situational(raw, angles)
    applied = {t for a in angles.values() for t in a.get("applied_to", [])}
    print(f"12_Historical_Trends   {len(files)} files")
    print(f"  angles authored      {len(angles)} "
          f"(1 system + {len(angles) - 1} angles)")
    print(f"  stability components {len(raw['components'])}")
    print(f"  register entries     {len(raw['narrative_records'])} across "
          f"{len({r['page'] for r in raw['narrative_records']})} pages")
    print(f"  teams named          {len(applied)} of {len(teams)}")
    print(f"13_Situational_Angles  historical half appended")


if __name__ == "__main__":
    main()
