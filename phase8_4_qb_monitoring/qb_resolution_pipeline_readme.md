# QB Resolution → Candidate Build Pipeline (Phase 8.4A)

A reliable, one-command pipeline that converts **human-approved** QB
resolutions into a **verified** workbook candidate — without touching any
production workbook or Google Sheet, and without re-running the 138-team
research.

**All scripts live in `scripts/`. Nothing writes to production.** The pipeline
reads a source workbook and *writes a new candidate file you name*; the source
is never modified (its SHA-256 is asserted unchanged).

## Components

| Script | Role |
|---|---|
| `pipeline_lib.py` | Shared helpers: workbook geometry, formula detection, pending/review-log loaders, quarter-point & ISO-date validators, faithful G/M status evaluation. |
| `apply_pending_qb_resolutions.py` | Validate + apply APPROVED resolutions to a **copy**; dry-run or apply. Writes only allowed QB inputs + banner + CHANGELOG; never a formula. |
| `verify_qb_candidate.py` | Compare candidate vs source; full structural + content checks; JSON + Markdown reports. |
| `build_qb_candidate.py` | Orchestrator: validate → dry-run → apply → verify → changed-cell audit; refuses a candidate on an empty ledger or failed verification. |
| `test_pipeline.py` | 12-scenario test harness (temp copies only; never commits workbooks). |

## The ledger the pipeline consumes

`../pending_qb_resolutions.csv` / `.json` — the cross-sweep working ledger.
The pipeline acts **only** on rows whose `resolution_status == APPROVED`.

**Apply-input fields** (extra monitoring columns are ignored):
`abbrev, team, resolution_status, confidence, baseline_qb, baseline_value,
active_qb, active_value, source, source_date, last_update, reviewed_season,
notes`.

## Validation (all must hold before anything is written)

- Every `abbrev` matches **exactly one** workbook team (138 present & unique).
- **No team appears more than once** in the pending file.
- `resolution_status == APPROVED`.
- `confidence` is **H or M** (never L).
- `baseline_qb` and `active_qb` are populated.
- `source`, `source_date`, `last_update`, `notes` are populated.
- `reviewed_season == 2026`.
- `source_date` and `last_update` are **ISO YYYY-MM-DD**.
- `baseline_value == 0` (deviation-only).
- **No formula cell will be overwritten** (target inputs C,D,E,F,H,I,J,K,L must
  be non-formula; A,B,G,M are never targeted).

In **apply mode**, any single validation error aborts the whole build — **no
output is written and the source is untouched.**

## Zero-initialization rule

When `baseline_qb == active_qb`:
`baseline_value = 0`, `active_value = 0` → expected **QB delta 0**, expected
**QB status OK** (with H/M + season 2026).

## Baseline-mismatch rule

When `baseline_qb != active_qb`:
- Do **not** auto-initialize 0/0 and do **not** invent a deviation.
- Require a **matching APPROVED** record in `qb_deviation_review_log`
  (same Abbrev + Active QB; `Status = active`; `Review action = entered`;
  `Applied/Revised deviation` equals `active_value`; a `Reviewer` and an ISO
  `Review date`).
- The deviation must be a **quarter-point in [-4.00, +2.00]**.
- A merely **proposed / pending / unapproved** review-log record (e.g.
  `Status = under review`) is **rejected**.
- The `ADJUSTMENTS` sheet must **never** be used as a substitute for a QB
  deviation.

## What the pipeline may change (and nothing else)

- QB VALUES inputs for approved teams: **Baseline QB, Baseline value, Active
  QB, Active value, Confidence, Source, Reviewed for season, Last update,
  Notes** (columns C, D, E, F, H, I, J, K, L).
- The **version banner** (`START HERE!A1`).
- **New CHANGELOG rows** (appended).

It **never** writes the calculated **QB delta (G)** or **QB status (M)**, and
never any other sheet (MARKET LINES, ADJUSTMENTS, TEAM RATINGS, HFA, SETTINGS,
IMPORT SCHEDULE, IMPORT STATS, etc.).

## Verification (candidate vs source — all must pass)

