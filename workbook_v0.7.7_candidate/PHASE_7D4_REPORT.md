# Phase 7D.4 — Final Group of Five QB Verification

**Date:** 2026-08-03 (America/New_York) · **Candidate:** `TTW_NCAAF_Power_Ratings_2026_v0.7.7_CANDIDATE.xlsx`
**v0.6.2 AUTHORITATIVE:** unmodified · **v0.7.6:** unmodified · **Google Sheet:** never accessed · **NOT promoted.**

## Recommendation: **OPTION B — DEFER AND REPAIR REMAINING CASES**

**26 of 31 verified; 5 remain.** Option A requires the backlog to reach **zero**;
it stands at **5**. Everything else that Option A asks for is satisfied — all
corrections applied, numerical-consistency rules met, regressions pass, no
structural drift — so the gap is purely the five unverified records.

## 1. Starting backlog — reproduced, matches expectation

**31 teams**, distribution **Pac-12 6 · American 6 · Mountain West 6 · Sun Belt 6
· CUSA 4 · MAC 3** — matched exactly, **no P4/Independent remaining**. Machine-
readable table: `g5_backlog_starting_state.json` / `.csv`.

## 2. MAC (3/3 verified) — incl. the open conflict

| Team | Result | Finding |
|---|---|---|
| **Miami (OH)** | **CONFLICT RESOLVED**, L retained | **Both 7D.2 claims were right.** Gotkowski **is** on the official roster (RS-So; 5 games, **3 starts in 2025 incl. the MAC-title-clinching win**). The "Kansas transfer" is **David McComb** (RS-Fr) — **not Isaiah Marshall**, who remains on Kansas's roster. Three-way race with senior transfer **Caleb Heavner**; entering MAC Media Days the Kansas transfer appeared to hold the projected role. |
| **Buffalo** | **DEFECT**, L retained | Entry listed **CJ Ogbonna — Buffalo's 2024 SENIOR starter** (13 starts, 2,381 yds, 19 TD), no longer on the roster. Pete Lembo's actual room: **Jason Wright / Mason Cumbie / Elijah Holmes** (Wingate transfer). Buffalo News: UB "still searching for a starting quarterback." |
| **Sacramento State** | **CONFIRMED** M | **Carson Conklin returns** — on the official hornetsports.com 2026 roster, announced by Sac State ("HE'S BACK") after 2025 at Fresno State; Hornets' 2024 starter. |

## 3. Conference USA (4/4 verified)

**FIU** — JJ Kohl (App State transfer) confirmed as the new starter → **M**.
**Kennesaw State** — Rickie Collins (Syracuse transfer) **must hold off juco transfer Landon Varnes** → **M**, entry refined.
**Missouri State** — new HC **Casey Woods**, QB battle, **no starter named** → **L**.
**New Mexico State** — rebuild, likely competition, **no starter named** → **L**.

## 4. American (5/6 verified)

**East Carolina** — Chaston Ditta "likely takes the reins" after starting the 2025 Military Bowl → **M**.
**Navy** — Braxton Woodson, projected starter → **M**. **Rice** — Jacurri Brown → **M**. **Tulsa** — Baylor Hayes → **M**.
**Temple** — Jaxon Smolik (Penn State) vs Ajani Sheppard (Washington State), **Smolik owning the inside track** → **M**, entry refined.
**North Texas — NOT VERIFIED.**

## 5. Mountain West (6/6 verified)

| Team | Result | Finding |
|---|---|---|
| **Northern Illinois** | **DEFECT**, **L → M** | Entry listed "Davidson / Macon / Hamric" — **none appear in current coverage**. Verified: **Taron Dickens**, Western Carolina transfer and **FCS Walter Payton Award runner-up**, paired with new OC Tony Petersen (hired March 2026). Values **remain blank** per the L→M rule. |
| **UTEP** | **UPGRADE M → H** | **EJ Colson was NAMED the starter in the spring** (Incarnate Word transfer); no competition reported. Zeros **retained** (correct for H). |
| North Dakota State | CONFIRMED M | Nathan Hayes, **first-time** starter (senior). |
| Nevada | CONFIRMED L | Competition in fall camp; entry generalized. |
| San José State | CONFIRMED L | Niumatalolo "total reset," picking among **three** candidates. |
| Wyoming | CONFIRMED M | Tyler Hughes (W&M transfer; 2,330 pass/670 rush, 31 total TD), prior staff ties. |

