#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Source Extraction
=====================================================

Extracts structured entity tables from the 2026 VSiN College Football Betting
Guide PDF into JSON, plus a page-marked full-text dump for grep-based research.

This script is the ONLY path by which guide content enters the library.
Everything downstream is generated from its output, so extraction bugs are
fixed here once rather than in 138 hand-written files.

Usage:
    python3 extract_guide.py /path/to/2026-VSiN-CFB-Betting-Guide.pdf [outdir]

Requires: PyMuPDF  (pip install pymupdf)

Provenance is recorded in _source/SOURCE_MANIFEST.md. Verify the PDF md5
before trusting output against a different printing of the guide.
"""

import json
import os
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF required:  pip install pymupdf")


# --- page-geometry helpers ----------------------------------------------------

def page_spans(doc, page_index):
    """All text spans on a page as (font_size, text) pairs."""
    out = []
    for block in doc[page_index].get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span["text"].strip()
                if text:
                    out.append((round(span["size"], 1), text))
    return out


def flatten(text):
    """Collapse PDF line wrapping so regexes can cross line breaks."""
    return re.sub(r"\s+", " ", re.sub(r"-\n", "", text))


# --- extraction ---------------------------------------------------------------

# The contents page lists every conference preview and every team with its page.
# Rows are "Name.........<page>"; conference rows carry "Betting Preview".
TOC_ROW = re.compile(r"^\s*(.+?)\.{2,}\s*(\d{2,3})\s*$", re.M)

# Team header block, bottom of each team's left-hand page.
COACH = re.compile(r"^(.+?)\s*[-–]\s*(\d+)(?:st|nd|rd|th)\s+season\s*$", re.M)
# "7-6 SU & ATS, 5-8 O-U"   (SU==ATS)
# "1-11 SU & 5-7 ATS, 6-6 O-U"
# "9-4 SU & 8-4-1 ATS, 6-7 O-U"   (ties appear in ATS records)
RECORD = re.compile(
    r"(\d+-\d+(?:-\d+)?)\s*SU\s*&\s*(?:(\d+-\d+(?:-\d+)?)\s*)?ATS,"
    r"\s*(\d+-\d+(?:-\d+)?)\s*O-U"
)
SCHED_STRENGTH = re.compile(r"([\d.]+)\s*#(\d+)\s+toughest\s+of\s+(\d+)")
RANK = re.compile(r"#(\d+)\s+of\s+(\d+)")

# Coordinator mentions. Deliberately case-SENSITIVE: using re.I here would let
# [A-Z] match lowercase and swallow the word after the name ("Aaron Henry left").
NAME_WORD = r"(?:[A-Z]\.(?:[A-Z]\.)?|[A-Z][a-z]+(?:['\-][A-Za-z]+)*)"
PERSON = NAME_WORD + r"(?:\s+" + NAME_WORD + r"){1,2}"
COORD_PATTERNS = [
    ("OC", re.compile(r"\bOC\s+(" + PERSON + r")")),
    ("DC", re.compile(r"\bDC\s+(" + PERSON + r")")),
    ("OC", re.compile(r"[Oo]ffensive [Cc]oordinator\s+(" + PERSON + r")")),
    ("DC", re.compile(r"[Dd]efensive [Cc]oordinator\s+(" + PERSON + r")")),
]

# Uniform across all 138 team pages (verified).
OFFENSIVE_STATS = [
    "POINTS PER GAME", "YARDS PER POINT", "PLAYS PER GAME", "TIME OF POSSESSION",
    "3RD DOWN CONV. %", "TOTAL YARDS PER GAME", "YARDS PER PLAY",
    "RUSH ATTEMPTS PER GAME", "RUSH YARDS PER GAME", "YARDS PER RUSH ATTEMPT",
    "PASS ATTEMPTS PER GAME", "COMPLETION %", "PASSING YARDS PER GAME",
    "YARDS PER PASS ATTEMPT", "TURNOVERS",
]
DEFENSIVE_STATS = [
    "POINTS PER GAME", "YARDS PER POINT", "3RD DOWN CONV. %",
    "TOTAL YARDS PER GAME", "YARDS PER PLAY", "RUSH YARDS PER GAME",
    "YARDS PER RUSH ATTEMPT", "COMPLETION %", "PASSING YARDS PER GAME",
    "YARDS PER PASS ATTEMPT", "SACKS", "TURNOVERS",
]

# Feature articles, from the contents page. Page numbers are printed page
# numbers, which equal PDF page numbers throughout this guide.
FEATURES = [
    (1, "Cover"), (2, "Contents / Staff / Abbreviations"),
    (3, "Welcome to the 2026 VSiN College Football Betting Guide"),
    (4, "2026 Season Predictions"),
    (5, "VSiN Host College Football Best Bets"),
    (16, "Leave No Doubt: Irish Top Matt Youmans' Preseason Top 50"),
    (21, "Quantifying College Football's Biggest Advantage: Home-Field Advantage"),
    (22, "2026 College Football Win Totals I'm Betting Now"),
    (28, "The Coaching Carousel Never Stops"),
    (38, "Nobody Believed Then. Nobody's Betting Now."),
    (39, "Value in the Heisman Race"),
    (40, "Taking Advantage of College Football Stability in 2026"),
    (45, "The Year of the Quarterback"),
    (46, "Steve Makinen's 2026 College Football Power Rating Projections"),
]


def extract(pdf_path, outdir):
    doc = fitz.open(pdf_path)
    pages_dir = os.path.join(outdir, "extracted", "pages")
    data_dir = os.path.join(outdir, "data")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # --- full text, one file per page + one marked concatenation -------------
    page_text = {}
    parts = []
    for i, page in enumerate(doc):
        n = i + 1
        text = page.get_text("text")
        page_text[n] = text
        with open(os.path.join(pages_dir, f"p{n:03d}.txt"), "w") as fh:
            fh.write(text)
        parts.append(f"\n\n===== [PAGE {n}] =====\n{text}")
    with open(os.path.join(outdir, "extracted", "guide_full.txt"), "w") as fh:
        fh.write("".join(parts))

    # --- conferences and teams from the contents page ------------------------
    conference = None
    teams, conferences = [], []
    for name, page in TOC_ROW.findall(page_text[2]):
        name = re.sub(r"[\.\s]+$", "", name.strip())
        if "Betting Preview" in name:
            conference = name.replace(" Betting Preview", "").strip()
            conferences.append({"conference": conference, "preview_page": int(page)})
        else:
            teams.append({"team": name, "page": int(page), "conference": conference})

    # --- per-team fields -----------------------------------------------------
    for team in teams:
        left = page_text[team["page"]]          # team header + schedule
        right = page_text[team["page"] + 1]     # burning questions + stats

        m = COACH.search(left)
        raw_coach = m.group(1).strip()
        team["head_coach"] = re.sub(r"\s*\(interim\)", "", raw_coach).strip()
        team["interim"] = "(interim)" in raw_coach
        team["hc_season"] = int(m.group(2))

        m = RECORD.search(left)
        team["su_2025"] = m.group(1)
        team["ats_2025"] = m.group(2) or m.group(1)  # "SU & ATS" means identical
        team["ou_2025"] = m.group(3)

        m = SCHED_STRENGTH.search(flatten(left))
        team["sched_strength"] = m.group(1) if m else None
        team["sched_strength_rank"] = f"#{m.group(2)} of {m.group(3)}" if m else None

        # The power rating is the sole display-size numeral on the right page.
        big = [t for sz, t in page_spans(doc, team["page"])
               if sz >= 23 and re.fullmatch(r"-?\d+\.?\d*", t)]
        team["power_rating"] = big[0] if big else None
        team["_power_rating_candidates"] = big

        ranks = RANK.findall(right)
        team["conf_rank"] = f"#{ranks[0][0]} of {ranks[0][1]}" if ranks else None
        team["natl_rank"] = f"#{ranks[1][0]} of {ranks[1][1]}" if len(ranks) > 1 else None

    page_to_team = {}
    for team in teams:
        page_to_team[team["page"]] = team["team"]
        page_to_team[team["page"] + 1] = team["team"]

    # --- coordinators (guide mentions, not a complete roster) ----------------
    found = {}
    for n, text in page_text.items():
        flat = flatten(text)
        for role, pattern in COORD_PATTERNS:
            for m in pattern.finditer(flat):
                found.setdefault((role, m.group(1).strip()), set()).add(n)
    coordinators = [
        {
            "role": role,
            "name": name,
            "pages": sorted(pages),
            "teams": sorted({page_to_team[p] for p in pages if p in page_to_team}),
        }
        for (role, name), pages in sorted(found.items())
    ]

    # --- new head coach profiles (Coaching Carousel, pp. 28-37) --------------
    carousel = []
    for n in range(29, 38):
        for size, text in page_spans(doc, n - 1):
            if 34 <= size <= 38:
                carousel.append({"name": text, "page": n})

    # --- Paul Stone's Top 15 quarterbacks (p. 45) ---------------------------
    flat45 = flatten(page_text[45])
    qbs = {}
    for rank, qb, team in re.findall(
        r"(\d{1,2})\.\s+([A-Z][A-Z'\.\- ]+?),\s+([A-Z][A-Za-z'\.\-& ]+?)(?=\s+[A-Z][a-z])",
        flat45,
    ):
        if 1 <= int(rank) <= 15:
            qbs[int(rank)] = {"rank": int(rank), "qb": qb.strip().title(),
                              "team": team.strip()}
    quarterbacks = [qbs[k] for k in sorted(qbs)]

    # --- Matt Youmans' Preseason Top 50 (pp. 16-20) -------------------------
    flat_top50 = "".join(page_text[p] for p in range(16, 21))
    seen = {}
    for rank, team in re.findall(r"^(\d{1,2})\.\s+([A-Z][A-Za-z'\.\-&\( \)]+)\s*$",
                                 flat_top50, re.M):
        rank = int(rank)
        if 1 <= rank <= 50 and rank not in seen:
            seen[rank] = team.strip()
    top50 = [{"rank": k, "team": v} for k, v in sorted(seen.items())]

    # --- best-bet contributors (pp. 5-15) -----------------------------------
    contributors, order = [], []
    for n in range(5, 16):
        for size, text in page_spans(doc, n - 1):
            if 10.5 <= size <= 11.5 and re.fullmatch(r"[A-Z][A-Z\.' ]{3,30}", text):
                if text not in order:
                    order.append(text)
                    contributors.append({"contributor": text.title(), "page": n})

    # --- abbreviation glossary (p. 2) ---------------------------------------
    block = page_text[2]
    block = block[block.find("ATS – Against"):block.find("COMMON ABBREVIATIONS")]
    block = re.sub(r"\s+", " ", block).replace("•", " ")
    key = re.compile(r"([A-Z][A-Za-z0-9/#’']*(?:\s+(?:FA|STRG|BR|PR))?)\s+[–-]\s+")
    marks = list(key.finditer(block))
    abbreviations = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(block)
        abbreviations.append({"abbr": m.group(1).strip(),
                              "meaning": block[m.end():end].strip().rstrip(" ,")})

    bundle = {
        "conferences": conferences,
        "teams": teams,
        "coordinators": coordinators,
        "new_head_coaches": carousel,
        "quarterbacks_top15": quarterbacks,
        "youmans_top50": top50,
        "contributors": contributors,
        "abbreviations": abbreviations,
        "offensive_stat_categories": OFFENSIVE_STATS,
        "defensive_stat_categories": DEFENSIVE_STATS,
        "features": [{"page": p, "title": t} for p, t in FEATURES],
        "page_count": doc.page_count,
    }
    for name, payload in bundle.items():
        with open(os.path.join(data_dir, f"{name}.json"), "w") as fh:
            json.dump(payload, fh, indent=1)
    return bundle


def validate(bundle):
    """Fail loudly rather than emit a library built on bad extraction."""
    problems = []
    teams = bundle["teams"]

    if len(teams) != 138:
        problems.append(f"expected 138 teams, got {len(teams)}")
    if len(bundle["conferences"]) != 11:
        problems.append(f"expected 11 conferences, got {len(bundle['conferences'])}")

    for field in ("head_coach", "su_2025", "power_rating", "conf_rank", "natl_rank"):
        blank = [t["team"] for t in teams if not t.get(field)]
        if blank:
            problems.append(f"{field} missing for: {blank[:5]}")

    ambiguous = [t["team"] for t in teams if len(t["_power_rating_candidates"]) != 1]
    if ambiguous:
        problems.append(f"ambiguous power rating on: {ambiguous[:5]}")

    ranks = sorted(int(t["natl_rank"].split()[0][1:]) for t in teams)
    if ranks != list(range(1, 139)):
        problems.append("national ranks are not a complete 1-138 sequence")

    # A higher power rating must never sit below a worse national rank.
    ordered = sorted(teams, key=lambda t: int(t["natl_rank"].split()[0][1:]))
    for a, b in zip(ordered, ordered[1:]):
        if float(b["power_rating"]) > float(a["power_rating"]) + 1e-9:
            problems.append(f"rank/rating inversion: {a['team']} vs {b['team']}")

    if len(bundle["quarterbacks_top15"]) != 15:
        problems.append("Top 15 quarterbacks incomplete")
    if len(bundle["youmans_top50"]) != 50:
        problems.append("Youmans Top 50 incomplete")

    return problems


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "2026-VSiN-CFB-Betting-Guide.pdf"
    out = sys.argv[2] if len(sys.argv) > 2 else "_source"
    data = extract(pdf, out)
    issues = validate(data)
    print(f"pages          {data['page_count']}")
    print(f"conferences    {len(data['conferences'])}")
    print(f"teams          {len(data['teams'])}")
    print(f"coordinators   {len(data['coordinators'])}")
    print(f"new HC files   {len(data['new_head_coaches'])}")
    print(f"abbreviations  {len(data['abbreviations'])}")
    if issues:
        print("\nVALIDATION FAILED")
        for issue in issues:
            print("  -", issue)
        sys.exit(1)
    print("\nvalidation passed")
