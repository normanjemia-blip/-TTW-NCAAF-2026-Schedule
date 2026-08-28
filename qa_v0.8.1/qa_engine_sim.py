"""QA Parts 3/4/5 — faithful re-implementation of the ENGINE row logic,
transcribed directly from the v0.8.1 formulas, then driven with scenarios.

Nothing in the workbook is modified. The simulator mirrors the formula text
exactly; where the formula is ambiguous the test asserts on the formula text.
"""
import collections, json

# ---- SETTINGS as shipped in v0.8.1 ----
S = dict(B3=2026, B4=None, B5=None, B6=2.5, B7=0, B8=1, B9=1.5, B10=3, B11="N",
         B12=2.5, B13=5, B14=28, B22=None, B23=None, B24=3)

def engine_row(*, gameid="G1", week=1, date="2026-08-29",
               away="AAA", home="BBB", neutral=0,
               away_type="FBS", home_type="FBS",
               away_rating=10.0, home_rating=14.0,
               team_hfa=2.5, qb_delta_home="", qb_delta_away="",
               qb_status_home="OK", qb_status_away="OK",
               travel_rest=0.0, manual_adj=0.0,
               n_margin_override=0, margin_override_value=None,
               mkt_home_spread="", mkt_total="",
               dup_gameid=1, dup_market_row=0, invalid_favorite=False,
               transitional="", settings=None, min_eff_games=5,
               as_of_minus_line_days=None):
    st = settings or S
    A = "" if gameid in (None,"") else gameid
    if A=="": return {c:"" for c in "ABCDEFGHIJKLMNOPQRSTVWXY"}
    G, H = away_type, home_type
    # I / J  ratings
    I = "" if (G=="FBS" and away_rating is None) else (away_rating if G in ("FBS","FCS") else "")
    J = "" if (H=="FBS" and home_rating is None) else (home_rating if H in ("FBS","FCS") else "")
    K = "" if (I=="" or J=="") else J - I                      # neutral diff
    # L  HFA
    if neutral==1:      L = st["B7"]
    elif H != "FBS":    L = st["B6"]
    else:               L = team_hfa
    # M  QB adj  (blank delta coerced to 0)
    def z(x): return 0 if x=="" else x
    M = 0 if H!="FBS" else (z(qb_delta_home) - (0 if G!="FBS" else z(qb_delta_away)))
    N, O = travel_rest, manual_adj
    P = "" if K=="" else K + L + M + N + O
    Q = margin_override_value if n_margin_override==1 else ""
    R = Q if isinstance(Q,(int,float)) else ("" if P=="" else P)
    S_ = "" if (R=="") else (f"{home} -{abs(R):.1f}" if R>0 else (f"{away} -{abs(R):.1f}" if R<0 else "PICK"))
    T = mkt_home_spread
    V = "" if (R=="" or T=="") else R + T
    W = "" if V=="" else (home if V>0 else away)
    # AE QB status
    away_unc = False if G!="FBS" else (qb_status_away!="OK")
    home_unc = False if H!="FBS" else (qb_status_home!="OK")
    AE = "QB UNCERTAIN" if (away_unc or home_unc) else "OK"
    AF = transitional
    AG = "FCS OPP" if (G=="FCS" or H=="FCS") else ""
    # AH block reasons
    AH = ""
    if dup_gameid>1: AH += "DUP GAMEID; "
    if G=="BLOCK" or H=="BLOCK": AH += "TEAM NOT FOUND; "
    if G=="FBS" and I=="": AH += "AWAY RATING MISSING; "
    if H=="FBS" and J=="": AH += "HOME RATING MISSING; "
    if invalid_favorite: AH += "INVALID FAVORITE; "
    if dup_market_row==1: AH += "DUPLICATE MARKET ROW; "
    if n_margin_override>1: AH += "DUPLICATE OVERRIDE; "
    # CALC S (pending) and Q (stale)
    calc_S = 0 if K=="" else (1 if (T=="" or T is None) else 0)
    if st["B5"] is None or as_of_minus_line_days is None: calc_Q = 0
    else: calc_Q = 1 if as_of_minus_line_days > st["B13"] else 0
    # AI status precedence
    if   AH != "":            AI = "BLOCKED"
    elif AG != "":            AI = "FCS — NO PLAY"
    elif calc_S == 1:         AI = "PENDING LINE"
    elif calc_Q == 1:         AI = "STALE LINE"
    elif AE == "QB UNCERTAIN":AI = "QB UNCERTAIN"
    elif AF != "":            AI = "TRANSITION UNCERTAIN"
    elif week=="" or date=="":AI = "DATA INCOMPLETE"
    else:                     AI = "READY"
    # X spread label
    if V=="" or AI in ("BLOCKED","PENDING LINE","STALE LINE"): X=""
    elif abs(V) < st["B8"]: X=""
    elif abs(V) < st["B9"]: X="LEAN"
    elif (abs(V) < st["B10"] or st["B11"]!="Y" or AI!="READY" or AF!="" or AG!=""): X="INVESTIGATE"
    else: X="BET"
    # Y model total
    Y = "" if (st["B22"] is None or st["B23"] is None or G!="FBS" or H!="FBS") else "COMPUTED"
    Z_ = mkt_total
    AA = "" if (Y=="" or Z_=="") else "TOTALEDGE"
    # AJ confidence
    if AI in ("","BLOCKED","PENDING LINE","FCS — NO PLAY"): AJ=""
    else:
        AJ = 3 - (1 if min_eff_games < st["B24"] else 0) - (1 if AE=="QB UNCERTAIN" else 0) \
               - (1 if AF!="" else 0) - (1 if AG!="" else 0) + (1 if min_eff_games>=6 else 0)
        AJ = max(1, min(5, AJ))
    return dict(A=A,G=G,H=H,I=I,J=J,K=K,L=L,M=M,P=P,Q=Q,R=R,S=S_,T=T,V=V,W=W,
                X=X,Y=Y,AA=AA,AE=AE,AF=AF,AG=AG,AH=AH,AI=AI,AJ=AJ)

