# TTW COLLEGE FOOTBALL POWER RATINGS — QB CLOSEOUT, 24 AUGUST 2026

**Verification timestamp:** Monday, 2026-08-24, **10:02:59 EDT** (America/New_York)
**Container clock at run:** 2026-08-24 14:02:59 UTC
**Research cutoff:** the verification timestamp above
**Task type:** READ-ONLY research and reconciliation — no production writes
**Predecessor handoff:** `TTW_v084_Promotion_2026-08-21.md`

---

## 1. PRE-FLIGHT

### 1.1 Repository

| Item | Value |
|---|---|
| Repository | `/home/user/-TTW-NCAAF-2026-Schedule` |
| Remote | `https://github.com/normanjemia-blip/-TTW-NCAAF-2026-Schedule` |
| Branch | `claude/2026-ncaaf-schedule-build-by6j5n` |
| HEAD | `14cf041fd414730aaf13dbc569758c875bd9100e` — *Promote v0.8.4 NIU/Tulane packet with live resync* |
| Git status at pre-flight | **clean** — no modified, staged or untracked files |
| Sync with origin | **0 ahead / 0 behind** |

**No reset, checkout, discard, clean or overwrite was performed at any point.**

### 1.2 Authoritative workbook — CONFIRMED

| Item | Value |
|---|---|
| File | `promotion_v0.8.4/TTW_College_Football_Power_Ratings_v0.8.4_AUTHORITATIVE.xlsx` |
| SHA-256 | `ed5d3b3d9aa3dd4f845e91688216a28276aaa0b3e4bd68ba09a9ceb96a8adaff` |
| Matches `PROJECT_MANIFEST.json` `current_version` | yes |
| QB status census | **104 OK / 34 UNCERTAIN** |
| Confidence census | **69 H / 40 M / 29 L** |

### 1.3 Live production master — read-only verification

Read via metadata only. **No write of any kind was issued.**

| Item | Value |
|---|---|
| Sheet ID | `1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA` |
| **Title, exactly as read** | **`TTW College Football Power Ratings v0.8.4 — PRODUCTION MASTER`** |
| Last modified | 2026-08-23T13:14:58Z |

The title was **verified live, not inferred** from any older file.

### 1.4 Harnesses and research assets located

`promotion_v0.8.4/{build_v084,verify_v084,make_v084_artifacts}.py` ·
`phase11_week0_dryrun/week0_dryrun.py` · `validate_schedule.py` ·
`phase8_4_qb_monitoring/scripts/{pipeline_lib,build_qb_candidate,apply_pending_qb_resolutions,verify_qb_candidate,test_pipeline,due_this_sweep}.py`

### 1.5 ⚠️ MISSING INPUT — reported, not improvised around

**`2026_NCAAF_QB_Settled_Starters_Update_2026-08-19.docx` DOES NOT EXIST.**

A filesystem-wide search found **no file of that name, and no `.docx` file anywhere** on
this machine — not in the repository, not in the session scratchpad.

The task's stop condition is scoped to the authoritative **handoff or workbook**, and
both were located, so this pass proceeded. But the consequence must be stated plainly:
**any settled-starter conclusion that exists only inside that document is not
incorporated here.** Every finding below rests on independent research against the
stated source hierarchy. If that document contains additional settled starters, this
report will under-count activations. Please supply it if you want it reconciled.

**Handoff filename note.** The brief names `TTW_v084_Promotion_20260821.md`. The file
on disk is `TTW_v084_Promotion_2026-08-21.md` (hyphenated), in the session scratchpad.
Content verified as the August 21 promotion report. Treated as the same document.

---

## 2. TWO DISCREPANCIES BETWEEN THE BRIEF AND THE VERIFIED STATE

Both are reported rather than silently reconciled.

### 2.1 Syracuse is **not** a confirmed starter in the model

The brief states: *"Syracuse: Steve Angeli was previously confirmed. Verify there has
been no reversal, but do not count him as a new activation."*

**The workbook does not carry Syracuse as confirmed.** Row 69 reads confidence **`L`**,
baseline blank, active `Steve Angeli`, status **UNCERTAIN**.

Syracuse was never activated. The August 21 pass explicitly recommended against it, and
the August 21 closeout rejected an apparent naming as a **stale 2025 article** — one
that named Angeli starter for a "Week 1 game against Tennessee on August 30," which was
the 2025 opener. The 2026 Week 1 game is **Charleston Southern… no — New Hampshire at
Syracuse on 2026-09-05**, per the workbook schedule.