21 sheets · identical order · identical hidden/visible states · exactly
**123,011 formulas** · identical formula coordinates + text (no formula
overwritten/added/removed) · no unrelated cells changed · only approved QB
rows + banner + CHANGELOG changed · 138 teams present & unique · Baseline/Active
values are only blank/0/**approved** deviation · every nonzero value has a
matching approved review-log record · focused QB status counts match the
expected OK/UNCERTAIN · no MARKET LINES/ADJUSTMENTS/TEAM RATINGS/HFA/SETTINGS/
IMPORT/SCHEDULE change. A machine-readable **JSON** and a readable **Markdown**
report are produced. (The memory-heavy full 123,011-formula engine is **not**
run.)

## Command examples

Set paths (from `phase8_4_qb_monitoring/`):

```bash
SRC=../workbook_v0.7.2_QB_values_candidate/TTW_NCAAF_Power_Ratings_2026_v0.7.2_QB_VALUES_CANDIDATE.xlsx
PEND=pending_qb_resolutions.csv          # or .json
RLOG=../workbook_v0.7.2_QB_values_candidate/qb_deviation_review_log.csv
OUT=/tmp/TTW_NCAAF_Power_Ratings_2026_v0.7.3_QB_VALUES_CANDIDATE.xlsx
```

**1) Dry-run** (validate + show intended changes; writes nothing):

```bash
python3 scripts/apply_pending_qb_resolutions.py \
  --source "$SRC" --pending "$PEND" --review-log "$RLOG" \
  --output "$OUT" --version-label v0.7.3
```

**2) One-command candidate build** (validate → dry-run → apply → verify → audit;
refuses on empty ledger or failed verification):

```bash
python3 scripts/build_qb_candidate.py \
  --source "$SRC" --pending "$PEND" --review-log "$RLOG" \
  --output "$OUT" --version-label v0.7.3 --report-dir /tmp/qb_reports
```

**3) Verify only** (e.g., an already-built candidate):

```bash
python3 scripts/verify_qb_candidate.py \
  --source "$SRC" --candidate "$OUT" --pending "$PEND" --review-log "$RLOG" \
  --report-json /tmp/verify.json --report-md /tmp/verify.md
```

**Try it with the fictional examples** (produces 107 OK / 31 UNCERTAIN / 1
nonzero — a demo only; the QB names are made up):

```bash
python3 scripts/build_qb_candidate.py --source "$SRC" \
  --pending examples/pending_qb_resolutions.example.json \
  --review-log examples/qb_deviation_review_log.example.csv \
  --output /tmp/v0.7.3_EXAMPLE.xlsx --version-label v0.7.3-EXAMPLE \
  --report-dir /tmp/qb_reports
```

## How the August sweeps feed the ledger

1. During each monitoring window (Aug 3–5, 10–12, 17–19, 24–26), research
   **only** the tracker rows that are **due** (`scripts/due_this_sweep.py`) or
   have a meaningful new update.
2. Record the compact findings as a row in `pending_qb_resolutions.csv/.json`.
   - Set `resolution_status = UNRESOLVED` while still uncertain.
   - **Zero-init case** (resolved starter == baseline): fill `baseline_qb` =
     `active_qb`, `baseline_value = 0`, `active_value = 0`, `confidence = H/M`,
     source/date/notes, `reviewed_season = 2026`; set
     `resolution_status = APPROVED` once you (the human) approve.
   - **Baseline-mismatch case**: add a record to `qb_deviation_review_log`,
     **propose** a quarter-point deviation (`Status = under review`), and keep
     the pending row `PROPOSED-DEVIATION` / not APPROVED until you approve. On
     approval, set the review-log record `Status = active`,
     `Review action = entered`, and the pending row `resolution_status =
     APPROVED` with `active_value` = the approved deviation.
3. **Build a new candidate only** when **≥5 teams have cleared** *or* at the
   **final Aug 24–26** sweep. Versions: `v0.7.3_QB_VALUES_CANDIDATE`,
   incrementing; final `v0.8.0_PRESEASON_READY_CANDIDATE`.

The pipeline ignores non-APPROVED rows, so the ledger can hold in-progress
observations safely between sweeps.

## Recovery when verification fails

`build_qb_candidate.py` **deletes** the candidate automatically if verification
fails (exit code 3), so a bad candidate is never retained. To recover:

1. **Read the report.** `verification_report_<ver>.md` (and `.json`) lists each
   failed check with detail; `changed_cells_<ver>.csv/.json` shows exactly what
   changed.
2. **Diagnose by symptom:**
   - *Formula count ≠ 123,011 / formula overwritten* → a source or input cell
     was a formula, or the source is not the intended checkpoint. Re-check
     `--source`.
   - *Unrelated cell changed / other sheet changed* → the source was not
     pristine, or the wrong source was passed. Rebuild from the approved
     checkpoint.
   - *Nonzero value without approved review-log record* → the review-log record
     is missing/`under review`/mismatched. Fix the review log or set the row
     back to non-APPROVED.
   - *OK/UNCERTAIN count mismatch* → a row that should stay UNCERTAIN was marked
     APPROVED (e.g., confidence should be L, or an unresolved injury). Correct
     the ledger.
3. **Fix the ledger or review log** (never hand-edit the workbook), then re-run
   `build_qb_candidate.py`. The source is guaranteed unchanged, so re-runs are
   safe and idempotent.
4. If a dry-run reports **validation errors**, no file is written at all — fix
   the listed rows and re-run.

## Test harness

```bash
python3 scripts/test_pipeline.py          # 12 scenarios, temp copies, auto-clean
python3 scripts/test_pipeline.py --keep    # keep the temp dir for inspection
```

Scenarios: valid zero-init · valid approved nonzero deviation · missing source
· invalid date · duplicate team · unknown abbreviation · low-confidence row ·
baseline mismatch without approval · out-of-bounds deviation · attempt to
overwrite a formula · unexpected unrelated-cell change · empty pending ledger.
Every invalid scenario must **fail safely** and leave the source workbook
byte-unchanged. Generated test workbooks are temporary and are **never
committed**.
