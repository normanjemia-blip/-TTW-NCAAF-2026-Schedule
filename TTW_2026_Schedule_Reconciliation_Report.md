# TTW 2026 NCAAF Schedule - Reconciliation Report

**Report generated:** 2026-07-19T05:08:23Z

## 1. ESPN Retrieval Method

- **Primary source:** ESPN's public structured JSON APIs (no HTML parsing).
- **Game data endpoint:** `https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard`
  - Queried per season-week using `dates=YYYYMMDD-YYYYMMDD` (ESPN's own week start/end boundaries), `groups=80` (ESPN's structured FBS grouping - includes any game with at least one FBS-tree team, which covers FBS-vs-FBS, FBS-vs-FCS, and both 2026 reclassifiers), and `limit=300`.
  - **Retrieval-method finding:** the `week=` query parameter and any `limit` value above ~500 both silently truncate results to 25 events regardless of the true weekly game count. This was discovered during manual verification (week 1 truncated from a true count of 99 down to 25) and cross-validated against `sports.core.api.espn.com`'s authoritative per-week event counts. The `dates=` range + `limit=300` combination was verified to return complete, untruncated results for every week and was used for the full build.
- **Reference/metadata endpoints:** `https://sports.core.api.espn.com/v2/sports/football/leagues/college-football/...`
  - `seasons/2026/types/{1,2,3}` and `.../weeks` - season type and week enumeration/date boundaries.
  - `seasons/2026/types/2/groups/{80,81}` and `.../children` - FBS and FCS conference (group) ID -> name mapping.
  - `seasons/2026/types/2/groups/80/teams` - definitive FBS team roster, used to verify per-team schedule counts and identify non-competing entities ESPN also tags under the FBS group.
- **Network reachability test:** confirmed before the full build (HTTP 200 from all three endpoint families).
- All raw HTTP responses are saved untouched under `raw_espn/`. Every request (including reference/metadata requests) is logged to `retrieval_log.csv`.

- **Retrieval date/time (UTC):** 2026-07-19T02:49:43Z to 2026-07-19T02:56:50Z (see `retrieved_at` column in `retrieval_log.csv` for the exact timestamp of every request).
- **Total HTTP requests logged:** 80 (80 succeeded on first attempt, 0 total retries across all requests).

## 2. Weeks Requested / Retrieved

| Season type | Weeks requested | Weeks successfully retrieved |
|---|---|---|
| Preseason (type 1) | Week 1 (full range 2026-02-01 to 2026-08-22) | 1 of 1 |
| Regular Season (type 2) | Weeks 1-15 | 15 of 15 |
| Postseason (type 3) | Week 1 ("Bowls", full range 2026-12-13 to 2027-01-28) | 1 of 1 |

No gaps in the weekly retrieval sequence. All 17 week-requests returned HTTP 200 with no retries needed.

- **First scheduled date in final file:** 2026-08-29
- **Final scheduled date in final file:** 2026-12-12

## 3. Event Counts

- **Raw event count (all events returned by ESPN across all week-requests, before filtering):** 946
- **Retained game count (rows in final CSV):** 888
- **Excluded game count:** 58

### Exclusion reasons

| Category | Count | Reason |
|---|---|---|
| Bowl / CFP placeholder games | 44 | Postseason (type 3) games where both participants are still ESPN placeholder entities (team id -1/-2, display name "TBD"). Per project instructions, bowl/playoff placeholders are excluded until participants are known. None of the 2026 bowl or CFP games have participants determined yet. |
| Regular-season TBD-opponent games | 4 | Four Week 13 (2026-11-28) games where a real home team (Colorado State, Fresno State, Utah State, Washington State - all Pac-12) is scheduled but the opponent is still an ESPN placeholder ("TBD"). Excluded under the same no-fabrication / no-unknown-participant principle applied to bowls. Flagged in Section 13 for manual review once ESPN publishes the opponent. |
| Official conference-championship event shells | 10 | The 10 officially scheduled 2026 conference championship games. Date, venue, and conference are real ESPN data; both participating teams are still ESPN placeholder entities ("TBD"). Per the phase-3 amendment, placeholder-participant rows are never loaded into the CSV, with no exception for championship games - see Section 5 for the full list, documented outside the loadable file as `OFFICIAL EVENT SHELL — PARTICIPANTS UNKNOWN — NOT YET LOADABLE`. |
| **Total excluded** | **58** | |

