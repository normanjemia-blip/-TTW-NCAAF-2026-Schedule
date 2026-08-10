<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_calibration.py
     Source:   2026 VSiN College Football Betting Guide;
               TTW Power Ratings Workbook v0.8.1 AUTHORITATIVE (read-only) -->

# VSiN Inclusion — Diagnostics Without Results

> **Source class: TTW DERIVED.** Every number below is this library's arithmetic over guide figures and workbook inputs. It is not a workbook output and not VSiN's claim.

> **v0.8.1 AUTHORITATIVE remains frozen.** This phase reads it and writes nothing to it: no weights, no SETTINGS, no formulas, no VSiN column, no new version.

> **This is not predictive validation.** Nothing on this page measures whether VSiN improves prediction. It measures how the blend would move and how much independent information VSiN carries. Those are decision-relevant, and they are not evidence of forecasting skill.

## The two configurations compared

| | BASELINE | VSIN-INCLUDED |
| --- | --- | --- |
| Sources blended | SP+, FPI, TeamRankings | SP+, FPI, TeamRankings, VSiN |
| VSiN weight | — (column blank) | 0.1, the workbook's own reserved weight |
| SP+ effective weight | 0.4286 | 0.3750 |
| FPI effective weight | 0.3571 | 0.3125 |
| TeamRankings effective weight | 0.2143 | 0.1875 |
| VSiN effective weight | — | 0.1250 |
| Distribution SD | 12.533 | 12.519 |

Both configurations use the workbook's own renormalisation rule — weights spread across whatever sources are present, missing is never zero. Neither changes any stored weight.

## How far the prior would actually move

| Measure | Points |
| --- | --- |
| Mean absolute change | 0.117 |
| Median absolute change | 0.104 |
| Largest change | 0.414 |
| Teams moving 0.5 pts or more | 0 of 138 |
| Teams moving 1.0 pt or more | 0 of 138 |
| Teams whose rank does not change | 100 of 138 |
| Largest rank move | 3 places |

## How much new information VSiN carries

The question is not whether VSiN agrees with the existing sources — Phase 6 already showed it does. It is whether VSiN says anything the three live sources do not already say. Regressing the VSiN column on the other three answers that directly.

| | Value |
| --- | --- |
| R² of VSiN on SP+, FPI and TeamRankings | **0.9930** |
| Residual standard deviation | **1.040 points** |

99.3% of the variance in Makinen's ratings is already explained by the three sources the workbook blends today. What remains is about 1.04 points of standard deviation of genuinely independent opinion — real, but small against a distribution whose own SD is 12.5 points.

Whether that independent component is *skilful* or merely *different* is exactly the question no data in this project can currently answer.

### Pairwise correlations between normalised sources

| Pair | r |
| --- | --- |
| SP+~FPI | 0.9590 |
| SP+~TeamRankings | 0.9794 |
| SP+~VSiN | 0.9877 |
| FPI~TeamRankings | 0.9752 |
| FPI~VSiN | 0.9778 |
| TeamRankings~VSiN | 0.9931 |

## Weight sensitivity — diagnostic only

> **This is not predictive validation.** Nothing on this page measures whether VSiN improves prediction. It measures how the blend would move and how much independent information VSiN carries. Those are decision-relevant, and they are not evidence of forecasting skill.

These are experiments, not candidate configurations. No weight below is proposed for production, and none was selected by minimising anything.

| VSiN weight | Effective | Mean abs Δ | Max abs Δ | Teams ≥1 pt | Max rank move | Blend SD |
| --- | --- | --- | --- | --- | --- | --- |
| 0.05 | 0.0667 | 0.062 | 0.221 | 0 | 2 | 12.525 |
| 0.1 | 0.1250 | 0.117 | 0.414 | 0 | 3 | 12.519 |
| 0.15 | 0.1765 | 0.165 | 0.585 | 0 | 4 | 12.513 |
| 0.2 | 0.2222 | 0.208 | 0.737 | 0 | 5 | 12.508 |
| 0.3 | 0.3000 | 0.281 | 0.994 | 0 | 5 | 12.501 |

The relationship is close to linear and the magnitudes stay small throughout: even at triple its reserved weight, VSiN moves the average team by well under a point. That is a useful thing to know before spending effort on the decision — but it cuts both ways, since a change too small to matter is also a change too small to be worth risking.

## Teams the inclusion would move most

