<div align="center">
  <img src="plugins/deep-research/assets/logo.png" width="112" alt="Deep Research icon">
  <h1>Deep Research for Codex</h1>
  <p>Explore deeply, develop original understanding, and write clearly from files, web sources, or both.</p>
  <p><a href="README_ZN.md">简体中文</a> | <strong>English</strong></p>
</div>

## Why This Plugin Exists

Deep Research is a local Codex plugin for exploratory research and substantial writing. Version **0.6.2** supports supplied files, pasted material, existing drafts, web sources, and combinations of them. Opening questions explore assumptions and wider perspectives, while research, interpretation, and writing can inform each other. Important facts and conclusions receive appropriate verification, and every article receives structural review and final language polishing.

It is primarily designed for:

- Literary, film, and cultural criticism
- Academic papers, policy research, and research reports
- Market, industry, financial, and legal analysis
- Evidence-based long-form work ranging from thousands to tens of thousands of words
- Research deliverables that need charts, diagrams, or explanatory images

## Core Capabilities

- **Exploratory opening questions**: the first substantive reply asks questions and waits unless explicitly waived. Detailed requests and referenced conversations do not count as answered intake.
- **Flexible or complete operation**: select skills as needed, or explicitly request the default/full workflow to use all seven skills.
- **Multiple input types**: read actual supplied material with the host's available tools. File-only writing is valid; external search is not compulsory.
- **Original understanding**: develop connections, hypotheses, competing readings, and structures without forcing novelty or treating a source summary as the final explanation.
- **Required writing actions**: establish focus and organization, develop the material, review the completed structure, and polish language while checking affected meaning.
- **Bounded delegation**: subagents handle useful research branches, factual checks, figure production, and full-manuscript structural review. The lead retains core interpretation, writing, and final language polishing.
- **Useful visualization**: make charts, diagrams, or clearly labeled illustrations when they improve understanding.

## Workflow

```text
read input and ask opening questions -> wait for answers and confirm direction
  -> research supplied material, web sources, or both
  -> check important findings
  -> develop interpretation and organization
  -> decide whether a visual helps; produce one only when useful
  -> lead-authored manuscript
  -> subagent structural review; lead implements useful revisions
  -> lead performs whole-text language polishing
  -> focused final factual check; lead corrects and repolishes affected passages
```

This complete sequence is selected by an explicit default/full workflow request. Without one, the model selects skills as needed. Both modes preserve opening questions and the four writing actions. Discovery can change the provisional focus, interpretation, and structure. Full workflow additionally uses a managed research session with an evidence gate and dependency-based workflow gate; flexible work does so only when selected or resuming a managed project. No content fingerprints, fixed paragraph template, question quota, or paired drafts are required.

## Installation

Requires a Codex CLI version that supports plugin marketplaces.

```powershell
codex plugin marketplace add Aiyanye123/deep-research
codex plugin add deep-research@aiyanye-deep-research
```

Start a new Codex task after installation or upgrade so the updated Skills are loaded completely.

## Usage

Select **Deep Research** in Codex, or make a request such as:

```text
Use Deep Research's default full workflow to develop an article from these files.
Ask questions that deepen or broaden the inquiry, and wait for my answers before formal research.
```

To use flexible operation, select the plugin without requesting the full workflow, or explicitly ask it to use skills as needed. Opening questions may be preceded by relevant input reading and a bounded orientation check. Formal research and drafting wait for actual answers unless you explicitly ask to skip questions.

Delegation is driven by skill instructions and the host's subagent tools, not a dispatch script. In the full workflow, structural review goes to a subagent with the complete current manuscript, user purpose and constraints, and relevant source access. It returns located issues and proposals; the lead decides and implements changes and performs final language polishing. Independent research, verification, and production tasks are delegated when they exist and save work. Do not create an agent per skill. If delegation is prohibited or unavailable, the lead completes the work and states the limitation.

## Seven Skills

| Skill | Responsibility |
| --- | --- |
| `deep-research` | Opening inquiry, workflow selection, writing actions, and division of labor |
| `research-orchestrator` | Source discovery, research strategy, gaps, and stop conditions |
| `evidence-auditor` | Focused factual, citation, and support checks |
| `insight-architect` | Original connections, interpretation, organization, and structural review |
| `research-visualizer` | Charts, tables, diagrams, and generated images |
| `longform-writer` | Lead-authored drafting and continuity |
| `prose-humanizer` | Required final prose review and lead-performed language polishing |

Read a skill when using it and actually perform its work. The lead reads decisive original material rather than relying solely on subagent summaries; well-supported routine checks need not be repeated. These authorship boundaries also apply when using an orchestration mode.

## Chinese Prose Profiles

Writing direction follows the user's purpose, preferred writing, reader, and material. The subject or publication venue does not automatically determine the article type or voice. The Chinese prose reference offers these optional tendencies:

