# Phase 8.3 — Methodology Cleanup, Vanderbilt Re-Verification & v0.7.2 CANDIDATE

**Status: CANDIDATE — NOT AUTHORITATIVE, NOT PROMOTED. No nonzero QB
deviation exists. No Google Sheet was edited.**

- **Candidate workbook:** `TTW_NCAAF_Power_Ratings_2026_v0.7.2_QB_VALUES_CANDIDATE.xlsx`
- **Source:** `../workbook_v0.7.1_QB_values_working/TTW_NCAAF_Power_Ratings_2026_v0.7.1_QB_VALUES_WORKING.xlsx`
  (v0.7.1 SHA `608068e5…`, preserved unmodified).
- **v0.7.2 SHA-256:** `82ee5b3d4731c18a2deb3288d63c9b6eb8e1dae4bc5c28bb6be0cdebf151a183`
- **Untouched:** authoritative v0.6.2 XLSX; v0.6.2 Google Sheet
  (`1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc`); v0.6.1 rollback sheet
  (`1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo`); v0.7.1 working workbook.

## Headline result: Vanderbilt re-verification FAILED

The Phase 8.2 recommendation to reclassify Vanderbilt **L → M** and zero-init
it was **re-verified against fresh current sources and REJECTED**.

At **Vanderbilt's SEC Media Days session (2026-07-21)**, HC **Clark Lea**
declined to name a starting QB and confirmed a **genuine, undecided
competition** between five-star freshman **Jared Curtis** and veteran **Blaze
Berlowitz** (two seasons in OC Tim Beck's system, Diego Pavia's 2025 backup —
"knows the system better and has more experience" right now); the battle may
run to the opener vs Austin Peay, and both QBs may play. This **fails** both
"consistently projected Day-1 starter" and "uncontested by a genuine equal
competitor."

The Low is **not** driven by Curtis's freshman status (the guardrail against
that was honored); it reflects a **real open competition**. Therefore
Vanderbilt **stays L / UNCERTAIN — not reclassified, not initialized.**

**Because re-verification failed, the workbook carries no QB-data change.**
Final QB status counts remain **105 OK / 33 UNCERTAIN** (not the 106 / 32 that
a successful Vanderbilt update would have produced). See
`vanderbilt_verification_note.md`.

## What changed in the workbook (v0.7.2 vs v0.7.1)

Only **13 cells**, all text/metadata — **no QB VALUES data, no formulas**:

| Sheet | Cells | Change |
|---|---|---|
| START HERE | `A1` (1) | Version banner → v0.7.2 CANDIDATE (notes Vanderbilt re-verified, stays UNCERTAIN) |
| CHANGELOG | `A64:D66` (12) | 3 rows documenting the failed re-verification, the null result, and the doc cleanup |

`QB VALUES` is unchanged. Formula count is **exactly 123,011** in both files;
every formula coordinate and text is identical (no formula overwritten). See
`changed_cells_v072.csv` / `.json` and `workbook_verification_report_v072.txt`.

## Documentation corrections (Phase 8.3)

1. **`future_qb_deviation_rubric.md` — corrected bands.** The negative bands
   no longer overlap; each classification now uses **discrete quarter-point
   values** (e.g., `−0.50` is *functionally equivalent* only; `−0.75` is the
   first *minor downgrade* step). Max deviation stays **−4.00 to +2.00**;
   quarter-point increments only; **no backdoor QB value via ADJUSTMENTS** —
   anything outside the bounds needs a formal methodology amendment.
2. **`qb_deviation_review_log.csv` / `.json` — new, empty.** A **separate**
   future-use audit log (27-field schema + validation rules, **no records**),
   created because the exception tracker never contained review-log columns.
3. **`valuation_methodology_report.md` — corrected.** Now references the
   separate review log (not "tracker columns") and the corrected discrete
   bands.
4. **`qb_exception_resolution_tracker.csv` / `.json` — dated.** Added ISO
   fields `last_checked_date`, `most_recent_source_date`, `next_research_date`,
   `resolution_date`. Existing descriptive data kept; exact source dates left
   blank where unavailable (only Vanderbilt has a precise `2026-07-21`).
   Practical next-research dates assigned per case type (open competition &
   conflicting sourcing → early fall camp `2026-08-03`; injury → medical
   checkpoint, `TTU 2026-08-21`, others `2026-08-03`).

## Verification (all PASS)

- 21 sheets; order + visibility unchanged.
- Formula count **123,011** in both files; **no formula overwritten/added/removed**.
- Only START HERE (1) + CHANGELOG (12) differ; **QB VALUES unchanged**.
- D/F contain only 0 or blank; **105 zero / 33 blank**; no nonzero delta.
- All 138 research rows present; A/B/G/M formulas intact.
- Vanderbilt (row 21): D/F blank, Active QB = Jared Curtis, Confidence L
  (unchanged).
- **Live-calc: 105 status OK / 33 UNCERTAIN / 0 nonzero deltas** (see report).

## Files

| File | Purpose |
|---|---|
| `TTW_NCAAF_Power_Ratings_2026_v0.7.2_QB_VALUES_CANDIDATE.xlsx` | The candidate workbook (banner + CHANGELOG only vs v0.7.1). |
| `future_qb_deviation_rubric.md` | **CORRECTED** — discrete non-overlapping quarter-point deviation values; no-backdoor rule. |
| `valuation_methodology_report.md` | **CORRECTED** — references the separate review log + corrected bands. |
| `qb_deviation_review_log.csv` / `.json` | **NEW (empty)** — 27-field review-log schema + validation rules; no records. |
| `qb_exception_resolution_tracker.csv` / `.json` | **UPDATED** — added 4 ISO date fields; Vanderbilt re-verification recorded. |
| `qb_exception_resolution_playbook.md` | Updated — Vanderbilt section now records the rejected reclassification. |
| `vanderbilt_verification_note.md` | **NEW** — the fresh re-verification, criteria table, sources + dates, FAILED result. |
| `changed_cells_v072.csv` / `.json` | Exact 13-cell changed-cell audit (banner + CHANGELOG). |
| `workbook_verification_report_v072.txt` | Full structural verification + live-calc status counts. |
| `MANIFEST.md` | File inventory with SHA-256 checksums. |
| `scripts/` | `build_v072.py`, `verify_v072.py`, `livecalc_v072.py`, `changed_cells_v072.py`, `update_tracker_dates.py`, `build_review_log.py`. |

Carried-forward research artifacts (unchanged this phase) remain in
`../workbook_v0.7.1_QB_values_working/` (`qb_research.csv/json`,
`source_audit.md`, `baseline_identity_audit.md`, `teams_initialized.md`,
`teams_uncertain.md`, `post_rating_changes.md`, `phase8_2_review_note.md`).

## Constraints honored

No other exception was resolved; no nonzero QB deviation was entered; the
authoritative v0.6.2 workbook was not modified; **neither Google Sheet was
edited**; v0.7.2 was **not promoted**; no market-line entry, adjustments, or
preseason activation was begun. Work stops after building and verifying the
candidate.