OUT=[]; FIND=[]
def say(s): print(s); OUT.append(s)
def expect(name, got, want, sev="CRITICAL"):
    ok = got==want
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}\n        got={got!r} want={want!r}")
    if not ok: FIND.append((sev,name,f"got={got!r} want={want!r}"))

say("="*78); say("PART 4 — EDGE VALIDATION (value flow)"); say("="*78)
# Baseline: home 14.0, away 10.0, team HFA 2.5, market home -5.5
r = engine_row(home_rating=14.0, away_rating=10.0, team_hfa=2.5, mkt_home_spread=-5.5)
say(f"\n  baseline row: {json.dumps({k:v for k,v in r.items() if k in 'KLMPRTVWXAIAJ'}, default=str)}")
expect("4.1 neutral diff K = home - away = 14.0 - 10.0", r["K"], 4.0)
expect("4.2 HFA L = team-specific 2.5", r["L"], 2.5)
expect("4.3 QB adj M = 0 (all deltas blank/zero)", r["M"], 0)
expect("4.4 base margin P = K+L+M+N+O = 6.5", r["P"], 6.5)
expect("4.5 FINAL MARGIN R = P when no override", r["R"], 6.5)
expect("4.6 model spread S names the favourite correctly", r["S"], "BBB -6.5")
expect("4.7 market home spread T passes through", r["T"], -5.5)
expect("4.8 spread EDGE V = R + T = 6.5 + (-5.5) = +1.0", r["V"], 1.0)
expect("4.9 side W = HOME when edge positive", r["W"], "BBB")
expect("4.10 label = LEAN at edge 1.0 (>=B8 1, <B9 1.5)", r["X"], "LEAN")
expect("4.11 STATUS = READY", r["AI"], "READY")

say("\n  -- the sign convention worked example from START HERE --")
r2 = engine_row(home="UGA", away="XXX", home_rating=10.0, away_rating=1.0,
                team_hfa=0.0, mkt_home_spread=-7.5)