- `essayistic`: emphasizes interpretation, judgment, and prose rhythm, allowing evidence-based first person and asymmetrical paragraph structures.
- `formal`: emphasizes precise attribution, argumentative boundaries, stable structure, and conventional components of research documents.
- `technical`: emphasizes terminological consistency, explicit conditions, direct procedures, and exact preservation of code, formulas, units, and identifiers.

Prioritize natural, concrete, accurate Chinese, precise verbs, meaningful detail, and supported judgments. Develop connected passages rather than repeated reversals, disclaimers, or closing maxims. Theory should explain the material; useful ambiguity and rhetoric may remain. Learn a sample's viewpoint and movement without importing its content into reusable rules. Preserve facts, quotations, terminology, and the meaning of necessary qualifications; repetitive cautionary wording can be revised. No style-sheet file or paired drafts are required.

For optional diagnostics of a specific Chinese prose issue, use:

```powershell
python plugins/deep-research/scripts/check_chinese_prose.py <draft.md> --profile <essayistic|formal|technical>
```

The checker fails only on high-confidence residue such as model self-disclosure, chat endings, and opaque promotional jargon. Punctuation, contrast, first person, and context-dependent terminology produce warnings at most and are not mechanically removed. Direct quotations, citation markers, references, tables, figure captions, links, code, names, numbers, and machine fields are protected. English and other languages use their corresponding editing rules and do not run the Chinese checker.

## Research Depth

Whole-text structural review and the lead's final language pass actively address clusters of mechanical symmetry, parallel verdicts, aphoristic endings, defensive self-commentary, and disclaimer padding. Rebuild connected passages and sentence rhythm when needed, rather than only swap synonyms; preserve meaningful distinctions, counterevidence, and limits.

In the default/full workflow, complementary delegated searches expand coverage and the useful original-source candidate pool beyond the minimum needed to draft. Set task-appropriate retrieval targets or ranges in `research-plan.md`, normally beginning with deep's target of 60 useful opened sources for substantial work (standard targets 30). Open promising sources, consolidate derivative evidence chains, and retain useful unexpected leads. The lead checks coverage, follows consequential gaps, and selects decisive originals for deep reading. Adapt targets to corpus availability and user boundaries; quantity alone does not prove quality or support.

Research depth follows the question, consequential unknowns, and promising paths. Read important sources, compare relevant alternatives, and investigate gaps that could change the answer. Stop when the central explanation is supported and further work is unlikely to improve it materially. Do not pad source counts or claim exhaustive coverage without doing it. Managed sessions record actual waves and saturation checks; numerical shortfalls in schema 3 and later are effort-review warnings rather than proof of unsupported findings.

## Sessions And Evaluation

The explicitly selected default/full workflow automatically creates `research-sessions/<YYYY-MM-DD-topic>/` using `research_session.py` after intake is answered or waived and the direction is chosen. Preserve separate stage-based files: `brief.md`, `research-plan.md`, `pre-outline-audit.md`, `outline.md`, `visuals.md`, `draft.md`, `structure-review.md`, and `final-audit.md`, along with session state, stage records, and actual query, source, important claim, gap, and relevant anchor records. Use `research-notes.md` for useful working findings when needed. Save the complete manuscript before structural review, then update it through revision, whole-text polish, and corrections. Export the approved draft to any requested final path; deliver the manuscript and session location. Preserve existing files and respect explicit changes to saving or gates.

New managed sessions use nine stages with prerequisites rather than a fixed child-agent return order. Drafting and visual review can finish in either order after synthesis; polish waits for structural and visual review, and final factual review waits for polish. Consolidate independent child results before serial updates to shared records. Reopening a stage invalidates that node and its dependency descendants, leaving unrelated branches intact. Run `gate` before committed structure and drafting and `workflow-gate` before delivery. No content fingerprints are computed or compared: meaningful file edits require the lead to reopen affected stages and actually review them again. Existing sessions retain their original required stages and historical fingerprints as inert data.

In flexible operation, use conversation context, notes, or files according to resumption needs, and select managed operation only when requested or continuing a managed project. Session files and passing gates do not prove research quality or actual reading. The evaluator remains optional. See the [session schema](plugins/deep-research/references/session-schema.md).

For an explicitly selected managed session, its structural evaluator is:

```powershell
python plugins/deep-research/scripts/evaluate_run.py --session <research-session-directory>
```

## Project Structure

```text
.agents/plugins/marketplace.json     Codex Git marketplace manifest
plugins/deep-research/
  .codex-plugin/plugin.json          Plugin metadata
  skills/                             Seven workflow Skills
  scripts/                            Brief, chart, optional diagnostic and managed-session tools
  references/                         Research and writing rules
  tests/                              Regression tests
```

See [`ARCHITECTURE.md`](plugins/deep-research/ARCHITECTURE.md) for implementation details.

## Validation

Validate skill frontmatter, the plugin manifest, and affected tools when changing the package. The `tests/` directory retains tests for the optional managed runtime. Run checks appropriate to the change and the user's tool restrictions; structural checks do not establish actual model behavior, originality, or writing quality. Model-level behavior requires real research and writing trials.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
