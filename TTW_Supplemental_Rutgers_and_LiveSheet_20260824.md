# TTW — SUPPLEMENTAL PACKET + MANUAL LIVE-SHEET UPDATE LIST

**Date:** 2026-08-24 (America/New_York) · **Repo state:** v0.8.5 promoted at commit `12e88dc`
**Status:** Rutgers and Colorado State are **NOT applied** — awaiting explicit approval.
**Live Sheet:** nothing was written. The connector cannot write cells. Section D is a manual list.

---

# PART 1 — SUPPLEMENTAL PACKET (approval required)

## 1.1 RUTGERS — row 35 — proposed **ACTIVATE at M**

| Field | Value |
|---|---|
| Team | Rutgers Scarlet Knights |
| Row | **35** — located by abbreviation `RUTG`, confirmed |
| Player | **Dylan Lonergan** |
| Prior status | `M` / UNCERTAIN, active field `Dylan Lonergan (likely starter; AJ Surace competing)` |
| Proposed status | `M` / **OK** — **confidence unchanged** |
| Source | ESPN — Pete Thamel, reported Monday morning; carried by On3/The Knight Report, 247Sports, Yahoo Sports, On the Banks, Press of Atlantic City |
| URL | `https://www.on3.com/sites/the-knight-report/news/rutgers-names-dylan-lonergan-starting-quarterback-for-2026/` · `https://247sports.com/college/rutgers/article/-dylan-lonergan-named-rutgers-starting-quarterback-289146979/` |
| Publication date | **2026-08-24** |
| Verification date/time | 2026-08-24 10:49 EDT |
| Confidence | **M** |
| Justification | Reporter-sourced naming, not a team or coach announcement — the same provenance class as Georgia Southern and North Carolina, both activated at M. Lonergan won the job over AJ Surace after competing through spring and fall camp. |
| Corroboration | Reporting says Lonergan "will lead the Scarlet Knights into Week 1 against UMass." The workbook independently confirms: `wk1 2026-09-03 Massachusetts Minutemen @ Rutgers Scarlet Knights`. |

### Proposed cells

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `C35` | *(blank)* | `Dylan Lonergan` | text |
| `D35` | *(blank)* | `0` | **numerical** |
| `E35` | `Dylan Lonergan (likely starter; AJ Surace competing)` | `Dylan Lonergan` | text |
| `F35` | *(blank)* | `0` | **numerical** |
| `H35` | `M` | `M` — **unchanged** | — |
| `I35` | SI Big Ten QB projections | ESPN/Thamel 2026-08-24 + corroborating outlets | metadata |
| `J35` | `2026` | **must not be rewritten** | — |
| `K35` | `2026-08-03` | `2026-08-24` | metadata |
| `L35` | prior note | activation note | text |
| **`G35`** | *(formula)* | **DO NOT WRITE** | formula |
| **`M35`** | *(formula)* | **DO NOT WRITE** | formula |

### Justification for the two zeros

`D35 = 0` and `F35 = 0`. `QB VALUES!G = F − D`, so `0 − 0 = 0` — the delta is **exactly
zero** and `ENGINE!M` contributes **nothing** to any game. The zeros do not rate Lonergan;
they record that the confirmed starter **is** the quarterback the preseason blend already
assumed, so no deviation applies. Blank forces UNCERTAIN; zero clears the gate while
moving no number. **No nonzero value is proposed.**

## 1.2 ⚠️ CORRECTION TO YOUR PROJECTED TOTALS

You projected *"likely 72 H / 41 M / 25 L"* after Rutgers, flagged as subject to exact
workbook verification. **Verified against the workbook: that is not what happens.**

**Rutgers already carries `M`, not `L`.** Activating at M therefore changes **no**
confidence code:

| | v0.8.5 now | After Rutgers | You projected |
|---|:--:|:--:|:--:|
| QB status | 108 OK / 30 UNCERTAIN | **109 OK / 29 UNCERTAIN** | 109 OK / 29 UNCERTAIN ✅ |
| Confidence | 72 H / 40 M / 26 L | **72 H / 40 M / 26 L — unchanged** | 72 H / 41 M / 25 L ❌ |

Your **status** projection is exactly right. The confidence projection assumed Rutgers
was `L`. Population totals after Rutgers: **5 activations · 1 medically gated ·
28 unresolved** — all three exactly as you projected.

## 1.3 COLORADO STATE — row 74 — ruled, prepared, **not applied**

