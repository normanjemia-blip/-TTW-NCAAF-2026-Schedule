# TTW NCAAF 2026 — WASHINGTON STATE RECHECK, 2026-08-24

**Verification timestamp:** Monday, 2026-08-24, **15:54 EDT** (America/New_York, owner timezone —
container UTC not used)
**Scope:** Washington State only. Read-only. No workbook, Google Sheet or rating was changed.
**Authorising instruction:** *"Keep Washington State unresolved and recheck later today."*
**Prior check:** same day, 10:49 EDT — decision unpublished.

---

## 1. Ruling

> **WASHINGTON STATE REMAINS UNRESOLVED.** No qualifying naming has published as of 15:54 EDT.
> **No cell changed. No activation candidate is raised.**

Washington State stays at confidence `L`, status `UNCERTAIN`, `D`/`F` blank.

---

## 2. What the deadline actually was

| Fact | Source | Verified |
|---|---|:--:|
| Kirby Moore would decide among Pinnick / Eshelman / Dugger **by Aug. 24**, the first day of the semester | The Columbian, 2026-08-06 | ✅ |
| Coaches "still on track to announce their starting quarterback **by Monday**, the first day of the new semester" | Spokesman-Review, 2026-08-21 | ✅ |
| Fall-camp finale was **Sunday** evening at Gesa Field | Spokesman-Review, 2026-08-21 | ✅ |

**Date arithmetic, computed not assumed:** 2026-08-23 = Sunday, **2026-08-24 = Monday**,
2026-09-06 = Sunday. So "by Monday" and "by Aug. 24" are the **same deadline — today**, and the
camp finale was yesterday. The two beat reports agree; there is no second, later deadline.

> One automated page summary rendered the deadline as "August 25." That is a summarizer arithmetic
> error, not text from the article. The article says "by Monday," and Monday is the 24th.

---

## 3. Primary-source check — no naming found

Per the standing rule, search snippets were **not** accepted as evidence. The beat outlet's own
article index was fetched directly:

**`spokesman.com/sports/team/wsu-football/news/`** — most recent items:

| Date | Headline |
|---|---|
| 2026-08-22 | What will WSU's special teams unit look like this season? |
| 2026-08-21 | WSU to announce starting QB by Monday, coach Kirby Moore says… |
| 2026-08-21 | Not up to the standard: WSU offense finds end zone just twice in final fall camp scrimmage |
| 2026-08-21 | They're invested in this conference: Leaf returns to Pullman… |
| 2026-08-20 | WSU is ready for its second and final scrimmage of fall camp |

**Nothing dated 2026-08-23 or 2026-08-24. No headline names a starter.** The Aug 21 article was
fetched in full and confirmed to announce only that a decision is coming.

Secondary attempts: `wsucougars.com/sports/football` returned navigation chrome only with no news
body; `cougcenter.com` returned **HTTP 403**; `spokesman.com/sports/wsu-cougars/football/` returned
**HTTP 404**. These are access failures, **not** evidence of absence, and are recorded as such.

---

## 4. Evidence explicitly rejected as non-qualifying

| Claim encountered | Why rejected |
|---|---|
| "Caden Pinnick is Washington State's **expected** starting quarterback for the Apple Cup" | Projection. Standing rule: *do not infer a starter from preseason projections.* |
| Pinnick "**likely frontrunner**" / "**early frontrunner**" (Spokesman 2026-08-21) | Frontrunner language is not a naming. It is the same status that already justified `L`. |
| "QB Caden Pinnick **takes reins**" (Spokesman 2026-08-15) | First-scrimmage rep distribution, not a decision. Predates the deadline. |
| Absence of an Aug 23–24 article | Standing rule: *absence of evidence is not proof.* Recorded as "not yet published," not "no decision." |

The Aug 21 scrimmage reporting in fact **weakens** the frontrunner case: Pinnick threw one
interception plus two others tipped, Dugger did not play, and Eshelman was nearly intercepted
twice. Nothing here separates the field.

---

## 5. Workbook state — unchanged and verified

