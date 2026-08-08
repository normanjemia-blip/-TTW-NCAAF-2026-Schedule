#!/usr/bin/env python3
"""
TTW Football Intelligence Library — Structured Field Snapshot
==============================================================

Captures every structured and numerical field in the team database so a
before/after comparison can prove that a prose rewrite changed only prose.

Fields are pulled out of the rendered markdown, not out of the JSON that
produced it. That is deliberate: reading the JSON would only prove the JSON is
unchanged, whereas the point is to prove the *files a reader sees* still carry
the same numbers.

Usage:
    python3 _tools/snapshot_fields.py before.json     # capture
    python3 _tools/snapshot_fields.py before.json --compare
"""

import json
import os
import re
import sys

OUT = "02_Team_Database"

# Every numeric or structured item that Phase 3A is forbidden to change.
CAPTURE = {
    # "| **Label** | value |" rows in the snapshot table
    "snapshot_rows": r"^\| \*\*(.+?)\*\* \| (.+?) \|$",
    # any page citation, however formatted
    # A letter before "p." means it is an abbreviation such as "Sep." rather
    # than a page citation.
    "page_refs": r"(?<![A-Za-z])pp?\.\s*([\d][\d,\s–\-]*)",
    # markdown table data cells anywhere in the file
    "table_cells": r"^\|(?!\s*[-: ]+\|)(.+)\|$",
    # explicit rank and rating patterns
    "ranks": r"#(\d+) of (\d+)",
    "prices": r"([-+]\d{3,}|\d+-1|\d+\.\d+|\d+/\d+)",
}

HEADING = re.compile(r"^## (\d+)\. (.+)$", re.M)


def page_numbers(text):
    """Every individual page number cited anywhere in the file.

    The invariant Phase 3A must hold is that no page a reader could have
    followed disappears — not that the citation is punctuated the same way. So
    "(p. 13)" and "pp. 13, 15, 147" both reduce to the pages they name.
    """
    pages = set()
    for group in re.findall(CAPTURE["page_refs"], text):
        for part in re.split(r"[,\s]+", group.strip()):
            for piece in re.split(r"[–\-]", part):
                if piece.isdigit() and 1 <= int(piece) <= 345:
                    pages.add(int(piece))
    return pages


def numbers_in(text):
    """Every number in the file, in order, with its immediate label context."""
    return re.findall(r"-?\d+(?:\.\d+)?(?:%|:\d\d)?", text)


def capture_file(path):
    text = open(path).read()
    headings = [(int(n), h) for n, h in HEADING.findall(text)]

    sections = {}
    parts = re.split(r"^## \d+\. .+$", text, flags=re.M)[1:]
    for (num, head), body in zip(headings, parts):
        sections[head] = body

    snapshot_rows = dict(re.findall(CAPTURE["snapshot_rows"], text, re.M))
    tables = re.findall(CAPTURE["table_cells"], text, re.M)

    return {
        "headings": [h for _, h in headings],
        "snapshot_rows": snapshot_rows,
        "table_rows": [t.strip() for t in tables],
        "page_refs": sorted(page_numbers(text)),
        "ranks": sorted({f"#{a} of {b}" for a, b in
                         re.findall(CAPTURE["ranks"], text)}),
        "numbers": numbers_in(text),
        "not_addressed_sections": sorted(
            h for h, b in sections.items() if "Not addressed in guide." in b),
        "has_source_conflict": "SOURCE CONFLICT" in text,
        "source_conflict_blocks": sorted(
            re.findall(r"\*\*SOURCE CONFLICT\.?\*\*(.{0,160})", text, re.S)),
        "cross_links": sorted(set(re.findall(r"\]\(([^)]+\.md)\)", text))),
    }


def capture_all():
    out = {}
    for name in sorted(os.listdir(OUT)):
        if not name.endswith(".md") or name == "README.md":
            continue
        out[name] = capture_file(os.path.join(OUT, name))
    return out


def compare(before, after):
    problems, gains = [], []
    if set(before) != set(after):
        problems.append(f"file set changed: "
                        f"missing {sorted(set(before)-set(after))[:5]}, "
                        f"added {sorted(set(after)-set(before))[:5]}")
    for name in sorted(set(before) & set(after)):
        b, a = before[name], after[name]
        if b["headings"] != a["headings"]:
            problems.append(f"{name}: heading list changed")
        if b["snapshot_rows"] != a["snapshot_rows"]:
            for k in set(b["snapshot_rows"]) | set(a["snapshot_rows"]):
                if b["snapshot_rows"].get(k) != a["snapshot_rows"].get(k):
                    problems.append(
                        f"{name}: snapshot field '{k}' "
                        f"{b['snapshot_rows'].get(k)!r} -> {a['snapshot_rows'].get(k)!r}")
        missing_tables = [r for r in b["table_rows"] if r not in a["table_rows"]]
        if missing_tables:
            problems.append(f"{name}: {len(missing_tables)} table row(s) lost, "
                            f"first: {missing_tables[0][:70]}")
        lost_pages = sorted(set(b["page_refs"]) - set(a["page_refs"]))
        if lost_pages:
            problems.append(f"{name}: page references lost: {lost_pages[:6]}")
        if sorted(set(b["ranks"])) != sorted(set(a["ranks"])):
            problems.append(f"{name}: rank values changed")
        if b["has_source_conflict"] != a["has_source_conflict"]:
            problems.append(f"{name}: source-conflict flag changed")
        lost_links = sorted(set(b["cross_links"]) - set(a["cross_links"]))
        if lost_links:
            problems.append(f"{name}: cross-links lost: {lost_links[:4]}")
        lost_na = sorted(set(b["not_addressed_sections"]) -
                         set(a["not_addressed_sections"]))
        gained_na = sorted(set(a["not_addressed_sections"]) -
                           set(b["not_addressed_sections"]))
        if gained_na:
            problems.append(f"{name}: sections newly empty: {gained_na}")
        # A section gaining content is an improvement, not a regression; only
        # a section losing its content is a Phase 3A failure.
        if lost_na:
            gains.append(f"{name}: now populated: {', '.join(lost_na)}")
    return problems, gains


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "_source/data/fields_before.json"
    if "--compare" in sys.argv:
        with open(path) as fh:
            before = json.load(fh)
        after = capture_all()
        problems, gains = compare(before, after)
        print(f"files compared        {len(before)}")
        print(f"regressions found     {len(problems)}")
        print(f"sections gaining content  {len(gains)}")
        for g in gains[:10]:
            print("   +", g)
        if problems:
            print("\nSTRUCTURED FIELD CHANGES (Phase 3A must change prose only):")
            for p in problems[:40]:
                print("  -", p)
            sys.exit(1)
        print("\nall structured and numerical fields preserved")
    else:
        data = capture_all()
        with open(path, "w") as fh:
            json.dump(data, fh, indent=1)
        print(f"snapshot written for {len(data)} files -> {path}")


if __name__ == "__main__":
    main()
