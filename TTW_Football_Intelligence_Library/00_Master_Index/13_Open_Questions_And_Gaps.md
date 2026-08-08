<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_index.py
     Source:   2026 VSiN College Football Betting Guide (345 pp.) -->

# 13 — Open Questions and Gaps

Items requiring a Director decision, and honest statements of what the source
does **not** contain. Nothing here is filled by guessing.

## Owner decisions on record

All Phase 1 open questions were resolved by the Director on 2026-08-08. They are
retained here with their resolutions so the reasoning stays visible.

**1. Returning-starters field ordering.** ✅ **DEFERRED, APPROVED 2026-08-08.** Every team header prints three
returning-starter numbers under the labels `total / offense / defense`, but the
PDF's text layer emits labels and values in different orders, so the mapping
cannot be read reliably from text alone. Army shows `3, 8*, 11`; Northern
Illinois shows `0, 6, 6`. Resolving this needs coordinate-based extraction
(matching each value to its label by x/y position). It is **deferred to
`08_Returning_Production`**, where returning production is the subject. No
returning-starters figures appear anywhere in Phase 1 output, because a wrong
mapping would be worse than none. The Director has approved deferral, with the standing instruction: do not guess
these values, do not infer them from malformed text extraction, and do not
fabricate missing figures.

**2. Futures price labelling.** ✅ **DEFERRED, APPROVED 2026-08-08.** Each team's right page carries three futures
prices near the labels `CFP Championship`, `make the playoff` and a conference
line. Text order does not reliably pair price to label. Same fix, same method,
**deferred to Phase 8 (Futures)**.

**3. Phase numbering does not match directory numbering.** ✅ **DECIDED
2026-08-08 — no Phases 12–16.** The five unassigned directories fold into the
approved phase structure as follows:

| Directory | Folded into |
| --- | --- |
| `08_Returning_Production` | **Phase 3** (Team Database), with conference-level summaries in **Phase 2** where relevant |
| `09_Transfer_Portal` | **Phase 3** (Team Database), with conference-level summaries in **Phase 2** where relevant |
| `10_Schedule_Intelligence` | **Phase 2** (Conference Database) and **Phase 3** (Team Database) |
| `13_Situational_Angles` | **Phase 9** (Betting Concepts) if conceptual, **Phase 10** (Historical Trends) if historical or system-based |
| `14_Statistics_Reference` | **Phase 9** (Betting Concepts) / reference material, preserving every guide-specific statistic and definition |

Note that phase numbers and directory numbers still differ by design
(`05_Power_Ratings` is Phase 6, `07_Futures` is Phase 8). This library therefore
uses **directory names, never bare phase numbers**, wherever ambiguity is
possible.

**4. Depth of the Phase 3 team files.** ✅ **DECIDED 2026-08-08 — option (a).**
Every FBS team file carries the **full standardised 24-heading schema**. Where
the guide does not address a heading, the file states exactly:

> Not addressed in guide.

Headings are never omitted merely because the source is silent, so all 138 team
files share one searchable structure.

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

None recorded, and **none authorised**. The Director's standing instruction as of
2026-08-08 is that outside updating has not begun and requires explicit
authorisation. The guide's publication date has not been established from the
source, so the cut-off for "post-publication" remains undefined. Coaching changes, portal
movement, injuries and suspensions occurring after publication must be filed
under POST-PUBLICATION UPDATE and are **not** part of Phase 1.
