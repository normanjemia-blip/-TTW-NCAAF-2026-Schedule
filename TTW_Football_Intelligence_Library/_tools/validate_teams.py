#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Phase 3 Validation
=======================================================

Checks the built team database against the Phase 3 completion requirements:

  * 138 team files exist, one per FBS team, none duplicated, none missing
  * every file carries all 29 standardised headings in the correct order
  * every team maps to exactly one canonical conference
  * every printed Makinen rating reconciles to the Phase 1 / Phase 2 figures
  * every file carries page provenance
  * deferred values are explicitly marked

Exits non-zero if any check fails.

Usage:
    python3 _tools/validate_teams.py
"""

import json
import os
import re
import sys
from collections import Counter

SRC = "_source/data"
OUT = "02_Team_Database"

NO_CONFLICT = "No source conflict identified for this team."

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


def load(name):
    with open(os.path.join(SRC, f"{name}.json")) as fh:
        return json.load(fh)


def slug(name):
    # Matches coach_lib.slug and build_teams.slug. All three diverged on
    # "&" until Phase 11's repository-wide link check exposed it.
    s = name.lower().replace("\u2019", "").replace("'", "").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def main():
    teams = load("teams")
    details = {t["team"]: t for t in load("team_details")}
    previews = load("conference_previews")
    standings = {r["team"]: r for c in previews for r in c["standings"]}

    failures, notes = [], []

    files = {f for f in os.listdir(OUT) if f.endswith(".md") and f != "README.md"}
    expected = {f"{slug(t['team'])}.md" for t in teams}

    if len(teams) != 138:
        failures.append(f"expected 138 teams, source lists {len(teams)}")
    missing = expected - files
    extra = files - expected
    if missing:
        failures.append(f"missing team files: {sorted(missing)[:5]}")
    if extra:
        failures.append(f"unexpected files: {sorted(extra)[:5]}")

    slugs = Counter(slug(t["team"]) for t in teams)
    dupes = [s for s, n in slugs.items() if n > 1]
    if dupes:
        failures.append(f"duplicate team slugs: {dupes}")

    conf_of = {}
    for t in teams:
        conf_of.setdefault(t["team"], set()).add(t["conference"])
    multi = [k for k, v in conf_of.items() if len(v) != 1]
    if multi:
        failures.append(f"teams mapped to more than one conference: {multi}")

    schema_ok = rating_ok = provenance_ok = 0
    deferred_marks, conflict_files, no_conflict_files = 0, 0, 0

    for team in teams:
        path = os.path.join(OUT, f"{slug(team['team'])}.md")
        if not os.path.exists(path):
            continue
        text = open(path).read()

        headings = re.findall(r"^## \d+\. (.+)$", text, re.M)
        if headings == SCHEMA:
            schema_ok += 1
        else:
            failures.append(f"{team['team']}: schema mismatch "
                            f"({len(headings)} headings)")

        printed = details[team["team"]]["power_rating"]
        phase1 = team["power_rating"]
        phase2 = standings[team["team"]]["sm_power_rating"]
        if (float(printed) == float(phase1) == float(phase2)
                and re.search(rf"\*\*{re.escape(str(printed))}\*\* — as printed", text)):
            rating_ok += 1
        else:
            failures.append(
                f"{team['team']}: rating reconciliation failed "
                f"(file {printed}, phase1 {phase1}, phase2 {phase2})")

        if re.search(r"\(p\. \d+\)|pp\. \d+", text):
            provenance_ok += 1
        else:
            failures.append(f"{team['team']}: no page provenance found")

        deferred_marks += len(re.findall(r"DEFERRED — EXTRACTION NOT RELIABLE", text))
        # This counter searched for the literal uppercase "SOURCE CONFLICT",
        # which the team schema never renders -- its heading is "## 27. Source
        # Conflicts". It therefore never measured what it printed. After the
        # N-2 repair it began matching the words "SOURCE CONFLICT block" inside
        # a Phase 5 citation, so it reported 7 while 74 files carried a
        # conflict. It now counts §27 bullets, and the complement is counted
        # beside it so the two must add to 138.
        if re.search(r"\n## 27\. Source Conflicts\n\n- \*\*", text):
            conflict_files += 1
        elif NO_CONFLICT in text:
            no_conflict_files += 1

    if conflict_files + no_conflict_files != len(teams):
        failures.append(f"§27 accounting: {conflict_files} carry a conflict + "
                        f"{no_conflict_files} assert none != {len(teams)} teams")

    print(f"team files present                 {len(files)}/138")
    print(f"schema complete (29 headings)      {schema_ok}/138")
    print(f"power ratings reconciled           {rating_ok}/138")
    print(f"files with page provenance         {provenance_ok}/138")
    print(f"files carrying a source conflict   {conflict_files}")
    print(f"files asserting no source conflict {no_conflict_files}")
    print(f"explicit deferred markers          {deferred_marks}")

    conferences = Counter(t["conference"] for t in teams)
    print("\nteams by conference:")
    for conf, n in sorted(conferences.items(), key=lambda x: -x[1]):
        built = sum(1 for t in teams if t["conference"] == conf
                    and os.path.exists(os.path.join(OUT, f"{slug(t['team'])}.md")))
        flag = "" if built == n else "  ← MISMATCH"
        print(f"  {conf:<16} {built}/{n}{flag}")

    if failures:
        print(f"\nVALIDATION FAILED ({len(failures)}):")
        for f in failures[:20]:
            print("  -", f)
        sys.exit(1)
    print("\nall Phase 3 completion checks passed")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Maintenance gates added after Live Retrieval Test #1 (Georgia).
# Each corresponds to a demonstrated defect that the pre-existing validators
# did not catch, because they checked structure, links and counts but never
# whether a SELECTION was correct.
# ---------------------------------------------------------------------------

def maintenance_gates():
    import json as _json
    import re as _re
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from futures_lib import load_best_bets

    OUT_DIR = "02_Team_Database"
    teams = _json.load(open("_source/data/team_details.json"))
    canon = {t["team"] for t in teams}
    files = {t["team"]: open(os.path.join(OUT_DIR, slug(t["team"]) + ".md")).read()
             for t in teams}
    P, F = [], []

    def ck(ok, msg, detail=""):
        (P if ok else F).append(msg + (f" — {detail}" if detail and not ok else ""))

    # G1/G2 -- best-bet joins are canonical, and no bet reaches a team whose
    # name merely CONTAINS another team's name.
    bets = load_best_bets()["bets"]
    wrong, contain = [], []
    for b in bets:
        if not b["team"]:
            # a parlay resolves to no single team and must appear on none
            for t, body in files.items():
                if b["headline"] in body:
                    wrong.append(f"{b['headline'][:32]}->{t}")
            continue
        for t, body in files.items():
            if b["headline"] in body and t != b["team"]:
                wrong.append(f"{b['headline'][:32]}->{t}")
                if b["team"] in t or t in b["team"]:
                    contain.append(f"{b['team']}|{t}")
    ck(not wrong,
       f"all {len(bets)} best bets appear only on the canonical team they "
       f"resolve to; parlays appear on none", str(wrong[:3]))
    ck(not contain,
       "no best bet reaches a team by name containment", str(contain[:3]))

    # G3/G4 -- no standardized heading is empty or a bare page pointer, and
    # unsupported headings carry the sentinel.
    empty, noschema = [], []
    PTR = _re.compile(r"^Referenced in the guide on \*\*pp?\.[^*]+\*\*[^\n]*$")
    for t, body in files.items():
        nums = [int(n) for n in _re.findall(r"\n## (\d+)\. ", body)]
        if nums != list(range(1, 30)):
            noschema.append(t)
        for m in _re.finditer(r"\n## \d+\. ([^\n]+)\n(.*?)(?=\n## |\Z)", body, _re.S):
            b = m.group(2).strip()
            if not b or PTR.fullmatch(b):
                empty.append(f"{t}:{m.group(1)}")
    ck(not empty, "no standardized team heading is empty or a bare page "
                  "pointer", str(empty[:3]))
    ck(not noschema, f"all {len(files)} team files keep the 29-heading schema",
       str(noschema[:3]))
    # A file with no sentinel at all is not a defect -- it means every
    # heading is populated, which is true of 6 teams. What matters is that
    # any absence marker uses one of the two ESTABLISHED forms and has not
    # drifted into a paraphrase.
    NA = "Not addressed in guide."
    NA_HEAD = "Not addressed in guide under this heading."
    DRIFT = _re.compile(r"\bNot (?:addressed|covered|discussed|mentioned)\b"
                        r"(?! in guide\.)(?! in guide under this heading\.)",
                        _re.I)
    drifted = [f"{t}:{DRIFT.search(b).group(0)}" for t, b in files.items()
               if DRIFT.search(b)]
    withs = sum(1 for b in files.values() if NA in b or NA_HEAD in b)
    ck(not drifted,
       f"every absence marker uses an established sentinel form "
       f"({withs} of {len(files)} files carry one; the rest are fully "
       f"populated)", str(drifted[:3]))

    # G5 -- a team carrying a conflict may never assert it has none.
    both = [t for t, b in files.items()
            if "No source conflict identified for this team." in b
            and _re.search(r"\n## 27\. Source Conflicts\n\n- \*\*", b)]
    ck(not both, "no team both carries a conflict and asserts none exists",
       str(both[:3]))

    # G6 -- the schedule-rank discrepancy detector still fires where the guide
    # prints two different ranks.
    confs = _json.load(open("_source/data/conference_previews.json"))
    rank = {r["team"]: r.get("schedule_rank") for c in confs for r in c["standings"]}
    expect = set()
    for t, body in files.items():
        for m in _re.finditer(r"\b(\d{1,3})(?:st|nd|rd|th)[- ]ranked schedule\b",
                              body, _re.I):
            if rank.get(t) and str(rank[t]) != m.group(1):
                expect.add(t)
    missed = [t for t in expect
              if "Schedule rank printed two ways" not in files[t]]
    ck(not missed,
       f"every schedule-rank discrepancy ({len(expect)} found) is recorded as "
       f"a source conflict", str(missed[:3]))

    # G7 -- Bull/Bear directional sanity: no statement classified to a side
    # carries a contrastive connective.
    CONTRA = _re.compile(r"\b(but|however|though|although|despite)\b", _re.I)
    inverted = []
    for t, body in files.items():
        for head in ("## 24. Bull Case", "## 25. Bear Case"):
            m = _re.search(_re.escape(head) + r"\n(.*?)(?=\n## )", body, _re.S)
            if not m:
                continue
            for line in m.group(1).splitlines():
                if line.startswith("- ") and CONTRA.search(line):
                    inverted.append(f"{t}:{head[-9:]}")
    ck(not inverted,
       "no Bull/Bear bullet carries a contrastive connective — two-sided "
       "statements are left unclassified", str(inverted[:3]))

    # G8 -- conference prose is free of page furniture.
    FURN = _re.compile(r"steve makinen power rating|make the playoff RANK|"
                       r"CONFERENCE: NATIONAL:")
    dirty = []
    for fn in sorted(os.listdir("01_Conference_Database")):
        if not fn.endswith(".md"):
            continue
        for line in open(os.path.join("01_Conference_Database", fn)):
            if _re.match(r"- \*\*[^*]+\*\* \(p\. \d+\) — ", line) and FURN.search(line):
                dirty.append(fn)
    ck(not dirty, "no conference quoted bullet contains page furniture",
       str(sorted(set(dirty))[:3]))

    # ------------------------------------------------------ N-2 gates
    #
    # G5 above is a WITHIN-FILE invariant: it can only see a contradiction a
    # team file makes with itself. N-2 was invisible to it because the file
    # was internally consistent and wrong -- it asserted no conflict, and
    # carried none, while four other databases recorded one. These three
    # gates read the other databases independently of build_teams.py and
    # compare, so the class cannot return silently.
    from cross_conflicts import cross_database_conflicts
    xref = cross_database_conflicts()

    stray = sorted(set(xref) - canon)
    ck(not stray, "every cross-database conflict resolves to a canonical team",
       str(stray[:3]))

    # G9 -- no team asserts it has no conflict while another phase records one.
    NONE = "No source conflict identified for this team."
    false_none = sorted(t for t in xref if NONE in files.get(t, ""))
    ck(not false_none,
       f"no team asserts it has no source conflict while another database "
       f"records one ({len(xref)} teams carry a cross-database conflict)",
       str(false_none[:4]))

    # G10 -- every recorded conflict actually reaches §27, either in its own
    # words or as a verbatim duplicate of a row the Team Database already
    # renders. Absence of an assertion is not the same as presence of the
    # record, and G9 alone would pass on an empty section.
    def _key(text):
        return _re.sub(r"[^a-z0-9]+", "", text.lower())

    unsurfaced = []
    for t, recs in xref.items():
        m = _re.search(r"\n## 27\. Source Conflicts\n(.*?)(?=\n## )",
                       files.get(t, ""), _re.S)
        section = _key(m.group(1)) if m else ""
        for r in recs:
            if _key(r["detail"]) not in section:
                unsurfaced.append(f"{t}/P{r['phase']}")
    ck(not unsurfaced,
       f"all {sum(len(v) for v in xref.values())} cross-database conflict "
       f"records reach the canonical team file", str(unsurfaced[:4]))

    # G11 -- every §27 cross-link resolves, and each cites its phase. A
    # pointer to an artifact that does not exist is worse than no pointer.
    broken = []
    for t, body in files.items():
        m = _re.search(r"\n## 27\. Source Conflicts\n(.*?)(?=\n## )", body, _re.S)
        if not m:
            continue
        for target in _re.findall(r"\[source\]\(([^)]+)\)", m.group(1)):
            if not os.path.exists(os.path.normpath(
                    os.path.join(OUT_DIR, target))):
                broken.append(f"{t} -> {target}")
    ck(not broken, "every §27 cross-database source link resolves on disk",
       str(broken[:3]))

    print("\nMAINTENANCE GATES — added after Live Retrieval Test #1")
    print("=" * 66)
    for m in P:
        print(f"  PASS  {m}")
    for m in F:
        print(f"  FAIL  {m}")
    if F:
        print(f"\n{len(F)} of {len(P) + len(F)} maintenance gates failed")
        sys.exit(1)
    print(f"\nall {len(P)} maintenance gates passed")


maintenance_gates()
