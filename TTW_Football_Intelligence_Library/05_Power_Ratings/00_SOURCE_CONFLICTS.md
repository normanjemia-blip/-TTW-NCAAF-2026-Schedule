<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_power.py
     Source:   2026 VSiN College Football Betting Guide;
               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->

# Source Conflict Audit — power ratings

> **Source class: GUIDE CONTENT.** Every figure is printed in the 2026 VSiN College Football Betting Guide. No outside research and no post-publication updates.

> **Nothing here is corrected.** Where the guide prints the same rating two ways, both are reproduced.

## Method

Every rating is printed twice: in Makinen's master table on p. 47 and on the team's own right-hand page. The two lists were extracted independently — the master table by parsing p. 47, the team pages by the Phase 3 extraction — and compared row by row.

## Result

**All 138 ratings agree between the two printings.** No conflict found.

This is worth recording as a positive result rather than silence: it means the Phase 3 team-page extraction reproduced the master table exactly across 138 independent values, and the ratings used throughout this phase are corroborated twice within the guide itself.

## Projected-line anomaly

The line-model verification reconstructs 1528 of 1530 printed game lines from the printed ratings and field ratings. One fixture does not reconstruct under either neutral-site form:

| Team page | Opponent | Printed line | Model |
| --- | --- | --- | --- |
| [Cincinnati Bearcats](../02_Team_Database/cincinnati_bearcats.md) | Miami (Ohio) RedHawks | -8.8 | +8.5 |
| [Miami (Ohio) RedHawks](../02_Team_Database/miami_ohio_redhawks.md) | Cincinnati Bearcats | +8.8 | -8.5 |

The two rows are the same fixture seen from both team pages and they agree with each other, so the guide is internally consistent about the line — it simply does not follow from the ratings it prints, by 0.3 points. Neither the line nor the ratings are adjusted here.

## Conflicts carried in from earlier phases

Phase 5 recorded 16 coaching conflicts and Phase 2 recorded several structural ones. None bears on the power ratings, and none is restated here. They remain in their own phase files, preserved and unresolved.

## Cross-links

- [Ratings in full](00_MAKINEN_RATINGS.md) · [Phase 5 conflicts](../03_Coaching_Database/00_SOURCE_CONFLICTS.md)
