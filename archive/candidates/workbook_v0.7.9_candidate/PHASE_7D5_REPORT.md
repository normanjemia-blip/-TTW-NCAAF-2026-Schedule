# Phase 7D.5 — Complete the QB Verification Project

**Date:** 2026-08-04 (America/New_York)
**Candidate:** `TTW_NCAAF_Power_Ratings_2026_v0.7.9_CANDIDATE.xlsx` — **the final QB-verification candidate**
**v0.6.2 AUTHORITATIVE:** unmodified · **v0.7.8:** unmodified · **Google Sheets:** never accessed · **NOT promoted.**

## Recommendation: **READY TO REPLACE v0.6.2 — with two conditions stated below**

The QB verification project is complete. Backlog **0**, audit-trail gap **0**,
regression suite **38/38**, formula changes **0** against the authoritative
workbook. Every one of the 73 Tier-1 records now carries an in-workbook
verification date and an evidence note, which was not true of any prior candidate.

**Not promoted — awaiting owner approval, as instructed.**

---

## 0. Correction to the phase brief's starting state

The brief described v0.7.7 as the current candidate with five teams outstanding.
That was already out of date: **Phase 7D.4A resolved all five and produced v0.7.8**
(SHA `8f655e5e…`, committed and pushed earlier today). This phase built on v0.7.8.

7D.4A also surfaced **finding F-7**, which is why this phase was not a formality:
**21 Tier-1 records were credited as verified in the phase ledger while the workbook
still carried their original 2026-07-21 build stamp and build note.** The backlog
counter said zero; the workbook could not substantiate it. Closing that gap is the
bulk of this phase, and it found three more defects.

## 1. The five — re-verified against official and primary sources

All five determinations from 7D.4A **stand**. Two new facts surfaced.

| Team | Code | Basis (primary source) |
|---|:--:|---|
| **Texas State** | **M** | Returning starter Brad Jackson — 2025: 3,050 pass yds, 18 TD, 71.5%, 16–17 rush TD (school QB record), 3,968 total yds (7th nationally); **MVP of the 2026 Armed Forces Bowl** (173 yds, 3 pass TD + rushing score, 41–10 over Rice). **NEW:** Boston College transfer **Shaker Reisig is the primary BACKUP, not a challenger**; QBs Keldric Luster (→ Ball State) and Holden Geriner (→ Pittsburgh) transferred out. No competition. |
| **Washington State** | **L** | HeraldNet 7/30 "wide-open QB competition"; Columbian 8/1 "unresolved"; HC Kirby Moore declined to commit; Pinnick "wasn't able to create meaningful separation from Eshelman." **Corroborated by the official transfer ledger:** Pinnick in from UC Davis; Jaxon Potter out to Old Dominion and Ajani Sheppard out to Temple — both appear as competitors in those teams' records. |
| **North Texas** | **M** | **HC Neal Brown**, American Kickoff broadcast 7/29: Tayven Jackson "now has a slight lead" in a three-man race with Chaston Ditta and Chris Jimerson Jr.; no starter declared. **NEW context:** UNT is replacing **Drew Mestemaker, the 2025 national passing-yards leader** — a full replacement, not a succession. |
| **Georgia Southern** | **M** | **HC Clay Helton**, Sun Belt Media Days 7/15: Max Johnson "is expected to be the starter if the season began today." Values stay blank (L→M rule). |
| **Old Dominion** | **M** | Quinn Henicle — 2025 Cure Bowl MVP, 2–0 as a starter; beat says "has a leg up" / "front runner" while "remains enmeshed in a three-way battle" with Jaxon Potter and Ryan Huff. Rahne has not named a starter. |

**On the "do not infer from preseason projections" rule:** none of the four M
classifications rests on a projection. Texas State and Old Dominion rest on the
incumbent's own starting record; North Texas and Georgia Southern rest on direct
head-coach statements. Where a source offered only a projection, I held the
conservative code — see Florida, Stanford and USF in §3.

