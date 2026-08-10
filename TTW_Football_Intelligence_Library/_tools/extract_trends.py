#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 10 (Historical Trends) extraction
============================================================================

Pulls every historical claim the guide prints from the 67 pages Phase 1
flagged as carrying them, and writes `_source/data/trends_raw.json`.

What this tool does NOT do is the point of it. It does not compute a hit
rate, extend a span, backtest a system, or reconcile a printed percentage
against a printed record by changing either. The library has no game-level
historical data -- that is exactly what the auxiliary calibration study
established -- so every figure here is the guide's own, reproduced as
printed and attributed to a page.

Two things in the source are preserved rather than repaired:

  * p. 40's fourth bullet reads "NEW starting quarterbacks ... versus
    returning DEFENSIVE COORDINATORS since 2021". Read against its three
    neighbours the intended comparison is plainly returning starting
    quarterbacks. The text is reproduced as printed and flagged.

  * The first bullet prints 110-132 ATS at 45.4%, where 110/242 rounds to
    45.5%. Recorded as an observation, never corrected.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "_source", "data")
PAGES = os.path.join(ROOT, "_source", "extracted", "pages")

STABILITY = (40, 44)

# A record the guide prints: wins-losses, optionally with pushes.
RECORD = re.compile(r"\b(\d{1,4})-(\d{1,4})(?:-(\d{1,3}))?\s*(SU|ATS)\b")
PERCENT = re.compile(r"\((\d{1,2}(?:\.\d)?)%\)")


def page_text(n):
    with open(os.path.join(PAGES, f"p{n:03d}.txt")) as fh:
        return re.sub(r"\s+", " ", fh.read()).strip()


def reconcile(w, l, pct):
    """Does a printed record reconcile with its printed percentage?

    Reported, never applied. A mismatch is a property of the guide, and
    this library does not adjust either number to make them agree.
    """
    if pct is None or (w + l) == 0:
        return None
    return round(100 * w / (w + l), 1)


def stability_components(t):
    """p. 40's six bullets: each a class of team, with SU and ATS records."""
    out = []
    for chunk in t.split("•")[1:]:
        # The final bullet runs on into the paragraph that follows it, which
        # carries the system's own record. Take the FIRST SU and ATS pair in
        # each chunk rather than requiring exactly one pair, so the last
        # bullet is not silently dropped by its trailing prose.
        chunk = chunk.strip()
        recs = RECORD.findall(chunk)
        pct = PERCENT.search(chunk)
        su = next((r for r in recs if r[3] == "SU"), None)
        ats = next((r for r in recs if r[3] == "ATS"), None)
        if not su or not ats:
            continue
        subject = chunk.split(" are ")[0].strip()
        printed = float(pct.group(1)) if pct else None
        w, l = int(ats[0]), int(ats[1])
        out.append({
            "subject": subject,
            "su_record": f"{su[0]}-{su[1]}" + (f"-{su[2]}" if su[2] else ""),
            "ats_record": f"{ats[0]}-{ats[1]}" + (f"-{ats[2]}" if ats[2] else ""),
            "ats_pct_printed": printed,
            "ats_pct_recomputed": reconcile(w, l, printed),
            "span": "since 2021",
            "window": "first four weeks (Weeks 0-3)",
            "scope": "FBS vs. FBS games only",
            "comparison": chunk.split(" versus ")[-1].split(" since ")[0].strip()
            if " versus " in chunk else None,
            "page": 40,
            "text_as_printed": chunk[:400].strip(),
        })
    return out


