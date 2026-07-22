# Phase 8.4 — Fall-Camp QB Monitoring & Batch Resolution Plan

**Objective:** resolve the remaining **33 QB exceptions** efficiently as
credible fall-camp information appears — **without** re-running the 138-team
research. Targeted exception sweeps only.

**Status today (2026-07-22):** 105 OK / 33 UNCERTAIN / 0 nonzero deviations.
v0.7.2 is the approved working checkpoint — **not authoritative, not
promoted.** **No research performed today** (per the immediate instruction).

## Source of truth
- `../workbook_v0.7.2_QB_values_candidate/TTW_NCAAF_Power_Ratings_2026_v0.7.2_QB_VALUES_CANDIDATE.xlsx`
- `../workbook_v0.7.2_QB_values_candidate/qb_exception_resolution_tracker.csv` / `.json`
- `../workbook_v0.7.2_QB_values_candidate/qb_exception_resolution_playbook.md`
- `../workbook_v0.7.2_QB_values_candidate/future_qb_deviation_rubric.md`
- `../workbook_v0.7.2_QB_values_candidate/qb_deviation_review_log.csv` / `.json`
- This folder: `pending_qb_resolutions.csv` / `.json` (cross-sweep ledger).

## Sweep cadence (do NOT run continuous broad research)

| Sweep | Window | Scope |
|---|---|---|
| 1 | **Aug 3–5, 2026** | 32 teams due 2026-08-03 (all exceptions except TTU). |
| 2 | **Aug 10–12, 2026** | Only rows still UNRESOLVED from sweep 1, plus any meaningful new update. |
| 3 | **Aug 17–19, 2026** | Still-UNRESOLVED rows; pre-check **TTU** (ACL clearance checkpoint ~Aug 21). |
| 4 (final) | **Aug 24–26, 2026** | All remaining; confirm **TTU**; build **v0.8.0_PRESEASON_READY_CANDIDATE**. |

On each sweep, research **only** tracker rows whose `next_research_date` is due
**or** that received a meaningful new update. Do not re-research resolved teams
or the other 105 teams unless credible news reports a **starter change,
injury, suspension, eligibility issue, or departure.**

## Due-date schedule (from tracker `next_research_date`)

- **Due 2026-08-03 → Sweep 1 (Aug 3–5): 32 teams**
  - *Open competition (27):* ALA, ARST, BALL, BUFF, CCU, CMU, CSU, FLA, FRES,
    GASO, IOWA, KAN, LIB, M-OH, MEM, MOST, NEV, NIU, NMSU, OHIO, ORST, RUTG,
    SJSU, TULN, USF, USM, VAN
  - *Injury/availability (3):* STAN, SYR, UNC
  - *Conflicting/insufficient sourcing (2):* NEB, TENN
- **Due 2026-08-21 → Sweeps 3–4 (Aug 17–19 pre-check, Aug 24–26 confirm): 1 team**
  - *Injury/availability (1):* **TTU** (Hammond ACL medical-clearance checkpoint).

Use `scripts/due_this_sweep.py YYYY-MM-DD` to list rows due on/before a sweep date.

## Source-efficiency order (stop when the threshold is met)
1. Official school announcements, camp reports, press conferences, depth charts
2. Head coach / offensive coordinator statements
3. Established local beat reporters
4. ESPN / major national / 247Sports / On3 / comparable credible reporting

Record only (no narrative): current candidates · current leader · resolution
status · confidence · availability · source · source date · baseline identity ·
whether zero-init is justified · whether a nonzero adjustment may be necessary.
→ logged in `pending_qb_resolutions.csv/.json`.

## Resolution standards
- **H** — starter officially named; **or** an established returning starter
  with no credible active competition or availability concern.
- **M** — multiple credible sources strongly agree on the projected starter,
  no official announcement expected, no genuine equal competition / unresolved
  availability concern.
- **L (keep UNCERTAIN)** — genuine competition; unresolved injury/availability;
  materially conflicting sources; baseline QB cannot be established; or a likely
  starter based mainly on speculation.

Do **not** force every team to resolve before Week 1.

## Workbook-update & versioning rules
- Do **not** create a new workbook per individual resolution. Maintain interim
  state in the tracker + `pending_qb_resolutions.*`.
- Build a new candidate **only** when **≥5 additional teams cleared** *or* at
  the **final Aug 24–26** sweep. Avoid empty/doc-only workbook versions.
- Versions: first ≥5 batch → **v0.7.3_QB_VALUES_CANDIDATE**; further ≥5 batch →
  increment; final preseason → **v0.8.0_PRESEASON_READY_CANDIDATE**.

### Resolved, Active QB == baseline (zero-init)
Baseline QB = confirmed/projected baseline player · Baseline value **0** ·
Active QB = same player · Active value **0** · Confidence **H/M** · Reviewed
season **2026** · Last update = research date · Source/Notes updated · QB delta
must calc **0** · QB status must calc **OK**.

### Resolved, Active QB != baseline (possible baseline change)
Do **not** auto-enter 0/0 and do **not** invent a deviation. Add to
`qb_deviation_review_log`, research the baseline-vs-active comparison under the
deviation-only methodology, **propose** a specific quarter-point deviation with
evidence, and **leave the row UNCERTAIN until explicit approval.** No nonzero
value is ever written without approval.

### Injury / availability
Reconfirm every due sweep. Do not clear merely because a player is "expected
back" — require credible evidence of **normal participation** or **confirmed
game availability.** If a replacement will start, treat as a possible baseline
mismatch → **propose, not enter**, the deviation.

## Efficient verification (interim batches)
Diff vs the prior candidate · formula count **123,011** · formula coords/text
unchanged · focused QB delta/status harness (`livecalc_v072.py`-style) · no
unrelated cells changed. **Do not** run the memory-heavy full 123,011-formula
engine unless a formula/structural change occurred. Reserve full workbook +
Google Sheets round-trip verification for the **final** preseason candidate.

## Per-sweep checkpoint report (only these)
Teams checked · newly resolved · still unresolved · updated OK/UNCERTAIN counts
· zero-init candidates · proposed nonzero-deviation cases · injury/eligibility
changes · exact tracker files changed · whether the 5-team threshold was reached
· commit hash + branch when committed.

## Early-trigger exception
Between sweeps, act only on **major confirmed** QB news (starter named, injury,
suspension, eligibility, departure) for an exception team — otherwise wait for
the next window.
