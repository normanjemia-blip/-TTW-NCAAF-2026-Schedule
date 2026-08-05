# PROMOTION CERTIFICATE

## TTW College Football Power Ratings
## v0.8.0 AUTHORITATIVE

**Phase 7E — Authoritative Promotion.** This certificate formally closes the
TTW Workbook Build Project.

---

## 1. Version

| Field | Value |
|---|---|
| **Official designation** | **TTW College Football Power Ratings — v0.8.0 AUTHORITATIVE** |
| File | `promotion_v0.8.0/TTW_College_Football_Power_Ratings_v0.8.0_AUTHORITATIVE.xlsx` |
| Promoted from | `v0.7.9_CANDIDATE` — **byte-for-byte** |
| Supersedes | `v0.6.2 AUTHORITATIVE` |
| Rollback target | `v0.6.2 AUTHORITATIVE` (unmodified, retained) |

## 2. SHA-256

```
661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7
```

Size 3,010,398 bytes. **Identical to the SHA-256 of `v0.7.9_CANDIDATE`** — verified
by `cmp` and by hash after every promotion file operation.

| Workbook | SHA-256 |
|---|---|
| **v0.8.0 AUTHORITATIVE** | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` |
| v0.7.9 CANDIDATE (archived) | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` |
| v0.6.2 AUTHORITATIVE (rollback) | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` |

## 3. Build date

| Event | Date (America/New_York) |
|---|---|
| Candidate built (v0.7.9) | 2026-08-04 |
| Promotion audit | 2026-08-04 |
| **Promotion (Phase 7E)** | **2026-08-04** |
| QB dataset as-of date | 2026-08-04 |
| Preseason source blend | SP+ 2026-03-27 · FPI 2026-07-19 · TeamRankings 2026-07-19 · TTW 2025 · VSiN |

## 4. Formula count

**123,011** — re-counted from the promoted file, identical to v0.6.2 and to every
candidate in the line.

| Sheet | Formulas | Sheet | Formulas |
|---|---:|---|---:|
| ENGINE | 36,000 | TEAM RATINGS | 2,208 |
| CLEAN | 33,000 | PRESEASON | 1,932 |
| DASHBOARD | 26,000 | QB VALUES | 552 |
| CALC | 17,104 | ADJUSTMENTS | 500 |
| MARKET LINES | 5,000 | IMPORT STATS | 200 |
| TEAM MAP | 476 | DATA QUALITY | 16 |
| AUDIT | 15 | START HERE | 8 |
| SETTINGS · IMPORT SCHEDULE · FCS TIERS · HISTORY · BACKTEST · DICTIONARY · CHANGELOG | 0 | | |
| | | **TOTAL** | **123,011** |

## 5. Worksheet count

**21** — order and visibility identical to v0.6.2.

## 6. Regression summary

| Suite | Result |
|---|---|
| Phase 7D.5 regression battery | **38 / 38 PASS** |
| Promotion audit (3 parts, ~60 independent checks) | **0 BLOCKERS** |
| Formula changes vs v0.6.2 | **0** |
| Cell changes vs v0.6.2 | 1,249 — QB VALUES 1,132 · CHANGELOG 116 · START HERE 1 |
| Worksheet XML parts byte-identical to v0.6.2 | **18 of 21** |
| Unrelated / unauthorized / unknown changes | **0** |

Proven, not asserted: scanning all 123,011 formulas, the only QB VALUES columns any
formula reads are **A, G, M**. **Column H (the confidence code) is read by nothing**,
so H/M/L edits are inert to the engine. Every QB delta is blank or 0 and `ENGINE!M`
coerces blank→0, so the QB adjustment computes **0 − 0 = 0 for every game** in both
workbooks. `TEAM RATINGS` and `ENGINE` are byte-identical parts. Defined names,
conditional formatting and data validation identical.

Two audit checks failed and were traced to **bugs in the audit, not the workbook**
(a formula-vs-literal comparison, and a set of cached-value comparisons that were
vacuous because neither workbook stores cached results). Both were corrected and the
claims re-proved from literals and formula text. Documented in `promotion_audit_log3.txt`.

## 7. Verified QB records

| Metric | v0.6.2 | **v0.8.0** |
|---|---|---|
| Confidence codes populated | **0 / 138** | **138 / 138** |
| Tier-1 (M+L) records independently verified and stamped | 0 / 73 | **73 / 73** |
| QB verification backlog | n/a | **0** |
| Audit-trail gap (Tier-1 records lacking a stamp) | n/a | **0** |
| QB status | 138 UNCERTAIN | **99 OK / 39 UNCERTAIN** |

Verification used team-specific primary sourcing — official athletics sites, head-coach
statements, and local beat reporting. **11 defects were found across 80 team-specific
verification passes (~1 in 7):** Akron, Arkansas, UConn, Buffalo, Northern Illinois,
Appalachian State, Washington State, Georgia Southern, North Carolina, UNLV (all
over-confident), and Missouri (the single under-confident case).

## 8. H / M / L classifications

| Code | Meaning | Count |
|---|---|---:|
| **H** | Confirmed starter | **65** |
| **M** | Clear leader, not officially named | **40** |
| **L** | Genuine competition or unverifiable | **33** |
| | **Total** | **138** |

Numerical inputs: **39 blank / 99 zero**. **0 nonzero QB values** and **0 nonzero QB
deltas** anywhere in the dataset. Every L-coded team has blank inputs and resolves to
UNCERTAIN — **0 violations**.

## 9. Unresolved L classifications

**33** — each is a genuine, documented, still-open quarterback competition, not a gap
in research. Every one carries an evidence note and an explicit RECHECK trigger.

Alabama · Florida · Tennessee · Vanderbilt · Nebraska · Stanford · Syracuse · Kansas ·
Iowa · Rutgers · Memphis · USF · Tulane · Ball State · Central Michigan · Miami (OH) ·
Buffalo · Ohio · Missouri State · New Mexico State · Nevada · San José State ·
Colorado State · Fresno State · **Washington State** · Arkansas State · Coastal
Carolina · Appalachian State · Southern Miss · Akron · **North Carolina** · **UNLV** ·
Liberty

Bolded entries were reclassified **into** L during verification because the prior
record overstated certainty.

These records are **perishable** — depth charts land before the 2026-08-29 openers and
will settle many of them. This is expected behaviour, not a defect.

## 10. Files archived

Nothing deleted. All history preserved in git.

**`archive/candidates/`** — the QB verification candidate line, superseded by v0.8.0:
`workbook_v0.7.0_QB_working`, `v0.7.1_QB_values_working`, `v0.7.2_QB_values_candidate`,
`v0.7.3`, `v0.7.4`, `v0.7.5`, `v0.7.6`, `v0.7.7`, `v0.7.8`, `v0.7.9` — each retaining
its own manifest, phase report, build script and verification log.

**`archive/pre_qb_project/`** — the pre-QB lineage: `workbook_v0.3.1`, `v0.4`, `v0.4.1`,
`v0.4.2`, `v0.5`, `v0.5.1`, `v0.5.2`, `v0.6`, `v0.6.1` deliverables.

**NOT archived, deliberately:** `workbook_v0.6.2_deliverables/` remains in place at the
repository root because it is the **rollback target**. Do not move, modify or delete it.

## 11. Rollback procedure

Full detail in `promotion_v0.8.0/ROLLBACK.md`. Rollback is **lossless** — v0.6.2 is
unmodified and hash-verified.

```bash
cd /home/user/-TTW-NCAAF-2026-Schedule
# 1. Confirm the rollback target is intact FIRST
sha256sum workbook_v0.6.2_deliverables/TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx
#   must print bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd
# 2. Restore
cp workbook_v0.6.2_deliverables/TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx \
   ./TTW_CFB_Power_Ratings_AUTHORITATIVE.xlsx
