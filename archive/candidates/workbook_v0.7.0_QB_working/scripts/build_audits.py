import json, csv
rows=[json.loads(l) for l in open('qb_research.jsonl')]
teams=json.load(open('teams_138.json'))
order={t['abbrev']:t['row'] for t in teams}
rows.sort(key=lambda r: order[r['abbrev']])
RD="2026-07-21"  # research date

# 1. Full CSV
cols=['abbrev','team','conference','active_qb','status_type','prev_school','confidence',
      'confirmed_level','injury_eligibility','stats_2025','candidates','notes','sources','research_date']
with open('qb_research.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(cols)
    for r in rows:
        w.writerow([r['abbrev'],r['team'],r['conference'],r['active_qb'],r['status_type'],
            r.get('prev_school'),r['confidence'],r['confirmed_level'],r.get('injury_eligibility'),
            r.get('stats_2025'),' | '.join(r.get('candidates') or []),r.get('notes'),
            ' ; '.join(f"{s['name']} ({s['url']}, {s.get('date','')})" for s in r['sources']),RD])
json.dump(rows, open('qb_research.json','w'), indent=1, ensure_ascii=False)

# 2. Source audit (every team + supporting sources)
with open('source_audit.md','w') as f:
    f.write("# Phase 8 QB Research — Source Audit (all 138 FBS teams)\n\n")
    f.write(f"Research date: {RD}. Every team has >=1 recorded source; competitions cite multiple where possible.\n\n")
    f.write("| Team | Abbrev | Conf | Active QB | Conf | Sources |\n|---|---|---|---|---|---|\n")
    for r in rows:
        srcs='<br>'.join(f"[{s['name']}]({s['url']}) — {s.get('date','')}" for s in r['sources'])
        f.write(f"| {r['team']} | {r['abbrev']} | {r['conference']} | {r['active_qb']} | {r['confidence']} | {srcs} |\n")

# 3. Unresolved competitions (confidence L)
comps=[r for r in rows if r['confidence']=='L']
with open('unresolved_competitions.md','w') as f:
    f.write(f"# Unresolved QB Competitions (confidence L) — {len(comps)} teams\n\n")
    f.write("These are genuinely open competitions / injury or eligibility questions / insufficient info. "
            "No starter was forced; Baseline QB is left blank (identity not established).\n\n")
    f.write("| Team | Reported leader / status | Candidates | Reason |\n|---|---|---|---|\n")
    for r in comps:
        f.write(f"| {r['team']} ({r['abbrev']}) | {r['active_qb']} | {' | '.join(r.get('candidates') or [])} | {r['confirmed_level']} |\n")

# 4. Injury / eligibility concerns
inj=[r for r in rows if r.get('injury_eligibility')]
with open('injury_eligibility.md','w') as f:
    f.write(f"# Injury / Eligibility / Suspension Concerns — {len(inj)} teams\n\n")
    f.write("| Team | QB | Concern |\n|---|---|---|\n")
    for r in inj:
        f.write(f"| {r['team']} ({r['abbrev']}) | {r['active_qb']} | {r['injury_eligibility']} |\n")

print("CSV rows:", len(rows))
print("Unresolved competitions (L):", len(comps))
print("Injury/eligibility notes:", len(inj))
print("Files: qb_research.csv, qb_research.json, source_audit.md, unresolved_competitions.md, injury_eligibility.md")
