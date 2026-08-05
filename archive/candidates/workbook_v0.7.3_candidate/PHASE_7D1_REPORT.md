# Phase 7D.1 — QB Candidate Repair & Completion

**Date:** 2026-08-03 (America/New_York) · **Candidate:** `TTW_NCAAF_Power_Ratings_2026_v0.7.3_CANDIDATE.xlsx`
**v0.6.2 AUTHORITATIVE:** unmodified · **v0.7.2:** unmodified · **Google Sheet:** never accessed · **NOT promoted.**

## Recommendation: **OPTION B — DEFER PROMOTION**

Both approved repairs are applied and every regression passes. Promotion is
nonetheless deferred for one decisive reason: **Tier 1 live verification is
incomplete — 54 of 77 Tier 1 teams remain unverified**, and the very first
sweep of that backlog **found a real defect** (a graduated quarterback listed as
a returning starter). That is direct evidence the backlog carries more errors.
Promoting now would import unverified data into production.

---

## 1. Texas Tech correction report (approved repair)

Row alignment verified before editing: **TEAM MAP row 52 = TTU / Texas Tech**,
Active QB = **Will Hammond** (asserted in code, not assumed).

| Cell | Before | After |
|---|---|---|
| `QB VALUES!H52` | `L` | **`M`** |
| `QB VALUES!K52` | 2026-07-21 | **2026-08-03** |
| `QB VALUES!L52` | "backup promotion \| OPEN COMPETITION…" | Full clearance note (below) |
| `QB VALUES!D52` / `F52` | blank | **blank — deliberately untouched** |

Notes text records: surgeon clearance reported; projected Week 1 starter; **final
team medical clearance still pending** (~Aug 21 nine-month mark); **LIKELY (M),
not KNOWN (H)** — no official naming; **numerical QB delta remains gated**.

**Gating confirmed:** `H52 = M`, `D52`/`F52` blank → `G52` blank → **status stays
UNCERTAIN**. The metadata change creates **no numerical adjustment**.

## 2. Exact list of previously unverified teams

**Re-derived from the candidate — the true figure is 59, not the ~47 estimated in
Phase 7D.** (Phase 7D under-counted; correction logged.)

Tier 1 population = all M (45) + all L (32) = **77**; verified in Phases 7A–7D = **18**;
**remaining at phase start = 59**, distributed: MAC 11 · CUSA 8 · Big Ten 6 ·
Pac-12 6 · American 6 · Mountain West 6 · Sun Belt 6 · Big 12 4 · ACC 3 · SEC 2 ·
Independent 1. Full list in `qb_inventory_v073.json` → `tier1_outstanding_teams`.

## 3. Live-verification results (this phase)

**6 teams freshly verified. 53 of the 59 remain outstanding** (54 counting Akron's
reclassification into the L pool — see inventory).

| Team | Candidate entry | Live finding | Result |
|---|---|---|---|
| **Akron** | Ben Finley (M), noted *"returning starter"* | **Finley GRADUATED** after a two-year starting run; Poffenbarger (North Texas transfer, 5th school in 6 seasons) entered spring as projected starter; **no clear QB1**, open camp competition | **CORRECTED** |
| Texas Tech | Will Hammond (L) | Surgeon clearance; Week-1 projection; team clearance pending | **CORRECTED (approved)** |
| Ball State | Luster (L, open) | Mizzell/Luster both may see action | **CONFIRMED** |
| Central Michigan | Open (L) | Flores among contenders; unsettled | **CONFIRMED** |
| Toledo | John Alan Richter (M) | Returns; 699 yds/7 TD over two seasons | **CONFIRMED** |
| Western Michigan | Broc Lowry (M) | Returning MAC-champion QB; 1,803 pass/963 rush/23 TD | **CONFIRMED** |