## 2. Three defects found in the 21 unstamped records

| Team | Row | Change | Finding |
|---|---:|:--:|---|
| **Missouri** | 14 | **M → H** | **HC Eli Drinkwitz OFFICIALLY NAMED Austin Simmons on 2026-03-19**, right after spring camp and ~6 months before the opener, over Matt Zollers and Nick Evers. Reasoning on record: Simmons "was better in managing the team in two-minute drills and end-of-game situations," and naming him early would "allow him to really establish himself as a leader." Reaffirmed at SEC Media Days. The entry read "projected leader, some competition" — **stale; the competition had been formally settled five months earlier.** Zeros retained. |
| **North Carolina** | 65 | **M → L** | Entry asserted the Wisconsin transfer as "projected transfer QB1." **"UNC quarterback battle remains WIDE OPEN"** (2026-07-18). No starter named; Belichick left it open — "our quarterbacks after spring ball are still here." **Four** candidates: Billy Edwards Jr., Miles O'Neill (Texas A&M), Au'Tori Newkirk, Travis Burgess. |
| **UNLV** | 125 | **M → L** | Entry read "projected transfer QB1 **(verified)**" — the word *verified* was supported by nothing. Las Vegas Review-Journal 7/28: "even if coaches won't name a front-runner throughout training camp, there is definitely a battle between returner **Alex Orji** and Auburn transfer **Jackson Arnold**." Orji is proving out a Grade 3 LCL sprain and severe hamstring tear. Zeros cleared. |

**Numerical-cell consistency repairs: 1** (UNLV). **North Carolina needed none** —
it was one of seven M-coded rows that were never zero-initialized, so its values were
already blank and its status was already UNCERTAIN. The build script's guard caught my
assumption that zeros existed there; the L code now makes that gate explicit rather
than incidental.

## 3. The other 18 — confirmed, and where I declined to upgrade

Confirmed at their existing codes, now stamped with evidence notes:

**SEC** — Alabama **L** (Russell only "slightly favored," 55-45; undecided) · Auburn **M** (Byrum Brown, USF transfer following Golesh; 3,158 yds/28 TD in 2025) · Tennessee **L** (Brandon favored, undecided) · Kentucky **M** (Kenny Minchey, ND transfer, new HC Will Stein) · **Vanderbilt L** — *this closes the Phase 8.3 FAILED re-verification;* Curtis favored but the competition "remains open."

**Big Ten / ACC** — Nebraska **L** (Colandrea, 2025 Mountain West POY, joins TJ Lateef; no naming) · Stanford **L** · Syracuse **L** (Angeli "full go" post-Achilles, but reporting frames it as "another QB battle").

