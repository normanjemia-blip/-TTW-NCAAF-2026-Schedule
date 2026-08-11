<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_search.py
     Source:   derived from approved Phases 1–10 — pointers only -->

# 12 — Query Recipes

> **Source class: TTW DERIVED — navigation only.** This page contains **no football information**. Every fact it points at was extracted, authored, validated and approved in an earlier phase, and lives in the file linked. The search layer may point; it may not assert. It creates no score, grade, probability, ranking or betting recommendation, and it resolves no source conflict.

The questions the project brief asked, and where each is answered now that the library is built.

| Question | Start here |
| --- | --- |
| *Everything about one team* | [team lookup](../99_Search_Index/02_TEAM_LOOKUP.md) — one row, every phase |
| *Everything about a conference* | [conference lookup](../99_Search_Index/03_CONFERENCE_LOOKUP.md) |
| *Every coach entering Year 1* | [04 — Coaching Index](../00_Master_Index/04_Coaching_Index.md) |
| *Every quarterback competition* | [Quarterback Database](../04_Quarterback_Database/README.md) |
| *Compare Makinen with TTW* | [Power Ratings](../05_Power_Ratings/00_TTW_VS_MAKINEN.md) |
| *Every win total VSiN bets* | [29 feature picks](../06_Win_Totals/00_FEATURE_PICKS.md) |
| *Every SEC futures recommendation* | [best bets](../07_Futures/00_BEST_BETS.md) + [conference](../99_Search_Index/03_CONFERENCE_LOOKUP.md) |
| *One contributor's whole position* | [contributor lookup](../99_Search_Index/06_CONTRIBUTOR_LOOKUP.md) |
| *Every slow-tempo offense* | [offensive statistics](../14_Statistics_Reference/00_OFFENSE.md) — plays per game |
| *Every trap game* | [Situational Angles](../13_Situational_Angles/README.md) — argued case by case, **no printed hit rate** |
| *Every portal-heavy roster* | [Transfer Portal](../09_Transfer_Portal/README.md) — 91 of 138 teams |
| *Teams meeting a stability threshold* | [Returning Production](../08_Returning_Production/README.md) |
| *Does this angle have a track record?* | [angle lookup](../99_Search_Index/08_HISTORICAL_ANGLE_LOOKUP.md) — **guide records, not TTW backtests** |
| *What does the guide mean by X?* | [Betting Concepts](../11_Betting_Concepts/README.md) |
| *Where does the guide contradict itself?* | [conflict roll-up](../99_Search_Index/09_SOURCE_CONFLICT_ROLLUP.md) |
| *What is missing, and why* | [gap register](../99_Search_Index/10_GAP_REGISTER.md) |

## Searching the raw guide

The full text is extracted and greppable when a question is not yet indexed:

```bash
grep -n 'Georgia' _source/extracted/guide_full.txt   # with page numbers
cat _source/extracted/pages/p292.txt                 # one page
```

## Cross-links

- [Search Index](README.md) · [00 — Master Index](../00_Master_Index/00_MASTER_INDEX.md)
