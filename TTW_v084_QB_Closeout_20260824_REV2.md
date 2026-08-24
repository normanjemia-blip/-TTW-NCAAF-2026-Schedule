# TTW COLLEGE FOOTBALL POWER RATINGS — QB CLOSEOUT, 24 AUGUST 2026 (REV 2)

## SUPERSEDES `TTW_v084_QB_Closeout_20260824.md`

**Current research cutoff:** Monday, **2026-08-24 10:49:36 EDT** (America/New_York)
**Supersession reason:** the required authoritative input
`2026_NCAAF_QB_Settled_Starters_Update_2026-08-19.docx` was unavailable at the first
pass and has now been supplied and read in full. Re-sweeping to the new cutoff also
surfaced **three namings that post-date the first report.**

**Task type:** READ-ONLY. No workbook change, no live-Sheet write, nothing promoted.

---

## 1. THE AUTHORITATIVE INPUT — READ IN FULL

| | |
|---|---|
| File | `2026_NCAAF_QB_Settled_Starters_Update_20260819.docx` |
| SHA-256 | `52f74de820926f08946ec5d4f9b9bd46bf17b2c58851943ba7d1f1f83ede3947` |
| Read | 28 paragraphs + 2 tables (4-row settled table, 35-row open table) — **complete** |
| Its research cutoff | **2026-08-19** |
| Its scope | the 37-team post-UNC UNCERTAIN list |

**Its decision rule, verbatim:** *"Formal coach/team designation **or an unequivocally
retained incumbent**; projections and first-team reps do not count."*

**Its bottom line:** three of 37 have a settled starter identity — **Stanford (Warren),
Syracuse (Angeli), Texas Tech (Hammond, availability gated)**. The other 34 stay on the
recheck list.

### 1.1 What this changed in my analysis — and a correction I owe you

**Syracuse: I was wrong on 2026-08-24 (Rev 1), and the document shows why.**

Rev 1 classified Syracuse UNRESOLVED because I could not locate a formal 2026 naming,
and the only Fran Brown attribution I found was an SB Nation team blog, which my source
hierarchy excludes. **Two things I did not have:**

1. **An official Syracuse Athletics source** — the Aug 4 camp preview, source class 1.
2. **The explicit "retained incumbent" clause** in the governing decision rule.

The document records that Angeli's 2025 starting job carried into 2026, that the
official camp preview has him healthy and returning, and — decisively — that **the live
competition is for the backup role.** Under the stated rule that is a settled identity,
not an open battle. My Rev 1 reasoning applied a "formal naming" test to a case the rule
resolves as a retained incumbent.

**Syracuse is corrected to ACTIVATE at H.** Health monitoring is retained as a note, not
as a competition flag, exactly as the document directs.

### 1.2 Where the document is now superseded by events

The document's cutoff is 2026-08-19; the current cutoff is five days later. Three of its
"still open" rows have since resolved, and two of those were already promoted:

| Team | Document (Aug 19) | Reality at current cutoff |
|---|---|---|
| Missouri State | open — *"Casey Woods still has not named a starter"* | **Promoted 2026-08-21** — Skyler Locklear, H, now OK |
| San Jose State | open — three-way, *"no naming found"* (July 31) | **Promoted 2026-08-21** — Luke Weaver, H, now OK |
| Georgia Southern | open — *"Coach said Johnson would start 'if today'; not a final naming"* (July 17) | **Named 2026-08-23** — see §4.4 |
| Alabama | open — *"Ongoing; no staff winner named"* (Aug 14) | **Named 2026-08-22** — see §4.2 |
| Tennessee | open — *"Current preview still frames an either/or starter"* (Aug 18) | **Named 2026-08-24** — see §4.3 |

This is not a defect in the document; it is a five-day-old cutoff behaving correctly.
**Both the document and live research were required — neither alone was sufficient.**

---

## 2. RESEARCH STATUS vs WORKBOOK-APPLICATION STATUS

These are reconciled separately, as instructed.

