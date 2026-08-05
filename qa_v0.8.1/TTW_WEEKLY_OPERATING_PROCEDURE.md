# TTW WEEKLY OPERATING PROCEDURE

**The permanent weekly checklist.** Workbook: TTW College Football Power Ratings
v0.8.1 AUTHORITATIVE. Derived from the workbook's own `START HERE` steps 1–8 and
verified against the live formula chain.

**Target: 25–40 minutes.** Times below are estimates from the structure of each
step (number of manual inputs, number of rows touched), not stopwatch
measurements — I could not drive the live UI.

---

## ONE-TIME SETUP (before Week 0 — do this once, ever)

| # | Action | Where | Why it matters |
|---|---|---|---|
| S1 | Set **Time zone = America/New_York** | Sheets: File → Settings | The `.xlsx` cannot carry this. Wrong TZ shifts every date by a day. |
| S2 | Enter **Season = 2026** | `SETTINGS!B3` | Already set. Verify it survived import. |
| S3 | Decide on **totals** | `SETTINGS!B22`, `B23` | **Both ship blank, so the entire totals pipeline returns blank forever.** Either populate them or accept that model total / total edge / total label / team totals stay empty all season. This is not a malfunction — see QA Major #1. |
| S4 | Leave **BET toggle = "N"** | `SETTINGS!B11` | Suppresses BET labels until you deliberately enable them. Everything still computes; you just see INVESTIGATE instead of BET. |
| S5 | Save a **known-good copy** | — | There is no cell protection anywhere in the workbook. This copy is your only way to detect an accidental paste over a formula column. |

---

## THE WEEKLY RUN

### Step 1 — Set the week header · ~1 min · 2 inputs
- `SETTINGS!B4` = current week number
- `SETTINGS!B5` = as-of date (today)

**Do not skip.** While `B5` is blank, **STALE LINE can never fire** — a line five
weeks old still reads READY. Verified in testing. `START HERE!C7` shows
*"— set week + as-of date"* until both are filled; that is your only warning.

### Step 2 — Import the schedule · ~2 min · 1 paste
- Pull the CFBD schedule file (recipe in `DICTIONARY`)
- Paste the **whole file** into `IMPORT SCHEDULE` at **A6**

Check `START HERE!C10` → should read *"N games loaded"*.
For 2026 the schedule is **already loaded (888 games)**; you only re-paste if it changes.

### Step 3 — Import season-to-date stats · ~2 min · 1 paste
- Paste the CFBD stats file into `IMPORT STATS` at **A6** (replaces old)

Check `START HERE!C9`. In preseason it reads *"— (preseason: priors drive ratings)"* —
that is correct and expected for Week 0.

### Step 4 — Ratings update · ~0 min · automatic
Ratings recompute from `IMPORT STATS` + `PRESEASON` priors. **No manual action.**
Weekly movement is capped at `SETTINGS!B12` = 2.5 pts.

### Step 5 — Confirm QB information · **~5–10 min · the real bottleneck**
- Open `QB VALUES`. Work only rows flagged UNCERTAIN.
- Check `START HERE!C11` → *"N teams QB UNCERTAIN"*.

**As shipped: 39 teams UNCERTAIN** (33 L-coded competitions + 6 M-coded with blank
values). Each needs: active starter, delta, confidence code, `Reviewed for season` =
2026, fresh date.

**This is the step that will consume your time and the step most likely to be
skipped.** A team left UNCERTAIN gates its games out of your card entirely.

### Step 6 — Enter market lines · **~10–15 min · the biggest input load**
- `MARKET LINES`: one row per game — **Favorite + POSITIVE spread + total + date**

**Sign convention (this trips everyone once):**
> Georgia -7.5 at home → enter Favorite = `UGA`, Spread = `7.5`
> The sheet stores market home spread = **-7.5**

**Team codes:** bare `Miami` is rejected. Use `MIA` (ACC) or `M-OH` (Miami OH).
Schedule imports resolve automatically; manual entry does not.

Check `START HERE!C12` → *"Missing: N lines"*.

### Step 7 — Log injuries and situational spots · ~2–5 min · variable
- `ADJUSTMENTS`: **reason is required**. Undated/unexpired rows are flagged.
- Use `MARGIN OVERRIDE` sparingly — it **replaces** the model margin entirely.
- **Never enter two MARGIN OVERRIDEs for the same GameID** — that BLOCKS the game.

Check `START HERE!C13`.

### Step 8 — Clear DATA QUALITY, then work the DASHBOARD · ~5–10 min
- `START HERE!C15` (structural audit) **must** read *"OK — all invariants pass"* before you trust anything above it.
- `START HERE!C14` → resolve anything BLOCKED.
- Then `DASHBOARD`, sorted by Priority.

### Step 9 — Finalize the card
Read `ENGINE!AI` (STATUS) and `ENGINE!X` (Spread label).

**Only `READY` games can carry a bet label.** Status precedence, verified in testing:

```
BLOCKED  >  FCS — NO PLAY  >  PENDING LINE  >  STALE LINE
         >  QB UNCERTAIN   >  TRANSITION UNCERTAIN
         >  DATA INCOMPLETE  >  READY
```

Labels: `LEAN` ≥ 1.0 · `INVESTIGATE` ≥ 1.5 · `BET` ≥ 3.0 **and** toggle = Y **and** status = READY.

Confidence (`ENGINE!AJ`) runs 1–5: starts at 3, **−1** each for small sample /
QB uncertain / transitional / FCS, **+1** if ≥ 6 effective games.

---

## BOTTLENECKS (ranked)

1. **Market line entry (Step 6)** — the single largest manual load. Every game, hand-typed, with a sign convention that inverts. Highest error risk in the whole workflow.
2. **QB confirmation (Step 5)** — 39 open records at season start. Front-loaded; shrinks as depth charts settle.
3. **Adjustments (Step 7)** — unbounded; depends how much you log.

Steps 1–4 and 8–9 are fast. **Roughly 70% of your weekly time is Steps 5 and 6.**

---

## WEEKLY ABORT CONDITIONS

Stop and fix before betting anything if:

- `START HERE!C15` shows **AUDIT FAILING** — nothing above it is trustworthy
- Any game shows `BLOCKED` you did not expect
- A rating moved more than 2.5 pts in one week (the cap should prevent this)
- `START HERE!C11` shows more UNCERTAIN teams than last week without a roster reason
- Formula count is no longer **123,011**, or the sheet count is no longer **21**
