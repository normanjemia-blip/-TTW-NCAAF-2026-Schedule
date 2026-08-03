# Methodology Addendum — Manual Rating Override Standard (Phase 7B.1)

**Adopted:** 2026-08-03 (owner decision, Phase 7B.1). Applies to every manual
`TEAM RATINGS` Rating OVERRIDE recommendation from this point forward.

## The standard

A manual rating override requires evidence of a **material fact** that was either:

1. **unknown** when the workbook's source ratings were published
   (SP+ 2026-03-27; FPI 2026-07-19; TeamRankings 2026-07-19), or
2. **incorrectly represented** in the source ratings, or
3. **materially changed after publication**, or
4. **demonstrably distorted by one source** in a way supported by independent
   football evidence.

## Explicitly insufficient on their own

- Cross-source disagreement (the weighted blend exists to absorb it).
- Narrative, conference-contender status, or public reputation.
- Portal-class ranking, win total, or title odds, standing alone — these may
  corroborate an override case but never constitute one, and any use must
  explain the relationship between the market/roster signal and points of
  team strength.

## The gate question

Every override recommendation must explicitly answer:

> **What does the current workbook baseline fail to capture?**

If that question cannot be answered with verified evidence, **hold the current
rating.**

## Process notes

- Overrides land only in `TEAM RATINGS` column L (Rating OVERRIDE input) with
  reason (M) and date (N), plus a CHANGELOG row. Formulas, weights, HFA, QB
  values, and structure are never touched by an override decision.
- Deferred cases are tracked in `deferred_trigger_register.csv`; a trigger
  firing produces a **review note**, not an automatic adjustment. In
  particular, a starting-QB announcement creates **no presumption** of a
  rating change — the named starter is reassessed against the preseason
  baseline that the sources already priced.
