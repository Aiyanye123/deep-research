# Depth Profiles

Depth profiles use a quality-first dynamic target. The floor prevents shallow
research; the target encourages broader discovery; information saturation decides
whether searching beyond the floor is still materially useful.

Only qualified sources count toward the floor or target. A qualified source must be
opened, assessed, usable, not low quality, and have at least one of:

- Primary, official, academic, filing, regulatory, standard, case-law, or direct-text authority.
- Independent reporting or analysis.
- Deep reading rather than a skim.
- Unique information unavailable from the existing evidence base.

Do not count search snippets, near-duplicate rewrites, SEO pages, superficial
aggregations, irrelevant pages, or sources included only to increase the total.

Sources also earn evidence-value units. A normal qualified source is worth one
unit. High-quality, deeply read, authoritative, independent, and uniquely useful
sources earn additional units, capped at 2.5 units each. This lets a small body of
rare, primary, or unusually deep material outweigh a larger pile of shallow pages.

| Profile | Source floor | Evidence-unit floor | Dynamic source target | Minimum executed queries | Query ceiling |
| --- | ---: | ---: | ---: | ---: | ---: |
| light | 4 | 7 | 12 | 6 | 25 |
| standard | 8 | 18 | 30 | 15 | 60 |
| deep | 16 | 40 | 60 | 30 | 140 |
| exhaustive | 24 | 65 | 100 | 55 | 300 |

These are defaults. Raise dynamic targets for unusually broad scope, many
jurisdictions, multiple languages, or high-stakes consequences. Do not
automatically lower the anti-shallow floors for a scarce topic; let rare, primary,
deeply read, and uniquely valuable material contribute additional evidence units.

## Dynamic Stop Rule

Research may pass below the dynamic target only after:

1. The profile source floor, evidence-unit floor, and every required gate have passed.
2. Required source lanes and research waves are covered.
3. High-impact gaps are resolved.
4. Counterpoints and verification have been checked when required.
5. Further targeted searches mostly repeat known evidence or add no material change.
6. The agent records a concrete information-saturation note.
7. The final two required waves each include at least one executed query with a
   substantive result note showing what was checked and learned.

Record saturation:

```powershell
python <plugin-root>/scripts/research_session.py assess-saturation `
  --session <path> `
  --status pass `
  --note "<specific account of what was searched, what repeated, and why remaining gaps are low impact>"
```

If useful niche, primary, long-form, or high-authority sources remain unexplored,
record `--status continue` and keep researching.

## Profile Selection

- `light`: quick but sourced orientation.
- `standard`: normal sourced report or article.
- `deep`: default for Deep Research, long-form work, criticism, market research,
  policy work, and literature reviews.
- `exhaustive`: book-length, academic, legal, financial, high-risk, or explicitly
  exhaustive work.

## Literary And Cultural Work

External source counts do not replace primary-text analysis. The runtime also
requires textual anchors for literary and cultural criticism.

## Budgets

Budgets are upper bounds, not completion signals. If the ceiling is exhausted
before saturation and evidence gates pass, report the limitation and remaining
gaps instead of calling the result fully researched.
