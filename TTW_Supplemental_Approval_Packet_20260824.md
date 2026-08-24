# TTW NCAAF 2026 — COMBINED SUPPLEMENTAL APPROVAL PACKET

**Packet timestamp:** Monday, **2026-08-24, 18:20 EDT** (America/New_York, owner timezone)
**Status:** **READ-ONLY PROPOSAL. NOTHING APPLIED.** No workbook, no Google Sheet, no cell changed.
**Base:** v0.8.5 AUTHORITATIVE at commit `12e88dc` — **accepted, preserved, unmodified**
**Base SHA-256:** `0676aa1a05d661ca0d99c917c8dc471c0030128cc42ea8fd1bd2f17dcea767be` (re-verified this session)
**Awaiting:** explicit owner approval. Rutgers, Washington State and Colorado State are **not** applied.

Items: **1.** Rutgers r35 · **2.** Washington State r80 · **3.** Colorado State r74

---

# ITEM 1 — RUTGERS, row 35 — ACTIVATE at `M`

| Field | Value |
|---|---|
| Team / abbrev | Rutgers Scarlet Knights · `RUTG` · row **35** |
| Player | **Dylan Lonergan** (Boston College transfer) |
| Current | `M` / **UNCERTAIN** |
| Proposed | `M` / **OK** — **confidence unchanged** |
| Source | ESPN — Pete Thamel; carried by On3/The Knight Report, 247Sports, Yahoo Sports, On the Banks |
| URL | `https://www.on3.com/sites/the-knight-report/news/rutgers-names-dylan-lonergan-starting-quarterback-for-2026/` · `https://247sports.com/college/rutgers/article/-dylan-lonergan-named-rutgers-starting-quarterback-289146979/` |
| Publication date | **2026-08-24** |
| Confidence | **M** |
| Justification | **Reporter-sourced naming, not a team or coach announcement.** Same provenance class as Georgia Southern and North Carolina, both activated at `M`. Lonergan won the job over AJ Surace after competing through spring and fall camp. `M` not `H` because no first-party team release exists. |
| Corroboration | Reporting says Lonergan "will lead the Scarlet Knights into Week 1 against UMass." The workbook independently confirms: `wk1 2026-09-03 Massachusetts Minutemen @ Rutgers Scarlet Knights`. |

### Exact cells

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `C35` | *(blank)* | `Dylan Lonergan` | text — **see 1.1, required** |
| `D35` | *(blank)* | **`0`** | **numerical** |
| `E35` | `Dylan Lonergan (likely starter; AJ Surace competing)` | `Dylan Lonergan` | text |
| `F35` | *(blank)* | **`0`** | **numerical** |
| `H35` | `M` | `M` — **unchanged** | — |
| `I35` | `Sports Illustrated (Big Ten QB projections) (https://www.si.com/college-football/projecting-every-big-ten-starting-quarterback-ahead-of-2026-season)` | `ESPN / Pete Thamel via On3 The Knight Report + 247Sports 2026-08-24 (https://www.on3.com/sites/the-knight-report/news/rutgers-names-dylan-lonergan-starting-quarterback-for-2026/)` | metadata |
| `J35` | `2026` | **must not be rewritten** | — |
| `K35` | `2026-08-03` | `2026-08-24` | metadata |
| `L35` | prior verification note | activation note (below) | text |
| **`G35`** | *(formula)* | **DO NOT WRITE** | formula |
| **`M35`** | *(formula)* | **DO NOT WRITE** | formula |

**Proposed `L35`:**