Today's research reaches the same conclusion: Angeli is healthy and taking first-team
reps, no competition is described, but **no formal 2026 naming and no official depth
chart could be located**. The only source carrying a Fran Brown attribution to the job
is an SB Nation team blog, which the stated hierarchy excludes.

**Syracuse is classified UNRESOLVED.** There is nothing to reverse, because there was
never an activation.

### 2.2 The three carried-forward record corrections are a different set than described

The brief describes Fresno State plus *"the other two candidate-record corrections
documented in the August 21 handoff."*

The August 21 handoff documented three corrections: **Northern Illinois, Tulane and
Colorado State.** Fresno State was not among them — its correction was applied to the
**live sheet** at an earlier pass.

Current state of all four:

| Team | Row | Repo v0.8.4 | Live master | Status |
|---|:--:|---|---|---|
| Northern Illinois | 123 | ✅ corrected (M→L, four-way list) | ❌ not yet applied | **open on the live sheet** |
| Tulane | 91 | ✅ corrected (four-way list) | ❌ not yet applied | **open on the live sheet** |
| Colorado State | 74 | ❌ unchanged **by your instruction** | ❌ unchanged | **still open, both sides** |
| **Fresno State** | 75 | ❌ **still stale** | ✅ corrected earlier | **open in the repo** |

**Braden Atkinson check.** The brief warns he must not remain listed as a Fresno State
candidate. He is **not** listed there — Fresno State row 75 reads
`Open (three-way battle into August)`. Atkinson appears on **Oregon State row 76**
(`Maalik Murphy (leader; Braden Atkinson pushing…)`), which matches the brief's
statement that he is at Oregon State. No cross-team contamination exists.

---

## 3. EXECUTIVE TOTALS

Review population: the **34 teams** carrying QB UNCERTAIN in v0.8.4. None was dropped.

| Outcome | Count |
|---|:--:|
| **ACTIVATE CANDIDATE** | **1** — Georgia Southern |
| **MEDICALLY GATED** | **1** — Texas Tech |
| **UNRESOLVED** | **32** |
| **RECORD CORRECTION** | **1 row** — Fresno State *(inside the 32; a data-quality change, not an activation)* |
| **NO CHANGE** | **1** — Stanford *(outside the 34; verified no reversal)* |

1 + 1 + 32 = **34.** Population reconciles.

**Projected census if the single activation is approved:**

| | Now | After |
|---|:--:|:--:|
| QB status | 104 OK / 34 UNCERTAIN | **105 OK / 33 UNCERTAIN** |
| Confidence | 69 H / 40 M / 29 L | **69 H / 40 M / 29 L — unchanged** |

Georgia Southern already carries `M` with blank numerical values, so writing 0/0 clears
the gate without moving any confidence code.

---

## 4. TEAM-BY-TEAM EVIDENCE TABLE — FULL POPULATION (34)

Verification date/time for every row below: **2026-08-24 10:02:59 EDT**.

