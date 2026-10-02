#!/usr/bin/env python3
"""Report structural checks and activity metrics for a Deep Research session."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import research_session


DEFAULT_RUBRIC = {
    "task_type": "General research",
    "criteria": [
        "Check that the report answers the confirmed research question and respects the requested scope and format.",
        "Check whether important facts and arguments are represented accurately and with enough context.",
        "Check that the evidence directly supports the claims, and that important claims use suitable independent sources.",
        "Check for synthesis, counterevidence, uncertainty, and conclusions that follow from the evidence.",
        "Check whether the contribution is useful and supported; confirming a consensus, clarifying its limits, or establishing an unknown can qualify.",
        "Check whether the structure, continuity, and prose fit the intended reader and deliverable.",
    ],
}

TASK_MODE_RUBRICS = {
    "literary_or_cultural_criticism": {
        "task_type": "Literary or cultural criticism",
        "modes": ["literary_criticism", "cultural_criticism", "review"],
        "criteria": [
            "Check whether the interpretive question, observation, or thesis is specific and responsive to the requested work and angle.",
            "Check that interpretations rest on precise passages, scenes, formal choices, or other primary evidence.",
            "Check whether the report connects close reading to context without treating context as proof by itself.",
            "Where applicable, check plausible alternative readings and details that complicate the interpretation, without forcing false balance or novelty.",
            "Check that fact, inference, and uncertainty remain distinct, and that the conclusion advances beyond plot or source summary.",
        ],
    },
    "academic_literature_review": {
        "task_type": "Academic literature review",
        "modes": ["academic", "academic_literature_review", "literature_review"],
        "criteria": [
            "Check whether the review defines a focused question, field boundary, and relevant time or method limits.",
            "Check whether coverage represents the important theories, methods, evidence, and disagreements rather than a paper-by-paper list.",
            "Compare study designs, populations, measures, and limitations before combining findings.",
            "Check whether the synthesis explains agreement, disagreement, uncertainty, and evidence gaps.",
            "Check citation accuracy and whether the stated contribution or research gap follows from the reviewed literature.",
        ],
    },
    "market_or_company_research": {
        "task_type": "Market or company research",
        "modes": ["market_research", "company_research", "market_or_company_research"],
        "criteria": [
            "Check that the market, geography, customer segment, time period, and decision question are defined consistently.",
            "Check important market-size, growth, financial, and operating claims against traceable source data and stated definitions.",
            "Check whether primary company disclosures and independent market evidence are distinguished and compared.",
            "Check competitors, demand drivers, constraints, counterevidence, and material risks rather than relying on a single growth story.",
            "Check that assumptions, scenarios, and recommendations are explicit and proportionate to the evidence.",
        ],
    },
    "technical_research": {
        "task_type": "Technical research",
        "modes": ["technical_research", "technical_briefing", "policy_brief", "policy_or_technical_briefing"],
        "criteria": [
            "Check whether the problem, system boundary, users, operating context, and decision are clearly defined.",
            "Check technical or policy claims against relevant primary documentation, standards, data, or direct evidence.",
            "Check whether the report explains mechanisms and dependencies rather than listing features or rules.",
            "Check failure cases, trade-offs, counterevidence, security or implementation constraints, and unresolved uncertainty.",
            "Check whether recommendations are feasible in the stated context and supported by the analysis.",
        ],
    },
    "factual_investigation": {
        "task_type": "Factual investigation or explanation",
        "modes": ["factual_investigation", "factual_research", "explanatory_article"],
        "criteria": [
            "Check whether the factual question, time frame, and included events are clearly bounded.",
            "Trace central claims to original records; distinguish independent corroboration from repeated reporting.",
            "Check chronology and conflicting accounts without treating temporal succession as causation.",
            "Separate established facts, witness or institutional claims, inference, and unknowns.",
            "Check whether the explanation answers the question and states what missing evidence could change it.",
        ],
    },
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty_markdown(path: Path) -> bool:
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8").strip()
    body = "\n".join(line for line in content.splitlines() if not line.startswith("#")).strip()
    return bool(body)


def qualitative_rubric(task_mode: str) -> dict:
    for rubric in TASK_MODE_RUBRICS.values():
        if task_mode in rubric["modes"]:
            return {
                "task_type": rubric["task_type"],
                "criteria": rubric["criteria"],
            }
    return DEFAULT_RUBRIC


def current_gate_status(result: dict) -> dict:
    return {
        "status": result["status"],
        "reasons": result.get("reasons", []),
        "warnings": result.get("warnings", []),
        "next_actions": result.get("next_actions", []),
    }


def evaluate(session: Path) -> dict:
    state = read_json(session / "session.json")

    # Read the gates from session state and artifacts on every run. Persisted audit
    # files are historical records and can be stale.
    evidence_gate = research_session.gate_result(session)
    workflow_gate = research_session.workflow_gate_result(session)

    task_mode = state.get("task_mode", "general_research")
    artifact_paths = {
        "brief": session / "brief.md",
        "outline": session / "outline.md",
        "insight_audit": session / "insight-audit.md",
        "researched_draft": session / "researched-draft.md",
        "draft": session / "draft.md",
        "continuity": session / "continuity.md",
    }

    return {
        "session": str(session),
        "structural_checks": {
            "evidence_gate": current_gate_status(evidence_gate),
            "workflow_gate": current_gate_status(workflow_gate),
            "report_artifacts_nonempty": {
                name: nonempty_markdown(path) for name, path in artifact_paths.items()
            },
        },
        "research_review_required": True,
        "qualitative_rubric": qualitative_rubric(task_mode),
        "activity_metrics": {
            "task_mode": task_mode,
            "evidence_gate": evidence_gate.get("metrics", {}),
            "workflow_gate": workflow_gate.get("metrics", {}),
        },
        "note": (
            "Structural checks and activity counts do not establish research quality. "
            "Complete the qualitative review against the task-specific rubric."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    session = Path(args.session).expanduser().resolve()
    result = evaluate(session)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