> `2026-08-24 ACTIVATED, confidence M (UNCHANGED from M). ESPN's Pete Thamel reported that Rutgers named Dylan Lonergan its starting quarterback, won over AJ Surace after spring and fall camp; carried by On3/The Knight Report, 247Sports, Yahoo Sports and On the Banks. M rather than H because this is a reporter-sourced claim rather than a team or coach announcement, matching the precedent set when North Carolina and Georgia Southern were activated at M on Thamel sources reports. INDEPENDENTLY CORROBORATED BY THE WORKBOOK: reporting that Lonergan leads Rutgers into Week 1 against UMass matches IMPORT SCHEDULE exactly (wk1 2026-09-03 Massachusetts Minutemen @ Rutgers Scarlet Knights). Supersedes the 2026-08-03 SI projection entry, which recorded only 'likely starter'. Baseline and active values are 0/0 under the deviation-only convention: QB VALUES!G = F - D, so 0 - 0 = 0 and ENGINE!M contributes exactly nothing to any game. The zeros do not rate the quarterback - they record that the active starter IS the quarterback the preseason rating already assumed, so no deviation applies. No nonzero QB adjustment and no model change.`

### 1.1 ⚠️ `C35` is required, not optional — a workbook invariant depends on it

I swept all 138 rows. **Every one of the 108 OK rows has a populated baseline QB in column `C`.
108 of 108, zero exceptions.** Blank `C` occurs *only* on UNCERTAIN rows — 23 of the 30.

Rutgers row 35 currently has `C` **blank**. Writing only `D35=0` and `F35=0` would clear the gate
and make Rutgers the **first OK row in the workbook with no baseline quarterback recorded** —
breaking an invariant that currently holds without exception, and leaving a zero deviation that
cannot be audited because nothing says *deviation from whom*.

**Basis for the value:** the source already cited in `I35` — the SI Big Ten projection — names
Lonergan as Rutgers' projected starter. He *is* the quarterback the preseason blend assumed, so
`C35 = Dylan Lonergan` makes the zero deviation literally true rather than merely conventional.

> This cell is **flagged for your explicit approval** because it goes beyond a bare "activate row 35."
> If you prefer to withhold it, Rutgers should **not** be activated this cycle — activating with a
> blank `C` is the one combination I would not recommend.

Washington State needs no equivalent cell: `C80` is **already populated** (item 2).

---

# ITEM 2 — WASHINGTON STATE, row 80 — ACTIVATE at `H`

| Field | Value |
|---|---|
| Team / abbrev | Washington State Cougars · `WSU` · row **80** |
| Player | **Caden Pinnick** (UC Davis transfer) |
| Current | `L` / **UNCERTAIN** |
| Proposed | **`H`** / **OK** |
| Source | Spokesman-Review — *"UC Davis transfer Caden Pinnick to start at QB for Washington State this fall"* |
| URL | `https://www.spokesman.com/stories/2026/aug/24/uc-davis-transfer-caden-pinnick-to-start-at-qb-for/` |
| Publication date | **2026-08-24**, stamped *updated Mon., Aug. 24, 2026 at 3:18 p.m.* |
| Confidence | **H** |
| Justification | **First-party team announcement.** Verbatim: *"The Cougars will start UC Davis transfer Caden Pinnick, **the program announced on social media Monday afternoon**"* — a `@WSUCougarFB` "QB1" post. A team's own announcement is the strongest provenance tier in this project, **above** the reporter-sourced `M` used for Rutgers and Georgia Southern. It also satisfies the deadline Kirby Moore set publicly on 2026-08-06 ("by Aug. 24") and restated 2026-08-21 ("by Monday"). |
| Corroboration | Article states *"WSU's season-opener is set for Sept. 6 at No. 17 Washington."* Workbook independently confirms: `wk1 2026-09-06 Washington State Cougars @ Washington Huskies`. |

### Exact cells

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `C80` | **`Caden Pinnick`** | **`Caden Pinnick` — NO CHANGE** | — |
| `D80` | *(blank)* | **`0`** | **numerical** |
| `E80` | `Open (Caden Pinnick / Owen Eshelman / Julian Dugger)` | `Caden Pinnick` | text |
| `F80` | *(blank)* | **`0`** | **numerical** |
| `H80` | `L` | **`H`** | confidence |
| `I80` | `Athlon/ESPN Pac-12 (https://athlonsports.com/college-football/pac-12-football-2026-predictions)` | `Washington State official team announcement (@WSUCougarFB) via Spokesman-Review 2026-08-24 (https://www.spokesman.com/stories/2026/aug/24/uc-davis-transfer-caden-pinnick-to-start-at-qb-for/)` | metadata |
| `J80` | `2026` | **must not be rewritten** | — |
| `K80` | `2026-08-04` | `2026-08-24` | metadata |
| `L80` | prior defect-corrected note | activation note (below) | text |
| **`G80`** | *(formula)* | **DO NOT WRITE** | formula |
| **`M80`** | *(formula)* | **DO NOT WRITE** | formula |

