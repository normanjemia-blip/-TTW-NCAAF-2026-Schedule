<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_index.py
     Source:   2026 VSiN College Football Betting Guide (345 pp.) -->

# 00 — TTW Football Intelligence Library: Master Index

**Phase 1 deliverable — the navigation system for the entire library.**


| | |
| --- | --- |
| **Primary source** | 2026 VSiN College Football Betting Guide (345 pp.) |
| **Conferences** | 11 |
| **FBS teams** | 138 |
| **Head coaches** | 138 (34 in Year 1) |
| **Coordinators named** | 115 |
| **Ranked quarterbacks** | 15 |
| **Abbreviations defined** | 45 |
| **Library status** | Phase 1 complete; Phases 2–11 pending approval |


## Index files


| File | What it answers |
| --- | --- |
| [01 — Guide Structure Map](01_Guide_Structure_Map.md) | What is on any page, 1–345 |
| [02 — Conference Index](02_Conference_Index.md) | Conference membership, previews, 2026 realignment |
| [03 — Team Index](03_Team_Index.md) | All 138 teams: pages, coach, records, rating, ranks |
| [04 — Coaching Index](04_Coaching_Index.md) | Every head coach, tenure, and Year-1 arrivals |
| [05 — Coordinator Index](05_Coordinator_Index.md) | Every coordinator the guide names |
| [06 — Quarterback Index](06_Quarterback_Index.md) | Top 15 quarterbacks and where QB content lives |
| [07 — Feature Article Index](07_Feature_Article_Index.md) | Every article, author, and the Top 50 |
| [08 — Contributor Index](08_Contributor_Index.md) | Who wrote and who picked what |
| [09 — Power Rating Index](09_Power_Rating_Index.md) | All 138 Makinen ratings, ranked |
| [10 — Betting Concept Index](10_Betting_Concept_Index.md) | Where each concept appears — and which are absent |
| [11 — Metric and Abbreviation Glossary](11_Metric_Abbreviation_Glossary.md) | What every abbreviation means |
| [12 — Statistical Category Index](12_Statistical_Category_Index.md) | The 27-category team stat schema |
| [13 — Open Questions and Gaps](13_Open_Questions_And_Gaps.md) | Decisions needed from the Director |

## How to search this library

Every question in the project brief maps to a starting file:

| Question | Start here |
| --- | --- |
| *Everything about Georgia* | [03 — Team Index](03_Team_Index.md) → pp. 292–293, then Phase 3 team file |
| *Every coach entering Year 1* | [04 — Coaching Index](04_Coaching_Index.md) → Year 1 ⭐ |
| *Every quarterback competition* | [06 — Quarterback Index](06_Quarterback_Index.md) → Phase 4 |
| *Compare Makinen's rating with TTW* | [09 — Power Rating Index](09_Power_Rating_Index.md) → Phase 6 |
| *Every SEC futures recommendation* | [08 — Contributor Index](08_Contributor_Index.md) + [02](02_Conference_Index.md) → Phase 8 |
| *Every slow-tempo offense* | [12 — Statistical Category Index](12_Statistical_Category_Index.md) → `14_Statistics_Reference` |
| *Every trap game* | [01 — Guide Structure Map](01_Guide_Structure_Map.md) → `10_Schedule_Intelligence` |
| *Every portal-heavy roster* | `09_Transfer_Portal` |

Questions marked with a later phase are **not yet answerable**. The index tells you where the answer will live and what still has to be built — it does not pretend to answer them now.


## Raw source access

The full guide text is extracted and greppable, which makes ad-hoc questions answerable without reopening the PDF:

```bash
# every mention of a team, with page numbers
grep -n 'Georgia' _source/extracted/guide_full.txt

# read one page
cat _source/extracted/pages/p292.txt

# rebuild everything from the PDF
python3 _tools/extract_guide.py /path/to/guide.pdf _source
python3 _tools/build_index.py
```


## Standing rules

These govern every phase and are not restated in each file:

1. **Three source classes, never mixed** — GUIDE CONTENT, POST-PUBLICATION UPDATE, PERSONAL INFERENCE. Every claim carries one.
2. **Never invent, guess, or fill gaps.** A gap is recorded as a gap.
3. **Preserve disagreement.** When guide authors conflict, every view is kept with attribution; nothing is reconciled.
4. **Page references wherever possible.** Printed page = PDF page here.
5. **The workbook is frozen.** This library supplements TTW College Football Power Ratings v0.8.1 AUTHORITATIVE and never modifies, critiques or redesigns it.
