# TULANE ROW 91 — COMPLETE APPROVAL TABLE

**Status:** **READ-ONLY. NOT APPLIED.** Awaiting explicit approval.
**Base workbook:** v0.8.6 AUTHORITATIVE, **frozen at commit `c6bc5f8`, unmodified**
**Base SHA-256:** `bb76901a96a3fa63e14f0cc582891de82846c12fa5f7ce41d182c8addab967f9` *(re-verified this session)*
**Source packet:** `TTW_Tulane_Packet_and_Final_Sweep_20260824.md`, committed at `9dd5a43`

---

## 1. Every writable cell on row 91

| Cell | Current value | Proposed value | Type | Source / date | Rationale |
|---|---|---|---|---|---|
| **`C91`** | *(blank)* | `Zeon Chriss-Gremillion` | text | ESPN / Pete Thamel, **2026-08-24** | **Required.** All 110 OK rows in v0.8.6 carry a populated baseline QB — 110/110, no exceptions. Activating with a blank `C` would create the first OK row with no baseline, leaving a zero deviation that cannot be audited. The workbook's own 2026-08-21 note already records that the job "defaults to Chriss-Gremillion if no one separates," so he is the quarterback the preseason blend assumed. |
| **`D91`** | *(blank)* | **`0`** | **numeric** | — | Baseline value. `G = F − D`; deviation-only convention. |
| **`E91`** | `Open (Semonza / Chriss-Gremillion / Johnson / Bruno)` | `Zeon Chriss-Gremillion` | text | ESPN / Thamel, **2026-08-24** | Four-way camp competition resolved; he beat out Kadin Semonza. |
| **`F91`** | *(blank)* | **`0`** | **numeric** | — | Active value. Equals `D`, so the delta is exactly zero. |
| **`H91`** | `L` | **`M`** | confidence | ESPN / Thamel, **2026-08-24** | **Reporter-sourced**, not a team announcement. Thamel's "**Sources:** Tulane fifth-year senior Zeon Chriss-Gremillion will start…" is the same construction and tier as Georgia Southern, North Carolina and Rutgers — all activated at `M`. |
| **`I91`** | `FOX 8 New Orleans, 2026-07-24 (https://www.fox8live.com/2026/07/24/four-qbs-battling-starting-spot-tulane/)` | `ESPN / Pete Thamel 2026-08-24, carried by On3 (https://www.on3.com/news/tulane-names-zeon-chriss-gremillion-starting-quarterback-for-season-opener/)` | metadata | — | Replaces the 2026-07-24 four-way-battle citation. |
| **`K91`** | `2026-08-21` | `2026-08-24` | metadata (audit-trail date) | — | Last-update stamp. Not a QB value; not read by `ENGINE`. |
| **`L91`** | 2026-08-21 record-correction note | activation note *(full text in the source packet, §1.4)* | text | — | Records the naming, the `M`-not-`H` reasoning, the schedule corroboration, and the zero justification. |

### Formula cells — DO NOT WRITE

| Cell | Content | Status |
|---|---|---|
| **`G91`** | `=IF(OR($D91="",$F91=""),"",$F91-$D91)` | **DO-NOT-WRITE** — computes to `0` |
| **`M91`** | `=IF($A91="","",IF(OR($G91="",$H91="L",$J91<>SETTINGS!$B$3),"UNCERTAIN","OK"))` | **DO-NOT-WRITE** — resolves to `OK` |
| **`A91`** | `=IF('TEAM RATINGS'!$A91="","",'TEAM RATINGS'!$A91)` | **DO-NOT-WRITE** |
| **`B91`** | `=IF('TEAM RATINGS'!$A91="","",'TEAM RATINGS'!$B91)` | **DO-NOT-WRITE** |
| **`J91`** | `2026` | **DO-NOT-REWRITE** — already correct; rewriting risks the season gate |

---

## 2. Exact changed-cell count

| Sheet | Cells |
|---|:--:|
| `QB VALUES` row 91 — `C`, `D`, `E`, `F`, `H`, `I`, `K`, `L` | **8** |
| `START HERE!A1` — version banner + confidence census | **1** |
| **TOTAL** | **9** |

## 3. Every proposed numeric entry — complete

| Cell | Value |
|---|:--:|
| `D91` | **`0`** |
| `F91` | **`0`** |

**Two numeric entries. Both the integer `0`. No nonzero value is proposed anywhere.**
`G91 = 0 − 0 = 0`, so `ENGINE!M` contributes **nothing** to any of the 888 games.

## 4. Resulting census — computed directly from the v0.8.6 rows

| | v0.8.6 (frozen) | **After Tulane** |
|---|:--:|:--:|
| QB status | 110 OK / 28 UNCERTAIN | **111 OK / 27 UNCERTAIN** |
| Confidence | 73 H / 40 M / 25 L | **73 H / 41 M / 24 L** |
| Total | 138 | **138** |
| Nonzero QB values | 0 | **0** |

Tulane `L → M` is the only confidence movement: **−1 `L`, +1 `M`**; `H` unchanged at 73.

## 5. Formulas and model outputs — confirmed unchanged

- **No formula is written.** `G91`, `M91`, `A91`, `B91` remain the workbook's own formulas.
- `ENGINE` reads only `A`, `G`, `M` from `QB VALUES` — established by scanning all 123,011 formulas.
- The delta computes to `0`, and `ENGINE!M` treats blank and `0` identically.
- **Every model output is unchanged**, including `MEM at UNLV -5.6` · `UNC at TCU -4.2` ·
  `NMSU at FSU -27.7` · `SJSU at USC -35.2` · `HAW at STAN -3.7`.
- Baseline preserved: 138 teams · 888 games · 761 FBS-v-FBS · 127 FCS-involved · 0 BLOCK.
- Tulane does not play in Week 0. First game: Week 1, **2026-09-05 at Duke** — confirmed against the
  workbook's own schedule.

**Not applied. Awaiting your approval.**