**American** — FAU **M** (Veltkamp returning; "zero questions about their starter"; Kittley's "5-man battle" concerns the **backup** order) · Memphis **L** (Huff choosing between Stokes and Noland; "one of the later ones settled") · USF **L** · Tulane **L** (Semonza "has to hold off" three challengers).

**MAC** — Toledo **M** (Richter "finally gets the keys in 2026") · Western Michigan **M** (Broc Lowry returning, **MAC Offensive Player of the Year**) · Ball State **L** · Central Michigan **L**.

**Sun Belt** — Southern Miss **L** (HC Blake Anderson: Lyddy "very much in the race"; no starter named).

**Three teams where a source offered a leader and I declined to upgrade**, because the
7D.5 rule bars inferring a starter from a projection: **Florida** (Philo "holds the
edge entering fall camp" — media characterization, no staff naming), **Stanford**
(Warren "in a strong position"), **USF** (Van Buren "seems to have the edge"). All
held at **L**, consistent with the Colorado State precedent.

**Two records carry thinner evidence than the rest, and I am flagging rather than
burying it:** **Ball State** and **Central Michigan** rest on the Phase 7D.1 live check
plus the absence of contradicting evidence this phase — no fresh confirmation was
located. **Nebraska**'s transfer is documented but the competition's state is inferred
from the absence of a naming. All three are **L**, the conservative code, so the
exposure is bounded.

## 4. The defect pattern — and its first exception

**11 defects across 80 team-specific passes, about 1 in 7.**

Ten were **over-confident**: an unsupported M or a stale named starter — Akron,
Arkansas, UConn, Buffalo, Northern Illinois, Appalachian State, Washington State,
Georgia Southern, North Carolina, UNLV.

**Missouri is the first defect in the opposite direction** — a record rated **too
uncertain**, sitting at M while the starter had been officially named five months
earlier. **I have claimed in three previous reports that no team was ever rated too
uncertain. That claim is now false and is corrected here and in the CHANGELOG.**

The asymmetry is still strong (10:1) and still argues that the dataset's residual risk
is over-confidence rather than over-caution. But it is no longer absolute, and the
Missouri case shows the cost of the other direction is real: a settled, officially
named starter was carrying an "UNCERTAIN"-adjacent classification for months.

## 5. Dataset integrity — final state

| Check | Result |
|---|---|
| 138 unique teams / abbrevs, no missing, duplicate or shifted rows | ✔ |
| Invalid H/M/L codes | **0** ✔ |
| Every L-coded team has blank numerical inputs | ✔ **0 violations** |
| Every L-coded team resolves to UNCERTAIN | ✔ |
| Nonzero QB values / nonzero deltas | **0 / 0** ✔ |
| Formula columns A, B, G, M intact on all 138 rows | ✔ |
| Input columns C–F, H–L hold constants only | ✔ |
| **Final H / M / L** | **65 H / 40 M / 33 L** = 138 |
| **Final OK / UNCERTAIN** | **99 OK / 39 UNCERTAIN** |
| **Blank / zero numerical** | **39 blank / 99 zero** = 138 |
| **QB verification backlog** | **0** ✔ |
| **Audit-trail gap (Tier-1 rows unstamped)** | **0** ✔ — finding F-7 closed |
| Every Tier-1 record carries an evidence note | ✔ |
| H-coded tier-2 rows still on the 2026-07-21 build stamp | **61** — never in Tier-1 scope (see §7) |

Tier-1 population is now **73** (M+L), down one because Missouri moved to H.

## 6. Regression suite — 38 / 38 PASS

Full log: `verification_log_v079.txt`.

**0 formula changes this phase and 0 against v0.6.2 AUTHORITATIVE** ✔ · formula count
**123,011** identical across v0.6.2, v0.7.8 and v0.7.9 ✔ · 21 sheets, order and
visibility identical ✔ · **TEAM RATINGS, ENGINE, SETTINGS, ADJUSTMENTS, MARKET LINES,
PRESEASON and IMPORT SCHEDULE untouched — both this phase and cumulatively against the
authoritative workbook** ✔ · `ENGINE!AI` status precedence, `ENGINE!M`, `ENGINE!AE`,
`QB VALUES!G` and `QB VALUES!M` formulas byte-identical to v0.6.2 ✔ ·
`SETTINGS!B3`=2026, `B6`=2.5 HFA, `B11`="N" ✔ · no confidence edit created a numerical
adjustment ✔ · no team-rating or projected-spread movement ✔ · diff confined to the 26
intended QB rows ✔ · 0 unrelated / unauthorized / unknown cells ✔.

**Status masking is unchanged:** with **0 market spreads loaded**, PENDING LINE
outranks QB UNCERTAIN, so every game still reads PENDING LINE. UNLV's OK → UNCERTAIN
move changes no game status, no rating and no spread.

## 7. Remaining unresolved issues

1. **61 H-coded tier-2 records still carry the 2026-07-21 build stamp.** These were never in Tier-1 verification scope by design — H means the starter was already established at build time. They are **not** part of the backlog, and no phase has ever claimed otherwise. But if the owner wants the *entire* dataset self-substantiating, this is the remaining population. Spot-checking them is a defensible pre-season task; Missouri showed that H-tier assumptions can also go stale.
2. **Three thin confirmations** — Ball State, Central Michigan, Nebraska (§3). All L-coded, so bounded.
3. **Fall camp is live.** Every M and L record is a snapshot dated 2026-08-04, with camps opening 8/1–8/6 and openers 8/29–9/5. Depth charts will land in the next three weeks and will settle many of the 33 L records. Each note carries an explicit RECHECK trigger.
4. **Texas Tech** still carries the Phase 7C.1 provisional acceptance — surgeon clearance reported, final team medical clearance pending around the nine-month mark (~Aug 21).

None of these blocks promotion. Items 3 and 4 are the ordinary business of the
Phase 8.4 monitoring sweeps, which already have a pipeline built for them.

## 8. Diff

**v0.7.8 → v0.7.9: 73 changed cells · 0 formula changes · 0 unrelated/unauthorized/unknown.**
Detail: `diff_v078_to_v079.csv`.

| Classification | Count |
|---|---:|
| F-7 AUDIT-TRAIL STAMP (verification date + evidence note) | 41 |
| VERSION OR CHANGELOG | 13 |
| VERIFIED QB CLASSIFICATION CHANGE | 12 |
| FINAL-FIVE RE-VERIFICATION NOTE REFRESH | 5 |
| **NUMERICAL-CELL CONSISTENCY REPAIR** (UNLV D125/F125) | **2** |
| **UNRELATED / UNAUTHORIZED / UNKNOWN** | **0** |

**Cumulative v0.6.2 AUTHORITATIVE → v0.7.9: 1,249 changed cells · 0 formula changes**,
confined to exactly **three sheets** — QB VALUES (1,132), CHANGELOG (116), START HERE (1).
Detail: `diff_v062_to_v079.csv`. **Eighteen sheets are byte-identical to the
authoritative workbook.** This is the diff the owner is being asked to approve.

## 9. Manifest / SHA-256

| File | SHA-256 |
|---|---|
| **v0.7.9 CANDIDATE** (new, FINAL) | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` |
| v0.7.8 CANDIDATE | `8f655e5e369a6a8c12fdb34f3309cff13a92c9310af6186b77081be4b3c389cb` — **UNCHANGED** ✔ |
| v0.6.2 AUTHORITATIVE | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` — **UNCHANGED**, = `PROJECT_MANIFEST.json` ✔ |

Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` and rollback sheet
`1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo` — **never accessed.** No rating, HFA,
formula, structure, threshold, schedule, source-weight or status-logic change. VSiN
guide and VSiN database — **not accessed this phase.**

## 10. Promotion recommendation

**Recommended: promote v0.7.9 to AUTHORITATIVE**, subject to two conditions.

**Why it is ready.** The change against v0.6.2 is entirely additive metadata in one
data sheet plus a changelog and a banner. **Zero formulas changed. Zero ratings moved.
Zero spreads moved. Eighteen of twenty-one sheets are byte-identical.** The workbook
computes exactly what the authoritative workbook computes today; what it gains is a
QB dataset where all 138 records are populated (v0.6.2 has **0/138** confidence codes)
and all 73 Tier-1 records are independently verified and stamped with evidence.

**Condition 1 — promote before the openers, not during.** With 0 market lines loaded,
promotion is behaviorally inert today. Once lines load, the 39 UNCERTAIN records begin
gating games. Promoting into a quiet workbook is materially safer than promoting mid-week.

**Condition 2 — the 33 L records are perishable.** They are accurate as of 2026-08-04
and many will be settled by depth charts within three weeks. Promotion should be paired
with the first Phase 8.4 monitoring sweep so the dataset does not go stale the moment
it becomes authoritative.

**What I am not claiming.** I am not claiming the 61 H-coded tier-2 records have been
independently verified — they have not, and Missouri is proof that an H-tier assumption
can go stale. I am claiming that every record the project scoped for verification has
been verified, and that the workbook can now show its work for each one.

**Not promoted. Awaiting owner approval.**
