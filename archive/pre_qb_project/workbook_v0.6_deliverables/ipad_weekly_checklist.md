# TTW Weekly Checklist (iPad-friendly)

Grounded in the workbook's own built-in 8-step routine
(`START HERE!A6:C15`, live status column already does the checking for
you — this is that same routine, reformatted for a phone/tablet screen).
Target time: 25–40 minutes. **You only ever touch yellow cells.** Every
step below stays on the 10 sheets you already know; nothing here requires
opening ENGINE, CLEAN, CALC, TEAM MAP, PRESEASON, FCS TIERS, HISTORY,
BACKTEST, AUDIT, DICTIONARY, or CHANGELOG.

---

### ☐ 1. SETTINGS — set the week
Open **SETTINGS**, tab down to:
- `B4` Current week → type this week's number
- `B5` As-of date → type today's date

*(`START HERE!C7` flips to "OK — week N" when both are filled.)*

### ☐ 2. Get your files
Pull the CFBD stats file and confirm the schedule is current (recipes on
the DICTIONARY tab — one-time reference, not a weekly edit).

### ☐ 3. IMPORT STATS — paste stats
Open **IMPORT STATS**, tap cell `A6`, paste the whole stats file (it
replaces last week's). Don't touch column K — it fills itself in and
tells you if a team name didn't match (see step 8).

### ☐ 4. IMPORT SCHEDULE — paste schedule (only if it changed)
Same idea, cell `A6`. Most weeks you skip this — the season schedule is
already loaded.

### ☐ 5. QB VALUES — confirm starters
Open **QB VALUES**. For any team you're about to bet on, check its row:
- `C` Baseline QB, `D` Baseline value
- `E` Active QB, `F` Active value
- `H` Confidence (H/M/L)
- `J` Reviewed for season (must equal the current season)
Leave a team's row blank if you're not sure — it correctly shows
UNCERTAIN and the model will not price that team's QB. Don't guess.

### ☐ 6. MARKET LINES — enter lines
Open **MARKET LINES**, one row per game:
- `A` GameID (copy from DASHBOARD)
- `C` Favorite → the **team abbreviation**, e.g. `UGA` (never a bare
  nickname like "Georgia" — and never "Miami" alone, use `MIA` or
  `M-OH`)
- `D` Spread → always **positive**, even for a home underdog favorite
- `E` Total
- `F` Source, `G` Line date
Column `Q` flags problems automatically (missing pieces, stale line,
invalid favorite) — if it's not blank, fix that row before trusting it.

### ☐ 7. ADJUSTMENTS — log anything unusual
Open **ADJUSTMENTS** only if something specific happened (injury, travel
spot, weather). One row per adjustment:
- `A` Type, `B` Target (abbrev or GameID), `C` Value (points), `D` Reason
  (**required** — leave nothing here blank), `H` Active = `Y`
Keep single adjustments **small** (a few points) — the sheet will flag
anything over 4 points as large, but it does **not stop it from being
applied**, so don't rely on the flag as a safety net; review anything
large yourself before trusting the game.

### ☐ 8. DATA QUALITY → DASHBOARD
Open **DATA QUALITY** first — every count should read 0 except the ones
that are expected to be nonzero this early (FCS — NO PLAY games, teams
still QB UNCERTAIN). Then open **DASHBOARD** and work games in Priority
order (highest first). A game's `Status` column tells you exactly what's
blocking it, in this order — the first one that applies is the one
you'll see:

```
BLOCKED  →  FCS — NO PLAY  →  PENDING LINE  →  STALE LINE  →
QB UNCERTAIN  →  TRANSITION UNCERTAIN  →  DATA INCOMPLETE  →  READY
```

Only **READY** games get a spread/total label. FCS — NO PLAY games never
get one, no matter what — that's permanent, not something a line entry
can fix.

### ☐ A. Structural check (always look at this)
Still on **DATA QUALITY** — if the AUDIT-invariant line says anything
other than "OK", stop and don't trust any status above until that clears.

---

**Sign convention reminder:** Georgia –7.5 at home → Favorite=`UGA`,
Spread=`7.5` (positive). The sheet stores it internally as –7.5 and
handles the math from there — you never type a negative spread.

**Never type into a plain (white) cell.** If a formula cell looks wrong,
that's a "stop and report it" situation, not a "fix it yourself" one.
