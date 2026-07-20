"""
v0.4.2: extract the complete 138-team overall SP+ table from ESPN's
official article "2026 college football SP+ rankings for all 138 FBS teams"
(story id 48306284, published 2026-03-27, captured 2026-07-19) and map every
team to its canonical TEAM MAP abbreviation.

Only the OVERALL SP+ column is extracted for the blend; the offensive,
defensive, and special-teams component columns are read but never used,
per the user's directive.
"""
import html as htmllib
import json
import re

SRC = "raw_sources/espn_spplus_article_PAYWALLED_20260719.html"  # capture (filename label 'PAYWALLED' was erroneous; see v0.4.2 CHANGELOG)
ARTICLE_URL = "https://www.espn.com/college-football/story/_/id/48306284/2026-college-football-sp+-rankings-138-fbs-teams"
PUBLISHED = "2026-03-27"  # from the page's own datePublished metadata (2026-03-27T10:33:00Z)

# Explicit ESPN-article name -> canonical abbreviation. Built by manual
# review of all 138 table rows against the canonical TEAM MAP list —
# every entry individually checked, no fuzzy/auto matching.
SPPLUS_TO_ABBREV = {
    "Ohio State": "OHST", "Oregon": "ORE", "Notre Dame": "ND", "Georgia": "UGA",
    "Indiana": "IND", "Texas": "TEX", "Texas Tech": "TTU", "Miami": "MIA",
    "Texas A&M": "TAMU", "LSU": "LSU", "Alabama": "ALA", "Oklahoma": "OU",
    "USC": "USC", "Michigan": "MICH", "Tennessee": "TENN", "Ole Miss": "MISS",
    "Penn St.": "PSU", "BYU": "BYU", "Florida": "FLA", "Missouri": "MIZ",
    "Washington": "WASH", "Iowa": "IOWA", "Clemson": "CLEM",
    "S. Carolina": "SCAR", "Utah": "UTAH", "Auburn": "AUB",
    "Louisville": "LOU", "SMU": "SMU", "Kansas St.": "KSU", "Arizona": "ARIZ",
    "Vanderbilt": "VAN", "Va. Tech": "VT", "Illinois": "ILL", "TCU": "TCU",
    "Florida St.": "FSU", "Houston": "HOU", "Nebraska": "NEB",
    "Oklahoma St.": "OKST", "Boise State": "BSU", "Virginia": "UVA",
    "Pittsburgh": "PITT", "Arizona St.": "AZST", "Ga. Tech": "GT",
    "Duke": "DUKE", "Minnesota": "MINN", "UCLA": "UCLA", "Arkansas": "ARK",
    "NC State": "NCST", "Northwestern": "NW", "Cincinnati": "CIN",
    "Baylor": "BAY", "Miss. St.": "MSST", "Kentucky": "UK",
    "N. Carolina": "UNC", "Maryland": "MD", "California": "CAL",
    "Kansas": "KAN", "Wake Forest": "WAKE", "UNLV": "UNLV", "UCF": "UCF",
    "Wisconsin": "WISC", "Rutgers": "RUTG", "Navy": "NAVY",
    "Iowa State": "ISU", "Colorado": "COLO", "W. Virginia": "WVU",
    "Michigan St.": "MSU", "New Mexico": "UNM", "Syracuse": "SYR",
    "Memphis": "MEM",
    "SDSU": "SDSU",     # San Diego State (San Jose State appears separately as SJSU)
    "NDSU": "NDSU",     # North Dakota State (FBS-reclassifying; prose confirms 72nd)
    "UTSA": "UTSA", "Boston Coll.": "BC", "Stanford": "STAN", "ECU": "ECU",
    "JMU": "JMU", "Fresno St.": "FRES", "Air Force": "AFA", "USF": "USF",
    "Miami-OH": "M-OH", "Purdue": "PUR", "Army": "ARMY", "Hawaii": "HAW",
    "Wash. St.": "WSU", "WKU": "WKU", "Tulane": "TULN", "ODU": "ODU",
    "Texas St.": "TXST", "Troy": "TROY", "Oregon St.": "ORST",
    "Marshall": "MRSH", "Liberty": "LIB", "FAU": "FAU", "WMU": "WMU",
    "Tulsa": "TLSA", "Utah St.": "USU", "J'ville State": "JVST",
    "Colorado St.": "CSU", "La. Tech": "LT", "Arkansas St.": "ARST",
    "Temple": "TEM", "Ga. Southern": "GASO", "Louisiana": "ULL",
    "Kennesaw St.": "KENN", "Wyoming": "WYO", "UConn": "CONN",
    "Toledo": "TOL", "North Texas": "UNT", "Buffalo": "BUFF",
    "App. St.": "APP", "Nevada": "NEV", "CMU": "CMU", "Delaware": "DEL",
    "BGSU": "BGSU", "S. Alabama": "USA", "Ohio": "OHIO", "FIU": "FIU",
    "Coastal Caro.": "CCU", "Rice": "RICE", "EMU": "EMU", "SJSU": "SJSU",
    "NMSU": "NMSU", "UAB": "UAB", "NIU": "NIU", "Missouri St.": "MOST",
    "Akron": "AKR", "Kent St.": "KENT", "UTEP": "UTEP",
    "Sac State": "SAC",  # Sacramento State (FBS-reclassifying; prose confirms 130th)
    "So. Miss": "USM", "UL-Monroe": "ULM", "Georgia St.": "GAST",
    "Ball State": "BALL", "MTSU": "MTSU", "Sam Houston": "SHSU",
    "UMass": "MASS", "Charlotte": "CLT",
}