**Verification could not be completed at scale this phase.** Aggregator sources
that would cover many teams at once (Athlon's all-138 projection) returned
**HTTP 403**, and conference-level searches produced partial, mixed-reliability
results that fail the "no snippet as final evidence" standard. Rather than
inflate coverage, I stopped and reported the true state.

## 4. QB correction log

| Team | Field | Prior value | Corrected value | Reason | Source | Verified |
|---|---|---|---|---|---|---|
| Texas Tech | H52 | `L` | `M` | Approved 7C.1/7D conclusion: surgeon-cleared, projected Week 1 starter, team clearance pending → LIKELY | ESPN; On3 Red Raider coverage | 2026-08-03 |
| Texas Tech | K52 / L52 | 2026-07-21 / old note | 2026-08-03 / clearance note | Accompanies the approved change | — | 2026-08-03 |
| **Akron** | **E105** | **`Ben Finley`** | **`Open (Reese Poffenbarger / Brayden Roggow)`** | **Finley graduated — stale record listing a departed player as the 2026 starter** | Yahoo/Hustle Belt (Poffenbarger signing); ESPN player page; Akron athletics spring roster | 2026-08-03 |
| **Akron** | **H105** | **`M`** | **`L`** | No clear QB1; open fall-camp competition — fails the M standard | same | 2026-08-03 |
| Akron | K105 / L105 | 2026-07-21 / old note | 2026-08-03 / correction note | Accompanies the correction | — | 2026-08-03 |

**No other record was altered.** Dates were **not** refreshed for the 53
unverified teams — they still read 2026-07-21, truthfully.

## 5–7. Final inventory and counts

| Metric | Result |
|---|---|
| Teams | **138 unique** — 0 missing, 0 duplicated, 0 shifted ✔ |
| **Final H/M/L** | **61 H / 45 M / 32 L** |
| Invalid codes | **None** ✔ |
| Formula columns (A,B,G,M) | intact on all 138 rows ✔ |
| Input columns | constants only ✔ |
| Nonzero QB values | **0** ✔ |

The aggregate counts are **unchanged by coincidence** — the two repairs offset
(TTU `L→M`, AKR `M→L`). This was not targeted; it is arithmetic.

**Status counts changed: 105 OK / 33 UNCERTAIN → 104 OK / 34 UNCERTAIN.** The
single mover is **Akron**, correctly re-gated by its `L` code.

## 8. Source & conflict log

| # | Claim | Source 1 | Source 2 | Resolution | Residual |
|---|---|---|---|---|---|
| E-1 | Akron QB = Ben Finley, "returning starter" | Candidate (July research) | Finley graduated; Poffenbarger signed as projected starter | **Candidate wrong → corrected** | Whether Poffenbarger holds the job |
| E-2 | Akron has a settled starter (M) | Candidate | "Akron doesn't have a clear QB1 for 2026" | **M unjustified → L** | Camp outcome |
| E-3 | Tier 1 backlog size | Phase 7D: "~47" | Re-derivation: **59** | **7D under-counted; corrected** | None |
| E-4 | Bulk verification feasible via aggregator | Athlon all-138 article | **HTTP 403** | Blocked; per-team/beat sourcing required | 53 teams outstanding |
| E-5 | Toledo / WMU / Ball State / CMU entries | Candidate | Live reporting | **Confirmed accurate** | None |

## 9. Regression-test report

| # | Test | Result |
|---|---|---|
| 1 | H + populated metadata | 61 teams → **OK** ✔ |
| 2 | M + populated metadata | 43 → OK; **2 → UNCERTAIN** (UNC, Texas Tech — both blank D/F, correctly gated) ✔ |
| 3 | L + populated metadata | 32 → **UNCERTAIN** ✔ |
| 4 | Blank numerical values | → UNCERTAIN ✔ (34 teams) |
| 5 | Zero numerical values | → delta 0, no adjustment ✔ (104 teams) |
| 6 | QB status output | **104 OK / 34 UNCERTAIN** ✔ (Akron the only mover) |
| 7 | Starter-to-backup delta | **0 nonzero deltas** ✔ |
| 8 | PENDING LINE priority | Outranks QB UNCERTAIN; 0 market spreads loaded → **every game still PENDING LINE**; no visible status change ✔ |
| 9 | FCS — NO PLAY priority | Outranks QB gate; unaffected ✔ |
| 10 | TRANSITION UNCERTAIN priority | Ranks below QB gate; masked by PENDING LINE; unchanged ✔ |
| 11 | BET toggle | `SETTINGS!B11 = "N"`, untouched; unreachable without lines ✔ |
| 12 | **No team-rating movement** | TEAM RATINGS **byte-identical**; `ENGINE!M` = 0 throughout ✔ |
| 13 | **No projected-spread movement** | ENGINE sheet **unchanged** ✔ |
| 14 | **No formula changes** | **0** ✔ |
| 15 | No unrelated status changes | Only Akron's QB status moved, by design ✔ |
| 16 | **Texas Tech L→M creates no numerical adjustment** | Confirmed — D52/F52 blank, G52 blank ✔ |
| 17 | **Texas Tech remains gated** | Status **UNCERTAIN** ✔ |
| 18 | **No confidence edit moves a rating** | Confirmed — ratings untouched ✔ |

## 10–11. Diff v0.7.2 → v0.7.3

**20 changed cells. Zero formula changes. Zero unrelated/unauthorized/unknown.**

| Cells | Classification |
|---|---|
| `QB VALUES!H52`, `K52`, `L52` | **APPROVED TEXAS TECH CORRECTION** (3) |
| `QB VALUES!E105`, `H105` | **VERIFIED QB FACTUAL UPDATE** (2) |
| `QB VALUES!K105`, `L105` | **NOTE OR DATE UPDATE** (2) |
| `CHANGELOG!A67:D69` | **VERSION OR CHANGELOG** (12) |
| `START HERE!A1` | **VERSION OR CHANGELOG** (1) |

**UNRELATED: 0 · UNAUTHORIZED: 0 · UNKNOWN: 0.** Formula count **123,011 →
123,011 (delta 0)**; 21 sheets, order and visibility identical; 18 sheets untouched.

## 12. Open item requiring owner decision

**OI-1 — Akron is now `L`-coded but retains `D=0 / F=0`.** Under the original
build rule (initialize H/M only), an L team would be blank. Behavior is
nonetheless **correct**: `G = 0` (no adjustment) and status **UNCERTAIN** (the
`L` code forces the gate). I did **not** clear the values, because that is a
numerical change the phase instruction reserves. Options: (a) leave as-is —
behaviorally correct; (b) clear D105/F105 for methodological consistency.

## 13–14. Zero-change verification & manifest

| File | SHA-256 | Status |
|---|---|---|
| **v0.6.2 AUTHORITATIVE** | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` | **UNCHANGED** = `PROJECT_MANIFEST.json` ✔ |
| **v0.7.2 CANDIDATE** | `82ee5b3d4731c18a2deb3288d63c9b6eb8e1dae4bc5c28bb6be0cdebf151a183` | **UNCHANGED** ✔ |
| **v0.7.3 CANDIDATE** (new) | `07bed6dedc647124e77d78324b8e5f37e1f35ca5eef37c0ee36615dd8c7da72d` | Built this phase |

Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` — **never accessed.**
No rating, HFA, formula, structure, threshold, schedule, or source-weight change.

## Path to Option A

Verify the **53 outstanding Tier 1 teams** (list in `qb_inventory_v073.json`),
correct whatever that surfaces, then revalidate. Given that the first six checks
already produced one hard defect, I'd budget for **several more corrections** in
that backlog. The MAC (11) and CUSA (8) are the largest clusters and the most
likely to contain stale records, since they receive the least coverage.
