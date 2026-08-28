# PROMOTION NOTES — v0.8.0 AUTHORITATIVE

**Date:** 2026-08-04 (America/New_York) · **Promoted from:** v0.7.9 CANDIDATE, byte-for-byte

## What this promotion does

It replaces an authoritative workbook with an **empty QB dataset** (0/138 confidence
codes) with one where all 138 records are populated and all 73 Tier-1 records are
independently verified against team-specific primary sources and stamped with a
verification date and evidence note.

## What this promotion does NOT do

**It cannot move a rating or a projected spread.** This is provable, not asserted:

1. Scanning all 123,011 formulas, the only QB VALUES columns any formula reads are
   **A** (abbrev), **G** (delta) and **M** (status). Column **H** — the confidence
   code — **is read by nothing**. Every H/M/L edit is therefore inert to the engine.
2. Every QB delta in column G is blank or exactly **0**, in both workbooks.
   `ENGINE!M` explicitly coerces a blank lookup to 0, so the QB adjustment computes
   `0 − 0 = 0` for every game row in both v0.6.2 and v0.8.0.
3. `TEAM RATINGS` and `ENGINE` are byte-identical OOXML parts.

The only behavioural difference is the **QB UNCERTAIN gate**, and today it is masked:
`ENGINE!AI` evaluates **PENDING LINE before QB UNCERTAIN**, and **0 market spreads are
loaded**, so every game reads PENDING LINE. Promotion is behaviourally inert until
lines are entered.

## Visible changes on open

- `START HERE!A1` banner now reads v0.8.0.
- `START HERE!C11` = `IF(COUNTIF('QB VALUES'!$M$6:$M$143,"UNCERTAIN")=0,"OK",…)` will
  display **"39 teams QB UNCERTAIN"** instead of **"138 teams QB UNCERTAIN"**.
- CHANGELOG carries the full v0.7.0 → v0.7.9 history (116 new cells).

## Known limitations carried into production

These are disclosed, not discovered late. None blocks promotion; each is worse or
equal in v0.6.2.

1. **61 H-coded records were never independently verified.** They were out of declared
   Tier-1 scope — H means the starter was established at the July build. **Missouri
   proved an H-tier assumption can go stale** (it sat at M while officially named).
   Their numerical values are all 0, so they cannot move a rating; the exposure is that
   a departed or displaced starter could sit unflagged. **Recommended: spot-check these
   61 in the first monitoring sweep.**
2. **The 33 L-coded records are perishable.** Accurate as of 2026-08-04, with camps
   opening 8/1–8/6 and openers 8/29–9/5. Depth charts will settle many within three
   weeks. Every note carries an explicit RECHECK trigger.
3. **Alabama note is directionally contested.** The stamped note records Keelon Russell
   as slightly favored over Austin Mack (CBS, 8/4, 55-45 to 60-40). Separate 8/4
   reporting has HC Kalen DeBoer suggesting **Mack** may hold a slight edge on system
   familiarity. **Both sources agree the competition is open and undecided, so the `L`
   code is correct either way** and nothing downstream is affected — but the note's
   directional claim should be neutralised in the first sweep. Not corrected here
   because the audit instruction was to change no cell unless promotion is blocked.
4. **Texas Tech remains provisional** — surgeon clearance reported; final team medical
   clearance expected around the nine-month mark (~2026-08-21).
5. **No cached formula results are stored** in either workbook, so a consumer reading
   cached values sees blanks. Excel and Google Sheets recalculate on open. This is a
   **pre-existing property of v0.6.2**, not a regression — verified: 0 of 123,011
   formula cells carry a cached result in *both* files.

## Operating instructions after promotion

1. Load market lines before expecting any game status other than PENDING LINE.
2. `SETTINGS!B11` stays **"N"** until the owner enables betting output.
3. Run the first Phase 8.4 monitoring sweep **immediately after promotion** — the
   pipeline in `phase8_4_qb_monitoring/scripts/` is built for exactly this.
4. Do not begin VSiN integration until the guide is re-uploaded and indexed.

## Sign-off record

| Question | Answer |
|---|---|
| Any technical reason not to promote? | **No** |
| Any football-data reason not to promote? | **No** |
| Approve promotion if frozen today for Week 0? | **Yes** |

Audit: 3 parts, ~60 independent checks, **0 blockers**. Two audit findings were
**bugs in the audit itself**, corrected and documented rather than dismissed —
see `promotion_audit_log3.txt`.
