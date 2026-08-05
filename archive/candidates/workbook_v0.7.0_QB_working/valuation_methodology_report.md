# Phase 8 — QB Valuation Methodology Report & Proposed Rubric (FOR APPROVAL)

## 1. Finding: no approved numerical QB-value rubric exists

Per the Phase 8 valuation rules, I inspected DICTIONARY, CHANGELOG,
SETTINGS, PRESEASON, the formulas, and every prior workbook version /
deliverable. Result, consistent with the v0.4 and v0.5.1 findings already
recorded in the workbook's own CHANGELOG:

- **DICTIONARY / SETTINGS / architecture docs contain no QB-value scale.**
  The v0.4 CHANGELOG states verbatim: *"no explicit QB-value quantification
  source is named in the approved architecture docs."*
- The v0.5.1 QB research file states: *"baseline value and adjustment value
  (a numeric points quantification of QB quality) have no approved,
  verified source or methodology anywhere in the project's architecture
  docs."*

Therefore, per the instruction ("If the repository does not contain a
complete numerical valuation rubric, still complete all research and
starter identification, then produce a clearly defined proposed rubric for
approval before writing numerical values"), **no numbers were written.**
`QB VALUES!D` (Baseline value) and `QB VALUES!F` (Active value) are blank
for all 138 teams; `G` (QB delta) stays blank; all 138 remain QB UNCERTAIN.

## 2. What the workbook's existing QB formulas require

- `QB VALUES!G` (delta) `=IF(OR($D6="",$F6=""),"",$F6-$D6)` →
  **delta = Active value − Baseline value** (sign convention: a positive
  delta means the active QB is rated **better** than the baseline QB).
- `QB VALUES!M` (status) `=IF($A6="","",IF(OR($G6="",$H6="L",$J6<>SETTINGS!$B$3),"UNCERTAIN","OK"))`
  → a team is "OK" only when the delta exists (both values entered),
  confidence is not L, and Reviewed-for-season equals SETTINGS!B3 (2026).
- Downstream, `ENGINE!M` (QB adj) consumes the delta as **points added to
  the team's projected margin**. So the value scale is **points of game
  margin**.

This is a **baseline–delta** system: *only the delta moves the projection*
(DICTIONARY confirms "only deltas move projections").

## 3. Key design consideration the rubric must resolve

The 2026 preseason team ratings already loaded (SP+ + FPI + TeamRankings
blend, Phase 4) are **forward-looking 2026 projections built on each
team's projected 2026 roster and starter**. They already price in the
expected QB. If we now add an *absolute* QB value on top, we **double-count
the QB** that the priors already reflect.

This is why "Baseline QB" matters: the baseline is **the QB the preseason
prior was built around** (the projected starter). For 138/138 teams at
preseason, Baseline QB = Active QB (the projected 2026 starter) — which is
exactly how column C was populated (for H/M teams; left blank for the 32
open competitions where that identity isn't yet established).

## 4. Proposed rubric — two options, one recommended

### ★ Recommended — Option A: "Deviation-only" (preseason delta = 0)

Set **Baseline value = Active value** for every team at preseason, so
**delta = 0** and no preseason QB adjustment is applied on top of the
priors (no double-count). The QB VALUES system then does its intended job
**in-season**: when the *active* starter deviates from the *baseline*
(injury, benching, suspension, transfer), you change only the Active value
to the replacement's tier, and delta = Active − Baseline moves the number.

- Concrete implementation: pick a single constant anchor (e.g. `0.0`) for
  both D and F on every H/M team at preseason. Delta = 0. Status → OK for
  H/M teams (values present, not L, season 2026); the 32 L teams stay
  UNCERTAIN until their competition resolves.
- Pros: zero double-counting with the priors; fully objective (no
  subjective per-QB points); matches "only deltas move projections";
  immediately makes the model usable while staying honest about what the
  priors already contain.
- Cons: assigns no preseason QB differentiation beyond what the priors
  already have (by design).

### Option B: "Absolute tier" (per-QB points, documented basis)

Assign each QB an absolute points value from a reproducible tier table,
with Baseline = the prior's implied starter and Active = the confirmed
starter; delta captures any upgrade/downgrade. Suggested tier table
(points of margin; anchor = average returning FBS starter ≈ 0), assigned
from **documented, reproducible inputs only** (prior-season ESPN QBR / PFF
grade / yards-per-attempt + TD:INT, career starts, role):

| Tier | Description | Points |
|---|---|---|
| Elite proven | Returning All-America-level (top ~10 nationally) | +2.5 |
| Strong proven | Multi-year productive returning starter | +1.5 |
| Solid | Established average-plus starter | +0.5 |
| Replacement/average | First-time starter or lateral transfer | 0.0 |
| Unproven | Limited-sample promotion / mid-tier transfer | −0.5 |
| Freshman/high-risk | True freshman or clear downgrade | −1.5 |

- Pros: granular preseason QB differentiation.
- Cons: **double-counts** the priors unless the priors are first stripped
  of their QB assumption (not currently possible from the loaded blend);
  tier placement is partly judgmental. **Not recommended** without a
  companion decision to neutralize the priors' embedded QB.

## 5. Sign-convention confirmation

`delta = Active value − Baseline value`. Positive delta = active QB rated
better than baseline (adds points to the team's margin); negative = worse.
Confirmed against `QB VALUES!G` and the downstream `ENGINE!M` consumer.

## 6. What I need from you

**Approve a rubric (A recommended, or B, or a variant), and I will then, in
a separate step, write only the Baseline value (D) and Active value (F)
numbers** — using the approved scale consistently for all 138 teams, keep
the 32 L-competition teams UNCERTAIN, and re-run the full verification. No
numbers are written until you approve.
