# MASTER AND WORKING-COPY POLICY

**Permanent. Applies every week of every season.**

---

## The three tiers

| Tier | Artifact | Role | Ever edited? |
|---|---|---|:--:|
| **1 — ARCHIVE** | **current:** `TTW_College_Football_Power_Ratings_v0.8.8_AUTHORITATIVE.xlsx` · SHA-256 `b2a920fe…6450`<br>**frozen:** `…v0.8.7…` · `46671dee…15cd`<br>**frozen:** `…v0.8.6…` · `bb76901a…67f9`<br>**frozen:** `…v0.8.5…` · `0676aa1a…67be`<br>**frozen:** `…v0.8.4…` · `ed5d3b3d…a892`<br>**frozen:** `…v0.8.3…` · `ff557825…96b8`<br>**frozen:** `…v0.8.2…` · `22508544…90d0`<br>**frozen predecessor:** `…v0.8.1_AUTHORITATIVE.xlsx` · SHA-256 `e2da9a4c…cdfd6` | Immutable reference of record | **Never** |
| **2 — PRODUCTION MASTER** | Google Sheet `1w2cATBNYFtFXU32xw8_3btbFAtaqhdSx5HQxiFPnWmA` | The clean template every week is copied from | **Only for approved structural changes** |
| **3 — WORKING COPY** | `TTW WORKING YYYY-MM-DD Wk N` | Where all live data goes | **Every week** |

---

## 1. The `.xlsx` archive is untouched, permanently

Its SHA-256 is recorded in `PROJECT_MANIFEST.json` and in the promotion and
maintenance certificates. It is the only artifact that can prove what v0.8.1
actually contained. **Never open it to edit, never re-save it** — even opening and
saving in Excel rewrites bytes and breaks the hash.

If you need to inspect it, work on a copy.

---

## 2. The Google Sheet becomes the production master only after import verification

**Import verification: COMPLETE** (Phase 9A Part 6). 21 sheets · 888 games ·
138 teams · 65 H / 40 M / 33 L · 39 UNCERTAIN · 0 market lines · BET toggle N ·
**0 formula errors** · **0 failing audit invariants** · Week 0 and Week 1 spreads
computing correctly.

**Two conditions remain before it is formally the master:**

1. **Rename it** — drop the trailing ` 4` from `…AUTHORITATIVE 4`, and confirm no ` 1` / ` 2` / ` 3` siblings survive in Drive to be confused with it.
2. **Set the timezone** to America/New_York. The `.xlsx` cannot carry it; it is lost on every import.

Protection (Deliverable 3) is strongly recommended but not a blocker — the weekly
working copy already limits blast radius.

---

## 3. Create a dated working copy before entering live data

**Every week, first action:**

> File → Make a copy → `TTW WORKING 2026-09-01 Wk1`

**Everything happens in the copy:** market lines, adjustments, QB updates, stats
pastes, the betting card.

**Why this is the most important rule here.** The workbook has no cell protection
today and stores no cached formula results, so a mis-aimed paste over a formula
column is **silent** — nothing looks stale, nothing errors, a number is just wrong.
The working copy means the worst case is losing one week's inputs, not the model.

**Keep every weekly copy.** They are your audit trail — what you knew, and when.

---

## 4. Never experiment in the production master

Testing a new adjustment type, a threshold change, a "what if the line moved"
scenario, or anything else — **do it in a working copy, or a copy of a copy.**

The master exists to be *copied*, not used. If you find yourself typing into it,
stop.

**The only legitimate reasons to edit the master:**
- Applying the protection map (one time)
- Setting the timezone (one time)
- An approved structural change that has been through a promotion audit

Anything else is a working-copy activity.

---

## 5. Rollback procedure

### Level 1 — a bad week (most common)
**Delete the working copy and make a fresh one from the master.** Costs one week of
inputs. Nothing else is affected. Never hesitate over this.

### Level 2 — the production master is damaged
1. Confirm the archive is intact: current v0.8.8 SHA-256 must be `b2a920feddc0f49f0647957334db0ecd0e922fe6a3933fc6a11af31587b56450`; the frozen v0.8.7 predecessor must remain `46671deeaaa94d98c63cb32d0e94af9907e76e7e2638de431b918987df2e15cd`; the frozen v0.8.6 predecessor must remain `bb76901a96a3fa63e14f0cc582891de82846c12fa5f7ce41d182c8addab967f9`; the frozen v0.8.5 predecessor must remain `0676aa1a05d661ca0d99c917c8dc471c0030128cc42ea8fd1bd2f17dcea767be`; the frozen v0.8.4 predecessor must remain `ed5d3b3d9aa3dd4f845e91688216a28276aaa0b3e4bd68ba09a9ceb96a8adaff`; the frozen v0.8.3 predecessor must remain `ff55782586ef1adb662eba59710e824dc382769a24579e48917b101fbcdd96b8`; the frozen v0.8.2 predecessor must remain `225085449b5a1db5903a3998cb909be1f7ae0037782ea65d412bcb4d9d9490d0`; the frozen v0.8.1 predecessor must remain `e2da9a4c28bd5c0f094ab06a2a85d3e31b37c2aba894f97f3415e15f799cdfd6`
2. Try **File → Version history → See version history** first, and restore the last good version — faster and cleaner than re-importing
3. If version history cannot recover it, re-import the `.xlsx`, then **re-run Phase 9A Part 6 verification** before use
4. Re-apply timezone and protection

### Level 3 — the model itself is wrong
Roll back to **v0.6.2** (SHA `bbb17b50…a838efd`) per `promotion_v0.8.0/ROLLBACK.md`.
**Cost:** v0.6.2 has an empty QB dataset — 0/138 confidence codes, every team
UNCERTAIN. Ratings and spreads are identical, so you lose the QB verification layer,
not any computed output.

### Do NOT roll back for
A stale QB record · an unexpected `PENDING LINE` · `Model total = NOT AVAILABLE`
(intentional) · `INVESTIGATE` where you expected `BET` (that is the toggle).
These are weekly-maintenance items, not failures.

---

## Weekly file hygiene

- **Name format:** `TTW WORKING YYYY-MM-DD Wk N` — sorts chronologically
- **Never** name a working copy anything containing `AUTHORITATIVE` or `MASTER`
- Before entering lines, confirm the title bar shows **WORKING**, not the master
- Archive finished weeks into a `TTW 2026 Season` folder; keep the master outside it