Your ruling is recorded: active field `Hauss Hejny vs. K'saan Farrar`; Darius Curry may
appear in a depth-room note but **not** the active competition field unless a later
qualifying source restores him. Colorado State remains UNCERTAIN.

**I did not apply it**, because the same instruction said *"apply only those approved
cells"* and Colorado State was not among items 1–5. It is held here rather than assumed.

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `E74` | `Hauss Hejny (K'saan Farrar competing)` | `Hauss Hejny vs. K'saan Farrar` | text |
| `I74` | Athlon/ESPN/CBS Pac-12 previews | authoritative research update 2026-08-19 | metadata |
| `K74` | `2026-08-03` | `2026-08-24` | metadata |
| `L74` | prior note | ruling note incl. Curry as depth-room only | text |
| `H74` | `L` | `L` — **unchanged** | — |
| `D74` / `F74` | blank | **blank — unchanged** | — |

**No numerical entry. No census effect.** Colorado State stays UNCERTAIN either way.

## 1.4 Washington State — kept unresolved, recheck outstanding

Kept UNRESOLVED as instructed. WSU said it would name a starter **by today**; nothing had
published at 10:49 EDT. Pinnick is the frontrunner. **Recheck later today** — this is the
most likely next activation.

---

# PART 2 — MANUAL LIVE-SHEET UPDATE LIST

**These changes have NOT been applied to the live Sheet.** The Google Drive connector
exposes no Sheets API — no cell write is possible — so this is a manual list for you.
Sheet: `TTW College Football Power Ratings v0.8.4 — PRODUCTION MASTER`,
ID `1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA`.

**Before you start:** make a dated working copy. **Never write `G` or `M` on any row —
they are formulas. Never rewrite `J` — it must stay `2026`.**

## A. APPROVED v0.8.5 CHANGES — apply to the live Sheet

#### Syracuse — `QB VALUES` row 69

| Cell | Set to |
|---|---|
| `C69` | `Steve Angeli` |
| `D69` | `0` |
| `E69` | `Steve Angeli` |
| `F69` | `0` |
| `H69` | `H` |
| `I69` | see verbatim text below |
| `K69` | `2026-08-24` |
| `L69` | see verbatim text below |

**`I69` verbatim:**

```
Syracuse Athletics official camp preview 2026-08-04; position review 2026-08-17; per authoritative research update 2026-08-19. Corroborated: Spectrum Local News / AP 2026-08-19 (https://spectrumlocalnews.com/nys/central-ny/news/2026/08/19/with-qb-steve-angeli-healthy--fran-brown-coached-syracuse-seeks-to-rebound-from-3-9-season)
```

**`L69` verbatim:**

```
2026-08-24 ACTIVATED (RETAINED QB1), confidence H. Angeli's 2025 starting job carried into 2026: the official Syracuse Athletics camp preview (2026-08-04) has him healthy and returning, and the 2026-08-17 position review records that the starting job has remained his with the live competition being for the BACKUP role. Qualifies under the governing rule's 'unequivocally retained incumbent' clause; absence of a new annual depth chart is not a reversal. CORRECTS the 2026-08-24 Rev 1 review, which classified this UNRESOLVED because it applied a formal-naming test and lacked the official team source. HEALTH MONITOR (separate from competition status): post-Achilles recovery from the 2025 season; monitor availability, not the job. Baseline and active values are 0/0 under the deviation-only convention: QB VALUES!G = F - D, so 0 - 0 = 0 and ENGINE!M contributes exactly nothing to any game. The zeros do not rate the quarterback - they record that the active starter IS the quarterback the preseason rating already assumed, so no deviation applies. No nonzero QB adjustment and no model change.
```

#### Alabama — `QB VALUES` row 6

| Cell | Set to |
|---|---|
| `C6` | `Keelon Russell` |
| `D6` | `0` |
| `E6` | `Keelon Russell` |
| `F6` | `0` |
| `H6` | `H` |
| `I6` | see verbatim text below |
| `K6` | `2026-08-24` |
| `L6` | see verbatim text below |

**`I6` verbatim:**

```
CBS Sports / USA TODAY, 2026-08-22 (https://www.cbssports.com/college-football/news/alabama-keelon-russell-starting-qb-battle-austin-mack-kalen-deboer-sec/)
```

**`L6` verbatim:**

