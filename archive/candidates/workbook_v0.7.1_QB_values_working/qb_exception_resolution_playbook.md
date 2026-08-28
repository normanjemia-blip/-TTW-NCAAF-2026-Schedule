# QB Exception-Resolution Playbook (33 UNCERTAIN teams)

Companion to `qb_exception_resolution_tracker.csv` / `.json`. Explains how
to clear each exception and decide, at resolution, between **zero-init** and
a **proposed nonzero deviation** (which still requires rubric approval).
**No resolution is forced.** An official starter announcement is preferred,
but a strong multi-source consensus may justify **Medium** confidence when
no formal announcement is expected.

## Groups (33 total)

- **Open competition — 27:** ALA, ARST, BALL, BUFF, CCU, CMU, CSU, FLA,
  FRES, GASO, IOWA, KAN, LIB, MEM, MOST, M-OH, NEV, NIU, NMSU, OHIO, ORST,
  RUTG, SJSU, TULN, USF, USM, VAN.
- **Injury / availability — 4:** NC (North Carolina), STAN, SYR, TTU.
- **Conflicting / insufficient sourcing — 2:** NEB, TENN.

## Resolution workflow (per team)

1. **Check best sources** (in priority order): official team depth
   chart / athletics release → HC or OC press conference → established
   local beat writer → 247Sports / On3 camp reporting.
2. **Apply the clear-condition** in the tracker's `condition_to_clear`.
3. **Record** `final_resolution`, `resolution_source`,
   `confidence_after_resolution` (H/M/L), with date.
4. **Decide the value path:**
   - If the resolved starter **is** the presumed baseline and there is no
     unresolved issue → **zero-init** (Baseline 0 / Active 0), status OK.
   - If the resolved starter is a **meaningful up/downgrade** vs the
     presumed baseline → **propose a nonzero Active value** per
     `future_qb_deviation_rubric.md` (still needs approval before entry).
   - If still unresolved → **leave blank / QB UNCERTAIN**; set the next
     checkpoint.
5. **Never** enter a value in this documentation phase; the tracker records
   the plan only.

## Confidence-after-resolution guidance

- **H:** official depth-chart/coach naming of QB1, or an unambiguous
  returning starter cleared to play.
- **M:** strong multi-source consensus with no formal announcement expected,
  or a named starter with modest residual uncertainty (e.g., a young but
  uncontested projected starter).
- **L:** remains genuinely unresolved (open battle, ongoing injury/eligibility
  doubt, or materially conflicting sources).

## Category-specific guidance

### Open competitions (27)
Clear on an official depth chart or a clear 2+ source consensus. Most will
resolve during fall camp (early–mid August 2026). If the winner is the
presumed incumbent/baseline → zero-init. If the winner is clearly better or
worse than the presumed baseline → propose a nonzero deviation.

### Injury / availability (4) — specific treatment
- **North Carolina (Edwards Jr.):** **Do NOT initialize** until Edwards is
  healthy enough to participate normally **and** is the established projected
  starter (currently only "inside track," PCL still recovering). Require
  updated injury-recovery evidence + a settled depth chart.
- **Texas Tech (Hammond):** require ACL medical-clearance evidence
  (~Aug 21, 2026) and a named starter; note the gambling-investigation
  eligibility reference. Re-confirm weekly once resolved.
- **Stanford (Warren)** and **Syracuse (Angeli):** require updated injury-
  recovery evidence **and** competition resolution (Rizk/Mitchell Jr. at
  Stanford; Odom at Syracuse) before any disposition.

### Conflicting / insufficient sourcing (2) — specific treatment
- **Nebraska (Colandrea vs Lateef; Kaelin option)** and **Tennessee
  (Brandon vs MacIntyre; Staub option):** **resolve the source conflict**
  via an official/coach statement or 2+ agreeing credible sources —
  **do not simply choose whichever article is newest.** Only after a
  consensus/announcement decide zero-init vs a proposed deviation.

## Classification correction flagged (internal-consistency review)

- **Vanderbilt (VAN):** currently L / "open competition," but **Jared Curtis
  is the consistently projected Day-1 starter** (Blaze Berlowitz is a
  backup, not a genuine competitor). The Low confidence is driven **solely
  by true-freshman youth**, which — per the Phase 8.2 instruction — should
  **not** automatically force Low. **Recommendation: reclassify to Medium
  and treat as eligible for zero-init.** This is documented only; **no
  workbook change is made in this phase** (v0.7.1 is not edited). Applying
  it would be a future one-cell confidence edit (H8-column) plus D/F
  zero-init, on approval.

No other exception shows a comparable inconsistency: Tennessee's freshman
(Brandon) sits inside a genuine, source-disputed competition; every other L
team has a real unresolved battle, injury, or sourcing conflict.
