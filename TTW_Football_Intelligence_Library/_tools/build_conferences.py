#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 2 Conference Database Builder
=======================================================================

Writes one intelligence file per conference into 01_Conference_Database/,
plus an index.

Design rule that governs this whole file: **thematic sections quote the guide
rather than summarise it.** Each theme is populated by selecting sentences from
the conference preview essay that address that theme, reproduced verbatim with
a page reference. Where the preview says nothing on a theme, the section reads
"Not addressed in guide." rather than being filled with inference.

That keeps every line traceable to a page, and makes silence visible instead of
papering over it.

Usage:
    python3 _tools/build_conferences.py     # run from the library root
"""

import json
import os
import re
from collections import Counter, defaultdict

SRC = "_source/data"
OUT = "01_Conference_Database"

BANNER = (
    "<!-- GENERATED FILE — do not hand-edit.\n"
    "     Rebuild:  python3 _tools/build_conferences.py\n"
    "     Source:   2026 VSiN College Football Betting Guide (345 pp.) -->\n\n"
)

NOT_ADDRESSED = "> *Not addressed in guide.*"

# Sentences from the preview essay are routed to themes by keyword. A sentence
# may serve several themes; that is intended, since the same line often carries
# both a portal point and a quarterback point.
THEMES = {
    "quarterback": r"\bquarterback|\bQB\b|\bpasser|signal-caller|\bpassing\b",
    "returning_production": r"\breturn|\bback\b|\bstarters?\b|experience|production|veteran",
    "portal": r"\bportal\b|\btransfer|\bNIL\b|\btransferred\b",
    "schedule": r"\bschedule|\broad\b|\bhome\b|\btravel|\bopener|\bcrossover|\bplays? at\b",
    "coaching": r"\bcoach|\bhire|\bstaff\b|coordinator|\bsideline\b",
    "win_totals": r"win total|\bwins\b|\bover\b|\bunder\b|\bprops?\b",
    "futures": r"\bodds\b|favorite|\bfutures\b|championship|\btitle\b|\bchampion|\+\d{3}|\bpriced\b",
    "playoff": r"\bplayoff|\bCFP\b|Group of (?:Five|Six)|at-large|\bbid\b|\bseeding\b",
    "betting": r"\bbet\b|\bbetting|\bvalue\b|\bprice|\bmarket|\bmoney\b|\bATS\b|\bbettors?\b",
    "historical": r"last season|last year|\bin 20\d\d\b|\bsince\b|historically|\bstreak\b|"
                  r"\bpast (?:season|five|decade)|back-to-back|\bever\b",
}

THEME_TITLES = [
    ("quarterback", "Quarterback themes"),
    ("returning_production", "Returning-production themes"),
    ("portal", "Transfer-portal themes"),
    ("schedule", "Schedule themes"),
    ("historical", "Historical and situational notes"),
]


def load(name):
    with open(os.path.join(SRC, f"{name}.json")) as fh:
        return json.load(fh)


PAGES = "_source/extracted/pages"


def prose_sentences(page):
    """Readable sentences from a team page, with table noise filtered out."""
    raw = open(os.path.join(PAGES, f"p{page:03d}.txt")).read()
    raw = re.sub(r"-\n", "", raw)
    raw = re.sub(r"\s+", " ", raw)
    # Strip the fixed furniture on every team spread so it cannot be mistaken
    # for prose: the running header, the left-page table labels, and the
    # right-page statistics labels.
    raw = re.sub(r"\d{1,3} 2026 VSiN COLLEGE FOOTBALL BETTING GUIDE", " ", raw)
    raw = re.sub(r"Date Opponent/Projected Line.*?total offense defense", " ", raw)
    raw = re.sub(r"Date Opponent/Projected Line.*?Opponent Power Rating", " ", raw)
    raw = re.sub(r"Three Burning Questions for the 2026 Season", " ", raw)
    raw = re.sub(r"(?:OFFENSIVE|DEFENSIVE) STATISTICS.*?(?=[A-Z][a-z])", " ", raw)
    raw = re.sub(r"\s+", " ", raw)
    out = []
    for s in sentences(raw):
        # The win-total pick sits beside the prose column and can lead a
        # sentence; it is a separate field, not part of the sentence.
        s = re.sub(r"^(?:Over|Under)\s+\d+\.5\s+", "", s)
        words = [w for w in s.split() if re.search(r"[a-z]", w)]
        # Real prose, not a schedule row or a statistics column.
        if len(words) >= 8 and len(words) / max(len(s.split()), 1) > 0.7:
            out.append(s)
    return out


def team_page_evidence(standings, pattern, limit=8):
    """Sentences from this conference's team pages that address a theme."""
    hits, teams_hit = [], []
    for row in sorted(standings, key=lambda r: r["team"]):
        found = []
        for page in (row["page"], row["page"] + 1):
            for s in prose_sentences(page):
                if re.search(pattern, s, re.I):
                    found.append((s, page))
        if found:
            teams_hit.append(row["team"])
            hits.append((row["team"], found))
    return hits, teams_hit


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z“\"])", text)
    return [p.strip() for p in parts if len(p.strip()) > 25]


