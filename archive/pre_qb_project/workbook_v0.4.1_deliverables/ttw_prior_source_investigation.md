# TTW Independent 2025 Prior — Public-Dataset Source Investigation (v0.4.1)

**Directive:** before declaring the TTW independent 2025 prior blocked,
investigate the official/public cfbfastR and SportsDataverse 2025
college-football datasets permitted by the approved architecture; verify
whether a complete final 2025 dataset contains the fields required to
reproduce the approved prior methodology; document source, retrieval
date, season completeness, fields, and validation result. Do not
substitute a proxy or change the methodology.

**Investigation date:** 2026-07-20. All probe artifacts archived under
`cfbfastr_probe/` in this deliverables directory.

## 1. The approved methodology's data requirements

Per Architecture Amendment v0.2 §1 (verbatim requirements): the prior is
"an independently constructed TTW 2025 performance rating built in Phase 4
from verified 2025 CFBD/cfbfastR data: opponent-adjusted scoring margin
(per-game capped, default ±28), offensive/defensive EPA per play, success
rate, points per play, strength of schedule via opponent adjustment, venue
adjustment, and recency weighting."

Field checklist a 2025 dataset must support:

| Requirement | Field(s) needed |
|---|---|
| Scoring margin, per-game | final scores per game, teams |
| Opponent adjustment / SoS | full game graph (who played whom) |
| Venue adjustment | home/away/neutral designation |
| Recency weighting | game date or week ordering |
| Off/def EPA per play | per-play EPA attributed to offense/defense |
| Success rate | per-play success indicator |
| Points per play | scores + play counts (derivable) |

## 2. Source identification (official, public)

The official public distribution of cfbfastR data is documented in the
cfbfastR package's own loader source code
(`R/load_cfb_pbp.R`, fetched 2026-07-20 from
`raw.githubusercontent.com/sportsdataverse/cfbfastR/main/R/load_cfb_pbp.R`
— archived as `cfbfastr_probe/` evidence):

> `https://github.com/sportsdataverse/sportsdataverse-data/releases/download/cfbfastR_cfb_pbp/play_by_play_{season}.rds`, seasons 2014–most recent.

i.e., **GitHub release assets on `sportsdataverse/sportsdataverse-data`,
release tag `cfbfastR_cfb_pbp`**. The older `sportsdataverse/cfbfastR-data`
repository holds in-tree copies (`pbp/{rds,csv,parquet}/play_by_play_{year}.*`)
only up to **season 2020** (probed directly: 2019/2020 return HTTP 200;
2021–2025 return 404 under every documented path pattern).

## 3. Season-completeness verification (2025)

The data repo's publicly readable manifest
`data/games_in_data_repo.csv` (retrieved 2026-07-20, archived in
`cfbfastr_probe/games_in_data_repo.csv`; 13,894 rows, seasons 2014-2025)
documents exactly what the release dataset contains:

- **2025: 1,662 games** — in line with verified-complete prior seasons
  (2022: 1,626; 2023: 1,695; 2024: 1,661).
- Postseason inclusion was verified structurally against 2024, a season
  whose completeness is independently checkable: the 2024 manifest shows
  Notre Dame and Ohio State with 16 games each (12 regular + full CFP
  runs) — postseason games fold into low week numbers rather than
  appearing as weeks 17+. The 2025 manifest shows the same shape:
  teams reaching 16 games (Indiana, Miami), week-1 bucket inflated the
  same way (190 vs 201 in 2024). Conclusion: **the 2025 dataset includes
  the full postseason** and is a complete final season.
- **Reclassifier coverage confirmed:** North Dakota State appears in 13
  2025 games and Sacramento State in 12 — both FBS-reclassifying teams'
  2025 (FCS) seasons are present in the dataset.

## 4. Field verification

The 2025 release asset itself could not be opened from this session (see
§5), so the dataset family's schema was verified from the **same
repository's accessible 2019 parquet**
(`pbp/parquet/play_by_play_2019.parquet`, 71,104,314 bytes, retrieved
2026-07-20; 156,511 rows × **368 columns**; full column list archived as
`cfbfastr_probe/cfbfastR_2019_schema_columns.txt`). Against the checklist:

| Requirement | Present in schema |
|---|---|
| Scores/margin | `home_score`, `away_score`, per-play running scores |
| Game graph | `game_id`, `home_team_name`/`away_team_name` (+ids/abbrevs) |
| Venue | home/away designation per game; **no neutral-site flag** — joins from the already-approved ESPN schedule source via `game_id` (cfbfastR's `game_id` IS the ESPN event id) |
| Recency | `week`, `season` (game date likewise joinable via ESPN `game_id`) |
| EPA off/def | `epa`, `def_epa` (+ rush/pass/scrimmage splits) |
| Success | `epa_success` family (incl. down-type splits) |
| Points per play | derivable exactly from scores + play rows; `drive_points` present |

**Verdict: the dataset family supports every component of the approved
methodology** — with the neutral-site/date join coming from the ESPN
schedule data already approved and loaded in Phase 3 (no new source, no
methodology change).

## 5. Access result — the actual blocker

The 2025 asset lives only in GitHub **release assets**, and this session's
platform blocks them:

1. Direct download of
   `github.com/sportsdataverse/sportsdataverse-data/releases/download/cfbfastR_cfb_pbp/play_by_play_2025.rds`
   returns the session gate: *"GitHub access to this repository is not
   enabled for this session. Use add_repo to request access."*
2. `add_repo sportsdataverse/cfbfastR-data` was denied with the platform
   error: *"cross-tier adds are not supported in v1: requested
   'sportsdataverse/cfbfastr-data' but session already has repos from
   owner(s) [normanjemia-blip]."*
3. In-tree files on `raw.githubusercontent.com` ARE reachable (that is how
   the manifest, loader source, README, and 2019 schema above were
   retrieved and archived) — but in-tree season files stop at 2020.
4. The CFBD API remains 401 without a key (user confirmed none available).

## 6. Validation result and decision

- The official public 2025 dataset **exists, is final-season complete
  (including postseason and both reclassifiers), and contains the fields
  required to reproduce the approved methodology**.
- It is, however, **unreachable from this session** — a platform access
  limitation, not dataset incompleteness and not methodology
  infeasibility.
- Per the directive and Amendment v0.2 §1, the prior therefore **remains
  blank**; no proxy was substituted and the methodology was not changed.
- Documented unblock paths (any one suffices):
  1. a session created with a `sportsdataverse` repository as an initial
     source (release assets would then be in scope);
  2. the user downloads `play_by_play_2025.rds` or `.parquet` (~70 MB)
     from the release page and supplies it to the project;
  3. a CollegeFootballData.com API key.
- Note for when it unblocks: constructing the prior still involves
  parameters the approved docs name but do not fix numerically (venue
  adjustment magnitude, recency-weight curve, blend weights of the margin
  vs. EPA/success/PPP composites). Per project rules these are material
  decisions that will be proposed for approval before any values are
  loaded — not chosen silently.