def system_record(t):
    """The revised Stability System's records, and last season's.

    Makinen's "official new College Football Stability System(s)" is TWO
    rules, not one, and each carries its own record. An earlier parse took
    only the first and labelled it as the system's record, which understated
    what the guide actually publishes.
    """
    out = []
    RULE = re.compile(r"\((?:FADE record )?(\d+)-\s*(\d+) SU and "
                      r"(\d+)-(\d+)(?:-(\d+))? ATS, (\d{2}\.\d)% "
                      r"since (\d{4})\)")
    labels = ["College Football Stability System — PLAY ON rule",
              "College Football Stability System — FADE rule"]
    conditions = [
        ("Play ON any team with a STABILITY SCORE EDGE of 6+ in "
         "non-conference games in the first four weeks (Weeks 0-3), assuming "
         "the game does NOT have a point spread of -30 or higher for either "
         "team."),
        ("Play AGAINST any team with STABILITY SCORES of 0-6 in "
         "non-conference games in the first four weeks (Weeks 0-3) versus "
         "teams with higher scores, assuming the game does NOT have a point "
         "spread of -30 or higher for either team."),
    ]
    for i, m in enumerate(RULE.finditer(t)):
        if i >= len(labels):
            break
        w, l = int(m.group(3)), int(m.group(4))
        ats = f"{m.group(3)}-{m.group(4)}" + (f"-{m.group(5)}" if m.group(5) else "")
        out.append({
            "label": labels[i],
            "condition": conditions[i],
            "su_record": f"{m.group(1)}-{m.group(2)}",
            "ats_record": ats,
            "ats_pct_printed": float(m.group(6)),
            "ats_pct_recomputed": reconcile(w, l, float(m.group(6))),
            "span": f"since {m.group(7)}",
            "page": 40,
        })
    m = re.search(r"only two losing seasons, one of them being last year", t)
    if m:
        out.append({
            "label": "Revised Stability Score Edge System — losing seasons",
            "condition": None,
            "su_record": None, "ats_record": None,
            "ats_pct_printed": None, "ats_pct_recomputed": None,
            "span": "the last 13 years",
            "page": 40,
            "note": ("Makinen reports that regression on the tweaked system "
                     "found only two losing seasons in 13 years, one of them "
                     "2025."),
        })
    m = re.search(r"teams with 0-6 scores, even lost a year ago, as they "
                  r"were (\d+)-(\d+) ATS", t)
    if m:
        out.append({
            "label": "FADE rule — 2025 season",
            "condition": None,
            "su_record": None,
            "ats_record": f"{m.group(1)}-{m.group(2)}",
            "ats_pct_printed": None,
            "ats_pct_recomputed": reconcile(int(m.group(1)), int(m.group(2)), 0),
            "span": "2025 season",
            "page": 40,
            "note": "The second angle lost last year too.",
        })
    m = re.search(r"final record wound up being just (\d+)-(\d+) ATS", t)
    if m:
        out.append({
            "label": "College Football Stability System — 2025 season",
            "su_record": None,
            "ats_record": f"{m.group(1)}-{m.group(2)}",
            "ats_pct_printed": None,
            "ats_pct_recomputed": reconcile(int(m.group(1)), int(m.group(2)), 0),
            "span": "2025 season",
            "page": 40,
            "note": ("The guide reports this as a failure it is responding "
                     "to, not as a supporting figure. It travels with the "
                     "long-run record wherever that is quoted."),
        })
    return out


# Every team's left-hand page prints a header block of last-season records in
# the form "7-6 SU & ATS, 5-8 O-U". Those are not trends -- they are one
# season's results, and Phase 3 already holds them for all 138 teams as
# su_2025 / ats_2025 / ou_2025. Matching them here would pad the trend
# register with 138 rows of data the library already has, so they are
# separated out rather than counted.
HEADER_BLOCK = re.compile(r"\bO-U\b|\b\d+(?:st|nd|rd|th) season\b", re.I)

# Most historical claims in this guide are argued in prose rather than
# tabulated as an SU/ATS record: "only five non-quarterbacks have won since
# 2000", "three of the last four winners", "has never had a losing season
# three years in a row". A record-only pattern finds almost none of them, so
# the sweep looks for a SPAN marker -- the thing that makes a claim historical
# -- and captures the sentence around it for triage.
# A period followed by whitespace and a capital, a bullet, or a digit-paren
# list marker. Decimals inside figures do not match.
SENT_END = re.compile(r"\.(?=\s+(?:[A-Z“”\"']|\d\)|•))")

SPAN = re.compile(
    r"\b(?:since (?:19|20)\d\d"
    r"|(?:in|over|across) the (?:last|past) (?:\w+|\d+) (?:season|year|game|"
    r"week|decade)s?"
    r"|\d+ of the last \d+"
    r"|(?:three|four|five|six|seven|eight|nine|ten|\d+) (?:of the )?last "
    r"(?:\w+ )?(?:winners|seasons|years)"
    r"|(?:has|have) (?:never|not) .{0,40}\bsince\b"
    r"|(?:straight up|ATS) over the (?:last|past)"
    r"|(?:consecutive|straight) (?:losing |winning )?seasons"
    r"|(?:for the )?first time since (?:19|20)\d\d)\b", re.I)


