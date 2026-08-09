#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phases 5B-5F
=================================================

Builds the searchable indexes that sit on top of the 138 Phase 5A records:

  5B  00_COACH_DIRECTORY.md        head coaches and coordinators, searchable
  5C  00_CONTINUITY_MATRIX.md      the printed Stability Score components, 138 rows
  5D  00_NEW_HEAD_COACHES.md       + six more change indexes
  5E  00_QB_COACHING_CROSSLINK.md  quarterback situation against staff situation
  5F  00_SOURCE_CONFLICTS.md       every place the guide contradicts itself

Everything here is GUIDE CONTENT. Three rules are enforced by construction:

  * The continuity matrix reproduces Steve Makinen's printed components and
    totals. It never recomputes, re-weights or substitutes a TTW score.
  * The change indexes carry the guide's own assessment alongside every
    change. Change is not labelled positive or negative by this library.
  * The QB cross-link is an intelligence index. It states what the guide
    says about the quarterback and what it says about the staff, and makes
    no claim that any combination produces market value unless the guide
    makes that argument itself, in which case the guide is quoted.

Phase 4 is read, never written.

Usage:  python3 _tools/build_coaching_indexes.py
"""

import glob
import json
import os
import re
from collections import defaultdict

from coach_lib import (NA, coaching_conflicts, load_carousel, load_details,
                       load_notes, load_stability, load_teams, slug)

OUT = "03_Coaching_Database"
HEADER = ("<!-- GENERATED FILE — do not hand-edit.\n"
          "     Rebuild:  python3 _tools/build_coaching_indexes.py\n"
          "     Source:   2026 VSiN College Football Betting Guide -->\n")

SOURCE_LINE = (
    "> **Source: 2026 VSiN College Football Betting Guide.** GUIDE CONTENT "
    "throughout — no outside research and no post-publication updates. "
    "Continuity readings come from Steve Makinen's printed Stability Score "
    "table (pp. 41–44), reproduced exactly; this library does not recompute "
    "or re-weight it.")


def ordinal(n):
    return f"{n}{'st' if n == 1 else 'nd' if n == 2 else 'rd' if n == 3 else 'th'}"


def link(team):
    return f"[{team}]({slug(team)})"


def first_sentence(text, limit=240):
    """One sentence of the guide's assessment, for index rows."""
    if not text or text == NA:
        return NA
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    out = parts[0]
    for p in parts[1:]:
        if len(out) >= 110:
            break
        out += " " + p
    return out if len(out) <= limit else out[:limit].rsplit(" ", 1)[0] + "…"


