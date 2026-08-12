#!/usr/bin/env python3
"""
TTW Football Intelligence Library — cross-database conflict index
==================================================================

Maintenance repair for defect **N-2**, found by Live Retrieval Test #2.

The Team Database's §27 *Source Conflicts* was built from Phase 3's own
data only. Every other phase recorded its conflicts in its own database and
nowhere else, so a team whose only conflict lived in Phase 4, 5, 7 or 8 had
a §27 that read "No source conflict identified for this team." — an
assertion the library could not support. UNLV Rebels asserted no conflict
while Phase 7 recorded three.

This module is the single place that answers, for a canonical team, *what
conflicts has any completed phase recorded about it*. It reads the same
authored source records the owning phase reads — `_source/qb/*.json`,
`_source/coaching/*.json`, `_source/wintotals/*.json`, the conference and
feature tables, the futures price table — so nothing is re-derived from
rendered markdown and no build-order dependency is created between
directories.

Three rules govern what comes out:

  * **Nothing is merged.** Each record keeps the wording of the layer that
    authored it, and each is attributed to that layer by name and by link.
    Where two phases record the same disagreement in different words, both
    survive; the library does not decide which phrasing is the real one.

  * **Nothing is adjudicated.** No record is resolved, ranked or corrected
    here. That is Phase 11's rule for the search layer and it holds just as
    firmly for a cross-reference.

  * **Kinds are not flattened.** A guide contradiction, an unresolved
    ambiguity, a recorded absence and a defect in a TTW artefact are four
    different things. Each carries the title its own phase gave it.

Canonical identity is the enumerated bijection every phase already uses.
Teams are keyed by their full canonical name; no substring, prefix or fuzzy
match is performed anywhere in this file.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

NOT_ADDRESSED = "Not addressed in guide."


def _slug(name):
    """The one canonical slug, matching coach_lib.slug and build_teams.slug."""
    s = name.lower().replace("’", "").replace("'", "").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def _clean(text):
    """A conflict record as its author wrote it, on one markdown table line.

    Only line breaks are removed — nothing is reworded, shortened or
    re-punctuated. A record whose value is the absence marker is not a
    record.
    """
    if not text:
        return None
    t = " ".join(str(text).split())
    if not t or t == NOT_ADDRESSED:
        return None
    return t


# --------------------------------------------------------------- collectors
#
# Each collector yields (team, record). A record is:
#   phase    the phase that authored it
#   title    the kind, in that phase's own language — never generalised
#   detail   that phase's own wording, verbatim
#   where    human-readable citation of the field or page it lives in
#   link     relative path from 02_Team_Database to the authoring artifact

def _qb_records():
    """Phase 4, field 23 — Source conflicts / ambiguities."""
    from qb_lib import load_qb_notes
    for team, rec in load_qb_notes().items():
        detail = _clean(rec.get("conflicts"))
        if not detail:
            continue
        yield team, {
            "phase": 4,
            "title": "Quarterback Database — source conflict / ambiguity.",
            "detail": detail,
            "where": "field 23 of this team's quarterback record",
            "link": f"../04_Quarterback_Database/{_slug(team)}.md",
        }


def _coaching_records():
    """Phase 5, field 28 and the labelled SOURCE CONFLICT block.

    Phase 5 renders a team's conflicts one of two ways: derived conflicts
    become a labelled block and field 28 points at it, otherwise field 28
    carries the authored note. Both are read here, and a team with a block
    contributes one record per labelled paragraph — the block's own
    structure, not a summary of it.
    """
    from coach_lib import (coaching_conflicts, load_carousel, load_notes,
                           load_stability, load_teams)
    derived = coaching_conflicts(load_teams(), load_stability(), load_carousel())
    for c in derived:
        detail = _clean(c.get("detail"))
        if not detail:
            continue
        yield c["team"], {
            "phase": 5,
            "title": f"Coaching Database — {c['field']}.",
            "detail": detail,
            "where": "the labelled SOURCE CONFLICT block of this team's "
                     "coaching record",
            "link": f"../03_Coaching_Database/{_slug(c['team'])}.md",
        }
    for team, rec in load_notes().items():
        detail = _clean(rec.get("conflicts"))
        if not detail or detail == "See the labelled block below.":
            continue
        yield team, {
            "phase": 5,
            "title": "Coaching Database — source conflict / ambiguity.",
            "detail": detail,
            "where": "field 28 of this team's coaching record",
            "link": f"../03_Coaching_Database/{_slug(team)}.md",
        }


# Phase 7 wrote two conflict tables into its audit page. Their headings are
# reproduced here as the kind, so a team file names the conflict the same way
# the audit does rather than inventing a category for it.
_WT_AUDIT = "../06_Win_Totals/00_SOURCE_CONFLICTS.md"


def _wintotal_records():
    """Phase 7 — field 26, plus the two tables of the win-total audit.

    The two tables are recomputed from the same loaders build_wintotals.py
    uses, not scraped from the rendered page, so the team files and the
    audit page cannot drift apart.
    """
    from wintotal_lib import (load_conference_rows, load_feature, load_notes,
                              load_team_picks)
    rows = load_conference_rows()
    picks = load_team_picks()
    _, feat = load_feature()

    for team in sorted(rows):
        pick = (picks.get(team) or {}).get("pick")
        if not pick:
            continue
        if str(pick["number"]) != str(rows[team]["dk_win_total"]):
            yield team, {
                "phase": 7,
                "title": "Win Totals — the team page and the conference table "
                         "print different numbers.",
                "detail": f"The conference table prints "
                          f"**{rows[team]['dk_win_total']}**; the team page "
                          f"prints **{pick['side'].title()} {pick['number']}**. "
                          f"Both are reproduced as printed and neither is "
                          f"corrected.",
                "where": "one of 21 teams in the win-total source conflict "
                         "audit",
                "link": _WT_AUDIT,
            }

    for team in sorted(feat):
        pick = (picks.get(team) or {}).get("pick")
        if not pick or pick["side"] == feat[team]["side"]:
            continue
        yield team, {
            "phase": 7,
            "title": "Win Totals — the team page and the feature recommend "
                     "opposite sides.",
            "detail": f"The feature (pp. 22–27) bets "
                      f"**{feat[team]['side'].title()} "
                      f"{feat[team]['number']:g}**; the team page bets "
                      f"**{pick['side'].title()} {pick['number']}**. Both are "
                      f"reproduced as printed and neither is corrected.",
            "where": "one of 11 teams in the win-total source conflict audit",
            "link": _WT_AUDIT,
        }

    for team, rec in load_notes().items():
        detail = _clean(rec.get("conflicts"))
        if not detail:
            continue
        # Phase 7's field 26 records two different things: conflicts in the
        # guide, and defects Phase 7 found in a stored TTW artefact. The
        # audit page keeps them under separate headings and so does this.
        artefact = "artefact" in detail.lower()
        yield team, {
            "phase": 7,
            "title": ("Win Totals — a defect found in a TTW artefact, not in "
                      "the guide." if artefact else
                      "Win Totals — source conflict / ambiguity."),
            "detail": detail,
            "where": "field 26 of this team's win-total record",
            "link": f"../06_Win_Totals/{_slug(team)}.md",
        }


def _futures_records():
    """Phase 8 — a conference price with no market.

    Phase 8's audit page names its teams as plain text rather than links,
    so this reads the price table it was generated from instead. The other
    entries on that page are about contributors, rosters and typesetting
    rather than about a team, and a contributor disagreement is not a
    source conflict; none of them is reported here.
    """
    from futures_lib import load_team_prices
    prices = load_team_prices()
    absent = sorted(t for t, v in prices.items()
                    if any(r["no_price_printed"] for r in v["rows"]))
    for team in absent:
        yield team, {
            "phase": 8,
            "title": "Futures — a conference price with no market.",
            "detail": f"{len(absent)} teams — {', '.join(absent)} — carry the "
                      f"conference row's label with **no price at all**. Both "
                      f"are Independents, which have no conference title to "
                      f"win. Recorded as an absence rather than filled in.",
            "where": "the futures source conflict audit",
            "link": "../07_Futures/00_SOURCE_CONFLICTS.md",
        }


COLLECTORS = (_qb_records, _coaching_records, _wintotal_records,
              _futures_records)


def cross_database_conflicts():
    """canonical team name -> [record], ordered by phase then by title.

    Only phases that record something appear. A team absent from the result
    has no conflict recorded anywhere outside the Team Database's own data,
    which is a finding in its own right and is what lets §27 keep saying so.
    """
    out = {}
    for collector in COLLECTORS:
        for team, rec in collector():
            out.setdefault(team, []).append(rec)
    for team in out:
        seen, keep = set(), []
        for rec in sorted(out[team], key=lambda r: (r["phase"], r["title"])):
            key = (rec["phase"], rec["title"], rec["detail"])
            if key in seen:
                continue
            seen.add(key)
            keep.append(rec)
        out[team] = keep
    return out


def render(records, already=()):
    """Markdown bullets for §27, one per record, each cross-linked.

    `already` is the set of conflict texts the Team Database has itself
    rendered above. A record whose wording the team file already carries
    verbatim is not repeated; a record that words the same disagreement
    differently is kept, because the two are different layers' statements
    and the library does not merge them.
    """
    seen = {re.sub(r"[^a-z0-9]+", "", t.lower()) for t in already}
    rows = []
    for rec in records:
        key = re.sub(r"[^a-z0-9]+", "", rec["detail"].lower())
        if key in seen:
            continue
        seen.add(key)
        rows.append(f"- **{rec['title']}** {rec['detail']} "
                    f"*Recorded in Phase {rec['phase']}, {rec['where']} — "
                    f"[source]({rec['link']}).*")
    return rows


def _verify():
    idx = cross_database_conflicts()
    from xref_lib import teams
    canon = {t["team"] for t in teams()}
    stray = sorted(set(idx) - canon)
    if stray:
        raise SystemExit(f"cross_conflicts: non-canonical team keys {stray}")


if __name__ == "__main__":
    _verify()
    idx = cross_database_conflicts()
    from collections import Counter
    per_phase = Counter(r["phase"] for v in idx.values() for r in v)
    teams_phase = Counter(p for v in idx.values() for p in {r["phase"] for r in v})
    print(f"teams with a cross-database conflict: {len(idx)}")
    print(f"records: {sum(len(v) for v in idx.values())}  by phase "
          f"{dict(sorted(per_phase.items()))}")
    print(f"teams by phase {dict(sorted(teams_phase.items()))}")
    for t in ("UNLV Rebels", "Georgia Bulldogs", "Arizona Wildcats"):
        print(f"\n{t}:")
        for line in render(idx.get(t, [])):
            print("  " + line)
