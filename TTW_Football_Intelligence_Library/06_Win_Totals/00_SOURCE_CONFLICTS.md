<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_wintotals.py
     Source:   2026 VSiN College Football Betting Guide -->

# Source Conflict Audit — win totals

> **Source class: GUIDE CONTENT.** Every number and argument is printed in the 2026 VSiN College Football Betting Guide. TTW reference notes paraphrase the reasoning; the judgement is the guide's. No outside research, no post-publication updates.

> **Nothing here is corrected.** Every printed figure is reproduced as printed.

## The team page and the conference table print different numbers — 21 teams

The conference tables print the DraftKings number. The team pages carry their own. The guide acknowledges this itself on Houston's page, which says the win total *is either 7.5 or 8.5 depending on where you look*. Both are reproduced.

| Team | Conference table | Team page |
| --- | --- | --- |
| [Air Force Falcons](../02_Team_Database/air_force_falcons.md) | 6.5 | Over 7.5 |
| [Appalachian State Mountaineers](../02_Team_Database/appalachian_state_mountaineers.md) | 5.5 | Over 6.5 |
| [Baylor Bears](../02_Team_Database/baylor_bears.md) | 6.5 | Over 5.5 |
| [Buffalo Bulls](../02_Team_Database/buffalo_bulls.md) | 5.5 | Over 6.5 |
| [Georgia State Panthers](../02_Team_Database/georgia_state_panthers.md) | 4.5 | Under 3.5 |
| [Houston Cougars](../02_Team_Database/houston_cougars.md) | 8.5 | Over 7.5 |
| [Iowa State Cyclones](../02_Team_Database/iowa_state_cyclones.md) | 5.5 | Under 4.5 |
| [Maryland Terrapins](../02_Team_Database/maryland_terrapins.md) | 5.5 | Over 4.5 |
| [Miami (Ohio) RedHawks](../02_Team_Database/miami_ohio_redhawks.md) | 6.5 | Over 7.5 |
| [Michigan State Spartans](../02_Team_Database/michigan_state_spartans.md) | 4.5 | Over 3.5 |
| [Michigan Wolverines](../02_Team_Database/michigan_wolverines.md) | 7.5 | Under 8.5 |
| [Middle Tennessee Blue Raiders](../02_Team_Database/middle_tennessee_blue_raiders.md) | 3.5 | Over 4.5 |
| [Minnesota Golden Gophers](../02_Team_Database/minnesota_golden_gophers.md) | 5.5 | Under 6.5 |
| [New Mexico Lobos](../02_Team_Database/new_mexico_lobos.md) | 7.5 | Under 8.5 |
| [Penn State Nittany Lions](../02_Team_Database/penn_state_nittany_lions.md) | 8.5 | Over 9.5 |
| [Rutgers Scarlet Knights](../02_Team_Database/rutgers_scarlet_knights.md) | 5.5 | Over 4.5 |
| [San Diego State Aztecs](../02_Team_Database/san_diego_state_aztecs.md) | 6.5 | Under 7.5 |
| [TCU Horned Frogs](../02_Team_Database/tcu_horned_frogs.md) | 6.5 | Under 7.5 |
| [Texas State Bobcats](../02_Team_Database/texas_state_bobcats.md) | 5.5 | Over 6.5 |
| [UNLV Rebels](../02_Team_Database/unlv_rebels.md) | 7.5 | Under 8.5 |
| [Western Kentucky Hilltoppers](../02_Team_Database/western_kentucky_hilltoppers.md) | 6.5 | Over 7.5 |

## The team page and the feature recommend opposite sides — 11 teams

| Team | Feature (pp. 22–27) | Team page |
| --- | --- | --- |
| [Illinois Fighting Illini](illinois_fighting_illini.md) | **Over 7.5** | **Under 7.5** |
| [Kansas State Wildcats](kansas_state_wildcats.md) | **Over 7.5** | **Under 7.5** |
| [Kentucky Wildcats](kentucky_wildcats.md) | **Under 4.5** | **Over 4.5** |
| [Liberty Flames](liberty_flames.md) | **Under 8.5** | **Over 8.5** |
| [Memphis Tigers](memphis_tigers.md) | **Under 7.5** | **Over 7.5** |
| [South Alabama Jaguars](south_alabama_jaguars.md) | **Over 5.5** | **Under 5.5** |
| [South Carolina Gamecocks](south_carolina_gamecocks.md) | **Over 6.5** | **Under 6.5** |
| [Texas A&M Aggies](texas_aandm_aggies.md) | **Over 8.5** | **Under 8.5** |
| [Toledo Rockets](toledo_rockets.md) | **Under 7.5** | **Over 7.5** |
| [UCLA Bruins](ucla_bruins.md) | **Over 6.5** | **Under 6.5** |
| [UNLV Rebels](unlv_rebels.md) | **Over 7.5** | **Under 8.5** |

## A defect found in a TTW artefact, not in the guide

Phase 7 re-derived the feature list from pp. 22–27 and found that the stored Phase 2 artefact `phase2_win_totals.json` disagreed with its own generator in two rows: **Memphis** (UNDER 7.5) was missing, **South Florida** carried 7.5 instead of 8.5, and **UTSA** appeared although it is not in the feature at all. The counts still read 14 Overs and 15 Unders, which is why the original validation passed. Re-running the committed Phase 2 extractor today reproduces the correct 29, so the stored file was stale rather than the code being wrong. It has been regenerated and the American conference file rebuilt; no other phase output changed.

## Cross-links

- [Internal disagreement](00_DISAGREEMENT_INDEX.md) · [Phase 5 conflicts](../03_Coaching_Database/00_SOURCE_CONFLICTS.md)