| # | Team | Row | Prior status | Candidates / player | Current evidence | Decision | Conf. |
|:--:|---|:--:|:--:|---|---|---|:--:|
| 1 | **Georgia Southern** | 131 | M / UNCERTAIN | **Max Johnson** | **ESPN, 2026-08-23: "Max Johnson to start at quarterback for Georgia Southern." Pete Thamel: "Sources: Georgia Southern has named veteran Max Johnson the school's starting quarterback."** Corroborated internally — Thamel's detail that Johnson debuts vs Charleston Southern then faces Clemson in Week 2 matches the workbook schedule exactly. | **ACTIVATE CANDIDATE** | **M** |
| 2 | **Texas Tech** | 52 | H / UNCERTAIN | Will Hammond | Identity settled. Clearance still only forward-looking: McGuire, *"August 21 is nine months, so he should be released August 21."* ESPN remains conditional: *"Week 1 starter **if cleared**."* **No team medical release located as of 10:02 EDT.** | **MEDICALLY GATED** | H |
| 3 | **Fresno State** | 75 | L / UNCERTAIN | Khristian Martin vs Jayden Mandal | Two-way battle; Entz deciding late in camp. No 2026 naming. Repo record still reads the stale `Open (three-way battle into August)`. | **RECORD CORRECTION** + UNRESOLVED | L |
| 4 | Memphis | 85 | L | Stokes vs Air Noland | Huff named a starter **to the team** Sunday 2026-08-23 but will not announce publicly: *"You guys won't know until they flip the coin."* | UNRESOLVED | L |
| 5 | UNLV | 125 | L | Jackson Arnold vs Alex Orji | Mullen has not announced; *"Maybe we'll play both against Memphis."* | UNRESOLVED | L |
| 6 | Washington State | 80 | L | Pinnick / Eshelman / Dugger | Spokesman-Review 2026-08-21: WSU **to announce by Monday 2026-08-24**. Pinnick the frontrunner. **No announcement located as of 10:02 EDT.** | UNRESOLVED | L |
| 7 | Syracuse | 69 | L | Steve Angeli | Healthy, first-team reps, no competition described — but no formal 2026 naming or official depth chart. See §2.1. | UNRESOLVED | L |
| 8 | Colorado State | 74 | L | Hejny / Farrar / Darius Curry | Mora will not name early. Three-way, incl. returning part-time starter Curry. Correction carried forward, unapplied per instruction. | UNRESOLVED | L |
| 9 | Northern Illinois | 123 | L | Davidson / Macon / Hamric / Dickens | No starter named; interim HC Rob Harley after Hammock left for the NFL. Repo corrected in v0.8.4; live sheet not yet. | UNRESOLVED | L |
| 10 | Tulane | 91 | L | Semonza / Chriss-Gremillion / Johnson / Bruno | Four-way; Will Hall yet to select. Repo corrected in v0.8.4; live sheet not yet. | UNRESOLVED | L |
| 11 | Alabama | 6 | L | Keelon Russell vs Austin Mack | Projection sources only; described as a coin flip. | UNRESOLVED | L |
| 12 | Arkansas | 7 | L | KJ Jackson / AJ Hill | No naming located. | UNRESOLVED | L |
| 13 | Florida | 9 | L | Aaron Philo vs Tramell Jones Jr. | Official Florida release 2026-08-17: *"The Competition Continues."* | UNRESOLVED | L |
| 14 | Tennessee | 18 | L | Faizon Brandon + three others | No naming located. | UNRESOLVED | L |
| 15 | Vanderbilt | 21 | L | Jared Curtis | Frontrunner language only. | UNRESOLVED | L |
| 16 | Iowa | 24 | L | Hecklinski / Hank Brown | Still open in camp. | UNRESOLVED | L |
| 17 | Nebraska | 29 | L | Anthony Colandrea | Expected starter; **no formal declaration**. | UNRESOLVED | L |
| 18 | Rutgers | 35 | M | Lonergan vs Surace | No naming. A conflicting third name surfaced in one low-grade source and is **not** used. | UNRESOLVED | M |
| 19 | Kansas | 48 | L | Ballard vs Marshall | Outlets disagree on the leader. | UNRESOLVED | L |
| 20 | Oregon State | 76 | M | Maalik Murphy; Atkinson pushing | 2026-08-11: *"far from being named."* | UNRESOLVED | M |
| 21 | South Florida | 89 | L | Kromenhoek / Van Buren Jr. / Cooper | **No qualifying current reporting located.** | UNRESOLVED | L |
| 22 | Liberty | 99 | L | Purdie / Henderson / Vasko | Pre-camp projected chart shows an **OR** — excluded by standard. | UNRESOLVED | L |
| 23 | Akron | 105 | L | Poffenbarger / Roggow | No naming. | UNRESOLVED | L |
| 24 | Ball State | 106 | L | Keldric Luster | **No qualifying current reporting located.** | UNRESOLVED | L |
| 25 | Buffalo | 108 | L | Wright / Cumbie / Hough | No naming. | UNRESOLVED | L |
| 26 | Central Michigan | 109 | L | Flores / Beamon / Glasser | **No qualifying current reporting located.** | UNRESOLVED | L |
| 27 | Miami (OH) | 112 | L | McComb / Gotkowski / Cale | No 2026 naming; 2025 designations rejected. | UNRESOLVED | L |
| 28 | Ohio | 113 | M | Nick Poulos | Leader, not named. | UNRESOLVED | M |
| 29 | Nevada | 120 | L | Open; Carter Jones returning | No naming. | UNRESOLVED | L |
| 30 | Appalachian State | 128 | L | Singleton / Hasselbeck | "Likely candidate" language only. | UNRESOLVED | L |
| 31 | Arkansas State | 129 | L | Owens / Dickey / St. Hilare / Haly | "Favorite" language only. | UNRESOLVED | L |
| 32 | Coastal Carolina | 130 | L | Deuce Bailey among candidates | Official CCU release 2026-08-10: competition ongoing. | UNRESOLVED | L |
| 33 | Southern Miss | 139 | L | White / Hampton / Lyddy | No naming. | UNRESOLVED | L |
| 34 | UConn | 143 | L | Room in flux after HC departure | Camp opened 2026-08-09 with an open battle. | UNRESOLVED | L |

