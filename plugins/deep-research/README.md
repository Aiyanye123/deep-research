# Deep Research

Deep Research is a local Codex plugin for exploratory, source-backed research and
polished writing. It supports literary criticism, factual investigation, academic
reviews, market analysis, technical explanations, and mixed inquiries.

## Input Material

Use supplied files or pasted material, combine them with web research, or research
primarily online. File-only writing is supported and does not require an external
search. Inputs can include text and Markdown, Word or PDF documents, spreadsheets,
slides, screenshots, datasets, interview notes, and existing drafts, as the host's
reading tools support them.

Read the relevant material before asking topic-specific questions. Clarify whether
it serves as the factual basis, a primary work, creative material, a writing sample,
or a draft to develop when that distinction matters. Respect a supplied-material-only
boundary, identify inaccessible content, and do not pretend to have read it.
Source locations need only be sufficient to revisit important passages or data.
No separate file-ingestion stage or inventory is required.

## Default Approach

With no workflow instruction, use skills flexibly. An explicit request such as
"使用默认流程", "默认全流程", or the equivalent default/full workflow selects
the complete sequence: opening questions and direction, research, findings check,
synthesis and structure, visual decision, drafting, final prose polish, and a
focused final evidence check. Read and use all seven skills in that mode, with
`evidence-auditor` checking findings and the final text. Make visuals only when
useful, and polish affected passages after factual corrections.

Both modes retain opening questions and the required article-writing routine
below. Flexible skill selection does not make those writing actions optional.
The full sequence does not require managed-session gates, fingerprints, ledgers,
or proof files.

For a new research or writing task, the first substantive reply asks opening
questions and waits. Referenced chats, earlier recommendations, existing outlines,
drafts, and detailed requests do not constitute completed intake. The user need
not explicitly ask for questions. Only answered opening questions for this work
in the current chat or an explicit request to skip them permits proceeding.

Begin with questions that help the user discover worthwhile directions, not just
fill gaps in the original request. Explore assumptions, wider contexts, unfamiliar
comparisons, and deeper levels of explanation. Wait for the user's answers unless
they explicitly ask to skip questions. A complete prompt still receives thoughtful
opening questions; do not repeat information already supplied.

Confirm the chosen direction briefly. Research, interpret, outline, and write as
the inquiry develops. Use relevant skills and tools when they help. Follow useful
connections, consider evidence that complicates the explanation, and preserve
explicit user boundaries. Skills are selected as needed in flexible operation;
the explicitly selected full sequence uses all seven. Neither requires a fixed
number of research waves.

Check important factual claims, numbers, quotations, citations, and conclusions
against their sources. The extent of verification follows their impact and risk.
Ideas and tentative interpretations can be developed before their factual basis
is fully established, with that status kept clear.

**Every article or substantial manuscript rewrite follows four required actions:**

1. Establish focus and organization from the user's purpose and actual material.
2. Draft through the material, developing the explanation across connected passages.
3. Read the completed structure and revise development, proportion, and continuity.
4. Polish the resulting language and recheck consequential meaning affected by edits.

Read `prose-humanizer` before drafting or rewriting and use it again for the final
pass. Actually perform structure review and expression polishing even when the
draft sounds fluent. Preserve facts, quotations, terminology, the meaning of
necessary qualifications, and the user's requested scope and length. These are
writing actions, not a fixed article outline, proof files, or extra approval steps.
Original connections, interpretations, structures, and voices remain open. Focus
and organization can change as discoveries develop; review preserves purposeful
irregularity and ambiguity rather than enforcing a conventional shape.

## Agent Responsibilities

The lead keeps opening questions, direction, decisive source reading, central
interpretation, initial organization, drafting, revision decisions, and final
language polishing. This authorship boundary also applies in orchestration mode.

In the complete workflow, delegate useful independent research branches, document
extraction, focused factual checks, calculations under an agreed method, and
figure production when those tasks exist. Assign whole-manuscript structural
review to a subagent using `insight-architect`; the lead implements useful revisions
and performs the final language pass. The reviewer receives the complete current
text, user purpose and constraints, and relevant original material, and returns
located issues and proposals rather than a rewritten article.

In flexible operation, delegate when beneficial; a narrow task may have its
structural review performed by the lead. If subagents are prohibited or unavailable,
the lead performs the work and reports that boundary. No fixed agent count or
one-agent-per-skill arrangement is required. Keep source access and necessary
context in handoffs; the lead reads decisive originals without repeating all
routine retrieval or verification. Do not default to parallel chapter drafting
or delegate final language polishing. No new review file or certificate is required.

Prose review considers the connected argument as well as individual sentences:
repeated paragraph shapes, automatic reversals, quotable endings, detached source
summaries, and abstractions that obscure the subject. Learn the movement and
viewpoint of a user sample without importing its content into reusable rules or
substituting louder rhetoric for clearer writing.
Remove defensive padding aimed at imagined objections and place real limits by
the claims they affect. Theory should explain specific material, with its meaning
and relevance clear to the reader; labels alone do not supply analysis.

## Skills As A Toolbox

- `deep-research`: opening inquiry, user direction, and overall judgment.
- `research-orchestrator`: source discovery, research strategy, and depth.
- `insight-architect`: deeper interpretation, synthesis, and useful structure.
- `evidence-auditor`: focused checks of consequential evidence and claims.
- `longform-writer`: drafting and continuity when work spans sections or installments.
- `research-visualizer`: charts, diagrams, and illustrations when they aid understanding.
- `prose-humanizer`: required final prose review and polishing.

Read a skill when using it. Select companions according to the chosen workflow;
the four writing actions always take place. Do not generate a no-visuals report when prose
is enough or create a style sheet, continuity ledger, or audit file just to satisfy
a stage.

## Sources And Working Notes

Keep enough information to revisit important evidence: useful links or document
locations and precise passages, dates, or data references where relevant.
A compact note can serve a long project or a handoff. The default workflow does
not require JSONL query and claim logs, evidence IDs for every section, input
fingerprints, two draft copies, stage records, or gate commands.

Research depth depends on the question. Substantial work should seek a supported
explanation and examine meaningful alternatives, without padding counts or
claiming exhaustive coverage it did not achieve. Literary work uses the primary
text and preserves ambiguity; market, academic, factual, and technical work use
evidence appropriate to their questions.

## Optional Tools

- `scripts/build_research_brief.py` produces a compact working brief.
- `scripts/render_chart.py` renders common charts from CSV.
- `scripts/check_chinese_prose.py` offers advisory Chinese prose diagnostics.
- The existing `research_session.py` runtime and `evaluate_run.py` remain available
  for explicitly chosen managed projects or resumption of projects using them.
  Their stage and artifact requirements apply only to that optional runtime.
  Do not start it automatically because a task is serious or long.

Existing sessions and tools are preserved. The runtime's structural results do
not prove research quality. Follow the user's tool and verification restrictions;
the default workflow performs no hash-based approval checks.

This is an unofficial workflow and does not imply access to OpenAI's private
Deep Research implementation. Relevant method, prose, and source-handling notes
are in `references/`; the optional runtime format is in
`references/session-schema.md`.