| Team | Research status (evidence) | Workbook status (v0.8.4) | Reconciled action |
|---|---|---|---|
| **Stanford** | Settled since 2026-08-18 | **Already OK**, H, 0/0 | **NO CHANGE** — verified, no reversal |
| **Syracuse** | Settled (retained QB1) since the Aug 4 official preview | `L` / UNCERTAIN, values blank | **ACTIVATE** — workbook lags research |
| **Texas Tech** | Identity settled; availability unresolved | `H` / UNCERTAIN, values blank | **HOLD** — gate is correct as-is |
| **Alabama** | Settled 2026-08-22 | `L` / UNCERTAIN | **ACTIVATE** |
| **Tennessee** | Settled 2026-08-24 | `L` / UNCERTAIN | **ACTIVATE** |
| **Georgia Southern** | Settled 2026-08-23 | `M` / UNCERTAIN | **ACTIVATE** |
| **Fresno State** | Open; candidate field stale | `L` / UNCERTAIN, stale text | **RECORD CORRECTION**, stays UNCERTAIN |

**The key distinction:** Stanford's research and workbook status agree. Syracuse's do
not — the research settled on Aug 4 and the workbook never caught up. That gap is the
whole reason this reconciliation was needed.

---

## 3. FULLY RECONCILED POPULATION TOTALS

Population: the **34** teams carrying QB UNCERTAIN in v0.8.4. None dropped.

| Outcome | Count | Teams |
|---|:--:|---|
| **ACTIVATE CANDIDATE** | **4** | Syracuse, Alabama, Tennessee, Georgia Southern |
| **MEDICALLY GATED** | **1** | Texas Tech |
| **UNRESOLVED** | **29** | balance of the population |
| **RECORD CORRECTION** | **1 row** | Fresno State *(inside the 29)* |
| **NO CHANGE** | **1** | Stanford *(outside the 34)* |

4 + 1 + 29 = **34.** Reconciles.

### Resulting census

| | Current (v0.8.4) | After the 4 activations |
|---|:--:|:--:|
| QB status | 104 OK / 34 UNCERTAIN | **108 OK / 30 UNCERTAIN** |
| Confidence | 69 H / 40 M / 29 L | **72 H / 40 M / 26 L** |
| Total | 138 | **138** ✓ |
| Nonzero QB values | 0 | **0** |

Derivation: Syracuse, Alabama and Tennessee each move `L → H` (−3 L, +3 H); Georgia
Southern stays `M`. All four move UNCERTAIN → OK. Texas Tech and Fresno State remain
UNCERTAIN.

---

## 4. ACTIVATION PACKET — EXACT CELLS

**Protected on every row below — never written:** `QB VALUES!G{row}` (QB delta formula),
`QB VALUES!M{row}` (QB status formula). `J{row}` already reads `2026` and must not be
rewritten.

### 4.1 SYRACUSE — row 69 — **ACTIVATE, confidence H**

Prior status: `L` / UNCERTAIN · Proposed: `H` / OK

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `C69` | *(blank)* | `Steve Angeli` | text |
| `D69` | *(blank)* | `0` | **numerical** |
| `E69` | `Steve Angeli` | `Steve Angeli` — unchanged | text |
| `F69` | *(blank)* | `0` | **numerical** |
| `H69` | `L` | `H` | metadata |
| `I69` | SI ACC projections, May 14 2026 | Syracuse Athletics official camp preview, 2026-08-04; position review 2026-08-17; per authoritative research update 2026-08-19 | metadata |
| `K69` | `2026-08-04` | `2026-08-24` | metadata |
| `L69` | prior 7D.5 note | retained-QB1 note incl. post-Achilles health monitor | text |