## 6. Pac-12 (4/6 verified)

**Colorado State** — Hejny **locked in a battle with UConn transfer K'saan Farrar into fall camp** → **L**. *(Note: CSU's HC is Jim Mora, who left UConn — ties to the 7D.3A UConn finding.)*
**Fresno State** — **three-way battle "deep into August"** incl. Mercer transfer Braden Atkinson (Jerry Rice Award winner); prior single name uncorroborated → **L**, entry generalized.
**Oregon State** — **L → M** with documented tension: an SI headline says Maalik Murphy was **named starter**, while SI's Pac-12 tiers say he has "a slight upper hand" with a transfer "right on his tail." Both agree he **leads** → M, **not H**. Values stay blank.
**Utah State** — returning QB McCae Hillstead reunited with OC Robert Anae → **M**.
**Texas State — NOT VERIFIED. Washington State — NOT VERIFIED.**

## 7. Sun Belt (4/6 verified)

| Team | Result | Finding |
|---|---|---|
| **Appalachian State** | **DEFECT**, **M → L** + zeros cleared | Singleton **and Hasselbeck** are "the **main competitors**" — **no leader identified**. Per your standard, M must not rest on one player being the most recognizable name; Singleton's Arkansas/Purdue pedigree is name recognition, not evidence of a lead. |
| Arkansas State | CONFIRMED L | HC Butch Jones: race "continues," **four capable players**. |
| Coastal Carolina | CONFIRMED L | **Deuce Bailey** a "potential" starter, followed Beard from Missouri State. |
| James Madison | CONFIRMED M (tension noted) | "Reloads at QB" with Memphis transfer Arrington Maiden, but same coverage says "expected to **compete** for the starting role" → M, not H. |
| **Georgia Southern** | **NOT VERIFIED** | — |
| **Old Dominion** | **NOT VERIFIED** | — |

## 8. QB correction log — code and value changes

| Team | Row | Prior starter | Corrected | Code | D/F | Reason |
|---|---:|---|---|---|---|---|
| **Buffalo** | 108 | CJ Ogbonna | **Open (Wright / Cumbie / Holmes)** | L → L | blank | Stale: Ogbonna was the 2024 senior starter |
| **Northern Illinois** | 123 | Open (Davidson/Macon/Hamric) | **Taron Dickens (WCU transfer)** | **L → M** | blank (unchanged) | Stale names; Dickens is the FCS Payton runner-up |
| **Appalachian State** | 128 | Malachi Singleton | **Open (Singleton / Hasselbeck)** | **M → L** | **0/0 → blank** | No leader; M rested on name recognition |
| **UTEP** | 126 | EJ Colson | *unchanged* | **M → H** | 0/0 retained | Officially named in spring |
| **Oregon State** | 76 | Maalik Murphy | **Murphy (leader; Atkinson pushing)** | **L → M** | blank (unchanged) | Clear leader; naming claim contested |
| **Miami (OH)** | 112 | Thomas Gotkowski | **Open (McComb / Gotkowski / Heavner)** | L → L | blank | Conflict resolved; three-way race |
| Nevada, SJSU, Fresno St., CSU, Kennesaw, Temple, Coastal, Missouri St. | — | single names | competition-accurate entries | unchanged | unchanged | Entry refinement only |

**Numerical-cell consistency repairs: 1** (Appalachian State M→L, zeros cleared). **No nonzero QB value created anywhere.**

## 9. Dataset integrity — all confirmed

