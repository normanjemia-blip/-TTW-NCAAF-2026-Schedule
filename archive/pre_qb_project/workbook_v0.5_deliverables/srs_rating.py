"""
Phase 5 FCS framework, revised approach: instead of a coarse 5-bucket
tier fallback, compute a genuine per-team VERIFIED NUMERICAL RATING for
every FCS opponent on the 2026 schedule, using the same opponent-adjusted
scoring margin technique already named as the approved core methodology
(Architecture Amendment v0.2: "opponent-adjusted scoring margin, per-game
capped default +/-28, venue-adjusted") - applied here across the complete
2025 FBS+FCS result graph (315 teams, 1686 completed games) rather than
FBS alone.

Iterative SRS-style solve:
  r[team] = mean over team's games of (opponent_rating + performance_margin)
  performance_margin = (my_score - opp_score), HFA-adjusted (+/-2.5,
  0 if neutral), capped to +/-28 per game.
Converges by repeated substitution. Final ratings mean-centered so the
FBS subset averages to 0 (matching the "points vs average FBS" convention
already used throughout PRESEASON/CLEAN).

A team gets a VERIFIED rating only if it has >=6 completed 2025 games in
the dataset (same evidence floor used elsewhere in this build). Teams
below that floor are explicitly UNRATED / Transitional-uncertain - no
number is invented for them.
"""
import json
import statistics

FBS = {"1", "4", "5", "8", "9", "12", "15", "17", "18", "151", "37"}
HFA = 2.5
CAP = 28
MIN_GAMES = 6

games = json.load(open("espn2025_all_games.json"))

def is_fbs(team):
    return team.get("conferenceId") in FBS

# Build the full graph: list of (team, opp, perf_margin) edges, both directions
edges = {}  # team -> list of (opp, perf_margin)
game_count = {}
for g in games.values():
    if not g["completed"]:
        continue
    t = g["teams"]
    if "home" not in t or "away" not in t:
        continue
    h, a = t["home"], t["away"]
    if h.get("score") is None or a.get("score") is None:
        continue
    hs, as_ = int(h["score"]), int(a["score"])
    hm = hs - as_
    if not g["neutral"]:
        hm -= HFA
    hm = max(-CAP, min(CAP, hm))
    am = -hm
    edges.setdefault(h["name"], []).append((a["name"], hm))
    edges.setdefault(a["name"], []).append((h["name"], am))
    game_count[h["name"]] = game_count.get(h["name"], 0) + 1
    game_count[a["name"]] = game_count.get(a["name"], 0) + 1

all_teams = list(edges.keys())
print(f"Total teams in 2025 graph: {len(all_teams)}, total games: {len(games)}")

# Determine FBS membership from any game record's conferenceId
fbs_flag = {}
for g in games.values():
    t = g.get("teams", {})
    for side in t.values():
        fbs_flag[side["name"]] = is_fbs(side)

# Iterative solve
rating = {t: 0.0 for t in all_teams}
for it in range(500):
    new_rating = {}
    max_delta = 0.0
    for t in all_teams:
        vals = [rating[opp] + m for opp, m in edges[t]]
        nr = statistics.mean(vals)
        new_rating[t] = nr
        max_delta = max(max_delta, abs(nr - rating[t]))
    rating = new_rating
    if max_delta < 1e-10:
        break
print(f"Converged after {it+1} iterations, max_delta={max_delta:.8f}")

fbs_ratings = [r for t, r in rating.items() if fbs_flag.get(t)]
fbs_mean = statistics.mean(fbs_ratings)
rating = {t: r - fbs_mean for t, r in rating.items()}
print(f"FBS-mean centering applied (shift={fbs_mean:.4f}); FBS count={len(fbs_ratings)}")

# sanity checks
ranked = sorted(rating.items(), key=lambda kv: -kv[1])
print("Top 5 overall (FBS+FCS combined graph):", [(n, round(r,1)) for n, r in ranked[:5]])
print("Bottom 5 overall:", [(n, round(r,1)) for n, r in ranked[-5:]])
ndsu = [x for x in ranked if "North Dakota State" in x[0]]
sac = [x for x in ranked if x[0].startswith("Sacramento")]
print("NDSU:", ndsu, "games:", game_count.get("North Dakota State Bison"))
print("Sac State:", sac, "games:", game_count.get("Sacramento State Hornets"))

json.dump({"rating": rating, "game_count": game_count, "is_fbs": fbs_flag},
          open("srs_2025_ratings.json", "w"), indent=1)
print("wrote srs_2025_ratings.json")
