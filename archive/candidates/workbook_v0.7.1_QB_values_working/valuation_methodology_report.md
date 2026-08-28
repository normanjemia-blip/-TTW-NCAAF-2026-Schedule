# QB Valuation Methodology Report (CORRECTED — Phase 8.2)

**Framework: permanently DEVIATION-ONLY. There is no absolute cross-team QB
tier scale in columns D or F.** Every value is relative to a team's own
preseason baseline quarterback. This report supersedes the Phase 8.0/8.1
proposal (which floated an "absolute tier" Option B and a tier-based
Section B — both are withdrawn; see `phase8_2_review_note.md`).

## 1. Finding (unchanged): no pre-existing numerical rubric

The project's DICTIONARY / SETTINGS / architecture docs contain no QB-value
scale (confirmed in the v0.4 and v0.5.1 findings). This methodology is the
approved replacement, built to match the workbook's existing baseline–delta
formulas without inventing an absolute scale.

## 2. What the workbook formulas require

- `QB VALUES!G` (delta) `=IF(OR($D6="",$F6=""),"",$F6-$D6)` →
  **delta = Active value − Baseline value** (points of game margin;
  positive = active QB better than baseline).
- `QB VALUES!M` (status) `=IF($A6="","",IF(OR($G6="",$H6="L",$J6<>SETTINGS!$B$3),"UNCERTAIN","OK"))`.
- `ENGINE!M` consumes the delta as points added to the team's projected
  margin. DICTIONARY: "only deltas move projections."

## 3. Approved framework — DEVIATION-ONLY (Option A), APPLIED in v0.7.1

The imported SP+/FPI/TeamRankings preseason rating already includes each
team's expected starting quarterback. Therefore the preseason QB adjustment
is **zero**, and the preseason starter is the **neutral reference**:

- **Baseline value = 0** (and it is **never rewritten** once initialized).
- **Active value = the active QB's point difference relative to that team's
  own preseason baseline QB — nothing else.** It is **not** an absolute
  rating and is **never** comparable across teams.
- **QB delta = Active value − Baseline value.** Since Baseline value stays
  0, **Active value IS the applied deviation** (delta = Active value).
- Baseline QB starting normally → **Active value = 0**, delta 0, status OK.
- Baseline QB returns fully healthy → **Active value resets to 0**.
- A replacement QB may get a positive or negative Active value (deviation).
- An unresolved QB situation stays **blank** and **QB UNCERTAIN**.
- **Do not compare absolute QB values across teams. Do not rewrite a
  previously initialized Baseline value. Do not introduce an absolute
  cross-team tier scale into D or F.**

### Worked example (one team)
| Event | Baseline (D) | Active (F) | Delta (G) |
|---|---|---|---|
| Preseason baseline QB A; QB A starts | 0 | 0 | 0 |
| QB A injured; QB B meaningful downgrade | 0 | −1.5 | −1.5 |
| QB A returns fully healthy, starts | 0 | 0 | 0 |

### Applied result (v0.7.1)
105 teams initialized at Baseline 0 / Active 0 (delta 0, status OK); 33 held
blank and QB UNCERTAIN. No nonzero value entered. See the Phase 8.1
baseline-identity audit for snapshot dates (SP+ 2026-03-27; FPI/TR
2026-07-19) and the 105/33 disposition.

## 4. Future nonzero deviations

Governed by the separate, **proposed (not approved)**
`future_qb_deviation_rubric.md`: quarter-point bands (−4.0 max negative,
+2.0 max positive), a required baseline-vs-active evidence comparison,
sourcing thresholds, and a no-arbitrary-decay double-counting/review rule.
Positive deviations should be uncommon (the priors and TEAM RATINGS already
capture the projected starter and performance). **Nothing nonzero is
applied until that rubric is approved.**

## 5. Sign convention (confirmed)
`delta = Active value − Baseline value`; with Baseline value fixed at 0, the
Active value is the deviation and the delta equals it. Verified against
`QB VALUES!G` and `ENGINE!M`.
