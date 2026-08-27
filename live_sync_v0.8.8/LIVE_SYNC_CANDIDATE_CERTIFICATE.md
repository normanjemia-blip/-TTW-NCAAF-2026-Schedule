# LIVE-SYNC CANDIDATE — CERTIFICATE AND APPROVAL REPORT

> **CANDIDATE ONLY. THE LIVE GOOGLE SHEET WAS NOT WRITTEN.**
> Authoritative v0.8.8 unmodified. No pointer repointed. No formula or setting altered.

**Built:** 2026-08-26 · from live-sync packet `d9b6425`

| | |
|---|---|
| **Candidate** | `live_sync_v0.8.8/TTW_LIVE_SYNC_CANDIDATE_v0.8.8.xlsx` |
| **Candidate SHA-256** | `474490c826b86a3620871c3467dc93e32523c7f3d28ed2fbfa1b7c1061ba26de` |
| **Base** | live Google Sheet export · `78d7151c…a3b3` — verified unmodified |
| **Sync source** | authoritative v0.8.8 · `b2a920fe…6450` — verified unmodified |
| **Certificate** | `verify_live_sync_candidate.py` — **36 passed, 0 failed** |
| **Cells written** | **246** |

---

## 1. Write count — computed independently

| | |
|---|:--:|
| Proposed synchronization cells (from the approved CSV) | 252 |
| Less preserved owner-authored QB notes | −6 |
| **Write count** | **246** ✅ |

The build **stops** unless the recomputed count is exactly 246. It was.

| Sheet | Cells |
|---|:--:|
| `IMPORT SCHEDULE` | 133 |
| `QB VALUES` | 112 |
| `START HERE` | 1 |

By class: 133 schedule date · 92 QB activation · 20 QB record correction · 1 banner.

---

## 2. Rulings applied

| # | Ruling | Result |
|:--:|---|:--:|
| 1 | Preserve 72 live MARKET LINES cells | ✅ checks 3.1–3.3 |
| 2 | Preserve 20 live CHANGELOG cells | ✅ check 3.4 |
| 3 | Preserve `SETTINGS!B4` / `B5` | ✅ checks 3.5, 3.6 |
| 4 | Preserve six owner QB notes | ✅ six individual checks |
| 5 | Apply every other approved change | ✅ 246 applied, check 8.1 |
| 6 | Banner = v0.8.8 with "0 market lines loaded" → "8 market lines loaded" | ✅ checks 4.1–4.4 |
| 7 | No other banner or metadata correction | ✅ check 4.4 proves reversal reproduces v0.8.8 exactly |

Preserved owner notes: `QB VALUES!I75 K75 L75` (Fresno State) · `L91` (Tulane) ·
`I123 L123` (Northern Illinois).

**Resulting banner:** `… (v0.8.8 AUTHORITATIVE — promotion complete 2026-08-04. … 76 H / 43 M / 19 L;
0 nonzero QB values. Preseason state: 8 market lines loaded, BET toggle = N.)`

---

## 3. Certificate results — 36 / 0

| Requirement | Check | Result |
|---|---|:--:|
| 123,011 formulas byte-identical | 1.2, 2.1 | **123,011**, zero formula changes |
| All eight market lines exact | 3.1, 3.2, 3.3 | 8 rows, **72** value cells intact |
| 20 changelog cells exact | 3.4 | `[]` |
| `SETTINGS!B4`/`B5` exact | 3.5, 3.6 | `0`, `2026-08-26` |
| Six owner-note cells exact | 3.x | all six |
| 117 OK / 21 UNCERTAIN | 5.1 | ✅ |
| 76 H / 43 M / 19 L | 5.2 | ✅ |
| 234 QB zeros, 0 nonzero | 5.3, 5.4 | ✅ |
| 888 / 761 / 127 | 7.1 | ✅ |
| 133 approved schedule dates present | 6.1, 6.2, 6.3 | 133 applied, all −1 day |
| Five reference spreads | 7.x | all five match |
| No unexplained drift | 8.1 | every changed cell is approved |

Reference spreads: `UNLV −5.6` · `TCU −4.2` · `FSU −27.7` · `USC −35.2` · `STAN −3.7`.

---

## 4. Operational impact of the approved QB activations, with the 8 market lines live

**Zero change to any dashboard label, gate, edge or side on the lined games.**

| Game | Market | Model | Edge | Label before | Label after | Gate before | Gate after |
|---|---|---|:--:|---|---|---|---|
| SAC @ EMU | EMU −9.5 | EMU −4.8 | −4.67 | INVESTIGATE | INVESTIGATE | READY | READY |
| NMSU @ FSU | FSU −30.5 | FSU −27.7 | −2.76 | INVESTIGATE | INVESTIGATE | READY | READY |
| JVST @ NDSU | NDSU −7.5 | NDSU −7.0 | −0.54 | *(blank)* | *(blank)* | READY | READY |
| HAW @ STAN | STAN −3.5 | STAN −3.7 | +0.24 | *(blank)* | *(blank)* | READY | READY |
| UNC @ TCU | TCU −7.5 | TCU −4.2 | −3.34 | INVESTIGATE | INVESTIGATE | READY | READY |
| **MEM @ UNLV** | UNLV −4.5 | UNLV −5.6 | +1.14 | LEAN | LEAN | **QB UNCERTAIN** | **QB UNCERTAIN** |
| SJSU @ USC | USC −38.5 | USC −35.2 | −3.31 | INVESTIGATE | INVESTIGATE | READY | READY |
| NCST @ UVA | UVA −5.5 | UVA −5.3 | −0.17 | *(blank)* | *(blank)* | READY | READY |

**Games with any change: 0.** Every activation carries a zero QB deviation, so no model spread moves,
and no lined game's gate flips. **Memphis @ UNLV correctly stays QB-gated** — UNLV activated, but
Memphis remains deliberately unresolved until kickoff.

**Where the activations do show up:** across all 761 FBS-v-FBS games, QB-gated games fall
**323 → 206** — 117 games released from the QB gate. None of them currently carries a market line.

> **Correction to my earlier packet.** The operational table in the previous message showed some of
> these games as `BET`. That came from my own simplified reconstruction (`|edge| ≥ B10 → BET`), which
> ignored the `SETTINGS!B11 <> "Y"` toggle in the real `ENGINE!X` formula. The table above uses the
> workbook's formula verbatim. **With the toggle at `N`, `BET` is currently unreachable at any edge**
> — see the threshold audit. The gate and edge figures were unaffected by that error.

---

## 5. Scope confirmations

| | |
|---|:--:|
| Authoritative v0.8.8 modified | **No** — SHA re-verified |
| Live export modified | **No** — SHA re-verified |
| Repository pointers repointed | **No** |
| QB values / model settings / 1.5 threshold altered | **No** |
| New QB or schedule research | **None** |
| **Live Google Sheet written** | **NO** |

---

## 6. Files

| File | Role |
|---|---|
| `TTW_LIVE_SYNC_CANDIDATE_v0.8.8.xlsx` | the candidate workbook |
| `build_live_sync_candidate.py` | deterministic build; stops unless the count is 246 |
| `verify_live_sync_candidate.py` | certificate — read-only, 36 checks |
| `live_sync_cells_v0.8.8.csv` | the 346-cell comparison |
| `THRESHOLD_AUDIT_1.5.md` · `threshold_audit.py` | Part B |

**Stopped for approval. No live-Sheet write has occurred or is scheduled.**
