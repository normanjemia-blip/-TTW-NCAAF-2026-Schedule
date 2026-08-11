#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 3 Team Database Builder
=================================================================

Writes one standardised intelligence file per FBS team into 02_Team_Database/.

Every file carries the same 29 headings in the same order. A heading whose
topic the guide does not address reads exactly "Not addressed in guide." and is
never dropped, so all 138 files stay structurally identical and searchable.

Content is drawn from the whole guide, not only a team's own spread: the
cross-guide mention index supplies references from conference previews, best
bets, win totals, the coaching carousel, staff predictions and every other
team's pages.

Usage:
    python3 _tools/build_teams.py        # run from the library root
    python3 _tools/build_teams.py SEC    # one conference at a time
"""

import json
import os
import re
import sys
from collections import Counter

SRC = "_source/data"
OUT = "02_Team_Database"

NOT_ADDRESSED = "Not addressed in guide."
DEFERRED = "**DEFERRED — EXTRACTION NOT RELIABLE**"

BANNER = (
    "<!-- GENERATED FILE — do not hand-edit.\n"
    "     Rebuild:  python3 _tools/build_teams.py\n"
    "     Source:   2026 VSiN College Football Betting Guide (345 pp.) -->\n\n"
)

SCHEMA = [
    "Program Snapshot", "Conference", "VSiN Team Rank / Conference Rank",
    "Steve Makinen Power Rating", "Home-Field Advantage Reference",
    "Head Coach", "Coordinator Notes", "Coaching Continuity / Changes",
    "Quarterback Situation", "Returning Production", "Transfer Portal",
    "Recruiting / Roster Notes", "Offensive Identity", "Defensive Identity",
    "Key Strengths", "Key Weaknesses", "Schedule Overview",
    "Difficult Stretches / Trap Spots", "Win Total Discussion",
    "Futures / Conference / Playoff Discussion", "Betting Notes / Best Bets",
    "Historical / Situational Trends", "Important Statistics", "Bull Case",
    "Bear Case", "Open Questions / Risks", "Source Conflicts",
    "Relevant Page References", "Cross-Links",
]

THEMES = {
    "quarterback": r"\bquarterback|\bQB\b|\bpasser|signal-caller|\bpassing\b|\bthrew\b|\bcompletion",
    "portal": r"\bportal\b|\btransfer|\bNIL\b|\btransferred\b",
    "recruiting": r"\brecruit|\bsignee|\bclass of 20|\bfreshman\b|\bfour-star|\bthree-star|\bfive-star",
    "offense": r"\boffens|\brushing\b|\brun game|\breceiv|\boffensive line|\bscoring\b|\btempo\b|\byards per play",
    "defense": r"\bdefens|\bsecondary\b|\bpass rush|\bsacks?\b|\btacklers?\b|\blinebacker|\bsafety\b",
    "schedule": r"\bschedule|\bopener|\broad\b|\bhome\b|\btravel|\bplays? at\b|\bnonconference|\bbye\b",
    "trap": r"\brest (?:advantage|disadvantage)|\btrap\b|\blook-?ahead|\bletdown\b|\bshort week|"
            r"\bgauntlet|\bbrutal\b|\bstretch\b|\bback-to-back\b",
    "historical": r"last season|last year|\bin 20\d\d\b|\bsince\b|historically|\bstreak\b|"
                  r"\bever\b|\bpast (?:season|two|three|five|decade)",
    "coaching": r"\bcoach|\bhire|\bstaff\b|coordinator|\bOC\b|\bDC\b",
    "betting": r"\bbet\b|\bbetting|\bvalue\b|\bprice|\bmarket|\bATS\b|\bcover|\bfavorite|\bunderdog",
}

POSITIVE = (r"\bimprove|\bupside\b|\bbest\b|\belite\b|\bstrength|\btalented|\breturns?\b|"
            r"\bexperienced|\bdeep\b|\bstrong\b|\bwinning\b|\boptimis|\bbreakout|\bcontend|"
            r"\bgood\b|\bsolid\b|\bimpress|\bexcellent|\bpromising|\bfavorable|\bstellar|"
            r"\bcredit|\bsuccess|\bwinnable|\bhigh floor|\bloaded\b")
NEGATIVE = (r"\bconcern|\bworry|\bstruggl|\bloss(?:es)?\b|\blost\b|\bquestion|\bweak|\bthin\b|"
            r"\binexperienc|\bregress|\bbrutal|\btough\b|\bdifficult|\binjur|\bmiss(?:ing|ed)?\b")


def load(name):
    with open(os.path.join(SRC, f"{name}.json")) as fh:
        return json.load(fh)


def load_paraphrases():
    """TTW-authored reference notes, one file per batch, merged on load.

    A team present here is rendered from notes written in TTW's own words. A
    team absent from here still renders from guide prose, so a part-finished
    Phase 3A leaves a coherent database rather than a broken one.
    """
    store = {}
    folder = "_source/paraphrase"
    if not os.path.isdir(folder):
        return store
    for name in sorted(os.listdir(folder)):
        if name.endswith(".json"):
            with open(os.path.join(folder, name)) as fh:
                store.update(json.load(fh))
    return store


def slug(name):
    # "&" becomes "and", matching coach_lib.slug. The two diverged, and
    # "Texas A&M Aggies" was the one team where it showed: this file
    # produced texas_a_m_aggies while Phases 4, 5, 7 and 8 linked to
    # texas_aandm_aggies, leaving 18 broken cross-links into the Team
    # Database. One canonical slug now serves the whole library.
    s = name.lower().replace("\u2019", "").replace("'", "").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z“\"])", text)
    return [p.strip() for p in parts if len(p.strip()) > 30]


def bullets(items, empty=NOT_ADDRESSED):
    if not items:
        return empty
    return "\n".join(items)


def cite(sentence, page):
    return f"- {sentence} *(p. {page})*"


class TeamFileBuilder:
    def __init__(self, data):
        self.d = data

    def sources_for(self, team):
        """Own-page prose plus every off-page sentence naming this team."""
        name = team["team"]
        detail = self.d["details"][name]
        mentions = self.d["mentions"][name]

        own = [(s, detail["pages"][0]) for s in sentences(detail["text"])]
        for q in detail["questions"]:
            own += [(s, detail["pages"][1]) for s in sentences(q["answer"])]
        off = [(m["sentence"], m["page"]) for m in mentions["off_page"]]
        return own, off

    def notes_for(self, team):
        return self.d["paraphrases"].get(team["team"])

    def themed_notes(self, team, key):
        """Theme lines drawn from TTW's paraphrase notes rather than guide prose."""
        notes = self.notes_for(team)
        if not notes:
            return None
        rows = []
        for item in notes.get("outlook", []):
            if key in item.get("t", []):
                rows.append(f"- {item['n']} *(p. {item['p']})*")
        for item in notes.get("questions", []):
            if key in item.get("t", []):
                rows.append(f"- **{item['q']}** {item['n']} *(p. {item['p']})*")
        return rows

    def themed(self, own, off, key, own_limit=12, off_limit=6):
        """Theme evidence, kept split by where in the guide it came from.

        Own-page lines are about this team by construction. Off-page lines are
        matched by name, and a school name that is also a place name ("Georgia",
        "Miami", "Washington") can catch a sentence that is not about the team
        at all. Labelling the two groups lets a reader weigh them differently
        instead of silently mixing them.
        """
        pattern = THEMES[key]
        rows, seen = [], set()
        picked_own = 0
        for sentence, page in own:
            if re.search(pattern, sentence, re.I) and sentence not in seen:
                seen.add(sentence)
                rows.append(cite(sentence, page))
                picked_own += 1
            if picked_own >= own_limit:
                break
        elsewhere = []
        for sentence, page in off:
            if re.search(pattern, sentence, re.I) and sentence not in seen:
                seen.add(sentence)
                elsewhere.append(cite(sentence, page))
            if len(elsewhere) >= off_limit:
                break
        if elsewhere:
            rows.append("\n**Elsewhere in the guide** — matched by team name, so "
                        "check the page before relying on a line where the school "
                        "name is also a place name:\n")
            rows.extend(elsewhere)
        return rows

    # -- individual sections ------------------------------------------------

    def build(self, team):
        name = team["team"]
        d = self.d
        detail = d["details"][name]
        ref = d["standings"][name]
        own, off = self.sources_for(team)
        left, right = detail["pages"]
        S = {}

        S["Program Snapshot"] = self.snapshot(team, detail, ref, left, right)
        S["Conference"] = self.conference(team, ref)
        S["VSiN Team Rank / Conference Rank"] = self.ranks(team, detail, right)
        S["Steve Makinen Power Rating"] = self.rating(team, detail, right)
        S["Home-Field Advantage Reference"] = self.hfa(detail, left)
        S["Head Coach"] = self.coach(team, detail, left)
        S["Coordinator Notes"] = self.coordinators(team)
        S["Coaching Continuity / Changes"] = self.continuity(team, own, off)
        S["Quarterback Situation"] = self.quarterback(team, detail, own, off)
        S["Returning Production"] = self.returning(detail, left)
        S["Transfer Portal"] = self.theme_section(team, own, off, "portal")
        S["Recruiting / Roster Notes"] = self.theme_section(team, own, off, "recruiting")
        S["Offensive Identity"] = self.theme_section(team, own, off, "offense")
        S["Defensive Identity"] = self.theme_section(team, own, off, "defense")
        S["Key Strengths"] = self.extremes(detail, right, best=True)
        S["Key Weaknesses"] = self.extremes(detail, right, best=False)
        S["Schedule Overview"] = self.schedule(detail, ref, left)
        S["Difficult Stretches / Trap Spots"] = self.theme_section(team, own, off, "trap")
        S["Win Total Discussion"] = self.win_total(team, detail, ref, left)
        S["Futures / Conference / Playoff Discussion"] = self.futures(team, detail, right)
        S["Betting Notes / Best Bets"] = self.best_bets(team, own, off)
        S["Historical / Situational Trends"] = self.theme_section(team, own, off, "historical")
        S["Important Statistics"] = self.statistics(detail, right)
        S["Bull Case"] = self.case(team, detail, ref, own, off, bull=True)
        S["Bear Case"] = self.case(team, detail, ref, own, off, bull=False)
        S["Open Questions / Risks"] = self.questions(team, detail, right)
        S["Source Conflicts"] = self.conflicts(team, detail)
        S["Relevant Page References"] = self.pages(team, detail, ref)
        S["Cross-Links"] = self.links(team)

        lines = [f"# {name}\n"]
        lines.append(
            f"> **Source: 2026 VSiN College Football Betting Guide, "
            f"pp. {left}–{right}** and every other page that names this team. "
            f"GUIDE CONTENT throughout unless a line says otherwise. "
            f"No outside research. Nothing inferred to fill a heading.\n"
        )
        for i, heading in enumerate(SCHEMA, 1):
            lines.append(f"\n## {i}. {heading}\n")
            lines.append(S[heading])
        return "\n".join(lines) + "\n"

    def elsewhere_pages(self, team, off, key):
        """Pages outside this team's spread that discuss it on a given theme.

        Once a file is paraphrased it no longer reproduces those sentences, so
        the pages are cited instead. That keeps the provenance a reader needs
        to go and check the guide, without carrying its prose.
        """
        pattern = THEMES[key]
        pages = sorted({page for sentence, page in off
                        if re.search(pattern, sentence, re.I)})
        return pages

    def theme_section(self, team, own, off, key):
        notes = self.themed_notes(team, key)
        if notes is None:
            return bullets(self.themed(own, off, key))
        parts = list(notes)
        pages = self.elsewhere_pages(team, off, key)
        if not parts:
            # No note carries this theme, so the pointer must also cover the
            # team's own spread — otherwise a topic the guide does address
            # would silently read as "Not addressed in guide."
            pages = sorted(set(pages) | set(self.elsewhere_pages(team, own, key)))
        if pages:
            parts.append(
                f"\nReferenced in the guide on "
                f"**pp. {', '.join(str(p) for p in pages)}** — those passages are "
                f"not reproduced here; see the pages for VSiN's own wording.")
        if not parts:
            return NOT_ADDRESSED
        return "\n".join(parts)

    def snapshot(self, team, detail, ref, left, right):
        rows = [
            ("Conference", team["conference"]),
            ("Guide pages", f"{left}–{right}"),
            ("Head coach", f"{team['head_coach']} "
                           f"({ordinal(team['hc_season'])} season"
                           f"{', interim' if team['interim'] else ''})"),
            ("2025 straight up", team["su_2025"]),
            ("2025 against the spread", team["ats_2025"]),
            ("2025 over/under", team["ou_2025"]),
            ("Makinen power rating", detail["power_rating"]),
            ("National rank", detail["natl_rank"]),
            ("Conference rank", detail["conf_rank"]),
            ("DraftKings win total", ref["dk_win_total"]),
            ("Makinen projected wins", f"{ref['proj_wins_all']}–{ref['proj_losses_all']} "
                                       f"overall, {ref['proj_wins_conf']}–"
                                       f"{ref['proj_losses_conf']} in conference"),
            ("Schedule strength", f"{ref['schedule_strength']} "
                                  f"(#{ref['schedule_rank']} toughest of 138)"),
        ]
        table = "| | |\n| --- | --- |\n" + "\n".join(
            f"| **{k}** | {v} |" for k, v in rows)
        notes = self.notes_for(team)
        if notes and notes.get("outlook"):
            table += (f"\n\n### Season outlook — VSiN's analysis in reference form "
                      f"(p. {left})\n\n")
            table += "\n".join(f"- {i['n']} *(p. {i['p']})*"
                                for i in notes["outlook"])
            table += ("\n\n*TTW reference notes summarising VSiN's analysis. "
                      "GUIDE CONTENT — facts, conclusions and reasoning are the "
                      "guide's; the wording is TTW's.*\n")
        else:
            outlook = detail["text"].strip()
            if outlook:
                table += (f"\n\n### Season outlook as written in the guide (p. {left})\n\n"
                          f"{outlook}\n")
        return table

    def conference(self, team, ref):
        return (
            f"**{team['conference']}** — see the conference file for league-wide "
            f"context: [{slug(team['conference'])}.md]"
            f"(../01_Conference_Database/{slug(team['conference'])}.md)\n\n"
            f"Makinen projects **{ref['proj_wins_conf']}–{ref['proj_losses_conf']}** "
            f"in conference play, ranking this team {ref['conf_rank']} in the "
            f"{team['conference']} by power rating."
        )

    def ranks(self, team, detail, right):
        top50 = next((t for t in self.d["top50"]
                      if self.d["resolve"].get(t["team"].upper()) == team["team"]), None)
        text = (f"- **National rank:** {detail['natl_rank']} *(p. {right})*\n"
                f"- **Conference rank:** {detail['conf_rank']} *(p. {right})*")
        if top50:
            text += (f"\n- **Matt Youmans' Preseason Top 50:** "
                     f"**#{top50['rank']}** *(pp. 16–20)*")
        else:
            text += "\n- **Matt Youmans' Preseason Top 50:** not ranked *(pp. 16–20)*"
        return text

    def rating(self, team, detail, right):
        return (
            f"**{detail['power_rating']}** — as printed on p. {right}, "
            f"reproduced exactly and not converted to any other scale.\n\n"
            f"Ranks {detail['natl_rank']} nationally and {detail['conf_rank']} in "
            f"the {team['conference']}. Methodology is set out on pp. 46–47.\n\n"
            f"> No comparison against the TTW workbook is made here. That is a "
            f"later-phase deliverable."
        )

    def hfa(self, detail, left):
        fr = detail["field_ratings"]
        if not fr:
            return DEFERRED
        return (
            f"- **Home field rating:** {fr['home']} *(p. {left})*\n"
            f"- **Road field rating:** {fr['road']} *(p. {left})*\n\n"
            f"Printed on the team page as `field ratings (HOME/ROAD)` and verified "
            f"against the same values in the conference projected standings table. "
            f"The guide's general treatment of home-field advantage is on p. 21."
        )

    def coach(self, team, detail, left):
        new = [c for c in self.d["new_coaches"] if c["team"] == team["team"]]
        text = (f"**{team['head_coach']}** — {ordinal(team['hc_season'])} season "
                f"at the programme{', listed as interim' if team['interim'] else ''} "
                f"*(p. {left})*.")
        if new:
            text += (f"\n\nProfiled among the guide's new head coaches in "
                     f"The Coaching Carousel *(p. {new[0]['page']})*.")
        return text

    def continuity(self, team, own, off):
        row = self.d["stability"].get(team["team"])
        parts = []
        if row:
            yes = lambda v: "returns" if v and v != "0" else "new for 2026"
            parts.append(
                f"**Steve Makinen's Stability Score: {row['stability_score']}** "
                f"*(p. {row['page']})*\n\n"
                f"| Component | Status | Points |\n| --- | --- | --- |\n"
                f"| Head coach | {yes(row['hc_returns'])} | {row['hc_returns']} |\n"
                f"| Offensive coordinator | {yes(row['oc_returns'])} | {row['oc_returns']} |\n"
                f"| Defensive coordinator | {yes(row['dc_returns'])} | {row['dc_returns']} |\n"
                f"| Starting quarterback | {yes(row['qb_returns'])} | {row['qb_returns']} |\n"
                f"| Returning starters | {row['returning_starters_count']} | "
                f"{row['returning_starters_points']} |\n\n"
                f"Scoring is the guide's own: head coach 4, offensive coordinator 3, "
                f"defensive coordinator 3, starting quarterback 4, plus points for "
                f"returning starters. A returning transfer quarterback counts as a "
                f"**new** quarterback in this system *(p. 41)*.\n")
        notes = self.themed_notes(team, "coaching")
        if notes is not None:
            themed = list(notes)
            pages = self.elsewhere_pages(team, off, "coaching")
            if pages:
                themed.append(
                    f"\nAlso referenced on **pp. {', '.join(str(p) for p in pages)}** "
                    f"— not reproduced here.")
        else:
            themed = self.themed(own, off, "coaching")
        if themed:
            parts.append(bullets(themed))
        elif not row:
            parts.append(NOT_ADDRESSED)
        return "\n".join(parts)

    def coordinators(self, team):
        rows = [c for c in self.d["coordinators"] if team["team"] in c["teams"]]
        if not rows:
            return NOT_ADDRESSED
        return "\n".join(
            f"- **{c['role']} {c['name']}** *(p. {', '.join(str(p) for p in c['pages'])})*"
            for c in sorted(rows, key=lambda c: c["role"]))

    def quarterback(self, team, detail, own, off):
        parts = []
        top15 = [q for q in self.d["qb_top15"]
                 if self.d["resolve"].get(q["team"].upper()) == team["team"]]
        if top15:
            parts.append(
                f"**Paul Stone ranks {top15[0]['qb']} the #{top15[0]['rank']} "
                f"quarterback in the country** *(p. 45)*.\n")
        row = self.d["stability"].get(team["team"])
        if row:
            same = row["qb_returns"] and row["qb_returns"] != "0"
            parts.append(
                f"**Starting quarterback continuity:** the Stability Score table "
                f"treats this team as having "
                f"{'the same starting quarterback as 2025' if same else 'a new starting quarterback for 2026'} "
                f"*(p. {row['page']})*. A transfer expected to start counts as new "
                f"in that system.\n")
        rs = detail["returning_starters"]
        if rs:
            flag = any(v.get("returning_qb") for v in rs.values())
            parts.append(
                f"**Returning starting quarterback:** "
                f"{'yes' if flag else 'no'} — the guide marks returning "
                f"quarterbacks with an asterisk on the returning-starters line "
                f"*(p. {detail['pages'][0]})*.\n")
        notes = self.themed_notes(team, "quarterback")
        if notes is not None:
            pages = self.elsewhere_pages(team, off, "quarterback")
            if pages:
                notes = list(notes) + [
                    f"\nAlso referenced on **pp. {', '.join(str(p) for p in pages)}** "
                    f"— not reproduced here."]
            parts.append(bullets(notes))
        else:
            parts.append(bullets(self.themed(own, off, "quarterback")))
        return "\n".join(parts)

    def returning(self, detail, left):
        rs = detail["returning_starters"]
        if not rs:
            return DEFERRED
        text = (
            f"| | Returning starters |\n| --- | --- |\n"
            f"| **Total** | {rs['total']['value']} |\n"
            f"| **Offence** | {rs['offense']['value']}"
            f"{' *(includes the returning quarterback)*' if rs['offense']['returning_qb'] else ''} |\n"
            f"| **Defence** | {rs['defense']['value']}"
            f"{' *(includes the returning quarterback)*' if rs['defense']['returning_qb'] else ''} |\n\n"
            f"Read by position from p. {left}. The three figures sit under the "
            f"printed labels `total / offense / defense`; they are matched to "
            f"those labels by their place on the page, because the PDF text "
            f"layer emits them in a different order than they are printed."
        )
        row = self.d["stability"].get(detail["team"])
        if row:
            text += (f"\n\nThe Stability Score table prints the same figure "
                     f"independently: **{row['returning_starters_count']} returning "
                     f"starters** *(p. {row['page']})*.")
        if detail.get("returning_starters_conflict"):
            text += f"\n\n> **SOURCE CONFLICT.** {detail['returning_starters_conflict']}"
        for c in self.d["stability_conflicts"]:
            if c["team"] == detail["team"]:
                text += f"\n\n> **SOURCE CONFLICT.** {c['detail']}"
        return text

    def extremes(self, detail, right, best=True):
        stats = detail["statistics"]
        if not stats or stats.get("guide_note"):
            return NOT_ADDRESSED
        rows = []
        for side in ("offense", "defense"):
            for row in stats[side]:
                if not row["rank"] or not row["rank"].isdigit():
                    continue
                rank = int(row["rank"])
                if (best and rank <= 25) or (not best and rank >= 114):
                    rows.append((rank, side, row))
        if not rows:
            return ("No category ranks inside the national top 25." if best
                    else "No category ranks inside the national bottom 25.")
        rows.sort(key=lambda r: r[0] if best else -r[0])
        head = ("National top-25 finishes in the guide's printed categories"
                if best else "National bottom-25 finishes in the guide's printed categories")
        out = [f"{head} *(p. {right})*:\n",
               "| Side | Category | Value | National rank |",
               "| --- | --- | --- | --- |"]
        for rank, side, row in rows:
            out.append(f"| {side.title()} | {row['category']} | {row['value']} | #{rank} |")
        return "\n".join(out)

    def schedule(self, detail, ref, left):
        games = detail["schedule"]
        if not games:
            return DEFERRED
        out = [
            f"Schedule strength **{ref['schedule_strength']}**, "
            f"**#{ref['schedule_rank']} toughest of 138** *(p. {left})*.\n",
            "| Date | Opponent | Site | Projected line | Opponent power rating |",
            "| --- | --- | --- | --- | --- |",
        ]
        for g in games:
            site = {"home": "Home", "away": "Away", "neutral": "Neutral"}[g["location"]]
            out.append(
                f"| {g['date']} | {g['opponent']} | {site} | "
                f"{g['projected_line'] or '—'} | {g['opponent_power_rating'] or '—'} |")
        out.append("\nProjected lines and opponent power ratings are Makinen's, "
                   "printed alongside the schedule on the team page.")
        return "\n".join(out)

    def win_total(self, team, detail, ref, left):
        parts = [
            f"- **DraftKings win total:** {ref['dk_win_total']} *(p. "
            f"{self.d['preview_page'][team['conference']]})*",
            f"- **Makinen projected wins:** {ref['proj_wins_all']} "
            f"*(p. {self.d['preview_page'][team['conference']]})*",
        ]
        diff = float(ref["proj_wins_all"]) - float(ref["dk_win_total"])
        parts.append(f"- **Difference:** {diff:+.1f} wins against the posted number")
        if detail["win_total_pick"]:
            parts.append(f"- **Recommendation on the team page:** "
                         f"**{detail['win_total_pick']['side']} "
                         f"{detail['win_total_pick']['number']}** *(p. {left})*")
        if detail["projected_wins"]:
            parts.append(f"- **Projection stated in the team-page essay:** "
                         f"{detail['projected_wins']} wins *(p. {left})*")
        featured = [w for w in self.d["win_totals"] if w["team"] == team["team"]]
        if featured:
            for w in featured:
                parts.append(
                    f"\n**Selected as one of Steve Makinen's win-total bets** "
                    f"*(pp. 22–27)*: **{w['side']} {w['number']}**.")
        return "\n".join(parts)

    def futures(self, team, detail, right):
        parts = []
        if detail["futures"]:
            parts.append("Prices printed on the team page *(p. "
                         f"{right})*:\n")
            parts.append("| Market | Price |\n| --- | --- |")
            for f in detail["futures"]:
                parts.append(f"| {f['market']} | {f['price']} |")
        else:
            parts.append(DEFERRED)
        picks = self.d["prediction_hits"].get(team["team"], [])
        if picks:
            parts.append("\n**VSiN staff predictions naming this team** *(p. 4)*:\n")
            parts.append("| Category | Votes |\n| --- | --- |")
            for label, votes in picks:
                parts.append(f"| {label} | {votes} of 22 |")
        return "\n".join(parts)

    def best_bets(self, team, own, off):
        rows = [b for b in self.d["best_bets"] if b["team"] == team["team"]]
        parts = []
        if rows:
            parts.append("**Host best bets naming this team** *(pp. 5–15)*:\n")
            parts.append("| Contributor | Pick | Page |\n| --- | --- | --- |")
            for b in rows:
                parts.append(f"| {b['contributor']} | {b['pick']} | {b['page']} |")
            parts.append("\nWhere contributors disagree, every position is kept "
                         "separately and none is reconciled.\n")
        notes = self.themed_notes(team, "betting")
        if notes is not None:
            pages = self.elsewhere_pages(team, off, "betting")
            themed = list(notes)
            if pages:
                themed.append(
                    f"\nAlso referenced on **pp. {', '.join(str(p) for p in pages)}** "
                    f"— not reproduced here.")
        else:
            themed = self.themed(own, off, "betting")
        parts.append(bullets(themed) if themed else
                     (NOT_ADDRESSED if not rows else ""))
        return "\n".join(p for p in parts if p)

    def statistics(self, detail, right):
        stats = detail["statistics"]
        if not stats:
            return DEFERRED
        if stats.get("guide_note"):
            return (f"The guide prints no 2025 statistics for this team, stating "
                    f"instead: **\"{stats['guide_note']}\"** *(p. {right})*.\n\n"
                    f"This is the guide's own note, not a gap in extraction.")
        out = [f"As printed on p. {right}. Each category carries a value and a "
               f"national rank.\n", "### Offence\n",
               "| Category | Value | National rank |", "| --- | --- | --- |"]
        for row in stats["offense"]:
            out.append(f"| {row['category']} | {row['value']} | {row['rank']} |")
        out += ["\n### Defence\n", "| Category | Value | National rank |",
                "| --- | --- | --- |"]
        for row in stats["defense"]:
            out.append(f"| {row['category']} | {row['value']} | {row['rank']} |")
        return "\n".join(out)

    def case(self, team, detail, ref, own, off, bull=True):
        pattern = POSITIVE if bull else NEGATIVE
        rows, seen = [], set()
        notes = self.notes_for(team)
        if notes:
            pool = [(i["n"], i["p"]) for i in notes.get("outlook", [])]
            pool += [(i["n"], i["p"]) for i in notes.get("questions", [])]
        else:
            pool = own + off
        for sentence, page in pool:
            if re.search(pattern, sentence, re.I) and sentence not in seen:
                seen.add(sentence)
                rows.append(cite(sentence, page))
            if len(rows) >= 10:
                break
        header = []
        diff = float(ref["proj_wins_all"]) - float(ref["dk_win_total"])
        if bull and diff > 0:
            header.append(f"- Makinen projects **{ref['proj_wins_all']} wins** against a "
                          f"posted total of {ref['dk_win_total']} — **{diff:+.1f}** in "
                          f"this team's favour.")
        if not bull and diff < 0:
            header.append(f"- Makinen projects **{ref['proj_wins_all']} wins** against a "
                          f"posted total of {ref['dk_win_total']} — **{diff:+.1f}** "
                          f"against this team.")
        if detail["win_total_pick"]:
            side = detail["win_total_pick"]["side"]
            if (bull and side == "OVER") or (not bull and side == "UNDER"):
                header.append(f"- The team page recommends **{side} "
                              f"{detail['win_total_pick']['number']}**.")
        body = header + rows
        if not body:
            # The guide argues both sides for every team, so an empty case means
            # the lexicon missed it rather than that the argument is absent.
            # Point at the pages instead of dropping the section.
            pages = sorted({p for _, p in pool})
            if pages:
                side = "optimistic" if bull else "pessimistic"
                return (f"No note in this file is phrased as an explicitly "
                        f"{side} claim. VSiN's reasoning on this side is on "
                        f"pp. {', '.join(str(p) for p in pages)} — see the other "
                        f"sections of this file, which carry the same analysis "
                        f"without splitting it by direction.")
            return NOT_ADDRESSED
        note = ("\n\n> *Assembled from statements the guide makes about this team. "
                "The statements are GUIDE CONTENT with page references; the "
                "selection of which ones argue this side is PERSONAL INFERENCE.*")
        return "\n".join(body) + note

    def questions(self, team, detail, right):
        notes = self.notes_for(team)
        if notes and notes.get("questions"):
            out = [f"VSiN poses *Three Burning Questions for the 2026 Season* "
                   f"*(p. {right})*. Its analysis, in reference form:\n"]
            for item in notes["questions"]:
                out.append(f"### {item['q']}\n\n{item['n']} *(p. {item['p']})*\n")
            out.append("*TTW reference notes. The questions are VSiN's; the "
                       "answers summarise VSiN's reasoning in TTW's wording.*")
            return "\n".join(out)
        if not detail["questions"]:
            return NOT_ADDRESSED
        out = [f"The guide's *Three Burning Questions for the 2026 Season* "
               f"*(p. {right})*, with the answers as written:\n"]
        for q in detail["questions"]:
            out.append(f"### {q['question']}\n\n{q['answer']}\n")
        return "\n".join(out)

    def conflicts(self, team, detail):
        rows = []
        if detail.get("returning_starters_conflict"):
            rows.append(f"- **Returning-starter arithmetic.** "
                        f"{detail['returning_starters_conflict']}")
        for c in self.d["stability_conflicts"]:
            if c["team"] == team["team"]:
                rows.append(f"- **Returning starters printed differently in two "
                            f"places.** {c['detail']}")
        for c in self.d["global_conflicts"]:
            if team["team"] in c["applies_to"]:
                rows.append(f"- **{c['title']}** {c['detail']}")
        if not rows:
            return "No source conflict identified for this team."
        return "\n".join(rows)

    def pages(self, team, detail, ref):
        mentions = self.d["mentions"][team["team"]]
        left, right = detail["pages"]
        preview = self.d["preview_page"][team["conference"]]
        rows = [
            f"| {left}–{right} | This team's two-page preview |",
            f"| {preview} | {team['conference']} conference preview and projected standings |",
            "| 4 | VSiN staff season predictions |",
            "| 46–47 | Steve Makinen power rating methodology |",
            "| 21 | Home-field advantage article |",
        ]
        others = [p for p in mentions["pages"] if p not in (left, right, preview, 4, 21)]
        if others:
            rows.append(f"| {', '.join(str(p) for p in others)} | "
                        f"Other pages naming this team |")
        table = ("| Pages | Content |\n| --- | --- |\n" + "\n".join(rows) +
                 f"\n\nThis team is named in **{mentions['total']} sentences across "
                 f"{len(mentions['pages'])} pages** of the guide.")
        if others:
            table += ("\n\nEvery page naming this team outside its own spread: "
                      f"pp. {', '.join(str(p) for p in others)}.")
        return table

    def links(self, team):
        conf = slug(team["conference"])
        return (
            f"**Conference** — [{team['conference']}]"
            f"(../01_Conference_Database/{conf}.md)\n\n"
            f"**Master Index** — "
            f"[Team Index](../00_Master_Index/03_Team_Index.md) · "
            f"[Power Rating Index](../00_Master_Index/09_Power_Rating_Index.md) · "
            f"[Coaching Index](../00_Master_Index/04_Coaching_Index.md) · "
            f"[Quarterback Index](../00_Master_Index/06_Quarterback_Index.md)\n\n"
            # This block once read "Not yet built -- these databases are
            # later phases and the links are placeholders". All of them are
            # now built, so the placeholders are live links. The Coaching
            # Database is keyed by TEAM, not by coach: the original pointer
            # was written before Phase 5 chose its naming and named a file
            # that existed under no convention, and it sat in backticks
            # rather than a link, so no checker had ever seen it.
            f"**Every other database, for this team:**\n\n"
            f"- Head coach — "
            f"[03_Coaching_Database/{slug(team['team'])}.md]"
            f"(../03_Coaching_Database/{slug(team['team'])}.md)\n"
            f"- Quarterback — "
            f"[04_Quarterback_Database/{slug(team['team'])}.md]"
            f"(../04_Quarterback_Database/{slug(team['team'])}.md)\n"
            f"- Power rating — "
            f"[05_Power_Ratings/00_MAKINEN_RATINGS.md]"
            f"(../05_Power_Ratings/00_MAKINEN_RATINGS.md)\n"
            f"- Win total — "
            f"[06_Win_Totals/00_ALL_TEAMS.md]"
            f"(../06_Win_Totals/00_ALL_TEAMS.md)\n"
            f"- Futures board — "
            f"[07_Futures/00_TEAM_FUTURES.md]"
            f"(../07_Futures/00_TEAM_FUTURES.md)\n"
            f"- Returning production — "
            f"[08_Returning_Production/README.md]"
            f"(../08_Returning_Production/README.md)\n"
            f"- Schedule — "
            f"[10_Schedule_Intelligence/00_BY_TEAM.md]"
            f"(../10_Schedule_Intelligence/00_BY_TEAM.md)\n"
            f"- Historical angles — "
            f"[12_Historical_Trends/00_BY_TEAM.md]"
            f"(../12_Historical_Trends/00_BY_TEAM.md)\n"
            f"- Everything at once — "
            f"[99_Search_Index/02_TEAM_LOOKUP.md]"
            f"(../99_Search_Index/02_TEAM_LOOKUP.md)\n"
        )


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def main():
    teams = load("teams")
    details = {t["team"]: t for t in load("team_details")}
    mentions = load("team_mentions")
    previews = load("conference_previews")
    standings, preview_page = {}, {}
    for conf in previews:
        preview_page[conf["conference"]] = conf["preview_page"]
        for row in conf["standings"]:
            standings[row["team"]] = row

    predictions = load("phase2_predictions")
    prediction_hits = {}
    for label, picks in predictions.items():
        tally = Counter(picks)
        for pick, votes in tally.items():
            for team in teams:
                if team["team"].lower().startswith(pick.lower()):
                    prediction_hits.setdefault(team["team"], []).append((label, votes))

    resolve = {}
    for conf in previews:
        for row in conf["standings"]:
            resolve[row["table_name"].upper()] = row["team"]
    for team in teams:
        resolve[team["team"].upper()] = team["team"]
        head = team["team"].rsplit(" ", 1)[0].upper()
        resolve.setdefault(head, team["team"])
    for alias, canon in {
        "OLE MISS": "Ole Miss Rebels", "MISSISSIPPI": "Ole Miss Rebels",
        "NORTH CAROLINA STATE": "NC State Wolfpack", "LSU": "LSU Tigers",
        "USC": "USC Trojans", "BYU": "BYU Cougars", "MIAMI": "Miami Hurricanes",
        "TEXAS A&M": "Texas A&M Aggies", "NOTRE DAME": "Notre Dame Fighting Irish",
        "OKLAHOMA": "Oklahoma Sooners", "GEORGIA": "Georgia Bulldogs",
        "TEXAS": "Texas Longhorns", "OREGON": "Oregon Ducks",
        "OHIO STATE": "Ohio State Buckeyes", "INDIANA": "Indiana Hoosiers",
        "SOUTH CAROLINA": "South Carolina Gamecocks", "AUBURN": "Auburn Tigers",
    }.items():
        resolve[alias] = canon

    global_conflicts = [
        {
            "title": "Charlotte printed in two conferences.",
            "detail": ("Charlotte appears in both the American (p. 49) and "
                       "Conference USA (p. 187) projected standings tables with "
                       "identical figures. The contents page, Charlotte's own "
                       "team page (p. 52, ranked #14 of 14 in the American) and "
                       "the '#N of 10' conference ranks on every Conference USA "
                       "team page all place Charlotte in the American."),
            "applies_to": {"Charlotte 49ers"},
        },
        {
            "title": "Head coach tenure stated inconsistently.",
            "detail": ("The American conference preview (p. 49) describes Brian "
                       "Newberry as beginning his fourth season; Navy's team page "
                       "(p. 60) states his fifth. Both are reproduced as printed "
                       "and neither is corrected."),
            "applies_to": {"Navy Midshipmen"},
        },
    ]

    data = {
        "details": details, "mentions": mentions, "standings": standings,
        "preview_page": preview_page, "coordinators": load("coordinators"),
        "new_coaches": load("phase2_new_coaches"),
        "win_totals": load("phase2_win_totals"),
        "best_bets": load("phase2_best_bets"),
        "qb_top15": load("quarterbacks_top15"), "top50": load("youmans_top50"),
        "prediction_hits": prediction_hits, "resolve": resolve,
        "paraphrases": load_paraphrases(),
        "stability": {r["team"]: r for r in load("stability_scores") if r.get("team")},
        "stability_conflicts": load("stability_conflicts"),
        "global_conflicts": global_conflicts,
    }

    only = sys.argv[1] if len(sys.argv) > 1 else None
    builder = TeamFileBuilder(data)
    os.makedirs(OUT, exist_ok=True)

    written = []
    for team in teams:
        if only and team["conference"].lower() != only.lower():
            continue
        path = os.path.join(OUT, f"{slug(team['team'])}.md")
        with open(path, "w") as fh:
            fh.write(BANNER + builder.build(team))
        written.append((team, path))

    print(f"team files written: {len(written)}"
          + (f" ({only})" if only else ""))
    return written


if __name__ == "__main__":
    main()
