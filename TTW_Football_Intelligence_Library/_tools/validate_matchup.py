#!/usr/bin/env python3
"""
TTW Football Intelligence Library — matchup-packet validation
==============================================================

Gates the retrieval workflow, not the library. The packet is the point
where frozen preseason material meets an operator who is about to bet, so
its prohibitions have to be machine-enforced rather than merely documented:
no recommendation, no edge, no depth chart, no preseason quarterback
expectation dressed as current status, no conflict quietly resolved, no
workbook read, no write of any kind.

Every gate below corresponds to one of those prohibitions.

Usage:
    python3 _tools/validate_matchup.py
"""

import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import matchup

PAIRS = [("UNLV Rebels", "North Dakota State Bison"),
         ("Georgia Bulldogs", "Miami (Ohio) RedHawks"),
         ("Texas A&M Aggies", "Ohio State Buckeyes")]

PASS, FAIL = [], []


def ck(ok, msg, detail=""):
    (PASS if ok else FAIL).append(msg + (f" — {detail}" if detail and not ok else ""))


def library_digest():
    h = hashlib.sha256()
    for d in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p) or d.startswith((".", "_")):
            continue
        for fn in sorted(os.listdir(p)):
            if fn.endswith(".md"):
                h.update(open(os.path.join(p, fn), "rb").read())
    return h.hexdigest()