| Check | Result |
|---|---|
| 138 unique teams, no missing / duplicate / shifted rows | ✔ |
| Invalid H/M/L codes | **0** ✔ |
| Every L-coded team has blank numerical inputs | ✔ **0 violations** |
| Nonzero QB values | **0** ✔ |
| Formula cells intact; columns A, B, G, M unchanged | ✔ |
| **Final H/M/L** | **64 H / 43 M / 31 L** = 138 |
| **Final OK/UNCERTAIN** | **101 OK / 37 UNCERTAIN** |
| **Blank / zero numerical** | **37 blank / 101 zero** = 138 |
| Unresolved conflicts | **0 blocking** (Miami OH closed; Oregon State and JMU carry documented tension, resolved conservatively) |
| Teams still dated 2026-07-21 | **87** — the 5 backlog teams **plus 82 H-coded tier-2 teams that were never in Tier 1 scope** (expected, not a defect) |
| **Remaining backlog** | **5** |

**Final backlog:** Texas State (Pac-12, M) · Washington State (Pac-12, M) · North Texas (American, M) · Georgia Southern (Sun Belt, L) · Old Dominion (Sun Belt, M).

## 10. Regression-test report — all pass

No confidence edit created an unintended numerical adjustment ✔ · no team rating
changes (TEAM RATINGS not in diff) ✔ · no projected spread changes (ENGINE not in
diff) ✔ · **no formula changes (0)** ✔ · PENDING LINE / FCS — NO PLAY /
TRANSITION UNCERTAIN priorities unchanged ✔ · BET toggle unchanged (SETTINGS not
in diff) ✔ · blank vs zero meanings preserved (37/101) ✔ · **every L-coded team
gated (0 violations)** ✔ · H/M behave per existing logic (64 H → OK; 37 M → OK;
6 M → UNCERTAIN, all blank-gated) ✔ · no row-alignment changes ✔ · no unrelated
sheet changes ✔.

## 11–12. Diff v0.7.6 → v0.7.7

**84 changed cells · ZERO formula changes · zero unrelated / unauthorized / unknown.**

| Classification | Count |
|---|---:|
| VERIFIED MAC QB UPDATE | 8 |
| VERIFIED CUSA QB UPDATE | 10 |
| VERIFIED AMERICAN QB UPDATE | 11 |
| VERIFIED MOUNTAIN WEST QB UPDATE | 16 |
| VERIFIED PAC-12 QB UPDATE | 12 |
| VERIFIED SUN BELT QB UPDATE | 12 |
| **NUMERICAL-CELL CONSISTENCY REPAIR** (App State D128/F128) | **2** |
| VERSION OR CHANGELOG | 13 |
| UNRELATED / UNAUTHORIZED / UNKNOWN | **0** |

Formula count **123,011 → 123,011 (delta 0)**; 21 sheets, order and visibility identical.

## 13. Manifest / SHA-256

| File | SHA-256 |
|---|---|
| **v0.7.7 CANDIDATE** (new) | `3da33d0c10a375c6bd3e43c06f1119b1a6a72cfb49d16abff65ed9c670d02a73` |
| v0.7.6 CANDIDATE | `080986dd5dc29dc23b22e104eb7aa523c757196562eb49846a4c3cae30d7a5bb` — **UNCHANGED** ✔ |
| v0.6.2 AUTHORITATIVE | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` — **UNCHANGED**, = `PROJECT_MANIFEST.json` ✔ |

Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` — **never accessed.**

## 14. Closing note on the sourcing standard

Where a team's evidence came from a **current conference QB projection that
independently corroborated the candidate's existing entry**, I recorded it as
verified at **M** and said so explicitly in the note ("no official naming
located") — never at H. **H was assigned only twice in this project's history on
a naming or established-returning-starter basis**, and in this batch only once
(UTEP, officially named in spring).

**Cumulative defect pattern across all batches: every single classification
defect found — Akron, Arkansas, UConn, Buffalo, Northern Illinois, Appalachian
State — was an M or a named starter that the evidence did not support.** Not one
was a team rated too uncertain. That asymmetry is the strongest argument for
finishing the last five before promotion.
