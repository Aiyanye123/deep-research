# Research Session Schema

This file describes the managed runtime automatically selected by an explicit
default/full-workflow request. Flexible operation selects it only when requested
or resuming a managed project. New sessions use schema 4 and the current skill
workflow's dependencies; existing sessions preserve their recorded required
stages. There are no content fingerprints or hash comparisons. Historical
fingerprint fields are ignored and are not rewritten or verified.

After answered or explicitly waived intake and direction selection, use
`scripts/research_session.py init --session <path> --title <title> --depth deep`
to create a new session directory. Use `resume` for an existing session, never
`init --force` to replace its files. Normally use deep's opened-source target of
60 for substantial full-workflow research; standard targets 30. Adapt targets
to the corpus and user constraints. Breadth targets guide actual discovery,
not evidence validity. The lead selects decisive originals for deep reading.

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
  visuals.md
  figures/
  research-notes.md              # Optional useful extracts and working findings
  draft.md
  structure-review.md
  final-audit.md
  audit.json
```

## `session.json`

Stores the current phase, depth profile, required research waves and lanes, must-cover
and covered items, budgets, thresholds, planned sections, evidence-gate result,
required companion-skill workflow stages, and ready actions. Schema 4 uses the
dependency graph below; earlier sessions retain their original required-stage
list and sequence. Records do not substitute for doing the work.

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

New sessions require these stages, matching the current full workflow:

| Stage | Required skill | Artifact | Prerequisites |
| --- | --- | --- | --- |
| `brief_confirmed` | `deep-research` | `brief.md` | Actual answers or explicit waiver |
| `research_plan` | `research-orchestrator` | `research-plan.md` | `brief_confirmed` |
| `evidence_preoutline_audit` | `evidence-auditor` | `pre-outline-audit.md` | `research_plan`, passing evidence gate |
| `insight_outline` | `insight-architect` | `outline.md` | `evidence_preoutline_audit` |
| `visualization_review` | `research-visualizer` | `visuals.md` | `insight_outline` |
| `draft_complete` | `longform-writer` | `draft.md` | `insight_outline` |
| `structure_review` | `insight-architect` | `structure-review.md` | `draft_complete` |
| `humanized_draft` | `prose-humanizer` | `draft.md` | `structure_review`, `visualization_review` |
| `evidence_final_audit` | `evidence-auditor` | `final-audit.md` | `humanized_draft` |

Stages from the findings audit onward also require a passing evidence gate.
`complete-stage` accepts any ready stage with completed prerequisites, its actual
artifact, and a substantive completion note; it does not enforce subagent return
order. `status` and `resume` show all `ready_stages`. Drafting and visual review
can finish in either order after synthesis, but final language polish waits for
structural and visual review. Independent discovery and factual checks can run
in parallel inside stages. The lead consolidates results before serial updates
to shared session records; avoid concurrent JSONL writes.

`workflow-gate` requires all recorded required stages, correct dependency order,
a currently passing evidence gate, substantive artifacts, and passing review
records. Structural review and evidence audits require `Status: pass` and
`Required revisions: none` after blocking problems have actually been resolved.
`audit-context` lists relevant inputs to inspect; it computes no fingerprint.
Read and assess the actual current manuscript and sources. No file or marker
proves that the reviewer did this or that the conclusion is sound.

There is no automatic detection of direct file edits. After a meaningful change
to sources, interpretation, manuscript, or figures, the lead identifies affected
work and uses `reopen-stage --session <path> --stage <stage> --note "<reason>"`.
It removes that stage and its dependency descendants while preserving unrelated
completed branches, files, and historical logs. Recheck and revise before recording
completion again; a stale audit cannot be reused just because its file exists.
Reopening final factual review also requires polishing any corrections before
delivery. Automated record updates invalidate related work where the runtime
recognizes changed evidence; direct edits still need the lead's judgment.

Run `gate --session <path>` before committed outlining and formal drafting, and
`workflow-gate --session <path>` before delivering the final `draft.md`. Resolve
actual failures; do not bypass checks by filling fabricated records. Legacy
sessions keep their original required stages. Their insight audit fields remain
required where applicable, but old fingerprints do not. New sessions do not
require those additional legacy stages, style sheets, continuity files, or paired drafts.

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
In schema 3 and later, major claims require a nonempty `evidence_note` and `locator`.
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
- `outline.md`: the focus and organization suited to the actual material.
- `visuals.md`: visualization decision and figure manifest, including source data or
  generation prompt, transformations, caption, alt text, placement, and audit state.
- `figures/`: generated assets and the cleaned data used to reproduce quantitative figures.
- `research-notes.md`: optional useful source context, findings, interpretations,
  and unresolved questions; retain important original material when helpful.
- `structure-review.md`: actual whole-manuscript findings, passage locations, and
  the lead's revision decisions. The subagent reviews; the lead implements changes
  and resolves blockers before recording the required pass markers.
- `draft.md`: current manuscript, revised and polished by the lead.
- `final-audit.md`: evidence-auditor review of the actual final draft and corrections.

The following remain available when useful or required by a legacy session:

- `insight-audit.md`: independent interpretation and contribution review.
- `pre-draft-audit.md`: legacy evidence approval after section assignments.
- `style-sheet.md`: prose-humanizer voice, article type, topic direction, Chinese
  prose profile when applicable, protected content, evidence-preservation policy,
  citation visibility, and checker profile.
- `continuity.md`: thesis, established claims, terminology, open loops, and handoff.
- `researched-draft.md`: a pre-polish snapshot for manual comparison; no fingerprint
  binds it to an approval. Legacy stages can still create it.
- `pre-humanize-audit.md`: audit of the researched draft before prose editing.

## `audit.json`

Written by `research_session.py gate`. It contains `pass` or `fail`, reasons,
metrics, and required next actions.

## `workflow-audit.json`

Written by `research_session.py workflow-gate`. It verifies required stages,
dependencies, review markers, and substantive artifacts. It cannot establish
that a final audit covers an unrecorded file edit.

## Information Saturation

The session state records whether further targeted research is likely to change
the result. Saturation must include a concrete note and is invalidated when new
queries, sources, claims, gaps, or textual anchors are added.

For schema 3 and later, numerical effort targets produce warnings rather than automatic
failure. Explain corpus boundaries, the checks performed, whether recent evidence
changed conclusions, and remaining unknowns in the saturation note and audits.
Queries can record targeted searches within supplied material, not just web search.
Legacy sessions remain readable and retain their numerical thresholds and
required-stage list. No historical evidence files are rewritten by loading a
session, and no historical content fingerprints are verified.