**Evidence:** Syracuse Athletics official camp preview (2026-08-04) — Angeli healthy and
returning; position review (2026-08-17) — the starting job has remained his and the live
competition is for the **backup** role. Corroborating: Spectrum/AP 2026-08-19,
*"Angeli is back and healthy"*, no competition described, transfers added as depth
*"in the event Angeli goes down again."*
URL: `https://spectrumlocalnews.com/nys/central-ho/news/2026/08/19/with-qb-steve-angeli-healthy--fran-brown-coached-syracuse-seeks-to-rebound-from-3-9-season`
**Confidence H** — retained incumbent supported by an official team source, which the
governing rule treats as equivalent to a formal naming.
**Health note stays separate from competition status**, as directed.

### 4.2 ALABAMA — row 6 — **ACTIVATE, confidence H**

Prior status: `L` / UNCERTAIN · Proposed: `H` / OK

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `C6` | *(blank)* | `Keelon Russell` | text |
| `D6` | *(blank)* | `0` | **numerical** |
| `E6` | `Keelon Russell` | `Keelon Russell` — unchanged | text |
| `F6` | *(blank)* | `0` | **numerical** |
| `H6` | `L` | `H` | metadata |
| `I6` | SI SEC QB projections | CBS Sports / USA TODAY, 2026-08-22 | metadata |
| `K6` | `2026-08-04` | `2026-08-24` | metadata |
| `L6` | prior note | naming note | text |

**Evidence:** Head coach Kalen DeBoer selected Russell over Austin Mack after the second
fall scrimmage; confirmed by USA TODAY Sports on Saturday **2026-08-22**. CBS Sports:
*"Alabama names Keelon Russell starting QB."*
URL: `https://www.cbssports.com/college-football/news/alabama-keelon-russell-starting-qb-battle-austin-mack-kalen-deboer-sec/`
**Confidence H** — the naming is attributed to the head coach as a decision made and
communicated, and is carried by multiple national outlets.

### 4.3 TENNESSEE — row 18 — **ACTIVATE, confidence H**

Prior status: `L` / UNCERTAIN · Proposed: `H` / OK

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `C18` | *(blank)* | `Faizon Brandon` | text |
| `D18` | *(blank)* | `0` | **numerical** |
| `E18` | `Faizon Brandon` | `Faizon Brandon` — unchanged | text |
| `F18` | *(blank)* | `0` | **numerical** |
| `H18` | `L` | `H` | metadata |
| `I18` | SI SEC QB projections | iHeart syndicated wire report, 2026-08-24 | metadata |
| `K18` | `2026-08-04` | `2026-08-24` | metadata |
| `L18` | prior note | naming note | text |

**Evidence:** Head coach Josh Heupel announced Brandon as the starter **in a team meeting
on Monday 2026-08-24** — verified by direct fetch as an official team announcement.
Brandon won a three-way race over George MacIntyre and Colorado transfer Ryan Staub, and
is Tennessee's first true freshman to start an opener since 2004.
URL: `https://ticket760.iheart.com/content/2026-08-24-volunteers-name-true-freshman-starting-qb/`
**Confidence H** — formal head-coach/team announcement. **This naming happened today and
post-dates both the authoritative document and Rev 1.**

### 4.4 GEORGIA SOUTHERN — row 131 — **ACTIVATE, confidence M**

Prior status: `M` / UNCERTAIN · Proposed: `M` *(unchanged)* / OK

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `C131` | *(blank)* | `Max Johnson` | text |
| `D131` | *(blank)* | `0` | **numerical** |
| `E131` | `Max Johnson (leader; Turner Helton competing)` | `Max Johnson` | text |
| `F131` | *(blank)* | `0` | **numerical** |
| `H131` | `M` | `M` — **unchanged** | — |
| `I131` | ESPN/Athlon Sun Belt previews | ESPN + Pete Thamel, 2026-08-23 | metadata |
| `K131` | `2026-08-04` | `2026-08-24` | metadata |
| `L131` | prior note | naming note | text |

