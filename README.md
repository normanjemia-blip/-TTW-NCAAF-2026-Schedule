# TTW College Football Power Ratings

Google Sheets–first college-football power-rating workbook: CFBD data in,
opponent-adjusted ratings out, your own market lines for edges. No picks
sold — just process.

> **The TTW Workbook Build Project is CLOSED** as of 2026-08-04 (Phase 7E, with a
> Phase 7E.1 documentation patch). Only monitoring sweeps remain. See the
> [maintenance certificate](promotion_v0.8.1/MAINTENANCE_CERTIFICATE.md) and the
> [promotion certificate](promotion_v0.8.0/PROMOTION_CERTIFICATE.md).

## Current authoritative version: **v0.8.9** ✅

| | |
|---|---|
| **Title** | **TTW College Football Power Ratings — v0.8.9 AUTHORITATIVE** |
| **Status** | APPROVED — current authoritative production workbook |
| **Release class** | **Spread BET rule + totals separation** over v0.8.8 — spread BET threshold 1.5 with the toggle enabled, totals thresholds and toggle moved to dedicated independent controls; **no QB, schedule, rating or model-output change** |
| **File** | [`promotion_v0.8.9/TTW_College_Football_Power_Ratings_v0.8.9_AUTHORITATIVE.xlsx`](promotion_v0.8.9/) |
| **SHA-256** | `334050660deb970f23cd9761490fb47e1f2b606b61d00a20c864cec529395cbb` |
| **Supersedes** | v0.8.8 — **frozen, unmodified**, and retained as the **immediate rollback**: `b2a920feddc0f49f0647957334db0ecd0e922fe6a3933fc6a11af31587b56450` (v0.8.7, v0.8.6, v0.8.5, v0.8.4, v0.8.3, v0.8.2, v0.8.1 also frozen) |
| **Promotion date** | 2026-08-18 (v0.8.3, and v0.8.2 earlier the same day) · 2026-08-04 (v0.8.0 → v0.8.1) |
| **Native Google Sheet** | **IMPORTED AND LIVE** — production master [`1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA`](https://docs.google.com/spreadsheets/d/1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA) *(the sheet carries v0.8.1; the v0.8.2 NMSU change is applied there separately by the owner)* |
| **Certificates** | [Promotion (v0.8.9)](promotion_v0.8.9/README.md) · [Promotion (v0.8.8)](promotion_v0.8.8/README.md) · [Promotion (v0.8.7)](promotion_v0.8.7/README.md) · [Promotion (v0.8.6)](promotion_v0.8.6/README.md) · [Promotion (v0.8.5)](promotion_v0.8.5/README.md) · [Promotion (v0.8.4)](promotion_v0.8.4/README.md) · [Promotion (v0.8.3)](promotion_v0.8.3/README.md) · [Promotion (v0.8.2)](promotion_v0.8.2/README.md) · [Maintenance (v0.8.1)](promotion_v0.8.1/MAINTENANCE_CERTIFICATE.md) · [Promotion (v0.8.0)](promotion_v0.8.0/PROMOTION_CERTIFICATE.md) |

**v0.8.1** corrects the `START HERE` banner, which still declared the workbook
*"NOT AUTHORITATIVE, NOT PROMOTED"* and cited 74 Tier-1 records instead of 73.
**Exactly one cell changed**; 20 of 21 worksheet XML parts byte-identical to v0.8.0;
43/43 regression PASS.

v0.8.0 delivers the completed **QB verification project**. v0.6.2 shipped with an
empty QB dataset — **0 of 138** confidence codes populated, so every team computed
UNCERTAIN. v0.8.0 populates all 138 records and independently verifies all **73 of 73**
Tier-1 records against team-specific primary sources, each stamped with a verification
date and evidence note.

**1,249 cell changes vs v0.6.2 · ZERO formula changes · 18 of 21 worksheet XML parts
byte-identical.** It cannot move a rating or a spread: no formula reads the confidence
code, and every QB delta is blank or 0.

## Rollback version: v0.6.2 (preserved, unmodified)

| | |
|---|---|
| **Title** | `TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE` |
| **Status** | PRESERVED — rollback target |
| **SHA-256** | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` |
| **Native Google Sheet** | production master [`1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA`](https://docs.google.com/spreadsheets/d/1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA) · archived v0.6.2 `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` (superseded rollback target) |
| **Deliverables** | [`workbook_v0.6.2_deliverables/`](workbook_v0.6.2_deliverables/) |
| **Procedure** | [`promotion_v0.8.0/ROLLBACK.md`](promotion_v0.8.0/ROLLBACK.md) |

`workbook_v0.6.2_deliverables/` is deliberately **not archived** — it must stay in
place as the rollback target. Neither Google Sheet was accessed by any phase of the QB
verification project.

## Production state (v0.8.1, clean preseason)

21 sheets · 123,011 formula cells · 888 games (761 FBS-vs-FBS, 127 FCS — NO PLAY) ·
0 BLOCKED · 0 DATA INCOMPLETE · 0 audit failures · 0 market lines · 0 adjustments ·
0 in-season stats · BET toggle = N.

**QB dataset:** 138/138 codes populated · **65 H / 40 M / 33 L** · 99 OK / 39 UNCERTAIN ·
39 blank / 99 zero numerical inputs · **0 nonzero QB values** · backlog 0 ·
audit-trail gap 0.

## Phase status

- **Phases 3–6.2:** CLOSED — schedule build, preseason sources, FCS — NO PLAY, operational testing, DATA INCOMPLETE repair.
- **Phases 7A–7D.5 (QB verification project):** COMPLETE — 11 defects found across 80 team-specific verification passes.
- **Promotion audit:** COMPLETE — 3-part adversarial audit, ~60 independent checks, **0 blockers**.
- **Phase 7E (authoritative promotion):** COMPLETE — **project closed**.
- **Phase 7E.1 (documentation maintenance patch):** COMPLETE — banner corrected, 43/43 regression PASS.
- **Phase 8.4 (fall-camp monitoring):** pipeline built, **first sweep not yet run** — run it next.
- **Phase V1 (VSiN reference library):** PAUSED — the guide upload produced a 1-byte file; nothing was indexed or integrated.

## Known limitations carried into production

1. **~~START HERE banner~~ — RESOLVED in v0.8.1.** One residual note: the workbook's internal `CHANGELOG` tab records history only through v0.7.9, because adding a row would have broken the *"only START HERE changed"* regression Phase 7E.1 required. The external record (certificates, manifest, this README) is complete. A **v0.8.2** patch could bring the internal changelog current if wanted.
2. **61 H-coded records were never independently verified** — out of declared Tier-1 scope. Missouri proved an H-tier assumption can go stale. Spot-check in the first sweep.
3. **The 33 L records are perishable** — depth charts land before the 2026-08-29 openers.
4. **Alabama's note is directionally contested** (Russell vs Mack); the `L` code is correct either way.
5. **Texas Tech is provisional** pending final medical clearance (~2026-08-21).
6. **No cached formula results** in either workbook — Excel/Sheets recalculate on open. Pre-existing, not a regression.

## Repository layout

- `promotion_v0.8.1/` — **the authoritative workbook**, maintenance certificate, regression log and diff.
- `promotion_v0.8.0/` — the promotion certificate, manifest, promotion notes, rollback procedure and archive index. Retained as an intermediate (cosmetic) rollback point.
- `workbook_v0.6.2_deliverables/` — **rollback target. Do not move, modify or delete.**
- `archive/candidates/` — the QB verification candidate line (v0.7.0 → v0.7.9), each with its own manifest, phase report, build script and verification log.
- `archive/pre_qb_project/` — pre-QB deliverables (v0.3.1 → v0.6.1).
- `phase8_4_qb_monitoring/` — fall-camp monitoring plan, the `pending_qb_resolutions` ledger, and the QB resolution → candidate build pipeline. **Run the first sweep next.**
- `phase7_preseason_calibration/` — the override standard, deferred-trigger register and source-conflict log that govern future rating changes.
- `TTW_2026_Verified_Schedule_ESPN_v1.0.csv`, `TTW_2026_Schedule_Reconciliation_Report.md`, `raw_espn/`, `scripts/`, `validate_schedule.py` — the Phase 3 schedule build and its provenance.

See [`PROJECT_MANIFEST.json`](PROJECT_MANIFEST.json) for the machine-readable version registry.
