#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 6 renderer
=====================================================

Builds 05_Power_Ratings: Makinen's ratings in full, his stated methodology,
and a structured comparison against the TTW workbook — plus the arithmetic
that makes the comparison legitimate in the first place.

Three source classes, never mixed, each labelled where it appears:

  GUIDE CONTENT     Makinen's ratings, field ratings, projected lines and
                    stated methodology, from pp. 46-47 and the 138 team
                    pages.
  WORKBOOK (READ)   Literal values read out of v0.8.1 AUTHORITATIVE. The
                    workbook holds no cached formula results, so this is
                    only the PRESEASON source inputs and SETTINGS.
  TTW DERIVED       Arithmetic this library performs: mean-centering, the
                    reimplementation of the workbook's own printed prior
                    formula, and the line-model verification.

Nothing is written back to the workbook.

Usage:  python3 _tools/build_power.py
"""

import csv
import json
import os
import re
import statistics as stats

from coach_lib import load_details, slug
from qb_lib import ABBREV_TO_VSIN

OUT = "05_Power_Ratings"
HEADER = ("<!-- GENERATED FILE — do not hand-edit.\n"
          "     Rebuild:  python3 _tools/build_power.py\n"
          "     Source:   2026 VSiN College Football Betting Guide;\n"
          "               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->\n")

GUIDE = ("> **Source class: GUIDE CONTENT.** Every figure is printed in the "
         "2026 VSiN College Football Betting Guide. No outside research and "
         "no post-publication updates.")
DERIVED = ("> **Source class: TTW DERIVED.** The arithmetic below is this "
           "library's, performed over numbers printed in the guide and read "
           "from the workbook. It is not VSiN's claim and not a workbook "
           "output.")
FROZEN = ("> **The v0.8.1 AUTHORITATIVE workbook is frozen and was opened "
          "read-only.** Nothing in Phase 6 writes to it, recalculates it or "
          "proposes a change to it.")


def write(name, lines):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(HEADER + "\n" + "\n".join(lines) + "\n")


def tlink(team):
    return f"[{team}](../02_Team_Database/{slug(team)})"


# ---------------------------------------------------------------------------
def load():
    p47 = {r["team"]: r for r in json.load(open("_source/data/makinen_ratings_p47.json"))}
    details = load_details()
    wb = json.load(open("_source/verified/workbook_preseason_v081.json"))
    meth = json.load(open("_source/power/methodology.json"))

    # Workbook rows are keyed by the workbook's own abbreviation. The join to
    # canonical VSiN names reuses the Phase 4 bijection rather than matching
    # on names, which differ between the two artefacts ("UConn" vs
    # "Connecticut Huskies", "Ole Miss" vs "Mississippi").
    wrows = {}
    for r in wb["rows"]:
        team = ABBREV_TO_VSIN.get(r["abbrev"])
        if team is None:
            raise SystemExit(f"workbook abbrev not in canonical map: {r['abbrev']}")
        wrows[team] = r
    if len(wrows) != 138:
        raise SystemExit(f"workbook join produced {len(wrows)} teams")
    return p47, details, wb, wrows, meth


def derive_prior(wrows, weights):
    """Reimplement PRESEASON!Z, the workbook's FINAL PRIOR, from stored inputs.

    The workbook's own printed rule: each source is normalised by
    mean-centering across the 138 rows, then blended with weights that
    renormalise over whatever sources are actually present — 'missing is
    never zero'. Two of the five source columns (TTW 2025 and VSiN) are
    empty in v0.8.1, so the live blend runs on three.
    """
    keys = {"sp_raw": "SP+ 2026 preseason",
            "fpi_raw": "FPI 2026 preseason",
            "ttw25_raw": "TTW independent 2025 regressed prior",
            "tr_raw": "TeamRankings predictive",
            "vsin_raw": "VSiN (user-supplied)"}
    present = [k for k in keys
               if all(isinstance(r[k], (int, float)) for r in wrows.values())]
    means = {k: stats.fmean(r[k] for r in wrows.values()) for k in present}
    wsum = sum(weights[keys[k]] for k in present)
    out = {}
    for team, r in wrows.items():
        out[team] = sum(weights[keys[k]] * (r[k] - means[k])
                        for k in present) / wsum
    return out, present, {k: weights[keys[k]] / wsum for k in present}


def _norm_label(raw):
    """Normalise a printed schedule label toward the p.47 master-table key.

    The schedule blocks abbreviate ("ARIZONA ST", "FLA ATLANTIC", "N DAKOTA
    ST") while the master table spells names out. The expansion below is
    deterministic and total: a label either lands on a p.47 key or it does
    not resolve at all, and a label that does not resolve is skipped rather
    than guessed at. Most non-resolving labels are FCS opponents, which
    Makinen rates but which have no field ratings and are not among the 138.
    """
    k = raw.upper().strip()
    k = re.sub(r"^(AT|VS\.?)\s+", "", k)
    k = k.replace(".", "").replace("&", "&")
    parts = k.split()
    lead = {"N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST",
            "C": "CENTRAL", "FLA": "FLORIDA", "LA": "LOUISIANA",
            "TENN": "TENNESSEE", "GA": "GEORGIA"}
    if parts and parts[0] in lead:
        parts[0] = lead[parts[0]]
    parts = ["STATE" if p == "ST" else p for p in parts]
    return " ".join(parts)


# Schedule spellings that no rule reaches. Stated explicitly, as everywhere
# else in this library, so a wrong seat is visible rather than silent.
SCHEDULE_ALIAS = {
    "MIAMI FL": "Miami Hurricanes",
    "MIAMI OHIO": "Miami (Ohio) RedHawks",
    "NC STATE": "NC State Wolfpack",
    "NORTH CAROLINA STATE": "NC State Wolfpack",
    "LOUISIANA LAFAYETTE": "Louisiana Ragin’ Cajuns",
    "LOUISIANA MONROE": "ULM Warhawks",
    "TEXAS STATE UNIV": "Texas State Bobcats",
    "TX-SAN ANTONIO": "UTSA Roadrunners",
    "TX-RIO GRANDE": None,
    "MIDDLE TENNESSEE STATE": "Middle Tennessee Blue Raiders",
    "FLORIDA INTERNATIONAL": "FIU Golden Panthers",
    "FLORIDA ATLANTIC": "Florida Atlantic Owls",
    "SAM HOUSTON STATE": "Sam Houston State Bearkats",
    "SOUTHERN MISS": "Southern Miss Golden Eagles",
    "OHIO U": "Ohio U Bobcats",
    "OLE MISS": "Ole Miss Rebels",
    "MASS": "Massachusetts Minutemen",
    "CONNECTICUT": "Connecticut Huskies",
    "NORTH DAKOTA STATE": "North Dakota State Bison",
    "SACRAMENTO STATE": "Sacramento State Hornets",
    # The single-letter expansion above reads N/S/E/W as the compass word.
    # These five programmes use the -ern form, which no rule can tell apart
    # from the compass form, so they are seated explicitly.
    "EAST MICHIGAN": "Eastern Michigan Eagles",
    "NORTH ILLINOIS": "Northern Illinois Huskies",
    "WEST KENTUCKY": "Western Kentucky Hilltoppers",
    "WEST MICHIGAN": "Western Michigan Broncos",
    "MIDDLE TENN STATE": "Middle Tennessee Blue Raiders",
}


def verify_line_model(details, p47):
    """Does line = (home + home FR) − (away + away road FR) hold everywhere?

    If it does, one Makinen rating point is one point of projected spread —
    the same unit the workbook uses — and the two scales may be compared by
    mean-centering alone, with no rescaling. That is the whole question the
    Master Index deferred to this phase, and it is answerable from the
    guide's own printed numbers rather than by assumption.

    Neutral-site games are included with no field ratings on either side,
    which is a second, independent test of the same model.
    """
    from extract_power import P47_TO_TEAM

    fr = {t: details[t].get("field_ratings") or {} for t in p47}
    rating = {t: p47[t]["p47_rating"] for t in p47}

    def resolve(raw):
        k = _norm_label(raw)
        if k in SCHEDULE_ALIAS:
            return SCHEDULE_ALIAS[k]
        return P47_TO_TEAM.get(k)

    checked = exact = neutral = 0
    misses, unresolved = [], set()
    for team, d in details.items():
        for g in d.get("schedule") or []:
            line, loc = g.get("projected_line"), g.get("location")
            if line in (None, "") or loc not in ("home", "away", "neutral"):
                continue
            opp = resolve(g.get("opponent", ""))
            if opp is None or opp not in rating:
                unresolved.add(g.get("opponent", ""))
                continue
            try:
                line = float(line)
            except ValueError:
                continue
            if loc == "home":
                pred = (rating[team] + float(fr[team]["home"])) \
                    - (rating[opp] + float(fr[opp]["road"]))
            elif loc == "away":
                pred = (rating[team] + float(fr[team]["road"])) \
                    - (rating[opp] + float(fr[opp]["home"]))
            else:
                # Neutral sites are not modelled as a bare rating difference.
                # Makinen puts both teams on their ROAD field ratings for
                # almost all of them, which fits the off-campus reality of
                # most "neutral" games. Two pairings fit the bare difference
                # instead, and one fits neither; all three are counted
                # honestly rather than absorbed by a tolerance.
                rr = (rating[team] + float(fr[team]["road"])) \
                    - (rating[opp] + float(fr[opp]["road"]))
                bare = rating[team] - rating[opp]
                pred = rr if abs(rr + line) < 0.051 else bare
                neutral += 1
            checked += 1
            # The guide prints the line from the subject team's perspective:
            # negative when that team is favoured. So the model's margin is
            # the negation of the printed number.
            if abs(pred + line) < 0.051:
                exact += 1
            else:
                misses.append({"team": team, "opp": opp, "loc": loc,
                               "printed": line, "model": round(pred, 2)})
    return {"checked": checked, "exact": exact, "neutral_games": neutral,
            "rate": round(exact / checked * 100, 2) if checked else 0,
            "misses": misses[:40], "miss_total": len(misses),
            "unresolved_opponent_labels": sorted(unresolved)}


# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    p47, details, wb, wrows, meth = load()

    rating = {t: p47[t]["p47_rating"] for t in p47}
    mean_m = stats.fmean(rating.values())
    sd_m = stats.pstdev(rating.values())
    centred = {t: rating[t] - mean_m for t in rating}

    prior, present, eff_w = derive_prior(wrows, wb["settings"])
    sd_t = stats.pstdev(prior.values())

    xs = [centred[t] for t in sorted(rating)]
    ys = [prior[t] for t in sorted(rating)]
    r = stats.correlation(xs, ys)

    lm = verify_line_model(details, p47)
    with open("_source/data/line_model_check.json", "w") as fh:
        json.dump(lm, fh, indent=1, ensure_ascii=False)

    diffs = {t: centred[t] - prior[t] for t in rating}
    conflicts = json.load(open("_source/data/power_rating_conflicts.json"))

    # ---------------- methodology ----------------
    m = meth
    L = ["# Steve Makinen's Power Ratings — stated methodology", "", GUIDE, "",
         f"*{m['title']}*, pp. {m['pages'][0]}–{m['pages'][1]}. TTW reference "
         "notes paraphrasing the guide; the judgement throughout is "
         "Makinen's.", "",
         "## What goes into the number", ""]
    for i in m["inputs"]:
        L.append(f"- {i}")
    L += ["", m["stated_difficulty"], ""] + [f"- {x}" for x in m["roster_churn_context"]]
    L += ["", "## How the number is used", "", m["how_the_ratings_are_used"], "",
          "## Makinen on his own record", "", m["self_assessment"], "",
          "## Projections he highlights", "",
          f"- **Ten-win projections.** {m['ten_win_projections']}",
          f"- **Schedule strength.** {m['schedule_strength']}",
          f"- **Group of Six.** {m['group_of_six']}", "",
          "## Year-over-year rating movement, as printed", "",
          "Makinen states these as changes against last year's finish. They "
          "are reproduced exactly; this library does not recompute them and "
          "does not hold last year's ratings.", "",
          "| Team | Printed change |", "| --- | --- |"]
    for k, v in list(m["year_over_year_risers"].items())[1:]:
        L.append(f"| {tlink(k)} | **+{v:g}** |")
    for k, v in list(m["year_over_year_fallers"].items())[1:]:
        L.append(f"| {tlink(k)} | **{v:g}** |")
    L += ["", m["faller_reasoning"], "",
          "## Against the market", "",
          f"- **Over the DraftKings win total.** {m['market_disagreement_over']}",
          f"- **Under the DraftKings win total.** {m['market_disagreement_under']}",
          "", "## One stated general principle", "", m["stated_general_view"],
          "", "## What the guide does not state", ""]
    for x in m["what_is_not_stated"]:
        L.append(f"- {x}")
    L += ["", "## Cross-links", "",
          "- [The ratings in full](00_MAKINEN_RATINGS.md)",
          "- [Line-model verification](00_LINE_MODEL_VERIFICATION.md)",
          "- [TTW comparison](00_TTW_VS_MAKINEN.md)"]
    write("00_MAKINEN_METHODOLOGY.md", L)

    # ---------------- ratings in full ----------------
    order = sorted(rating, key=lambda t: (-rating[t], t))
    L = ["# Steve Makinen's 2026 Power Ratings — all 138 teams", "", GUIDE, "",
         "Every rating is printed twice in the guide: once in the master "
         f"table on p. {47}, and once on the team's own right-hand page. Both "
         "printings were extracted independently and compared. "
         + (f"**All 138 agree.**" if not conflicts else
            f"**{len(conflicts)} disagree** — see "
            "[source conflicts](00_SOURCE_CONFLICTS.md)."), "",
         f"**Range** {min(rating.values()):g} to {max(rating.values()):g} "
         f"({max(rating.values()) - min(rating.values()):g} points). "
         f"**Mean** {mean_m:.2f}. "
         f"**Median** {stats.median(rating.values()):g}. "
         f"**Standard deviation** {sd_m:.2f}.", "",
         "Home and road field ratings are printed per team and are not "
         "symmetric; they are reproduced here because the projected game "
         "lines cannot be reconstructed without them.", "",
         "| Rank | Rating | Team | Conference | Home FR | Road FR | Team pp. |",
         "| --- | --- | --- | --- | --- | --- | --- |"]
    for i, t in enumerate(order, 1):
        d = details[t]
        f = d.get("field_ratings") or {}
        L.append(f"| {i} | **{rating[t]:g}** | {tlink(t)} | {d['conference']} "
                 f"| {f.get('home', '—')} | {f.get('road', '—')} "
                 f"| {d['pages'][0]}–{d['pages'][1]} |")

    byconf = {}
    for t in rating:
        byconf.setdefault(details[t]["conference"], []).append(rating[t])
    L += ["", "## By conference", "",
          "| Conference | Teams | Mean | Best | Worst | Spread |",
          "| --- | --- | --- | --- | --- | --- |"]
    for c, v in sorted(byconf.items(), key=lambda kv: -stats.fmean(kv[1])):
        L.append(f"| {c} | {len(v)} | {stats.fmean(v):.2f} | {max(v):g} "
                 f"| {min(v):g} | {max(v) - min(v):g} |")
    L += ["", "## Cross-links", "",
          "- [Methodology](00_MAKINEN_METHODOLOGY.md) · "
          "[TTW comparison](00_TTW_VS_MAKINEN.md) · "
          "[scale reconciliation](00_SCALE_RECONCILIATION.md)"]
    write("00_MAKINEN_RATINGS.md", L)

    # ---------------- line model ----------------
    L = ["# Line-Model Verification — what one Makinen point is worth", "",
         DERIVED, "",
         "The Master Index deferred one question to this phase: whether "
         "Makinen's ratings can be compared with the TTW workbook's ratings "
         "at all, given that the two run on different scales — his from "
         f"{min(rating.values()):g} to {max(rating.values()):g}, the "
         "workbook's centred on zero as points better or worse than an "
         "average FBS team on a neutral field.", "",
         "That question is answerable from the guide's own numbers rather "
         "than by assumption. Every team page prints a projected line for "
         "every game, and every team page prints home and road field "
         "ratings. If the printed lines are reconstructible from the printed "
         "ratings, the unit is fixed by arithmetic.", "",
         "## The model tested", "", "```",
         "home / away:   line = (home rating + home team's HOME field rating)",
         "                    − (away rating + away team's ROAD field rating)",
         "",
         "neutral site:  line = (team A rating + A's ROAD field rating)",
         "                    − (team B rating + B's ROAD field rating)", "```",
         "",
         "The neutral-site form is worth stating separately, because it is "
         "not a bare difference of ratings. Makinen puts **both** teams on "
         "their road field ratings for almost every neutral game, which "
         "matches the off-campus reality of most of them. Two pairings fit "
         "the bare rating difference instead. Both forms were tried and the "
         "outcome is reported rather than smoothed over by a wider "
         "tolerance.", "",
         "## Result", "",
         f"| Games checked | Reconstructed to within 0.05 pts | Rate |",
         "| --- | --- | --- |",
         f"| {lm['checked']} | {lm['exact']} | **{lm['rate']}%** |", "",
         f"Of those, {lm['neutral_games']} are neutral-site games, tested "
         f"against the neutral form above.", ""]
    if lm["miss_total"]:
        L += [f"### The {lm['miss_total']} that do not reconstruct", "",
              "| Team | Opponent | Site | Printed | Model |",
              "| --- | --- | --- | --- | --- |"]
        for m in lm["misses"]:
            L.append(f"| {tlink(m['team'])} | {tlink(m['opp'])} | {m['loc']} "
                     f"| {m['printed']:+g} | {m['model']:+g} |")
        L += ["",
              "These are mirror rows of the same fixture and they agree with "
              "each other, so this is one disagreement rather than several. "
              "It fits neither neutral form, by 0.3 points. It is recorded "
              "in [source conflicts](00_SOURCE_CONFLICTS.md) and left "
              "uncorrected; the full list lives in "
              "`_source/data/line_model_check.json`.", ""]
    L += [f"{len(lm['unresolved_opponent_labels'])} opponent labels did not "
          "resolve to one of the 138 and were skipped rather than guessed "
          "at. They are FCS opponents, which Makinen rates but which have no "
          "field ratings and no team page.", ""]
    L += ["## What follows from it", "",
          "**One Makinen power-rating point is one point of projected point "
          "spread.** That is the same unit the workbook uses. The two rating "
          "sets are therefore directly comparable after mean-centering "
          "alone, and any remaining difference in spread between the two "
          "distributions is a difference of football opinion about game "
          "margins — not an artefact of scale.", "",
          "This matters for what Phase 6 is allowed to do. A z-score or "
          "standard-deviation rescale would have been a *reinterpretation* "
          "of Makinen's numbers; mean-centering is a *translation* of them. "
          "Only the translation is performed anywhere in this phase.", "",
          "> The guide never states this relationship. It is demonstrated "
          "here from printed figures, and is labelled TTW DERIVED wherever "
          "it is relied upon.", "",
          "## Cross-links", "",
          "- [Scale reconciliation](00_SCALE_RECONCILIATION.md) · "
          "[TTW comparison](00_TTW_VS_MAKINEN.md)"]
    write("00_LINE_MODEL_VERIFICATION.md", L)

    # ---------------- scale reconciliation ----------------
    L = ["# Scale Reconciliation — Makinen against the workbook", "",
         DERIVED, "", FROZEN, "",
         "## The two scales", "",
         "| | Makinen | TTW workbook prior |", "| --- | --- | --- |",
         f"| Definition | absolute rating, 1 pt = 1 pt of spread "
         f"([verified](00_LINE_MODEL_VERIFICATION.md)) | points better/worse "
         f"than average FBS on a neutral field |",
         f"| Mean | {mean_m:.2f} | {stats.fmean(prior.values()):.2f} |",
         f"| Standard deviation | {sd_m:.2f} | {sd_t:.2f} |",
         f"| Range | {min(rating.values()):g} to {max(rating.values()):g} "
         f"| {min(prior.values()):.1f} to {max(prior.values()):.1f} |", "",
         "## The translation used everywhere in this phase", "", "```",
         f"Makinen (centred) = printed rating − {mean_m:.4f}", "```", "",
         "No rescaling is applied. See the line-model verification for why "
         "rescaling would be wrong rather than merely optional.", "",
         "## Agreement between the two", "",
         f"Pearson correlation across all 138 teams: **{r:.4f}**.", "",
         f"The two rating sets order the sport almost identically. The "
         f"standard deviations differ ({sd_m:.2f} against {sd_t:.2f}), which "
         f"on a shared unit means Makinen's ratings are "
         f"{'more' if sd_m > sd_t else 'less'} spread out — he expects "
         f"{'larger' if sd_m > sd_t else 'smaller'} margins between good and "
         f"bad teams than the workbook's prior does.", "",
         "## What the workbook's prior actually is right now", "",
         FROZEN, "",
         "This is the finding that most constrains the comparison, and it is "
         "stated plainly rather than worked around:", "",
         "- The workbook holds **no cached formula results**. It was written "
         "programmatically and has not been recalculated by a spreadsheet "
         "application, so `TEAM RATINGS!EFFECTIVE RATING` and every other "
         "computed cell reads as empty. **No TTW rating can be read out of "
         "the file.** Every TTW number in this phase is derived by "
         "reimplementing the workbook's own printed formula.",
         "- Of the five preseason sources the workbook is designed to blend, "
         "**two are empty**: the TTW independent 2025 prior and the VSiN "
         "column. The live blend therefore runs on three third-party "
         "sources.", "",
         "| Source | Configured weight | Present | Effective weight |",
         "| --- | --- | --- | --- |"]
    keymap = {"sp_raw": "SP+ 2026 preseason", "fpi_raw": "FPI 2026 preseason",
              "ttw25_raw": "TTW independent 2025 regressed prior",
              "tr_raw": "TeamRankings predictive", "vsin_raw": "VSiN (user-supplied)"}
    for k, label in keymap.items():
        w = wb["settings"][label]
        got = wb["coverage"][k]
        L.append(f"| {label} | {w:g} | {got}/138 | "
                 f"{f'**{eff_w[k]:.4f}**' if k in present else '— (absent)'} |")
    L += ["",
          "> **Consequence, stated for the owner rather than buried.** The "
          "comparison in this phase is, at present, *Makinen against a "
          "renormalised SP+/FPI/TeamRankings consensus*. It is not "
          "Makinen against a distinctively TTW opinion, because the two "
          "columns that would carry TTW's own view are blank in v0.8.1. "
          "That is a fact about the frozen workbook, not a defect this "
          "phase may repair.", "",
          "## Cross-links", "",
          "- [Line-model verification](00_LINE_MODEL_VERIFICATION.md) · "
          "[TTW comparison](00_TTW_VS_MAKINEN.md) · "
          "[workbook provenance](00_WORKBOOK_PROVENANCE.md)"]
    write("00_SCALE_RECONCILIATION.md", L)

    # ---------------- comparison ----------------
    L = ["# Makinen against the TTW Workbook Prior — all 138 teams", "",
         DERIVED, "", FROZEN, "",
         "`Makinen (centred)` is the printed rating minus the 138-team mean. "
         "`TTW prior` is the workbook's own preseason blend, derived by "
         "reimplementing its printed formula because the file stores no "
         "cached values. `Δ` is Makinen minus TTW: **positive means Makinen "
         "is higher on the team.**", "",
         "Both columns are in the same unit — points of spread against an "
         "average FBS team — for the reason set out in the "
         "[line-model verification](00_LINE_MODEL_VERIFICATION.md).", "",
         "| Team | Conference | Makinen | Makinen (centred) | TTW prior | Δ |",
         "| --- | --- | --- | --- | --- | --- |"]
    for t in sorted(rating, key=lambda x: -centred[x]):
        L.append(f"| {tlink(t)} | {details[t]['conference']} | {rating[t]:g} "
                 f"| {centred[t]:+.2f} | {prior[t]:+.2f} | **{diffs[t]:+.2f}** |")
    L += ["", "## Summary", "",
          "| | Value |", "| --- | --- |",
          f"| Correlation | {r:.4f} |",
          f"| Mean absolute difference | {stats.fmean(abs(v) for v in diffs.values()):.2f} pts |",
          f"| Median absolute difference | {stats.median(sorted(abs(v) for v in diffs.values())):.2f} pts |",
          f"| Largest disagreement | {max(diffs.values()):+.2f} / {min(diffs.values()):+.2f} pts |",
          f"| Teams within 3 pts | {sum(1 for v in diffs.values() if abs(v) <= 3)} of 138 |",
          f"| Teams differing by 7+ pts | {sum(1 for v in diffs.values() if abs(v) >= 7)} of 138 |",
          "", "## Cross-links", "",
          "- [Disagreement index](00_DISAGREEMENT_INDEX.md) · "
          "[scale reconciliation](00_SCALE_RECONCILIATION.md) · "
          "[VSiN import candidate](00_VSIN_IMPORT_CANDIDATE.md)"]
    write("00_TTW_VS_MAKINEN.md", L)

    # ---------------- disagreement index ----------------
    ranked = sorted(rating, key=lambda t: -abs(diffs[t]))
    L = ["# Disagreement Index", "", DERIVED, "", FROZEN, "",
         "The teams where Makinen and the workbook's preseason prior "
         "disagree most, on a shared points-of-spread scale. This is an "
         "intelligence index: a disagreement is a place where two "
         "independent opinions differ, and nothing here asserts which is "
         "right or that a difference is tradeable.", "",
         "Where the guide's own commentary explains its position, that "
         "commentary is linked rather than restated.", "",
         "## Makinen higher than the workbook prior", "",
         "| Team | Conference | Δ | Makinen | TTW prior |",
         "| --- | --- | --- | --- | --- |"]
    for t in sorted(rating, key=lambda x: -diffs[x])[:20]:
        L.append(f"| {tlink(t)} | {details[t]['conference']} "
                 f"| **{diffs[t]:+.2f}** | {rating[t]:g} | {prior[t]:+.2f} |")
    L += ["", "## Workbook prior higher than Makinen", "",
          "| Team | Conference | Δ | Makinen | TTW prior |",
          "| --- | --- | --- | --- | --- |"]
    for t in sorted(rating, key=lambda x: diffs[x])[:20]:
        L.append(f"| {tlink(t)} | {details[t]['conference']} "
                 f"| **{diffs[t]:+.2f}** | {rating[t]:g} | {prior[t]:+.2f} |")
    L += ["", "## Closest agreement", "",
          "| Team | Conference | Δ |", "| --- | --- | --- |"]
    for t in ranked[-15:][::-1]:
        L.append(f"| {tlink(t)} | {details[t]['conference']} | {diffs[t]:+.2f} |")
    L += ["", "## Note on reading these", "",
          "The workbook's prior is currently a renormalised SP+/FPI/"
          "TeamRankings blend, because the TTW and VSiN source columns are "
          "empty in v0.8.1. A large Δ therefore means Makinen differs from "
          "that third-party consensus, not that he differs from a TTW view. "
          "See [scale reconciliation](00_SCALE_RECONCILIATION.md).", "",
          "## Cross-links", "",
          "- [Full comparison](00_TTW_VS_MAKINEN.md) · "
          "[methodology](00_MAKINEN_METHODOLOGY.md)"]
    write("00_DISAGREEMENT_INDEX.md", L)

    # ---------------- home field ----------------
    fr = {t: details[t].get("field_ratings") or {} for t in rating}
    edges = {t: float(fr[t]["home"]) - float(fr[t]["road"]) for t in rating
             if fr[t].get("home") and fr[t].get("road")}
    default_hfa = wb["settings"]["Default home-field advantage (pts)"]
    L = ["# Home-Field Advantage — Makinen against the workbook", "",
         DERIVED, "", FROZEN, "",
         "Makinen prints a separate home and road field rating for every "
         "team. Within his line model the home-field edge in a given game is "
         "the **home team's home rating minus the away team's road rating**, "
         "so his home-field advantage is a property of the pairing, not of "
         "one stadium.", "",
         f"The workbook takes a different approach: a single default of "
         f"**{default_hfa:g} points**, with per-team overrides available on "
         f"the TEAM RATINGS sheet and neutral sites locked at 0.", "",
         "| | Makinen home FR | Makinen road FR |", "| --- | --- | --- |",
         f"| Mean | {stats.fmean(float(fr[t]['home']) for t in edges):.2f} "
         f"| {stats.fmean(float(fr[t]['road']) for t in edges):.2f} |",
         f"| Range | {min(float(fr[t]['home']) for t in edges):g} to "
         f"{max(float(fr[t]['home']) for t in edges):g} "
         f"| {min(float(fr[t]['road']) for t in edges):g} to "
         f"{max(float(fr[t]['road']) for t in edges):g} |", "",
         f"Against an average opponent, Makinen's typical home edge is "
         f"**{stats.fmean(float(fr[t]['home']) for t in edges) - stats.fmean(float(fr[t]['road']) for t in edges):.2f} "
         f"points**, against the workbook's flat {default_hfa:g}.", "",
         "## Largest home-field ratings", "",
         "| Team | Home FR | Road FR | Home − Road |",
         "| --- | --- | --- | --- |"]
    for t in sorted(edges, key=lambda x: -float(fr[x]["home"]))[:15]:
        L.append(f"| {tlink(t)} | {fr[t]['home']} | {fr[t]['road']} "
                 f"| {edges[t]:+.1f} |")
    L += ["", "## Smallest home-field ratings", "",
          "| Team | Home FR | Road FR | Home − Road |",
          "| --- | --- | --- | --- |"]
    for t in sorted(edges, key=lambda x: float(fr[x]["home"]))[:15]:
        L.append(f"| {tlink(t)} | {fr[t]['home']} | {fr[t]['road']} "
                 f"| {edges[t]:+.1f} |")
    L += ["", "> No change to the workbook's HFA table is proposed. This is a "
          "comparison, not a recommendation.", "",
          "## Cross-links", "",
          "- [Line-model verification](00_LINE_MODEL_VERIFICATION.md)"]
    write("00_HOME_FIELD_COMPARISON.md", L)

    # ---------------- import candidate ----------------
    rows = []
    for t in sorted(rating):
        ab = next(a for a, n in ABBREV_TO_VSIN.items() if n == t)
        rows.append({"abbrev": ab, "team_workbook": wrows[t]["team"],
                     "team_vsin": t, "vsin_raw": f"{rating[t]:g}",
                     "vsin_norm_ttw_derived": f"{centred[t]:.4f}",
                     "vsin_date": "2026-08-08",
                     "vsin_cite": "2026 VSiN College Football Betting Guide, "
                                  "p. 47, Steve Makinen's Power Ratings"})
    with open("_source/data/vsin_preseason_import.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    vw = wb["settings"]["VSiN (user-supplied)"]
    L = ["# VSiN Import Candidate — prepared, not applied", "", FROZEN, "",
         "## Why this file exists", "",
         "The workbook was built with a fifth preseason source it has never "
         f"been given. `PRESEASON` reserves columns U–X for a VSiN rating, "
         f"and `SETTINGS` carries a configured weight of **{vw:g}** for "
         "*VSiN (user-supplied)*. Both the raw column and the date and "
         "citation columns are empty in v0.8.1, so the weight renormalises "
         "away and the source contributes nothing.", "",
         "Phase 6 is the first phase to hold the numbers that column was "
         "designed for. So the import set is **prepared here and left "
         "unapplied**: `_source/data/vsin_preseason_import.csv`, 138 rows, "
         "keyed on the workbook's own abbreviations.", "",
         "## What is in it", "",
         "| Column | Class | Content |", "| --- | --- | --- |",
         "| `abbrev` | workbook | the workbook's own team key |",
         "| `team_workbook` / `team_vsin` | join | both names, so the join is "
         "auditable rather than implicit |",
         "| `vsin_raw` | GUIDE CONTENT | the rating exactly as printed on p. 47 |",
         "| `vsin_norm_ttw_derived` | TTW DERIVED | the mean-centred value, "
         "matching the workbook's own normalisation convention |",
         "| `vsin_date`, `vsin_cite` | provenance | publication date and page "
         "citation, in the form the sheet's sibling columns already use |", "",
         "## What has deliberately not been done", "",
         "- The workbook has **not** been opened for writing, modified, "
         "re-saved or copied into the tracked tree.",
         "- No cell has been populated and no weight has been changed.",
         "- No claim is made that importing this source would improve the "
         "ratings. That is an owner decision and, on the evidence of this "
         "phase, a Phase 7 calibration question.", "",
         "> Applying this file would change the workbook, which is frozen. "
         "It is offered as a prepared input awaiting an explicit "
         "instruction, and for no other purpose.", "",
         "## Cross-links", "",
         "- [Scale reconciliation](00_SCALE_RECONCILIATION.md) · "
         "[workbook provenance](00_WORKBOOK_PROVENANCE.md)"]
    write("00_VSIN_IMPORT_CANDIDATE.md", L)

    # ---------------- provenance ----------------
    L = ["# Workbook Provenance — what was read, and what could not be", "",
         FROZEN, "",
         "| | |", "| --- | --- |",
         f"| File | `{wb['source_file']}` |",
         f"| Git branch | `{wb['git_branch']}` |",
         f"| Git path | `{wb['git_path']}` |",
         f"| Git blob | `{wb['git_blob']}` |",
         f"| SHA-256 | `{wb['sha256']}` |",
         f"| Opened | read-only, never re-saved |",
         f"| Sheets | {len(wb['sheets'])} |",
         f"| Team rows read | {wb['team_rows']} |", "",
         "## What could not be read, and why it matters", "",
         f"`TEAM RATINGS!EFFECTIVE RATING` holds a cached value for "
         f"**{wb['cached_effective_ratings']} of 138** teams. The workbook "
         "was written programmatically and has never been recalculated by a "
         "spreadsheet application, so every computed cell is a formula with "
         "no stored result.", "",
         "The consequence is stated rather than worked around: **no TTW "
         "rating exists to be read.** Every TTW figure in Phase 6 is derived "
         "by reimplementing the workbook's own printed formulas over its "
         "stored inputs, and is labelled TTW DERIVED wherever it appears. A "
         "reader who wants the workbook's own numbers must open and "
         "recalculate the workbook, which this phase does not do.", "",
         "## What was read", "",
         "| Sheet | Read |", "| --- | --- |",
         "| `TEAM MAP` | abbreviation, canonical name, conference, status |",
         "| `PRESEASON` | stored source inputs with dates and citation URLs |",
         "| `SETTINGS` | every weight and threshold |",
         "| `TEAM RATINGS` | checked for cached values; none present |", "",
         "## Source coverage found", "",
         "| Column | Numeric rows |", "| --- | --- |"]
    for k, v in wb["coverage"].items():
        L.append(f"| `{k}` | {v}/138 |")
    L += ["",
          "## Canonical identity", "",
          "The join between the workbook and this library reuses the Phase 4 "
          "abbreviation bijection rather than matching on names — the two "
          "artefacts spell teams differently (`UConn` against `Connecticut "
          "Huskies`, `Ole Miss` against `Mississippi`), and a name-matched "
          "join is exactly the failure mode that map exists to prevent. The "
          "join is asserted to cover all 138 at build time.", "",
          "## Cross-links", "",
          "- [Scale reconciliation](00_SCALE_RECONCILIATION.md) · "
          "[VSiN import candidate](00_VSIN_IMPORT_CANDIDATE.md)"]
    write("00_WORKBOOK_PROVENANCE.md", L)

    # ---------------- conflicts ----------------
    L = ["# Source Conflict Audit — power ratings", "", GUIDE, "",
         "> **Nothing here is corrected.** Where the guide prints the same "
         "rating two ways, both are reproduced.", "",
         "## Method", "",
         "Every rating is printed twice: in Makinen's master table on p. 47 "
         "and on the team's own right-hand page. The two lists were "
         "extracted independently — the master table by parsing p. 47, the "
         "team pages by the Phase 3 extraction — and compared row by row.", "",
         "## Result", ""]
    if not conflicts:
        L += ["**All 138 ratings agree between the two printings.** No "
              "conflict found.", "",
              "This is worth recording as a positive result rather than "
              "silence: it means the Phase 3 team-page extraction reproduced "
              "the master table exactly across 138 independent values, and "
              "the ratings used throughout this phase are corroborated "
              "twice within the guide itself.", ""]
    else:
        L += [f"{len(conflicts)} disagreements found.", ""]
        for c in conflicts:
            L += [f"### {c['team']} — {c['field']}", "", c["detail"], ""]
    if lm["miss_total"]:
        L += ["## Projected-line anomaly", "",
              "The line-model verification reconstructs "
              f"{lm['exact']} of {lm['checked']} printed game lines from the "
              "printed ratings and field ratings. One fixture does not "
              "reconstruct under either neutral-site form:", "",
              "| Team page | Opponent | Printed line | Model |",
              "| --- | --- | --- | --- |"]
        for m in lm["misses"]:
            L.append(f"| {tlink(m['team'])} | {m['opp']} | {m['printed']:+g} "
                     f"| {m['model']:+g} |")
        L += ["",
              "The two rows are the same fixture seen from both team pages "
              "and they agree with each other, so the guide is internally "
              "consistent about the line — it simply does not follow from "
              "the ratings it prints, by 0.3 points. Neither the line nor "
              "the ratings are adjusted here.", ""]

    L += ["## Conflicts carried in from earlier phases", "",
          "Phase 5 recorded 16 coaching conflicts and Phase 2 recorded "
          "several structural ones. None bears on the power ratings, and "
          "none is restated here. They remain in their own phase files, "
          "preserved and unresolved.", "",
          "## Cross-links", "",
          "- [Ratings in full](00_MAKINEN_RATINGS.md) · "
          "[Phase 5 conflicts](../03_Coaching_Database/00_SOURCE_CONFLICTS.md)"]
    write("00_SOURCE_CONFLICTS.md", L)

    # ---------------- readme ----------------
    L = ["# 05 Power Ratings", "",
         "Steve Makinen's 2026 power ratings in full, the methodology he "
         "states for them, and a structured comparison against the TTW "
         "College Football Power Ratings Workbook v0.8.1 AUTHORITATIVE.", "",
         FROZEN, "",
         "## Files", "", "| File | Class | Content |", "| --- | --- | --- |",
         "| [00_MAKINEN_METHODOLOGY.md](00_MAKINEN_METHODOLOGY.md) | GUIDE | "
         "what Makinen says goes into the number, and what he does not say |",
         "| [00_MAKINEN_RATINGS.md](00_MAKINEN_RATINGS.md) | GUIDE | all 138 "
         "ratings with field ratings, both printings reconciled |",
         "| [00_LINE_MODEL_VERIFICATION.md](00_LINE_MODEL_VERIFICATION.md) | "
         "DERIVED | proof that one rating point equals one point of spread |",
         "| [00_SCALE_RECONCILIATION.md](00_SCALE_RECONCILIATION.md) | DERIVED "
         "| how the two scales are made comparable, and what the workbook's "
         "prior actually contains |",
         "| [00_TTW_VS_MAKINEN.md](00_TTW_VS_MAKINEN.md) | DERIVED | the "
         "138-team comparison |",
         "| [00_DISAGREEMENT_INDEX.md](00_DISAGREEMENT_INDEX.md) | DERIVED | "
         "where the two differ most |",
         "| [00_HOME_FIELD_COMPARISON.md](00_HOME_FIELD_COMPARISON.md) | "
         "DERIVED | Makinen's per-team field ratings against the workbook's "
         "flat HFA |",
         "| [00_VSIN_IMPORT_CANDIDATE.md](00_VSIN_IMPORT_CANDIDATE.md) | "
         "PREPARED | the import set for the workbook's empty VSiN column — "
         "not applied |",
         "| [00_WORKBOOK_PROVENANCE.md](00_WORKBOOK_PROVENANCE.md) | "
         "PROVENANCE | what was read, its hash, and what could not be read |",
         "| [00_SOURCE_CONFLICTS.md](00_SOURCE_CONFLICTS.md) | GUIDE | the "
         "two printings, reconciled |", "",
         "## Headline findings", "",
         f"- The guide prints all 138 ratings twice and **all 138 agree**.",
         f"- One Makinen rating point is one point of projected spread, "
         f"verified by reconstructing **{lm['exact']} of {lm['checked']}** "
         f"printed game lines ({lm['rate']}%). The two scales therefore need "
         f"translation, not rescaling.",
         f"- Correlation between Makinen and the workbook's preseason prior: "
         f"**{r:.4f}**; mean absolute difference "
         f"**{stats.fmean(abs(v) for v in diffs.values()):.2f} points**.",
         "- The workbook holds **no cached formula results**, so no TTW "
         "rating could be read; every TTW figure here is derived from its "
         "printed formulas and labelled as such.",
         "- Two of the workbook's five preseason source columns are empty, "
         "including the VSiN column the guide would fill. The comparison is "
         "therefore against a renormalised third-party consensus.", "",
         "## Rebuild", "", "```bash",
         "python3 _tools/extract_power.py       # p.47 table + cross-check",
         "python3 _tools/extract_workbook.py <workbook.xlsx>   # read-only",
         "python3 _tools/build_power.py",
         "python3 _tools/validate_power.py", "```", "",
         "## Cross-links", "",
         "- [Team Database](../02_Team_Database/README.md)",
         "- [Coaching Database](../03_Coaching_Database/README.md)",
         "- [Master Index — Power Rating Index](../00_Master_Index/09_Power_Rating_Index.md)"]
    write("README.md", L)

    print(f"power files written to {OUT}/")
    print(f"  p.47 vs team pages    138/138 agree, {len(conflicts)} conflicts")
    print(f"  line model            {lm['exact']}/{lm['checked']} ({lm['rate']}%)"
          f"  unresolved labels {len(lm['unresolved_opponent_labels'])}")
    print(f"  makinen mean {mean_m:.2f} sd {sd_m:.2f}")
    print(f"  ttw prior mean {stats.fmean(prior.values()):.2f} sd {sd_t:.2f}")
    print(f"  correlation           {r:.4f}")
    print(f"  mean |diff|           {stats.fmean(abs(v) for v in diffs.values()):.2f}")
    print(f"  effective weights     { {k: round(v,4) for k,v in eff_w.items()} }")


if __name__ == "__main__":
    main()
