# LIVE GOOGLE SHEET → v0.8.8 SYNCHRONIZATION PACKET

> **READ-ONLY. NOTHING WAS WRITTEN TO THE LIVE SHEET.** No workbook, pointer, QB value, model
> setting or threshold was modified. This packet is for approval only.

**Generated:** 2026-08-26 · **Cutoff:** live Sheet as exported 2026-08-26 13:56 EDT

---

## 1. Headline

| | |
|---|:--:|
| **Cells requiring synchronization** | **252** |
| **Cells held pending your ruling** | **94** |
| Total differing cells | 346 |
| **Formula differences** | **0** ✅ |

**No formula differs anywhere in the workbook.** All 123,011 formula cells match between the live
Sheet and authoritative v0.8.8. Nothing is being prepared for formula overwrite, and there is no
formula stop-condition to report.

---

## 2. Preflight

| Check | Result |
|---|:--:|
| HEAD is `936fef1` | ✅ |
| Branch synchronized (0 ahead / 0 behind) | ✅ |
| Worktree clean | ✅ |
| Authoritative SHA-256 `b2a920fe…6450` | ✅ matched |
| `verify_v088` | ✅ **72 passed, 0 failed** |

---

## 3. What the live Sheet actually is — measured, not inferred

| | |
|---|---|
| **Title** | `TTW College Football Power Ratings v0.8.4 — PRODUCTION MASTER` |
| **File ID** | `1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA` |
| **Last modified** | 2026-08-26T13:20:46Z |
| **Tabs** | 21 — names and order **identical** to v0.8.8 |
| **Formula cells** | **123,011** — identical count to v0.8.8 |
| **Live banner** | `v0.8.4 AUTHORITATIVE … 69 H / 40 M / 29 L … 8 market lines loaded (Week 0), BET toggle = N` |

I did not take the version from the title or from earlier reports. I diffed the live export against
**repo v0.8.4** directly and measured the result:

> **LIVE = repo v0.8.4 + 102 live-only value cells, with ZERO formula differences.**
>
> MARKET LINES 72 · CHANGELOG 20 · QB VALUES 7 · SETTINGS 2 · banner 1

So the live Sheet is genuinely v0.8.4 content, plus operational data the owner added in the Sheet.
It has **not** received the v0.8.5, v0.8.6, v0.8.7 or v0.8.8 promotions.

---

## 4. EXPECTED ACCUMULATED CHANGES — 252 cells to synchronize

These are the four promotions the live Sheet has not yet received.

| Classification | Cells | Scope |
|---|:--:|---|
| **QB ACTIVATION** | **93** | v0.8.5 → v0.8.8 activations |
| **QB RECORD CORRECTION** | **25** | text/metadata corrections, no status change |
| **SCHEDULE DATE** | **133** | `IMPORT SCHEDULE!D`, every one **−1 day** (v0.8.8) |
| **BANNER** | **1** | `START HERE!A1` |
| **TOTAL** | **252** | |

### 4.1 QB VALUES — 118 cells across 20 rows

| Row | Team | Row | Team |
|:--:|---|:--:|---|
| 6 | Alabama | 76 | Oregon State |
| 7 | Arkansas | 80 | Washington State |
| 9 | Florida | 85 | Memphis |
| 18 | Tennessee | 89 | South Florida |
| 21 | Vanderbilt | 91 | Tulane |
| 29 | Nebraska | 113 | Ohio |
| 35 | Rutgers | 123 | Northern Illinois |
| 48 | Kansas | 125 | UNLV |
| 69 | Syracuse | 131 | Georgia Southern |
| 74 | Colorado State | 75 | Fresno State |

### 4.2 Schedule dates — 133 cells

All in `IMPORT SCHEDULE` column **D**, every change exactly **one calendar day backward**, per the
certified v0.8.8 venue-local rule. Includes the Week 0 gated game:
`401862693 Memphis @ UNLV` → **2026-08-30 → 2026-08-29**.

### 4.3 Banner — 1 cell

`START HERE!A1`: `v0.8.4 … 69 H / 40 M / 29 L … 8 market lines loaded (Week 0)`
→ `v0.8.8 … 76 H / 43 M / 19 L … 0 market lines loaded`

> ⚠️ **Note the banner conflict.** The v0.8.8 banner text says *"0 market lines loaded"*, but the
> live Sheet legitimately holds **8**. Writing the v0.8.8 banner verbatim would make the live banner
> **factually wrong about its own state**. See §6, ruling 4.

---

## 5. HELD PENDING RULING — 94 cells of live-only data

**None of these is prepared for overwrite.** Each exists in the live Sheet and not in the repo
artifact, so a blind push of v0.8.8 would **destroy** it.

### 5.1 MARKET LINES — 72 value cells, 8 Week 0 games

The repo artifact ships `MARKET LINES` **blank by design**; the live Sheet carries real lines dated
**2026-08-26** from FanDuel.

| Row | GameID | Favorite | Spread | Total |
|:--:|---|:--:|:--:|:--:|
| 6 | 401856766 | TCU | 7.5 | 47.5 |
| 7 | 401858201 | STAN | 3.5 | 48.5 |
| 8 | 401858202 | UVA | 5.5 | 53.5 |
| 9 | 401864494 | USC | 38.5 | 60.5 |
| 10 | 401864570 | FSU | 30.5 | 52.5 |
| 11 | 401864577 | NDSU | 7.5 | 46.5 |
| 12 | 401866408 | EMU | 9.5 | 52.5 |
| 13 | 401862693 | **UNLV** | **4.5** | 56.5 |

**Overwriting these would wipe the entire live Week 0 market card five days before kickoff.**

### 5.2 CHANGELOG — 20 cells, 7 live-authored rows

