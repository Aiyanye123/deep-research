#!/usr/bin/env python3
"""Build a Markdown brief for the Deep Research workflow."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


QUESTION_TEMPLATE = """## Dynamic Clarification Design

Before showing questions, silently induce possible dimensions from this specific
request and generate a candidate pool at least twice the size of the final batch.
The dimensions may concern content, production, evidence, audience, constraints,
or something unique to the task; no predefined category is mandatory or banned.
Rank candidates by how much an answer would redirect research, change the thesis,
expose overlooked material, or prevent generic conclusions.

Ask at least 3 questions across at least 3 distinct task-induced dimensions.
Three is only a safety floor, not a target, and four or five is not a ceiling.
Keep every candidate whose answer materially changes the work. If the useful set
is large, ask in coherent batches and reassess after each answer batch; do not
begin research until all remaining unknowns are low-impact, inferable, or
explicitly delegated to Codex.
Platform, audience, word count, source range, spoilers, tone, and citation format
are valid when materially important, but they are not a default checklist. When
useful, anchor questions to specific material from the prompt, chat, or outline.
Include at least one genuinely open question that cannot be answered with yes/no
or by selecting a supplied option. Do not ask about supplied choices or state a
preferred answer before the user responds. Use non-exhaustive examples only when
needed for clarity. Give each question one primary decision; split independent
choices rather than bundling several settings into one long question.

### Questions To Ask

1. `[dimension | impact | open]` [Genuinely open high-information question.]
2. `[different dimension | impact | choice or confirmation]` [One-decision question.]
3. `[third dimension | impact | any form]` [One-decision question.]
4. [Continue whenever another branch materially changes research or argument.]
"""


BRIEF_TEMPLATE = """## Rewritten Research Prompt

Research the topic below using the original prompt and clarification answers as binding constraints.

### Objective

[State the central research objective.]

### Task Mode

[State cultural criticism, market research, academic review, policy brief, technical briefing, comparison, or long-form essay.]

### Audience

[State the intended reader and use case.]

### Final Deliverable

[State report, essay, article, chapter, literature review, strategy memo, or other.]

### Article Type And Publication Constraints

[State essay, review, column, memo, literature review, technical briefing, personal reflection, or other type. State only binding publication constraints such as citation visibility, length, formatting, or moderation limits.]

### Target Length And Structure

[State total word count, sections, installments, and any outline requirements.]

### Tone And Style

[State voice, register, pacing, and any examples to emulate or avoid.]

### Scope

[State geography, timeframe, domain, comparison set, included entities, and exclusions.]

### Key Questions Or Hypotheses

[List the claims, questions, or hypotheses the research must address.]

### Must-Cover Details

[List specific people, characters, companies, products, scenes, datasets, concepts, or arguments that must appear.]

### Do-Not-Do Constraints

[List style, scope, spoiler, source, length, or tone constraints that must not be violated.]

### Source Requirements

[State preferred source types, citation style, source recency, and source strictness.]

### Uncertainty Policy

[State how to handle missing, conflicting, or low-confidence evidence.]

### Visualization Requirements

[State whether visuals are required, what questions they should answer, available datasets, output format, publication constraints, and whether generated explanatory imagery is acceptable.]

### Drafting Plan

[State the order of research, outline, drafting installments, and final review.]

### Prose-Humanizer Pass

[State the article type, target voice, language, protected quotations and structures, citation visibility, and terms, numbers, or technical phrases that must remain unchanged. For Chinese work, record the likely essayistic, formal, or technical profile; finalize it in the style sheet.]

### Supporting Skill Plan

- Research orchestrator:
- Evidence auditor:
- Insight architect:
- Research visualizer:
- Prose humanizer:
- Longform writer:

### Ordered Workflow Stages

- [ ] `brief_confirmed`
- [ ] `research_plan`
- [ ] `evidence_preoutline_audit`
- [ ] `insight_outline`
- [ ] `insight_audit`
- [ ] `evidence_predraft_audit`
- [ ] `visualization_review`
- [ ] `style_sheet`
- [ ] `continuity_ready`
- [ ] `draft_complete`
- [ ] `evidence_prehumanize_audit`
- [ ] `humanized_draft`
- [ ] `evidence_final_audit`

### Persistent Research Session

- Session path:
- Depth profile:
- Required source lanes:
- Must-cover items:
- Query and failure budgets:
- Qualified-source floor and dynamic target:
- Source qualification rules:
- Information-saturation criteria:
- Evidence-gate requirements:
"""


def read_text(value: str | None, file_path: str | None, field_name: str) -> str:
    if value and file_path:
        raise SystemExit(f"Use either --{field_name} or --{field_name}-file, not both.")
    if file_path:
        return Path(file_path).read_text(encoding="utf-8").strip()
    return (value or "").strip()


def build_markdown(prompt: str, answers: str) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    answers_block = answers if answers else "[Paste the user's answers here before rewriting.]"
    return f"""# Deep Research Brief

