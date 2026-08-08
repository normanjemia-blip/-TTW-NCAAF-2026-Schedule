# 01 Conference Database

**Status:** ✅ Built — Phase 2, complete 2026-08-08.

**Start here: [00_CONFERENCE_INDEX.md](00_CONFERENCE_INDEX.md)**

One intelligence file per conference, generated from the eleven preview pages
and every cross-cutting section of the guide that touches a conference.

## Rebuilding

```bash
python3 _tools/extract_conferences.py   # previews + projected standings
python3 _tools/extract_phase2.py        # predictions, win totals, best bets
python3 _tools/build_conferences.py     # → this directory
```

Both extraction scripts exit non-zero on validation failure, so a bad parse
cannot silently become a conference file.

## Rules

Content here follows the standing rules in the [library README](../README.md):
GUIDE CONTENT, POST-PUBLICATION UPDATE and PERSONAL INFERENCE are labelled and
never mixed; gaps are recorded as gaps; page references accompany every claim.
Thematic sections quote the guide verbatim rather than paraphrasing it, and a
section reading *Not addressed in guide* means the source is silent.
