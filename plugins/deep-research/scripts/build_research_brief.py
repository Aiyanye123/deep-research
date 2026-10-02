#!/usr/bin/env python3
"""Build an optional compact working brief for Deep Research."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


QUESTION_TEMPLATE = """## Opening Questions

For a new task, the first substantive reply must ask questions and end the turn
to wait for the user. Referenced chats, earlier recommendations, existing outlines,
drafts, and complete-looking requests are context, not completed opening intake.
A complete deliverable specification does not waive questions. No formal
research, research delegation, or drafting before
the reply. Continue without repeating intake only after actual opening questions
for this work were answered in the current chat or explicitly waived.

Explore before narrowing. Treat the initial framing as a starting point: question
premises, change the level of analysis, connect unfamiliar fields or comparisons,
and consider overlooked viewpoints or different criteria when fruitful. These
are possibilities, not a checklist. Include a substantive question that opens
or challenges the frame unless the user explicitly confines discussion to it.

Explain briefly what a new direction could reveal. Exploratory ideas need not
already have a full evidence plan; verify factual premises when appropriate.
Do not repeat supplied answers, require a candidate quota, or show process labels.

Ask a manageable set and wait for actual answers before formal research unless
the user explicitly requests skipping questions. Let the user choose which
extensions become part of the brief. Once a workable direction is chosen, proceed
without exhausting every branch or seeking approval for each ordinary step.
"""


BRIEF_TEMPLATE = """## Agreed Direction

[Confirm the central question and the wider or deeper direction chosen by the user
in one natural paragraph. Unselected suggestions are not requirements.]

## Workflow Choice

[Use skills flexibly unless the user explicitly requests the default/full workflow.
In that case, carry out: deep-research opening questions and agreed direction;
research-orchestrator research; evidence-auditor findings check; insight-architect
synthesis and structure; research-visualizer visual decision and useful visuals;
longform-writer draft; prose-humanizer full polish; evidence-auditor focused final
check. Polish affected passages after factual corrections. Read and use all seven
skills for the complete workflow; a text-only visual decision needs no artifact.
Both modes retain opening questions and the required article-writing routine
unless the user's explicit instructions change them. Flexible skill selection
does not waive the writing actions below. Neither mode activates managed-session
gates or requires proof files. Keep the selected mode in the working context,
not a separate form.]

## Execution Responsibilities

[The lead handles opening questions, direction, decisive original-source reading,
central interpretation, initial organization, manuscript drafting, revision
decisions, and final language polishing, including in orchestration mode.
In the complete workflow, delegate useful independent source searches and
extraction, focused factual checks, and figure production when those tasks exist.
Assign the complete manuscript's structural review to a subagent using
insight-architect; it returns located issues and proposals, not rewritten prose.
The lead implements useful changes and performs the final whole-text language pass.
In flexible operation, delegate when beneficial; the lead may perform structural
review for a narrow task. Give subagents actual sources and current text, and
require usable source locations, necessary context, and unresolved issues.
Read decisive originals rather than rely solely on summaries; do not repeat
well-supported routine checks or create an agent for every skill. If delegation
is prohibited or unavailable, perform the work directly and state the limitation.]

## Intended Work

[State the deliverable, reader, length, voice, and boundaries that actually matter.
Do not invent missing constraints or require every field to be filled.]

## Material To Use

[Note supplied files, pasted text, datasets, existing drafts, or web sources as
relevant. Read the actual material. State whether external lookup is allowed or
needed when that matters; supplied material alone is a valid basis for an article.
Keep useful source locations without a compulsory file inventory.]

## Research Priorities

[Note the most fruitful questions, relevant material, and important unknowns.
Use the method suited to the topic; let discoveries reshape the inquiry.]

## Working Notes And Sources

[Keep useful links, important findings, and source locations here if needed.
No per-query ledger, fixed search waves, stage records, or separate audits are
required. A short project can keep these in conversation context.]

## Writing And Final Polish

[Always perform these writing actions in either mode. Read prose-humanizer before
drafting or rewriting, and use it again for the final pass:

1. Establish focus and organization from the user's purpose and actual material;
   do not infer the article type or tone from its subject alone.
2. Draft through the material with developed, connected reasoning. Integrate
   sources and useful concepts into the explanation, without invented detail.
3. Obtain whole-text structural review under the division of labor; the lead
   revises passages where development, proportion, or continuity fails. Address
   repeated verdicts, automatic reversals, and defensive padding; keep meaningful
   limits with the claims they affect.
4. The lead reads and polishes the resulting whole text for natural, concrete,
   accurate expression and rhythm. Preserve facts, quotations, terminology, the
   meaning of qualifications, and the requested scope and length. Recheck consequential meaning or facts
   affected by edits and polish passages changed by corrections.

Actually perform the reviews even when the first draft sounds fluent. Learn a
sample's movement and viewpoint without copying its content. Research, drafting,
and revision may inform each other. New connections, interpretations, structures,
and voices remain open; discoveries can change the provisional focus and structure
within the user's boundaries. Preserve purposeful irregularity and ambiguity.
No separate style sheet, duplicate draft,
fingerprint, or completion certificate is required.]
"""


def read_text(value: str | None, file_path: str | None, field_name: str) -> str:
    if value and file_path:
        raise SystemExit(f"Use either --{field_name} or --{field_name}-file, not both.")
    if file_path:
        return Path(file_path).read_text(encoding="utf-8").strip()
    return (value or "").strip()


def build_markdown(prompt: str, answers: str) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    answers_block = answers if answers else "[Record the user's actual answers or explicit request to skip questions.]"
    return f"""# Deep Research Working Brief

Generated: {generated}

This is an optional aid, not a required workflow form.

## Original Request

{prompt if prompt else "[Paste the original user request here.]"}

{QUESTION_TEMPLATE}

## User Answers

{answers_block}

{BRIEF_TEMPLATE}
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create an optional compact Deep Research working brief."
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
