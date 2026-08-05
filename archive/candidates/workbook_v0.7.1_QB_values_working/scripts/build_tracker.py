import json, csv
rows={r['abbrev']:r for r in [json.loads(l) for l in open('qb_research.jsonl')]}
audit={a['abbrev']:a for a in json.load(open('baseline_audit.json'))}
exc=[a for a in audit.values() if a['disposition']=='EXCEPTION']

BEST="Official team depth chart / athletics release; HC or OC press conference; established local beat writer; 247Sports/On3 camp reporting"
def leader(r):
    aq=r['active_qb']
    return "" if aq.startswith("Open") else aq

# per-team overrides: (condition, next_checkpoint, baseline_assumption, elig, nonzero, notes)
OV={
 "UNC":("Edwards confirmed fully healthy (PCL) AND established as QB1 (not merely 'inside track')",
        "Fall camp early-Aug 2026; injury clearance; first depth chart",
        "Not established (Edwards presumed but injured/unsettled)",
        "N until healthy & established (per instruction)","Possibly — only if resolved starter is a meaningful downgrade vs a healthy Edwards baseline",
        "DO NOT initialize until Edwards is healthy enough to participate normally and is the established projected starter."),
 "TTU":("Hammond ACL medical clearance (~Aug 21, 2026) AND named starter; else Kirk Francis named",
        "~Aug 21, 2026 (ACL clearance); game-week depth chart",
        "Not established (Hammond injured; Francis fallback)",
        "N until cleared & starting","Possibly — if Francis (or a not-fully-cleared Hammond) is a downgrade vs the presumed healthy Hammond",
        "Injury + eligibility (gambling-investigation reference) cloud; re-confirm each week once resolved."),
 "STAN":("Warren ACL recovery confirmed AND competition (Rizk, Mitchell Jr.) resolved to a starter",
        "Fall camp early-Aug 2026; injury update; depth chart",
        "Not established (Warren injured; open)",
        "TBD — Y if a healthy settled starter emerges","Possibly — depends on who wins and health",
        "Both injury recovery AND an open competition to resolve."),
 "SYR":("Angeli Achilles recovery confirmed AND competition (Odom) resolved",
        "Fall camp early-Aug 2026; injury update; depth chart",
        "Not established (Angeli injured; Odom competing)",
        "TBD — Y if healthy & named","Possibly — if a non-Angeli starter or limited Angeli",
        "Achilles recovery timeline is the key gate."),
 "NEB":("Reconcile SI (Colandrea) vs Yahoo (Lateef) via an official/coach statement or 2+ agreeing credible sources — do NOT pick the newest article",
        "Fall camp; official depth chart; HC presser",
        "Not established (source conflict: Colandrea vs Lateef; Kaelin option)",
        "TBD — Y once one starter is confirmed by consensus","Possibly — only if the confirmed starter is a clear up/downgrade vs the presumed baseline",
        "Category = conflicting sourcing: two reputable outlets name different QB1s."),
 "TENN":("Reconcile SI (Brandon) vs Saturday Down South/Yahoo (MacIntyre); Staub also in mix — need official/coach statement or 2+ agreeing sources",
        "Fall camp; official depth chart; HC presser",
        "Not established (source conflict: Brandon vs MacIntyre; Staub veteran option)",
        "TBD — Y once one starter is confirmed by consensus","Possibly — a true-freshman winner could warrant a small negative; a veteran winner likely 0",
        "Category = conflicting sourcing; wide-open per multiple outlets."),
 "VAN":("Confirm Curtis (or another) as Day-1 starter; note this is a young-starter case, not a true competition",
        "Fall camp; HC statement",
        "Jared Curtis (consistently projected Day-1 starter)",
        "Y — RECOMMENDED reclassify to Medium (true-freshman youth alone should not force Low)","Unlikely — deviation-only init at 0 if reclassified to M",
        "CLASSIFICATION CORRECTION: currently L/'open competition' but Curtis is the consistently-projected starter (Berlowitz is a backup). Recommend Medium + zero-init. NOT applied in this documentation phase."),
}

def condition(a):
    if a['abbrev'] in OV: return OV[a['abbrev']][0]
    if a['category']=='injury/availability': return "Medical clearance to participate normally AND confirmed as the starter"
    if a['category']=='conflicting/insufficient sourcing': return "Reconcile conflicting reports via official/coach statement or 2+ agreeing credible sources (do not pick the newest article)"
    return "Official depth chart or HC/OC announcement of QB1 (or clear 2+ source consensus)"
def checkpoint(a):
    if a['abbrev'] in OV: return OV[a['abbrev']][1]
    return "Fall camp: early-mid Aug 2026; re-check game week (official depth chart)"
def baseline_assume(a):
    if a['abbrev'] in OV: return OV[a['abbrev']][2]
    ld=leader(rows[a['abbrev']])
    return (ld+" (presumed incumbent, not locked)") if ld else "Not established (competition unresolved)"
def elig(a):
    if a['abbrev'] in OV: return OV[a['abbrev']][3]
    return "TBD — Y if resolved starter = presumed baseline and no unresolved issue"
def nonzero(a):
    if a['abbrev'] in OV: return OV[a['abbrev']][4]
    return "TBD — Y only if the resolved starter is a meaningful up/downgrade vs the presumed baseline"
def notes(a):
    if a['abbrev'] in OV: return OV[a['abbrev']][5]
    return ""

GROUPS=["open competition","injury/availability","conflicting/insufficient sourcing"]
recs=[]
for a in exc:
    r=rows[a['abbrev']]; src=r['sources'][0]
    recs.append({
      "team":a['team'],"abbrev":a['abbrev'],"conference":r['conference'],
      "current_category":a['category'],"current_confidence":r['confidence'],
      "current_candidates":" | ".join(r.get('candidates') or []),
      "current_leader":leader(r),
      "baseline_qb_assumption":baseline_assume(a),
      "condition_to_clear":condition(a),
      "best_source_types":BEST,
      "most_recent_source":f"{src['name']} ({src.get('date','')})",
      "most_recent_source_url":src['url'],
      "next_research_checkpoint":checkpoint(a),
      "final_resolution":"PENDING","resolution_source":"","confidence_after_resolution":"",
      "eligible_for_zero_init":elig(a),
      "requires_proposed_nonzero_deviation":nonzero(a),
      "notes":notes(a),
    })
# order by group then abbrev
recs.sort(key=lambda x:(GROUPS.index(x['current_category']),x['abbrev']))
cols=list(recs[0].keys())
with open('qb_exception_resolution_tracker.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(recs)
json.dump({"generated":"2026-07-21","total_exceptions":len(recs),
           "groups":{g:[r['abbrev'] for r in recs if r['current_category']==g] for g in GROUPS},
           "records":recs}, open('qb_exception_resolution_tracker.json','w'), indent=1, ensure_ascii=False)
from collections import Counter
print("tracker rows:", len(recs), "| by group:", dict(Counter(r['current_category'] for r in recs)))