**Evidence:** ESPN, *"Max Johnson to start at quarterback for Georgia Southern"*; Pete
Thamel: *"Sources: Georgia Southern has named veteran Max Johnson the school's starting
quarterback."* Published **2026-08-23**.
URL: `https://www.espn.com/college-football/story/_/id/49704180/max-johnson-start-quarterback-georgia-southern`
**Independently corroborated by the workbook itself:** Thamel's detail that Johnson
debuts against Charleston Southern then faces Clemson in Week 2 matches the workbook
schedule exactly (`wk1 2026-09-05 Charleston Southern @ Georgia Southern` [FCS — NO PLAY];
`wk2 2026-09-12 Georgia Southern @ Clemson`).
**Confidence M, not H** — this is a reporter's sourced claim, not a team/coach
announcement. This matches the precedent set when North Carolina was activated at M on a
Thamel "sources" report. Also supersedes the authoritative document, which as of July 17
recorded only *"would start 'if today'"*.

### 4.5 Justification for every numerical entry

**Eight numerical values are proposed. All eight are the integer `0`.**

| Cells | Value | Justification |
|---|:--:|---|
| `D69`,`F69` · `D6`,`F6` · `D18`,`F18` · `D131`,`F131` | `0` | **Deviation-only convention.** `QB VALUES!G = F − D`, so `0 − 0 = 0`: the QB delta is **exactly zero** and `ENGINE!M` contributes **nothing** to any game. The zeros are not a rating of the quarterback — they record that the active starter **is** the quarterback the preseason rating already assumed, so no deviation applies. A blank leaves `G` blank, which forces status UNCERTAIN; a zero clears the gate while moving no number. **This is why activation is numerically inert.** |

**No nonzero QB value is proposed anywhere in this report.** No rating, weight, HFA,
adjustment, setting, schedule, market line or model output is touched.

---

## 5. MEDICAL GATE

### TEXAS TECH — row 52 — **HOLD. No activation.**

Identity is resolved and already recorded correctly: `H` confidence, `Will Hammond` in
both baseline and active. `D52`/`F52` are blank, which is what holds the gate, and status
is UNCERTAIN. **The record needs no change.**

Availability remains unresolved at the current cutoff. The only clearance statement is
still forward-looking — McGuire: *"August 21 is nine months, so he should be released
August 21."* ESPN remains conditional: *"Week 1 starter **if cleared**."* The strongest
current evidence is participation in a closed scrimmage (KCBD, 2026-08-15) with positive
McGuire comment — **practice participation, not a team medical release.**

**Required to lift the gate:** an official Texas Tech statement, a direct McGuire
confirmation of full clearance, official game notes, or a Week 1 depth chart listing
Hammond at QB1 with no injury limitation and no "OR". Texas Tech does not play in Week 0.

---

## 6. THE FOUR RECORD-CORRECTION THREADS — RECONCILED INDEPENDENTLY

| # | Team | Row | Repo (v0.8.4) | Live Sheet | Action this pass |
|:--:|---|:--:|---|---|---|
| 1 | **Fresno State** | 75 | ❌ **stale** — `Open (three-way battle into August)` | ✅ already corrected | **PROPOSE repo correction** (§6.1) |
| 2 | **Northern Illinois** | 123 | ✅ corrected in v0.8.4 — `M→L`, four-way list | ❌ **not applied** | **owner action on the live Sheet** |
| 3 | **Tulane** | 91 | ✅ corrected in v0.8.4 — four-way list | ❌ **not applied** | **owner action on the live Sheet** |
| 4 | **Colorado State** | 74 | ❌ unapplied **by standing instruction** | ❌ unapplied | **decision needed** (§6.2) |

### 6.1 Fresno State — row 75 — propose

Data-quality only. **`H75` stays `L`. Fresno State remains UNCERTAIN.**

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `E75` | `Open (three-way battle into August)` | `Open (Khristian Martin / Jayden Mandal)` | text |
| `I75` | Athlon/ESPN/CBS Pac-12 previews | authoritative research update 2026-08-19; 247Sports fall-camp report | metadata |
| `K75` | `2026-08-03` | `2026-08-24` | metadata |
| `L75` | prior note | two-way race; **Braden Atkinson is at Oregon State, not Fresno State** | text |
| `D75` / `F75` | blank | **blank — unchanged** | — |