def main():
    raw = open(SRC).read()
    tables = re.findall(r"<table.*?</table>", raw, re.S)
    assert len(tables) == 2, f"expected 2 tables (teams + conferences), got {len(tables)}"
    rows = re.findall(r"<tr.*?</tr>", tables[0], re.S)
    header = [re.sub(r"<[^>]+>", "", c).strip()
              for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", rows[0], re.S)]
    assert header == ["Team", "SP+", "Off. SP+", "Def. SP+", "ST SP+"], header

    parsed = []
    for r in rows[1:]:
        cells = [htmllib.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)]
        m = re.match(r"(\d+)\.\s*(.+)", cells[0])
        parsed.append({
            "rank": int(m.group(1)),
            "name_espn": m.group(2).strip(),
            "overall": float(cells[1]),
            # components read for the audit record only - NEVER blended:
            "off_raw": cells[2], "def_raw": cells[3], "st_raw": cells[4],
        })

    assert len(parsed) == 138, len(parsed)
    assert len({p["name_espn"] for p in parsed}) == 138, "duplicate team names"
    assert len({p["rank"] for p in parsed}) == 138, "duplicate ranks"
    assert sorted(p["rank"] for p in parsed) == list(range(1, 139))

    master = json.load(open("master_list.json"))
    canonical = {v[0] for v in master.values()}

    matched, unmatched = {}, []
    for p in parsed:
        ab = SPPLUS_TO_ABBREV.get(p["name_espn"])
        if ab is None:
            unmatched.append(p["name_espn"]); continue
        assert ab not in matched, f"duplicate mapping to {ab}"
        assert ab in canonical, f"{ab} not canonical"
        matched[ab] = p

    print(f"Parsed: {len(parsed)} | Matched: {len(matched)} | Unmatched: {unmatched}")
    missing = sorted(canonical - set(matched))
    print(f"Canonical abbrevs with no SP+ row: {missing}")
    assert not unmatched and not missing

    print("NDSU:", matched["NDSU"]["rank"], matched["NDSU"]["overall"])
    print("SAC:", matched["SAC"]["rank"], matched["SAC"]["overall"])
    print("MIA:", matched["MIA"]["overall"], "| M-OH:", matched["M-OH"]["overall"])
    print("SDSU:", matched["SDSU"]["overall"], "| SJSU:", matched["SJSU"]["overall"])

    json.dump(matched, open("spplus_matched.json", "w"), indent=2)
    print("Wrote spplus_matched.json")

if __name__ == "__main__":
    main()