| Team | Conference | Baseline | VSiN-included | Δ | Rank move |
| --- | --- | --- | --- | --- | --- |
| [Northern Illinois Huskies](../02_Team_Database/northern_illinois_huskies.md) | Mountain West | -17.18 | -17.60 | **-0.414** | +0 |
| [Sacramento State Hornets](../02_Team_Database/sacramento_state_hornets.md) | MAC | -17.35 | -17.74 | **-0.394** | +0 |
| [Texas Tech Red Raiders](../02_Team_Database/texas_tech_red_raiders.md) | Big 12 | +22.35 | +22.00 | **-0.356** | +0 |
| [Minnesota Golden Gophers](../02_Team_Database/minnesota_golden_gophers.md) | Big Ten | +4.39 | +4.72 | **+0.327** | +1 |
| [Boise State Broncos](../02_Team_Database/boise_state_broncos.md) | Pac-12 | +5.99 | +6.30 | **+0.314** | +0 |
| [Oregon State Beavers](../02_Team_Database/oregon_state_beavers.md) | Pac-12 | -7.52 | -7.83 | **-0.309** | -2 |
| [Houston Cougars](../02_Team_Database/houston_cougars.md) | Big 12 | +8.53 | +8.84 | **+0.309** | +3 |
| [Tulane Green Wave](../02_Team_Database/tulane_green_wave.md) | American | -1.92 | -1.62 | **+0.304** | +3 |
| [Charlotte 49ers](../02_Team_Database/charlotte_49ers.md) | American | -23.88 | -23.58 | **+0.298** | +0 |
| [LSU Tigers](../02_Team_Database/lsu_tigers.md) | SEC | +20.75 | +20.47 | **-0.280** | +0 |
| [Texas Longhorns](../02_Team_Database/texas_longhorns.md) | SEC | +26.06 | +25.80 | **-0.257** | +0 |
| [Ohio State Buckeyes](../02_Team_Database/ohio_state_buckeyes.md) | Big Ten | +31.01 | +30.76 | **-0.251** | +0 |
| [Boston College Eagles](../02_Team_Database/boston_college_eagles.md) | ACC | -2.72 | -2.95 | **-0.221** | +0 |
| [Fresno State Bulldogs](../02_Team_Database/fresno_state_bulldogs.md) | Pac-12 | -1.24 | -1.02 | **+0.218** | +0 |
| [Buffalo Bulls](../02_Team_Database/buffalo_bulls.md) | MAC | -12.28 | -12.50 | **-0.214** | -1 |
| [Missouri Tigers](../02_Team_Database/missouri_tigers.md) | SEC | +14.21 | +14.00 | **-0.213** | +0 |
| [New Mexico Lobos](../02_Team_Database/new_mexico_lobos.md) | Mountain West | -1.70 | -1.49 | **+0.213** | +1 |
| [Florida Gators](../02_Team_Database/florida_gators.md) | SEC | +15.18 | +14.97 | **-0.210** | +0 |
| [UCLA Bruins](../02_Team_Database/ucla_bruins.md) | Big Ten | +4.33 | +4.54 | **+0.209** | +0 |
| [Auburn Tigers](../02_Team_Database/auburn_tigers.md) | SEC | +12.17 | +11.96 | **-0.208** | -1 |

## Where Makinen most disagrees with the live consensus

The regression residual is the part of Makinen's rating that the three live sources cannot explain. A large residual is where his independent opinion actually lives.

| Team | Conference | VSiN residual | Makinen | Baseline prior |
| --- | --- | --- | --- | --- |
| [Tulane Green Wave](../02_Team_Database/tulane_green_wave.md) | American | **+3.00** | 42.5 | -1.92 |
| [Northern Illinois Huskies](../02_Team_Database/northern_illinois_huskies.md) | Mountain West | **-2.90** | 21.5 | -17.18 |
| [Sacramento State Hornets](../02_Team_Database/sacramento_state_hornets.md) | MAC | **-2.74** | 21.5 | -17.35 |
| [Texas Tech Red Raiders](../02_Team_Database/texas_tech_red_raiders.md) | Big 12 | **-2.45** | 61.5 | +22.35 |
| [Boise State Broncos](../02_Team_Database/boise_state_broncos.md) | Pac-12 | **+2.39** | 50.5 | +5.99 |
| [Oregon State Beavers](../02_Team_Database/oregon_state_beavers.md) | Pac-12 | **-2.20** | 32 | -7.52 |
| [Houston Cougars](../02_Team_Database/houston_cougars.md) | Big 12 | **+2.16** | 53 | +8.53 |
| [Western Michigan Broncos](../02_Team_Database/western_michigan_broncos.md) | MAC | **+2.12** | 37.5 | -6.08 |
| [South Alabama Jaguars](../02_Team_Database/south_alabama_jaguars.md) | Sun Belt | **-2.07** | 29 | -11.55 |
| [Charlotte 49ers](../02_Team_Database/charlotte_49ers.md) | American | **+2.07** | 20.5 | -23.88 |
| [North Dakota State Bison](../02_Team_Database/north_dakota_state_bison.md) | Mountain West | **-1.98** | 37 | -3.95 |
| [Arizona Wildcats](../02_Team_Database/arizona_wildcats.md) | Big 12 | **+1.80** | 52.5 | +9.02 |
| [Florida Gators](../02_Team_Database/florida_gators.md) | SEC | **-1.74** | 55.5 | +15.18 |
| [LSU Tigers](../02_Team_Database/lsu_tigers.md) | SEC | **-1.73** | 60.5 | +20.75 |
| [Missouri Tigers](../02_Team_Database/missouri_tigers.md) | SEC | **-1.58** | 54.5 | +14.21 |
| [Oklahoma State Cowboys](../02_Team_Database/oklahoma_state_cowboys.md) | Big 12 | **-1.58** | 46.5 | +5.87 |
| [Appalachian State Mountaineers](../02_Team_Database/appalachian_state_mountaineers.md) | Sun Belt | **-1.56** | 30 | -10.81 |
| [New Mexico Lobos](../02_Team_Database/new_mexico_lobos.md) | Mountain West | **+1.55** | 42 | -1.70 |
| [Georgia Tech Yellow Jackets](../02_Team_Database/georgia_tech_yellow_jackets.md) | ACC | **+1.52** | 49 | +5.53 |
| [Toledo Rockets](../02_Team_Database/toledo_rockets.md) | MAC | **+1.52** | 35.5 | -7.63 |

## Cross-links

- [Pre-registered test protocol](01_CALIBRATION_PROTOCOL.md)
- [Phase 7 report](01_PHASE7_REPORT.md)
- [VSiN import candidate](00_VSIN_IMPORT_CANDIDATE.md)
- [Scale reconciliation](00_SCALE_RECONCILIATION.md)