**Outside the population — verified for reversal only:**

| Team | Row | State | Finding |
|---|:--:|---|---|
| **Stanford** | 68 | H / **OK** | Davis Warren remains the named starter. **No reversal, no injury, no competition reopened.** | **NO CHANGE** |

**Absence of evidence, stated plainly.** For **South Florida, Ball State and Central
Michigan** no qualifying current reporting through 10:02 EDT was located. These are
recorded as an absence of evidence, **not** as "verified open."

---

## 5. ACTIVATION-CANDIDATE PACKET

### GEORGIA SOUTHERN — row 131 — recommend **ACTIVATE at M**

| Field | Value |
|---|---|
| Team | Georgia Southern Eagles |
| Player | **Max Johnson** |
| Prior status | `M` / UNCERTAIN, active text `Max Johnson (leader; Turner Helton competing)` |
| Source title | *Max Johnson to start at quarterback for Georgia Southern* (ESPN); Pete Thamel report |
| Direct URL | `https://www.espn.com/college-football/story/_/id/49704180/max-johnson-start-quarterback-georgia-southern` · `https://x.com/PeteThamel/status/2091599767289688141` |
| Publication date | **2026-08-23** |
| Verification date/time | 2026-08-24 10:02:59 EDT |
| Confidence | **M** |
| Reasoning | A credentialed national reporter directly attributing a naming — *"Sources: Georgia Southern has named veteran Max Johnson the school's starting quarterback."* **M rather than H** because this is sourced reporting, not an official school release, matching the precedent set when North Carolina was activated at M on a Thamel report. Independently corroborated by the workbook's own schedule: Thamel's Week 1 / Week 2 detail (Charleston Southern, then at Clemson) matches exactly. |

### Proposed cell changes — QB VALUES row 131

| Cell | Current value | Proposed value | Change type |
|---|---|---|---|
| `C131` | *(blank)* | `Max Johnson` | text |
| `D131` | *(blank)* | `0` | **numerical (zero only)** |
| `E131` | `Max Johnson (leader; Turner Helton competing)` | `Max Johnson` | text |
| `F131` | *(blank)* | `0` | **numerical (zero only)** |
| `H131` | `M` | `M` — **unchanged** | — |
| `I131` | Athlon/Underdog Sun Belt previews | ESPN 2026-08-23 + Thamel URL above | metadata |
| `J131` | `2026` | `2026` — **must not be rewritten** | — |
| `K131` | prior date | `2026-08-24` | metadata |
| `L131` | prior note | evidence note per §5 | text |
| **`G131`** | *(formula)* | **DO NOT WRITE — formula** | formula |
| **`M131`** | *(formula)* | **DO NOT WRITE — formula** | formula |

**The only numerical values proposed anywhere in this report are the two zeros above**,
which are the deviation-only convention. QB delta remains **0**. No rating, weight, HFA,
adjustment, market line or model output changes.

---

## 6. RECORD-CORRECTION PACKET

### 6.1 FRESNO STATE — row 75 — **apply**

Data-quality change only. **Confidence stays `L`; Fresno State remains UNCERTAIN.**

| Cell | Current value | Proposed value | Change type |
|---|---|---|---|
| `E75` | `Open (three-way battle into August)` | `Open (Khristian Martin / Jayden Mandal)` | text |
| `I75` | Athlon/ESPN/CBS Pac-12 previews | 247Sports fall-camp report / MWC Connection, August 2026 | metadata |
| `K75` | `2026-08-03` | `2026-08-24` | metadata |
| `L75` | prior note | note recording the two-way battle and that Braden Atkinson is at **Oregon State**, not Fresno State | text |
| `H75` | `L` | `L` — **unchanged** | — |
| `D75` / `F75` | blank | **blank — unchanged** | — |

This aligns the repository artifact with the live sheet, which already carries the
corrected text.

### 6.2 Carried forward — NOT applied in this pass

| Team | Row | What remains | Where |
|---|:--:|---|---|
| Northern Illinois | 123 | `E`, `H` (M→L), `I`, `K`, `L` | **live sheet only** — repo already correct |
| Tulane | 91 | `E`, `I`, `K`, `L` | **live sheet only** — repo already correct |
| Colorado State | 74 | `E` → `Open (Hejny / Farrar / Darius Curry)`, plus `I`/`K`/`L` | **both** — deliberately unapplied per your standing instruction |

---