def sweep(pages):
    """Narrative historical claims: printed records that are argued, not
    tabulated in a team header block."""
    out, header = [], 0
    for p in pages:
        try:
            t = page_text(p)
        except FileNotFoundError:
            continue
        # Sentence boundaries must not break on decimals. These trends are
        # full of them -- "-0.500 ATS", "15.4%", "8.7 wins" -- and splitting
        # on any period truncated a system statement mid-figure.
        bounds = [0] + [m.end() for m in SENT_END.finditer(t)] + [len(t)]
        seen = set()
        for m in SPAN.finditer(t):
            lo = max((b for b in bounds if b <= m.start()), default=0)
            hi = min((b for b in bounds if b >= m.end()), default=len(t))
            sentence = t[lo:hi].strip()
            # A team page's statistics block has no sentence punctuation, so
            # a span phrase near it captures a wall of figures rather than a
            # claim. Reject anything that is mostly numbers.
            words = sentence.split()
            numeric = sum(1 for w in words
                          if re.fullmatch(r"[\d.:%+-]+", w))
            if (HEADER_BLOCK.search(sentence) or len(sentence) < 25
                    or (words and numeric / len(words) > 0.4)):
                header += 1
                continue
            if sentence in seen:
                continue
            seen.add(sentence)
            rec = RECORD.search(sentence)
            out.append({
                "page": p,
                "span_phrase": m.group(0),
                "record": rec.group(0) if rec else None,
                "sentence": sentence[:400].rstrip()
                            + ("…" if len(sentence) > 400 else ""),
            })
    return out, header


def main():
    concepts = json.load(open(os.path.join(DATA, "concept_pages.json")))
    hist = concepts["Historical Angles"]

    t40 = page_text(40)
    components = stability_components(t40)
    if len(components) != 6:
        sys.exit(f"p. 40: parsed {len(components)} stability bullets, expected 6")
    systems = system_record(t40)

    others, header_rows = sweep([p for p in hist if p != 40])

    typo = [c for c in components
            if "starting quarterback" in c["subject"].lower()
            and c["comparison"] and "coordinator" in c["comparison"].lower()]
    mismatch = [c for c in components + systems
                if c["ats_pct_printed"] is not None
                and c["ats_pct_recomputed"] is not None
                and abs(c["ats_pct_printed"] - c["ats_pct_recomputed"]) >= 0.05]

    out = {
        "stability_pages": list(STABILITY),
        "historical_pages": hist,
        "components": components,
        "systems": systems,
        "narrative_records": others,
        "header_or_fragment_rows_skipped": header_rows,
        "printed_typos": [
            {"page": c["page"], "subject": c["subject"],
             "printed_comparison": c["comparison"],
             "note": ("Read against its three neighbouring bullets the "
                      "intended comparison is returning starting "
                      "quarterbacks. Reproduced as printed, not corrected.")}
            for c in typo],
        "percentage_mismatches": [
            {"page": c.get("page"), "subject": c.get("subject") or c.get("label"),
             "ats_record": c["ats_record"],
             "printed_pct": c["ats_pct_printed"],
             "recomputed_pct": c["ats_pct_recomputed"],
             "note": ("Recorded as an observation. Neither number is "
                      "adjusted to make them agree.")}
            for c in mismatch],
    }
    with open(os.path.join(DATA, "trends_raw.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    print(f"stability components  {len(components)} (p. 40, since 2021)")
    print(f"system records        {len(systems)}")
    print(f"narrative records     {len(others)} across "
          f"{len({o['page'] for o in others})} of {len(hist)} historical pages")
    print(f"header/fragment rows  {header_rows} skipped (team header "
          f"blocks; Phase 3 holds those for all 138 teams)")
    print(f"printed typos flagged {len(typo)}")
    print(f"pct mismatches noted  {len(mismatch)}")


if __name__ == "__main__":
    main()
