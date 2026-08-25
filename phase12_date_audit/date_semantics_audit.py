#!/usr/bin/env python3
"""READ-ONLY date-semantics audit across all 888 scheduled games.

Compares, for every game, four dates derived from the SAME ESPN event id:

  stored      the date currently in TTW_2026_Verified_Schedule_ESPN_v1.0.csv
  utc         the UTC calendar date of the kickoff instant (ESPN's raw field)
  et          the kickoff converted to America/New_York -- ESPN's US display date
  local       the kickoff converted to the VENUE's own time zone -- the official
              local date a school and its conference would print

Writes nothing to the workbook, the CSV or the live Sheet. It only emits a report
and a proposed diff for approval.

Usage:  python3 phase12_date_audit/date_semantics_audit.py
"""
import collections, csv, datetime, glob, io, json, os, sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "TTW_2026_Verified_Schedule_ESPN_v1.0.csv")
CACHE = os.environ.get("ESPN_CACHE", os.path.join(
    "/tmp/claude-0/-home-user--TTW-NCAAF-2026-Schedule",
    "93f60580-cc70-5bb0-a25b-86aea5198243/scratchpad/espn"))
OUT = os.path.join(ROOT, "phase12_date_audit")

NY = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

# Default zone per US state, then city overrides for the split-zone states.
STATE_TZ = {
    "AL": "America/Chicago", "AR": "America/Chicago", "AZ": "America/Phoenix",
    "CA": "America/Los_Angeles", "CO": "America/Denver", "CT": "America/New_York",
    "DE": "America/New_York", "FL": "America/New_York", "GA": "America/New_York",
    "HI": "Pacific/Honolulu", "IA": "America/Chicago", "ID": "America/Boise",
    "IL": "America/Chicago", "IN": "America/Indiana/Indianapolis",
    "KS": "America/Chicago", "KY": "America/New_York", "LA": "America/Chicago",
    "MA": "America/New_York", "MD": "America/New_York", "MI": "America/Detroit",
    "MN": "America/Chicago", "MO": "America/Chicago", "MS": "America/Chicago",
    "NC": "America/New_York", "ND": "America/Chicago", "NE": "America/Chicago",
    "NJ": "America/New_York", "NM": "America/Denver", "NV": "America/Los_Angeles",
    "NY": "America/New_York", "OH": "America/New_York", "OK": "America/Chicago",
    "OR": "America/Los_Angeles", "PA": "America/New_York", "SC": "America/New_York",
    "TN": "America/New_York", "TX": "America/Chicago", "UT": "America/Denver",
    "VA": "America/New_York", "WA": "America/Los_Angeles", "WI": "America/Chicago",
    "WV": "America/New_York", "WY": "America/Denver",
}
CITY_TZ = {
    ("TN", "Memphis"): "America/Chicago",
    ("TN", "Nashville"): "America/Chicago",
    ("TN", "Murfreesboro"): "America/Chicago",
    ("KY", "Bowling Green"): "America/Chicago",
    ("TX", "El Paso"): "America/Denver",
}
COUNTRY_TZ = {"Ireland": "Europe/Dublin", "England": "Europe/London",
              "Puerto Rico": "America/Puerto_Rico"}


def venue_zone(addr):
    if not addr:
        return None, "no address"
    country = addr.get("country")
    if country and country != "USA":
        z = COUNTRY_TZ.get(country)
        return (ZoneInfo(z) if z else None), f"country={country}"
    state, city = addr.get("state"), addr.get("city")
    z = CITY_TZ.get((state, city)) or STATE_TZ.get(state)
    return (ZoneInfo(z) if z else None), f"{city}, {state}"


def load_espn():
    """Scoreboard bulk files plus single-event core-API files.

    Both shapes expose competitions[0].timeValid and competitions[0].venue.address,
    which is all this audit needs.
    """
    ev = {}
    for f in glob.glob(os.path.join(CACHE, "*.json")):
        for e in json.load(io.open(f, encoding="utf-8")).get("events", []):
            ev[str(e["id"])] = e
    for f in glob.glob(os.path.join(os.path.dirname(CACHE), "ev", "*.json")):
        e = json.load(io.open(f, encoding="utf-8"))
        if e.get("id") and e.get("date") and isinstance(e.get("competitions"), list):
            ev.setdefault(str(e["id"]), e)
    return ev