## 7. MODEL CONTROLS — EXPLICIT CONFIRMATION

Confirmed for this pass:

- **No write of any kind to the live Google Sheet.** Metadata was read once to verify the title; no cell, range, property or permission was touched.
- **No workbook was rebuilt, replaced or modified.** `promotion_v0.8.4/…v0.8.4_AUTHORITATIVE.xlsx` remains `ed5d3b3d…a892`.
- **No formula changed.** `G` and `M` on every QB VALUES row remain formulas; `J` remains `2026`.
- **No rating, quarterback point value, adjustment, weight, HFA, setting, date, timezone, schedule, market line or model output changed.**
- **No nonzero quarterback value is proposed.** The only numerics proposed are two zeros on Georgia Southern.
- **No betting market was used as a team rating.**
- **Population baseline preserved and re-verified from the workbook:** 138 teams · 888 games · 761 FBS-vs-FBS · 127 FCS-involved no-play · 0 unresolved BLOCK classifications.
- Candidate-record corrections are treated as **data-quality changes only**, carrying no quarterback-value or rating implication.

---

## 8. SOURCE-DISCIPLINE NOTES

**Two stale-2025 traps caught and rejected this pass:**

1. **Fresno State / E.J. Warner.** A CBS47 item headlined *"E.J. Warner named Fresno State's starting Quarterback"* is dated **2026-08-11 in appearance but is the 2025 announcement** — it names Warner beating out **Carson Conklin**, who the workbook lists as Sacramento State's quarterback. Rejected.
2. **Syracuse / Angeli.** Re-confirmed that the apparent naming for a *"Week 1 game against Tennessee on August 30"* is the **2025** opener. The 2026 Week 1 game is New Hampshire at Syracuse on 2026-09-05 per the workbook schedule.

**Rejected as non-qualifying under the stated hierarchy:** ESPN and Athlon
"predicting starting quarterbacks" features; Ourlads, puntandrally, cfbdepth and
gunslingerbuzz projected charts; message-board threads; "expected"/"likely"/"favorite"
framing; first-team practice reps; and any OR depth-chart listing.

**Unresolved conflicts, surfaced not silenced:** Kansas — outlets disagree on whether
Ballard or Marshall leads. Rutgers — a third name appeared in one low-grade source
against the workbook's Lonergan/Surace; not used, team left unresolved.

---

## 9. RECOMMENDATIONS — AWAITING EXPLICIT APPROVAL

| # | Item | Recommendation |
|:--:|---|---|
| 1 | **Georgia Southern — Max Johnson** | **APPROVE activation at M.** Nine cells on row 131, two of them zeros. Moves the census to 105 OK / 33 UNCERTAIN with no confidence-code change. |
| 2 | **Fresno State — record correction** | **APPROVE.** Four cells on row 75. Text/metadata only; stays `L` / UNCERTAIN. |
| 3 | **Texas Tech** | **HOLD.** Do not activate. Clearance unverified. Recheck: a Texas Tech team medical release, a direct McGuire confirmation, official game notes, or a Week 1 depth chart listing Hammond at QB1 with no injury limitation and no "OR". |
| 4 | **Washington State** | **RECHECK TODAY.** WSU said it would announce by Monday 2026-08-24. Nothing published as of 10:02 EDT. Highest-probability next activation. |
| 5 | **Memphis / UNLV** | **HOLD through kickoff.** Both coaches on record that no starter will be revealed before the game. Expect these to remain UNCERTAIN through Week 0. |
| 6 | **Colorado State** | **DECISION NEEDED.** The correction has now been carried forward twice unapplied. Either approve it or retire it so it stops recurring. |
| 7 | **NIU / Tulane on the live sheet** | **OWNER ACTION.** The repo is correct; the live master is not. The connector cannot write cells. |
| 8 | **Missing `.docx`** | **SUPPLY IF IT MATTERS.** Any settled starter unique to that document is not reflected here. |

---

## 10. GIT STATUS AND FILES

**Final `git status --porcelain`:**

```
?? TTW_v084_QB_Closeout_20260824.md
```

| File | Action |
|---|---|
| `TTW_v084_QB_Closeout_20260824.md` | **created** (this report) |

**Nothing else was created, modified or deleted.** The August 21 handoff was **not
overwritten**. HEAD remains `14cf041`; no commit, no push, no merge, no branch change.

⚠️ This report is currently **untracked and uncommitted**. The August 21 handoff lives
only in the session scratchpad, which is ephemeral. Say the word and I will commit this
file so it survives; I have not done so because the brief ends by directing me to wait
for explicit approval.
