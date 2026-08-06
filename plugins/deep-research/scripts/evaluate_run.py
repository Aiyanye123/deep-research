#!/usr/bin/env python3
"""Score the structural quality of a completed Deep Research session."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_json_optional(path: Path) -> dict:
    return read_json(path) if path.exists() else {}


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def nonempty_markdown(path: Path) -> bool:
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8").strip()
    body = "\n".join(line for line in content.splitlines() if not line.startswith("#")).strip()
    return bool(body)


def bounded_score(value: float) -> int:
    return max(0, min(100, round(value)))


def source_units(source: dict, authoritative_types: set[str]) -> float:
    units = 1.0
    if source.get("quality") == "high":
        units += 0.5
    if source.get("reading_depth") == "deep":
        units += 0.5
    if source.get("source_type") in authoritative_types:
        units += 0.5
    if source.get("unique_value"):
        units += 0.5
    if source.get("independent"):
        units += 0.25
    return min(units, 2.5)


def evaluate(session: Path) -> dict:
    state = read_json(session / "session.json")
    audit = read_json(session / "audit.json")
    workflow_audit = read_json_optional(session / "workflow-audit.json")
    sources = read_jsonl(session / "sources.jsonl")
    claims = read_jsonl(session / "claims.jsonl")
    gaps = read_jsonl(session / "gaps.jsonl")
    anchors = read_jsonl(session / "textual-anchors.jsonl")

    opened = [source for source in sources if source.get("opened") and source.get("status") == "usable"]
    authoritative_types = {
        "primary",
        "primary_text",
        "official",
        "academic",
        "filing",
        "regulation",
        "standard",
        "case_law",
        "direct_text",
    }
    qualified = [
        source
        for source in opened
        if source.get("quality", "medium") != "low"
        and (
            source.get("independent")
            or source.get("unique_value")
            or source.get("reading_depth") == "deep"
            or source.get("source_type") in authoritative_types
        )
    ]
    qualified_units = sum(source_units(source, authoritative_types) for source in qualified)
    domains = {
        urlsplit(source.get("canonical_url", "")).netloc
        for source in qualified
        if urlsplit(source.get("canonical_url", "")).netloc
    }
    grounded_claims = [
        claim for claim in claims if claim.get("source_ids") or claim.get("anchor_ids")
    ]
    major_claims = [claim for claim in claims if claim.get("major")]
    grounded_major = [
        claim for claim in major_claims if claim.get("source_ids") or claim.get("anchor_ids")
    ]
    open_high_gaps = [
        gap for gap in gaps if gap.get("impact") == "high" and gap.get("status") != "resolved"
    ]
    workflow = state.get("workflow", {})
    required_stages = workflow.get("required_stages", [])
    completed_stages = {
        record.get("stage") for record in workflow.get("completed", []) if record.get("stage")
    }

    coverage = bounded_score(
        40 * len(state.get("completed_waves", [])) / max(1, len(state.get("required_waves", [])))
        + 20 * len(qualified) / max(1, state["thresholds"]["min_opened_sources"])
        + 15 * qualified_units / max(1, state["thresholds"].get("min_source_units", 1))
        + 15 * len(qualified) / max(1, state["thresholds"].get("target_opened_sources", 1))
        + 10 * qualified_units / max(1, state["thresholds"].get("target_source_units", 1))
    )
    source_quality = bounded_score(
        50 * len(domains) / max(1, state["thresholds"]["min_unique_domains"])
        + 30 * sum(bool(source.get("independent")) for source in qualified) / max(1, len(qualified))
        + 20 * sum(source.get("source_type") in authoritative_types for source in qualified)
        / max(1, len(qualified))
    )
    grounding = bounded_score(
        70 * len(grounded_claims) / max(1, len(claims))
        + 30 * len(grounded_major) / max(1, len(major_claims))
    )
    analysis = bounded_score(
        50 * len(anchors) / max(1, state["thresholds"].get("min_textual_anchors", 0) or 1)
        + 25 * sum(claim.get("kind") == "interpretation" for claim in claims) / max(1, len(claims))
        + 25 * sum(bool(claim.get("contradiction")) for claim in claims) / max(1, len(claims))
    )
    presentation = bounded_score(
        25 * nonempty_markdown(session / "brief.md")
        + 25 * nonempty_markdown(session / "outline.md")
        + 25 * nonempty_markdown(session / "draft.md")
        + 25 * nonempty_markdown(session / "continuity.md")
    )
    reliability = bounded_score(
        70 * (audit.get("status") == "pass")
        + 30 * (len(open_high_gaps) == 0)
    )
    workflow_integrity = bounded_score(
        70 * len(completed_stages) / max(1, len(required_stages))
        + 30 * (workflow_audit.get("status") == "pass")
    )

    dimensions = {
        "research_coverage": coverage,
        "source_quality_and_diversity": source_quality,
        "claim_grounding": grounding,
        "analysis_and_originality_structure": analysis,
        "presentation_and_longform_state": presentation,
        "reliability": reliability,
        "workflow_integrity": workflow_integrity,
    }
    overall = round(sum(dimensions.values()) / len(dimensions), 1)
    return {
        "session": str(session),
        "overall": overall,
        "dimensions": dimensions,
        "warnings": [
            warning
            for warning, condition in (
                ("Evidence gate has not passed.", audit.get("status") != "pass"),
                ("Full seven-skill workflow gate has not passed.", workflow_audit.get("status") != "pass"),
                ("High-impact gaps remain open.", bool(open_high_gaps)),
                ("Independent insight audit is missing.", not nonempty_markdown(session / "insight-audit.md")),
                ("Pre-humanize researched draft snapshot is missing.", not nonempty_markdown(session / "researched-draft.md")),
                ("Draft is empty.", not nonempty_markdown(session / "draft.md")),
                ("No textual anchors recorded.", not anchors and state.get("task_mode") in {"cultural_criticism", "literary_criticism", "review"}),
            )
            if condition
        ],
        "note": "This deterministic evaluator checks structure and provenance, not semantic prose quality.",
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
