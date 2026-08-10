#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 8 (Futures) renderer
================================================================

Writes 07_Futures/ from the four extracted layers plus authored reference
notes. Every file here is generated; fixes belong in this script or in
_source/futures/*.json, never in the markdown.

The organising principle is attribution. A futures opinion in this guide
belongs to a named person, and the same person can hold what looks like
two different views in two different places -- picking Miami to win the
ACC on p. 4 while betting Notre Dame to make the playoff on p. 9. Those
are different questions. Nothing here merges them, resolves them, or
declares a house position.
"""

import json
import os
import re

from coach_lib import slug
from futures_lib import (NA, bet_key, consensus, load_best_bets, load_heisman,
                         load_notes, load_predictions, load_team_prices)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "07_Futures")

HEAD = ("<!-- GENERATED FILE — do not hand-edit.\n"
        "     Rebuild:  python3 _tools/build_futures.py\n"
        "     Source:   2026 VSiN College Football Betting Guide -->\n")

GUIDE = ("> **Source class: GUIDE CONTENT.** Every price, pick, prediction and "
         "contributor name below is printed in the 2026 VSiN College Football "
         "Betting Guide. TTW reference notes paraphrase each argument; the "
         "judgement is the contributor's. No outside research, no "
         "post-publication updates.")

DERIVED = ("> **Source class: TTW DERIVED.** The counts on this page are this "
           "library's arithmetic over cells the guide prints. A count is not a "
           "probability, not a confidence grade and not a model input, and the "
           "majority of a staff room is not evidence that the majority is "
           "right. Every individual pick remains attributed and unmerged.")


def write(name, body):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(HEAD + "\n" + body.rstrip() + "\n")
    return name


def cslug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") + ".md"


def tlink(team, prefix="../02_Team_Database/"):
    return f"[{team}]({prefix}{slug(team)})"


def f(note, key):
    return (note or {}).get(key) or NA


# ------------------------------------------------------------------ pages

def build_predictions(real, anomalies, roster):
    L = [f"# 2026 Season Predictions — p. 4\n", GUIDE, "",
         f"Every one of the guide's **{len(roster)}** named contributors picks "
         f"a winner in **{len(real)}** categories: **{len(real) * len(roster)} "
         f"attributed picks**. No price and no reasoning is printed here — a "
         f"name in a box is the whole of it. Phase 2 captured these as "
         f"anonymous lists; the attribution below is what Phase 8 adds.", ""]
    for c in real:
        L.append(f"## {c['category']}\n")
        tally = consensus(c["picks"])
        lead = ", ".join(f"**{t}** {n}" for t, n in tally[:4])
        L.append(f"*{len(tally)} different teams named. {lead}"
                 f"{' …' if len(tally) > 4 else ''}*\n")
        L.append("| Contributor | Pick |")
        L.append("| --- | --- |")
        for k in c["picks"]:
            L.append(f"| {k['contributor']} | {k['pick']} |")
        L.append("")
    for c in anomalies:
        L.append(f"## {c['category']} — printed anomaly, reproduced as printed\n")
        L.append(f"> {c['anomaly']}\n")
        L.append("| Contributor | Printed cell |")
        L.append("| --- | --- |")
        for k in c["picks"]:
            L.append(f"| {k['contributor']} | {k['pick']} |")
        L.append("")
    L.append("## Cross-links\n")
    L.append("- [By contributor](00_BY_CONTRIBUTOR.md) · "
             "[consensus counts](00_CONSENSUS.md) · "
             "[source conflicts](00_SOURCE_CONFLICTS.md)")
    return write("00_PREDICTIONS.md", "\n".join(L))


def build_consensus(real, roster):
    L = [f"# Where the Staff Room Agrees — and Where It Splits\n", DERIVED, "",
         "One row per category. *Top pick* is the most-named team, *share* is "
         "how many of the "
         f"{len(roster)} named it, and *spread* is how many different teams "
         "were named at all. A category with a wide spread is one the guide's "
         "own staff cannot agree on.", "",
         "| Category | Top pick | Share | Different teams named | Also named |",
         "| --- | --- | --- | --- | --- |"]
    rows = []
    for c in real:
        t = consensus(c["picks"])
        top, n = t[0]
        others = ", ".join(f"{k} ({v})" for k, v in t[1:5])
        rows.append((len(t), -n, c["category"], top, n, others))
    for spread, negn, cat, top, n, others in sorted(rows, reverse=True):
        L.append(f"| {cat} | **{top}** | {n}/{len(roster)} | {spread} | "
                 f"{others or '—'} |")
    L.append("")
    L.append("## Unanimous and near-unanimous\n")
    for c in real:
        t = consensus(c["picks"])
        if t[0][1] >= len(roster) - 3:
            L.append(f"- **{c['category']}** — {t[0][0]}, {t[0][1]} of "
                     f"{len(roster)}")
    L.append("")
    L.append("## Most divided\n")
    for spread, negn, cat, top, n, others in sorted(rows, reverse=True)[:5]:
        L.append(f"- **{cat}** — {spread} different teams named; the leader "
                 f"{top} carries only {n} of {len(roster)}")
    L.append("\n> These counts are reported, never resolved. The guide does "
             "not print a house pick for any category, and this library does "
             "not manufacture one.")
    L.append("\n## Cross-links\n")
    L.append("- [Full attributed grid](00_PREDICTIONS.md)")
    return write("00_CONSENSUS.md", "\n".join(L))


def build_best_bets(bets, notes):
    L = [f"# VSiN Host College Football Best Bets — pp. 5–15\n", GUIDE, "",
         f"**{len(bets)} priced recommendations by "
         f"{len(set(b['contributor'] for b in bets))} contributors.** Unlike "
         f"p. 4, these are bets with a price and an argument attached. Each "
         f"row links to the contributor's page, where the reasoning is set "
         f"out in reference form.", "",
         "| Contributor | Market | Pick | Price(s) | p. |",
         "| --- | --- | --- | --- | --- |"]
    for b in sorted(bets, key=lambda b: (b["contributor"], b["page"])):
        prices = ", ".join(b["prices"]) or "—"
        L.append(f"| [{b['contributor']}]({cslug(b['contributor'])}) "
                 f"| {b['market']} | {b['headline']} | {prices} | {b['page']} |")
    L.append("")
    L.append("## By market\n")
    by = {}
    for b in bets:
        by.setdefault(b["market"], []).append(b)
    L.append("| Market | Picks | Teams / players |")
    L.append("| --- | --- | --- |")
    for m in sorted(by, key=lambda m: -len(by[m])):
        who = sorted({b["player"] or b["team"] or "—" for b in by[m]})
        L.append(f"| {m} | {len(by[m])} | {', '.join(who)} |")
    L.append("\n## Cross-links\n")
    L.append("- [By contributor](00_BY_CONTRIBUTOR.md) · "
             "[win-total overlap](00_WINTOTAL_OVERLAP.md) · "
             "[Heisman](00_HEISMAN.md)")
    return write("00_BEST_BETS.md", "\n".join(L))


def build_contributor_pages(real, bets, roster, notes):
    """One page per contributor: everything that person says, in one place."""
    bybet = {}
    for b in bets:
        bybet.setdefault(b["contributor"], []).append(b)
    written = []
    everyone = sorted(set(roster) | set(bybet))
    for name in everyone:
        L = [f"# {name} — every futures position in the guide\n", GUIDE, ""]
        mine = [(c["category"], k["pick"]) for c in real
                for k in c["picks"] if k["contributor"] == name]
        if mine:
            L.append(f"## Season predictions (p. 4) — {len(mine)} picks\n")
            L.append("| Category | Pick |")
            L.append("| --- | --- |")
            for cat, pick in mine:
                L.append(f"| {cat} | {pick} |")
            L.append("")
        else:
            L.append("## Season predictions (p. 4)\n")
            L.append(f"{name} is not one of the 22 contributors on p. 4.\n")
        mybets = sorted(bybet.get(name, []), key=lambda b: b["page"])
        if mybets:
            L.append(f"## Best bets (pp. 5–15) — {len(mybets)}\n")
            for b in mybets:
                note = notes.get(bet_key(b))
                L.append(f"### {b['headline']}\n")
                L.append(f"| | |\n| --- | --- |")
                L.append(f"| Market | {b['market']} |")
                L.append(f"| Team | {tlink(b['team']) if b['team'] else NA} |")
                if b["player"]:
                    L.append(f"| Player | {b['player']} |")
                L.append(f"| Price(s) | {', '.join(b['prices']) or NA} |")
                L.append(f"| Legs | {len(b['legs'])} |")
                L.append(f"| Page | p. {b['page']} |")
                L.append("")
                L.append("**The argument — TTW reference notes**\n")
                L.append(f(note, "summary"))
                L.append("")
                if f(note, "depends_on") != NA:
                    L.append(f"*Rests on:* {f(note, 'depends_on')}\n")
                if f(note, "conflicts") != NA:
                    L.append(f"*Conflict or ambiguity:* {f(note, 'conflicts')}\n")
        else:
            L.append("## Best bets (pp. 5–15)\n")
            L.append(f"{name} does not appear in the best-bets feature.\n")
        L.append("## Cross-links\n")
        L.append("- [All best bets](00_BEST_BETS.md) · "
                 "[prediction grid](00_PREDICTIONS.md) · "
                 "[contributor disagreement](00_DISAGREEMENT.md)")
        written.append(write(cslug(name), "\n".join(L)))

    L = ["# Contributors — who says what, and where\n", GUIDE, "",
         f"**{len(everyone)} people** state a futures position somewhere in "
         f"the guide. The two rosters are not the same: **{len(roster)}** fill "
         f"in the p. 4 grid and "
         f"**{len(bybet)}** write best bets. Only those in both columns can be "
         f"compared across the two.", "",
         "| Contributor | p. 4 picks | Best bets | Page |",
         "| --- | --- | --- | --- |"]
    for name in everyone:
        n4 = sum(1 for c in real for k in c["picks"]
                 if k["contributor"] == name)
        nb = len(bybet.get(name, []))
        L.append(f"| [{name}]({cslug(name)}) | {n4 or '—'} | {nb or '—'} | "
                 f"{cslug(name)} |")
    L.append("\n## Cross-links\n")
    L.append("- [Prediction grid](00_PREDICTIONS.md) · "
             "[best bets](00_BEST_BETS.md)")
    written.append(write("00_BY_CONTRIBUTOR.md", "\n".join(L)))
    return written


# p. 4 category labels, keyed by the conference a best-bet headline names.
# "MWC CCHAMPION" is the guide's own typo and is reproduced, not repaired.
CONF_CATEGORY = {
    "ACC": "ACC CHAMPION", "BIG TEN": "BIG TEN CHAMPION",
    "BIG 12": "BIG 12 CHAMPION", "SEC": "SEC CHAMPION",
    "AMERICAN": "AAC CHAMPION", "CONFERENCE USA": "CUSA CHAMPION",
    "MAC": "MAC CHAMPION", "MOUNTAIN WEST": "MWC CCHAMPION",
    "PAC-12": "PAC-12 CHAMPION", "SUN BELT": "SUN BELT CHAMPION",
}
_CONF_KEYS = sorted(CONF_CATEGORY, key=len, reverse=True)

# p. 4 prints short programme names; best bets resolve to canonical ones.
# The two are compared through the Phase 8 identity table, reversed.
def _short_name(team):
    from futures_lib import PRED_TO_TEAM
    for short, full in PRED_TO_TEAM.items():
        if full == team:
            return short
    return team


def _conf_of(headline):
    h = headline.upper()
    for k in _CONF_KEYS:
        if k in h:
            return k
    return None


def build_disagreement(real, bets, roster):
    """Same person, two layers. Recorded, never reconciled."""
    L = ["# Contributor Disagreement — preserved, not resolved\n", GUIDE, "",
         "> **Nothing here is corrected.** Two people disagreeing is the "
         "normal state of a staff room, and one person answering two "
         "different questions differently is not a contradiction at all. "
         "Every position stands as printed.", "",
         "## Where one contributor's p. 4 pick and their own best bet point "
         "at different teams\n",
         "A p. 4 cell answers *who wins this*. A best bet answers *what would "
         "I stake money on, at this price*. They can differ for good reasons — "
         "price being the obvious one — so these are listed as things worth "
         "reading together, not as errors.", ""]
    byname = {}
    for b in bets:
        byname.setdefault(b["contributor"], []).append(b)

    # A comparison is only meaningful inside one market. Adam Burke picking
    # UTSA to win the AAC while betting Appalachian State to win the Sun Belt
    # is not a disagreement -- those are different conferences.
    rows, context = [], []
    for name, mybets in byname.items():
        p4 = {c["category"]: k["pick"] for c in real
              for k in c["picks"] if k["contributor"] == name}
        if not p4:
            continue
        four = {p4.get(f"CFP FINAL FOUR #{i}") for i in range(1, 5)}
        for b in mybets:
            if not b["team"]:
                continue
            short = _short_name(b["team"])
            if b["market"] in ("Conference championship",
                               "Conference title game"):
                conf = _conf_of(b["headline"])
                cat = CONF_CATEGORY.get(conf)
                if cat and p4.get(cat) and p4[cat] != short:
                    rows.append((name, cat, p4[cat], b["headline"], b["page"],
                                 "picks one team to win the conference, bets "
                                 "another"))
            elif b["market"] == "College Football Playoff":
                if four and short not in four:
                    context.append((name, " / ".join(sorted(x for x in four if x)),
                                    b["headline"], b["page"]))
            elif b["market"] == "National championship":
                if p4.get("CFP CHAMPION") and p4["CFP CHAMPION"] != short:
                    rows.append((name, "CFP CHAMPION", p4["CFP CHAMPION"],
                                 b["headline"], b["page"],
                                 "picks one national champion, bets another"))
    if rows:
        n = len(set(rows))
        L.append(f"**{n} instance{'s' if n != 1 else ''}.**\n")
        L.append("| Contributor | p. 4 category | Their p. 4 pick | Their best bet | p. | What differs |")
        L.append("| --- | --- | --- | --- | --- | --- |")
        for r in sorted(set(rows)):
            L.append(f"| [{r[0]}]({cslug(r[0])}) | {r[1]} | {r[2]} | "
                     f"{r[3]} | {r[4]} | {r[5]} |")
    else:
        L.append("*No contributor's best bet points at a different team from "
                 "their own p. 4 pick in the same market.*")
    L.append("")
    L.append("## Not a disagreement: the playoff field is larger than four\n")
    L.append("The p. 4 grid asks for a **final four**. A best bet on a team "
             "*to make the College Football Playoff* is a bet on the "
             "**12-team field**. A contributor can consistently project four "
             "teams and stake money on a fifth, and the cases below are "
             "listed for context rather than as contradictions — reading a "
             "wider field into a four-slot grid would manufacture a conflict "
             "the guide does not contain.\n")
    if context:
        L.append("| Contributor | Their p. 4 final four | Their playoff bet | p. |")
        L.append("| --- | --- | --- | --- |")
        for r in sorted(set(context)):
            L.append(f"| [{r[0]}]({cslug(r[0])}) | {r[1]} | {r[2]} | {r[3]} |")
    L.append("")
    L.append("## Where the staff room splits hardest\n")
    for c in real:
        t = consensus(c["picks"])
        if len(t) >= 6:
            named = ", ".join(f"{k} ({v})" for k, v in t)
            L.append(f"- **{c['category']}** — {len(t)} different teams: {named}")
    L.append("\n## Cross-links\n")
    L.append("- [Consensus counts](00_CONSENSUS.md) · "
             "[source conflicts](00_SOURCE_CONFLICTS.md)")
    return write("00_DISAGREEMENT.md", "\n".join(L))


def build_heisman(heis, notes):
    L = [f"# {heis['title']} — p. {heis['page']}\n", GUIDE, "",
         f"*{heis['author']}, p. {heis['page']}.* **{len(heis['picks'])} "
         f"priced picks**, plus one competition he says he is monitoring "
         f"rather than betting.", "",
         "| Player | Team as printed | Price |",
         "| --- | --- | --- |"]
    for p in heis["picks"]:
        L.append(f"| **{p['player']}** | {p['headline']} | "
                 f"{', '.join(p['prices']) or NA} |")
    L.append("")
    L.append("## How he frames the market\n")
    L.append(f(notes.get("heisman|_framing"), "summary"))
    L.append("")
    for p in heis["picks"]:
        note = notes.get(f"heisman|{p['player']}")
        L.append(f"## {p['player']} — {p['headline']}\n")
        L.append("**The argument — TTW reference notes**\n")
        L.append(f(note, "summary"))
        L.append("")
        if f(note, "depends_on") != NA:
            L.append(f"*Rests on:* {f(note, 'depends_on')}\n")
        if f(note, "conflicts") != NA:
            L.append(f"*Conflict or ambiguity:* {f(note, 'conflicts')}\n")
    L.append("## Watched but not bet\n")
    L.append(f(notes.get("heisman|_monitoring"), "summary"))
    L.append("")
    L.append("## Heisman picks in the best-bets feature\n")
    L.append("The Heisman is also bet on pp. 5–15 by four other contributors; "
             "those picks live on their own pages and are listed in "
             "[00_BEST_BETS.md](00_BEST_BETS.md) under *Heisman*.")
    L.append("\n## Cross-links\n")
    L.append("- [Best bets](00_BEST_BETS.md) · "
             "[Quarterback Database](../04_Quarterback_Database/README.md)")
    return write("00_HEISMAN.md", "\n".join(L))


def build_team_prices(prices, bets):
    bet_team = {}
    for b in bets:
        if b["team"]:
            bet_team.setdefault(b["team"], []).append(b["headline"])
    L = ["# Team Futures Prices — all 138 right-hand pages\n", GUIDE, "",
         "Each team's right-hand page prints three futures markets. Prices are "
         "read by coordinate — price left, label right, three fixed rows — "
         "which is how Phase 1's deferred *futures price labelling* question "
         "is answered. Independents have a conference row with a **label and "
         "no price**; that absence is recorded, never filled in.", "",
         "| Team | CFP Championship | Make the playoff | Conference | p. | Bet by a host? |",
         "| --- | --- | --- | --- | --- | --- |"]
    for team in sorted(prices):
        v = prices[team]
        cells = []
        for r in v["rows"]:
            cells.append(r["price"] if r["price"]
                         else f"*{r['market']} — no price printed*")
        conf_label = v["rows"][2]["market"]
        cells[2] = (f"{cells[2]} ({conf_label})" if v["rows"][2]["price"]
                    else cells[2])
        mark = "yes" if team in bet_team else ""
        L.append(f"| {tlink(team)} | {cells[0]} | {cells[1]} | {cells[2]} "
                 f"| {v['page']} | {mark} |")
    L.append("\n## Cross-links\n")
    L.append("- [Best bets](00_BEST_BETS.md) · "
             "[Power Ratings](../05_Power_Ratings/00_MAKINEN_RATINGS.md)")
    return write("00_TEAM_FUTURES.md", "\n".join(L))


def build_wintotal_overlap(bets):
    """Best bets that are win totals already live in Phase 7. Link, do not
    duplicate -- and record where the two features disagree."""
    from wintotal_lib import load_feature
    _, feat = load_feature()
    wt = [b for b in bets
          if b["market"] in ("Season win total", "Conference wins")
          and b["team"]]
    L = ["# Best Bets That Are Win Totals — overlap with `06_Win_Totals`\n",
         GUIDE, "",
         f"**{len(wt)} of the best bets are season or conference win totals.** "
         f"Phase 7 already holds the win-total layer, so this page links "
         f"rather than duplicating — and records where a host on pp. 5–15 "
         f"takes a different side from Steve Makinen on pp. 22–27.", "",
         "| Contributor | Best bet | Makinen, pp. 22–27 | Same side? |",
         "| --- | --- | --- | --- |"]
    clash = 0
    for b in sorted(wt, key=lambda b: b["team"]):
        e = feat.get(b["team"])
        if e:
            mk = f"[{e['side'].title()} {e['number']:g}]" \
                 f"(../06_Win_Totals/{slug(b['team'])})"
            side = "OVER" if re.search(r"\bOVER\b", b["headline"]) else \
                   "UNDER" if re.search(r"\bUNDER\b", b["headline"]) else None
            if side and side != e["side"]:
                same, clash = "**no — opposite sides**", clash + 1
            elif side:
                same = "yes"
            else:
                same = "—"
        else:
            mk, same = "*not in the feature*", "—"
        L.append(f"| [{b['contributor']}]({cslug(b['contributor'])}) "
                 f"| {b['headline']} | {mk} | {same} |")
    L.append("")
    L.append(f"**{clash} direct contradiction"
             f"{'s' if clash != 1 else ''}** between a host's best bet and "
             f"Makinen's win-total feature. Both are reproduced; neither is "
             f"corrected, and no consensus side is derived from them.")
    L.append("\n## Cross-links\n")
    L.append("- [Win Totals](../06_Win_Totals/README.md) · "
             "[best bets](00_BEST_BETS.md)")
    return write("00_WINTOTAL_OVERLAP.md", "\n".join(L))


def build_conflicts(real, anomalies, bets, prices, roster):
    L = ["# Source Conflict Audit — futures\n", GUIDE, "",
         "> **Nothing here is corrected.** Every figure, label and name is "
         "reproduced as the guide prints it.", ""]
    L.append("## The SUN BELT CHAMP row\n")
    for c in anomalies:
        L.append(f"{c['anomaly']} The row is reproduced in full in "
                 f"[00_PREDICTIONS.md](00_PREDICTIONS.md).\n")
        L.append("| Contributor | Printed cell |")
        L.append("| --- | --- |")
        for k in c["picks"]:
            L.append(f"| {k['contributor']} | {k['pick']} |")
        L.append("")
    L.append("Note that the guide separately prints a **SUN BELT CHAMPION** "
             "row containing college teams. Both rows are kept.\n")

    L.append("## Contributor names printed inconsistently\n")
    L.append("| Where | As printed | Elsewhere |")
    L.append("| --- | --- | --- |")
    L.append("| p. 39 Heisman byline | Zach Cohen | Zachary Cohen (p. 4 grid, "
             "p. 8 best bets) |")
    L.append("| p. 7 best bets | Pauly Howard | Paul Howard (p. 4 grid) |")
    L.append("\nBoth pairs are almost certainly the same person, but the "
             "library records what each page prints and does not merge two "
             "printed names into one identity.\n")

    L.append("## A price printed without its closing bracket\n")
    L.append("Dave Ross's second leg on p. 5 is printed as "
             "`ALT OVER 7.5 WINS (+120` — the bracket does not close in the "
             "guide. Reproduced as printed.\n")

    L.append("## A conference price with no market\n")
    absent = [t for t, v in prices.items()
              if any(r["no_price_printed"] for r in v["rows"])]
    L.append(f"{len(absent)} teams — {', '.join(sorted(absent))} — carry the "
             f"conference row's label with **no price at all**. Both are "
             f"Independents, which have no conference title to win. Recorded "
             f"as an absence rather than filled in.\n")

    L.append("## A conference price typeset with a Unicode minus\n")
    L.append("Texas Tech's Big 12 price is typeset with U+2212 MINUS SIGN "
             "rather than an ASCII hyphen. The printed number is the same; "
             "the extractor normalises it so the price is not silently "
             "dropped.\n")

    L.append("## Two rosters, not one\n")
    byname = {b["contributor"] for b in bets}
    only4 = sorted(set(roster) - byname)
    onlyb = sorted(byname - set(roster))
    L.append(f"- On p. 4 only ({len(only4)}): {', '.join(only4) or '—'}")
    L.append(f"- In best bets only ({len(onlyb)}): {', '.join(onlyb) or '—'}")
    L.append("\nThe two features were assembled from different groups. Neither "
             "roster is treated as the canonical staff list.\n")
    L.append("## Cross-links\n")
    L.append("- [Contributor disagreement](00_DISAGREEMENT.md) · "
             "[Phase 7 conflicts](../06_Win_Totals/00_SOURCE_CONFLICTS.md)")
    return write("00_SOURCE_CONFLICTS.md", "\n".join(L))


def build_readme(real, bets, heis, prices, roster, notes):
    L = ["# 07 Futures\n", GUIDE, "",
         "Every futures market, price and recommendation the guide prints, "
         "with each position attributed to the person who holds it.", "",
         "## The four layers\n",
         "| Layer | Source | Coverage | What it gives you |",
         "| --- | --- | --- | --- |",
         f"| Season predictions | p. 4 | {len(real)} categories × "
         f"{len(roster)} contributors = **{len(real) * len(roster)}** picks | "
         f"a name in a box — no price, no reasoning |",
         f"| Best bets | pp. 5–15 | **{len(bets)}** picks by "
         f"{len(set(b['contributor'] for b in bets))} contributors | "
         f"priced recommendations with an argument |",
         f"| Heisman | p. 39 | **{len(heis['picks'])}** picks by "
         f"{heis['author']} | priced player futures |",
         f"| Team prices | 138 right-hand pages | **{len(prices) * 3}** "
         f"markets, {sum(1 for v in prices.values() for r in v['rows'] if r['price'])} "
         f"printed prices | the board for every team |",
         "",
         "## Files\n",
         "| File | Content |",
         "| --- | --- |",
         "| [00_PREDICTIONS.md](00_PREDICTIONS.md) | the attributed p. 4 grid |",
         "| [00_CONSENSUS.md](00_CONSENSUS.md) | **TTW DERIVED** counts — agreement and splits |",
         "| [00_BEST_BETS.md](00_BEST_BETS.md) | all priced host picks |",
         "| [00_BY_CONTRIBUTOR.md](00_BY_CONTRIBUTOR.md) | one page per person |",
         "| [00_HEISMAN.md](00_HEISMAN.md) | p. 39 |",
         "| [00_TEAM_FUTURES.md](00_TEAM_FUTURES.md) | all 138 boards |",
         "| [00_WINTOTAL_OVERLAP.md](00_WINTOTAL_OVERLAP.md) | overlap with Phase 7 |",
         "| [00_DISAGREEMENT.md](00_DISAGREEMENT.md) | disagreement, preserved |",
         "| [00_SOURCE_CONFLICTS.md](00_SOURCE_CONFLICTS.md) | conflicts and anomalies |",
         "",
         "## What this database does not do\n",
         "It does not convert a price into an implied probability, remove vig, "
         "rank contributors by past accuracy, or derive a house position from "
         "a staff vote. The consensus counts are arithmetic over printed "
         "cells and are labelled TTW DERIVED wherever they appear. Where the "
         "guide contradicts itself — or where one person answers two "
         "questions differently — both answers are printed and neither is "
         "resolved.\n",
         "## Rebuild\n",
         "```bash",
         "python3 _tools/extract_futures.py",
         "python3 _tools/build_futures.py",
         "python3 _tools/validate_futures.py",
         "```"]
    return write("README.md", "\n".join(L))


def main():
    preds, real, anomalies = load_predictions()
    bets = load_best_bets()["bets"]
    roster = load_predictions()[0]["roster"]
    heis = load_heisman()
    prices = load_team_prices()
    notes = load_notes()

    files = [build_readme(real, bets, heis, prices, roster, notes),
             build_predictions(real, anomalies, roster),
             build_consensus(real, roster),
             build_best_bets(bets, notes),
             build_heisman(heis, notes),
             build_team_prices(prices, bets),
             build_wintotal_overlap(bets),
             build_disagreement(real, bets, roster),
             build_conflicts(real, anomalies, bets, prices, roster)]
    files += build_contributor_pages(real, bets, roster, notes)

    keys = {bet_key(b) for b in bets} | {f"heisman|{p['player']}"
                                         for p in heis["picks"]}
    print(f"futures files written to 07_Futures/  ({len(files)})")
    print(f"  prediction cells  {len(real) * len(roster)} "
          f"({len(real)} categories x {len(roster)} contributors)")
    print(f"  best bets         {len(bets)} by "
          f"{len(set(b['contributor'] for b in bets))} contributors")
    print(f"  heisman picks     {len(heis['picks'])}")
    print(f"  team markets      {len(prices) * 3}")
    print(f"  notes authored    {len(keys & set(notes))}/{len(keys)}")


if __name__ == "__main__":
    main()
