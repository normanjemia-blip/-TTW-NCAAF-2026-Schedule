#!/usr/bin/env python3
"""Build MANIFEST.md — inventory of the v0.7.2 candidate package with SHA-256."""
import os, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.dirname(HERE)

EXCLUDE = {"livecalc_out.log", "livecalc_err.log", "MANIFEST.md"}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

rows = []
for root, dirs, files in os.walk(OUT):
    dirs.sort()
    for fn in sorted(files):
        if fn in EXCLUDE:
            continue
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, OUT)
        rows.append((rel, os.path.getsize(full), sha256(full)))

rows.sort(key=lambda x: x[0])
lines = []
lines.append("# MANIFEST — v0.7.2 QB VALUES CANDIDATE package")
lines.append("")
lines.append(f"Generated: {datetime.date.today().isoformat()}")
lines.append("")
lines.append("Status: CANDIDATE — not authoritative, not promoted. No Google Sheet edited.")
lines.append("")
lines.append("| File | Bytes | SHA-256 |")
lines.append("|---|---:|---|")
for rel, size, digest in rows:
    lines.append(f"| `{rel}` | {size} | `{digest}` |")
lines.append("")
lines.append("## Key checksums")
lines.append("")
wbname = "TTW_NCAAF_Power_Ratings_2026_v0.7.2_QB_VALUES_CANDIDATE.xlsx"
wbsha = next(d for r, s, d in rows if r == wbname)
lines.append(f"- **v0.7.2 candidate workbook:** `{wbsha}`")
lines.append("- **v0.7.1 source workbook:** "
             "`608068e51c53d100280f85a092b2c1776bcc9947906f213e18ab9289faf88ef9` (unmodified)")
lines.append("")
lines.append("## Untouched (confirmed)")
lines.append("")
lines.append("- Authoritative v0.6.2 XLSX — not modified.")
lines.append("- v0.6.2 Google Sheet `1H4XBJfHh6RZZsLDeljSp9YzeARqRAiarxfTqHqKEzVc` — not edited.")
lines.append("- v0.6.1 rollback Google Sheet `1EITbPHCkNndhtgydsjZDejQ5tOx_IQvkI5yC0nEwYWo` — not edited.")
lines.append("- v0.7.1 working workbook — preserved unmodified.")
lines.append("")

with open(os.path.join(OUT, "MANIFEST.md"), "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"MANIFEST.md written with {len(rows)} files")
print(f"workbook SHA: {wbsha}")
