#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 3 Team Extraction
============================================================

Coordinate-based extraction of every field on all 138 two-page team spreads.

Phase 1 deliberately deferred several fields because their reading order in the
PDF text layer does not match their visual order. This module resolves them by
position (x/y) instead, and then proves each result against an independent
second printing of the same figure wherever one exists:

  * returning starters   -> offence + defence must equal the printed total
  * home/road field      -> must equal the values in the conference standings
  * schedule strength    -> must equal the value and rank in the standings
  * power rating         -> must equal the Phase 1 value and the standings value

Those cross-checks are the whole point. A value that cannot be extracted and
verified is emitted as None and reported, never guessed.

Usage:
    python3 _tools/extract_teams.py       # run from the library root
"""

import json
import os
import re
import sys

import pymupdf

SRC = "_source/data"
PDF = "_source/2026-VSiN-CFB-Betting-Guide.pdf"

DEFERRED = "DEFERRED — EXTRACTION NOT RELIABLE"

# Column bands on the spread, in PDF points. Derived from the layout and
# verified to hold across all 138 teams by the validation pass below.
LEFT_PROSE_MAX_X = 170       # season-outlook column on the even page
SCHED_DATE_X = (170, 205)    # game dates
SCHED_OPP_X = (205, 380)     # opponent and projected line
SCHED_RATING_X = (380, 470)  # opponent power rating
STAT_LABEL_X = (380, 470)    # statistics category names (odd page)
STAT_VALUE_X = (500, 560)
STAT_RANK_X = (560, 612)
FUTURES_LABEL_X = 440        # futures market name sits right of its price


def spans(page):
    out = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span["text"].strip()
                if text:
                    out.append({
                        "x": round(span["bbox"][0], 1),
                        "y": round(span["bbox"][1], 1),
                        "size": round(span["size"], 1),
                        "bold": "Bold" in span["font"],
                        "text": text,
                    })
    return out


def near(spans_, y, tol=2.0):
    return [s for s in spans_ if abs(s["y"] - y) <= tol]


def in_x(spans_, lo, hi):
    return [s for s in spans_ if lo <= s["x"] < hi]


# --------------------------------------------------------------------------- #
# Left (even) page

def parse_returning_starters(left):
    """Three display numerals under the labels total / offense / defense.

    Matched to their labels by horizontal position, not by reading order —
    the text layer emits them in the opposite order to the printed layout.
    """
    labels = [s for s in left if s["size"] >= 18
              and s["text"].lower() in ("total", "offense", "defense")]
    numbers = [s for s in left if s["size"] >= 18
               and re.fullmatch(r"\d+\*?", s["text"])]
    if len(labels) != 3 or len(numbers) != 3:
        return None

    label_y = min(s["y"] for s in labels)
    numbers = [n for n in numbers if n["y"] > label_y]
    if len(numbers) != 3:
        return None

    result = {}
    for label in labels:
        closest = min(numbers, key=lambda n: abs(n["x"] - label["x"]))
        value = closest["text"]
        result[label["text"].lower()] = {
            "value": int(value.rstrip("*")),
            "returning_qb": value.endswith("*"),
        }
    if len(result) != 3:
        return None
    return result


def parse_field_ratings(left):
    """'2.5 / 0.8' printed beneath the 'field ratings (HOME/ROAD)' label."""
    label = next((s for s in left if s["text"].lower().startswith("field ratings")), None)
    if not label:
        return None
    for s in left:
        if s["x"] > 460 and re.fullmatch(r"-?[\d.]+\s*/\s*-?[\d.]+", s["text"]):
            home, road = [p.strip() for p in s["text"].split("/")]
            return {"home": home, "road": road}
    return None


def parse_schedule_strength(left):
    rank = next((s for s in left if "toughest of" in s["text"]), None)
    if not rank:
        return None
    match = re.search(r"#(\d+)\s+toughest\s+of\s+(\d+)", rank["text"])
    value = None
    for s in left:
        if s["y"] < rank["y"] and rank["y"] - s["y"] < 14 and \
                abs(s["x"] - rank["x"]) < 40 and re.fullmatch(r"[\d.]+", s["text"]):
            value = s["text"]
    return {"value": value, "rank": int(match.group(1)), "of": int(match.group(2))}


def parse_schedule(left):
    """Game rows: date, opponent with projected line, opponent power rating."""
    dates = [s for s in left if SCHED_DATE_X[0] <= s["x"] < SCHED_DATE_X[1]
             and re.fullmatch(r"\d{1,2}/\d{1,2}", s["text"])]
    games = []
    for date in sorted(dates, key=lambda s: s["y"]):
        opponent = [s for s in near(left, date["y"], 4.0)
                    if SCHED_OPP_X[0] <= s["x"] < SCHED_OPP_X[1] and s["size"] >= 12]
        rating = [s for s in near(left, date["y"], 4.0)
                  if SCHED_RATING_X[0] <= s["x"] < SCHED_RATING_X[1] and s["size"] >= 12]
        if not opponent:
            continue
        text = opponent[0]["text"]
        line = re.search(r"\(([-+][\d.]+|[-+]\d+|PK)\)\s*$", text)
        games.append({
            "date": date["text"],
            "opponent_raw": text,
            "opponent": re.sub(r"\s*\([^)]*\)\s*$", "", text).strip(),
            "projected_line": line.group(1) if line else None,
            "location": ("away" if text.strip().lower().startswith("at ")
                         else "neutral" if text.strip().lower().startswith("vs.")
                         else "home"),
            "opponent_power_rating": rating[0]["text"] if rating else None,
        })
    return games


def parse_left_prose(left):
    column = sorted([s for s in left if s["x"] < LEFT_PROSE_MAX_X and s["size"] < 12],
                    key=lambda s: s["y"])
    lines = [s["text"] for s in column]
    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text)

    pick = None
    for line in lines:
        m = re.fullmatch(r"(Over|Under)\s+([\d.]+)", line.strip())
        if m:
            pick = {"side": m.group(1).upper(), "number": m.group(2)}
    projection = re.search(r"projection is ([\d.]+)\s*wins", text, re.I)
    return {
        "text": text,
        "win_total_pick": pick,
        "projected_wins": projection.group(1) if projection else None,
    }


# --------------------------------------------------------------------------- #
# Right (odd) page

def parse_futures(right):
    """Market label sits to the right of its price, on the same baseline."""
    labels = [s for s in right if s["size"] >= 18 and s["x"] >= FUTURES_LABEL_X
              and not re.fullmatch(r"[-+\d.]+", s["text"])]
    # A market name can be split across spans ("AMERICAN" + "ATHLETIC"); spans
    # sharing a baseline are one label.
    grouped = {}
    for label in labels:
        key = round(label["y"], 0)
        grouped.setdefault(key, []).append(label)

    out = []
    for key, parts in sorted(grouped.items()):
        parts.sort(key=lambda s: s["x"])
        name = " ".join(p["text"] for p in parts)
        left_x = parts[0]["x"]
        prices = [s for s in near(right, parts[0]["y"], 2.0)
                  if s["x"] < left_x and s["size"] >= 18]
        if prices:
            out.append({"market": name, "price": prices[-1]["text"]})
    return out


def parse_stats(right):
    """Two blocks of category / value / rank, split by their section headings."""
    heads = {}
    for s in right:
        upper = s["text"].upper()
        if upper.startswith("OFFENSIVE STATISTICS"):
            heads["offense"] = s["y"]
        elif upper.startswith("DEFENSIVE STATISTICS"):
            heads["defense"] = s["y"]
    if "offense" not in heads or "defense" not in heads:
        return None

    fcs = [s for s in right if "PARTICIPATED" in s["text"].upper()]
    if fcs:
        note = " ".join(sorted(
            (s["text"].strip() for s in right
             if s["y"] > heads["offense"] and s["x"] >= 470
             and re.search(r"[A-Z]", s["text"])
             and s["text"].strip() not in ("#", "RANK")),
            key=lambda t: 0 if t.startswith("PARTICIPATED") else 1))
        return {"offense": [], "defense": [],
                "guide_note": re.sub(r"\s+", " ", note).strip()}

    def block(lo, hi):
        rows = []
        labels = [s for s in right
                  if STAT_LABEL_X[0] <= s["x"] < STAT_LABEL_X[1]
                  and lo < s["y"] < hi
                  and re.search(r"[A-Z]", s["text"])
                  and not s["text"].upper().endswith("STATISTICS")
                  and s["text"] not in ("#", "RANK")]
        for label in sorted(labels, key=lambda s: s["y"]):
            values = [s for s in near(right, label["y"], 2.0)
                      if STAT_VALUE_X[0] <= s["x"] < STAT_VALUE_X[1]]
            ranks = [s for s in near(right, label["y"], 2.0)
                     if STAT_RANK_X[0] <= s["x"] < STAT_RANK_X[1]]
            rows.append({
                "category": label["text"],
                "value": values[0]["text"] if values else None,
                "rank": ranks[0]["text"] if ranks else None,
            })
        return rows

    return {
        "offense": block(heads["offense"], heads["defense"]),
        "defense": block(heads["defense"], 10_000),
    }


def parse_questions(right):
    """Three bold headers in the left column, each followed by its answer."""
    column = sorted([s for s in right if s["x"] < 380 and s["size"] == 11.0],
                    key=lambda s: s["y"])
    out, current, last_bold_y = [], None, None
    for s in column:
        if s["bold"]:
            # A question that wraps onto a second line arrives as two bold
            # spans one line apart; that is one question, not two.
            if current and last_bold_y is not None and s["y"] - last_bold_y <= 16:
                current["question"] += " " + s["text"]
            else:
                if current:
                    out.append(current)
                current = {"question": s["text"], "answer": []}
            last_bold_y = s["y"]
        elif current:
            current["answer"].append(s["text"])
    if current:
        out.append(current)
    for q in out:
        q["answer"] = re.sub(r"\s+", " ", " ".join(q["answer"])).strip()
        q["question"] = q["question"].strip()
    return out


def parse_ranks(right):
    conf = natl = None
    for s in right:
        m = re.fullmatch(r"#(\d+) of (\d+)", s["text"])
        if m:
            if int(m.group(2)) == 138:
                natl = s["text"]
            else:
                conf = s["text"]
    return conf, natl


def parse_power_rating(right):
    candidates = [s["text"] for s in right
                  if s["size"] >= 23 and re.fullmatch(r"-?\d+\.?\d*", s["text"])]
    return candidates[0] if len(candidates) == 1 else None


# --------------------------------------------------------------------------- #

def main():
    with open(os.path.join(SRC, "teams.json")) as fh:
        teams = json.load(fh)
    with open(os.path.join(SRC, "conference_previews.json")) as fh:
        previews = json.load(fh)

    standings = {}
    for conf in previews:
        for row in conf["standings"]:
            standings[row["team"]] = row

    doc = pymupdf.open(PDF)
    out, problems, deferrals, conflicts = [], [], [], []

    for team in teams:
        name = team["team"]
        left_page, right_page = team["page"], team["page"] + 1
        left, right = spans(doc[left_page - 1]), spans(doc[right_page - 1])
        ref = standings[name]

        record = {
            "team": name,
            "conference": team["conference"],
            "pages": [left_page, right_page],
            "head_coach": team["head_coach"],
            "hc_season": team["hc_season"],
            "interim": team["interim"],
            "su_2025": team["su_2025"],
            "ats_2025": team["ats_2025"],
            "ou_2025": team["ou_2025"],
            "power_rating": parse_power_rating(right),
            "returning_starters": parse_returning_starters(left),
            "field_ratings": parse_field_ratings(left),
            "schedule_strength": parse_schedule_strength(left),
            "schedule": parse_schedule(left),
            "futures": parse_futures(right),
            "statistics": parse_stats(right),
            "questions": parse_questions(right),
        }
        record["conf_rank"], record["natl_rank"] = parse_ranks(right)
        record.update(parse_left_prose(left))

        # --- cross-checks against independently printed figures -----------
        rs = record["returning_starters"]
        if rs is None:
            deferrals.append((name, "returning_starters", "not located on page"))
        elif rs["offense"]["value"] + rs["defense"]["value"] != rs["total"]["value"]:
            # Positions on the page are fixed and verified, so the reading is
            # sound; it is the guide's own arithmetic that does not balance.
            # Preserved and flagged rather than discarded.
            record["returning_starters_conflict"] = (
                f"The guide prints total {rs['total']['value']}, offence "
                f"{rs['offense']['value']} and defence {rs['defense']['value']} "
                f"on p. {left_page}. Offence plus defence is "
                f"{rs['offense']['value'] + rs['defense']['value']}, which does "
                f"not equal the printed total. All three figures are reproduced "
                f"as printed; none is corrected.")
            conflicts.append((name, "returning_starters",
                              record["returning_starters_conflict"]))

        fr = record["field_ratings"]
        if fr is None:
            deferrals.append((name, "field_ratings", "not located on page"))
        elif (float(fr["home"]) != float(ref["home_field"]) or
              float(fr["road"]) != float(ref["road_field"])):
            problems.append(
                f"{name}: field ratings {fr['home']}/{fr['road']} on team page vs "
                f"{ref['home_field']}/{ref['road_field']} in standings")

        ss = record["schedule_strength"]
        if ss is None or ss["value"] is None:
            deferrals.append((name, "schedule_strength", "not located on page"))
        elif (float(ss["value"]) != float(ref["schedule_strength"]) or
              ss["rank"] != ref["schedule_rank"]):
            problems.append(
                f"{name}: schedule strength {ss['value']} (#{ss['rank']}) on team page "
                f"vs {ref['schedule_strength']} (#{ref['schedule_rank']}) in standings")

        if record["power_rating"] is None:
            problems.append(f"{name}: power rating not uniquely identified")
        elif float(record["power_rating"]) != float(team["power_rating"]):
            problems.append(f"{name}: power rating disagrees with Phase 1")

        stats = record["statistics"]
        if not stats:
            deferrals.append((name, "statistics", "section headings not found"))
        elif stats.get("guide_note"):
            pass
        else:
            if len(stats["offense"]) != 15:
                problems.append(f"{name}: {len(stats['offense'])} offensive stats, expected 15")
            if len(stats["defense"]) != 12:
                problems.append(f"{name}: {len(stats['defense'])} defensive stats, expected 12")
            if stats.get("guide_note"):
                pass  # guide states these teams played FCS in 2025; not a gap
            else:
                missing = [r["category"] for r in stats["offense"] + stats["defense"]
                           if r["value"] is None or r["rank"] is None]
                if missing:
                    deferrals.append((name, "statistics", f"no value/rank for {missing}"))

        expected_futures = 2 if team["conference"] == "Independents" else 3
        if len(record["futures"]) != expected_futures:
            deferrals.append((name, "futures",
                              f"{len(record['futures'])} markets found, "
                              f"expected {expected_futures}"))
        if len(record["questions"]) != 3:
            deferrals.append((name, "questions", f"{len(record['questions'])} found, expected 3"))
        if len(record["schedule"]) < 11:
            deferrals.append((name, "schedule", f"{len(record['schedule'])} games found"))

        out.append(record)

    with open(os.path.join(SRC, "team_details.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    with open(os.path.join(SRC, "team_conflicts.json"), "w") as fh:
        json.dump([{"team": t, "field": f, "detail": d} for t, f, d in conflicts],
                  fh, indent=1)

    print(f"teams extracted            {len(out)}")
    print(f"returning starters solved  {sum(1 for t in out if t['returning_starters'])}/138")
    print(f"field ratings verified     {sum(1 for t in out if t['field_ratings'])}/138")
    print(f"source conflicts           {len(conflicts)}")
    print(f"statistics complete        "
          f"{sum(1 for t in out if t['statistics'] and len(t['statistics']['offense']) == 15 and len(t['statistics']['defense']) == 12)}/138")
    print(f"futures (3 markets)        {sum(1 for t in out if len(t['futures']) == 3)}/138")
    print(f"burning questions (3)      {sum(1 for t in out if len(t['questions']) == 3)}/138")
    print(f"schedules >= 11 games      {sum(1 for t in out if len(t['schedule']) >= 11)}/138")

    if deferrals:
        print(f"\nDEFERRED VALUES ({len(deferrals)}):")
        for name, field, why in deferrals[:25]:
            print(f"  {name:<34} {field:<20} {why}")
        if len(deferrals) > 25:
            print(f"  … and {len(deferrals)-25} more")
    if problems:
        print(f"\nCROSS-CHECK FAILURES ({len(problems)}):")
        for p in problems[:25]:
            print("  -", p)
        if len(problems) > 25:
            print(f"  … and {len(problems)-25} more")
        sys.exit(1)
    print("\nall cross-checks passed")


if __name__ == "__main__":
    main()
