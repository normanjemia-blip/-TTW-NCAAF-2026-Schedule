# FINAL LIVE v0.8.9 CANDIDATE — CERTIFICATE

> **THE LIVE GOOGLE SHEET WAS NOT WRITTEN. Its Drive title was NOT renamed.**
> Two independent blockers stop the write; both are described in §7. The repository promotion
> (complete) and the live synchronization (outstanding) are **two separate outcomes**.

| | |
|---|---|
| **Final live candidate** | `live_sync_v0.8.9/TTW_LIVE_CANDIDATE_v0.8.9.xlsx` |
| **SHA-256** | `131703870095f6e3ddebaf7df368259d55e9c5e8510e39e90d1356cbfeb31dd5` |
| **Built from** | fresh live export `ecab9034…da8d` + authoritative v0.8.9 `33405066…5cbb` |
| **Certificate** | `verify_final_live_candidate.py` — **47 passed, 0 failed** |
| **Write cells** | **1,265** |
| **Preserved operational cells** | **100** |
| **Held back for approval** | **4** (`CHANGELOG A87:D87`) |
| **Pre-write rollback snapshot** | `PREWRITE_ROLLBACK_SNAPSHOT_2026-08-28.xlsx` · `ecab9034…da8d` |

---

## 1. The live Sheet changed since the previous export

| | |
|---|---|
| Previous export | `78d7151c…a3b3` |
| Fresh export (`modifiedTime` **2026-08-28T13:05:04Z**) | `ecab9034…da8d` |
| Differing cells | **34** |
| **Formula differences** | **0** |
| Structural drift | **none** — 21 sheets, same names and order |

Every one of the 34 falls inside an already-approved operational category:

| Cells | What changed | Category |
|:--:|---|---|
| 8 | `MARKET LINES` D — spreads re-priced | MARKET LINES |
| 6 | `MARKET LINES` E — totals re-priced | MARKET LINES |
| 8 | `MARKET LINES` F — source relabelled *"FanDuel Sportsbook live Week 0 odds"* | source metadata |
| 8 | `MARKET LINES` G — line date `2026-08-26` → `2026-08-28` | date metadata |
| 8 | `MARKET LINES` H — retrieval note `09:18 ET` → `2026-08-28 09:03 ET` | source metadata |
| 1 | `SETTINGS!B5` as-of date `2026-08-26` → `2026-08-28` | SETTINGS B4/B5 |

**No unexplained drift.** Nothing outside those categories moved.

### Re-priced lines

| Game | Spread | Total |
|---|---|---|
| UNC @ TCU | 7.5 → **8.5** | 47.5 → **46.5** |
| NCST @ UVA | 5.5 → **4.5** | 53.5 → **51.5** |
| NMSU @ FSU | 30.5 → **32.5** | 52.5 → **53.5** |
| JVST @ NDSU | 7.5 → **6.5** | — |
| SJSU @ USC | — | 60.5 → **61.5** |
| SAC @ EMU | — | 52.5 → **53.5** |
| HAW @ STAN · MEM @ UNLV | — | — |

## 2. Classifications recomputed from the fresh lines

The fresh export is authoritative for market-line-dependent results. The prior four-game
expectation was **not assumed** — every edge was recomputed:

| Game | Edge (prior → fresh) | Label | Gate |
|---|---:|---|---|
| UNC @ TCU | −3.34 → **−4.34** | **BET** | READY |
| SJSU @ USC | −3.31 → −3.31 | **BET** | READY |
| NMSU @ FSU | −2.76 → **−4.76** | **BET** | READY |
| SAC @ EMU | −4.67 → −4.67 | **BET** | READY |
| MEM @ UNLV | +1.14 → +1.14 | LEAN | **QB UNCERTAIN** |
| NCST @ UVA | −0.17 → **+0.83** | *(blank)* | READY |
| JVST @ NDSU | −0.54 → **+0.46** | *(blank)* | READY |
| HAW @ STAN | +0.24 → +0.24 | *(blank)* | READY |

**BET list from the fresh lines: SAC@EMU, UNC@TCU, SJSU@USC, NMSU@FSU** — the same four, but
reached by recomputation. Four edges moved materially; none crossed the 1.5 boundary. Memphis at
UNLV keeps a LEAN edge classification and remains blocked by the QB gate.

Market lines loaded = **8**, counted by the workbook's own rule (`AUDIT!B16`:
`SUMPRODUCT(--('MARKET LINES'!$A$6:$A$1005<>""))`, i.e. populated GameID game-rows), not by
populated cells.

## 3. Write set — 1,265 cells, recomputed not carried over

Computed directly from a full cell diff of the fresh export against authoritative v0.8.9:

| Sheet | Write cells |
|---|:--:|
| `ENGINE` | 1,000 |
| `IMPORT SCHEDULE` | 133 |
| `QB VALUES` | 112 |
| `SETTINGS` | 15 |
| `AUDIT` | 4 |
| `START HERE` (banner) | 1 |
| **Total** | **1,265** |

**Reconciliation.** The earlier estimate was 1,269 (246 + 1,024 − 1). The 4 held-back CHANGELOG
cells account for the whole difference: **1,269 − 4 = 1,265**. The 34 fresh-export changes all
landed in the preserved overlay, so they do not move the write count. The stale expectation was
recomputed rather than reused.

Per-cell listing: `live_write_packet_v0.8.9.csv`.

