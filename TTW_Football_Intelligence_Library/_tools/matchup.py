#!/usr/bin/env python3
"""
TTW Football Intelligence Library — static matchup-reference packet
===================================================================

Deterministic retrieval. Give it two canonical team names; it returns the
frozen preseason reference material the library already holds about them,
reproduced from the approved artifacts and cited back to them.

    python3 _tools/matchup.py "UNLV Rebels" "North Dakota State Bison"
    python3 _tools/matchup.py "UNLV Rebels" "Idaho State Bengals" -o packet.md

WHAT THIS IS
------------
A reference packet, not an analysis. Every line is lifted from an approved
file in this library and carries the page or file it came from. The packet
introduces no football fact of its own.

WHAT THIS IS NOT
----------------
It does not recommend a wager, compute an edge, build a depth chart,
resolve a source conflict, read the workbook, or treat any preseason
quarterback expectation as current. The guide was published before the
season; every number in here is stale by construction, and the packet says
so at the top of every run.

The last section is the only place the packet says anything of its own,
and it is deliberately a list of QUESTIONS: the things this frozen record
cannot answer and which must be verified against current sources before a
betting decision. Each question is generated from something the library
itself marks as uncertain — an unresolved quarterback job, a source
conflict, an absence marker — never from a judgement about the teams.

Retrieval is by exact canonical name. A partial name is rejected with the
candidate list rather than resolved by guesswork, because "North Dakota
State" and "North Texas", or "Miami" and "Miami (Ohio)", are different
programmes and the library will not choose between them for you.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

NA = "Not addressed in guide."
NO_CONFLICT = "No source conflict identified for this team."
# The packet's own two sentinels. Named so the validator can reference them
# rather than re-typing the strings and drifting from them.
NO_CROSS_CONFLICT = ("No conflict recorded for this team in any other "
                     "database.")
NOT_ON_SCHEDULE = (
    "This matchup does not appear on either team's guide-printed schedule. "
    "That is a statement about the guide's schedule table only — it is not a "
    "claim that the game is not played.")

NOTICE = (
    "> **STATIC PRESEASON REFERENCE** — This material reflects the committed "
    "2026 VSiN College Football Betting Guide and related frozen library "
    "databases. Verify all quarterbacks, injuries, depth charts, rosters, "
    "statistics and market prices with current sources before making a "
    "betting decision."
)

# The thirteen requested sections, mapped to where the library already keeps
# them. Nothing is re-derived: each entry names a rendered heading in an
# approved file, and the packet reproduces that heading's body.
TEAM_SECTIONS = [
    ("Canonical identity and conference", [1, 2, 3]),
    ("Source-specific preseason expectations", [4, 19, 20]),
    ("Head coach and coordinators", [6, 7, 8]),
    ("Offensive identity", [13]),
    ("Defensive identity", [14]),
    ("Returning production, strengths and weaknesses", [10, 11, 12, 15, 16]),
    ("Schedule context", [17, 18]),
    ("Betting notes and best bets", [21]),
    ("Historical and situational trends", [22]),
    ("Important statistics", [23]),
    ("Bull case", [24]),
    ("Bear case", [25]),
    ("Open questions and risks", [26]),
    ("Source conflicts", [27]),
    ("Page references and provenance", [28]),
]


def slug(name):
    s = name.lower().replace("’", "").replace("'", "").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def load(name):
    with open(os.path.join(ROOT, "_source", "data", f"{name}.json")) as fh:
        return json.load(fh)


def read(path):
    p = os.path.join(ROOT, path)
    return open(p).read() if os.path.exists(p) else ""


def heading(body, n):
    """The body of '## <n>. <title>', with its title, exactly as rendered."""
    m = re.search(rf"\n## {n}\. ([^\n]*)\n(.*?)(?=\n## |\Z)", body, re.S)
    return (m.group(1).strip(), m.group(2).strip()) if m else (None, None)


def named_section(body, title):
    m = re.search(rf"\n## {re.escape(title)}\n(.*?)(?=\n## |\Z)", body, re.S)
    return m.group(1).strip() if m else ""


def resolve(name, canon):
    """Exact canonical match, or a refusal that lists the candidates.

    Deliberately strict. Prefix resolution is how "GEORGIA SOUTHERN" once
    landed on Georgia's page and how a North Dakota State query could
    silently return North Texas; the library's identity discipline is an
    enumerated bijection, and this entry point holds the same line.
    """
    if name in canon:
        return name
    low = name.strip().lower()
    near = sorted(t for t in canon if low and low in t.lower())
    raise SystemExit(
        f"'{name}' is not a canonical team name.\n"
        + (f"Did you mean: {', '.join(near)}?\n" if near else
           "No canonical name contains that string.\n")
        + "Retrieval requires the exact name as the library stores it.")


def team_block(team, canon, xconf):
    det = canon[team]
    body = read(f"02_Team_Database/{slug(team)}.md")
    coach = read(f"03_Coaching_Database/{slug(team)}.md")
    qb = read(f"04_Quarterback_Database/{slug(team)}.md")

    L = [f"# {team}", "",
         f"| | |", "| --- | --- |",
         f"| Canonical identity | **{team}** |",
         f"| Conference (as the guide prints it) | {det['conference']} |",
         f"| Guide pages | pp. {det['pages'][0]}–{det['pages'][-1]} |",
         f"| Head coach as printed | {det.get('head_coach') or NA} |",
         f"| Makinen power rating as printed | {det['power_rating']} |",
         f"| Team file | [02_Team_Database/{slug(team)}.md]"
         f"(../02_Team_Database/{slug(team)}.md) |",
         ""]

    for title, nums in TEAM_SECTIONS:
        L += [f"## {title}", ""]
        for n in nums:
            h, b = heading(body, n)
            if h is None:
                continue
            L += [f"**§{n}. {h}** — *02_Team_Database/{slug(team)}.md*", "",
                  b or NA, ""]

    # Quarterback — layer A only, and labelled every time it is shown.
    L += ["## Frozen preseason quarterback outlook", "",
          "> **NOT CURRENT STATUS.** This is the VSiN guide's preseason "
          "expectation as published. The library's separately maintained "
          "verification layer is deliberately NOT reproduced here; read it "
          "in the quarterback file and verify against current sources.", ""]
    # The source heading is emitted with the body so the packet names the
    # section it reproduces rather than presenting the table unattributed.
    secA = named_section(qb, "A. VSiN PRESEASON QB INTELLIGENCE")
    L += [f"**A. VSiN PRESEASON QB INTELLIGENCE** — "
          f"*04_Quarterback_Database/{slug(team)}.md*", "",
          secA or NA, "",
          f"*Quarterback file (both layers): "
          f"[04_Quarterback_Database/{slug(team)}.md]"
          f"(../04_Quarterback_Database/{slug(team)}.md)*", ""]

    # Coaching — the stability block is printed, never recomputed.
    L += ["## Coaching record and printed Stability Score", ""]
    stab = named_section(coach, "VSiN Stability Score — as printed")
    L += [stab or NA, "",
          f"*Coaching file: [03_Coaching_Database/{slug(team)}.md]"
          f"(../03_Coaching_Database/{slug(team)}.md)*", ""]

    # Cross-database conflicts, restated with their originating layer.
    L += ["## Cross-database source conflicts", ""]
    recs = xconf.get(team, [])
    if recs:
        for r in recs:
            L.append(f"- **{r['title']}** {r['detail']} *Recorded in Phase "
                     f"{r['phase']}, {r['where']}.*")
    else:
        L.append(NO_CROSS_CONFLICT)
    L.append("")
    return "\n".join(L)


def head_to_head(a, b, canon):
    """Is this game on either schedule? Reproduced, not inferred."""
    rows = []
    for x, y in ((a, b), (b, a)):
        short = y.rsplit(" ", 1)[0]
        for g in (canon[x].get("schedule") or []):
            opp = (g.get("opponent") or "").strip()
            if opp.upper().replace("AT ", "") == short.upper():
                rows.append(
                    f"| {x} | {g.get('date')} | {g.get('opponent_raw')} | "
                    f"{g.get('location')} | {g.get('projected_line') or '—'} | "
                    f"{g.get('opponent_power_rating') or '—'} |")
    if not rows:
        return [NOT_ON_SCHEDULE, ""]
    return ["| Team | Date | Opponent as printed | Site | Projected line | "
            "Opp. power rating |",
            "| --- | --- | --- | --- | --- | --- |"] + rows + [
        "", "*Projected lines are Makinen's preseason numbers as printed in "
        "the guide's schedule tables. They are not a current market price "
        "and must not be compared to one without re-verification.*", ""]


def verification_questions(a, b, canon, xconf):
    """The only section the packet authors, and it authors only questions.

    Each item is generated from something the library itself flags: an
    unresolved quarterback job, a recorded source conflict, a missing
    field. Nothing here evaluates the teams or the matchup.
    """
    from qb_lib import VSIN_TO_ABBREV
    xr = {r["team"]: r for r in
          json.load(open(os.path.join(ROOT, "_source", "data",
                                      "qb_crossref.json")))["records"]}
    out = []
    for t in (a, b):
        r = xr.get(t)
        if r and r["relationship"] != "ALIGNED":
            out.append(
                f"**{t} — quarterback.** The library classifies this team "
                f"**{r['relationship']}** between the guide's preseason "
                f"expectation ({r['vsin_starter']}) and its last verified "
                f"state ({r['verified_starter']}, confidence {r['confidence']}, "
                f"verified {r['verification_date']}). Who is taking the first "
                f"snap, and what has changed since that verification date?")
        elif r:
            out.append(
                f"**{t} — quarterback.** Guide and last verification agree on "
                f"{r['vsin_starter']} as of {r['verification_date']} "
                f"(confidence {r['confidence']}). Confirm the job and the "
                f"health of the room today.")
        if xconf.get(t):
            kinds = sorted({x["title"].rstrip(".") for x in xconf[t]})
            out.append(
                f"**{t} — unresolved source conflict.** The library records "
                f"{len(xconf[t])} conflict(s) it deliberately does not "
                f"resolve ({'; '.join(kinds)}). Which printed figure does the "
                f"current market agree with?")
        body = read(f"02_Team_Database/{slug(t)}.md")
        gaps = [h for n in range(1, 28)
                for h, bd in [heading(body, n)]
                if h and bd and bd.startswith(NA)]
        if gaps:
            out.append(
                f"**{t} — the guide is silent.** {len(gaps)} standard "
                f"heading(s) carry the absence marker "
                f"({', '.join(gaps[:4])}{'…' if len(gaps) > 4 else ''}). "
                f"These are gaps to fill from current sources, not evidence "
                f"that nothing is there.")
        rs = (canon[t].get("returning_starters") or {}).get("total") or {}
        if rs.get("value") is not None:
            out.append(
                f"**{t} — roster.** The guide printed {rs['value']} returning "
                f"starters at publication. Confirm the current two-deep, "
                f"portal departures and injuries before using that figure.")
    out.append(
        "**Both teams — market.** This packet contains no current spread, "
        "total or price. Obtain the current market and its movement "
        "independently.")
    out.append(
        "**Both teams — venue and weather.** Not addressed in guide.")
    return out


def build(a, b):
    canon = {t["team"]: t for t in load("team_details")}
    a, b = resolve(a, canon), resolve(b, canon)
    if a == b:
        raise SystemExit("a matchup needs two different teams")
    from cross_conflicts import cross_database_conflicts
    xconf = cross_database_conflicts()

    L = [f"# Static matchup reference — {a} vs {b}", "", NOTICE, "",
         "*Source classes: GUIDE CONTENT (2026 VSiN College Football Betting "
         "Guide, 345 pp., as published) and TTW DERIVED navigation. Every "
         "section below is reproduced from an approved file in this frozen "
         "library and cited back to it. This packet recommends no wager, "
         "computes no edge, resolves no source conflict, and reads nothing "
         "from the v0.8.1 workbook.*", "",
         "---", "", "## Head-to-head as the guide prints it", ""]
    L += head_to_head(a, b, canon)
    L += ["---", "", team_block(a, canon, xconf),
          "---", "", team_block(b, canon, xconf),
          "---", "",
          "## Betting-relevant questions requiring current verification", "",
          "*The library cannot answer these. They are generated from what it "
          "marks uncertain, and each must be resolved against current sources "
          "before any betting analysis.*", ""]
    L += [f"{i}. {q}" for i, q in
          enumerate(verification_questions(a, b, canon, xconf), 1)]
    L += ["", "---", "", "## Required next steps — the separation this packet "
          "does not cross", "",
          "1. Retrieve this frozen matchup-reference packet.",
          "2. Read the current matchup numbers from the v0.8.1 workbook.",
          "3. Independently verify quarterback status, injuries, depth "
          "charts, roster changes, weather and venue.",
          "4. Obtain current market spreads, totals and movement.",
          "5. Reconcile agreements and conflicts between the four.",
          "6. Only then conduct betting analysis.",
          "7. Any proposed workbook adjustment follows the existing approval "
          "and audit process.", "",
          "> Current information may read and cite this frozen library. It "
          "may never be written back into it. This packet is generated "
          "read-only and changes nothing in the library or the workbook.", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(
        description="Static matchup-reference packet from the frozen library.")
    ap.add_argument("team_a")
    ap.add_argument("team_b")
    ap.add_argument("-o", "--out", help="write to a file instead of stdout")
    args = ap.parse_args()
    text = build(args.team_a, args.team_b)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text + "\n")
        print(f"packet written: {args.out} ({len(text.splitlines())} lines)")
    else:
        print(text)


if __name__ == "__main__":
    main()