def quote(lines, page):
    if not lines:
        return NOT_ADDRESSED
    return "\n\n".join(f"> {ln}\n>\n> — *conference preview, p. {page}*" for ln in lines)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def tier_teams(standings):
    """Tiering strictly from Makinen's projected conference wins."""
    if not standings or all(float(r["proj_wins_conf"]) == 0 for r in standings):
        return None
    rows = sorted(standings, key=lambda r: -float(r["proj_wins_conf"]))
    top = float(rows[0]["proj_wins_conf"])
    bottom = float(rows[-1]["proj_wins_conf"])
    span = top - bottom
    if span == 0:
        return None
    tiers = defaultdict(list)
    for row in rows:
        position = (float(row["proj_wins_conf"]) - bottom) / span
        if position >= 0.75:
            tiers["Contenders"].append(row)
        elif position >= 0.5:
            tiers["Upper middle"].append(row)
        elif position >= 0.25:
            tiers["Lower middle"].append(row)
        else:
            tiers["Bottom"].append(row)
    return tiers


def find_tenure_conflicts(prose, page, standings):
    """Preview essays sometimes state a coach's season number that disagrees
    with the same coach's team page. Both are guide content, so both are kept."""
    conflicts = []
    ordinals = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
                "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
                "11th": 11, "12th": 12, "13th": 13}
    by_coach = {r["head_coach"]: r for r in standings}
    for coach, row in by_coach.items():
        surname = coach.split()[-1]
        for match in re.finditer(
            rf"{re.escape(surname)}[^.]*?\b(first|second|third|fourth|fifth|sixth|"
            rf"seventh|eighth|ninth|tenth|11th|12th|13th)\s+(?:season|year)", prose, re.I
        ):
            stated = ordinals[match.group(1).lower()]
            if stated != row["hc_season"]:
                conflicts.append({
                    "coach": coach,
                    "team": row["team"],
                    "preview_says": stated,
                    "team_page_says": row["hc_season"],
                    "team_page": row["page"],
                    "quote": match.group(0).strip(),
                })
    return conflicts


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def build_conference(conf, data):
    name = conf["conference"]
    page = conf["preview_page"]
    standings = conf["standings"]
    prose = conf["prose"]
    sents = sentences(prose)

    themed = {}
    for key, pattern in THEMES.items():
        themed[key] = [s for s in sents if re.search(pattern, s, re.I)]

    lines = [f"# {name} — Conference Intelligence\n"]
    lines.append(
        f"| | |\n| --- | --- |\n"
        f"| **Conference preview** | p. {page} |\n"
        f"| **Section author** | {conf['author']} |\n"
        f"| **Teams** | {len(standings)} |\n"
        f"| **Team pages** | {min(r['page'] for r in standings)}–"
        f"{max(r['page'] for r in standings) + 1} |\n"
    )
    lines.append(
        "\n> **Source class: GUIDE CONTENT.** Everything below is drawn from the "
        "2026 VSiN College Football Betting Guide. Thematic sections quote the "
        "preview essay verbatim rather than paraphrasing it. A section reading "
        "*Not addressed in guide* means the preview is silent on that theme — "
        "not that the answer is unknown elsewhere in the guide.\n"
    )

    # --- overview ---------------------------------------------------------
    lines.append(f"\n## Conference overview\n\n*Preview by {conf['author']}, p. {page}. "
                 "Reproduced in full.*\n")
    for s in sents:
        lines.append(f"\n> {s}")

    # --- teams ------------------------------------------------------------
    lines.append("\n\n## Team list\n")
    lines.append("\n| Team | Pages | Head Coach | Yr | SM PR | Conf Rank | National |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(standings, key=lambda r: int(r["conf_rank"].split()[0][1:])):
        lines.append(
            f"| {row['team']} | {row['page']}–{row['page']+1} | {row['head_coach']} | "
            f"{row['hc_season']} | {row['sm_power_rating']} | {row['conf_rank']} | "
            f"{row['natl_rank']} |"
        )

    # --- projected standings ---------------------------------------------
    lines.append(f"\n## Makinen projected standings (p. {page})\n")
    lines.append(
        "\nAs printed in the preview. *DK Wins* is the DraftKings season win "
        "total; *Hm/Rd Fld* are home and road field-advantage values; *SS* is "
        "schedule strength with its national rank.\n"
    )
    lines.append("\n| Team | DK Wins | SM PR | Hm Fld | Rd Fld | SS (rank) | "
                 "Proj W-L (all) | Proj W-L (conf) |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in standings:
        lines.append(
            f"| {row['team']} | {row['dk_win_total']} | {row['sm_power_rating']} | "
            f"{row['home_field']} | {row['road_field']} | "
            f"{row['schedule_strength']} ({row['schedule_rank']}) | "
            f"{row['proj_wins_all']}–{row['proj_losses_all']} | "
            f"{row['proj_wins_conf']}–{row['proj_losses_conf']} |"
        )

    if conf["duplicate_rows"]:
        lines.append("\n### ⚠️ Source anomaly in this table\n")
        for dup in conf["duplicate_rows"]:
            lines.append(f"\n**{dup['table_name']}** is printed in this table but "
                         f"belongs to the **{dup['belongs_to']}**.\n\n> {dup['note']}\n")

    # --- hierarchy --------------------------------------------------------
    lines.append("\n## Projected hierarchy\n")
    tiers = tier_teams(standings)
    if tiers is None:
        lines.append(
            "\n> *Not applicable.* The guide projects no conference games for "
            "these teams, so no conference hierarchy is stated.\n"
        )
    else:
        lines.append(
            "\nTiers are derived strictly from Makinen's **projected conference "
            "wins** in the table above. The guide does not print tier labels; the "
            "grouping is arithmetic, and the underlying numbers are shown so the "
            "split can be checked.\n"
        )
        for label in ("Contenders", "Upper middle", "Lower middle", "Bottom"):
            if tiers.get(label):
                teams = ", ".join(
                    f"{r['team']} ({r['proj_wins_conf']})" for r in tiers[label])
                lines.append(f"\n- **{label}** — {teams}")
        lines.append("\n\n*Classification: PERSONAL INFERENCE (arithmetic grouping "
                     "of guide figures). The figures themselves are GUIDE CONTENT.*\n")

    # --- power rating context --------------------------------------------
    ratings = [float(r["sm_power_rating"]) for r in standings]
    national = [int(r["natl_rank"].split()[0][1:]) for r in standings]
    lines.append("\n## Conference power-rating context\n")
    lines.append(
        f"\n| | |\n| --- | --- |\n"
        f"| Highest rating | {max(ratings)} ({max(standings, key=lambda r: float(r['sm_power_rating']))['team']}) |\n"
        f"| Lowest rating | {min(ratings)} ({min(standings, key=lambda r: float(r['sm_power_rating']))['team']}) |\n"
        f"| Average | {round(sum(ratings)/len(ratings), 2)} |\n"
        f"| Spread | {round(max(ratings)-min(ratings), 1)} points |\n"
        f"| Best national rank | #{min(national)} |\n"
        f"| Worst national rank | #{max(national)} |\n"
        f"| Teams in national top 25 | {sum(1 for n in national if n <= 25)} |\n"
        f"| Teams in national bottom 25 | {sum(1 for n in national if n > 113)} |\n"
    )
    lines.append("\nFull national context: "
                 "[09 — Power Rating Index](../00_Master_Index/09_Power_Rating_Index.md)\n")

    # --- coaching ---------------------------------------------------------
    lines.append("\n## Coaching changes\n")
    new_here = [c for c in data["new_coaches"] if c["conference"] == name]
    if new_here:
        lines.append(f"\n**{len(new_here)}** coaches in this conference are profiled in "
                     "The Coaching Carousel (pp. 28–37).\n")
        lines.append("\n| Coach | Team | Year | Profile |")
        lines.append("| --- | --- | --- | --- |")
        for c in sorted(new_here, key=lambda c: c["coach"]):
            lines.append(f"| {c['coach']} | {c['team']} | {c['hc_season']} | p. {c['page']} |")
    else:
        lines.append("\n> *No coach in this conference is profiled in The Coaching "
                     "Carousel (pp. 28–37).*\n")
    lines.append(f"\n**What the preview says about coaching:**\n\n{quote(themed['coaching'], page)}\n")

    # --- themed sections --------------------------------------------------
    # The preview essays are short narratives and are frequently silent on a
    # given theme. Where that happens the conference-level answer lives on the
    # team pages instead, so both levels are reported separately and neither is
    # allowed to stand in for the other.
    for key, title in THEME_TITLES:
        lines.append(f"\n## {title}\n")
        lines.append(f"\n**From the conference preview (p. {page}):**\n\n"
                     f"{quote(themed[key], page)}\n")
        hits, teams_hit = team_page_evidence(standings, THEMES[key])
        if hits:
            lines.append(
                f"\n**From the team pages in this conference** — "
                f"{len(teams_hit)} of {len(standings)} teams' pages address this "
                f"theme. A sample follows; Phase 3 carries the full treatment "
                f"team by team.\n"
            )
            shown = 0
            for team, found in hits:
                if shown >= 8:
                    break
                s, pg = found[0]
                lines.append(f"\n- **{team}** (p. {pg}) — {s}")
                shown += 1
            if len(hits) > shown:
                lines.append(f"\n\n*{len(hits) - shown} further teams also address "
                             f"this theme; see their team pages.*\n")
        else:
            lines.append(f"\n**From the team pages in this conference:** "
                         f"*no team page in this conference addresses this theme.*\n")

    # --- win totals -------------------------------------------------------
    lines.append("\n## Win-total discussion\n")
    picks = [w for w in data["win_totals"] if w["conference"] == name]
    if picks:
        lines.append("\nSteve Makinen's win-total bets involving this conference "
                     "(pp. 22–27):\n")
        lines.append("\n| Team | Pick | Number |")
        lines.append("| --- | --- | --- |")
        for p in sorted(picks, key=lambda p: (p["side"], p["team"])):
            lines.append(f"| {p['team']} | **{p['side']}** | {p['number']} |")
    else:
        lines.append("\n> *No team in this conference appears among Makinen's "
                     "win-total bets (pp. 22–27).*\n")
    lines.append(f"\n**What the preview says about win totals:**\n\n"
                 f"{quote(themed['win_totals'], page)}\n")

    # --- futures ----------------------------------------------------------
    lines.append("\n## Futures and championship discussion\n")
    label = next((lbl for lbl, cname in data["prediction_labels"].items()
                  if cname == name), None)
    if label and label in data["predictions"]:
        picks = data["predictions"][label]
        tally = Counter(picks)
        lines.append(f"\n### Staff champion picks (p. 4)\n\n**{len(picks)}** VSiN staff "
                     f"members picked a champion. Printed under the label "
                     f"`{label}`.\n")
        lines.append("\n| Pick | Votes | Share |")
        lines.append("| --- | --- | --- |")
        for team, count in tally.most_common():
            lines.append(f"| {team} | {count} | {round(100*count/len(picks))}% |")
        if len(tally) == 1:
            lines.append("\n**Unanimous.**\n")
        else:
            lines.append(f"\nSpread across **{len(tally)}** different teams — the "
                         "degree of disagreement is itself the signal.\n")
    else:
        lines.append("\n> *No conference champion is predicted for this group on "
                     "p. 4.*\n")
    lines.append(f"\n**What the preview says about futures:**\n\n"
                 f"{quote(themed['futures'], page)}\n")

    # --- playoff ----------------------------------------------------------
    lines.append(f"\n## Playoff discussion\n\n{quote(themed['playoff'], page)}\n")
    cfp_mentions = []
    for cfp_label in data["cfp_labels"]:
        for team_name in set(data["predictions"].get(cfp_label, [])):
            if any(team_name.lower() in r["team"].lower() or
                   r["team"].lower().startswith(team_name.lower())
                   for r in standings):
                cfp_mentions.append((cfp_label, team_name,
                                     data["predictions"][cfp_label].count(team_name)))
    if cfp_mentions:
        lines.append("\n### Teams from this conference in the staff CFP picks (p. 4)\n")
        lines.append("\n| Category | Team | Votes |")
        lines.append("| --- | --- | --- |")
        for cfp_label, team_name, votes in sorted(cfp_mentions):
            lines.append(f"| {cfp_label} | {team_name} | {votes} |")

    # --- betting ----------------------------------------------------------
    lines.append(f"\n## Betting observations\n\n{quote(themed['betting'], page)}\n")
    bets = [b for b in data["best_bets"] if b["conference"] == name]
    if bets:
        lines.append("\n### Host best bets involving this conference (pp. 5–15)\n")
        lines.append("\n| Contributor | Pick | Page |")
        lines.append("| --- | --- | --- |")
        for b in sorted(bets, key=lambda b: b["page"]):
            lines.append(f"| {b['contributor']} | {b['pick']} | {b['page']} |")
        lines.append(
            "\n> Best-bet headlines are matched to teams by name. Picks phrased "
            "without a team (Heisman player props, generic playoff prices) are not "
            "listed here. Phase 8 builds the authoritative futures database.\n"
        )

    # --- disagreements ----------------------------------------------------
    lines.append("\n## Competing viewpoints and internal disagreements\n")
    conflicts = find_tenure_conflicts(prose, page, standings)
    any_conflict = False
    if conflicts:
        any_conflict = True
        lines.append("\n### Coach tenure stated differently in different places\n")
        for c in conflicts:
            lines.append(
                f"\n- **{c['coach']} ({c['team']})** — the preview (p. {page}) "
                f"describes his **{ordinal(c['preview_says'])}** season; his team "
                f"page (p. {c['team_page']}) states his **{ordinal(c['team_page_says'])}**. "
                f"Preview wording: *\"…{c['quote']}…\"* Both are reproduced as "
                f"printed; neither is corrected."
            )
    if label and label in data["predictions"]:
        tally = Counter(data["predictions"][label])
        if len(tally) > 1:
            any_conflict = True
            leaders = tally.most_common()
            lines.append(
                f"\n### Staff do not agree on a champion\n\n"
                f"{len(tally)} teams received votes. "
                f"{leaders[0][0]} leads with {leaders[0][1]} of {sum(tally.values())}, "
                f"but {sum(c for _, c in leaders[1:])} votes went elsewhere "
                f"({', '.join(f'{t} {c}' for t, c in leaders[1:])}). "
                f"Recorded in full rather than reduced to a consensus.\n"
            )
    dk_gaps = [(r, float(r["proj_wins_all"]) - float(r["dk_win_total"])) for r in standings]
    notable = [x for x in dk_gaps if abs(x[1]) >= 1.0]
    if notable:
        any_conflict = True
        lines.append(
            "\n### Makinen's projection vs the DraftKings number\n\n"
            "Teams where Makinen's projected wins differ from the posted win "
            "total by a full game or more. This is the guide disagreeing with "
            "the market, and it is where the preview's own betting value sits.\n"
        )
        lines.append("\n| Team | DK Wins | Makinen projected | Difference |")
        lines.append("| --- | --- | --- | --- |")
        for row, diff in sorted(notable, key=lambda x: -abs(x[1])):
            lines.append(f"| {row['team']} | {row['dk_win_total']} | "
                         f"{row['proj_wins_all']} | {diff:+.1f} |")
    if not any_conflict:
        lines.append("\n> *No internal disagreement detected for this conference.*\n")

    # --- references -------------------------------------------------------
    lines.append("\n## Page references\n")
    lines.append(f"\n| Pages | Content |\n| --- | --- |")
    lines.append(f"| {page} | Conference preview and Makinen projected standings |")
    lines.append(f"| {min(r['page'] for r in standings)}–"
                 f"{max(r['page'] for r in standings)+1} | Team spreads |")
    lines.append("| 4 | Staff season predictions |")
    if new_here:
        pgs = sorted({c["page"] for c in new_here})
        lines.append(f"| {', '.join(str(p) for p in pgs)} | New head coach profiles |")
    if picks:
        lines.append("| 22–27 | Makinen win-total bets |")
    if bets:
        lines.append("| 5–15 | Host best bets |")
    lines.append("| 46–47 | Makinen power rating methodology |")

    # --- cross-links ------------------------------------------------------
    lines.append("\n## Cross-links\n")
    lines.append("\n**Master Index:** "
                 "[Conference Index](../00_Master_Index/02_Conference_Index.md) · "
                 "[Team Index](../00_Master_Index/03_Team_Index.md) · "
                 "[Coaching Index](../00_Master_Index/04_Coaching_Index.md) · "
                 "[Power Ratings](../00_Master_Index/09_Power_Rating_Index.md)\n")
    lines.append("\n**Team files** (Phase 3, `02_Team_Database/`) — not yet built:\n")
    for row in sorted(standings, key=lambda r: r["team"]):
        lines.append(f"\n- `{slug(row['team'])}.md` — {row['team']} "
                     f"(guide pp. {row['page']}–{row['page']+1})")

    path = os.path.join(OUT, f"{slug(name)}.md")
    with open(path, "w") as fh:
        fh.write(BANNER + "\n".join(lines) + "\n")
    return path, conflicts


def main():
    previews = load("conference_previews")
    data = {
        "predictions": load("phase2_predictions"),
        "anomalies": load("phase2_prediction_anomalies"),
        "win_totals": load("phase2_win_totals"),
        "best_bets": load("phase2_best_bets"),
        "new_coaches": load("phase2_new_coaches"),
        "prediction_labels": {
            "ACC CHAMPION": "ACC", "BIG TEN CHAMPION": "Big Ten",
            "BIG 12 CHAMPION": "Big 12", "SEC CHAMPION": "SEC",
            "AAC CHAMPION": "American", "CUSA CHAMPION": "Conference USA",
            "MAC CHAMPION": "MAC", "MWC CCHAMPION": "Mountain West",
            "PAC-12 CHAMPION": "Pac-12", "SUN BELT CHAMPION": "Sun Belt",
        },
        "cfp_labels": ["CFP FINAL FOUR #1", "CFP FINAL FOUR #2", "CFP FINAL FOUR #3",
                       "CFP FINAL FOUR #4", "CFP TITLE GAME #1", "CFP TITLE GAME #2",
                       "CFP CHAMPION"],
    }

    os.makedirs(OUT, exist_ok=True)
    written, all_conflicts = [], []
    for conf in previews:
        path, conflicts = build_conference(conf, data)
        written.append(path)
        all_conflicts.extend(conflicts)

    build_index(previews, data, all_conflicts)
    for path in written:
        print(f"  {os.path.basename(path):<24} {os.path.getsize(path):>7,} bytes")
    print(f"\n{len(written)} conference files + index written to {OUT}/")
    print(f"tenure conflicts detected: {len(all_conflicts)}")


def build_index(previews, data, conflicts):
    lines = [
        "# 01 — Conference Database\n",
        "**Phase 2 deliverable.** One intelligence file per conference, built "
        "from the eleven preview pages and every cross-cutting section that "
        "touches a conference.\n",
        "\n| Conference | File | Preview | Author | Teams |",
        "| --- | --- | --- | --- | --- |",
    ]
    for conf in previews:
        name = conf["conference"]
        lines.append(
            f"| **{name}** | [{slug(name)}.md]({slug(name)}.md) | "
            f"p. {conf['preview_page']} | {conf['author']} | "
            f"{len(conf['standings'])} |"
        )

    lines.append("\n## What each file contains\n")
    lines.append(
        "\nConference overview (preview essay in full) · section author · team "
        "list · Makinen projected standings · projected hierarchy · power-rating "
        "context · coaching changes · quarterback, returning-production, "
        "transfer-portal, schedule and historical themes · win-total discussion · "
        "futures and championship discussion · playoff discussion · betting "
        "observations · competing viewpoints · page references · cross-links to "
        "the Phase 3 team files.\n"
    )

    lines.append("\n## Section authorship\n")
    by_author = defaultdict(list)
    for conf in previews:
        by_author[conf["author"]].append(conf["conference"])
    lines.append("\n| Author | Conferences |\n| --- | --- |")
    for author, confs in sorted(by_author.items(), key=lambda x: -len(x[1])):
        lines.append(f"| {author} | {', '.join(sorted(confs))} |")
    lines.append(
        "\n> The p. 115 Big 12 preview is signed **Zach Cohen**; the p. 3 welcome "
        "letter credits the Big 12 previews to **Zachary Cohen**. Recorded as "
        "printed in both places.\n"
    )

    lines.append("\n## Champion prediction consensus (p. 4)\n")
    lines.append("\n| Conference | Leading pick | Votes | Teams receiving votes |")
    lines.append("| --- | --- | --- | --- |")
    for label, name in data["prediction_labels"].items():
        picks = data["predictions"].get(label, [])
        if not picks:
            continue
        tally = Counter(picks)
        top, count = tally.most_common(1)[0]
        lines.append(f"| {name} | {top} | {count} of {len(picks)} | {len(tally)} |")

    lines.append("\n## Source anomalies found in Phase 2\n")
    lines.append(
        "\n1. **Charlotte printed in two conferences.** Charlotte appears in both "
        "the American (p. 49) and Conference USA (p. 187) projected standings "
        "tables with identical figures. Its own team page (p. 52) and every "
        "Conference USA team page ('#N of 10') place it in the American. Treated "
        "as a duplicate printing in the Conference USA table.\n"
    )
    for anomaly in data["anomalies"]:
        lines.append(
            f"\n2. **Mislabelled prediction row on p. 4.** A row printed under "
            f"`{anomaly['printed_label']}` holds 22 picks that are almost all NFL "
            f"teams (Falcons, Panthers, Buccaneers, Saints — the NFC South), with "
            f"a single college entry (James Madison) among them. The label does "
            f"not describe the contents. Verified against the page geometry at "
            f"several row tolerances, all of which return the same 22 entries, so "
            f"this is how the guide is printed rather than an extraction artifact. "
            f"The row is excluded from conference prediction data and recorded "
            f"here as printed.\n"
        )
    lines.append(
        "\n3. **`MWC CCHAMPION`** — the Mountain West row on p. 4 is printed with "
        "a doubled C. Reproduced as printed.\n"
    )
    if conflicts:
        lines.append(
            f"\n4. **Coach tenure stated inconsistently** in {len(conflicts)} "
            "case(s), where a preview essay and a team page give different season "
            "numbers for the same coach. Both figures are kept:\n"
        )
        for c in conflicts:
            lines.append(
                f"\n   - **{c['coach']} ({c['team']})** — preview says season "
                f"{c['preview_says']}, team page (p. {c['team_page']}) says "
                f"{c['team_page_says']}."
            )

    with open(os.path.join(OUT, "00_CONFERENCE_INDEX.md"), "w") as fh:
        fh.write(BANNER + "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
