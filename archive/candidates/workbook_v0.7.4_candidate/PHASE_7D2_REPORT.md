# Phase 7D.2 — Akron Consistency Repair & QB Verification Batch 1 (MAC + CUSA)

**Date:** 2026-08-03 (America/New_York) · **Candidate:** `TTW_NCAAF_Power_Ratings_2026_v0.7.4_CANDIDATE.xlsx`
**v0.6.2 AUTHORITATIVE:** unmodified · **v0.7.3:** unmodified · **Google Sheet:** never accessed · **NOT promoted.**

## Promotion status: **DEFER — 47 of 54 backlog teams remain unverified**

## 1. Akron consistency repair (approved) ✔

All pre-conditions asserted in code before editing (build aborts on any mismatch):

| Assertion | Result |
|---|---|
| Row 105 = Akron | ✔ |
| Active QB = corrected open competition (Poffenbarger / Roggow) | ✔ |
| Confidence = `L` | ✔ |
| `D105` and `F105` both equal **0** | ✔ |
| Both are user-input cells, not formulas | ✔ |

**Applied:** `D105` → **blank**, `F105` → **blank**; note extended to record the
methodology rationale (zero would assert an affirmative evaluation of both
starter and replacement; blank correctly represents an unresolved numerical
assessment).

**Post-repair confirmation:**

| Check | Result |
|---|---|
| `G105` blank | ✔ (D/F blank → delta blank) |
| `M105` = UNCERTAIN | ✔ |
| Confidence still `L` | ✔ |
| Team ratings changed | **No** — TEAM RATINGS byte-identical |
| Projected spreads changed | **No** — ENGINE sheet unchanged |
| Unrelated status changes | **None** |

**Blank vs zero now carry distinct meanings across the dataset: 34 blank / 104
zero = 138.**

## 2. Exact starting backlog — reproduced, and a prior figure corrected

Re-derived from `qb_inventory_v073.json` + the 7D/7D.1 logs rather than trusting
the stated number:

| Quantity | Value |
|---|---:|
| Tier 1 (all M + all L) | **77** |
| Verified in Phases 7A–7D | 18 |
| Fresh in Phase 7D.1 | 6 — but **only 5 were *newly* verified** |
| **Exact backlog at 7D.2 start** | **54** |

**Correction:** Phase 7D.1 reported **53**. That was an off-by-one — **Texas
Tech was counted as newly verified when it was already in the 7A–7D verified
set**. The correct figure is **54**. Logged as correction E-6.

## 3. Batch 1 scope — 14 teams (6 MAC + 8 CUSA)

MAC: BGSU, BUFF, M-OH, MASS, OHIO, SAC · CUSA: FIU, KENN, LIB, MOST, MTSU, NMSU, SHSU, WKU
*(Akron, Ball State, Central Michigan, Toledo, Western Michigan were completed in
7D.1 and were not redone — prior verification confirmed current.)*

## 4. MAC verification report

| Team | Code | Finding | Result |
|---|---|---|---|
| **Bowling Green** | M | **Austin Novosad** (Oregon transfer; former 4★, No. 13 QB in 2023 class; portal QB was a stated program priority) confirmed projected starter | **CONFIRMED** |
| **UMass** | M | **William "Pop" Watson** (Virginia Tech transfer) confirmed arriving to lead the program | **CONFIRMED** |
| **Ohio** | L → **M** | HC **John Hauser**: Nick Poulos *"is still in the lead"*; Ohio has **no Week 1 starter named** | **RECLASSIFIED** |
| Miami (OH) | L | Candidate lists **Thomas Gotkowski**; one outlet references a **Kansas transfer** as holding the projected starting role | **CONFLICT — unresolved** |
| Buffalo | L | No sufficient current evidence located | **NOT VERIFIED** |
| Sacramento State | M | No sufficient current evidence located | **NOT VERIFIED** |

## 5. Conference USA verification report

