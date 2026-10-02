# Deep Research Architecture

The default workflow relies on model judgment and a small set of outcome
requirements. Flexible operation selects skills as needed; the explicit full
workflow additionally uses a managed session with dependency-based gates.

## Workflow Selection

Without a workflow instruction, companions are selected as needed. An explicit
request to use the default/full workflow selects: opening inquiry, research,
findings verification, synthesis and structure, visual decision, drafting,
prose polish, and focused final verification. This uses all seven skills;
`evidence-auditor` checks the findings and the final text. A text-only decision is
valid for the visual step. Revisions can return to the relevant work without
restart certificates or a new approval round.

Opening questions and the required article-writing routine apply in both modes.
Companion selection is flexible; the writing actions are mandatory. Selecting
the full sequence automatically selects the managed-session runtime and its
stage-based artifacts. It uses evidence and workflow gates without fingerprints.

## Default Flow

Opening inquiry helps the user discover deeper or wider questions. Wait for
answers unless the user explicitly waives questions, then briefly confirm the
chosen direction. Research, interpretation, structure, and drafting can develop
together. Check important facts and conclusions, and always review and polish the
completed prose before delivery.

Every article or substantial manuscript rewrite carries out four actions:
establish focus and organization; draft through the material; read and revise
the completed structure; polish language and check consequential meaning affected
by edits. Read `prose-humanizer` before drafting and use it again for the final
pass. Structure review precedes expression polishing, with revision where needed
even in flexible operation. These actions require no additional runtime stages,
fixed article structure, or completion artifacts.

## Agent Responsibilities

The lead owns inquiry direction, firsthand understanding of decisive sources,
central synthesis, initial organization, writing, revision decisions, and final
language polishing. Independent source discovery, extraction, targeted factual
verification, calculations under an agreed method, and figure production are
delegated when useful in the complete workflow. Whole-manuscript structural
review is assigned to a subagent using `insight-architect`; the lead resolves
and implements proposals, then polishes the whole text itself.

These authorship boundaries remain in orchestration mode. Flexible operation
uses the same boundaries and delegates when beneficial; a narrow structural
review can stay with the lead. Respect source and delegation restrictions, and
perform the work directly if agents are unavailable. Pass actual source access,
current manuscript, necessary context, and locators rather than only summaries.
Do not repeat well-supported routine checks, create an agent per skill, or add
mandatory handoff records. Original ideas can come from any agent; integration
and the article's voice remain with the lead.

In the complete workflow, complementary retrieval branches expand coverage and
the useful candidate pool beyond the minimum draft-ready sources. The research
plan sets task-appropriate retrieval targets or ranges, adapted to the available
corpus and user boundaries. Agents open promising sources and trace original
material; shared evidence origins are consolidated. The lead checks coverage,
follows consequential gaps, and selects decisive originals for deep reading.
These effort goals are not universal quotas or evidence-validity gates.

On a new task, the first substantive reply presents questions and ends the turn
to wait. Referenced discussions and complete-looking input are context, not an
answered intake. Formal research, research delegation, drafting, and article-file
creation follow actual answers for this work in the current chat or an explicit
waiver. No new runtime stage or management file is needed to observe this boundary.

The full workflow records actual research, important evidence, required waves,
and stage completion; numerical source goals are effort guidance, not evidence
validity. New sessions use nine stages matching the current skills, rather than
restoring the legacy thirteen-stage sequence. Independent work is parallel;
committed downstream stages wait for their real prerequisites. Flexible operation
does not require this runtime. Neither mode uses fingerprints or requires paired drafts.

Exploratory ideas may precede evidence. Verify factual premises as appropriate
and keep speculative, interpretive, and established claims distinguishable.
Respect explicit boundaries; let the user choose material scope extensions.

## Capabilities

- `deep-research` coordinates the inquiry and preserves user direction.
- `research-orchestrator` helps find, read, and compare useful sources.
- `insight-architect` develops interpretation, synthesis, and structure.
- `evidence-auditor` checks consequential facts and support when useful.
- `longform-writer` handles prose and continuity for substantial work.
- `research-visualizer` adds informative visuals when justified.
- `prose-humanizer` performs the required final prose review and polish.

Read companions when using them. The explicitly selected full workflow uses the
entire toolbox; otherwise choose useful companions.
Final polishing is always required; dedicated style files, duplicate drafts,
or additional audit certificates are not.

## Persistence And Tools

Inputs can come from user files, pasted text, existing drafts, web sources, or a
combination. The host reads the actual material using tools suited to its format;
the plugin requires no dedicated ingestion pipeline or automatic web search.
Honor user limits on external lookup and distinguish document content from
instructions. Keep relevant source locations when they aid the work.

Conversation context and concise working notes can hold the chosen question,
important sources, findings, uncertainties, and current draft in flexible operation.
Save files when resumption or handoff benefits. The explicitly selected full
workflow creates `research-sessions/<YYYY-MM-DD-topic>/` in the task workspace or
selected output root after answered or waived intake and direction selection,
unless the user declines file saving. Preserve stage-based files: `brief.md`,
`research-plan.md`, `pre-outline-audit.md`, `outline.md`, `visuals.md`, `draft.md`,
`structure-review.md`, and `final-audit.md`, together with state, stage records,
and actual query, source, important claim, gap, and relevant anchor records.
Use `research-notes.md` for working findings when helpful. Export the approved
draft to any user-specified delivery path. Update sources, findings,
uncertainties, and actual review feedback with revision decisions as work develops.
Retain generated assets in `figures/` when useful. Save the manuscript before structural
review, then update it through revision, polish, and corrections. Provide the
final manuscript and session location at delivery. Preserve existing files;
report unavailable write access accurately. No additional completion artifacts
are required. Read the schema before initializing or resuming the managed runtime.
Run the evidence gate before committed outlining and drafting, then the workflow
gate before delivery. These checks do not establish actual reading or quality.

`complete-stage` accepts any ready stage, not only one next item. Drafting and
visual review are parallel after synthesis; structural review needs the manuscript;
polish needs structural and visual review; final factual review needs polish.
Reopening a stage clears that node and its dependency descendants while retaining
unrelated completed branches. Lead judgment must trigger reopening after meaningful
file edits; no content fingerprint automatically detects them. Shared session
records are updated serially after child results are consolidated.

The brief generator creates an optional compact aid. The chart renderer and
Chinese prose checker serve specific needs. Existing session-management and
evaluation scripts support managed projects. The runtime is selected by explicit
full workflow or a separate managed request; the evaluator remains optional.
Legacy sessions retain their own stage list, with old fingerprints ignored.

The scripts do not browse or run a model. Their structural results cannot establish
semantic support, originality, depth, or prose quality. The default process
uses no fingerprint or hash-based approval checks.

## Quality Boundary

Effort follows the question's breadth, difficulty, and consequences. Verify what
could materially change understanding or a decision: important facts, data,
quotations, interpretations presented as facts, and central conclusions.
Source locations should be useful enough to revisit the relevant material;
records should not become a substitute for reading it.

Writing and final polish must preserve facts, source boundaries, and the requested
scope. Recheck affected content when substantive edits could change meaning.
Unknowns should influence the conclusion instead of being hidden or turned into
mandatory paperwork.
