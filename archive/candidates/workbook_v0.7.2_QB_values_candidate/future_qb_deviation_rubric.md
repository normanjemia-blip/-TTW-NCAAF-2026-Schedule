# Future QB Deviation Rubric (PROPOSED — not approved, not applied)

**Framework is permanently deviation-only. There is no absolute cross-team
QB tier scale in columns D or F.** Every value is *relative to that team's
own preseason baseline quarterback*.

> **Phase 8.3 correction:** the deviation bands below have been replaced with
> **discrete, non-overlapping quarter-point values** (the earlier bands put
> −0.50 in two classifications). The review-log fields referenced in §4 now
> live in a **separate** file — `qb_deviation_review_log.csv` / `.json` — not
> in the exception tracker.

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
  Active value (the deviation) per the discrete values below.
- An **unresolved** QB situation stays **blank** and **QB UNCERTAIN** — no
  value is entered.
- **Never** compare absolute QB values across different teams. **Never**
  rewrite a previously initialized Baseline value.

### Worked example (single team)
| Event | Baseline value (D) | Active value (F) | Delta (G) |
|---|---|---|---|
| Preseason baseline = QB A; QB A starts | 0 | 0 | 0 |
| QB A injured, QB B is a meaningful downgrade | 0 | −1.50 | −1.50 |
| QB A returns fully healthy and starts | 0 | 0 (reset) | 0 |

## 2. Proposed deviation values (discrete quarter-point steps)

These are **proposed allowed values, not permission to enter values.** The
Active value (deviation vs the team's own baseline) must be **exactly one of
the discrete quarter-point values** listed for the classification that
matches the documented comparison. The bands are **mutually exclusive** —
no value appears in two rows.

| Classification | Allowed deviation values (Active value) |
|---|---|
| Functionally equivalent replacement | `0`, `−0.25`, `−0.50` |
| Minor downgrade | `−0.75`, `−1.00` |
| Clear downgrade | `−1.25`, `−1.50`, `−1.75`, `−2.00` |
| Major downgrade | `−2.25`, `−2.50`, `−2.75`, `−3.00` |
| Extreme elite-to-unproven downgrade | `−3.25`, `−3.50`, `−3.75`, `−4.00` |
| Modest upgrade | `+0.25`, `+0.50`, `+0.75` |
| Clear upgrade | `+1.00`, `+1.25`, `+1.50` |
| Exceptional upgrade | `+1.75`, `+2.00` |

**Rules for the values:**

- **Quarter-point increments only.** No value may fall between two
  quarter-points (e.g., −0.60 or +1.10 are invalid).
- **Maximum permitted QB deviation is −4.00 to +2.00**, inclusive. `0` is a
  valid value (functionally equivalent replacement).
- **No overlap.** Each quarter-point value belongs to exactly one
  classification. `−0.50` is *functionally equivalent* only; `−0.75` is the
  first *minor downgrade* step.
- **Anything outside the approved bounds** (below −4.00, above +2.00, or a
  non-quarter-point value) **requires a formal methodology amendment and
  explicit approval before being entered anywhere.**
- **No backdoor adjustments.** The `ADJUSTMENTS` sheet must **not** be used
  to add QB-driven point value beyond these bounds. QB quality is expressed
  **only** through `QB VALUES!F` within −4.00…+2.00; any additional QB-based
  point movement routed through `ADJUSTMENTS` (or any other sheet) is a
  prohibited backdoor and requires a documented, separately approved
  methodology amendment.
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
adjustment** — a functionally equivalent replacement is `0`, `−0.25`, or
`−0.50`.

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
6. **Record every adjustment, reduction, reset, or continuation** — with
   **date, source, and reason** — in the **separate review log**
   (`qb_deviation_review_log.csv` / `.json`). The exception tracker does
   **not** contain review-log columns; the review log is its own file.
7. **Never silently decay** an adjustment.

## 5. What this rubric does NOT do

- It does not assign absolute QB ratings.
- It does not compare QBs across teams.
- It does not touch Baseline value (always 0).
- It does not authorize any value entry — this document is proposed for
  approval only. Until approved, the workbook stays at the zero-init state
  (105 teams at 0/0, 33 UNCERTAIN).