# 3. Revert the manifest pointer
git checkout PROJECT_MANIFEST.json
```

**Roll back if:** the workbook fails to open; recalculation yields `#REF!`/`#N/A` in
ENGINE/CLEAN/CALC/TEAM RATINGS; formula count ≠ 123,011; sheet count ≠ 21;
`SETTINGS!B3`≠2026, `B6`≠2.5 or `B11`≠"N"; or any rating/spread differs from its
pre-promotion value (which should be impossible).

**Do not roll back** merely because a QB record has gone stale — that is a monitoring
sweep, not a rollback. **Cost of rollback:** losing the QB verification metadata and
returning to a blanket 138-team UNCERTAIN gate. Ratings and spreads are identical in
both workbooks, so no computed output is lost.

## 12. Git commit

| Item | Value |
|---|---|
| Branch | `claude/2026-ncaaf-schedule-build-by6j5n` |
| Promotion-audit commit | `dda2b1a` — *Promotion audit passed: promote v0.7.9 → v0.8.0 AUTHORITATIVE* |
| Candidate commit | `4e6f53a` — *Phase 7D.5: final QB-verification candidate v0.7.9* |
| Backlog-closure commit | `5e3c99c` — *Phase 7D.4A: final five QB resolution* |
| **Phase 7E promotion commit** | recorded in the commit that adds this certificate |