- **FBS-vs-FBS count:** 761
- **FBS-vs-FCS count:** 127
- **Conference championship count (loadable, in the CSV):** 0 - by design. All 10 official 2026 conference championship event shells are documented in Section 5 instead, since neither participant is known yet.
- **Games involving reclassifying teams (North Dakota State + Sacramento State, de-duplicated for their head-to-head matchup):** 23
- **Neutral-site count:** 11
- **Week 0 count:** 8 (project-normalized; see Section 4 - Week 0 Normalization Methodology)

## 4. Week 0 Normalization Methodology

Per the phase-3 amendment: the 2026 season's opening slate is normalized to project **Week 0**, even though ESPN's own structured source labels those events as regular-season week 1. ESPN's raw event id, date, home/away orientation, and neutral-site status are never altered - only the `week` column is normalized, and ESPN's original `season_type`/`week` value is preserved verbatim in each row's `notes` field.

- **Cutoff rule:** any retained game dated earlier than **2026-09-03** is normalized to `week=0`. ESPN's data has games on 2026-08-29 and 2026-08-30, then nothing until 2026-09-03 (Thursday) - so this rule resolves cleanly to exactly the 2026-08-29/2026-08-30 opening weekend, with no ambiguous dates in between.
- **Week 0 row count:** 8
- **First normalized Week 1 date:** 2026-09-03 (confirmed below)

### Named opening-weekend examples (explicitly verified)

| Matchup | Date | Normalized week |
|---|---|---|
| North Carolina Tar Heels at TCU Horned Frogs | 2026-08-29 | 0 |
| Hawai'i Rainbow Warriors at Stanford Cardinal | 2026-08-29 | 0 |
| NC State Wolfpack at Virginia Cavaliers | 2026-08-29 | 0 |
| San José State Spartans at USC Trojans | 2026-08-29 | 0 |
| New Mexico State Aggies at Florida State Seminoles | 2026-08-29 | 0 |
| Jacksonville State Gamecocks at North Dakota State Bison | 2026-08-29 | 0 |
| Sacramento State Hornets at Eastern Michigan Eagles | 2026-08-29 | 0 |
| Memphis Tigers at UNLV Rebels | 2026-08-30 | 0 |

