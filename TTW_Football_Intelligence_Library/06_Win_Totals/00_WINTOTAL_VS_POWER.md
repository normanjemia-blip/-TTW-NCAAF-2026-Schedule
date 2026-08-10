<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_wintotals.py
     Source:   2026 VSiN College Football Betting Guide -->

# Win Total × Power Rating — consistency check

> **Source class: TTW DERIVED — CONSISTENCY CHECK.** This compares two things the guide prints. It does **not** claim that a power rating determines a win total: schedule and the distribution of opponents matter, which is why Makinen runs his ratings against each schedule rather than reading wins off the rating. The purpose is to surface interesting inconsistencies, not to declare errors.

Across all 138 teams the posted win total and Makinen's power rating correlate at **0.7592**. A least-squares line through them gives an expected total for each rating; the residual below is the posted total minus that expectation. A positive residual means the market total is higher than the rating alone would suggest — most often because the schedule is soft.

## Largest positive residuals — total high for the rating

| Team | Conf | Total | PR | SoS rank | Residual | Feature pick |
| --- | --- | --- | --- | --- | --- | --- |
| [Liberty Flames](../02_Team_Database/liberty_flames.md) | Conference USA | 8.5 | 34.5 | #133 | **+3.06** | Under 8.5 |
| [North Dakota State Bison](../02_Team_Database/north_dakota_state_bison.md) | Mountain West | 8.5 | 37 | #130 | **+2.78** | — |
| [South Florida Bulls](../02_Team_Database/south_florida_bulls.md) | American | 8.5 | 41 | #112 | **+2.33** | Under 8.5 |
| [Louisiana Ragin’ Cajuns](../02_Team_Database/louisiana_ragin_cajuns.md) | Sun Belt | 7.5 | 32.5 | #128 | **+2.28** | — |
| [James Madison Dukes](../02_Team_Database/james_madison_dukes.md) | Sun Belt | 8.5 | 41.5 | #129 | **+2.27** | — |
| [Notre Dame Fighting Irish](../02_Team_Database/notre_dame_fighting_irish.md) | Independents | 11.5 | 68.5 | #59 | **+2.25** | — |
| [Jacksonville State Gamecocks](../02_Team_Database/jacksonville_state_gamecocks.md) | Conference USA | 7.5 | 34 | #134 | **+2.11** | — |
| [Marshall Thundering Herd](../02_Team_Database/marshall_thundering_herd.md) | Sun Belt | 7.5 | 34 | #124 | **+2.11** | — |
| [Texas Tech Red Raiders](../02_Team_Database/texas_tech_red_raiders.md) | Big 12 | 10.5 | 61.5 | #69 | **+2.04** | — |
| [Toledo Rockets](../02_Team_Database/toledo_rockets.md) | MAC | 7.5 | 35.5 | #132 | **+1.94** | Under 7.5 |
| [Miami Hurricanes](../02_Team_Database/miami_hurricanes.md) | ACC | 10.5 | 63 | #61 | **+1.87** | — |
| [Old Dominion Monarchs](../02_Team_Database/old_dominion_monarchs.md) | Sun Belt | 7.5 | 37 | #122 | **+1.78** | — |
| [FIU Golden Panthers](../02_Team_Database/fiu_golden_panthers.md) | Conference USA | 6.5 | 28.5 | #131 | **+1.73** | — |
| [Western Michigan Broncos](../02_Team_Database/western_michigan_broncos.md) | MAC | 7.5 | 37.5 | #99 | **+1.72** | — |
| [Hawaii Rainbow Warriors](../02_Team_Database/hawaii_rainbow_warriors.md) | Mountain West | 7.5 | 38.5 | #108 | **+1.61** | — |

## Largest negative residuals — total low for the rating

| Team | Conf | Total | PR | SoS rank | Residual | Feature pick |
| --- | --- | --- | --- | --- | --- | --- |
| [Stanford Cardinal](../02_Team_Database/stanford_cardinal.md) | ACC | 3.5 | 39 | #15 | **-2.45** | — |
| [Purdue Boilermakers](../02_Team_Database/purdue_boilermakers.md) | Big Ten | 3.5 | 39 | #9 | **-2.45** | — |
| [Mississippi State Bulldogs](../02_Team_Database/mississippi_state_bulldogs.md) | SEC | 4.5 | 47 | #4 | **-2.34** | — |
| [Kentucky Wildcats](../02_Team_Database/kentucky_wildcats.md) | SEC | 4.5 | 47 | #3 | **-2.34** | Under 4.5 |
| [Boston College Eagles](../02_Team_Database/boston_college_eagles.md) | ACC | 3.5 | 37.5 | #19 | **-2.28** | — |
| [Arkansas Razorbacks](../02_Team_Database/arkansas_razorbacks.md) | SEC | 4.5 | 45.5 | #5 | **-2.17** | — |
| [North Carolina Tar Heels](../02_Team_Database/north_carolina_tar_heels.md) | ACC | 4.5 | 44.5 | #24 | **-2.06** | — |
| [Colorado Buffaloes](../02_Team_Database/colorado_buffaloes.md) | Big 12 | 4.5 | 43 | #33 | **-1.89** | — |
| [Vanderbilt Commodores](../02_Team_Database/vanderbilt_commodores.md) | SEC | 5.5 | 51.5 | #18 | **-1.85** | — |
| [Michigan State Spartans](../02_Team_Database/michigan_state_spartans.md) | Big Ten | 4.5 | 42.5 | #8 | **-1.84** | — |
| [Syracuse Orange](../02_Team_Database/syracuse_orange.md) | ACC | 4.5 | 42 | #32 | **-1.78** | Over 4.5 |
| [Colorado State Rams](../02_Team_Database/colorado_state_rams.md) | Pac-12 | 3.5 | 32.5 | #71 | **-1.72** | — |
| [Oregon State Beavers](../02_Team_Database/oregon_state_beavers.md) | Pac-12 | 3.5 | 32 | #70 | **-1.66** | — |
| [Minnesota Golden Gophers](../02_Team_Database/minnesota_golden_gophers.md) | Big Ten | 5.5 | 49 | #42 | **-1.57** | — |
| [Charlotte 49ers](../02_Team_Database/charlotte_49ers.md) | American | 2.5 | 20.5 | #77 | **-1.38** | — |

## Reading these

A large residual is a place where the market's number and Makinen's rating sit further apart than usual. That is often a schedule effect and sometimes a disagreement. It is never, on its own, an error — and this page does not treat it as one.

## Cross-links

- [Power Ratings](../05_Power_Ratings/00_MAKINEN_RATINGS.md) · [all teams](00_ALL_TEAMS.md)