Rows 85–91 record v0.7.9, v0.8.3 and v0.8.4 go-live history written **in the Sheet** and never
carried into the repo artifact. Overwriting drops that history permanently.

### 5.3 SETTINGS — 2 cells

| Cell | Live | v0.8.8 | Meaning |
|---|:--:|:--:|---|
| `B4` | `0.0` | *(blank)* | results-through-week |
| `B5` | `2026-08-26` | *(blank)* | run date, drives line staleness |

**Verified harmless to ratings:** `TEAM RATINGS!J` short-circuits on `SETTINGS!$B$4<=1`, so `B4=0.0`
behaves exactly as blank and `K = I`. `B5` feeds only `CALC!Q` staleness. **Neither touches a
rating.** These are correct operational settings that the repo artifact simply does not ship.

### 5.4 ⚠️ Six owner-authored QB note cells inside the sync set

These are **not** stale v0.8.4 content — they are text the owner wrote directly in the Sheet, and
they differ from **both** repo v0.8.4 and v0.8.8. Synchronizing replaces them with repo wording.

| Cell | Team | Live-authored content |
|---|---|---|
| `QB VALUES!I75` | Fresno State | `Fresno State Athletics / KMPH, 2026-08-10/11 (…)` |
| `QB VALUES!K75` | Fresno State | `2026-08-21` |
| `QB VALUES!L75` | Fresno State | `2026-08-21 FINAL QB VERIFICATION: …` |
| `QB VALUES!L91` | Tulane | `2026-08-21 CLOSEOUT CORRECTION: Head coach Will Hall identif…` |
| `QB VALUES!I123` | Northern Illinois | `HERO Sports NIU quarterback report / NIU Athletics 2026 rost…` |
| `QB VALUES!L123` | Northern Illinois | `2026-08-21 CLOSEOUT CORRECTION: Current reporting identifies…` |

For **Tulane** the live note is superseded anyway — v0.8.8 activates the row. For **Fresno State**
and **Northern Illinois** the repo and live texts describe the same corrections in different words,
and both rows stay `L`/UNCERTAIN either way. **No status or value is affected.** Flagged because the
owner's own wording and citations would be lost.

---

## 6. Rulings required before any write

| # | Question | My recommendation |
|:--:|---|---|
| 1 | **MARKET LINES (72 cells)** — preserve the live Week 0 card, or overwrite it blank? | **PRESERVE.** Do not push blank values. |
| 2 | **CHANGELOG (20 cells)** — keep the live-authored history rows? | **PRESERVE**, and separately backfill them into the repo artifact. |
| 3 | **SETTINGS `B4`/`B5`** — keep live operational state? | **PRESERVE.** Proven not to affect ratings. |
| 4 | **Banner wording** — v0.8.8 says "0 market lines loaded" but live has 8. | **Write the version and census, but keep the live market-line clause** so the banner stays true. Needs your explicit wording approval — I will not improvise production banner text. |
| 5 | **Six owner-authored QB note cells** | Your call. Overwriting is safe for status and values; only wording is lost. |

---

## 7. Projected post-synchronization state — verified by simulation

I applied the 252 sync cells to an **in-memory copy** of the live export and recomputed everything
from the live workbook's own inputs. Nothing was written anywhere.

| Measure | Projected | Target | |
|---|:--:|:--:|:--:|
| QB status | **117 OK / 21 UNCERTAIN** | 117 / 21 | ✅ |
| Confidence | **76 H / 43 M / 19 L** | 76 / 43 / 19 | ✅ |
| QB zeros | **234** | 234 | ✅ |
| Nonzero QB values | **0** | 0 | ✅ |
| Games | **888 / 761 FBS-v-FBS / 127 FCS** | 888 / 761 / 127 | ✅ |
| Teams | 138 | 138 | ✅ |

### Five reference spreads — recomputed from the post-sync live workbook

| Game | Projected | Expected | |
|---|:--:|:--:|:--:|
| Memphis at UNLV | **UNLV −5.6** | UNLV −5.6 | ✅ |
| UNC at TCU | **TCU −4.2** | TCU −4.2 | ✅ |
| New Mexico State at Florida State | **FSU −27.7** | FSU −27.7 | ✅ |
| San José State at USC | **USC −35.2** | USC −35.2 | ✅ |
| Hawai'i at Stanford | **STAN −3.7** | STAN −3.7 | ✅ |

**All five match.** Model settings and the BET threshold are untouched: `B8` LEAN 1.0 ·
`B9` INVESTIGATE **1.5** · `B10` BET 3.0 · `B11` toggle `N` · `B12` cap 2.5 · `B13` stale 5 ·
weights `0.30 / 0.25 / 0.20 / 0.15`.

---

## 8. Unexpected drift

**None.** Every one of the 346 differing cells is explained:

- **252** are the four promotions the Sheet has not yet received (expected accumulation);
- **94** are live-only operational data and live-authored history (expected, and must be preserved);
- **0** are unexplained, and **0** are formula differences.

No cell fell into the `UNEXPECTED DRIFT` classification.

---

## 9. Deliverables

| File | Role |
|---|---|
| `live_sync_cells_v0.8.8.csv` | machine-readable, **sorted by sheet, row, column** — columns: `sheet, cell, row, column, column_letter, context, live_value, authoritative_value, expected_action, classification` |
| `build_live_sync_packet.py` | the read-only generator |
| `LIVE_SYNC_APPROVAL_v0.8.8.md` | this report |

---

## 10. Bottom line

> **252 live cells require synchronization.**
> **94 cells are held pending your ruling and must not be blindly overwritten.**
> **0 formulas differ.**

**Nothing was written to the live Google Sheet.** The connector cannot write cells in any case;
application remains a manual owner action. **Stopped for approval.**