**Proposed `L80`:**

> `2026-08-24 ACTIVATED, confidence L -> H. Washington State announced Caden Pinnick as QB1; the program posted the announcement from @WSUCougarFB on the afternoon of 2026-08-24, reported by the Spokesman-Review: 'The Cougars will start UC Davis transfer Caden Pinnick, the program announced on social media Monday afternoon.' H rather than M because this is a FIRST-PARTY TEAM ANNOUNCEMENT, not a reporter-sourced claim - a tier above the Georgia Southern / North Carolina / Rutgers precedent. Resolves the three-way competition with Owen Eshelman and Julian Dugger and satisfies the deadline HC Kirby Moore set publicly on 2026-08-06 ('by Aug. 24') and restated 2026-08-21 ('by Monday'). Supersedes the 2026-08-04 defect-corrected entry, which recorded a wide-open camp battle with no leader. INDEPENDENTLY CORROBORATED BY THE WORKBOOK: the report that WSU opens Sept. 6 at Washington matches IMPORT SCHEDULE exactly (wk1 2026-09-06 Washington State Cougars @ Washington Huskies). DEVIATION IS EXACTLY ZERO AND VERIFIED: Pinnick was ALREADY the recorded baseline quarterback in column C before this activation, so the announced starter and the preseason assumption are the same player and no deviation applies. QB VALUES!G = F - D, so 0 - 0 = 0 and ENGINE!M contributes exactly nothing to any game. No nonzero QB adjustment and no model change.`

### 2.1 Verification you requested — baseline identity and zero deviation

| Check | Result |
|---|:--:|
| Is Pinnick already the preseason baseline quarterback? | **YES** — `C80` reads `Caden Pinnick` **today**, before any change, set 2026-08-04 |
| Does the announced starter equal the baseline? | **YES** — `C80` = `E80` proposed = `Caden Pinnick` |
| Does `C80` require editing? | **NO** — it is correct as-is and is proposed unchanged |
| Proposed `D80`, `F80` | `0` and `0` |
| Resulting `G80` = `F80 − D80` | **`0` — exactly zero** |
| Does `ENGINE!M` move? | **NO** — a zero delta contributes nothing to any game |

This is the cleanest possible activation: the workbook's 2026-08-04 entry recorded Pinnick as the
baseline **while explicitly refusing to call him the starter** (correctly, at `L`, since camp was
wide open). The announcement confirms the baseline assumption rather than departing from it, so the
zero is **literally** true, not merely conventional.

---

# ITEM 3 — COLORADO STATE, row 74 — TEXT / METADATA CORRECTION ONLY

| Field | Value |
|---|---|
| Team / abbrev | Colorado State Rams · `CSU` · row **74** |
| Current | `L` / **UNCERTAIN** |
| Proposed | **`L` / UNCERTAIN — unchanged** |
| Change class | **Record correction only. No numerical entry. No confidence change. No status change.** |
| Source | Existing — ESPN 2026 conference preview (`https://www.espn.com/college-football/story/_/id/48892618/2026-college-football-pac-12-conference-preview-predictions-transfers-more`), publication 2026 preseason; entry verified 2026-08-03 |
| Authority | Owner ruling, 2026-08-24: active field is `Hauss Hejny vs. K'saan Farrar`; Darius Curry may sit in a depth-room note but not the active competition field |
| Justification | Aligns the active field with the ruling. Competition remains genuinely unresolved, so `L` is retained and the gate stays closed. |

### Exact cells