expect("4.12 model margin +9.0", r2["R"], 9.0)
expect("4.13 edge = 9.0 + (-7.5) = +1.5 -> value on HOME", r2["V"], 1.5)
expect("4.14 side = HOME (UGA)", r2["W"], "UGA")
r3 = engine_row(home="UGA", away="XXX", home_rating=6.0, away_rating=1.0,
                team_hfa=0.0, mkt_home_spread=-7.5)
expect("4.15 margin +5.0 -> edge -2.5 -> value on AWAY", r3["V"], -2.5)
expect("4.16 side = AWAY", r3["W"], "XXX")

say("\n  -- manual override --")
r4 = engine_row(mkt_home_spread=-5.5, n_margin_override=1, margin_override_value=10.0)
expect("4.17 override replaces base margin", r4["R"], 10.0)
expect("4.18 edge recomputed from override", r4["V"], 4.5)
r5 = engine_row(mkt_home_spread=-5.5, n_margin_override=2, margin_override_value=10.0)
expect("4.19 DUPLICATE override blocks the game", r5["AI"], "BLOCKED")
expect("4.20 duplicate-override reason surfaced", "DUPLICATE OVERRIDE" in r5["AH"], True)

say("\n  -- QB adjustment --")
r6 = engine_row(qb_delta_home=-3.0, mkt_home_spread=-5.5)
expect("4.21 home QB delta -3.0 lowers margin by 3", r6["P"], 3.5)
r7 = engine_row(qb_delta_away=-3.0, mkt_home_spread=-5.5)
expect("4.22 away QB delta -3.0 RAISES home margin by 3", r7["P"], 9.5)
r8 = engine_row(qb_delta_home="", qb_delta_away="", mkt_home_spread=-5.5)
expect("4.23 blank QB deltas coerce to 0 (no #VALUE!)", r8["M"], 0)

say("\n  -- home-field adjustment --")
expect("4.24 neutral site forces HFA = SETTINGS!B7 = 0",
       engine_row(neutral=1, mkt_home_spread=-5.5)["L"], 0)
expect("4.25 non-FBS home falls back to default 2.5",
       engine_row(home_type="FCS", home_rating=-20.0, mkt_home_spread=-5.5)["L"], 2.5)
expect("4.26 FBS home uses team-specific HFA",
       engine_row(team_hfa=3.5, mkt_home_spread=-5.5)["L"], 3.5)

say("\n  -- confidence --")
expect("4.27 confidence 4 with ample sample, clean flags",
       engine_row(mkt_home_spread=-5.5, min_eff_games=6)["AJ"], 4)
expect("4.28 confidence drops on small sample",
       engine_row(mkt_home_spread=-5.5, min_eff_games=2)["AJ"], 2)
expect("4.29 confidence blank when PENDING LINE",
       engine_row(mkt_home_spread="")["AJ"], "")

say("\n"+"="*78); say("PART 3 — PRODUCTION SCENARIOS"); say("="*78)
sc = [
 ("QB ruled out (home QB coded L -> UNCERTAIN)",
  dict(qb_status_home="UNCERTAIN", mkt_home_spread=-5.5), "AI", "QB UNCERTAIN"),
 ("QB questionable (same gate — workbook has no separate state)",
  dict(qb_status_home="UNCERTAIN", mkt_home_spread=-5.5), "AI", "QB UNCERTAIN"),
 ("neutral-site game", dict(neutral=1, mkt_home_spread=-5.5), "L", 0),
 ("rivalry game (no special handling; manual adj is the lever)",
  dict(manual_adj=1.5, mkt_home_spread=-5.5), "P", 8.0),
 ("FCS opponent", dict(away_type="FCS", away_rating=-25.0, mkt_home_spread=-5.5),
  "AI", "FCS — NO PLAY"),
 ("bye week (team simply absent — no row)", dict(gameid=""), "A", ""),
 ("missing market line", dict(mkt_home_spread=""), "AI", "PENDING LINE"),
 ("line movement (re-enter line -> edge recomputes)",
  dict(mkt_home_spread=-7.0), "V", -0.5),
 ("postponed game (no dedicated state; user must blank the line)",
  dict(mkt_home_spread=""), "AI", "PENDING LINE"),
 ("cancelled game (same — no dedicated state)",
  dict(mkt_home_spread=""), "AI", "PENDING LINE"),
]
for name,kw,key,want in sc:
    got=engine_row(**kw)[key]
    expect(f"3.x {name}  [{key}]", got, want)

