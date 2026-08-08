# Source Manifest

Provenance and integrity record for every source this library draws on.
Anything not listed here has **not** been consulted.

---

## Primary source

| Field | Value |
| --- | --- |
| Title | 2026 VSiN College Football Betting Guide |
| Pages | 345 |
| File | `_source/2026-VSiN-CFB-Betting-Guide.pdf` (committed) |
| Size | 6,995,586 bytes |
| MD5 | `a4af70fac06969d33f2c5b8ceb94aff1` |
| PDF version | 1.6 |
| Origin | Uploaded to the repository by the Director, 2026-08-07 (commit `c1ec899`, branch `claude/2026-ncaaf-schedule-build-by6j5n`) |
| Originally retrieved | 2026-08-06 from Google Drive, file ID `18bWkdYxqqkAft1E8lnoV5xAVgEy7_jym` |

**Verify the MD5 before trusting this library against a different copy.** A
re-issued or corrected printing would shift page numbers and invalidate every
page reference here.

The guide is **committed alongside the library** so the whole thing is
self-contained and rebuildable without external retrieval. It was originally
obtained from the Director's Drive and later uploaded to the repository; both
copies are byte-identical, verified by MD5.

### Verification history

| Date | Event | Result |
| --- | --- | --- |
| 2026-08-06 | Phase 1 built from the Drive copy | validation passed |
| 2026-08-08 | Repository copy verified against the Drive copy | MD5 identical |
| 2026-08-08 | Full pipeline re-run against the repository copy | index regenerated **byte-for-byte identical**; zero diffs |

The re-run is the meaningful check: it confirms the Master Index is fully
reproducible from the committed source, so nothing in it depends on a transient
file or a one-off manual step.

### Quality of the source file

Two other files with the same name exist in the Director's Drive
(`1d7h2ccicIr5c_sJF8BS-t_D7a67ROUir`, `1UwLHFuO3BZu7zMMRlhEwCpTbn1PcvTyc`).
Both are **1 byte** — failed uploads. Neither was used. The file above is the
only complete copy.

---

## Extraction method

| Field | Value |
| --- | --- |
| Library | PyMuPDF 1.28.0 (MuPDF 1.29.0) |
| Mode | `page.get_text("text")` for prose; `get_text("dict")` for font-size-aware field extraction |
| Script | `_tools/extract_guide.py` |
| Text layer | Present on all 345 pages — **no OCR was required and none was performed** |
| Image-only pages | None |
| Characters extracted | 1,028,199 |

Because every page carries a real text layer, extraction is lossless with
respect to characters. No content was reconstructed, inferred or transcribed.

### Known extraction constraints

The guide is a design-led layout. On the team pages, values sit in visual tables
whose reading order in the text layer does not always match their visual order.
This affects three things, all of which are **deliberately excluded from Phase 1**
rather than guessed:

1. **Returning-starter counts** — three numbers under `total / offense / defense`
   whose label-to-value mapping cannot be resolved from text order alone.
2. **Futures prices** — three prices whose pairing to `CFP Championship`,
   `make the playoff` and the conference line is likewise ambiguous.
3. **Statistics values** — the 27 category values and their national ranks are
   emitted in separate runs from their labels.

All three require coordinate-based (x/y) extraction. The category *names* and
schema are verified and published; the *values* are not, and no partial or
probable mapping appears anywhere in this library.

---

## Validation performed

`extract_guide.py` refuses to emit output unless all of the following hold. Every
check passed on the build of 2026-08-06:

| Check | Result |
| --- | --- |
| 138 teams parsed from the contents page | ✅ |
| 11 conferences parsed | ✅ |
| Head coach, tenure, 2025 records present for all 138 | ✅ 0 missing |
| Power rating present and unambiguous for all 138 | ✅ 0 ambiguous |
| National ranks form a complete 1–138 sequence | ✅ |
| No rank/rating inversions (rating monotonic with rank) | ✅ 0 violations |
| Statistics schema identical across all 138 teams | ✅ 0 deviations |
| Youmans Top 50 complete | ✅ 50/50 |
| Stone Top 15 quarterbacks complete | ✅ 15/15 |
| Every team page carries a coach line and a record line | ✅ 0 anomalies |

The rank/rating monotonicity check is the strongest signal available: it
independently confirms that the power rating captured for each team is the one
that belongs to that team, since a misattributed rating would almost certainly
break the ordering.

---

## Cross-check findings

**Coaching carousel vs. team pages.** 34 coaches are listed as entering Year 1 on
their team pages; all 34 have a profile in The Coaching Carousel (pp. 28–37). The
carousel carries one extra: **Mark Carney (Kent State)**, whose team page shows
Year 2. The guide explains this itself — Carney was Kent State's interim in 2025
and had the tag removed mid-season (p. 34). Recorded as a definitional
difference, not an error; both figures stand as printed.

---

## Apparent errors in the source

Recorded, never silently corrected. Guide text is reproduced as printed; the
correction is kept separate and labelled `PERSONAL INFERENCE`.

| Location | As printed | Probable intent |
| --- | --- | --- |
| p. 2, abbreviations | `PYPG – Passing Yards per Page` | Passing Yards per **Game**, by analogy with `RYPG` and `TYPG` |

---

## Optional reference sources

| Source | Status |
| --- | --- |
| TTW College Football Power Ratings Workbook v0.8.1 AUTHORITATIVE | **Not consulted.** Present in the Director's Drive but not read into this library. Required for Phase 6. |

---

## Outside research

**None performed.** No `POST-PUBLICATION UPDATE` content exists anywhere in this
library as of Phase 1. Every statement is `GUIDE CONTENT`, except items
explicitly labelled `PERSONAL INFERENCE` (the `PYPG` typo note, the Carney
reconciliation, and the recommendations in
[13 — Open Questions and Gaps](../00_Master_Index/13_Open_Questions_And_Gaps.md)).

The guide's publication date has not been established from the source, so the
cut-off for what counts as "post-publication" is currently undefined. This
matters before any outside research begins.