**Braden Atkinson verified.** He is **not** listed under Fresno State — row 75 reads
`Open (three-way battle into August)`. He appears on **Oregon State row 76**
(`Maalik Murphy (leader; Braden Atkinson pushing…)`), which the authoritative document
confirms (`Oregon State | Maalik Murphy vs. Braden Atkinson`). **No cross-team
contamination exists in either the repo or the document.**

### 6.2 Colorado State — row 74 — decision needed, plus a source conflict

Carried forward unapplied for a third pass. **There is also an unresolved conflict:**

- My 2026-08-21 research found a **three-way** race including returning part-time starter **Darius Curry**.
- The authoritative document records a **two-way** race: `Hauss Hejny vs. K'saan Farrar` (Aug 19 check).

**I am not selecting between these.** Colorado State stays UNRESOLVED either way, and no
correction is proposed until you rule. If you want it applied, tell me which candidate
field is correct.

### 6.3 Observation — further candidate-field drift, NOT proposed

The authoritative document lists candidate fields that differ from the workbook on
several other teams — Nevada (`Duncan / Jones / Bianco` vs `Open competition`), UConn
(`Merklinger / Osborne / McDonald` vs `Unverified`), Ball State (`Luster vs Mizzell`),
Arkansas State (`Crawford` and spelling `St-Hilaire`), Ohio (`Poulos vs Vezza`),
Tennessee, Vanderbilt, Nebraska and Alabama (all listed as two-way where the workbook
names one). **None is proposed here** — you scoped this pass to four threads. Flagging so
the drift is on record, not to expand scope.

---

## 7. UNRESOLVED — 29 TEAMS

All verified against the authoritative document **and** re-swept to 2026-08-24 10:49 EDT.

| Team | Row | Race | Why it stays open |
|---|:--:|---|---|
| Rutgers | 35 | Lonergan vs Surace | **Schiano has still not named one** — *"I don't know exactly what day… it'll be soon."* Explicitly checked per your list |
| Washington State | 80 | Pinnick / Eshelman / Dugger | **Announcement promised by today.** Nothing published as of 10:49 EDT. Pinnick the frontrunner. Explicitly checked per your list |
| Memphis | 85 | Stokes vs Air Noland | Named to the team 2026-08-23, **withheld publicly until kickoff** |
| UNLV | 125 | Arnold vs Orji | Mullen: both will play; competition continues |
| Fresno State | 75 | Martin vs Mandal | Two-way; no winner announced *(record correction §6.1)* |
| Colorado State | 74 | Hejny vs Farrar *(± Curry)* | No naming; source conflict §6.2 |
| Northern Illinois | 123 | Dickens / Davidson / Macon / Hamric | Favored ≠ declared; interim HC Rob Harley |
| Tulane | 91 | Semonza / Chriss-Gremillion / Johnson / Bruno | Four-way, too close to call |
| Arkansas | 7 | KJ Jackson vs AJ Hill | Active competition |
| Florida | 9 | Philo vs Jones Jr. | Official team story: competition continues |
| Vanderbilt | 21 | Curtis vs Berlowitz | Both still competing |
| Iowa | 24 | Hecklinski vs Hank Brown | Trending, not named |
| Nebraska | 29 | Colandrea vs TJ Lateef | Presumed, not declared |
| Kansas | 48 | Ballard vs Marshall | Leads projections only |
| Oregon State | 76 | Murphy vs Atkinson | Camp competition still live |
| South Florida | 89 | Van Buren Jr. vs Kromenhoek | Official coverage: active competition |
| Liberty | 99 | Vasko / Purdie / Henderson | Crowded battle |
| Akron | 105 | Poffenbarger vs Roggow | Projected only |
| Ball State | 106 | Luster vs Mizzell | Both expected to play |
| Buffalo | 108 | Wright / Holmes / Cumbie | No declared winner |
| Central Michigan | 109 | Flores / Glasser / Beamon | Official preview indicates shared work |
| Miami (OH) | 112 | McComb / Gotkowski / Heavner | Three-way, no decision |
| Ohio | 113 | Poulos vs Vezza | Leader, still a competition |
| Nevada | 120 | Duncan / Jones / Bianco | Three-way active |
| Appalachian State | 128 | Singleton vs Hasselbeck | No naming |
| Arkansas State | 129 | Crawford / Owens / Dickey / St-Hilaire | All four in the mix |
| Coastal Carolina | 130 | Bailey among an open room | No naming |
| Southern Miss | 139 | Lyddy / White / Hampton | Three-way |
| UConn | 143 | Merklinger / Osborne / McDonald | Three-way, no winner |

