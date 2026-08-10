#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 8 (Futures) extraction
=================================================================

Four layers, each read from the page by structure rather than by reading
order, and each written to `_source/data/futures_*.json`:

  A. p. 4      2026 Season Predictions. A 17-category by 22-contributor
               grid. Phase 2 stored this as anonymous 22-long lists; the
               whole point of Phase 8 is that each cell belongs to a named
               person. Cells are assigned to a contributor by x-column
               against the printed header, never by reading order, because
               a single dropped cell in reading order would silently
               misattribute picks to real people for the rest of the row.

  B. pp. 5-15  VSiN Host College Football Best Bets. The page distinguishes
               a contributor (Montserrat-Black 11pt) from a pick headline
               (Montserrat-Bold 8pt) from reasoning (everything else) by
               font, so that is what the parser keys on. A contributor's
               run carries across the page break -- p. 6 opens with two
               headlines that belong to p. 5's last contributor.

  C. p. 39     Value in the Heisman Race, by Zach Cohen. Same font logic.

  D. 138 pp.   Each team's right-hand page prints three futures prices in
               a fixed three-row block. Open Question #2 deferred these to
               this phase because text order does not pair price to label.
               It does not need to: the rows sit at fixed y bands with the
               price left of the label, so both are read by coordinate.

Nothing here resolves a conflict, adjusts an odd-looking price, or merges
two contributors' opinions.
"""

import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = os.path.join(ROOT, "_source", "2026-VSiN-CFB-Betting-Guide.pdf")
DATA = os.path.join(ROOT, "_source", "data")

PRED_PAGE = 4
BETS_FIRST, BETS_LAST = 5, 15
HEISMAN_PAGE = 39

# ---------------------------------------------------------------- layer A

# Column order on p. 4 is alphabetical by surname. The roster is enumerated
# rather than parsed: the header prints each name as two rotated tokens whose
# vertical order does not reliably put the surname first (column 3 reads
# BURKE/ADAM, column 12 reads MITCH/MOSS), so the tokens are asserted against
# this list instead of being ordered heuristically. If the guide's header ever
# differs from this roster the extractor stops rather than guessing.
PRED_ROSTER = [
    "Femi Abebefe", "Matt Brown", "Stormy Buonantony", "Adam Burke",
    "Zachary Cohen", "Sean Green", "Paul Howard", "Ryan Kramer",
    "Jensen Lewis", "Steve Makinen", "John McKechnie", "Patrick Meagher",
    "Mitch Moss", "Tim Murray", "Wes Reynolds", "Scott Seidenberg",
    "Tyler Shoemaker", "Paul Stone", "Dustin Swedelson", "Dave Tuley",
    "Matt Youmans", "Jonathan Von Tobel",
]
COL_X0, COL_PITCH, N_COLS = 172.0, 60.72, 22

# The row printed under this label contains NFL team names. Phase 2 recorded
# it; Phase 8 reproduces it as printed and excludes it from conference data.
ANOMALY_LABEL = "SUN BELT CHAMP"


def _header_column(x):
    """Header names are single tokens centred in their column."""
    i = round((x - COL_X0) / COL_PITCH)
    return i if 0 <= i < N_COLS else None


def _cell_column(x):
    """Body cells are LEFT-aligned at the column edge and run rightward.

    Rounding to the nearest column centre splits multi-word picks: in the
    ACC row "Virginia" lands at x=599 and "Tech" at x=633, which rounds
    into the next column and hands Jensen Lewis a pick belonging to Ryan
    Kramer. A word therefore belongs to the last column that starts at or
    before it.
    """
    i = int((x - COL_X0 + 4.0) // COL_PITCH)
    return min(max(i, 0), N_COLS - 1) if x >= COL_X0 - 4.0 else None


def extract_predictions(doc):
    page = doc[PRED_PAGE - 1]
    words = page.get_text("words")

    # Header roster, verified against PRED_ROSTER token-set by token-set.
    header = {}
    for w in words:
        if 70 <= w[1] <= 145:
            i = _header_column(w[0])
            if i is not None:
                header.setdefault(i, set()).add(w[4].strip())
    if len(header) != N_COLS:
        sys.exit(f"p.4 header: {len(header)} columns, expected {N_COLS}")
    for i, name in enumerate(PRED_ROSTER):
        want = set(name.upper().split())
        if header.get(i) != want:
            sys.exit(f"p.4 column {i}: header {sorted(header.get(i, []))} "
                     f"does not match roster entry {name!r}")

    # Category labels sit in the left margin (x < COL_X0); every pick word
    # sits in one of the 22 columns. A category's band runs from its label
    # down to the next label, which lets a wrapped pick ("North Dakota
    # State" spilling onto a second line) rejoin inside its own column.
    labels = []
    for w in words:
        if w[1] > 150 and w[0] < COL_X0 - 2:
            labels.append(w)
    bands = {}
    for w in sorted(labels, key=lambda w: (round(w[1] / 6) * 6, w[0])):
        bands.setdefault(round(w[1] / 6) * 6, []).append(w[4])
    tops = sorted(bands)
    cats = []
    for n, y in enumerate(tops):
        lo = y - 3
        hi = tops[n + 1] - 3 if n + 1 < len(tops) else 10 ** 6
        cats.append((" ".join(bands[y]).strip(), lo, hi))

    out, anomaly = [], None
    for label, lo, hi in cats:
        cells = {}
        for w in words:
            if lo <= w[1] < hi and w[0] >= COL_X0 - 4:
                i = _cell_column(w[0])
                if i is not None:
                    cells.setdefault(i, []).append((w[1], w[0], w[4]))
        if len(cells) != N_COLS:
            sys.exit(f"p.4 {label!r}: {len(cells)} columns filled, "
                     f"expected {N_COLS}")
        picks = []
        for i in range(N_COLS):
            txt = " ".join(t for _, _, t in sorted(cells[i]))
            picks.append({"contributor": PRED_ROSTER[i], "pick": txt.strip()})
        rec = {"category": label, "page": PRED_PAGE, "picks": picks}
        if label == ANOMALY_LABEL:
            rec["anomaly"] = (
                "Printed under a Sun Belt label but containing NFL team "
                "names. Reproduced exactly as printed and excluded from "
                "conference prediction data. Not corrected.")
            anomaly = rec
        out.append(rec)
    return out, anomaly


# ---------------------------------------------------------------- layer B/C

# Some prices are typeset with U+2212 MINUS SIGN rather than an ASCII hyphen
# (Texas Tech's conference price, among others). Normalised on read; the
# stored value is the printed number either way.
DASHES = {"\u2212": "-", "\u2013": "-", "\u2014": "-"}


def _ascii(t):
    return "".join(DASHES.get(c, c) for c in t)


NAME_FONT, NAME_SIZE = "Montserrat-Black", 10.5
PICK_FONT, PICK_SIZE = "Montserrat-Bold", 8.6
CHROME = re.compile(r"^(?:\d{1,3}|2026 VSiN COLLEGE FOOTBALL BETTING GUIDE)$")


def _spans(page):
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            for s in line["spans"]:
                t = s["text"].strip()
                if t:
                    yield s, t


def _kind(s, t):
    if CHROME.match(t):
        return "chrome"
    if s["font"] == NAME_FONT and s["size"] >= NAME_SIZE and t.isupper():
        return "name"
    if s["font"] == PICK_FONT and s["size"] <= PICK_SIZE and t.isupper():
        return "pick"
    return "prose"


LINE_GAP = 14.0     # one line of 8pt headline plus leading
SAME_COL = 3.0      # headline lines in one pick share a left edge


def _flush(picks, open_pick, prose):
    """Close the open pick, attaching whatever prose has accumulated."""
    if open_pick:
        open_pick["prose"] = " ".join(prose).strip()
        picks.append(open_pick)
    prose.clear()


def _read_run(doc, first, last):
    """Walk pages in order, returning [{contributor, page, picks[]}].

    Two things make this geometric rather than textual.

    A contributor's run continues across the page break -- p. 6 opens with
    two pick headlines belonging to Dave Tuley, who is named on p. 5 -- so
    the current contributor persists until the next name span.

    A headline that does not fit on one line is typeset as a second bold
    span directly beneath the first ("PARLAY: NOTRE DAME, OHIO STATE," /
    "TEXAS TO MAKE COLLEGE FOOTBALL PLAYOFF (+115)"). Continuation is
    detected by that adjacency, not by punctuation: keying on a trailing
    "&" alone truncated two picks and dropped their reasoning.
    """
    runs, cur, open_pick, prose, last_box = [], None, None, [], None
    for pg in range(first, last + 1):
        last_box = None                       # a pick never wraps across pages
        for s, t in _spans(doc[pg - 1]):
            k = _kind(s, t)
            if k == "chrome":
                continue
            x0, y0, _, y1 = s["bbox"]
            if k == "name":
                if cur:
                    _flush(cur["picks"], open_pick, prose)
                open_pick, last_box = None, None
                cur = {"contributor": t.title(), "page": pg, "picks": []}
                runs.append(cur)
            elif k == "pick":
                if cur is None:
                    continue
                cont = (last_box is not None
                        and abs(x0 - last_box[0]) <= SAME_COL
                        and 0 < y0 - last_box[1] <= LINE_GAP)
                if cont:
                    open_pick["lines"].append(t)
                else:
                    _flush(cur["picks"], open_pick, prose)
                    open_pick = {"lines": [t], "page": pg}
                last_box = (x0, y0)
            elif cur is not None and open_pick:
                prose.append(t)
                last_box = None               # prose ends any headline wrap
    if cur:
        _flush(cur["picks"], open_pick, prose)
    return runs


PRICE = re.compile(r"\(([+-]?\d+(?:\.\d+)?(?:-1)?)\)?")


def _shape(entry):
    """Normalise one raw pick into the stored record.

    The headline is the wrapped lines rejoined. Legs are then split on the
    "&" the guide itself prints, so a two-leg recommendation stays one
    recommendation. A leg may elide its subject ("PENN STATE OVER 8.5 WINS
    (-160) & TO MAKE COLLEGE FOOTBALL PLAYOFF (+425)"); the elision is left
    as printed rather than expanded.
    """
    headline = _ascii(" ".join(entry["lines"])).strip()
    headline = re.sub(r"\s+", " ", headline)
    legs = [l.strip() for l in headline.split("&") if l.strip()]
    return {
        "headline": headline,
        "legs": legs,
        "prices": PRICE.findall(headline),
        "page": entry["page"],
        "prose": entry["prose"],
        "words": len(entry["prose"].split()),
    }


def extract_best_bets(doc):
    runs = _read_run(doc, BETS_FIRST, BETS_LAST)
    out = []
    for r in runs:
        for p in r["picks"]:
            rec = _shape(p)
            rec["contributor"] = r["contributor"]
            rec["contributor_named_on_page"] = r["page"]
            out.append(rec)
    return out, [r["contributor"] for r in runs]


def extract_heisman(doc):
    page = doc[HEISMAN_PAGE - 1]
    byline = None
    m = re.search(r"\bby ([A-Z][a-z]+(?: [A-Z][a-z]+)+)\s*$",
                  page.get_text().strip())
    if m:
        byline = m.group(1)
    runs = _read_run(doc, HEISMAN_PAGE, HEISMAN_PAGE)
    picks = []
    for r in runs:
        for p in r["picks"]:
            rec = _shape(p)
            rec["player"] = r["contributor"]
            picks.append(rec)
    return {"page": HEISMAN_PAGE, "title": "Value in the Heisman Race",
            "author": byline, "picks": picks}


# ---------------------------------------------------------------- layer D

# The three futures rows sit at fixed y bands on every team's right-hand
# page, price on the left and label on the right.
FUT_BANDS = ((55, 100), (130, 175), (205, 250))
FUT_XSPLIT = 440.0
FUT_PRICE = re.compile(r"^(?:\d+-1|[+-]\d+)$")
def extract_team_futures(doc, teams):
    out = {}
    for t in teams:
        page = doc[t["pages"][1] - 1]      # the right-hand page
        words = [w for w in page.get_text("words") if w[0] > 370]
        rows = []
        for lo, hi in FUT_BANDS:
            band = sorted((w for w in words if lo <= w[1] <= hi),
                          key=lambda w: w[0])
            price = [_ascii(w[4]) for w in band
                     if w[0] < FUT_XSPLIT and FUT_PRICE.match(_ascii(w[4]))]
            label = [w[4] for w in band if w[0] >= FUT_XSPLIT]
            market = " ".join(label).strip()
            # Independents print the conference row's label with no price at
            # all -- there is no conference title market for them. That is a
            # property of the source, recorded as an absence, never filled in.
            rows.append({"market": market,
                         "price": price[0] if len(price) == 1 else None,
                         "prices_found": len(price),
                         "no_price_printed": len(price) == 0 and bool(market)})
        out[t["team"]] = {"page": t["pages"][1], "rows": rows}
    return out


# ---------------------------------------------------------------- main

def main():
    doc = pymupdf.open(PDF)
    teams = json.load(open(os.path.join(DATA, "team_details.json")))

    preds, anomaly = extract_predictions(doc)
    bets, roster = extract_best_bets(doc)
    heis = extract_heisman(doc)
    fut = extract_team_futures(doc, teams)

    def dump(name, obj):
        with open(os.path.join(DATA, name), "w") as fh:
            json.dump(obj, fh, indent=1, ensure_ascii=False)
            fh.write("\n")

    dump("futures_predictions.json",
         {"page": PRED_PAGE, "title": "2026 Season Predictions",
          "roster": PRED_ROSTER, "categories": preds})
    dump("futures_best_bets.json",
         {"pages": [BETS_FIRST, BETS_LAST],
          "title": "VSiN Host College Football Best Bets",
          "roster": roster, "bets": bets})
    dump("futures_heisman.json", heis)
    dump("futures_team_prices.json", fut)

    bad = {t: v for t, v in fut.items()
           if any(r["prices_found"] > 1 or not r["market"] for r in v["rows"])}
    absent = sorted(t for t, v in fut.items()
                    if any(r["no_price_printed"] for r in v["rows"]))
    print(f"predictions   {len(preds)} categories x {N_COLS} contributors "
          f"= {len(preds) * N_COLS} attributed cells"
          f"{'  (incl. 1 anomaly row)' if anomaly else ''}")
    print(f"best bets     {len(bets)} picks by {len(set(b['contributor'] for b in bets))} "
          f"contributors, pp. {BETS_FIRST}-{BETS_LAST}")
    print(f"              {sum(len(b['legs']) > 1 for b in bets)} multi-leg, "
          f"{sum(b['words'] for b in bets):,} words of reasoning")
    print(f"heisman       {len(heis['picks'])} picks by {heis['author']}, "
          f"p. {HEISMAN_PAGE}")
    print(f"team futures  {len(fut)} teams x 3 rows = {len(fut) * 3} markets, "
          f"{sum(1 for v in fut.values() for r in v['rows'] if r['price'])} "
          f"prices printed"
          f"{f'  UNRESOLVED: {sorted(bad)[:4]}' if bad else ''}")
    print(f"              no conference price printed: {absent or 'none'}")


if __name__ == "__main__":
    main()
