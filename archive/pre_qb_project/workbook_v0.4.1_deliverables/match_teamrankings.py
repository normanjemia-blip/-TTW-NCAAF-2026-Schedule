import ast, html, json

master = json.load(open("master_list.json"))  # row -> [abbrev, canonical_name, conference]
abbrev_by_canon = {v[1]: v[0] for v in master.values()}
conf_by_abbrev = {v[0]: v[2] for v in master.values()}

# Explicit TeamRankings displayed name -> canonical abbrev.
# Built by manual review of every one of the 138 TR rows against the
# canonical TEAM MAP list (no fuzzy/auto-guessing - every entry checked).
TR_TO_ABBREV = {
    "Ohio St": "OHST", "Oregon": "ORE", "Notre Dame": "ND", "Indiana": "IND",
    "Georgia": "UGA", "Texas": "TEX", "Miami": "MIA", "Texas Tech": "TTU",
    "Texas A&M": "TAMU", "Mississippi": "MISS", "LSU": "LSU", "Oklahoma": "OU",
    "Alabama": "ALA", "USC": "USC", "Michigan": "MICH", "Florida": "FLA",
    "Tennessee": "TENN", "Washington": "WASH", "Penn St": "PSU",
    "Missouri": "MIZ", "BYU": "BYU", "SMU": "SMU", "Iowa": "IOWA",
    "Louisville": "LOU", "Auburn": "AUB", "Utah": "UTAH",
    "South Carolina": "SCAR", "Clemson": "CLEM", "Houston": "HOU",
    "Kansas St": "KSU", "Pittsburgh": "PITT", "Vanderbilt": "VAN",
    "Illinois": "ILL", "Virginia": "UVA", "Kentucky": "UK",
    "Arizona St": "AZST", "Arizona": "ARIZ", "TCU": "TCU",
    "Wisconsin": "WISC", "UCLA": "UCLA", "Virginia Tech": "VT",
    "Minnesota": "MINN", "Nebraska": "NEB", "Florida St": "FSU",
    "Oklahoma St": "OKST", "Boise St": "BSU", "Mississippi St": "MSST",
    "NC State": "NCST", "Georgia Tech": "GT", "Kansas": "KAN",
    "Northwestern": "NW", "Arkansas": "ARK", "Baylor": "BAY",
    "West Virginia": "WVU", "California": "CAL", "UCF": "UCF",
    "Maryland": "MD", "Wake Forest": "WAKE", "North Carolina": "UNC",
    "Fresno St": "FRES", "Duke": "DUKE", "San Diego St": "SDSU",
    "Navy": "NAVY", "Rutgers": "RUTG", "Cincinnati": "CIN",
    "Iowa St": "ISU", "Syracuse": "SYR", "Michigan St": "MSU",
    "UNLV": "UNLV", "Army": "ARMY", "Colorado": "COLO", "UTSA": "UTSA",
    "J Madison": "JMU", "Memphis": "MEM", "Washington St": "WSU",
    "Texas St": "TXST", "New Mexico": "UNM", "Purdue": "PUR",
    "S Florida": "USF", "North Dakota State": "NDSU", "Tulane": "TULN",
    "Stanford": "STAN", "E Carolina": "ECU", "Utah St": "USU",
    "Old Dominion": "ODU", "Boston College": "BC", "Hawai'i": "HAW",
    "Air Force": "AFA", "Troy": "TROY", "W Michigan": "WMU",
    "W Kentucky": "WKU", "Liberty": "LIB", "Toledo": "TOL",
    "Louisiana Tech": "LT", "N Texas": "UNT", "Florida Atlantic": "FAU",
    "Marshall": "MRSH", "Oregon St": "ORST", "Louisiana": "ULL",
    "Tulsa": "TLSA", "Miami OH": "M-OH", "Colorado St": "CSU",
    "Jacksonville St": "JVST", "S Alabama": "USA", "Ohio": "OHIO",
    "Temple": "TEM", "UConn": "CONN", "App State": "APP",
    "Arkansas St": "ARST", "Georgia So": "GASO", "Delaware": "DEL",
    "C Michigan": "CMU", "Wyoming": "WYO", "Coastal Car": "CCU",
    "E Michigan": "EMU", "Kennesaw St": "KENN", "San Jose St": "SJSU",
    "Florida Intl": "FIU", "Rice": "RICE", "Buffalo": "BUFF",
    "Bowling Green": "BGSU", "Southern Miss": "USM", "Akron": "AKR",
    "Nevada": "NEV", "UAB": "UAB", "New Mexico St": "NMSU",
    "Missouri St": "MOST", "Sacramento State": "SAC",
    "Georgia St": "GAST", "UL Monroe": "ULM", "N Illinois": "NIU",
    "Middle Tenn": "MTSU", "UTEP": "UTEP", "Kent St": "KENT",
    "Ball St": "BALL", "Charlotte": "CLT", "Sam Houston": "SHSU",
    "UMass": "MASS",
}

rows = []
with open("tr_teams_dump.txt") as f:
    for line in f:
        line = line.strip()
        if not line or not line.startswith("("):
            continue
        rank, name, rating = ast.literal_eval(line)
        name = html.unescape(name)
        rows.append((int(rank), name, float(rating)))

print(f"Parsed {len(rows)} TeamRankings rows")

matched = {}
unmatched = []
for rank, name, rating in rows:
    ab = TR_TO_ABBREV.get(name)
    if ab is None:
        unmatched.append((rank, name, rating))
    else:
        if ab in matched:
            print(f"DUPLICATE MATCH: {ab} already matched, now also matches {name}")
        matched[ab] = {"rank": rank, "name_tr": name, "rating": rating}

print(f"Matched: {len(matched)} / {len(rows)}")
print(f"Unmatched: {unmatched}")

# Cross-check: every one of the 138 master-list abbrevs got exactly one TR match
missing_from_tr = [ab for ab in abbrev_by_canon.values() if ab not in matched]
print(f"Master-list abbrevs with NO TeamRankings match: {missing_from_tr}")

# Conference sanity spot-check for a few disambiguation-prone teams
for ab in ["UNT", "NIU", "USF", "USA", "ECU", "EMU", "WMU", "CMU", "JMU", "GASO", "MISS", "MSST"]:
    print(ab, "->", conf_by_abbrev.get(ab), "|", matched.get(ab))

json.dump(matched, open("tr_matched.json", "w"), indent=2)
print("\nWrote tr_matched.json")
