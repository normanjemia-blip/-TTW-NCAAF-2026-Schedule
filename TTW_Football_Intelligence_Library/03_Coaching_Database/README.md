<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_coaching_indexes.py
     Source:   2026 VSiN College Football Betting Guide -->

# Coaching Intelligence Database

> **Source: 2026 VSiN College Football Betting Guide.** GUIDE CONTENT throughout — no outside research and no post-publication updates. Continuity readings come from Steve Makinen's printed Stability Score table (pp. 41–44), reproduced exactly; this library does not recompute or re-weight it.

One standardised coaching record for each of the 138 FBS programmes, plus the indexes built on top of them. Everything is the guide's position at publication: no outside research, no post-publication updates, and no change to the frozen TTW Power Ratings Workbook v0.8.1.

## Files

| File | What it holds |
| --- | --- |
| [00_COACH_DIRECTORY.md](00_COACH_DIRECTORY.md) | Head coaches and every coordinator the guide names, searchable |
| [00_CONTINUITY_MATRIX.md](00_CONTINUITY_MATRIX.md) | All 138 programmes with the printed Stability Score components |
| [00_NEW_HEAD_COACHES.md](00_NEW_HEAD_COACHES.md) | 33 programmes |
| [00_NEW_OFFENSIVE_COORDINATORS.md](00_NEW_OFFENSIVE_COORDINATORS.md) | 68 programmes |
| [00_NEW_DEFENSIVE_COORDINATORS.md](00_NEW_DEFENSIVE_COORDINATORS.md) | 63 programmes |
| [00_NEW_PLAY_CALLERS.md](00_NEW_PLAY_CALLERS.md) | 15 programmes |
| [00_MAJOR_SCHEME_CHANGES.md](00_MAJOR_SCHEME_CHANGES.md) | 49 programmes |
| [00_HIGH_CONTINUITY_STAFFS.md](00_HIGH_CONTINUITY_STAFFS.md) | 25 programmes scoring 14+ |
| [00_LOW_CONTINUITY_STAFFS.md](00_LOW_CONTINUITY_STAFFS.md) | 36 programmes scoring 6 or fewer |
| [00_QB_COACHING_CROSSLINK.md](00_QB_COACHING_CROSSLINK.md) | Quarterback situation against staff situation |
| [00_SOURCE_CONFLICTS.md](00_SOURCE_CONFLICTS.md) | 16 preserved contradictions |
| *team files* | 138 records, 29 fields each |

## The 29 fields

Fields 1–5, 26, 27 and 29 are machine-derived from tables this library already extracted and validated. Fields 6–25 and 28 are authored from the team pages, the Coaching Carousel and the conference previews, and stored in `_source/coaching/*.json`.

Two rules are enforced by construction rather than by care:

- Scheme and tendency fields say `Not addressed in guide.` unless the guide states them. A coach's reputation is not evidence.
- Source conflicts are rendered as their own labelled block, never resolved into a single value.

## Rebuild

```bash
python3 _tools/build_coaching.py           # the 138 records
python3 _tools/build_coaching_indexes.py   # the indexes
python3 _tools/validate_coaching.py        # 10 checks
```

## Cross-links

- [Team Database](../02_Team_Database/README.md)
- [Quarterback Database](../04_Quarterback_Database/README.md)
- [Conference Database](../01_Conference_Database/)
