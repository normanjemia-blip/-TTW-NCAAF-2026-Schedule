# QB Research Continuation — v0.5.1 (2026-07-20)

## What changed from the earlier ESPN-API-only check

The v0.5 QB check re-tested ESPN's structured depth-chart/roster
endpoints only (both empty/unusable). This pass went further: genuine
web research across reputable outlets (ESPN, CBS Sports, Bleacher
Report, On3, 247Sports, etc.) for actual 2026 starter reporting, not
just API availability.

## Finding 1: fall camp hasn't started - most coverage is explicitly
   speculative, by its own framing

Fall camps open late July/early August 2026 (confirmed via team-specific
camp-schedule articles). The bulk of current media content is titled
"**Predicting** starting QBs for every Power 4 team," "**Projecting**
Every SEC Starting Quarterback," "**Ranking** all 138 FBS quarterback
situations" - i.e., explicitly framed as projection/opinion, not
reporting a confirmed decision. That framing itself is evidence these
are not yet "supportable" sources for a loaded value.

## Finding 2: a smaller set of programs have a genuinely low-ambiguity
   case (multi-year returning starter, no reported competition)

For reference only (**not loaded into QB VALUES** - see Finding 3),
found via multiple independent reputable outlets:

| Team | Reported QB1 | Basis |
|---|---|---|
| Ohio State | Julian Sayin | Returning 2025 starter, "gives the Buckeyes a QB to build around" |
| Oregon | Dante Moore | Turned down 2026 NFL Draft entry to return; framed as clear #1 |
| Notre Dame | CJ Carr | Won the job in 2025, coach on record praising him entering 2026 |
| Arizona | Noah Fifita | Multi-year returning starter, described as "established" |
| SMU | Kevin Jennings | Entering 3rd year as starter, statistical track record cited |
| Penn State | Rocco Becht | Transferred with HC Matt Campbell from Iowa State, "rare 4-year starter" |
| Ole Miss | Trinidad Chambliss | Returning 2025 SEC passing leader, extra year of eligibility confirmed by court ruling |
| Georgia | Gunner Stockton | "Returns after a solid first season as starter" |
| Texas | Arch Manning | Returning 2025 starter, no reported competition |

Several teams were explicitly reported as **genuinely open competitions**
(correctly stay UNCERTAIN, not just "unresearched"): Alabama (Austin Mack
vs. Keelon Russell), Florida (Aaron Philo vs. Tramell Jones Jr.), and
others. Georgia Tech's reporting used hedge language ("more or less been
named") - not treated as confirmed.

## Finding 3: none of this can be loaded into QB VALUES yet - a deeper,
   separate blocker than starter identification

Even for the ~9 low-ambiguity cases above, **QB VALUES requires all six
fields together** (starter, baseline comparison, adjustment value,
confidence, review date, source) to load a team. Knowing *who* is
starting only supports field 1. Fields 2-3 (**baseline value** and
**adjustment value** - a numeric points quantification of QB quality) have
**no approved, verified source or methodology** anywhere in the project's
architecture docs. This is a distinct, more fundamental gap than API
availability, first flagged in the Phase 4 research and still unresolved.

**This was not invented or filled in unilaterally.** Per the lesson from
this same session's FCS-rating episode (a self-built rating methodology
was constructed without asking first, and the user's next instruction
removed it from scope) - a numeric QB-value system is a materially larger
methodology decision than sourcing, and is not something to build without
the user's direction on approach. Plausible paths, **none chosen here**:
a named external QB-grading source (e.g., PFF grades, if accessible/
licensed), a returning-production/experience-based proxy the user
pre-approves, or continuing to defer QB entirely until closer to the
season when depth charts and more concrete reporting exist.

## Result

**QB VALUES is unchanged: 0 of 138 teams loaded, all UNCERTAIN** - same
state as v0.4.2/v0.5. The unresolved-QB report from v0.5
(`unresolved_qb_report.tsv`) still applies; this file supplements it with
the starter-identification research above, kept separate from the
workbook pending a methodology decision on quantification.
