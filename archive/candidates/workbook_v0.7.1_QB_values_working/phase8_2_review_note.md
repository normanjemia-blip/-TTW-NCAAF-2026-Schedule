# Phase 8.2 Review Note — Substantive Changes vs the Phase 8.1 Proposal

Documentation-only phase. **No XLSX or Google Sheet was modified**; v0.7.1's
applied zero-init state (105 at 0/0, 33 UNCERTAIN) is unchanged.

## Substantive changes to the proposed methodology

1. **Withdrew the "absolute tier" scale entirely.**
   - The Phase 8.0/8.1 report floated **Option B (absolute per-QB tier
     table)** and a Section B that said to "rate **both** [baseline and
     active] on the same tier scale." Both are **withdrawn**. There is now
     **no absolute, cross-team QB scale** anywhere. Active value is strictly
     the deviation vs a team's **own** preseason baseline QB.

2. **Baseline value is now explicitly permanent = 0 and never rewritten.**
   - The old Section B implied Baseline value could be set to "the tier of
     the QB the rating assumed." Corrected: **Baseline value stays 0
     always**; the delta equals the Active value; the Active value is the
     applied deviation.

3. **Replaced the old deviation bands with the approved quarter-point bands.**
   - Old (withdrawn): 6 coarse rows (e.g., "elite→backup −2.0 to −3.5").
   - New: 8 classifications in quarter-point increments —
     equiv 0→−0.5, minor −0.5→−1.0, clear −1.25→−2.0, major −2.25→−3.0,
     extreme −3.25→−4.0, modest upgrade +0.25→+0.75, clear upgrade
     +1.0→+1.5, exceptional +1.75→+2.0.

4. **Lowered the maximum positive deviation from +3.5 to +2.0.**
   - Negative bound unchanged at −4.0. Anything beyond ±(−4.0/+2.0) now
     requires a separately documented manual adjustment + approval.
   - Added rationale: **positive adjustments should be uncommon** (priors
     already include the projected starter; performance gains are captured
     by TEAM RATINGS).

5. **Removed the arbitrary "reset by midseason" decay.**
   - Old B8 allowed a time-based reset. New rule: **no automatic/arbitrary
     decay.** Reset to 0 only when the baseline QB returns healthy; injury
     deltas re-confirmed **weekly**; review a lasting replacement **after 3
     starts**; reduce **only** with documented evidence of double-counting
     vs TEAM RATINGS; **record every reduction/reset/continuation with date,
     source, reason**; never silently decay.

6. **Expanded the evidence framework to the full 9 factors** (identity/
   availability, career starts, passing efficiency, turnover/sack avoidance,
   rushing, system familiarity, sample quality, injury limits, credible
   sourcing) with explicit sourcing thresholds (1 source uncontested, 2 for
   disputed, no 1-game upgrade, ≥3 games for a performance upgrade).

7. **Built the 33-team exception-resolution system** (new): tracker
   (`.csv`/`.json`) with the full required column set, grouped into open
   competition / injury-availability / conflicting-sourcing, plus a
   `qb_exception_resolution_playbook.md` with per-category and per-team
   guidance and the confidence-after-resolution rule (multi-source consensus
   may justify Medium absent a formal announcement).

## Exception-category corrections

- **Vanderbilt (VAN): category correction recommended.** Currently
  L / "open competition," but Jared Curtis is the **consistently projected
  Day-1 starter** (Berlowitz is a backup, not a real competitor); the Low is
  driven **only** by true-freshman youth. Per the Phase 8.2 instruction,
  youth alone should not force Low → **recommend reclassify to Medium and
  treat as eligible for zero-init.** Documented only; **not applied**
  (v0.7.1 unchanged).
- No other exception category was changed. The 4 injury/availability and 2
  conflicting-sourcing assignments hold.

## Teams whose current classification appears internally inconsistent

- **Vanderbilt (VAN)** — the single flagged case (see above): L "open
  competition" is inconsistent with a consistently-projected uncontested
  starter. Recommended → Medium.
- All other 32 exceptions are internally consistent (genuine open battles,
  active injuries, or materially conflicting sources).

## What did NOT change

- The applied deviation-only zero-init (105 at 0/0, 33 UNCERTAIN).
- The sign convention (delta = Active − Baseline).
- The baseline-identity audit and its snapshot dates (SP+ 2026-03-27;
  FPI/TR 2026-07-19).
- The workbook itself — untouched this phase.
