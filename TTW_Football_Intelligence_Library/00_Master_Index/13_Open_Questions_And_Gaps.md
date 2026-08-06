<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_index.py
     Source:   2026 VSiN College Football Betting Guide (345 pp.) -->

# 13 — Open Questions and Gaps

Items requiring a Director decision, and honest statements of what the source
does **not** contain. Nothing here is filled by guessing.

## Decisions needed before Phase 2

**1. Returning-starters field ordering.** Every team header prints three
returning-starter numbers under the labels `total / offense / defense`, but the
PDF's text layer emits labels and values in different orders, so the mapping
cannot be read reliably from text alone. Army shows `3, 8*, 11`; Northern
Illinois shows `0, 6, 6`. Resolving this needs coordinate-based extraction
(matching each value to its label by x/y position). It is **deferred to
`08_Returning_Production`**, where returning production is the subject. No
returning-starters figures appear anywhere in Phase 1 output, because a wrong
mapping would be worse than none. *Confirm you are happy for this to wait.*

**2. Futures price labelling.** Each team's right page carries three futures
prices near the labels `CFP Championship`, `make the playoff` and a conference
line. Text order does not reliably pair price to label. Same fix, same method,
**deferred to Phase 8 (Futures)**.

**3. Phase numbering does not match directory numbering.** The brief defines a
**16-directory structure** but an **11-phase workflow**, and the two number
differently — `05_Power_Ratings` is built in Phase 6, `07_Futures` in Phase 8.
More importantly, five directories are never assigned a phase at all:

| Directory | Assigned phase |
| --- | --- |
| `08_Returning_Production` | none |
| `09_Transfer_Portal` | none |
| `10_Schedule_Intelligence` | none |
| `13_Situational_Angles` | none |
| `14_Statistics_Reference` | none |

Several brief questions depend on exactly these — *"find every portal-heavy
roster"*, *"list every trap game"*, *"show every slow-tempo offense"*. This
library uses **directory names, never bare phase numbers**, to avoid ambiguity.
*Decision needed: add phases 12–16 for the unassigned directories, or fold them
into existing phases (portal and returning production into Phase 3, schedule and
situational into Phase 10, statistics into Phase 11)?* **Recommendation: fold
them in** — the underlying content lives on the team pages and would otherwise
be read twice.

**4. Depth of the Phase 3 team files.** The brief lists 24 sections per team.
Several — Recruiting Notes, Offensive Identity, Defensive Identity — are not
discrete fields in the guide; they exist only as prose that must be read and
attributed. Options: (a) keep all 24 headings and mark unsupported ones
*Not addressed in guide*, or (b) carry only headings the source actually
supports. **Recommendation: (a)** — a visible empty heading is a research
prompt, and it keeps all 138 files structurally identical. *Your call.*

## Known source limitations

**Coordinators are incomplete by nature.** 115 coordinators are
named across the guide, but there is no coordinator field in the team header.
The guide names them only where a writer found them relevant, so a complete
276-coordinator roster (OC + DC for 138 teams) **cannot** be built from this
source. Completing it requires outside research filed as POST-PUBLICATION UPDATE.

**No appendix.** The guide ends with Troy on pp. 344–345. The brief anticipated
appendices; there are none. Nothing is missing from the extraction.

**Concepts the brief expects that the guide lacks.** Closing Line Value,
Conference Strength, and Weather are effectively absent — see
[10 — Betting Concept Index](10_Betting_Concept_Index.md). Phase 9 entries for
these cannot cite the guide.

**No TTW workbook comparison yet.** The workbook (v0.8.1 AUTHORITATIVE) has not
been read into this library. Any Makinen-vs-TTW comparison is a Phase 6
deliverable requiring the workbook as contextual reference. Phase 1 makes no
comparison and no claim about TTW numbers.

## Deliberate scope limits in Phase 1

Phase 1 built the navigation layer only. The following are **indexed but not
extracted**, by design, because each belongs to a later phase:

| Content | Destination |
| --- | --- |
| Team schedules with projected lines and opponent ratings | Phase 3 → `02_Team_Database` |
| Season-outlook and Three Burning Questions prose | Phase 3 → `02_Team_Database` |
| Win-total recommendations and projected win figures | Phase 7 → `06_Win_Totals` |
| Full offensive/defensive statistics values and ranks | `14_Statistics_Reference` *(unassigned)* |
| Conference projected standings | Phase 2 → `01_Conference_Database` |
| Host best-bet picks with reasoning | Phase 8 → `07_Futures` |

## Post-publication updates outstanding

None recorded. The guide's publication date has not been established from the
source, and no outside research has been performed. Coaching changes, portal
movement, injuries and suspensions occurring after publication must be filed
under POST-PUBLICATION UPDATE and are **not** part of Phase 1.