Workbook: `promotion_v0.8.5/TTW_College_Football_Power_Ratings_v0.8.5_AUTHORITATIVE.xlsx`
SHA-256 re-computed this session: `0676aa1a05d661ca0d99c917c8dc471c0030128cc42ea8fd1bd2f17dcea767be` ✅ matches promotion record

**`QB VALUES` row 80 — `WSU` / Washington State**

| Col | Value |
|---|---|
| C baseline QB | `Caden Pinnick` |
| D baseline value | *(blank)* |
| E active QB | `Open (Caden Pinnick / Owen Eshelman / Julian Dugger)` |
| F active value | *(blank)* |
| G delta | `=IF(OR($D80="",$F80=""),"",$F80-$D80)` → blank |
| H confidence | `L` |
| J reviewed | `2026` |
| K last update | `2026-08-04` |
| M status | formula → **UNCERTAIN** |

The candidate field is **already correct** — the exact three-way named in the beat reporting. No
record correction is warranted either; the recheck produced nothing the row does not already say.

---

## 6. Gating exposure — none this week

Washington State's schedule, read from the project's own verified schedule file:

| Week | Date | Game |
|:--:|---|---|
| 1 | **2026-09-06** (Sunday) | Washington State @ Washington — Apple Cup |
| 2 | 2026-09-12 | Washington State @ Kansas State |
| 3 | 2026-09-19 | Duquesne @ Washington State |

**Washington State is not in the Week 0 slate** (all eight Week 0 games verified: UNC@TCU, HAW@STAN,
NCST@UVA, SJSU@USC, NMSU@FSU, JVST@NDSU, SAC@EMU, MEM@UNLV). The Spokesman's separate "Sunday Apple
Cup" kickoff report independently corroborates the workbook's `2026-09-06` date.

**Consequence:** the unresolved gate costs nothing operationally right now. There are **13 days** of
runway before it can affect a graded game, and **Memphis at UNLV remains the single QB-gated Week 0
game.**

---

## 7. Censuses — unchanged

| | v0.8.5 | After this recheck |
|---|:--:|:--:|
| QB status | 108 OK / 30 UNCERTAIN | **108 OK / 30 UNCERTAIN** |
| Confidence | 72 H / 40 M / 26 L | **72 H / 40 M / 26 L** |
| Nonzero QB values | 0 | **0** |

Baseline preserved: 138 teams · 888 games · 761 FBS-v-FBS · 127 FCS-involved · 0 BLOCK.

---

## 8. Still open — closeout is NOT complete

| Item | Row | State |
|---|:--:|---|
| **Rutgers** — Dylan Lonergan | 35 | Packet issued; **awaiting owner approval**. Not applied. |
| **Colorado State** — `Hauss Hejny vs. K'saan Farrar` | 74 | Ruled by owner but outside approved items 1–5. **Held, not applied.** |
| **Texas Tech** — Will Hammond | 52 | Medical gate retained. QB1 identity not in question. |
| **Washington State** | 80 | **UNRESOLVED — this document.** |
| **Live-Sheet application** | — | Sections A–C (v0.8.5 + NIU + Tulane) are owner actions; connector cannot write cells. |

---

## 9. Recommended next recheck

The deadline is today and has roughly five hours of Pacific business day left (15:54 EDT = 12:54
PDT). The most likely publication windows are this evening Pacific, or Tuesday 2026-08-25 with
Moore's game-week press availability — which is also the point at which a first depth chart for the
Apple Cup would normally appear.

**Recheck trigger:** an official Washington State Athletics release, a WSU depth chart, or a direct
Kirby Moore quote naming a starter. Frontrunner or projection language does **not** qualify.

If Washington State is named, the expected treatment mirrors the Georgia Southern / Rutgers
reporter-sourced precedent: activate at `M` (or `H` on an official team release), write `D=0` and
`F=0`, `G` computes to `0`, status clears to OK, and **no rating moves**. If Pinnick is the name,
he is already the baseline QB in column C, so the deviation is genuinely zero.