def write(name, lines):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(HEADER + "\n" + "\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# 5B — Coach Directory
# ---------------------------------------------------------------------------
def directory(rows, notes, carousel):
    L = [f"# Coach Directory — 2026", "", SOURCE_LINE, "",
         "Every head coach and every coordinator the guide names, searchable by "
         "name, by programme and by conference. The assessment column is a "
         "pointer, not a summary: the full record lives in the programme file.",
         ""]

    L += ["## Head coaches", "",
          "| Coach | Team | Conference | Season | New / returning | Coaching Carousel |",
          "| --- | --- | --- | --- | --- | --- |"]
    for r in sorted(rows, key=lambda x: x["head_coach"].split()[-1]):
        car = (f"p. {r['carousel_page']}" if r["carousel_page"] else "—")
        L.append(f"| **{r['head_coach']}**{' *(interim)*' if r['interim'] else ''} "
                 f"| {link(r['team'])} | {r['conference']} | "
                 f"{ordinal(r['hc_season'])} | "
                 f"{'**New**' if r['new_hc'] else 'Returning'} | {car} |")
    L.append("")

    for role, key, flagkey, label in (
            ("Offensive coordinators", "oc", "new_oc", "OC"),
            ("Defensive coordinators", "dc", "new_dc", "DC")):
        named = [r for r in rows if r[key] != NA]
        L += [f"## {role}", "",
              f"The guide names {len(named)} of 138. Where it does not, the "
              f"programme file records `{NA}` and the Stability Score column is "
              f"still reproduced.", "",
              f"| {label} | Team | Conference | New / returning |",
              "| --- | --- | --- | --- |"]
        for r in sorted(named, key=lambda x: x[key]):
            name = r[key].split(",")[0].split(" — ")[0].rstrip(".")
            L.append(f"| **{name}** | {link(r['team'])} | {r['conference']} | "
                     f"{'**New**' if r[flagkey] else 'Returning'} |")
        L.append("")

    pc = [r for r in rows if r["play_caller"] != NA]
    L += ["## Play-callers", "",
          f"The guide identifies the play-caller, or a change of play-caller, "
          f"for {len(pc)} programmes.", "",
          "| Team | Conference | What the guide says |",
          "| --- | --- | --- |"]
    for r in sorted(pc, key=lambda x: x["team"]):
        L.append(f"| {link(r['team'])} | {r['conference']} | "
                 f"{first_sentence(r['play_caller'])} |")
    L += ["", "## Cross-links", "",
          "- [Continuity matrix](00_CONTINUITY_MATRIX.md)",
          "- [Change indexes](00_NEW_HEAD_COACHES.md)",
          "- [QB × coaching](00_QB_COACHING_CROSSLINK.md)",
          "- [Source conflicts](00_SOURCE_CONFLICTS.md)"]
    write("00_COACH_DIRECTORY.md", L)
    return len(L)


# ---------------------------------------------------------------------------
# 5C — Continuity / change matrix
# ---------------------------------------------------------------------------
def matrix(rows):
    L = ["# Continuity and Change Matrix — all 138 FBS programmes", "",
         SOURCE_LINE, "",
         "Every column below is a printed value. Steve Makinen's Stability "
         "Score table awards 4 points for a returning head coach, 3 for a "
         "returning offensive coordinator, 3 for a returning defensive "
         "coordinator, 4 for a returning quarterback and 0–4 for returning "
         "starters. A zero in one of those columns *is* the guide stating "
         "that the position changed — nothing here is inferred, and no TTW "
         "score is substituted.", "",
         "> The guide's own use of the total: it plays on teams with a "
         "Stability Score edge of 6 or more in non-conference games in weeks "
         "0–3, and against teams scoring 0–6 in the same window, excluding "
         "games with a spread of 30 or more (pp. 40–41).", "",
         "| Team | Conf | HC | OC | DC | QB | RS | Total | 2025 | Page |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]

    def mark(pts, isnew):
        return f"**0**" if isnew else str(pts)

    for r in sorted(rows, key=lambda x: (-x["stability_score"], x["team"])):
        L.append(
            f"| {link(r['team'])} | {r['conference']} "
            f"| {mark(r['hc_points'], r['new_hc'])} "
            f"| {mark(r['oc_points'], r['new_oc'])} "
            f"| {mark(r['dc_points'], r['new_dc'])} "
            f"| {mark(r['qb_points'], r['new_qb'])} "
            f"| {r['rs_points']} ({r['rs_count']}) "
            f"| **{r['stability_score']}** | {r['record_2025']} "
            f"| {r['stability_page']} |")

    hi = [r for r in rows if r["stability_score"] >= 14]
    lo = [r for r in rows if r["stability_score"] <= 6]
    L += ["", "## Distribution as printed", "",
          "| Band | Programmes |", "| --- | --- |",
          f"| 14–18 (highest continuity) | {len(hi)} |",
          f"| 7–13 | {138 - len(hi) - len(lo)} |",
          f"| 0–6 (lowest continuity, the guide's own fade band) | {len(lo)} |",
          "",
          "## Where the guide contradicts itself",
          "",
          "Six programmes are described differently by the Stability Score "
          "table and by their own team pages or the Coaching Carousel. Those "
          "contradictions are preserved, not resolved — see "
          "[source conflicts](00_SOURCE_CONFLICTS.md).",
          "",
          "## Cross-links", "",
          "- [Coach directory](00_COACH_DIRECTORY.md)",
          "- [Change indexes](00_NEW_HEAD_COACHES.md)",
          "- [QB × coaching](00_QB_COACHING_CROSSLINK.md)"]
    write("00_CONTINUITY_MATRIX.md", L)
    return len(hi), len(lo)


# ---------------------------------------------------------------------------
# 5D — Change indexes
# ---------------------------------------------------------------------------
def change_indexes(rows, notes, carousel, hi_n, lo_n):
    byteam = {r["team"]: r for r in rows}

    def note(team, key):
        return (notes.get(team) or {}).get(key) or NA

    neutrality = (
        "> **The guide's assessment travels with the change.** This index "
        "does not treat a change as good or bad. Where VSiN takes a view, "
        "that view is reproduced; where it does not, the row says so.")

    # --- new head coaches -------------------------------------------------
    new_hc = sorted([r for r in rows if r["new_hc"]], key=lambda x: x["team"])
    L = [f"# New Head Coaches — {len(new_hc)} programmes", "", SOURCE_LINE, "",
         neutrality, "",
         "A programme appears here when the Stability Score table awards 0 "
         "points for a returning head coach. Two programmes where the guide's "
         "three statements of head-coach status disagree are flagged; both "
         "readings are preserved in "
         "[source conflicts](00_SOURCE_CONFLICTS.md).", "",
         "| Team | Conf | Head coach | Carousel | VSiN's assessment |",
         "| --- | --- | --- | --- | --- |"]
    for r in new_hc:
        L.append(f"| {link(r['team'])} | {r['conference']} | {r['head_coach']}"
                 f"{' *(interim)*' if r['interim'] else ''} | "
                 f"{('p. ' + str(r['carousel_page'])) if r['carousel_page'] else '**not listed**'} | "
                 f"{first_sentence(note(r['team'], 'vsin_assessment'))} |")
    L += ["", "## Cross-links", "",
          "- [Coach directory](00_COACH_DIRECTORY.md) · "
          "[continuity matrix](00_CONTINUITY_MATRIX.md) · "
          "[new OCs](00_NEW_OFFENSIVE_COORDINATORS.md) · "
          "[new DCs](00_NEW_DEFENSIVE_COORDINATORS.md)"]
    write("00_NEW_HEAD_COACHES.md", L)

    # --- new coordinators -------------------------------------------------
    for fname, flag, key, title in (
            ("00_NEW_OFFENSIVE_COORDINATORS.md", "new_oc", "oc",
             "New Offensive Coordinators"),
            ("00_NEW_DEFENSIVE_COORDINATORS.md", "new_dc", "dc",
             "New Defensive Coordinators")):
        sel = sorted([r for r in rows if r[flag]], key=lambda x: x["team"])
        side = "offensive" if flag == "new_oc" else "defensive"
        L = [f"# {title} — {len(sel)} programmes", "", SOURCE_LINE, "",
             neutrality, "",
             f"A programme appears here when the Stability Score table awards "
             f"0 points for a returning {side} coordinator. Where the team "
             f"pages describe the position differently, both statements are "
             f"kept — see [source conflicts](00_SOURCE_CONFLICTS.md).", "",
             "| Team | Conf | Coordinator | What the guide records |",
             "| --- | --- | --- | --- |"]
        for r in sel:
            L.append(f"| {link(r['team'])} | {r['conference']} | "
                     f"{r[key] if r[key] != NA else '*not named*'} | "
                     f"{first_sentence(note(r['team'], key + '_status'))} |")
        L += ["", "## Cross-links", "",
              "- [New head coaches](00_NEW_HEAD_COACHES.md) · "
              "[major scheme changes](00_MAJOR_SCHEME_CHANGES.md) · "
              "[continuity matrix](00_CONTINUITY_MATRIX.md)"]
        write(fname, L)

    # --- play-callers -----------------------------------------------------
    pc = sorted([r for r in rows
                 if r["play_caller"] != NA
                 and re.search(r"chang|new|himself|his own|takes|took|promot",
                               r["play_caller"], re.I)],
                key=lambda x: x["team"])
    L = [f"# New Play-Callers — {len(pc)} programmes", "", SOURCE_LINE, "",
         neutrality, "",
         "Play-caller and coordinator are not the same field. This index "
         "lists the programmes where the guide states that the person calling "
         "plays has changed, or that a head coach is calling them himself — "
         "including cases where the Stability Score table still awards points "
         "for a returning coordinator.", "",
         "| Team | Conf | What the guide states |", "| --- | --- | --- |"]
    for r in pc:
        L.append(f"| {link(r['team'])} | {r['conference']} | {r['play_caller']} |")
    L += ["", "## Cross-links", "",
          "- [Coach directory](00_COACH_DIRECTORY.md) · "
          "[major scheme changes](00_MAJOR_SCHEME_CHANGES.md)"]
    write("00_NEW_PLAY_CALLERS.md", L)

    # --- scheme changes ---------------------------------------------------
    sc = sorted([r for r in rows if r["scheme_change"]], key=lambda x: x["team"])
    L = [f"# Major Scheme Changes — {len(sc)} programmes", "", SOURCE_LINE, "",
         neutrality, "",
         "A programme appears here only where the guide describes a change in "
         "how the team will play — a named system arriving, a stated shift in "
         "tempo, run/pass balance or personnel groupings, or an explicit "
         "statement that the offense or defense will look different. A "
         "coach's reputation is not evidence and does not qualify a "
         "programme for this list.", "",
         "| Team | Conf | Offensive scheme | Defensive scheme |",
         "| --- | --- | --- | --- |"]
    for r in sc:
        L.append(f"| {link(r['team'])} | {r['conference']} | "
                 f"{first_sentence(note(r['team'], 'offensive_scheme'))} | "
                 f"{first_sentence(note(r['team'], 'defensive_scheme'))} |")
    L += ["", "## Named schemes the guide states outright", "",
          "| Team | Scheme as named |", "| --- | --- |"]
    for r in sorted(rows, key=lambda x: x["team"]):
        for k in ("offensive_scheme", "defensive_scheme"):
            v = note(r["team"], k)
            if v != NA and re.search(
                    r"\b(3-3-5|4-2-5|3-4|4-3|Air Raid|triple option|Wing-T|"
                    r"spread|pro-style|Go-Go|Spread and Shred|21 personnel|"
                    r"12 personnel|option)\b", v):
                L.append(f"| {link(r['team'])} | {first_sentence(v)} |")
    L += ["", "## Cross-links", "",
          "- [New play-callers](00_NEW_PLAY_CALLERS.md) · "
          "[new OCs](00_NEW_OFFENSIVE_COORDINATORS.md) · "
          "[new DCs](00_NEW_DEFENSIVE_COORDINATORS.md)"]
    write("00_MAJOR_SCHEME_CHANGES.md", L)

    # --- high / low continuity -------------------------------------------
    for fname, sel, title, blurb in (
            ("00_HIGH_CONTINUITY_STAFFS.md",
             sorted([r for r in rows if r["stability_score"] >= 14],
                    key=lambda x: (-x["stability_score"], x["team"])),
             "High-Continuity Staffs",
             "Programmes scoring 14 or more on the printed Stability Score, "
             "with the head coach and both coordinators returning unless "
             "noted."),
            ("00_LOW_CONTINUITY_STAFFS.md",
             sorted([r for r in rows if r["stability_score"] <= 6],
                    key=lambda x: (x["stability_score"], x["team"])),
             "Low-Continuity Staffs",
             "Programmes scoring 6 or fewer on the printed Stability Score — "
             "the band the guide itself fades in weeks 0–3 non-conference "
             "games (pp. 40–41).")):
        L = [f"# {title} — {len(sel)} programmes", "", SOURCE_LINE, "",
             blurb, "", neutrality, "",
             "| Team | Conf | Total | HC | OC | DC | QB | RS | 2025 |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for r in sel:
            L.append(f"| {link(r['team'])} | {r['conference']} | "
                     f"**{r['stability_score']}** | {r['hc_points']} | "
                     f"{r['oc_points']} | {r['dc_points']} | {r['qb_points']} | "
                     f"{r['rs_points']} ({r['rs_count']}) | {r['record_2025']} |")
        L += ["", "## Cross-links", "",
              "- [Continuity matrix](00_CONTINUITY_MATRIX.md) · "
              "[new head coaches](00_NEW_HEAD_COACHES.md)"]
        write(fname, L)

    return {"new_hc": len(new_hc), "play_callers": len(pc),
            "scheme": len(sc), "high": hi_n, "low": lo_n}


# ---------------------------------------------------------------------------
# 5E — QB x coaching cross-link
# ---------------------------------------------------------------------------
def crosslink(rows, notes):
    qb = {}
    for f in sorted(glob.glob("_source/qb/*.json")):
        qb.update(json.load(open(f)))

    def cls(r):
        if r["new_qb"] and (r["new_oc"] or r["new_hc"]):
            return "New QB **and** new offensive staff"
        if r["new_qb"]:
            return "New QB, offensive staff intact"
        if r["new_oc"] or r["new_hc"]:
            return "Returning QB, new offensive staff"
        return "Returning QB and returning offensive staff"

    ORDER = ["New QB **and** new offensive staff",
             "New QB, offensive staff intact",
             "Returning QB, new offensive staff",
             "Returning QB and returning offensive staff"]

    groups = defaultdict(list)
    for r in rows:
        groups[cls(r)].append(r)

    L = ["# Quarterback × Coaching Cross-Link", "", SOURCE_LINE, "",
         "> **This is an intelligence index, not a betting system.** It states "
         "what the guide says about a programme's quarterback situation "
         "beside what it says about the staff that will coach him. It makes "
         "no claim that any combination produces market value. Where VSiN "
         "itself argues a coaching–quarterback combination matters to a "
         "price, that argument is reproduced in the programme file's betting "
         "field and nowhere else.", "",
         "> **Layer discipline.** Everything here is VSiN's preseason "
         "position (Phase 4 Layer 1) plus Phase 5 coaching content. The TTW "
         "verified quarterback state — the Phase 4 Layer 2 material and the "
         "frozen v0.8.1 workbook confidence codes — is deliberately absent "
         "from this table. Follow the quarterback link on each row for that "
         "layer, where it is kept separate.", ""]

    for g in ORDER:
        sel = sorted(groups[g], key=lambda x: x["team"])
        L += [f"## {g} — {len(sel)} programmes", "",
              "| Team | Conf | Guide's expected starter | Scheme fit as stated "
              "| QB development as stated | Files |",
              "| --- | --- | --- | --- | --- | --- |"]
        for r in sel:
            q = qb.get(r["team"], {})
            n = notes.get(r["team"]) or {}
            L.append(
                f"| {link(r['team'])} | {r['conference']} "
                f"| {q.get('expected_starter') or NA} "
                f"| {first_sentence(q.get('scheme_fit') or NA)} "
                f"| {first_sentence(n.get('qb_development') or NA)} "
                f"| [QB](../04_Quarterback_Database/{slug(r['team'])}) · "
                f"[coaching]({slug(r['team'])}) |")
        L.append("")

    dev = sorted([r for r in rows if r["qb_developer"]], key=lambda x: x["team"])
    L += [f"## Staffs the guide credits with a quarterback-development record "
          f"— {len(dev)} programmes", "",
          "A programme appears here only where the guide states a development "
          "record or an explicit developmental expectation attached to the "
          "staff. Reputation alone does not qualify.", "",
          "| Team | Conf | What the guide states |", "| --- | --- | --- |"]
    for r in dev:
        n = notes.get(r["team"]) or {}
        L.append(f"| {link(r['team'])} | {r['conference']} | "
                 f"{first_sentence(n.get('qb_development') or NA)} |")

    L += ["", "## Cross-links", "",
          "- [Coach directory](00_COACH_DIRECTORY.md) · "
          "[continuity matrix](00_CONTINUITY_MATRIX.md) · "
          "[Quarterback Database](../04_Quarterback_Database/README.md)"]
    write("00_QB_COACHING_CROSSLINK.md", L)
    return {g: len(groups[g]) for g in ORDER} | {"developer": len(dev)}


# ---------------------------------------------------------------------------
# 5F — Source conflict audit
# ---------------------------------------------------------------------------
def conflicts_file(machine, notes):
    L = ["# Source Conflict Audit — coaching", "", SOURCE_LINE, "",
         "> **Nothing here is corrected.** Where the 2026 VSiN College "
         "Football Betting Guide states the same fact two or three ways, "
         "every statement is reproduced as printed and the contradiction is "
         "preserved. That is the whole purpose of this file.", "",
         "Conflicts are found two ways: the Navy tenure discrepancy is "
         "carried forward by owner instruction from Phase 2, and the rest are "
         "derived by cross-checking the three independent places the guide "
         "states coaching status — the team pages, Steve Makinen's Stability "
         "Score table (pp. 41–44) and Adam Burke's Coaching Carousel "
         "(pp. 28–37).", ""]

    L += ["## Machine-detected conflicts", "",
          f"{len(machine)} recorded.", ""]
    for c in machine:
        L += [f"### {c['team']} — {c['field']}", "", c["detail"],
              f"", f"*Programme file: {link(c['team'])}*", ""]

    authored = [(t, n["conflicts"]) for t, n in sorted(notes.items())
                if n.get("conflicts") and n["conflicts"] != NA]
    L += ["## Conflicts recorded while authoring the programme records", "",
          f"{len(authored)} recorded. These were found by reading the team "
          f"pages against the Stability Score table during Phase 5A. Each is "
          f"reproduced in the programme's own file as well.", ""]
    for team, detail in authored:
        L += [f"### {team}", "", detail, "", f"*Programme file: {link(team)}*", ""]

    L += ["## What this audit does not do", "",
          "- It does not decide which printed statement is right.",
          "- It does not edit, footnote or silently harmonise the guide.",
          "- It does not extend to conflicts outside coaching; those recorded "
          "in earlier phases stay in their own phase files.", "",
          "## Cross-links", "",
          "- [Continuity matrix](00_CONTINUITY_MATRIX.md) · "
          "[coach directory](00_COACH_DIRECTORY.md)"]
    write("00_SOURCE_CONFLICTS.md", L)
    return len(machine), len(authored)


# ---------------------------------------------------------------------------
def readme(rows, counts, cl, conf_counts):
    L = ["# Coaching Intelligence Database", "", SOURCE_LINE, "",
         "One standardised coaching record for each of the 138 FBS "
         "programmes, plus the indexes built on top of them. Everything is "
         "the guide's position at publication: no outside research, no "
         "post-publication updates, and no change to the frozen TTW Power "
         "Ratings Workbook v0.8.1.", "",
         "## Files", "",
         "| File | What it holds |", "| --- | --- |",
         "| [00_COACH_DIRECTORY.md](00_COACH_DIRECTORY.md) | Head coaches and "
         "every coordinator the guide names, searchable |",
         "| [00_CONTINUITY_MATRIX.md](00_CONTINUITY_MATRIX.md) | All 138 "
         "programmes with the printed Stability Score components |",
         "| [00_NEW_HEAD_COACHES.md](00_NEW_HEAD_COACHES.md) | "
         f"{counts['new_hc']} programmes |",
         "| [00_NEW_OFFENSIVE_COORDINATORS.md](00_NEW_OFFENSIVE_COORDINATORS.md) | "
         f"{sum(1 for r in rows if r['new_oc'])} programmes |",
         "| [00_NEW_DEFENSIVE_COORDINATORS.md](00_NEW_DEFENSIVE_COORDINATORS.md) | "
         f"{sum(1 for r in rows if r['new_dc'])} programmes |",
         "| [00_NEW_PLAY_CALLERS.md](00_NEW_PLAY_CALLERS.md) | "
         f"{counts['play_callers']} programmes |",
         "| [00_MAJOR_SCHEME_CHANGES.md](00_MAJOR_SCHEME_CHANGES.md) | "
         f"{counts['scheme']} programmes |",
         "| [00_HIGH_CONTINUITY_STAFFS.md](00_HIGH_CONTINUITY_STAFFS.md) | "
         f"{counts['high']} programmes scoring 14+ |",
         "| [00_LOW_CONTINUITY_STAFFS.md](00_LOW_CONTINUITY_STAFFS.md) | "
         f"{counts['low']} programmes scoring 6 or fewer |",
         "| [00_QB_COACHING_CROSSLINK.md](00_QB_COACHING_CROSSLINK.md) | "
         "Quarterback situation against staff situation |",
         "| [00_SOURCE_CONFLICTS.md](00_SOURCE_CONFLICTS.md) | "
         f"{conf_counts[0] + conf_counts[1]} preserved contradictions |",
         "| *team files* | 138 records, 29 fields each |", "",
         "## The 29 fields", "",
         "Fields 1–5, 26, 27 and 29 are machine-derived from tables this "
         "library already extracted and validated. Fields 6–25 and 28 are "
         "authored from the team pages, the Coaching Carousel and the "
         "conference previews, and stored in `_source/coaching/*.json`.", "",
         "Two rules are enforced by construction rather than by care:", "",
         "- Scheme and tendency fields say `Not addressed in guide.` unless "
         "the guide states them. A coach's reputation is not evidence.",
         "- Source conflicts are rendered as their own labelled block, never "
         "resolved into a single value.", "",
         "## Rebuild", "", "```bash",
         "python3 _tools/build_coaching.py           # the 138 records",
         "python3 _tools/build_coaching_indexes.py   # the indexes",
         "python3 _tools/validate_coaching.py        # 10 checks", "```", "",
         "## Cross-links", "",
         "- [Team Database](../02_Team_Database/README.md)",
         "- [Quarterback Database](../04_Quarterback_Database/README.md)",
         "- [Conference Database](../01_Conference_Database/)"]
    write("README.md", L)


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = json.load(open("_source/data/coaching_matrix.json"))
    notes = load_notes()
    carousel = load_carousel()
    machine = coaching_conflicts(load_teams(), load_stability(), carousel)

    directory(rows, notes, carousel)
    hi, lo = matrix(rows)
    counts = change_indexes(rows, notes, carousel, hi, lo)
    cl = crosslink(rows, notes)
    cc = conflicts_file(machine, notes)
    readme(rows, counts, cl, cc)

    print(f"indexes written to {OUT}/")
    print(f"  new head coaches      {counts['new_hc']}")
    print(f"  new OCs               {sum(1 for r in rows if r['new_oc'])}")
    print(f"  new DCs               {sum(1 for r in rows if r['new_dc'])}")
    print(f"  new play-callers      {counts['play_callers']}")
    print(f"  major scheme changes  {counts['scheme']}")
    print(f"  high continuity (14+) {counts['high']}")
    print(f"  low continuity (0-6)  {counts['low']}")
    print(f"  conflicts             {cc[0]} machine + {cc[1]} authored")
    for k, v in cl.items():
        print(f"  crosslink: {k:<45} {v}")


if __name__ == "__main__":
    main()