## 4. Preserved operational overlay — 100 cells, all exact

| Category | Cells |
|---|:--:|
| `MARKET LINES` — spreads, totals, sources, line dates, retrieval notes | 72 |
| Live-authored `CHANGELOG` history (rows 87–91) | 20 |
| Owner-authored QB notes — Fresno State `I75`/`K75`/`L75`, Tulane `L91`, Northern Illinois `I123`/`L123` | 6 |
| `SETTINGS!B4` / `B5` | 2 |

Verified byte-identical to the fresh export. **No preserved cell appears in the write list** —
asserted, not assumed.

## 5. Certificate — 47 proofs, 0 failures

| § | Proves | Result |
|:--:|---|:--:|
| 0 | Inputs unmodified; 21 sheets, names and order preserved | ✅ |
| 1 | **Zero** formula cells differ from authoritative v0.8.9; no Sheets-compatibility equivalent needed; every other difference is a preserved cell or the banner | ✅ |
| 2 | All 100 preserved operational cells exact | ✅ |
| 3 | **117 OK / 21 UNCERTAIN** · **76 H / 43 M / 19 L** · **234 QB zeros, zero nonzero** · **888 / 761 / 127** | ✅ |
| 4 | Spread BET threshold **1.5**; ±1.50 **is** BET, ±1.49 is not; totals **2.0/3.0/6.0**; totals toggle **N**; totals inert; totals BET unreachable at every fixture | ✅ |
| 5 | Both audit guards **OK**; `ENGINE!AB` references neither `B10` nor `B11` | ✅ |
| 6 | Classifications recomputed from the fresh lines; BET list reported; Memphis QB-gated; no totals label activates | ✅ |
| 7 | Banner: v0.8.9, promotion date 2026-08-27, **8 market lines loaded**, no stale v0.8.8, otherwise identical to authoritative | ✅ |
| 8 | CHANGELOG conflict held back; live entry intact; authoritative entry written nowhere; nothing overwritten, moved or appended | ✅ |

**A defect this caught:** check 1.3's allow-list omitted the banner, so it failed on
`START HERE!A1`. The banner's single intended difference from authoritative is already proven
exactly by check 7.5; the check was corrected, not the candidate.

## 6. CHANGELOG conflict — **STOPPED, awaiting approval**

Authoritative v0.8.9 writes its entry at `CHANGELOG` **row 87**. The live Sheet already occupies
that row with a live-authored entry. Per safety correction 5 it is **neither overwritten, moved
nor appended**.

**Live `CHANGELOG` row 87** — `v0.8.3` · `2026-08-19`
> GO-LIVE: replaced the Phase 2 zero-market-row invariant with the validated operational MARKET
> LINES invariant; loaded eight Week 0 Circa spreads/totals from the owner-supplied OddsLogic
> screenshot captured 2026-08-18 11:10 PM ET; set Current week = 0 and As-of date = 2026-08-18.
> All eight rows resolve with no flags or duplicates. BET remains N; totals model remains
> unavailable; no rating, QB value, adjustment, or model formula changed.

*Source: Owner-supplied market screenshot; v0.8.3 repo guardrail commit 05b8a52*

**Authoritative v0.8.9 row 87** (held back) — `v0.8.9` · `2026-08-26`
> SPREAD BET RULE + TOTALS SEPARATION. (1) Spread BET threshold SETTINGS!B10 changed from 3.0 to
> 1.5… (2) Spread BET labels enabled — SETTINGS!B11 N → Y; B11 now controls SPREADS ONLY.
> (3) Totals thresholds separated onto dedicated cells B49/B50/B51 and PRESERVED at exactly
> 2.0 / 3.0 / 6.0… (4) Totals BET toggle separated onto dedicated cell B52 and RETAINED at N…
> (5) No projection, rating, edge, side or totals output changed… SUPERSEDES v0.8.9 REV 1.

*Source: Approved spread-threshold rule; REV 1 superseded*

**Exact conflicting cells:** `CHANGELOG!A87`, `B87`, `C87`, `D87`.

**Proposed first safe alternative row: `CHANGELOG` row 92** — the live history ends at row 91, and
row 92 is completely empty across every column (verified A–S). **Awaiting approval.**

## 7. Why the live Sheet was not written — two independent blockers

1. **CHANGELOG conflict (§6).** Safety correction 5 requires a stop before the live write.
2. **The connector cannot perform exact cell writes.** The available Google Drive tools are
   metadata- and file-level only — `update_file` accepts nothing but title and parent_id, and
   there is no Sheets values/range API. The only ways to push content would be `create_file` or
   `copy_file`, i.e. whole-workbook replacement, which safety correction 8 forbids. No partial
   approximation was attempted.

Per safety correction 8 the deliverables are the certified XLSX and the exact write packet, both
present. **One owner/Google-Sheets-capable write remains outstanding.**

## 8. Scope confirmations

| | |
|---|:--:|
| Live Google Sheet written | **NO** |
| Live Drive title renamed | **NO** — still *"…v0.8.4 — PRODUCTION MASTER"* |
| Whole-sheet replacement or workbook import attempted | **NO** |
| Any preserved operational cell in the write list | **NO** |
| CHANGELOG entry overwritten, moved or appended | **NO** |
| Totals enabled | **NO** — `B22`/`B23` blank, totals toggle `N` |
| Authoritative v0.8.9 or the fresh export modified | **No** — both re-hashed after the build |
