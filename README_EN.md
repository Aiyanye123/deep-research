<div align="center">
  <img src="plugins/deep-research/assets/logo.png" width="112" alt="Deep Research icon">
  <h1>Deep Research for Codex</h1>
  <p>A controllable, resumable, evidence-driven Deep Research plugin for high-quality long-form writing.</p>
  <p><a href="README.md">简体中文</a> | <strong>English</strong></p>
</div>

## Why This Plugin Exists

Ordinary "research this deeply" prompts often stop after opening only a handful of pages, then jump directly from search summaries to a finished draft. Deep Research turns research into an inspectable, persistent workflow: it first clarifies the uncertainties that materially affect the research direction, then searches in multiple waves, records sources and claims, checks evidence gaps, and allows outlining and drafting only after the dynamic evidence gate has passed.

It is primarily designed for:

- Literary, film, and cultural criticism
- Academic papers, policy research, and research reports
- Market, industry, financial, and legal analysis
- Evidence-based long-form work ranging from thousands to tens of thousands of words
- Research deliverables that need charts, diagrams, or explanatory images

## Core Capabilities

- **Dynamic clarification**: asks at least 3 questions with no fixed upper limit; questions are induced from genuine uncertainties in the topic rather than an unrelated fixed questionnaire.
- **Multi-wave research**: separates discovery into orientation, expansion, counterevidence, gap filling, and verification so the model cannot stop after searching only a few pages.
- **Dynamic evidence gate**: source count is not the only target. The plugin also checks source quality, information gain, coverage of major claims, counterevidence, and unresolved gaps.
- **Persistent research sessions**: queries, sources, claims, textual anchors, gaps, and stage state are written to files, allowing work to resume after context compression or in a new task.
- **Original insight**: distinguishes source consensus, existing interpretations, counterreadings, and the writer's own argument before drafting, avoiding mechanical assembly of web summaries.
- **Long-form continuity**: preserves terminology, argumentation, and section transitions through the outline, section-level evidence assignment, and continuity notes.
- **Multilingual prose editing**: adjusts expression according to language, article type, and content while protecting facts, citations, and the established argument.
- **Factual-drift protection**: automatically preserves an immutable copy of the researched draft before Humanizer editing, then rechecks citations, numbers, qualifications, and source boundaries afterward.
- **Research visualization**: can generate reproducible charts, Mermaid diagrams, tables, or clearly labeled explanatory images through Codex image generation.

## Workflow

```text
dynamic clarification
  -> confirm brief
  -> multi-wave research and source logging
  -> evidence gate
     -> fail: continue research
     -> pass: evidence audit
  -> insight and outline
  -> independent insight audit
  -> chart and visual decisions
  -> long-form drafting
  -> preserve researched draft
  -> article-type-aware prose editing
  -> final factual audit
  -> workflow gate
```

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
Use Deep Research for this topic. Before formal research, ask me about the uncertainties that materially affect the argument and research direction. Confirm the brief, conduct multi-wave research, and write the long-form article only after the evidence gate passes.
```

The plugin completes dynamic clarification first and does not begin searching in the same turn. After the user replies, it generates and confirms the brief, then creates a persistent research session.

## Seven Skills

| Skill | Responsibility |
| --- | --- |
| `deep-research` | Main workflow, clarification protocol, and stage gates |
| `research-orchestrator` | Query strategy, research waves, gaps, and stop conditions |
| `evidence-auditor` | Source, claim, citation, and factual-drift audits |
| `insight-architect` | Original thesis, counterreadings, and long-form structure |
| `research-visualizer` | Charts, tables, diagrams, and generated images |
| `longform-writer` | Section-by-section drafting and long-form continuity |
| `prose-humanizer` | Article-type-aware multilingual prose editing |

The main Skill invokes the other six Skills at fixed stages and uses `workflow-gate` to verify that no stage was skipped.

## Chinese Prose Profiles

Writing direction is determined by language, article type, subject, evidence density, reader relationship, and the confirmed brief. Publication venue is not used as a voice preset. Chinese deliverables select one content-driven profile:

- `essayistic`: emphasizes interpretation, judgment, and prose rhythm, allowing evidence-based first person and asymmetrical paragraph structures.
- `formal`: emphasizes precise attribution, argumentative boundaries, stable structure, and conventional components of research documents.
- `technical`: emphasizes terminological consistency, explicit conditions, direct procedures, and exact preservation of code, formulas, units, and identifiers.

`style-sheet.md` records the selected profile, protected content, citation visibility, evidence-preservation policy, sentence rhythm, paragraph movement, technical density, and expressions to retain or avoid. The editing stage uses the session's claims, sources, textual anchors, and outline as its material base. It may not restart clarification, create a second research plan, invent material, paraphrase direct quotations, or silently shorten the requested length. Evidence gaps must return to the research workflow.

After editing a Chinese draft, run:

```powershell
python plugins/deep-research/scripts/check_chinese_prose.py <draft.md> --profile <essayistic|formal|technical>
```

The checker fails only on high-confidence residue such as model self-disclosure, chat endings, and opaque promotional jargon. Punctuation, contrast, first person, and context-dependent terminology produce warnings at most and are not mechanically removed. Direct quotations, citation markers, references, tables, figure captions, links, code, names, numbers, and machine fields are protected. English and other languages use their corresponding editing rules and do not run the Chinese checker.

## Research Depth

The plugin provides `light`, `standard`, `deep`, and `exhaustive` profiles, but uses dynamic targets instead of padding a raw source count. The current `exhaustive` profile has a qualified-source floor of 24, an evidence-value floor of 65 units, and a dynamic source target of 100. Research may stop below the dynamic target only after source lanes, counterevidence, verification, and information-saturation checks are complete. Rare, authoritative, deeply read material that supports major claims can receive additional evidence value; low-quality aggregations, duplicate rewrites, and pages with no information gain cannot be used as padding.

## Sessions And Evaluation

Serious research tasks preserve `brief.md`, the research plan, source and claim ledgers, textual anchors, the outline, the original researched draft, and the final audit in a dedicated directory. Even after Codex context compression, the workflow can resume from session files instead of depending on chat memory.

Run the structural evaluator:

```powershell
python plugins/deep-research/scripts/evaluate_run.py --session <research-session-directory>
```

## Project Structure

```text
.agents/plugins/marketplace.json     Codex Git marketplace manifest
plugins/deep-research/
  .codex-plugin/plugin.json          Plugin metadata
  skills/                             Seven workflow Skills
  scripts/                            Session, gate, evaluation, and chart scripts
  references/                         Research and writing rules
  tests/                              Regression tests
```

See [`ARCHITECTURE.md`](plugins/deep-research/ARCHITECTURE.md) for implementation details.

## Validation

```powershell
cd plugins/deep-research
python -m unittest discover -s tests -v
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).
