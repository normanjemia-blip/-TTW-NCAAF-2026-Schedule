# TTW Independent 2025 Prior — Phase 5 Re-check (2026-07-20)

Re-tested both documented unblock paths from the v0.4.1 investigation
(`workbook_v0.4.1_deliverables/ttw_prior_source_investigation.md`).
Neither path opened up; findings are unchanged, re-verified fresh today:

1. **Direct release download**: `curl` against
   `https://github.com/sportsdataverse/sportsdataverse-data/releases/download/cfbfastR_cfb_pbp/play_by_play_2025.rds`
   → HTTP 403, body `{"message":"GitHub access to this repository is not
   enabled for this session. Use add_repo to request access."}`.
2. **`add_repo sportsdataverse/sportsdataverse-data`** → denied:
   `"cross-tier adds are not supported in v1: requested
   'sportsdataverse/sportsdataverse-data' but session already has repos
   from owner(s) [normanjemia-blip]. Start a new session with the
   requested repo as the initial source..."`
3. **CFBD API key**: re-checked environment (`env | grep -i cfbd/...`) —
   none configured; unauthenticated call to
   `api.collegefootballdata.com/games` → HTTP 401.

**Not substituted:** the ESPN scoreboard results fetched this phase for
the FCS framework (final scores only, no play-by-play/EPA) do **not**
satisfy the approved TTW-prior methodology, which requires per-play
EPA/success-rate/PPP data that only cfbfastR provides. They were not
used for the prior, and are not a proxy for it — used solely to build
the FCS opponent-rating framework (Phase 5 item 1), a different,
independently-scoped use of ESPN's schedule/results API.

## Decision

The TTW independent 2025 prior **remains blank**, per Architecture
Amendment v0.2 §1 and the user's explicit instruction not to substitute
SP+, polls, win totals, reputation, or another proxy.

## Exact file needed

`play_by_play_2025.rds` (or the equivalent `.parquet`/`.csv.gz`), from
GitHub release tag `cfbfastR_cfb_pbp` on repo
`sportsdataverse/sportsdataverse-data`. Confirmed complete for 2025
(1,662 games including full postseason and both reclassifiers — see the
v0.4.1 investigation) and schema-verified to carry every required field
(per-play EPA, success, scores, teams, game_id, week — verified from the
same dataset family's accessible 2019 file, 368 columns).

## Simplest user retrieval procedure

1. Open in a browser:
   `https://github.com/sportsdataverse/sportsdataverse-data/releases/tag/cfbfastR_cfb_pbp`
2. Download **`play_by_play_2025.rds`** (~65-75 MB; `.parquet` is a smaller,
   equally usable alternative if offered).
3. Upload the downloaded file into this project (any location the user
   points Claude to, e.g. attach it in a message).

No R installation or account is required — it is a plain public file
download; the friction is that the download is a release **asset**
(not a raw in-repo file), which this session's browsing tools cannot
reach directly given the current repo-scope restriction. A CFBD API key
(free tier) is the alternative unblock path.