| Team | Code | Finding | Result |
|---|---|---|---|
| **Western Kentucky** | M | **Rodney Tisdale Jr.** confirmed returning starter — **but Brock Glenn (7 career starts at Florida State) transferred in to challenge.** Clear leader with genuine competition → **M correct, not H** | **CONFIRMED** |
| **Liberty** | L | Genuine **three-way transfer race** (Purdie / Jaylen Henderson / Ethan Vasko); Chadwell expected to get quality play, **no starter named** | **CONFIRMED** |
| **Middle Tennessee** | M | **Roman Gagliano** confirmed signal-caller, cited as a breakout candidate | **CONFIRMED** |
| **Sam Houston** | M | **Landyn Locke** confirmed signal-caller, cited as a breakout candidate | **CONFIRMED** |
| FIU | M | Reporting says FIU is "likely to start a transfer" but **does not name JJ Kohl** — directionally consistent, insufficient to verify | **NOT VERIFIED** |
| Kennesaw State | M | No sufficient current evidence located | **NOT VERIFIED** |
| Missouri State | L | No sufficient current evidence located | **NOT VERIFIED** |
| New Mexico State | L | No sufficient current evidence located | **NOT VERIFIED** |

## 6. QB correction log

| Team | Prior starter | Corrected | Prior code | New code | Prior D/F | New D/F | Reason | Source | Date | Downstream |
|---|---|---|---|---|---|---|---|---|---|---|
| **Akron** | Open (Poffenbarger/Roggow) | *unchanged* | L | **L** | **0 / 0** | **blank / blank** | Zero misrepresents an unresolved room as an affirmative zero evaluation | Owner-approved methodology repair | 2026-08-03 | G blank; status UNCERTAIN; **no rating/spread effect** |
| **Ohio** | Open competition | **Nick Poulos (leader; not yet named)** | **L** | **M** | blank / blank | *unchanged* | HC describes a clear leader; no formal announcement → M standard | WOUB (Ohio U. public media), MAC Media Day | 2026-08-03 | Stays **UNCERTAIN** (values blank) |
| **Liberty** | Ethan Vasko | **Open (Purdie / Henderson / Vasko)** | L | **L** | blank / blank | *unchanged* | Verified three-way race; single name understated the uncertainty | CUSA QB projections; SI CUSA odds | 2026-08-03 | No change |
| BGSU, UMass, MTSU, SHSU, WKU | — | *unchanged* | — | *unchanged* | *unchanged* | *unchanged* | Records **confirmed accurate**; truthful note + date refreshed only | see §4–5 | 2026-08-03 | None |

**No record was changed to appear productive.** The six unverified teams and the
Miami (OH) conflict retain their **2026-07-21** dates — deliberately not refreshed.

## 7–8. Updated inventory and remaining backlog

**Final H/M/L: 61 H / 46 M / 31 L** (Ohio L→M is the sole mover).
**Final status: 104 OK / 34 UNCERTAIN**, unchanged from v0.7.3 — Akron was
already gated by its `L` code, and Ohio's new `M` still yields UNCERTAIN because
its numerical values remain blank.

**Backlog remaining: 47** (was 54; 7 verified this batch).

| Conference | Remaining |
|---|---|
| Big Ten | 6 — IOWA, MINN, MSU, PUR, RUTG, WISC |
| Pac-12 | 6 — CSU, FRES, ORST, TXST, USU, WSU |
| American | 6 — ECU, NAVY, RICE, TEM, TLSA, UNT |
| Mountain West | 6 — NDSU, NEV, NIU, SJSU, UTEP, WYO |
| Sun Belt | 6 — APP, ARST, CCU, GASO, JMU, ODU |
| Big 12 | 4 — AZST, HOU, KAN, WVU |
| Conference USA | 4 — FIU, KENN, MOST, NMSU |
| ACC | 3 — DUKE, UVA, WAKE |
| MAC | 3 — BUFF, M-OH *(conflict)*, SAC |
| SEC | 2 — ARK, MSST |
| Independent | 1 — CONN |

## 9. Source & conflict log

| # | Claim | Source 1 | Source 2 | Resolution | Residual |
|---|---|---|---|---|---|
| E-6 | Backlog = 53 (7D.1) | Phase 7D.1 report | Re-derivation: **54** | **7D.1 double-counted Texas Tech — corrected** | None |
| E-7 | Miami (OH) QB | Candidate: Thomas Gotkowski | Outlet: "the Kansas transfer has the projected starting role" | **UNRESOLVED** — cannot confirm which is current | **Open — L retained, date not refreshed** |
| E-8 | Ohio QB open | Candidate: "Open competition" | HC Hauser: Poulos "still in the lead," no Week 1 starter | Coach statement outranks generic label → **M** | Formal naming |
| E-9 | WKU settled at M | Candidate: Tisdale returning starter | Brock Glenn (7 FSU starts) transferred in to challenge | **M confirmed, not H** — real competition exists | Camp outcome |
| E-10 | Liberty = Vasko | Candidate single name | Three-way race (Purdie/Henderson/Vasko) | Entry refined; **L retained** | Winner |
| E-11 | Bulk MAC/CUSA verification | Conference roundups | Athlon **403**; snippets insufficient for 6 teams | Per-team beat sourcing required | 6 teams unverified |

