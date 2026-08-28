# TTW Independent 2025 Prior — v0.5.1 Re-check (2026-07-20)

Continuing the investigation per the user's explicit instruction, beyond
the two paths already tried and re-confirmed blocked in the v0.5 build
(direct release download → session repo-scope gate; `add_repo` →
cross-tier denial; CFBD API → 401, no key). New angles attempted this
pass, all against the same canonical file
(`play_by_play_2025.rds`/`.parquet`, release tag `cfbfastR_cfb_pbp`,
`sportsdataverse/sportsdataverse-data`):

| Attempt | Result |
|---|---|
| `api.github.com/repos/.../releases/tags/cfbfastR_cfb_pbp` (metadata only, not the asset) | HTTP 403 - same session repo-scope gate applies to the GitHub API too, not just raw/release downloads |
| jsdelivr GitHub CDN proxy (`cdn.jsdelivr.net/gh/.../@cfbfastR_cfb_pbp/...`) | HTTP 404. Control test against a known in-tree file on the same proxy (`@master/data/games_in_data_repo.csv`) returned 200, confirming the proxy itself works - the 404 is because GitHub Release assets live in a separate object store outside the git tree jsdelivr mirrors, not because of a session restriction |
| raw.githack / statically.io (another GitHub raw-content proxy) | Same git-tree limitation - a release tag isn't a resolvable ref for a file that's not committed to the repo |
| Hugging Face Hub dataset search (`cfbfastR`, "college football play by play") | 0 results |
| Kaggle public dataset search ("college football play by play") | No official/verifiable cfbfastR match (only unrelated NFL datasets) |

**Root cause confirmed, not just re-observed:** the blocker is specific to
GitHub **Release assets** (a separate storage tier from the repository's
git tree), and every third-party proxy that mirrors GitHub repo content
mirrors the git tree, not release assets - so no proxy can route around
it. The only two paths that could actually reach the file are (1) direct
GitHub access to that repo (blocked at the session/platform level) or
(2) a human downloading it through a browser and supplying it directly.

**Decision unchanged:** the prior remains blank. No unverified third-party
mirror was substituted - per the project's standing "verified sources
only" rule, an unofficial Kaggle/HF re-upload of unknown provenance and
completeness would not meet the bar even if one had been found.

Retrieval procedure is unchanged from the v0.5 write-up (still the
simplest path): open
`https://github.com/sportsdataverse/sportsdataverse-data/releases/tag/cfbfastR_cfb_pbp`
in a browser, download `play_by_play_2025.rds` (or `.parquet`), and
provide the file.
