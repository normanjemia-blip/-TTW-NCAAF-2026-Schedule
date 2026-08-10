<!-- GENERATED FILE — do not hand-edit.
     Rebuild:  python3 _tools/build_futures.py
     Source:   2026 VSiN College Football Betting Guide -->

# Source Conflict Audit — futures

> **Source class: GUIDE CONTENT.** Every price, pick, prediction and contributor name below is printed in the 2026 VSiN College Football Betting Guide. TTW reference notes paraphrase each argument; the judgement is the contributor's. No outside research, no post-publication updates.

> **Nothing here is corrected.** Every figure, label and name is reproduced as the guide prints it.

## The SUN BELT CHAMP row

Printed under a Sun Belt label but containing NFL team names. Reproduced exactly as printed and excluded from conference prediction data. Not corrected. The row is reproduced in full in [00_PREDICTIONS.md](00_PREDICTIONS.md).

| Contributor | Printed cell |
| --- | --- |
| Femi Abebefe | Falcons |
| Matt Brown | Panthers |
| Stormy Buonantony | Bucs |
| Adam Burke | Panthers |
| Zachary Cohen | Falcons |
| Sean Green | Saints |
| Paul Howard | Saints |
| Ryan Kramer | Saints |
| Jensen Lewis | James Madison |
| Steve Makinen | Bucs |
| John McKechnie | Saints |
| Patrick Meagher | Panthers |
| Mitch Moss | Saints |
| Tim Murray | Saints |
| Wes Reynolds | Panthers |
| Scott Seidenberg | Falcons |
| Tyler Shoemaker | Falcons |
| Paul Stone | Bucs |
| Dustin Swedelson | Bucs |
| Dave Tuley | Bucs |
| Matt Youmans | Falcons |
| Jonathan Von Tobel | Saints |

Note that the guide separately prints a **SUN BELT CHAMPION** row containing college teams. Both rows are kept.

## Contributor names printed inconsistently

| Where | As printed | Elsewhere |
| --- | --- | --- |
| p. 39 Heisman byline | Zach Cohen | Zachary Cohen (p. 4 grid, p. 8 best bets) |
| p. 7 best bets | Pauly Howard | Paul Howard (p. 4 grid) |

Both pairs are almost certainly the same person, but the library records what each page prints and does not merge two printed names into one identity.

## A price printed without its closing bracket

Dave Ross's second leg on p. 5 is printed as `ALT OVER 7.5 WINS (+120` — the bracket does not close in the guide. Reproduced as printed.

## A conference price with no market

2 teams — Connecticut Huskies, Notre Dame Fighting Irish — carry the conference row's label with **no price at all**. Both are Independents, which have no conference title to win. Recorded as an absence rather than filled in.

## A conference price typeset with a Unicode minus

Texas Tech's Big 12 price is typeset with U+2212 MINUS SIGN rather than an ASCII hyphen. The printed number is the same; the extractor normalises it so the price is not silently dropped.

## Two rosters, not one

- On p. 4 only (6): Femi Abebefe, Matt Brown, Patrick Meagher, Paul Howard, Ryan Kramer, Scott Seidenberg
- In best bets only (4): Aaron Moore, Ben Stevens, Dave Ross, Pauly Howard

The two features were assembled from different groups. Neither roster is treated as the canonical staff list.

## Cross-links

- [Contributor disagreement](00_DISAGREEMENT.md) · [Phase 7 conflicts](../06_Win_Totals/00_SOURCE_CONFLICTS.md)