| Cell | Current value | Proposed value | Type |
|---|---|---|---|
| `E74` | `Hauss Hejny (K'saan Farrar competing)` | `Hauss Hejny vs. K'saan Farrar` | text |
| `H74` | `L` | `L` — **unchanged** | — |
| `K74` | `2026-08-03` | `2026-08-24` | metadata |
| `L74` | prior verification note | note + `RULING` sentence (below) | text |
| `C74` `D74` `F74` `I74` `J74` | blank / blank / blank / ESPN / `2026` | **NO CHANGE** | — |
| **`G74`** `M74` | *(formulas)* | **DO NOT WRITE** | formula |

**Proposed `L74` addition** (appended to the existing 2026-08-03 note, which is retained verbatim):

> `RULING 2026-08-24: active competition field standardised to 'Hauss Hejny vs. K'saan Farrar'. Confidence L and status UNCERTAIN are UNCHANGED - this is a record correction only, with no numerical entry and no model effect. Darius Curry is not carried in the active competition field.`

### 3.1 ⚠️ Darius Curry does not appear anywhere in this workbook

I searched all 138 rows across every column of `QB VALUES`. **Darius Curry: 0 mentions.** He is not
in `E74`, not in `L74`, not on any other row.

Your instruction was permissive — Curry *may* remain in a depth-room note. Since he is **absent**,
"remain" has nothing to act on, and adding him would mean **introducing a new player name** into the
record rather than relocating an existing one. I have therefore **proposed no Curry entry**, and the
`L74` text above says only that he is not in the active field.

> **Please confirm one of these.** If the **live Google Sheet** carries Curry in Colorado State's
> active field, that is **live-vs-repo drift** worth knowing about independently, and I would add
> the removal to the manual live-Sheet list. If you want Curry recorded as a depth-room third, give
> me a source and I will draft that cell — I will not add a player name without one.

---

# 4. EVERY PROPOSED NUMERICAL ENTRY — COMPLETE LIST

| Cell | Value | Row |
|---|:--:|---|
| `D35` | **`0`** | Rutgers |
| `F35` | **`0`** | Rutgers |
| `D80` | **`0`** | Washington State |
| `F80` | **`0`** | Washington State |

**Total: 4 numerical entries. All four are the integer `0`. Zero nonzero values are proposed
anywhere in this packet.** Colorado State proposes **no** numerical entry.

Resulting deltas: `G35 = 0 − 0 = 0` · `G80 = 0 − 0 = 0` · `G74` stays blank.

---

# 5. CENSUSES — COMPUTED DIRECTLY FROM THE CURRENT WORKBOOK ROWS

Per your instruction, **no earlier projection was reused.** Both columns below were recomputed by
reading rows 6–143 of the v0.8.5 workbook and re-evaluating the `M` status rule
(`UNCERTAIN` if `G` blank **or** `H="L"` **or** `J≠2026`).

### Status

| | Current v0.8.5 | **After items 1–3** | Your expectation |
|---|:--:|:--:|:--:|
| OK | 108 | **110** | 110 ✅ |
| UNCERTAIN | 30 | **28** | 28 ✅ |
| Total | 138 | **138** | — |

### Confidence

| | Current v0.8.5 | **After items 1–3** |
|---|:--:|:--:|
| `H` | 72 | **73** |
| `M` | 40 | **40** |
| `L` | 26 | **25** |
| Total | 138 | **138** |

**Confidence census after this packet: `73 H / 40 M / 25 L`.**

**Derivation — only one confidence code moves.**

- **Rutgers is already `M`.** Activating at `M` changes **no** confidence code. It moves status only.
- **Washington State `L → H`** is the sole confidence movement: **−1 `L`, +1 `H`**.
- **Colorado State stays `L`.** No movement.
- Status: Rutgers and Washington State each clear UNCERTAIN → OK. **−2 UNCERTAIN, +2 OK.**

> **Note on the earlier projection.** The `72 H / 41 M / 25 L` figure carried into the last cycle was
> wrong in two places, and neither error is repeated here: it moved Rutgers `L → M` when Rutgers was
> **already** `M`, and it predated the Washington State announcement entirely. The correct current
> baseline is `72 H / 40 M / 26 L`, verified by direct row scan, and `73 H / 40 M / 25 L` after this packet.