```
2026-08-24 ACTIVATED, confidence H. Head coach Kalen DeBoer selected Keelon Russell over Austin Mack after the second fall scrimmage; the decision was confirmed on 2026-08-22 by USA TODAY Sports and carried by CBS Sports as 'Alabama names Keelon Russell starting QB'. A head-coach decision made and communicated, reported by multiple national outlets. Supersedes the 2026-08-19 authoritative update, which recorded the race as ongoing as of its 2026-08-14 check. Baseline and active values are 0/0 under the deviation-only convention: QB VALUES!G = F - D, so 0 - 0 = 0 and ENGINE!M contributes exactly nothing to any game. The zeros do not rate the quarterback - they record that the active starter IS the quarterback the preseason rating already assumed, so no deviation applies. No nonzero QB adjustment and no model change.
```

#### Tennessee — `QB VALUES` row 18

| Cell | Set to |
|---|---|
| `C18` | `Faizon Brandon` |
| `D18` | `0` |
| `E18` | `Faizon Brandon` |
| `F18` | `0` |
| `H18` | `H` |
| `I18` | see verbatim text below |
| `K18` | `2026-08-24` |
| `L18` | see verbatim text below |

**`I18` verbatim:**

```
Syndicated wire report, 2026-08-24 (https://ticket760.iheart.com/content/2026-08-24-volunteers-name-true-freshman-starting-qb/)
```

**`L18` verbatim:**

```
2026-08-24 ACTIVATED, confidence H. Head coach Josh Heupel announced Faizon Brandon as the starting quarterback in a team meeting on Monday 2026-08-24, over George MacIntyre and Colorado transfer Ryan Staub. Brandon is Tennessee's first true freshman to start a season opener since 2004. Formal team announcement. This naming post-dates the 2026-08-19 authoritative update, which recorded an either/or starter as of its 2026-08-18 check. Baseline and active values are 0/0 under the deviation-only convention: QB VALUES!G = F - D, so 0 - 0 = 0 and ENGINE!M contributes exactly nothing to any game. The zeros do not rate the quarterback - they record that the active starter IS the quarterback the preseason rating already assumed, so no deviation applies. No nonzero QB adjustment and no model change.
```

#### Georgia Southern — `QB VALUES` row 131

| Cell | Set to |
|---|---|
| `C131` | `Max Johnson` |
| `D131` | `0` |
| `E131` | `Max Johnson` |
| `F131` | `0` |
| `I131` | see verbatim text below |
| `K131` | `2026-08-24` |
| `L131` | see verbatim text below |

**`I131` verbatim:**

```
ESPN, 2026-08-23 (https://www.espn.com/college-football/story/_/id/49704180/max-johnson-start-quarterback-georgia-southern); Pete Thamel report (https://x.com/PeteThamel/status/2091599767289688141)
```

**`L131` verbatim:**

```
2026-08-24 ACTIVATED, confidence M (UNCHANGED from M). ESPN reported on 2026-08-23 that Max Johnson will start at quarterback for Georgia Southern; Pete Thamel: 'Sources: Georgia Southern has named veteran Max Johnson the school's starting quarterback.' M rather than H because this is a reporter-sourced claim rather than a team or coach announcement, matching the precedent set when North Carolina was activated at M on a Thamel sources report. INDEPENDENTLY CORROBORATED BY THE WORKBOOK: Thamel's detail that Johnson debuts against Charleston Southern then faces Clemson in Week 2 matches IMPORT SCHEDULE exactly (wk1 2026-09-05 Charleston Southern @ Georgia Southern, FCS - NO PLAY; wk2 2026-09-12 Georgia Southern @ Clemson). Supersedes the 2026-08-19 authoritative update, which as of its 2026-07-17 check recorded only 'would start if today'. Baseline and active values are 0/0 under the deviation-only convention: QB VALUES!G = F - D, so 0 - 0 = 0 and ENGINE!M contributes exactly nothing to any game. The zeros do not rate the quarterback - they record that the active starter IS the quarterback the preseason rating already assumed, so no deviation applies. No nonzero QB adjustment and no model change.
```

#### Fresno State — `QB VALUES` row 75

| Cell | Set to |
|---|---|
| `E75` | `Open (Khristian Martin / Jayden Mandal)` |
| `I75` | see verbatim text below |
| `K75` | `2026-08-24` |
| `L75` | see verbatim text below |

**`I75` verbatim:**

```
Authoritative research update 2026-08-19; 247Sports fall-camp report, August 2026 (https://247sports.com/college/fresno-state/article/fresno-state-quarterback-battle-unfolding-at-fall-camp-updates-from-qbs-khristian-martin-jayden-mandal-matt-entz-288830583/)
```

**`L75` verbatim:**

