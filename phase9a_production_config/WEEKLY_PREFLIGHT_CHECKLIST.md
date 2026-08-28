# TTW ONE-MINUTE WEEKLY PREFLIGHT

**Complete every line before you enter a single market line. No exceptions.**

---

## ☐ 1. Working copy created

**File → Make a copy** → name it `TTW WORKING YYYY-MM-DD Wk N`.
**You are now working in the copy. The production master is never touched.**

---

## ☐ 2. `SETTINGS!B4` — Current Week

| | |
|---|---|
| **Value** | The week number you are about to handicap (integer: `0`, `1`, `2`…) |
| **When** | First action of the week, before anything else |
| **Who** | Owner |
| **If left blank** | `START HERE!C7` reads `— set week + as-of date`. DASHBOARD week filtering is unreliable. |
| **Verify** | `START HERE!C7` changes to **`OK — week N`** |

---

## ☐ 3. `SETTINGS!B5` — As-of Date

| | |
|---|---|
| **Value** | **Today's date**, in the sheet's date format |
| **When** | Same moment as B4 — they share one status indicator |
| **Who** | Owner |
| **If left blank** | ⚠️ **STALE LINE PROTECTION IS SILENTLY OFF.** `CALC!Q` short-circuits to 0. A line five weeks old still reads READY. `DATA QUALITY` shows `STALE LINE = 0`, which looks identical to "all lines fresh." **This is the single most dangerous blank cell in the workbook.** |
| **Verify** | `START HERE!C7` reads `OK — week N`. Re-enter B5 **every week** — last week's date makes every line look stale. |

---

## ☐ 4. Timezone — America/New_York

| | |
|---|---|
| **Value** | `America/New_York` |
| **Where** | File → Settings → Time zone |
| **When** | **Once**, on any new copy or import. Re-check after any re-import. |
| **Who** | Owner |
| **If wrong** | Every date shifts by up to a day. Kickoff dates, staleness maths and week bucketing all drift. The `.xlsx` cannot carry this setting — it is lost on every import. |
| **Verify** | Open the setting and read it. There is no in-sheet indicator. |

---

## ☐ 5. `SETTINGS!B11` — BET toggle

| | |
|---|---|
| **Value** | **`N`** unless you have consciously decided otherwise |
| **When** | Confirm weekly; change only deliberately |
| **Who** | Owner |
| **If set to `Y`** | `BET` labels appear on any READY game with edge ≥ 3.0. Nothing else changes — all other maths is identical. |
| **If left `N`** | Those games show `INVESTIGATE` instead. **Nothing is hidden or lost.** |
| **Verify** | `AUDIT` invariant reads **`BET toggle default OFF — OK (OFF)`** |

---

## ☐ 6. Structural audit — the gate

**`START HERE!C15` must read `OK — all invariants pass`.**

**If it reads `WARNING: n AUDIT INVARIANT(S) FAILING` — STOP.** Nothing above it on
the tab is trustworthy. Open `AUDIT`, find the failing invariant, resolve it before
going further.

---

## ☐ 7. Baseline sanity — five numbers

| Check | Where | Expected before you start |
|---|---|---|
| Games loaded | `DATA QUALITY` | **888** |
| BLOCKED | `DATA QUALITY` | **0** |
| QB UNCERTAIN teams | `START HERE!C11` | a number you recognise (**39** at season start) |
| Failing invariants | `AUDIT` | **0** |
| Missing lines | `START HERE!C12` | **761** before entry, falling as you work |

---

## Known-and-accepted states — do **not** treat these as faults

- **`Model total = NOT AVAILABLE`** on every game — totals are **intentionally disabled for 2026**. Permanent, by decision. Not broken.
- **`FCS — NO PLAY`** with a blank model spread — correct and permanent for all 127 FBS-vs-FCS games.
- **`INVESTIGATE` where you expected `BET`** — that is the BET toggle at `N`, working as designed.

---

## ⛔ ABORT — do not place a bet if any of these is true

- `START HERE!C15` shows **AUDIT FAILING**
- `SETTINGS!B5` is **blank** — you have no staleness protection
- Games loaded ≠ **888**, or teams ≠ **138**
- Any unexpected **BLOCKED** game
- A rating moved **more than 2.5 points** in one week
- You are typing into the **production master** rather than a dated working copy
