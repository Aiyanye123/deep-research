# Research Session Schema

This file describes the existing optional managed runtime. Its logs, stages,
artifacts, and approval checks apply only when the user explicitly selects that
workflow or resumes a project already using it. They are not requirements of the
default Deep Research skills. Respect user restrictions on tools and verification;
do not run prohibited hash checks. Existing session data remains unchanged.

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
Questions can introduce frames beyond the initial prompt. Record the actual
exchange and concise impact on the selected direction, not every brainstorm or
a proof of each speculative idea. An `anchor` is optional; a wider connection
does not have to originate in the supplied material.
Record actual user answers to the default opening questions. `brief_confirmed`
requires at least one answered question, unless the user explicitly waived intake
and their exact request is supplied with `--skip-questions-request`. The stage
record stores this request as `skip_questions_request`. A complete prompt or
inferred preferences cannot waive intake. There is no fixed questionnaire,
dimension quota, or required open question. The brief and completion note explain
which constraints were provided, safely inferred, or explicitly delegated, and
why no consequential unknown still requires clarification.

## Workflow Stages

`complete-stage` records an ordered stage, the required companion skill, its
artifact, a substantive completion note, and an artifact hash. Research commands
are blocked until `research_plan` exists. Outlining is blocked until
`evidence_preoutline_audit` exists.

`workflow-gate` requires every stage, a currently passing evidence gate, substantive
artifacts, and a final evidence audit of the current `draft.md`. Editing the draft
after the final audit invalidates workflow completion.

Every audit stage requires `Status: pass`, `Required revisions: none`, and
`Input fingerprint: <current hash>` from `audit-context --session <path> --stage
<stage>`. The insight audit additionally records `Knowledge contribution`,
`Strongest alternative`, `Counterevidence`, and `Judgment update`. Explain when an
alternative is not applicable instead of inventing false balance. Fingerprints
track inputs; the auditor must still read and evaluate them.

Use `reopen-stage --session <path> --stage <stage> --note "<reason>"` for the
earliest completed stage needing revision. Existing files and logs are retained;
that stage and downstream approvals are removed until reviewed again. A stale
audit cannot be reapproved merely because its file still exists.

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
- `origin`: original evidence source shared by derivative reports
- `lane` and `source_type`
- `quality`: `high`, `medium`, or `low`
- `reading_depth`: `skim`, `read`, or `deep`
- `opened`
- `status`: `usable`, `failed`, or `rejected`
- `independent`
- `unique_value`
- `prompt_injection_suspected`

A search-result snippet is not an opened source.
Local documents may use absolute `file:///...` URIs. A common origin means repeated
reports are not separate corroboration. An origin label is provenance information,
not automatic proof of independence.
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
- `evidence_note`: what the evidence establishes and how the conclusion follows
- `locator`: source/anchor ID and exact passage, page, table, or timestamp
- `assumptions` and `limitations`
- `support_type`: `direct`, `inference`, `interpretation`, or `forecast`

Every claim requires a valid source or textual anchor before the evidence gate can pass.
Use `update-claim` to correct a claim or replace its evidence references.
In schema-3 sessions, major claims require a nonempty `evidence_note` and `locator`.
Use the additional fields for central, disputed, causal, or decision-relevant
claims; ordinary background facts do not require a long form.

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
  counterevidence and judgment-update review of the proposed contribution.
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

For schema 3, numerical effort targets produce warnings rather than automatic
failure. Explain corpus boundaries, the checks performed, whether recent evidence
changed conclusions, and remaining unknowns in the saturation note and audits.
Queries can record targeted searches within supplied material, not just web search.
Legacy sessions remain readable and retain their numerical thresholds. Existing
legacy audits must be redone with current input fingerprints before approval;
no historical evidence files are rewritten by loading a session.
