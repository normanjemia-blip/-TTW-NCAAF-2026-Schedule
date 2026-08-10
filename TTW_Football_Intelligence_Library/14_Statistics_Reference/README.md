<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_concepts.py
     Source:   2026 VSiN College Football Betting Guide -->

# 14 Statistics Reference

> **Source class: GUIDE CONTENT.** Every category, value, rank and abbreviation below is printed in the 2026 VSiN College Football Betting Guide. No outside research, no post-publication updates.

The guide's team statistics: **15 offensive** and **12 defensive** categories, each with a value and a national rank out of 138, for **136** of the **138** teams — **3,672** printed figures. The two teams promoted from FCS carry the headings and an explicit notice instead of values; see below.

> **Status corrected.** This directory long carried a note saying the values could not yet be extracted. Phase 3 resolved them; the schema and the values are both verified, and that stale status is withdrawn.

## The schema

| # | Offensive category | Defensive category |
| --- | --- | --- |
| 1 | POINTS PER GAME | POINTS PER GAME |
| 2 | YARDS PER POINT | YARDS PER POINT |
| 3 | PLAYS PER GAME | 3RD DOWN CONV. % |
| 4 | TIME OF POSSESSION | TOTAL YARDS PER GAME |
| 5 | 3RD DOWN CONV. % | YARDS PER PLAY |
| 6 | TOTAL YARDS PER GAME | RUSH YARDS PER GAME |
| 7 | YARDS PER PLAY | YARDS PER RUSH ATTEMPT |
| 8 | RUSH ATTEMPTS PER GAME | COMPLETION % |
| 9 | RUSH YARDS PER GAME | PASSING YARDS PER GAME |
| 10 | YARDS PER RUSH ATTEMPT | YARDS PER PASS ATTEMPT |
| 11 | PASS ATTEMPTS PER GAME | SACKS |
| 12 | COMPLETION % | TURNOVERS |
| 13 | PASSING YARDS PER GAME | — |
| 14 | YARDS PER PASS ATTEMPT | — |
| 15 | TURNOVERS | — |

## The asymmetry between the two tables

The defensive table omits three categories the offensive table carries — **plays per game**, **time of possession** and **rush/pass attempts per game** — and adds **sacks**. This is a property of the source, not an extraction gap: possession and tempo figures are team-level and would simply be duplicated on the defensive side.

**Practical consequence: defensive tempo cannot be read directly from this guide.** Any tempo work has to use the offensive plays-per-game and time-of-possession figures.

## Categories the guide defines

| Category | p. 2 abbreviation | As printed |
| --- | --- | --- |
| POINTS PER GAME | `PPG` | Points Per Game |
| YARDS PER PLAY | `YPP` | Yards per Play |
| YARDS PER POINT | `YPPT` | Yards per Point |
| TOTAL YARDS PER GAME | `TYPG` | Total Yards per Game |
| PASSING YARDS PER GAME | `PYPG` | Passing Yards per Page |
| RUSH YARDS PER GAME | `RYPG` | Rushing Yards per Game |
| YARDS PER RUSH ATTEMPT | `YPR` | Yards per Rush |
| TURNOVERS | `TO` | Turnovers |

The remaining categories are printed as column headings and never glossed.

## Two teams with no statistics, and the guide says why

**North Dakota State Bison and Sacramento State Hornets** carry the table headings with no values. In place of both tables the guide prints **`PARTICIPATED IN FCS IN 2025`** — twice, once for each side of the ball. Both programmes moved up for 2026, so there are no FBS figures to print.

This is an explicit, reasoned absence in the source, not an extraction gap. It is recorded as printed and never filled from FCS statistics or from anywhere else. The printed total is therefore **3,672** figures across 136 teams, not 3,726.

## A note on yards per point

Yards gained divided by points scored — how much field a team has to cover to produce a point. A **low** number is good on offense, because it means the team converts yardage into points efficiently.

The direction is the opposite of most rate statistics — lower is better on offense, higher is better on defense. The guide prints ranks, which resolve this, but the raw values invert.

## Files

| File | Content |
| --- | --- |
| [00_OFFENSE.md](00_OFFENSE.md) | all 138 teams × 15 offensive categories |
| [00_DEFENSE.md](00_DEFENSE.md) | all 138 teams × 12 defensive categories |
| [00_LEADERS.md](00_LEADERS.md) | who the guide ranks first in each category |

## Cross-links

- [12 — Statistical Category Index](../00_Master_Index/12_Statistical_Category_Index.md) · [11 — Betting Concepts](../11_Betting_Concepts/README.md) · team files in [`02_Team_Database`](../02_Team_Database/README.md)
