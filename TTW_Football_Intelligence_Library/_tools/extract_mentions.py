#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 3 Cross-Guide Mention Index
=====================================================================

Finds every meaningful mention of every team across all 345 pages, so a team
file can draw on the whole guide rather than only that team's own spread.

The hard part is precision, not recall. "Georgia" must not match Georgia Tech,
Georgia Southern or Georgia State; "Miami" must not conflate the Hurricanes
with the RedHawks. Each team's search term therefore carries a negative
lookahead built from every other team whose name extends it.

Usage:
    python3 _tools/extract_mentions.py     # run from the library root
"""

import json
import os
import re
import sys
from collections import defaultdict

SRC = "_source/data"
PAGES = "_source/extracted/pages"

# Printed short forms the guide uses that a canonical name would not match.
EXTRA_TERMS = {
    "UTSA Roadrunners": ["UTSA"],
    "FIU Golden Panthers": ["FIU", "Florida International"],
    "ULM Warhawks": ["ULM", "Louisiana-Monroe", "LA Monroe"],
    "Connecticut Huskies": ["UConn", "Connecticut"],
    "Ole Miss Rebels": ["Ole Miss", "Mississippi"],
    "Miami (Ohio) RedHawks": ["Miami (OH)", "Miami (Ohio)", "Miami Ohio"],
    "Miami Hurricanes": ["Miami"],
    "Ohio U Bobcats": ["Ohio U", "Ohio Bobcats"],
    "Massachusetts Minutemen": ["UMass"],
    "NC State Wolfpack": ["NC State", "North Carolina State"],
    "Texas A&M Aggies": ["Texas A&M"],
    "Louisiana Ragin’ Cajuns": ["Louisiana", "Ragin' Cajuns", "Ragin’ Cajuns"],
    "Southern Miss Golden Eagles": ["Southern Miss"],
    "Sam Houston State Bearkats": ["Sam Houston"],
    "Appalachian State Mountaineers": ["Appalachian State", "App State"],
    "Central Florida Knights": ["UCF"],
    "UCF Golden Knights": ["UCF"],
    "UNLV Rebels": ["UNLV"],
    "UTEP Miners": ["UTEP"],
    "UAB Blazers": ["UAB"],
    "SMU Mustangs": ["SMU"],
    "TCU Horned Frogs": ["TCU"],
    "BYU Cougars": ["BYU"],
    "LSU Tigers": ["LSU"],
    "USC Trojans": ["USC"],
    "UCLA Bruins": ["UCLA"],
    "Notre Dame Fighting Irish": ["Notre Dame", "Fighting Irish"],
    "North Dakota State Bison": ["North Dakota State", "NDSU"],
    "Sacramento State Hornets": ["Sacramento State", "Sac State"],
    "Northern Illinois Huskies": ["Northern Illinois", "NIU"],
    "Western Kentucky Hilltoppers": ["Western Kentucky", "WKU"],
    "Middle Tennessee Blue Raiders": ["Middle Tennessee"],
    "Florida Atlantic Owls": ["Florida Atlantic", "FAU"],
}

def school_terms(team_name, table_name):
    """Distinctive strings that identify this team in running prose.

    The school portion of a canonical name is found by truncating it to the
    token count of the guide's own short name from the projected standings
    tables — "Hawaii Rainbow Warriors" against "HAWAII" leaves "Hawaii",
    "Notre Dame Fighting Irish" against "NOTRE DAME" leaves "Notre Dame".
    That keeps the mascot out without maintaining a hand-written mascot list,
    which is what a previous version got wrong.
    """
    terms = set(EXTRA_TERMS.get(team_name, []))
    terms.add(team_name)

    depth = short_name_depth(table_name)
    tokens = team_name.split()
    if 0 < depth < len(tokens):
        terms.add(" ".join(tokens[:depth]))
    return {t for t in terms if len(t) >= 3}


FILLER = {"UNIV", "UNIVERSITY", "U"}


def short_name_depth(table_name):
    """How many leading words of the canonical name are the school's name.

    Filler words are dropped first — the guide prints "TEXAS ST UNIV" for Texas
    State, and counting that as three words would swallow the mascot. The
    result is also capped so at least one trailing token is always left over.
    """
    if not table_name:
        return 0
    words = [w for w in table_name.split() if w.upper() not in FILLER]
    return len(words)


def build_patterns(teams):
    """One regex per team, guarded against longer names that contain it."""
    with open(os.path.join(SRC, "conference_previews.json")) as fh:
        previews = json.load(fh)
    short = {}
    for conf in previews:
        for row in conf["standings"]:
            short[row["team"]] = row["table_name"]

    all_terms = {}
    for team in teams:
        all_terms[team["team"]] = school_terms(team["team"], short.get(team["team"]))

    patterns = {}
    for team in teams:
        parts = []
        for term in sorted(all_terms[team["team"]], key=len, reverse=True):
            # Any other team whose term begins with this one would otherwise
            # be swallowed: "Georgia" must not eat "Georgia Tech".
            extensions = set()
            for other, others_terms in all_terms.items():
                if other == team["team"]:
                    continue
                for other_term in others_terms:
                    if other_term.lower().startswith(term.lower() + " "):
                        nxt = other_term[len(term):].strip().split()[0]
                        extensions.add(re.escape(nxt))
            # And the mirror case: "Texas" must not fire inside "North Texas".
            prefixes = set()
            for other, others_terms in all_terms.items():
                if other == team["team"]:
                    continue
                for other_term in others_terms:
                    if other_term.lower().endswith(" " + term.lower()):
                        prev = other_term[: -len(term)].strip().split()[-1]
                        prefixes.add(prev)
            ahead = ""
            if extensions:
                ahead = r"(?!\s+(?:" + "|".join(sorted(extensions)) + r"))"
            # One lookbehind per prefix: Python requires each to be fixed width.
            behind = "".join(r"(?<!" + re.escape(pfx) + r"\s)"
                             for pfx in sorted(prefixes))
            parts.append(behind + re.escape(term) + ahead)
        patterns[team["team"]] = re.compile(
            r"\b(?:" + "|".join(parts) + r")\b", re.IGNORECASE)

    # Within a team's own two pages the writer switches to the mascot after the
    # first reference ("the Bobcats"), which is unambiguous in that context but
    # would fire everywhere if used guide-wide. So mascots are matched only on
    # the team's own spread.
    own_patterns = {}
    for team in teams:
        mascot_tokens = team["team"].split()
        depth = short_name_depth(short.get(team["team"], ""))
        mascot = " ".join(mascot_tokens[depth:]) if 0 < depth < len(mascot_tokens) else ""
        alts = [patterns[team["team"]].pattern]
        if len(mascot) >= 4:
            alts.append(r"\b" + re.escape(mascot) + r"\b")
        own_patterns[team["team"]] = re.compile("|".join(alts), re.IGNORECASE)
    return patterns, own_patterns


NUMERIC_RUN = re.compile(r"(?:(?:[-+]?[\d.]+|\([-+][\d.]+\))\s+){5,}")


def sentences(text):
    """Split into sentences, discarding anything that is plainly not prose.

    An over-long "sentence" means the splitter met a table rather than text —
    a schedule block or the contents page — and those must not reach a team
    file as if they were analysis.
    """
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z“\"])", text)
    out = []
    for part in parts:
        part = part.strip()
        if not (30 < len(part) <= 400):
            continue
        if NUMERIC_RUN.search(part):
            continue
        digits = sum(c.isdigit() for c in part)
        if digits / len(part) > 0.18:
            continue
        out.append(part)
    return out


def clean_page(page):
    raw = open(os.path.join(PAGES, f"p{page:03d}.txt")).read()
    raw = re.sub(r"-\n", "", raw)
    raw = re.sub(r"\s+", " ", raw)
    raw = re.sub(r"\d{1,3} 2026 VSiN COLLEGE FOOTBALL BETTING GUIDE", " ", raw)
    raw = re.sub(r"Date Opponent/Projected Line.*?total offense defense", " ", raw)
    raw = re.sub(r"Date Opponent/Projected Line.*?Opponent Power Rating", " ", raw)
    raw = re.sub(r"Three Burning Questions for the 2026 Season", " ", raw)
    raw = re.sub(r"(?:OFFENSIVE|DEFENSIVE) STATISTICS.*?(?=[A-Z][a-z])", " ", raw)
    return re.sub(r"\s+", " ", raw)


def main():
    with open(os.path.join(SRC, "teams.json")) as fh:
        teams = json.load(fh)
    patterns, own_patterns = build_patterns(teams)

    own_pages = {}
    for team in teams:
        own_pages[team["team"]] = {team["page"], team["page"] + 1}

    mentions = defaultdict(list)
    # The cover and the contents page carry no prose about any team, and the
    # contents page is one huge run of team names that would match everything.
    for page in range(3, 346):
        text = clean_page(page)
        if not text.strip():
            continue
        for sentence in sentences(text):
            words = [w for w in sentence.split() if re.search(r"[a-z]", w)]
            if len(words) < 8:
                continue
            for team in teams:
                own = page in own_pages[team["team"]]
                matcher = own_patterns[team["team"]] if own else patterns[team["team"]]
                if matcher.search(sentence):
                    mentions[team["team"]].append({
                        "page": page,
                        "sentence": sentence,
                        "own_page": own,
                    })

    out = {}
    for team in teams:
        rows = mentions[team["team"]]
        out[team["team"]] = {
            "total": len(rows),
            "off_page": [r for r in rows if not r["own_page"]],
            "on_page": [r for r in rows if r["own_page"]],
            "pages": sorted({r["page"] for r in rows}),
        }

    with open(os.path.join(SRC, "team_mentions.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    counts = sorted(((v["total"], k) for k, v in out.items()), reverse=True)
    print(f"teams indexed        {len(out)}")
    print(f"total mentions       {sum(v['total'] for v in out.values())}")
    print(f"off-own-page total   {sum(len(v['off_page']) for v in out.values())}")
    print("\nmost referenced:")
    for total, name in counts[:8]:
        print(f"  {name:<34} {total:>4} sentences across "
              f"{len(out[name]['pages'])} pages")
    print("\nleast referenced:")
    for total, name in counts[-5:]:
        print(f"  {name:<34} {total:>4}")
    zero = [k for k, v in out.items() if v["total"] == 0]
    if zero:
        print("\nWARNING — teams with no mentions at all:", zero)
        sys.exit(1)


if __name__ == "__main__":
    main()