## 10. Regression-test report — all pass

| # | Test | Result |
|---|---|---|
| 1 | **Akron cleared values preserve UNCERTAIN** | ✔ D/F blank → G blank → UNCERTAIN |
| 2 | **No confidence edit creates a numerical adjustment** | ✔ Ohio L→M with blank values; 0 nonzero deltas dataset-wide |
| 3 | **No team rating changes** | ✔ TEAM RATINGS not in diff |
| 4 | **No projected spread changes** | ✔ ENGINE not in diff |
| 5 | **No formula changes** | ✔ 0 |
| 6 | PENDING LINE priority | ✔ outranks QB UNCERTAIN; 0 spreads loaded → all games still PENDING LINE |
| 7 | FCS — NO PLAY priority | ✔ unchanged |
| 8 | TRANSITION UNCERTAIN priority | ✔ unchanged |
| 9 | BET-toggle behavior | ✔ `SETTINGS!B11="N"`, SETTINGS not in diff |
| 10 | **Blank vs zero retain distinct meanings** | ✔ 34 blank / 104 zero = 138 |
| 11 | **Formula columns A, B, G, M unchanged** | ✔ intact on all 138 rows |
| 12 | H + populated metadata | ✔ 61 → OK |
| 13 | M + populated metadata | ✔ 43 → OK; 3 → UNCERTAIN (UNC, Texas Tech, Ohio — all blank values, correctly gated) |
| 14 | L + populated metadata | ✔ 31 → UNCERTAIN |
| 15 | 138 unique teams, no shift/duplication | ✔ |
| 16 | Input columns constants only | ✔ |

## 11–12. Diff v0.7.3 → v0.7.4

**33 changed cells · ZERO formula changes · zero unrelated / unauthorized / unknown.**

| Cells | Classification | Count |
|---|---|---|
| `D105`, `F105`, `L105` | **APPROVED AKRON CONSISTENCY REPAIR** | 3 |
| `E113`, `H113` (Ohio) | **VERIFIED MAC QB UPDATE** | 2 |
| `E99` (Liberty) | **VERIFIED CUSA QB UPDATE** | 1 |
| `K99/L99, K100/L100, K103/L103, K104/L104, K107/L107, K113/L113, K116/L116` | **NOTE OR DATE UPDATE** | 14 |
| `CHANGELOG!A70:D72` | **VERSION OR CHANGELOG** | 12 |
| `START HERE!A1` | **VERSION OR CHANGELOG** | 1 |

Formula count **123,011 → 123,011 (delta 0)**; 21 sheets; order and visibility identical.

## 13. Manifest / SHA-256

| File | SHA-256 |
|---|---|
| **v0.7.4 CANDIDATE** (new) | `57cd6d20d38feb64e09dc3dcd00799f6a88ccad4502bd4624900036502d8d4c6` |
| v0.7.3 CANDIDATE | `07bed6dedc647124e77d78324b8e5f37e1f35ca5eef37c0ee36615dd8c7da72d` — **UNCHANGED** ✔ |
| v0.6.2 AUTHORITATIVE | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` — **UNCHANGED**, = `PROJECT_MANIFEST.json` ✔ |

Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` — **never accessed.**

## 14–15. Promotion recommendation

**DEFER PROMOTION.** 47 of 54 backlog teams remain unverified. Batch 1 produced
**1 classification change, 1 entry refinement, and 1 unresolved conflict out of
14 teams (~21% touched)** — a defect-discovery rate consistent with 7D.1's, and
direct evidence the remaining 47 still carry errors.

**Recommended next batch:** **Big Ten (6) + Big 12 (4) + ACC (3) + SEC (2) +
Independent (1) = 16 Power-conference teams.** Rationale: these carry the
largest rating weight, and P4 beat coverage is deepest — so verification success
per search is highest. That would leave the 25 remaining G5 teams (American,
Mountain West, Pac-12, Sun Belt) plus the 3 MAC / 4 CUSA stragglers for a final
batch.
