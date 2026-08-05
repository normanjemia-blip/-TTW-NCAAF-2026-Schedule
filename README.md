# TTW College Football Power Ratings

Google Sheets–first college-football power-rating workbook: CFBD data in,
opponent-adjusted ratings out, your own market lines for edges. No picks
sold — just process.

> **The TTW Workbook Build Project is CLOSED** as of 2026-08-04 (Phase 7E).
> Only monitoring sweeps remain. See
> [`promotion_v0.8.0/PROMOTION_CERTIFICATE.md`](promotion_v0.8.0/PROMOTION_CERTIFICATE.md).

## Current authoritative version: **v0.8.0** ✅

| | |
|---|---|
| **Title** | **TTW College Football Power Ratings — v0.8.0 AUTHORITATIVE** |
| **Status** | APPROVED — current authoritative production workbook |
| **File** | [`promotion_v0.8.0/TTW_College_Football_Power_Ratings_v0.8.0_AUTHORITATIVE.xlsx`](promotion_v0.8.0/) |
| **SHA-256** | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` |
| **Promotion date** | 2026-08-04 |
| **Promoted from** | `v0.7.9_CANDIDATE` — **byte-for-byte** (identical SHA-256) |
| **Native Google Sheet** | **NOT YET IMPORTED** — the sheet still holds v0.6.2; import is an owner action |
| **Certificate** | [`promotion_v0.8.0/PROMOTION_CERTIFICATE.md`](promotion_v0.8.0/PROMOTION_CERTIFICATE.md) |

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
| **Native Google Sheet** | [`1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc`](https://docs.google.com/spreadsheets/d/1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc) |
| **Deliverables** | [`workbook_v0.6.2_deliverables/`](workbook_v0.6.2_deliverables/) |
| **Procedure** | [`promotion_v0.8.0/ROLLBACK.md`](promotion_v0.8.0/ROLLBACK.md) |

`workbook_v0.6.2_deliverables/` is deliberately **not archived** — it must stay in
place as the rollback target. Neither Google Sheet was accessed by any phase of the QB
verification project.

## Production state (v0.8.0, clean preseason)

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
- **Phase 8.4 (fall-camp monitoring):** pipeline built, **first sweep not yet run** — run it next.
- **Phase V1 (VSiN reference library):** PAUSED — the guide upload produced a 1-byte file; nothing was indexed or integrated.

## Known limitations carried into production

1. **`START HERE!A1` banner is stale** — it still reads *"v0.7.9 … NOT AUTHORITATIVE, NOT PROMOTED"* and says *"74 Tier-1 records"* when the correct figure is **73**. Deliberately not corrected: Phase 7E required byte-identity to the audited candidate. No formula reads either string. A banner-only **v0.8.1** patch (2 cells) is available on request.
2. **61 H-coded records were never independently verified** — out of declared Tier-1 scope. Missouri proved an H-tier assumption can go stale. Spot-check in the first sweep.
3. **The 33 L records are perishable** — depth charts land before the 2026-08-29 openers.
4. **Alabama's note is directionally contested** (Russell vs Mack); the `L` code is correct either way.
5. **Texas Tech is provisional** pending final medical clearance (~2026-08-21).
6. **No cached formula results** in either workbook — Excel/Sheets recalculate on open. Pre-existing, not a regression.

## Repository layout

- `promotion_v0.8.0/` — **the authoritative workbook** plus its certificate, manifest, promotion notes, rollback procedure, and archive index.
- `workbook_v0.6.2_deliverables/` — **rollback target. Do not move, modify or delete.**
- `archive/candidates/` — the QB verification candidate line (v0.7.0 → v0.7.9), each with its own manifest, phase report, build script and verification log.
- `archive/pre_qb_project/` — pre-QB deliverables (v0.3.1 → v0.6.1).
- `phase8_4_qb_monitoring/` — fall-camp monitoring plan, the `pending_qb_resolutions` ledger, and the QB resolution → candidate build pipeline. **Run the first sweep next.**
- `phase7_preseason_calibration/` — the override standard, deferred-trigger register and source-conflict log that govern future rating changes.
- `TTW_2026_Verified_Schedule_ESPN_v1.0.csv`, `TTW_2026_Schedule_Reconciliation_Report.md`, `raw_espn/`, `scripts/`, `validate_schedule.py` — the Phase 3 schedule build and its provenance.

See [`PROJECT_MANIFEST.json`](PROJECT_MANIFEST.json) for the machine-readable version registry.