**Evidence-coverage improvement.** Rev 1 recorded three teams with *no* qualifying
source located (South Florida, Ball State, Central Michigan). The authoritative document
supplies dated checks for **all three** — Aug 4, Aug 16 and Aug 11 respectively. **That
gap is now closed; every one of the 29 has a dated basis.**

---

## 8. MODEL CONTROLS — EXPLICIT CONFIRMATION

- **No live Google Sheet write of any kind.** Metadata read once at Rev 1 to verify the title; nothing since.
- **No workbook modified.** `promotion_v0.8.4/…v0.8.4_AUTHORITATIVE.xlsx` remains `ed5d3b3d9aa3dd4f845e91688216a28276aaa0b3e4bd68ba09a9ceb96a8adaff`.
- **No formula changed.** `G` and `M` remain formulas on every row; `J` remains `2026`.
- **No rating, QB value, adjustment, weight, HFA, setting, date, timezone, schedule, market line or model output changed.**
- **No nonzero QB value proposed** — the only numerics are eight zeros, justified in §4.5.
- **Baseline preserved and re-verified from the workbook:** 138 teams · 888 games · 761 FBS-v-FBS · 127 FCS-involved no-play · 0 unresolved BLOCK.
- **Nothing promoted.** No candidate applied to repo or production.

---

## 9. RECOMMENDATIONS — AWAITING EXPLICIT APPROVAL

| # | Item | Recommendation |
|:--:|---|---|
| 1 | **Syracuse — Angeli, H** | **APPROVE.** Corrects my Rev 1 error; the retained-incumbent rule plus an official team source settles it. |
| 2 | **Tennessee — Brandon, H** | **APPROVE.** Formal Heupel team-meeting announcement, today. |
| 3 | **Alabama — Russell, H** | **APPROVE.** DeBoer's decision, 2026-08-22, multiple national outlets. |
| 4 | **Georgia Southern — Johnson, M** | **APPROVE at M.** Reporter-sourced naming; M matches the UNC precedent. H is defensible if you prefer to treat ESPN's dedicated article as equivalent to a team release — your call, and it does not change the gate. |
| 5 | **Fresno State — record correction** | **APPROVE.** Text/metadata only; stays `L` / UNCERTAIN. |
| 6 | **Texas Tech** | **HOLD.** Record is already correct. Do not activate until team medical clearance is verified. |
| 7 | **Colorado State** | **RULE ON IT.** Third pass carried forward, and my research and the authoritative document disagree on whether Darius Curry is in the race. |
| 8 | **NIU / Tulane on the live Sheet** | **OWNER ACTION.** Repo correct, live master not. The connector cannot write cells. |
| 9 | **Washington State** | **RECHECK TODAY.** Decision was promised by today and had not landed at 10:49 EDT. |

**If items 1–5 are approved, the resulting census is 108 OK / 30 UNCERTAIN and
72 H / 40 M / 26 L, with zero change to any model output.**

---

## 10. STATUS

Repository clean at `3ae4510`, 0 ahead / 0 behind. This report is a **new file**; the
Rev 1 report `TTW_v084_QB_Closeout_20260824.md` and the August 21 handoff are
**both preserved unmodified**.

Stopping here for explicit approval.