say("\n"+"="*78); say("PART 5 — STRESS / GRACEFUL FAILURE"); say("="*78)
st = [
 ("blank inputs (no gameid)", dict(gameid=""), "A", ""),
 ("duplicate GameID", dict(dup_gameid=2, mkt_home_spread=-5.5), "AI", "BLOCKED"),
 ("missing team (unmatched abbrev -> BLOCK)",
  dict(home_type="BLOCK", mkt_home_spread=-5.5), "AI", "BLOCKED"),
 ("misspelled team -> rating missing",
  dict(home_rating=None, mkt_home_spread=-5.5), "AI", "BLOCKED"),
 ("invalid favourite in MARKET LINES", dict(invalid_favorite=True, mkt_home_spread=-5.5),
  "AI", "BLOCKED"),
 ("duplicate market row", dict(dup_market_row=1, mkt_home_spread=-5.5), "AI", "BLOCKED"),
 ("invalid date (blank)", dict(date="", mkt_home_spread=-5.5), "AI", "DATA INCOMPLETE"),
 ("blank week", dict(week="", mkt_home_spread=-5.5), "AI", "DATA INCOMPLETE"),
 ("negative spread value accepted as a number",
  dict(mkt_home_spread=3.5), "V", 3.0),
 ("extremely large spread (+/-500)", dict(mkt_home_spread=-500.0), "V", -493.5),
 ("extreme ratings do not crash", dict(home_rating=1e6, away_rating=-1e6,
  mkt_home_spread=-5.5), "R", 2000002.5),
]
for name,kw,key,want in st:
    got=engine_row(**kw)[key]
    expect(f"5.x {name}  [{key}]", got, want, sev="MAJOR")

say("\n  -- precedence ordering proof --")
r=engine_row(dup_gameid=2, away_type="FCS", away_rating=-20.0, mkt_home_spread="",
             qb_status_home="UNCERTAIN")
expect("5.12 BLOCKED outranks everything", r["AI"], "BLOCKED")
r=engine_row(away_type="FCS", away_rating=-20.0, mkt_home_spread="", qb_status_home="UNCERTAIN")
expect("5.13 FCS outranks PENDING LINE and QB UNCERTAIN", r["AI"], "FCS — NO PLAY")
r=engine_row(mkt_home_spread="", qb_status_home="UNCERTAIN")
expect("5.14 PENDING LINE outranks QB UNCERTAIN", r["AI"], "PENDING LINE")

say("\n  -- shipped-SETTINGS gaps --")
r=engine_row(mkt_home_spread=-5.5, mkt_total=48.5)
expect("5.15 model TOTAL is inert because SETTINGS!B22/B23 are blank", r["Y"], "")
expect("5.16 total edge therefore blank", r["AA"], "")
r=engine_row(mkt_home_spread=-5.5, as_of_minus_line_days=99)
expect("5.17 STALE LINE never fires while SETTINGS!B5 (as-of date) is blank",
       r["AI"], "READY", sev="MAJOR")
S2=dict(S); S2["B5"]="2026-09-10"
r=engine_row(mkt_home_spread=-5.5, as_of_minus_line_days=99, settings=S2)
expect("5.18 STALE LINE fires once B5 is set", r["AI"], "STALE LINE")
r=engine_row(mkt_home_spread=-9.9)
expect("5.19 BET label suppressed while BET toggle = N", r["X"], "INVESTIGATE")
S3=dict(S); S3["B11"]="Y"
r=engine_row(mkt_home_spread=-9.9, settings=S3, min_eff_games=6)
expect("5.20 BET label appears when toggle=Y, READY and edge>=3", r["X"], "BET")

say("\n"+"#"*78)
say(f"# SIMULATOR FINDINGS: {len(FIND)}")
for a,b,c in FIND: say(f"#  [{a}] {b} :: {c}")
say("#"*78)
open("/tmp/qa/engine_sim_log.txt","w").write("\n".join(OUT)+"\n")
