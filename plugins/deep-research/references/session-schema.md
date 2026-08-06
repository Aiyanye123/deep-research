# Research Session Schema

Use `scripts/research_session.py init` to create a session directory.

```text
research-sessions/<slug>/
  brief.md
  clarifications.jsonl
  research-plan.md
  pre-outline-audit.md
  session.json
  stage-log.jsonl
  workflow-audit.json
  queries.jsonl
  sources.jsonl
  claims.jsonl
  gaps.jsonl
  textual-anchors.jsonl
  outline.md
  insight-audit.md
  pre-draft-audit.md
  visuals.md
  figures/
  style-sheet.md
  continuity.md
  draft.md
  researched-draft.md
  pre-humanize-audit.md
  final-audit.md
  audit.json
```

## `session.json`

Stores the current phase, depth profile, required research waves and lanes, must-cover
and covered items, budgets, thresholds, planned sections, evidence-gate result,
ordered companion-skill workflow stages, and next actions.

## `clarifications.jsonl`

Stores each dynamic clarification question and answer with its task-induced
`dimension`, its decision `impact`, and an optional prompt- or material-specific
`anchor`. `question_form` records `open`, `choice`, or `confirmation`.
`brief_confirmed` requires at least three records across three distinct
dimensions. Dimension names are free-form rather than selected from a fixed
taxonomy; no topic category is mandatory or forbidden. At least one record must
be genuinely `open`. There is no waiver path.

## Workflow Stages

`complete-stage` records an ordered stage, the required companion skill, its
artifact, a substantive completion note, and an artifact hash. Research commands
are blocked until `research_plan` exists. Outlining is blocked until
`evidence_preoutline_audit` exists.

`workflow-gate` requires every stage, a currently passing evidence gate, substantive
artifacts, and a final evidence audit of the current `draft.md`. Editing the draft
after the final audit invalidates workflow completion.

## `queries.jsonl`

One record per unique query:

- `id`
- `query`
- `normalized_query`
- `wave`
- `lane`
- `status`
- `result_note`

Duplicate normalized queries are rejected.

## `sources.jsonl`

One record per canonical URL:

- `id`
- `url` and `canonical_url`
- `title`, `publisher`, and `published_date`
- `lane` and `source_type`
- `quality`: `high`, `medium`, or `low`
- `reading_depth`: `skim`, `read`, or `deep`
- `opened`
- `status`: `usable`, `failed`, or `rejected`
- `independent`
- `unique_value`
- `prompt_injection_suspected`

A search-result snippet is not an opened source.
Low-quality sources and sources without authority, independence, deep reading, or
unique value do not count toward the qualified-source gate.

Qualified sources also receive evidence-value units. Depth, authority,
independence, high quality, and unique value increase their weight, so a rare
primary source or deeply analyzed niche document contributes more than a normal
secondary page.

Use `update-source` when later verification changes the source assessment.

## `claims.jsonl`

One atomic claim per record:

- `id`
- `claim`
- `kind`: `fact`, `interpretation`, or `forecast`
- `confidence`
- `major`
- `source_ids`
- `anchor_ids`
- `section`
- `contradiction`

Every claim requires a valid source or textual anchor before the evidence gate can pass.
Use `update-claim` to correct a claim or replace its evidence references.

## `gaps.jsonl`

Tracks unresolved questions, impact, status, and the next targeted query. The gate
cannot pass while a high-impact gap remains open.

## `textual-anchors.jsonl`

Use for literary and cultural criticism:

- location: scene, chapter, episode, timestamp, or passage
- formal feature
- observation
- interpretation
- alternative reading
- planned section

## Markdown Artifacts

- `brief.md`: confirmed user brief and binding constraints.
- `research-plan.md`: source strategy, waves, lanes, gaps, and stop conditions.
- `pre-outline-audit.md`: evidence-auditor handoff from research to outlining.
- `outline.md`: insight architecture and section cards.
- `insight-audit.md`: independent originality, conventional-alternative, and
  counterevidence review of the proposed thesis.
- `pre-draft-audit.md`: evidence-auditor approval after section evidence assignment.
- `visuals.md`: visualization decision and figure manifest, including source data or
  generation prompt, transformations, caption, alt text, placement, and audit state.
- `figures/`: generated assets and the cleaned data used to reproduce quantitative figures.
- `style-sheet.md`: prose-humanizer voice, article type, topic direction, Chinese
  prose profile when applicable, protected content, evidence-preservation policy,
  citation visibility, and checker profile.
- `continuity.md`: thesis, established claims, terminology, open loops, and handoff.
- `draft.md`: current researched draft.
- `researched-draft.md`: immutable automatic snapshot created immediately before
  Humanizer editing.
- `pre-humanize-audit.md`: audit of the researched draft before prose editing.
- `final-audit.md`: evidence-auditor review of the humanized final draft.

## `audit.json`

Written by `research_session.py gate`. It contains `pass` or `fail`, reasons,
metrics, and required next actions.

## `workflow-audit.json`

Written by `research_session.py workflow-gate`. It verifies that no companion-skill
stage was skipped and that the final audit matches the current draft.

## Information Saturation

The session state records whether further targeted research is likely to change
the result. Saturation must include a concrete note and is invalidated when new
queries, sources, claims, gaps, or textual anchors are added.