## 13. Promotion rationale

v0.6.2 shipped with an **empty QB dataset — 0 of 138 confidence codes populated**, so
every team computed UNCERTAIN regardless of what was actually known about its
quarterback. v0.8.0 replaces that with 138 populated records, of which all 73 Tier-1
records were independently verified against primary sources and stamped with a
verification date and evidence note.

The change is **purely additive metadata in one data sheet**, plus a changelog and a
banner. It cannot move a rating or a spread — proven three ways in the audit. Eighteen
of twenty-one worksheets are byte-identical to the outgoing authoritative workbook.

**Timing:** with **0 market spreads loaded** and `ENGINE!AI` evaluating PENDING LINE
ahead of QB UNCERTAIN, every game currently reads PENDING LINE. Promotion is
behaviourally inert today, which makes this the safest possible moment to do it —
strictly preferable to promoting mid-week once lines are live.

## 14. Known limitations

Disclosed, not discovered late. Each is equal or worse in v0.6.2.

1. **The internal banner is stale and contains two errors.** `START HERE!A1` still
   reads *"v0.7.9 FINAL QB-VERIFICATION CANDIDATE … NOT AUTHORITATIVE, NOT PROMOTED —
   awaiting owner approval"*, and states *"all 74 Tier-1 records"* when the correct
   figure is **73** (Missouri's M→H upgrade moved it out of Tier 1). Both are text I
   authored in the v0.7.9 build. **They were deliberately NOT corrected**, because
   Phase 7E requires promotion with no workbook content change and byte-identity to
   the audited candidate. Neither string is read by any formula, so nothing computes
   from them. **Recommended: a banner-only v0.8.1 patch — two cells, re-audited — at
   the owner's discretion.**
2. **61 H-coded records were never independently verified.** Out of declared Tier-1
   scope — H meant the starter was established at the July build. **Missouri proved an
   H-tier assumption can go stale.** Their values are all 0, so they cannot move a
   rating; the exposure is a displaced starter sitting unflagged. Spot-check in the
   first monitoring sweep.
3. **The 33 L records are perishable** (§9).
4. **Alabama's note is directionally contested** — it records Keelon Russell as
   slightly favored, while separate same-day reporting has HC Kalen DeBoer suggesting
   Austin Mack may hold a slight edge. Both agree the competition is open, so the `L`
   code is correct either way and nothing downstream is affected. Neutralise the note
   in the first sweep.
5. **Texas Tech remains provisional** — surgeon clearance reported; final team medical
   clearance expected around the nine-month mark (~2026-08-21).
6. **Three thin confirmations** — Ball State, Central Michigan and Nebraska rest partly
   on absence of contradicting evidence. All L-coded, so the exposure is bounded.
7. **No cached formula results** are stored in either workbook (0 of 123,011 in both).
   Excel and Google Sheets recalculate on open. **Pre-existing property of v0.6.2, not
   a regression.**
8. **The native Google Sheet still holds v0.6.2.** It was never accessed by any phase
   of this project. Importing v0.8.0 is an owner action — take a Sheets version
   snapshot first.

---

## Certification

The workbook now authoritative is:

> **`promotion_v0.8.0/TTW_College_Football_Power_Ratings_v0.8.0_AUTHORITATIVE.xlsx`**
> **SHA-256 `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7`**

**No workbook content changed during promotion.** The promoted file is byte-for-byte
identical to the audited `v0.7.9_CANDIDATE`; `cmp` is clean and the SHA-256 is
unchanged before and after every promotion file operation. The only actions taken were
a **file rename** to match the official designation and **directory moves** to archive
superseded versions — neither alters a single byte of workbook content.

**This certificate formally closes the TTW Workbook Build Project.**
