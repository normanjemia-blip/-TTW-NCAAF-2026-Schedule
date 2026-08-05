# v0.5.1 — FBS-vs-FCS Scope-Change: Formula Change Design

Base: approved `v0.4.2` (not v0.5 — v0.5's FCS-rating work is superseded
by this scope change and is not carried forward). Full trace of the
existing v0.4.2 formula chain, done before any edit, to find the minimal
set of formula changes needed.

## Finding: most of the required behavior already cascades for free

Once FCS TIERS' rating data (named overrides + tier values) is emptied,
these already produce the right output with **no formula edit**, because
of guard clauses already in the existing (approved) formula chain:

| Requirement | Why it already works |
|---|---|
| No spread calculated | `ENGINE!S` requires `R` (final margin) non-blank; `R` requires `K` (I/J ratings diff) non-blank; `I`/`J` pull FCS-side rating from `CLEAN!R`/`S`, which will be blank once FCS TIERS is empty |
| No total calculated | `ENGINE!Y` already requires **both** sides `="FBS"` — always did, unrelated to this change |
| No edges/team-totals | All derive from `R`/`Y`, both blank as above |
| No spread/total **label** | `ENGINE!X`/`AB` both start `IF($V6="","",...)` / `IF($AA6="","",...)` — already blank since edges are blank |
| Excluded from missing-line counts | `DATA QUALITY!B8` counts `ENGINE!AI="PENDING LINE"` — once AI short-circuits FCS games to a new status (below), they never reach the PENDING LINE check regardless of market-line presence |
| Excluded from DASHBOARD actionable ranking | `DASHBOARD!V` (Priority) is 0 unless `ENGINE!AI="READY"`; FCS games will never be READY |
| Excluded from weekly rating movement | `CALC!D` (adj_margin) = `perf_w_sum/w_sum`, both `SUMIFS` over `CLEAN!X/Y/Z/AA`, all four gated on `ISNUMBER(CLEAN!U or V)`, which requires `CLEAN!R/S` (FCS anchor) to be numeric — blank once FCS TIERS is empty |

## Finding: 4 formula patterns DO need to change

1. **`ENGINE!AI` (STATUS)** — needs a new, explicit, permanent
   `"FCS — NO PLAY"` branch. Without it, an FCS game with a blank FCS
   rating currently falls into the existing `"FCS/TRANSITION UNCERTAIN"`
   status (implies *temporarily* uncertain, resolvable) — not the
   *permanently* non-actionable label the user wants. Placed after
   `BLOCKED` (a genuine schedule data-integrity problem should still
   surface) and before every line/QB/transitional check (none of which
   should apply to a permanently non-actionable game).
2. **`ENGINE!AJ` (Confidence)** — must add `"FCS — NO PLAY"` to the
   blank-output guard list; without this it would compute and display a
   numeric confidence score for a game the model no longer opines on.
3. **`CLEAN!AB` (eg_home)** and **4. `CLEAN!AC` (eg_away)** — currently
   give an FCS opponent **partial** (0.5, `SETTINGS!B21`) effective-game
   credit. The user wants FCS results **excluded** from effective-game
   calculations, not partially counted — so the FCS branch is removed;
   an FCS-opponent game now contributes exactly 0, the same as a bye.

No other cell's formula is touched. `SETTINGS!B21` (FCS-opponent
effective-game weight) becomes an orphaned, unused constant — left in
place (not deleted) but its comment is updated to say so, since deleting
a named settings constant is a bigger, unnecessary change.

## Exact before/after text

### ENGINE!AI (STATUS) — pattern (row-relative refs shown for row 6)
Before:
```
=IF($A6="","",IF($AH6<>"","BLOCKED",IF(CALC!$S6=1,"PENDING LINE",IF(CALC!$Q6=1,"STALE LINE",IF($AE6="QB UNCERTAIN","QB UNCERTAIN",IF(OR($AF6<>"",AND($G6="FCS",$I6=""),AND($H6="FCS",$J6="")),"FCS/TRANSITION UNCERTAIN",IF(OR($B6="",$C6=""),"DATA INCOMPLETE","READY")))))))
```
After:
```
=IF($A6="","",IF($AH6<>"","BLOCKED",IF($AG6<>"","FCS — NO PLAY",IF(CALC!$S6=1,"PENDING LINE",IF(CALC!$Q6=1,"STALE LINE",IF($AE6="QB UNCERTAIN","QB UNCERTAIN",IF($AF6<>"","FCS/TRANSITION UNCERTAIN",IF(OR($B6="",$C6=""),"DATA INCOMPLETE","READY"))))))))
```
(Reuses the existing `$AG` "FCS flag" column, already `="FCS OPP"` for
any game with either side `="FCS"` — same trigger DASHBOARD's own FCS
column already uses, so no new classification logic is introduced. The
old FCS-specific sub-condition inside the transitional branch,
`AND($G6="FCS",$I6="")`/`AND($H6="FCS",$J6="")`, is now unreachable dead
code, since any such game is intercepted by the new branch first — removed
for clarity, changing nothing observable.)

### ENGINE!AJ (Confidence) — pattern
Before:
```
=IF(OR($AI6="",$AI6="BLOCKED",$AI6="PENDING LINE"),"",MAX(1,MIN(5,3-IF(CALC!$Z6<SETTINGS!$B$24,1,0)-IF($AE6="QB UNCERTAIN",1,0)-IF($AF6<>"",1,0)-IF($AG6<>"",1,0)+IF(CALC!$Z6>=6,1,0))))
```
After:
```
=IF(OR($AI6="",$AI6="BLOCKED",$AI6="PENDING LINE",$AI6="FCS — NO PLAY"),"",MAX(1,MIN(5,3-IF(CALC!$Z6<SETTINGS!$B$24,1,0)-IF($AE6="QB UNCERTAIN",1,0)-IF($AF6<>"",1,0)-IF($AG6<>"",1,0)+IF(CALC!$Z6>=6,1,0))))
```

### CLEAN!AB (eg_home) — pattern
Before: `=IF($A6="",0,$L6*IF($O6="FCS",SETTINGS!$B$21,IF($O6="FBS",1,0)))`
After:  `=IF($A6="",0,$L6*IF($O6="FBS",1,0))`

### CLEAN!AC (eg_away) — pattern
Before: `=IF($A6="",0,$L6*IF($Q6="FCS",SETTINGS!$B$21,IF($Q6="FBS",1,0)))`
After:  `=IF($A6="",0,$L6*IF($Q6="FBS",1,0))`

All four patterns are applied identically across every row 6:1005 in
their respective sheet (with each row's own row-relative references),
1000 rows x 4 columns = 4,000 formula cells changed.

## NDSU / Sacramento State — unaffected

Both remain `FBS-RECLASSIFYING` (not `FCS`) in `TEAM MAP!D`. `ENGINE!G`/`H`
(away/home type) resolve them to `"FBS"` via the alias table, exactly as
before — they never touch the `$AG6<>""` ("FCS flag") branch at all. Their
games stay fully in scope, under the existing (untouched) transitional
safeguard chain validated in the (superseded) v0.5 build.
