# Future QB Deviation Rubric (PROPOSED — not approved, not applied)

**Framework is permanently deviation-only. There is no absolute cross-team
QB tier scale in columns D or F.** Every value is *relative to that team's
own preseason baseline quarterback*.

## 1. Definitions (binding)

- `QB VALUES!D` **Baseline value = 0, always.** It is never rewritten once
  a team is initialized. It anchors the team's own preseason starter as the
  zero reference.
- `QB VALUES!F` **Active value = the active quarterback's point difference
  relative to that team's preseason baseline quarterback** — nothing else.
  It is **not** an absolute rating and is **never** comparable across teams.
- `QB VALUES!G` **QB delta = Active value − Baseline value.** Since Baseline
  value stays 0, **Active value *is* the applied deviation** (delta = Active).
- **Baseline QB starting normally → Active value = 0** (delta 0).
- **Baseline QB returns (fully healthy, starting) → Active value resets to 0.**
- A **replacement** quarterback may receive a **positive or negative**
  Active value (the deviation) per the bands below.
- An **unresolved** QB situation stays **blank** and **QB UNCERTAIN** — no
  value is entered.
- **Never** compare absolute QB values across different teams. **Never**
  rewrite a previously initialized Baseline value.

### Worked example (single team)
| Event | Baseline value (D) | Active value (F) | Delta (G) |
|---|---|---|---|
| Preseason baseline = QB A; QB A starts | 0 | 0 | 0 |
| QB A injured, QB B is a meaningful downgrade | 0 | −1.5 | −1.5 |
| QB A returns fully healthy and starts | 0 | 0 (reset) | 0 |

## 2. Proposed deviation bands (quarter-point increments)

These are **proposed boundaries, not permission to enter values.** The
Active value (deviation vs the team's own baseline) should fall in the band
matching the documented comparison.

| Classification | Proposed deviation (Active value) |
|---|---|
| Functionally equivalent replacement | 0 to −0.5 |
| Minor downgrade | −0.5 to −1.0 |
| Clear downgrade | −1.25 to −2.0 |
| Major downgrade | −2.25 to −3.0 |
| Extreme elite-to-unproven downgrade | −3.25 to −4.0 |
| Modest upgrade over baseline | +0.25 to +0.75 |
| Clear upgrade over baseline | +1.0 to +1.5 |
| Exceptional upgrade | +1.75 to +2.0 |

- **Maximum negative deviation: −4.0. Maximum positive deviation: +2.0.**
  Anything beyond these limits requires a **separately documented manual
  adjustment and explicit approval** — it is not covered by this rubric.
- **Positive adjustments should be uncommon.** The preseason rating already
  includes the projected starter, and performance-based improvement is
  captured by TEAM RATINGS, so an *upgrade vs the team's own baseline*
  should be rare and well-justified (e.g., a clearly better player displaces
  the assumed starter, or the assumed starter was a placeholder for an
  unresolved competition that resolves to a stronger QB).

## 3. Required evidence framework (per nonzero adjustment)

Every nonzero Active value must be backed by a **written comparison of the
baseline QB vs the active QB** covering:

1. Confirmed starter identity and availability
2. Career starts and meaningful game experience
3. Recent passing efficiency (completion %, yards/attempt, QBR/PFF if available)
4. Turnover and sack avoidance
5. Rushing contribution
6. Offensive-system familiarity
7. Quality and relevance of the statistical sample
8. Injury limitations
9. Credible coach / official-team / established beat-reporter evidence

**A change in starter identity alone does not automatically justify a large
adjustment** — a functionally equivalent replacement is 0 to −0.5.

### Sourcing thresholds
- **Uncontested change:** ≥ 1 official or highly credible source.
- **Disputed situation:** ≥ 2 independent credible sources.
- **No performance-driven upgrade based on one game.**
- **≥ 3 meaningful games** before considering any performance-based upgrade
  over the preseason baseline.

## 4. Double-counting & review rule (no arbitrary decay)

There is **no automatic/arbitrary decay** (e.g., no "reset by midseason").
Instead:

1. **Reset immediately to 0** when the preseason baseline QB returns fully
   healthy and starts.
2. **Injury adjustments are re-confirmed every affected week** (week-scoped).
3. **Review a lasting replacement after 3 starts.**
4. At that review, **determine whether TEAM RATINGS has begun absorbing the
   replacement's performance** (the ±2.5 weekly movement cap moves the team
   on results).
5. **Reduce the QB deviation only when documented evidence shows** that
   retaining the full adjustment would **duplicate movement already
   reflected in TEAM RATINGS**.
6. **Record every reduction, reset, or continuation** with **date, source,
   and reason** (see the review-log columns in the tracker).
7. **Never silently decay** an adjustment.

## 5. What this rubric does NOT do

- It does not assign absolute QB ratings.
- It does not compare QBs across teams.
- It does not touch Baseline value (always 0).
- It does not authorize any value entry — this document is proposed for
  approval only. Until approved, the workbook stays at the zero-init state
  (105 teams at 0/0, 33 UNCERTAIN).