def main():
    before = library_digest()
    packets = {p: matchup.build(*p) for p in PAIRS}
    after = library_digest()

    # 1 -- generating a packet writes nothing.
    ck(before == after,
       "generating a packet changes no file in the library — retrieval is "
       "strictly read-only", f"{before[:12]} != {after[:12]}")

    # 2 -- deterministic: same input, identical bytes.
    ck(all(matchup.build(*p) == packets[p] for p in PAIRS),
       f"packet generation is deterministic across {len(PAIRS)} matchups")

    # 3 -- exact canonical resolution only. Every one of these strings is a
    #      real prefix collision the library has to refuse rather than guess.
    refused = []
    for bad in ("North Dakota", "North Dakota State", "Miami", "Ohio",
                "Georgia", "Texas", "UNLV"):
        try:
            matchup.build(bad, "UNLV Rebels")
            refused.append(bad)
        except SystemExit:
            pass
    ck(not refused,
       "every partial or ambiguous team name is refused rather than resolved "
       "by guesswork", str(refused))

    canon = {t["team"] for t in matchup.load("team_details")}
    ck(len(canon) == 138 and all(matchup.resolve(t, {c: 1 for c in canon}) == t
                                 for t in canon),
       "all 138 canonical names resolve to themselves")

    try:
        matchup.build("UNLV Rebels", "UNLV Rebels")
        same = True
    except SystemExit:
        same = False
    ck(not same, "a team cannot be matched against itself")

    # 4 -- the required notice is present, verbatim, in every packet.
    ck(all(matchup.NOTICE in b for b in packets.values()),
       "every packet opens with the static-preseason verification notice")

    # 5 -- all thirteen requested content areas are present.
    REQUIRED = [
        "Canonical identity", "preseason expectations", "Head coach and coordinators",
        "Offensive identity", "Defensive identity",
        "Returning production, strengths and weaknesses",
        "Frozen preseason quarterback outlook", "Win Total Discussion",
        "Futures / Conference / Playoff", "Bull case", "Bear case",
        "Historical and situational trends", "Source conflicts",
        "Page references and provenance",
        "Betting-relevant questions requiring current verification",
    ]
    missing = {p: [r for r in REQUIRED if r not in b]
               for p, b in packets.items()}
    missing = {p: v for p, v in missing.items() if v}
    ck(not missing, f"all {len(REQUIRED)} required content areas appear in "
                    f"every packet", str(missing)[:120])

    # 6 -- no recommendation and no edge IN THE PACKET'S OWN VOICE.
    #
    # A packet reproduces the guide, and the guide recommends things: "the
    # team page bets Under 8.5", "it plays on teams with a Stability Score
    # edge of 6 or more". Scanning the whole packet would fail on the very
    # material it exists to carry. Reproduced source text is identifiable by
    # structure -- it is page-cited -- so it is stripped by that structure
    # and its presence is REQUIRED below rather than merely tolerated. The
    # scan then runs over what is left, which is the packet's own words.
    # The packet authors exactly three regions: the header and notice, the
    # verification questions, and the next-steps list. Everything else is
    # reproduced from an approved file. Rather than guess at which lines are
    # quotation -- an earlier attempt keyed on page citations and still
    # caught a page-cited table row -- the authored regions are extracted by
    # their headings, and gate 6b below proves the rest really is quotation.
    Q_HEAD = "## Betting-relevant questions requiring current verification"
    N_HEAD = "## Required next steps"

    def packet_voice(body):
        # Everything up to the second rule: title, notice, source-class
        # statement and the head-to-head table the generator assembles from
        # Phase 3's schedule rows.
        parts = body.split("\n---\n")
        head = "\n---\n".join(parts[:2])
        rest = ""
        for h in (Q_HEAD, N_HEAD):
            i = body.find(h)
            if i != -1:
                rest += body[i:body.find("\n---\n", i) if
                             body.find("\n---\n", i) != -1 else len(body)]
        return head + "\n" + rest

    CITED = re.compile(r"\(p{1,2}\. ?\d+")
    ck(all(CITED.search(b) for b in packets.values())
       and all("Stability Score edge of 6 or more" in b
               for b in packets.values()),
       "the guide's own page-cited recommendations survive into every packet "
       "— including the Stability System rule the next gates must not scan")

    # 6b -- the reproduced region really is reproduction: every line of it
    #       appears verbatim in an approved library file. This is the gate
    #       that makes scanning only the authored region safe, and it is the
    #       packet's core promise -- it introduces no football content.
    corpus = set()
    for d in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p) or d.startswith((".", "_")):
            continue
        for fn in sorted(os.listdir(p)):
            if fn.endswith(".md"):
                corpus.update(open(os.path.join(p, fn)).read().splitlines())
    invented = []
    for pair, b in packets.items():
        authored = set(packet_voice(b).splitlines())
        for ln in b.splitlines():
            t = ln.strip()
            if len(t) < 25 or ln in authored:
                continue
            # Scaffold the generator writes around each quotation: the
            # source-attribution lines, the identity table, the packet's own
            # section headings, and the conflict restatements (whose text is
            # checked verbatim against the library by the conflict gate
            # below). None of these is football prose.
            SCAFFOLD = ("**§", "**A. VSiN", "*Quarterback file", "*Coaching file",
                        "| Team file", "| Canonical identity",
                        "| Conference (as the guide", "| Guide pages",
                        "| Head coach as printed", "| Makinen power rating",
                        "- **", "*Projected", "#", "> ")
            if (ln not in corpus and not t.startswith(SCAFFOLD)
                    and t not in (matchup.NO_CROSS_CONFLICT,
                                  matchup.NOT_ON_SCHEDULE)):
                invented.append(f"{pair[0]}: {t[:60]}")
    ck(not invented,
       "every reproduced line in a packet appears verbatim in an approved "
       "library file — the packet introduces no football content of its own",
       str(invented[:2]))

    RECOMMEND = re.compile(
        r"\b(we (?:like|recommend|project|make it)|our (?:pick|play|number|edge)|"
        r"the play is|take the|lean(?:ing)? (?:to|toward)|"
        r"(?:this is|that is) a bet|value on the|"
        r"edge of [\d.]+|fair (?:line|number) (?:is|of)|"
        r"[\d.]+ points of (?:edge|value))\b", re.I)
    hits = {p: RECOMMEND.findall(packet_voice(b))[:2] for p, b in packets.items()
            if RECOMMEND.search(packet_voice(b))}
    ck(not hits, "no packet recommends a wager or states an edge in its own "
                 "voice", str(hits)[:140])

    # 7 -- no arithmetic against a market. The packet may reproduce the
    #      guide's own printed difference; it may not compute a new one.
    COMPUTED = re.compile(r"\b(implied probability|no-vig|remove the vig|"
                          r"expected value|EV of|our (?:line|total) of|"
                          r"TTW (?:line|number|rating) of)\b", re.I)
    hits = [p for p, b in packets.items() if COMPUTED.search(b)]
    ck(not hits, "no packet computes an edge, a fair line or an implied "
                 "probability", str(hits))

    # 8 -- the frozen quarterback layer is labelled on every appearance, and
    #      the verification layer is NOT reproduced inside the packet.
    bad = [p for p, b in packets.items()
           if "NOT CURRENT STATUS" not in b
           or "A. VSiN PRESEASON QB INTELLIGENCE" not in b]
    ck(not bad, "the frozen quarterback outlook is labelled NOT CURRENT "
                "STATUS in every packet", str(bad))
    leaked = [p for p, b in packets.items()
              if "B. CURRENT VERIFIED STATE" in b]
    ck(not leaked,
       "the packet does not reproduce the current-verification layer inside "
       "the frozen material — it points at the file instead", str(leaked))

    # 9 -- no depth chart is CONSTRUCTED.
    #
    # Same distinction as gate 6, and it matters here: VSiN writes "this
    # depth chart looking more flawed" on UNLV's page (p. 258). Reproducing
    # that sentence is the packet doing its job; building a two-deep of its
    # own is the prohibition. Page-cited source lines are stripped, and the
    # packet's own instruction to go and verify the two-deep is the opposite
    # of constructing one.
    DEPTH = re.compile(r"\b(depth chart|two-deep|first team|starting (?:11|eleven)|"
                       r"QB1|RB1|WR1)\b", re.I)
    ck(any("depth chart" in b for b in packets.values()),
       "the guide's own depth-chart language is reproduced where it exists")
    hits = []
    for p, b in packets.items():
        for line in packet_voice(b).splitlines():
            if DEPTH.search(line) and "Confirm the current two-deep" not in line:
                hits.append(f"{p[0]}: {line[:50]}")
    ck(not hits, "no packet constructs a depth chart of its own", str(hits[:2]))

    # 10 -- no conflict is resolved, and every conflict a team carries in the
    #       library reaches the packet.
    RESOLVED = re.compile(r"\b(the correct (?:value|number|side|pick) is|"
                          r"we side with|resolved in favou?r of|"
                          r"should be read as|the real number is)\b", re.I)
    hits = [p for p, b in packets.items() if RESOLVED.search(b)]
    ck(not hits, "no packet resolves or adjudicates a source conflict", str(hits))

    from cross_conflicts import cross_database_conflicts
    xconf = cross_database_conflicts()
    unsurfaced = []
    for pair, b in packets.items():
        for t in pair:
            for r in xconf.get(t, []):
                if r["detail"] not in b:
                    unsurfaced.append(f"{t}/P{r['phase']}")
    ck(not unsurfaced,
       "every cross-database conflict the library records for either team "
       "reaches the packet", str(unsurfaced[:3]))

    # 11 -- the workbook is neither read nor named as a data source. The
    #       packet must name it only as a SEPARATE later step.
    src = open(os.path.join(HERE, "matchup.py")).read()
    reads_wb = re.search(r"open\([^)]*(?:xlsx|xlsm|workbook|v0\.8\.1)", src, re.I)
    ck(not reads_wb, "the generator opens no workbook file")
    bad = [p for p, b in packets.items()
           if "v0.8.1" in b and "Read the current matchup numbers from the "
                                "v0.8.1 workbook" not in b]
    ck(not bad, "the workbook appears only as a separate downstream step, "
                "never as a source of packet content", str(bad))

    # 12 -- the live/frozen separation is stated in every packet.
    ck(all("may never be written back into it" in b for b in packets.values()),
       "every packet states that current information may read but never "
       "write the frozen library")

    # 13 -- absence stays visible rather than being filled.
    ck(all(matchup.NA in b for b in packets.values()),
       "the absence marker survives into the packet — gaps are shown, not "
       "filled")

    # 14 -- every relative link in a packet resolves. Packets are written
    #       from a sibling directory, so links are checked from there.
    broken = []
    for p, b in packets.items():
        for target in re.findall(r"\]\(([^)#][^)]*)\)", b):
            if target.startswith(("http", "mailto")):
                continue
            if not os.path.exists(os.path.normpath(
                    os.path.join(ROOT, "_packets", target.split("#")[0]))):
                broken.append(f"{p[0]}->{target}")
    ck(not broken, "every relative link a packet emits resolves from the "
                   "packet directory", str(broken[:3]))

    print("MATCHUP RETRIEVAL VALIDATION")
    print("=" * 74)
    for m in PASS:
        print(f"  PASS  {m}")
    for m in FAIL:
        print(f"  FAIL  {m}")
    print()
    if FAIL:
        print(f"{len(FAIL)} of {len(PASS) + len(FAIL)} checks failed")
        sys.exit(1)
    print(f"all {len(PASS)} checks passed")


if __name__ == "__main__":
    main()