---

# 6. FORMULAS AND MODEL OUTPUTS — CONFIRMED UNCHANGED

### Formulas

**No formula is written, edited or overwritten by this packet.** On all three rows, `G` and `M` are
explicitly marked **DO NOT WRITE** and remain the workbook's own formulas:

- `G{35,74,80}` = `=IF(OR($D_="",$F_=""),"",$F_-$D_)`
- `M{35,74,80}` = `=IF($A_="","",IF(OR($G_="",$H_="L",$J_<>SETTINGS!$B$3),"UNCERTAIN","OK"))`
- `A` and `B` remain formulas sourced from `TEAM MAP`.
- `J` is **not** rewritten on any row — it already reads `2026` on all three.

Every proposed write lands in a **value** cell: `C`, `D`, `E`, `F`, `H`, `I`, `K`, `L`.

### Model outputs

`ENGINE` reads only **three** columns of `QB VALUES` — `A`, `G` and `M` — established by scanning
all 123,011 formulas in the workbook. `H` is read only by `M` on the same sheet. So:

| Proposed change | Reaches the engine? |
|---|---|
| `C`, `E`, `I`, `K`, `L` text/metadata | **No** — not read by `ENGINE` at all |
| `H80` `L → H` | Only via `M80`, which changes UNCERTAIN → OK — a **gate**, not a number |
| `D`/`F` zeros | Via `G`, which computes to **`0`** — and `ENGINE!M` treats blank and `0` identically |

**Therefore every model output is unchanged**, including the five reference spreads:

`MEM at UNLV −5.6` · `UNC at TCU −4.2` · `NMSU at FSU −27.7` · `SJSU at USC −35.2` · `HAW at STAN −3.7`

After application, **every QB delta in the workbook would still be `0` or blank**, so `ENGINE!M`
contributes exactly nothing to any of the 888 games. Baseline preserved: **138 teams · 888 games ·
761 FBS-v-FBS · 127 FCS-involved · 0 BLOCK.** Market lines blank in the repo artifact · BET toggle
`N` · `B22`/`B23` blank · NDSU and Sacramento State transitional safeguards untouched.

### Week 0

None of Rutgers, Washington State or Colorado State plays in Week 0. **Memphis at UNLV remains the
single QB-gated Week 0 game**, unaffected. Washington State's first game is Week 1,
**Sunday 2026-09-06 at Washington** — 13 days out.

---

# 7. WHAT REMAINS OPEN AFTER THIS PACKET

If items 1–3 are approved, **28 teams remain UNCERTAIN.** Notable:

| Item | Row | State |
|---|:--:|---|
| **Texas Tech** — Will Hammond | 52 | `H` but gated: values blank pending **medical clearance**. QB1 identity not in question. |
| **Colorado State** | 74 | Stays `L` / UNCERTAIN **by design** — competition genuinely unresolved. |
| **Fresno State** | 75 | `L` / UNCERTAIN — `Open (Khristian Martin / Jayden Mandal)`. |
| Remaining 25 | — | Unresolved competitions, unchanged by this packet. |
| **Live-Sheet application** | — | v0.8.5 + NIU + Tulane sections remain **owner actions** — the connector cannot write cells. Not applied, not claimed as applied. |

**The QB closeout is NOT declared complete.**

---

# 8. APPROVAL REQUESTED

Nothing above has been applied. On your explicit approval I would build **v0.8.6** from frozen
v0.8.5 with a deterministic build script and a `verify_v086.py` identity certificate asserting
"v0.8.6 = v0.8.5 + exactly N cells, zero formula changes, exactly 4 zeros, zero nonzero QB values,"
then re-run the full validator chain.

Three points need an explicit answer:

1. **`C35 = Dylan Lonergan`** — approve, or withhold Rutgers entirely (see 1.1).
2. **Darius Curry** — confirm no entry, or supply a source (see 3.1).
3. **Confidence census** is **`73 H / 40 M / 25 L`**, not the earlier `72 H / 41 M / 25 L`.
   Status **110 OK / 28 UNCERTAIN** matches your expectation exactly.
