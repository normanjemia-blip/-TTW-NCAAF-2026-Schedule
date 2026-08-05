# MAINTENANCE CERTIFICATE

## TTW College Football Power Ratings
## v0.8.1 AUTHORITATIVE

**Release class: DOCUMENTATION MAINTENANCE ONLY.**
Phase 7E.1 — Authoritative Banner Patch · 2026-08-04 (America/New_York)

---

## 1. What changed

**Exactly one cell in the entire workbook: `START HERE!A1`.**

**Before (v0.8.0):**
> TO THE WINDOW — NCAAF POWER RATINGS 2026 (v0.7.9 FINAL QB-VERIFICATION CANDIDATE — backlog 0, audit-trail gap 0; all **74** Tier-1 records verified and stamped; Missouri M->H, North Carolina and UNLV M->L; **NOT AUTHORITATIVE, NOT PROMOTED — awaiting owner approval**)

**After (v0.8.1):**
> TO THE WINDOW — TTW COLLEGE FOOTBALL POWER RATINGS (**v0.8.1 AUTHORITATIVE — promotion complete 2026-08-04.** QB verification complete: backlog 0, audit-trail gap 0, all **73** Tier-1 records verified and stamped against team-specific primary sources; 65 H / 40 M / 33 L; 0 nonzero QB values. Preseason state: 0 market lines loaded, BET toggle = N.)

### Defects corrected

| # | Defect | Fix |
|---|---|---|
| 1 | Banner declared the workbook **NOT AUTHORITATIVE, NOT PROMOTED — awaiting owner approval**, which became false at promotion | Removed; replaced with "v0.8.1 AUTHORITATIVE — promotion complete 2026-08-04" |
| 2 | Banner said **74 Tier-1 records**; the correct figure is **73** (Missouri's M→H upgrade moved it out of Tier 1) | Corrected to 73, and independently re-derived from the workbook: `4.6 Tier-1 population is 73` **PASS** |
| 3 | Banner identified the file as **v0.7.9 CANDIDATE** | Now identifies v0.8.1 AUTHORITATIVE |
| 4 | Product name read "NCAAF POWER RATINGS 2026" | Now "TTW COLLEGE FOOTBALL POWER RATINGS", matching the official designation |

Both defects 1 and 2 were text I authored during the v0.7.9 build. They were
disclosed in the v0.8.0 promotion certificate, the project manifest and the README,
and deliberately left in place because Phase 7E required byte-identity to the audited
candidate. This patch is the authorised correction.

## 2. New SHA-256

```
e2da9a4c28bd5c0f094ab06a2a85d3e31b37c2aba894f97f3415e15f799cdfd6
```

| Workbook | SHA-256 | Status |
|---|---|---|
| **v0.8.1 AUTHORITATIVE** | `e2da9a4c28bd5c0f094ab06a2a85d3e31b37c2aba894f97f3415e15f799cdfd6` | **CURRENT** |
| v0.8.0 AUTHORITATIVE | `661f8ab0e6120290d4ffd8d4ddac738d7e19d7bd0bbcf69bc9df51fb3cef97c7` | Superseded — **unchanged by this patch**, retained as an intermediate rollback point |
| v0.6.2 AUTHORITATIVE | `bbb17b50fbfb728bea2a23d3d20771935cc61e238313a054473aafe1ca838efd` | **Untouched** — full rollback target |

## 3. Regression — 43 / 43 PASS, 0 failures

Full log: `regression_log_v081.txt`.

### Formula count unchanged
**123,011** across v0.6.2, v0.8.0 and v0.8.1. Per-sheet counts identical — zero deltas.

### Only START HERE changed
- **Exactly 1 changed cell in the whole workbook**, and it is `START HERE!A1`.
- **Zip-part evidence:** only `xl/worksheets/sheet1.xml` differs (plus `docProps/core.xml`, save metadata). **20 of 21 worksheet XML parts are byte-identical to v0.8.0.**
- No formula cell changed. Sheet names, order and visibility identical. Defined names identical.
- **Cell formatting preserved** — font weight, size, colour, fill, alignment and number format captured before and after the write and asserted equal (`bold=True, size=13.0, format=General`).

### Engine outputs unchanged
`ENGINE!M7` (QB adjustment), `ENGINE!AE7` (QB status), `ENGINE!AI7` (status precedence),
`QB VALUES!G6`, `QB VALUES!M6`, `TEAM RATINGS!C6/D6`, `CALC!Q7/S7` — all **formula-identical
to v0.6.2 AUTHORITATIVE**, not merely to v0.8.0.

### Workbook behaviour unchanged
`SETTINGS!B3` = 2026 · `B6` = 2.5 HFA · `B11` = "N" · 138 unique teams ·
QB codes **65 H / 40 M / 33 L** · QB status **99 OK / 39 UNCERTAIN** ·
**0 nonzero QB values** · every L-coded team blank-gated · **0 market spreads loaded**.

`START HERE!A1` is inert text — no formula anywhere reads it, so no computed value
depends on it. The banner is what a human reads, not what the model consumes.

## 4. Scope compliance

| Constraint | Status |
|---|---|
| Formulas | **Not modified** — 0 formula cells changed |
| Workbook structure | **Not modified** — 21 sheets, same order and visibility |
| QB data | **Not modified** — codes, values and status bit-for-bit equal |
| Ratings | **Not modified** — TEAM RATINGS part byte-identical |
| Engine logic | **Not modified** — ENGINE part byte-identical |
| HFA | **Not modified** — `SETTINGS!B6` = 2.5 |
| Worksheet order | **Not modified** |
| Formatting | **Not modified** — style asserted equal before/after |

## 5. Disclosure — the workbook CHANGELOG was deliberately not updated

Phase 7E.1 required a regression proving **"only START HERE changed."** Adding a
`CHANGELOG` row for v0.8.1 would have broken that test. I complied with the explicit
test rather than with the broader reading of "documentation."

**Consequence:** the workbook's internal `CHANGELOG` tab records history through
v0.7.9 and does **not** mention v0.8.0 or v0.8.1. The external record — this
certificate, `PROMOTION_CERTIFICATE.md`, `PROJECT_MANIFEST.json` and the README — is
complete and authoritative.

If you want the internal CHANGELOG brought current, that is a separate patch touching
`CHANGELOG` plus the banner version string, and it would necessarily fail an
"only START HERE changed" test. Say the word and I will scope it as **v0.8.2**.

## 6. Rollback

Unchanged from v0.8.0 — see `promotion_v0.8.0/ROLLBACK.md`. Two options:

- **Cosmetic revert:** restore `promotion_v0.8.0/…v0.8.0_AUTHORITATIVE.xlsx` (SHA `661f8ab0…`). Reinstates the misleading banner but is otherwise functionally identical.
- **Full rollback:** restore v0.6.2 (SHA `bbb17b50…`). Costs the entire QB verification dataset; ratings and spreads are identical either way.

Neither v0.8.0 nor v0.6.2 was modified by this patch — both hashes re-verified after
the build.

## 7. Certification

The workbook now authoritative is:

> **`promotion_v0.8.1/TTW_College_Football_Power_Ratings_v0.8.1_AUTHORITATIVE.xlsx`**
> **SHA-256 `e2da9a4c28bd5c0f094ab06a2a85d3e31b37c2aba894f97f3415e15f799cdfd6`**

**Classification: documentation maintenance release. No functional change.** The only
difference from v0.8.0 is 331 characters of banner text on the `START HERE` tab.