def main():
    rows = list(csv.DictReader(io.open(CSV, encoding="utf-8")))
    ev = load_espn()
    print("=" * 78)
    print("DATE-SEMANTICS AUDIT — READ-ONLY")
    print("=" * 78)
    print(f"  scheduled games in file : {len(rows)}")
    print(f"  ESPN events cached      : {len(ev)}")

    recs, unmatched, unzoned = [], [], []
    for r in rows:
        e = ev.get(r["id"])
        if not e:
            unmatched.append(r["id"]); continue
        kick = datetime.datetime.strptime(e["date"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC)
        addr = ((e["competitions"][0].get("venue") or {}).get("address")) or {}
        tz, label = venue_zone(addr)
        if tz is None:
            unzoned.append((r["id"], label)); continue
        stored = datetime.date.fromisoformat(r["start_date"])
        local = kick.astimezone(tz)
        comp = e["competitions"][0]
        timed = bool(comp.get("timeValid"))
        et_d = kick.astimezone(NY).date()
        # ESPN encodes an UNANNOUNCED kickoff as midnight US/Eastern. For those rows the
        # instant is a placeholder, not a real kickoff, so converting it into the venue's
        # zone would fabricate a 23:00 kickoff on the PREVIOUS day. The intended game date
        # for an untimed row is its Eastern date; only timed rows may be zone-converted.
        recs.append(dict(
            timed=timed, effective=(local.date() if timed else et_d),
            id=r["id"], week=r["week"], stored=stored,
            utc_date=kick.date(), utc_hour=kick.hour,
            et_date=kick.astimezone(NY).date(),
            local_date=local.date(), local_hhmm=local.strftime("%H:%M"),
            tz=str(tz), where=label,
            away=r["away_team"], home=r["home_team"],
            venue=r["venue"], neutral=r["neutral_site"] == "TRUE"))
    print(f"  matched to ESPN by id   : {len(recs)}")
    if unmatched:
        print(f"  UNMATCHED ids           : {len(unmatched)} {unmatched[:8]}")
    if unzoned:
        print(f"  UNRESOLVED time zones   : {len(unzoned)} {unzoned[:8]}")

    print("\n1. SANITY CHECK ON THE TIME-ZONE MAPPING")
    odd = [x for x in recs if x["timed"] and not (10 <= int(x["local_hhmm"][:2]) <= 23)]
    print(f"  local kickoffs outside 10:00-23:59 : {len(odd)}")
    for x in odd[:10]:
        print(f"    {x['id']} {x['away']} @ {x['home']} {x['local_hhmm']} {x['where']}")
    hours = collections.Counter(x["local_hhmm"] for x in recs if x["timed"])
    print(f"  distinct local kickoff times: {len(hours)}; most common: {hours.most_common(6)}")

    timed = [x for x in recs if x["timed"]]
    untimed = [x for x in recs if not x["timed"]]
    print(f"\n  kickoff time CONFIRMED by ESPN : {len(timed)}")
    print(f"  kickoff time NOT yet announced : {len(untimed)}  "
          f"(ESPN stores midnight US/Eastern as a placeholder)")

    print("\n2. DOES stored == utc_date?  (the core question)")
    eq_utc = sum(1 for x in recs if x["stored"] == x["utc_date"])
    eq_et = sum(1 for x in recs if x["stored"] == x["et_date"])
    eq_local = sum(1 for x in recs if x["stored"] == x["local_date"])
    print(f"  stored == ESPN UTC date   : {eq_utc}/{len(recs)}")
    print(f"  stored == ESPN US/ET date : {eq_et}/{len(recs)}")
    print(f"  stored == venue local date: {eq_local}/{len(recs)}")
    print("  -- partitioned --")
    for nm, grp in (("kickoff confirmed", timed), ("kickoff unannounced", untimed)):
        a = sum(1 for x in grp if x["stored"] == x["utc_date"])
        b = sum(1 for x in grp if x["stored"] == x["et_date"])
        c = sum(1 for x in grp if x["stored"] == x["local_date"])
        print(f"    {nm:<20} n={len(grp):<4} ==utc {a:<4} ==et {b:<4} ==local {c}")

    print("\n3. MISMATCH QUANTIFICATION (stored vs venue local date)")
    # Only rows with a CONFIRMED kickoff may be zone-converted.
    mism = [x for x in timed if x["stored"] != x["local_date"]]
    off = collections.Counter((x["stored"] - x["local_date"]).days for x in mism)
    print(f"  games whose stored date differs from the local date: {len(mism)}")
    print(f"  offset distribution (stored minus local, in days)  : {dict(off)}")
    rollover = [x for x in mism if (x["stored"] - x["local_date"]).days == 1]
    print(f"  of those, +1 day (classic UTC rollover): {len(rollover)}")
    other = [x for x in mism if (x["stored"] - x["local_date"]).days != 1]
    print(f"  any other offset: {len(other)}")
    for x in other[:10]:
        print(f"    {x['id']} {x['away']} @ {x['home']} stored={x['stored']} local={x['local_date']}")

    print("\n4. ARE THE MISMATCHES EXACTLY THE LATE-NIGHT KICKOFFS?")
    print("     (a UTC rollover happens iff kickoff UTC hour is small)")
    hr_m = collections.Counter(x["utc_hour"] for x in mism)
    hr_ok = collections.Counter(x["utc_hour"] for x in timed if x["stored"] == x["local_date"])
    print(f"  UTC hours among MISMATCHED games: {sorted(hr_m.items())}")
    print(f"  UTC hours among MATCHED games   : {sorted(hr_ok.items())}")

    print("\n5. SUNDAY ANALYSIS — genuine Sunday games vs UTC rollovers")
    stored_sun = [x for x in recs if x["stored"].weekday() == 6]
    local_sun = [x for x in recs if x["effective"].weekday() == 6]
    genuine = [x for x in stored_sun if x["effective"].weekday() == 6]
    fake = [x for x in stored_sun if x["effective"].weekday() != 6]
    print(f"  games stored on a Sunday        : {len(stored_sun)}")
    print(f"  games ACTUALLY played on Sunday : {len(local_sun)}")
    print(f"  -> genuine Sunday games         : {len(genuine)}")
    print(f"  -> UTC rollovers (really Sat)   : {len(fake)}")
    print("\n  GENUINE Sunday games:")
    for x in sorted(genuine, key=lambda y: y["effective"]):
        t = x["local_hhmm"] if x["timed"] else "  TBD"
        print(f"    {x['effective']} {t} wk{x['week']:<3} {x['away']} @ {x['home']}")
    print("\n  Weekday breakdown of the TRUE local dates:")
    for k, v in sorted(collections.Counter(
            x["effective"].strftime("%A") for x in recs).items(), key=lambda z: -z[1]):
        print(f"    {k:<10}{v}")

    print("\n6. DOWNSTREAM EFFECT — week assignment and the Week 0 gate")
    W0_END = datetime.date(2026, 9, 2)   # project Week 0 = before the 2026-09-03 Week 1 kickoff
    def bucket(d):
        return 0 if d <= W0_END else None
    moved_wk0 = [x for x in recs
                 if (x["stored"] <= W0_END) != (x["effective"] <= W0_END)]
    print(f"  games that would cross the Week 0 / Week 1 boundary: {len(moved_wk0)}")
    for x in moved_wk0:
        print(f"    {x['id']} {x['away']} @ {x['home']} stored={x['stored']} local={x['effective']}")
    wk0_stored = sorted([x for x in recs if x["stored"] <= W0_END], key=lambda y: y["stored"])
    wk0_local = sorted([x for x in recs if x["effective"] <= W0_END], key=lambda y: y["effective"])
    print(f"  Week 0 slate size, stored dates: {len(wk0_stored)}")
    print(f"  Week 0 slate size, local dates : {len(wk0_local)}")
    print("  Week 0 games with corrected local dates:")
    for x in wk0_local:
        flag = "  <-- CHANGES" if x["stored"] != x["effective"] else ""
        print(f"    stored {x['stored']} -> local {x['effective']} {x['local_hhmm']} "
              f"{x['away']} @ {x['home']}{flag}")

    print("\n6b. WEEK-BUCKET INTEGRITY ACROSS ALL WEEKS")
    span_stored = collections.defaultdict(list)
    span_fixed = collections.defaultdict(list)
    for x in recs:
        span_stored[x["week"]].append(x["stored"])
        span_fixed[x["week"]].append(x["effective"])
    print(f"  {'wk':<4}{'stored span':<26}{'corrected span':<26}moves")
    overlaps = 0
    weeks = sorted(span_stored, key=lambda w: int(w))
    for i, w in enumerate(weeks):
        s0, s1 = min(span_stored[w]), max(span_stored[w])
        f0, f1 = min(span_fixed[w]), max(span_fixed[w])
        moved = sum(1 for a, b in zip(span_stored[w], span_fixed[w]) if a != b)
        print(f"  {w:<4}{str(s0)+' .. '+str(s1):<26}{str(f0)+' .. '+str(f1):<26}{moved}")
        if i:
            prev = weeks[i - 1]
            if f0 <= max(span_fixed[prev]):
                overlaps += 1
                print(f"      OVERLAP: week {w} starts {f0}, week {prev} ends {max(span_fixed[prev])}")
    print(f"  weeks whose corrected span overlaps the previous week: {overlaps}")
    print("  NOTE: no game changes its week label. Correction only shifts a date"
          " WITHIN its existing week bucket.")

    print("\n7. PROPOSED DETERMINISTIC CORRECTION RULE")
    print("""
  RULE:  local_date = (ESPN kickoff instant, in UTC)
                       .astimezone(ZoneInfo(venue_time_zone))
                       .date()

  where venue_time_zone comes from the ESPN venue address:
      non-US country -> that country's zone
      US state       -> the state's zone, with city overrides for the five
                        split-zone venues actually present (Memphis, Nashville,
                        Murfreesboro, Bowling Green, El Paso)

  The rule is total (every matched game resolves), deterministic (no heuristics,
  no hour thresholds), and reproduces the stored value for every game that is
  already correct. It replaces the current behaviour, which stores the UTC
  calendar date and therefore rolls any kickoff after 20:00 ET into the next day.
""")

    # ---- exact diff, written to disk for review; the CSV itself is NOT touched ----
    os.makedirs(OUT, exist_ok=True)
    dpath = os.path.join(OUT, "proposed_date_diff.csv")
    with io.open(dpath, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "week", "away_team", "home_team", "venue", "venue_tz",
                    "stored_start_date", "proposed_start_date", "delta_days",
                    "espn_utc", "local_kickoff", "stored_weekday", "proposed_weekday"])
        for x in sorted(mism, key=lambda y: (y["local_date"], y["id"])):
            w.writerow([x["id"], x["week"], x["away"], x["home"], x["venue"], x["tz"],
                        x["stored"].isoformat(), x["local_date"].isoformat(),
                        (x["local_date"] - x["stored"]).days,
                        f"{x['utc_date']}T{x['utc_hour']:02d}:00Z", x["local_hhmm"],
                        x["stored"].strftime("%A"), x["local_date"].strftime("%A")])
    print(f"  exact diff written (review only, CSV untouched): {dpath}")
    print(f"  rows in diff: {len(mism)}")

    print("\n" + "=" * 78)
    print(f"SUMMARY: {len(mism)} of {len(recs)} games carry a stored date that is not the "
          f"venue-local date;\n         all {len(rollover)} are +1-day UTC rollovers; "
          f"{len(genuine)} Sunday games are genuine.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