Generated: {generated}

## Original Prompt

{prompt if prompt else "[Paste the original user prompt here.]"}

{QUESTION_TEMPLATE}

## Clarification Answers

{answers_block}

Record at least three answered questions with `add-clarification --dimension
"<task-induced dimension>" --impact "<what the answer changes>" --question-form
open|choice|confirmation` before `brief_confirmed`. The runtime requires three
distinct dimensions and at least one open question, but does not impose a fixed
topic taxonomy or content/production quota. It has no waiver path.

## Brief Confirmation

[Write one natural paragraph confirming the deliverable, audience, article type, focus, length, voice, and source boundary before researching.]

{BRIEF_TEMPLATE}

## Research Orchestration

[Use research-orchestrator to define source hierarchy, search lanes, risky sources, freshness requirements, search waves, evidence gates, and stop conditions.]

Create and maintain a persistent session with `scripts/research_session.py`. Log
queries, opened sources, atomic claims, textual anchors, and gaps after every wave.

## Research Depth Plan

[Use research-orchestrator to define depth level, search waves, evidence gates, gap checks, contradiction checks, verification checks, and stop conditions.]

### Search Waves

- Orientation:
- Authority:
- Detail:
- Counterpoint:
- Verification:

### Gap Loop

- Missing source lanes:
- Weakly supported sections:
- Unverified names, dates, numbers, quotes, or terms:
- Contradictions to check:
- Next targeted query:
- Saturation status and justification:

## Evidence Audit

| ID | Claim or detail | Source | Source type | Date | Evidence note | Confidence | Contradictions | Use in section |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## Insight Architecture

[Use insight-architect to build original insight, thesis, counterreading, outline, word budget, section sequence, and evidence assignment.]

- Primary interpretive question:
- Core thesis:
- Why this is not just a summary:
- Textual anchors:
- Source context:
- Tension or contradiction:
- Counterreading:
- Original insight candidates:
- Chosen argument:
- Claims to avoid:
- Evidence needed before drafting:

## Independent Insight Audit

Status: [pass or fail]
Original contribution:
Strongest conventional alternative:
Counterevidence:
Required revisions:

## Visualization Review

[Use research-visualizer to choose among tables, reproducible charts, Mermaid diagrams, advanced plotting tools, and Codex built-in image generation. Record retained figures, source data or final prompts, transformations, captions, alt text, placement, and audit status. Explain a text-only decision when no visual adds analytical value.]

## Style Sheet

[Use prose-humanizer to define voice, article and topic fit, paragraph movement, personal presence, citation visibility, protected content, and evidence-preservation policy. For Chinese work, select essayistic, formal, or technical and use the same checker profile.]

## Chapter Drafting Plan

[Use longform-writer to draft by section from the insight architecture, evidence audit, style sheet, and continuity note.]

## Source Log

Use this table during research.

| Source | Publisher | Date | URL | Relevance |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Continuity Notes

Use this section for long-form projects.

- Thesis:
- Voice:
- Chinese prose profile:
- Prose-humanizer notes:
- Established claims:
- Recurring terms:
- Open gaps:
- Next section:

## Final Evidence Audit

[Use evidence-auditor before and after prose-humanizer. Track unsupported claims, weak claims, citation mismatches, number/date/unit issues, and post-edit drift.]

## Hard Drafting Gate

Run `python <plugin-root>/scripts/research_session.py gate --session <session-path>`.

If the gate fails, continue research from its `next_actions`. Do not outline or
draft until the gate passes.

Record every companion-skill stage with `complete-stage`. Before returning the
final deliverable, run
`python <plugin-root>/scripts/research_session.py workflow-gate --session <session-path>`.
If it fails, follow its `next_actions` and do not call the work complete.
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a Markdown brief for the Deep Research workflow."
    )
    parser.add_argument("--prompt", help="Original user prompt.")
    parser.add_argument("--prompt-file", help="Path to a text file containing the original prompt.")
    parser.add_argument("--answers", help="Clarification answers from the user.")
    parser.add_argument("--answers-file", help="Path to a text file containing clarification answers.")
    parser.add_argument("--output", help="Write Markdown to this file instead of stdout.")
    args = parser.parse_args()

    prompt = read_text(args.prompt, args.prompt_file, "prompt")
    answers = read_text(args.answers, args.answers_file, "answers")
    markdown = build_markdown(prompt, answers)

    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        print(markdown)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
