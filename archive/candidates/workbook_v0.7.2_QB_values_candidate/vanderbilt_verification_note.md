# Vanderbilt QB Re-Verification Note (Phase 8.3)

**Verification date:** 2026-07-22
**Team:** Vanderbilt (VAN), SEC
**Question:** Does current evidence still support the Phase 8.2 recommendation
to reclassify Vanderbilt from **L → M** and zero-initialize it, on the basis
that Jared Curtis is the consistently projected, uncontested Day-1 starter?

## Result: **RE-VERIFICATION FAILED — Vanderbilt stays L / UNCERTAIN.**

Vanderbilt is **not** reclassified and **not** initialized. The Phase 8.2
recommendation is **superseded** by fresher, more authoritative evidence.
Final workbook counts remain **105 OK / 33 UNCERTAIN** (not 106 / 32).

## The four re-verification criteria (all must hold to reclassify)

| # | Criterion | Finding (2026-07-22) | Pass? |
|---|---|---|---|
| 1 | Consistently projected **Day-1 starter** | HC Clark Lea has **not named a starter**; competition may run to the opener vs Austin Peay | **No** |
| 2 | **Uncontested** by a genuine equal competitor | Blaze Berlowitz is a **genuine veteran competitor** — two seasons in OC Tim Beck's system, Diego Pavia's 2025 backup; "knows the system better and has more experience" right now | **No** |
| 3 | **Healthy and available** | No availability concern reported for either QB | Yes |
| 4 | **Reasonably priced** into preseason snapshots | Ambiguous — an unresolved competition (possible two-QB usage) is not a settled priced-in starter | Unclear |

Criteria **1 and 2 fail outright**, which is dispositive. Per the Phase 8.3
instruction — *"Only when current evidence still supports the Phase 8.2
conclusion, reclassify Vanderbilt from L to M and initialize it at zero"* —
the reclassification is **not** applied.

> Note on the guardrail: *"True-freshman status alone must not force Low
> confidence."* Low here is **not** driven by Curtis's freshman status. It is
> driven by an **actual, coach-confirmed open competition** against a credible
> veteran — exactly the kind of unresolved situation the L / UNCERTAIN state
> is meant to capture. If Curtis were the uncontested projected starter and
> only his youth were in question, reclassification to M would have been
> warranted; that is not the current situation.

## Evidence (fresh current sources)

At **Vanderbilt's SEC Media Days session on 2026-07-21**, head coach
**Clark Lea** said he is **not ready to name a starting quarterback**. Reported
specifics:

- The **Jared Curtis vs. Blaze Berlowitz** competition **will continue through
  fall camp** and **may not be decided before** the Commodores open the season
  against Austin Peay.
- **Berlowitz** — who **spent the past two seasons with Vanderbilt** and has
  **experience in OC Tim Beck's system, including time as Diego Pavia's
  backup** — "right now, knows the Commodores' system better and has more
  experience" than Curtis.
- Lea framed it around winning: *"The mission's winning… we have to evaluate
  all possibilities and put the best person on the field that's going to help
  us win."* He indicated Vanderbilt **could use both quarterbacks** in game
  situations, without committing to an even split.
- Curtis (Nashville Christian School) arrived as the **highest-rated recruit
  in program history**, but Lea said he **"has catching up to do in some
  ways."**

This is a **genuine, coach-acknowledged open competition with a credible
veteran**, not a young-but-uncontested projected starter.

### Sources
- **WSMV (Nashville NBC affiliate)** — "Vanderbilt QB competition headlines
  Commodores' SEC Media Days session," **2026-07-21**.
  https://www.wsmv.com/2026/07/21/vanderbilt-qb-competition-headlines-commodores-sec-media-days-session/
- **Yahoo Sports** — "Is Jared Curtis really in QB competition at Vanderbilt?
  Clark Lea says yes" (SEC Media Days coverage, July 2026).
  https://sports.yahoo.com/articles/jared-curtis-really-qb-competition-203929631.html
- **Saturday Down South** — "Clark Lea not ready to commit to starting QB amid
  Jared Curtis, Blaze Berlowitz battle" (July 2026).
  https://www.saturdaydownsouth.com/news/college-football/clark-lea-not-ready-to-commit-to-starting-qb-amid-jared-curtis-blaze-berlowitz-battle/
- **Sports Illustrated (Vanderbilt)** — "Post-Spring Vanderbilt Football Depth
  Chart Preview: Jared Curtis and The Quarterbacks" (2026 offseason context).
  https://www.si.com/college/vanderbilt/football/post-spring-vanderbilt-football-depth-chart-preview-jared-curtis-and-the-quarterbacks

(Exact publication dates are recorded only where verifiable: WSMV = 2026-07-21,
the SEC Media Days session date. The SI depth-chart preview is offseason and
its precise date was not verifiable, so no date is asserted for it.)

## Disposition applied in v0.7.2

- **Confidence:** L (unchanged).
- **QB status:** UNCERTAIN (unchanged).
- **Baseline value (D) / Active value (F):** left **blank** (not initialized).
- **Tracker:** VAN remains in the exception tracker (open-competition group)
  with `eligible_for_zero_init = N`, `last_checked_date = 2026-07-22`,
  `most_recent_source_date = 2026-07-21`, `next_research_date = 2026-08-03`,
  and a note recording that the Phase 8.2 reclassification was rejected on
  re-verification.
- **Next checkpoint:** fall camp (early Aug 2026) / HC availability / game-week
  depth chart. Re-evaluate for M only if Lea names Curtis (or Berlowitz)
  clearly, or a 2+ source consensus emerges. If the winner is the priced-in
  projected starter, the disposition at that point is zero-init (delta 0), not
  a nonzero deviation.