All 8 games named in the amendment request (North Carolina at TCU, NC State at Virginia, Jacksonville State at North Dakota State, Sacramento State at Eastern Michigan, Hawai'i at Stanford, Memphis at UNLV, San José State at USC, New Mexico State at Florida State) are present above and resolve to `week=0` - the amendment's own example list turned out to be the complete, exact set of ESPN's 2026-08-29/2026-08-30 games with no additions or omissions needed.

- **Confirmed:** the earliest normalized-Week-1 date is 2026-09-03 (Thursday) - see `validate_schedule.py` check 20c.

## 5. Official Conference-Championship Event Shells (Documented, Not Loaded)

All 10 of the 2026 conference championship games are officially scheduled by their conference (real date, and a real venue where the site is already fixed) but neither participating team is known yet - both are still ESPN placeholder entities. Per the phase-3 amendment, these are **excluded from the loadable CSV outright, with no championship exception**, and are classified as:

> `OFFICIAL EVENT SHELL — PARTICIPANTS UNKNOWN — NOT YET LOADABLE`

| ESPN event id | Conference | Date | Venue | Neutral site |
|---|---|---|---|---|
| 401858318 | Atlantic Coast Conference | 2026-12-05 | Bank of America Stadium | True |
| 401869532 | American Conference | 2026-12-06 | (not yet announced) | False |
| 401869533 | Big 12 Conference | 2026-12-05 | AT&T Stadium | True |
| 401869534 | Big Ten Conference | 2026-12-06 | Lucas Oil Stadium | True |
| 401869535 | Conference USA | 2026-12-04 | (not yet announced) | False |
| 401869536 | Mid-American Conference | 2026-12-05 | Ford Field | True |
| 401874049 | Mountain West Conference | 2026-12-05 | (not yet announced) | False |
| 401869542 | Pac-12 Conference | 2026-12-05 | (not yet announced) | False |
| 401869545 | Southeastern Conference | 2026-12-05 | Mercedes-Benz Stadium | True |
| 401869546 | Sun Belt Conference | 2026-12-05 | (not yet announced) | False |

These will be re-pulled and loaded once ESPN publishes both participants (see Section 13).

## 6. Data-Quality Counts

- **Duplicate GameID count:** 0
- **Blank GameID count:** 0
- **Missing-date count:** 0
- **Retained placeholder-team count:** 0 (hard-enforced by both the build script and `validate_schedule.py` check 19 - no exception for championship-labeled rows).
- **Unresolved-team count (placeholder team OR unresolved conference):** 0
- **Conference-mismatch count (ESPN-reported vs. approved assignment, reclassifiers only):** 0 - ESPN's own `conferenceId` for both North Dakota State and Sacramento State already resolves to the approved 2026 assignment (see Section 10).

## 7. Schedule Count for Every Retained FBS Team

ESPN's structured FBS group-80 roster lists 148 entries for 2026. Of those, 10 are non-competing exhibition/all-star placeholder entities with zero 2026 games (e.g. "East All-Stars", "Team Gaither" - roster ids ['125290', '125291', '3144', '3145', '3146', '3147', '3193', '3194', '3197', '3198']), leaving **138 genuine FBS programs**, each listed below with its conference and total 2026 game count (home + away) in the final file.

| Conference | Team | Games |
|---|---|---|
| American Conference | Army Black Knights | 12 |
| American Conference | Charlotte 49ers | 12 |
| American Conference | East Carolina Pirates | 12 |
| American Conference | Florida Atlantic Owls | 12 |
| American Conference | Memphis Tigers | 12 |
| American Conference | Navy Midshipmen | 12 |
| American Conference | North Texas Mean Green | 12 |
| American Conference | Rice Owls | 12 |
| American Conference | South Florida Bulls | 12 |
| American Conference | Temple Owls | 12 |
| American Conference | Tulane Green Wave | 12 |
| American Conference | Tulsa Golden Hurricane | 12 |
| American Conference | UAB Blazers | 12 |
| American Conference | UTSA Roadrunners | 12 |
| Atlantic Coast Conference | Boston College Eagles | 12 |
| Atlantic Coast Conference | California Golden Bears | 12 |
| Atlantic Coast Conference | Clemson Tigers | 12 |
| Atlantic Coast Conference | Duke Blue Devils | 12 |
| Atlantic Coast Conference | Florida State Seminoles | 12 |
| Atlantic Coast Conference | Georgia Tech Yellow Jackets | 12 |
| Atlantic Coast Conference | Louisville Cardinals | 12 |
| Atlantic Coast Conference | Miami Hurricanes | 12 |
| Atlantic Coast Conference | NC State Wolfpack | 12 |
| Atlantic Coast Conference | North Carolina Tar Heels | 12 |
| Atlantic Coast Conference | Pittsburgh Panthers | 12 |
| Atlantic Coast Conference | SMU Mustangs | 12 |
| Atlantic Coast Conference | Stanford Cardinal | 12 |
| Atlantic Coast Conference | Syracuse Orange | 12 |
| Atlantic Coast Conference | Virginia Cavaliers | 12 |
| Atlantic Coast Conference | Virginia Tech Hokies | 12 |
| Atlantic Coast Conference | Wake Forest Demon Deacons | 12 |
| Big 12 Conference | Arizona State Sun Devils | 12 |
| Big 12 Conference | Arizona Wildcats | 12 |
| Big 12 Conference | BYU Cougars | 12 |
| Big 12 Conference | Baylor Bears | 12 |
| Big 12 Conference | Cincinnati Bearcats | 12 |
| Big 12 Conference | Colorado Buffaloes | 12 |
| Big 12 Conference | Houston Cougars | 12 |
| Big 12 Conference | Iowa State Cyclones | 12 |
| Big 12 Conference | Kansas Jayhawks | 12 |
| Big 12 Conference | Kansas State Wildcats | 12 |
| Big 12 Conference | Oklahoma State Cowboys | 12 |
| Big 12 Conference | TCU Horned Frogs | 12 |
| Big 12 Conference | Texas Tech Red Raiders | 12 |
| Big 12 Conference | UCF Knights | 12 |
| Big 12 Conference | Utah Utes | 12 |
| Big 12 Conference | West Virginia Mountaineers | 12 |
| Big Ten Conference | Illinois Fighting Illini | 12 |
| Big Ten Conference | Indiana Hoosiers | 12 |
| Big Ten Conference | Iowa Hawkeyes | 12 |
| Big Ten Conference | Maryland Terrapins | 12 |
| Big Ten Conference | Michigan State Spartans | 12 |
| Big Ten Conference | Michigan Wolverines | 12 |
| Big Ten Conference | Minnesota Golden Gophers | 12 |
| Big Ten Conference | Nebraska Cornhuskers | 12 |
| Big Ten Conference | Northwestern Wildcats | 12 |
| Big Ten Conference | Ohio State Buckeyes | 12 |
| Big Ten Conference | Oregon Ducks | 12 |
| Big Ten Conference | Penn State Nittany Lions | 12 |
| Big Ten Conference | Purdue Boilermakers | 12 |
| Big Ten Conference | Rutgers Scarlet Knights | 12 |
| Big Ten Conference | UCLA Bruins | 12 |
| Big Ten Conference | USC Trojans | 12 |
| Big Ten Conference | Washington Huskies | 12 |
| Big Ten Conference | Wisconsin Badgers | 12 |
| Conference USA | Delaware Blue Hens | 12 |
| Conference USA | Florida International Panthers | 12 |
| Conference USA | Jacksonville State Gamecocks | 12 |
| Conference USA | Kennesaw State Owls | 12 |
| Conference USA | Liberty Flames | 12 |
| Conference USA | Middle Tennessee Blue Raiders | 12 |
| Conference USA | Missouri State Bears | 12 |
| Conference USA | New Mexico State Aggies | 12 |
| Conference USA | Sam Houston Bearkats | 12 |
| Conference USA | Western Kentucky Hilltoppers | 12 |
| FBS Independents | Notre Dame Fighting Irish | 12 |
| FBS Independents | UConn Huskies | 12 |
| Mid-American Conference | Akron Zips | 12 |
| Mid-American Conference | Ball State Cardinals | 12 |
| Mid-American Conference | Bowling Green Falcons | 12 |
| Mid-American Conference | Buffalo Bulls | 12 |
| Mid-American Conference | Central Michigan Chippewas | 12 |
| Mid-American Conference | Eastern Michigan Eagles | 12 |
| Mid-American Conference | Kent State Golden Flashes | 12 |
| Mid-American Conference | Massachusetts Minutemen | 12 |
| Mid-American Conference | Miami (OH) RedHawks | 12 |
| Mid-American Conference | Ohio Bobcats | 12 |
| Mid-American Conference | Sacramento State Hornets | 12 |
| Mid-American Conference | Toledo Rockets | 12 |
| Mid-American Conference | Western Michigan Broncos | 12 |
| Mountain West Conference | Air Force Falcons | 12 |
| Mountain West Conference | Hawai'i Rainbow Warriors | 12 |
| Mountain West Conference | Nevada Wolf Pack | 12 |
| Mountain West Conference | New Mexico Lobos | 12 |
| Mountain West Conference | North Dakota State Bison | 12 |
| Mountain West Conference | Northern Illinois Huskies | 12 |
| Mountain West Conference | San José State Spartans | 13 |
| Mountain West Conference | UNLV Rebels | 12 |
| Mountain West Conference | UTEP Miners | 12 |
| Mountain West Conference | Wyoming Cowboys | 12 |
| Pac-12 Conference | Boise State Broncos | 11 |
| Pac-12 Conference | Colorado State Rams | 11 |
| Pac-12 Conference | Fresno State Bulldogs | 11 |
| Pac-12 Conference | Oregon State Beavers | 11 |
| Pac-12 Conference | San Diego State Aztecs | 11 |
| Pac-12 Conference | Texas State Bobcats | 11 |
| Pac-12 Conference | Utah State Aggies | 11 |
| Pac-12 Conference | Washington State Cougars | 11 |
| Southeastern Conference | Alabama Crimson Tide | 12 |
| Southeastern Conference | Arkansas Razorbacks | 12 |
| Southeastern Conference | Auburn Tigers | 12 |
| Southeastern Conference | Florida Gators | 12 |
| Southeastern Conference | Georgia Bulldogs | 12 |
| Southeastern Conference | Kentucky Wildcats | 12 |
| Southeastern Conference | LSU Tigers | 12 |
| Southeastern Conference | Mississippi State Bulldogs | 12 |
| Southeastern Conference | Missouri Tigers | 12 |
| Southeastern Conference | Oklahoma Sooners | 12 |
| Southeastern Conference | Ole Miss Rebels | 12 |
| Southeastern Conference | South Carolina Gamecocks | 12 |
| Southeastern Conference | Tennessee Volunteers | 12 |
| Southeastern Conference | Texas A&M Aggies | 12 |
| Southeastern Conference | Texas Longhorns | 12 |
| Southeastern Conference | Vanderbilt Commodores | 12 |
| Sun Belt Conference | App State Mountaineers | 12 |
| Sun Belt Conference | Arkansas State Red Wolves | 12 |
| Sun Belt Conference | Coastal Carolina Chanticleers | 12 |
| Sun Belt Conference | Georgia Southern Eagles | 12 |
| Sun Belt Conference | Georgia State Panthers | 12 |
| Sun Belt Conference | James Madison Dukes | 12 |
| Sun Belt Conference | Louisiana Ragin' Cajuns | 12 |
| Sun Belt Conference | Louisiana Tech Bulldogs | 12 |
| Sun Belt Conference | Marshall Thundering Herd | 12 |
| Sun Belt Conference | Old Dominion Monarchs | 12 |
| Sun Belt Conference | South Alabama Jaguars | 12 |
| Sun Belt Conference | Southern Miss Golden Eagles | 12 |
| Sun Belt Conference | Troy Trojans | 12 |
| Sun Belt Conference | UL Monroe Warhawks | 12 |

## 8. Flagged Team Game Counts

- Teams with **fewer than 10** games: none
- Teams with **more than 13** games: none
- **San José State Spartans - 13 games** (highest count in the file). Verified against 13 distinct ESPN event ids (not a duplicate); left as-is since it traces to 13 genuine, distinct ESPN events.
- All other genuine FBS programs have between 10 and 13 games, consistent with a 12-game regular-season target plus scheduling variance.
- **All 8 Pac-12 Conference teams show 11 games instead of 12.** Their week-13 (2026-11-28) matchups are the conference's still-unresolved rivalry pairings: 4 teams (Colorado State, Fresno State, Utah State, Washington State) appear as a real home team against a "TBD" opponent - excluded per Section 3 - and the other 4 (Boise State, Oregon State, San Diego State, Texas State) have no week-13 entry at all in ESPN's data. This is a conference-wide gap, not an error in any single team's row.

## 9. Miami / Miami (OH) Identity Confirmation

Confirmed separate throughout the build, keyed by ESPN's numeric team id (Miami Hurricanes = ESPN team id 2390, Miami (OH) RedHawks = ESPN team id 193) rather than by name string, eliminating any risk of conflation:

- Miami Hurricanes: 12 games
- Miami (OH) RedHawks: 12 games
- No row in the final file uses a bare "Miami" label; both are always fully qualified ("Miami Hurricanes" / "Miami (OH) RedHawks").

## 10. North Dakota State Routing Confirmation

- **12 games retained** for North Dakota State (ESPN team id 2449).
- Conference column: **Mountain West Conference** in all 12 rows (approved 2026 assignment).
- ESPN's own structured `conferenceId` for this team already resolved to Mountain West Conference in all 12 of 12 rows - no override was actually needed, but the approved assignment is applied unconditionally by team id in the build script regardless of what ESPN reports, so any future ESPN change would be forced back to Mountain West Conference and logged.

## 11. Sacramento State Routing Confirmation

- **12 games retained** for Sacramento State (ESPN team id 16).
- Conference column: **Mid-American Conference** in all 12 rows (approved 2026 assignment).
- ESPN's own structured `conferenceId` for this team already resolved to Mid-American Conference in all 12 of 12 rows - no override was actually needed, but the approved assignment is applied unconditionally by team id in the build script regardless of what ESPN reports, so any future ESPN change would be forced back to Mid-American Conference and logged.

- North Dakota State at Sacramento State (2026-09-20, ESPN event id 401864507) is the reclassifiers' head-to-head matchup and is counted once in the schedule, correctly attributed to both teams.

## 12. Known Source Limitations

- **ESPN's own 2026 calendar has no distinct "Week 0" label.** ESPN's Preseason season-type (type 1) spans 2026-02-01 to 2026-08-22 and returned **zero** events on direct query. ESPN reports the 2026-08-29 and 2026-08-30 opening-weekend games as regular-season week 1. This project normalizes those two dates to Week 0 (Section 4); ESPN's own season_type/week value is preserved verbatim in each affected row's Notes.
- **Weeks 14-15 are sparse by design, not by retrieval error.** Verified by checking major programs (Michigan, Ohio State, Alabama, Texas, etc.) - all have their full 12-game regular-season slate already scheduled, concentrated in weeks 1-13. Week 14 contains only the 10 conference-championship event shells (documented in Section 5, not loaded); week 15 contains only the Celebration Bowl shell (excluded) and Navy at Army (retained).
- **10 non-competing entities in ESPN's FBS roster** (all-star/exhibition game placeholders such as "East All-Stars" and "Team Gaither") appear in the structured FBS group-80 team list but have no 2026 games; excluded from all schedule-count expectations (see Section 7).
- **4 regular-season games with a known home team but a TBD opponent** (all Pac-12, Week 13, 2026-11-28) are not yet resolvable and were excluded rather than guessed.
- **All bowl, CFP, and conference-championship games are unresolved as of this retrieval** (participants not yet determined); none are included in the loadable file, per the explicit no-placeholder-participant rule (no exception for championships).
- Scores/results are blank for all 888 retained games because the 2026 season has not started as of the retrieval date (2026-07-19); every row has `completed=FALSE`.

## 13. Items Requiring Manual Review

- The 4 excluded Pac-12 Week 13 TBD-opponent games (Colorado State, Fresno State, Utah State, Washington State hosts) should be re-pulled once ESPN publishes the opponent, so they can be added in a future revision.
- All 44 excluded bowl/CFP games should be re-pulled after the regular season concludes and participants are determined, if a future phase of this project wants bowl-season coverage.
- All 10 conference-championship event shells (Section 5) should be re-pulled once each conference's title-game participants are set by regular-season standings, so they can be loaded as normal two-real-team rows at that point.

## 14. Deliverable Paths

- Final schedule CSV: `TTW_2026_Verified_Schedule_ESPN_v1.0.csv` (888 rows)
- Validation script: `validate_schedule.py`
- Retrieval log: `retrieval_log.csv`
- Raw ESPN responses: `raw_espn/`
- Acquisition/build scripts: `scripts/`
