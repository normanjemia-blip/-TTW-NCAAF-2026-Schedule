import json
JL = "qb_research.jsonl"
def add(records):
    existing = {}
    try:
        for l in open(JL):
            r = json.loads(l); existing[r['abbrev']] = r
    except FileNotFoundError:
        pass
    for r in records:
        existing[r['abbrev']] = r  # upsert by abbrev (idempotent)
    with open(JL, "w") as f:
        for r in existing.values():
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"upserted {len(records)}; total unique teams now {len(existing)}")
