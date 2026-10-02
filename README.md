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

This complete sequence is selected by an explicit default/full workflow request. Without one, the model selects skills as needed. Both modes preserve opening questions and the four writing actions. Discovery can change the provisional focus, interpretation, and structure. No fixed paragraph template, question count, research waves, source quota, ledger, duplicate draft, or completion certificate is required.

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

Research depth follows the question, consequential unknowns, and promising paths. Read important sources, compare relevant alternatives, and investigate gaps that could change the answer. Stop when the central explanation is supported and further work is unlikely to improve it materially. Do not pad source counts or claim exhaustive coverage without doing it. Legacy depth profiles and gates belong only to the explicitly selected managed runtime.

## Sessions And Evaluation

Keep useful source locations, important findings, and unresolved questions in conversation context or concise notes. Files can support a long project, resumption, or handoff when helpful. The existing `research_session.py` and `evaluate_run.py` tools remain available only for an explicitly chosen managed workflow or projects already using it. A long or serious task does not activate them automatically. Their structural results do not prove research quality; respect user restrictions on verification.

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