```
2026-08-24 RECORD CORRECTION (data quality only; confidence L UNCHANGED, status remains UNCERTAIN, numerical values remain BLANK). The candidate field read 'Open (three-way battle into August)', which is stale. The current race is a TWO-MAN contest: Khristian Martin (Maryland transfer) vs Jayden Mandal (2025 backup); Matt Entz has named no winner. BRADEN ATKINSON IS AT OREGON STATE, NOT FRESNO STATE - he is correctly carried on Oregon State row 76 and was never present in this field. RECHECK: Entz naming or a Week 1 depth chart.
```

## B. OUTSTANDING CORRECTIONS — already in the repo since v0.8.4, still missing live

#### Northern Illinois — `QB VALUES` row 123

| Cell | Set to |
|---|---|
| `E123` | `Open (Davidson / Macon / Hamric / Dickens)` |
| `H123` | `L` |
| `I123` | see verbatim text below |
| `K123` | `2026-08-21` |
| `L123` | see verbatim text below |

**`I123` verbatim:**

```
HERO Sports NIU quarterback report (https://herosports.com/fbs-prolific-fcs-quarterback-taron-tyger-dickens-win-starting-job-northern-illinois-rcrc/)
```

**`L123` verbatim:**

```
2026-08-21 REVERSES THE 2026-08-03 UPGRADE. That review raised L to M on the reasoning that the prior candidates 'Davidson / Macon / Hamric' did not appear in current NIU coverage and that Taron Dickens was widely expected to start. Current reporting contradicts that premise directly: coaches have NOT named a starter among returners Brady Davidson and Jalen Macon and transfers Ean Hamric and Taron Dickens — all four are named in current coverage. 'Widely expected to start' is a projection, not a naming, so M is not supported. M downgraded to L and the four-way candidate list restored. Also corrects a citation defect: the prior source was a MOUNTAIN WEST conference preview cited for a MAC team. Context: HC Thomas Hammock departed for the NFL; Rob Harley is interim head coach. Numerical values remain blank; status stays UNCERTAIN either way. RECHECK: Week 1 depth chart, opener 2026-09-05 at Iowa.
```

#### Tulane — `QB VALUES` row 91

| Cell | Set to |
|---|---|
| `E91` | `Open (Semonza / Chriss-Gremillion / Johnson / Bruno)` |
| `I91` | see verbatim text below |
| `K91` | `2026-08-21` |
| `L91` | see verbatim text below |

**`I91` verbatim:**

```
FOX 8 New Orleans, 2026-07-24 (https://www.fox8live.com/2026/07/24/four-qbs-battling-starting-spot-tulane/)
```

**`L91` verbatim:**

```
2026-08-21 CANDIDATE RECORD CORRECTED: the active field named Kadin Semonza alone, which overstated a four-way competition the record's own note already described. Current reporting confirms four quarterbacks taking fall-camp reps — Semonza, Zeon Chriss-Gremillion, Trace Johnson and Dagan Bruno — with head coach Will Hall yet to select one, and reporting that the job defaults to Chriss-Gremillion if no one separates. Candidate list corrected to match. Confidence L is UNCHANGED and correct. Numerical values remain blank; status stays UNCERTAIN. RECHECK: Will Hall naming or Week 1 depth chart.
```

## C. BANNER

**`START HERE!A1` verbatim:**

```
TO THE WINDOW — TTW COLLEGE FOOTBALL POWER RATINGS (v0.8.5 AUTHORITATIVE — promotion complete 2026-08-04. QB verification complete: backlog 0, audit-trail gap 0, all 73 Tier-1 records verified and stamped against team-specific primary sources; 72 H / 40 M / 26 L; 0 nonzero QB values. Preseason state: 0 market lines loaded, BET toggle = N.)
```

---

## D. NOT INCLUDED ABOVE

Rutgers (row 35) and Colorado State (row 74) are **deliberately absent** from this list —
they are unapproved and unapplied. Add them only after you approve Part 1.

## E. AFTER APPLYING SECTIONS A–C

The live Sheet should read:

- **108 OK / 30 UNCERTAIN**
- **72 H / 40 M / 26 L**
- `AUDIT!E1` = **0**
- Model spreads unchanged: `MEM at UNLV -5.6` · `UNC at TCU -4.2` · `NMSU at FSU -27.7` · `SJSU at USC -35.2` · `HAW at STAN -3.7`
- Week 0: **Memphis at UNLV** remains the only QB-gated game

If any of those disagree, stop and re-check before entering market lines.

**I am not claiming any live-Sheet change was made. None was.**
