#!/usr/bin/env python3
"""Create, update, and gate a persistent Deep Research session."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


DEPTH_PROFILES = {
    "light": {
        "required_waves": ["orientation", "authority", "detail"],
        "min_executed_queries": 6,
        "min_queries_per_wave": 1,
        "min_opened_sources": 4,
        "target_opened_sources": 12,
        "min_source_units": 7.0,
        "target_source_units": 20.0,
        "min_unique_domains": 3,
        "min_independent_sources": 2,
        "min_authoritative_sources": 1,
        "min_covered_lanes": 2,
        "max_domain_share": 0.50,
        "min_claims": 5,
        "min_textual_anchors": 0,
        "max_queries": 25,
        "max_failed_sources": 8,
    },
    "standard": {
        "required_waves": [
            "orientation",
            "authority",
            "detail",
            "counterpoint",
            "verification",
        ],
        "min_executed_queries": 15,
        "min_queries_per_wave": 3,
        "min_opened_sources": 8,
        "target_opened_sources": 30,
        "min_source_units": 18.0,
        "target_source_units": 55.0,
        "min_unique_domains": 7,
        "min_independent_sources": 5,
        "min_authoritative_sources": 3,
        "min_covered_lanes": 3,
        "max_domain_share": 0.35,
        "min_claims": 15,
        "min_textual_anchors": 0,
        "max_queries": 60,
        "max_failed_sources": 15,
    },
    "deep": {
        "required_waves": [
            "orientation",
            "authority",
            "detail",
            "counterpoint",
            "verification",
        ],
        "min_executed_queries": 30,
        "min_queries_per_wave": 6,
        "min_opened_sources": 16,
        "target_opened_sources": 60,
        "min_source_units": 40.0,
        "target_source_units": 110.0,
        "min_unique_domains": 14,
        "min_independent_sources": 12,
        "min_authoritative_sources": 7,
        "min_covered_lanes": 4,
        "max_domain_share": 0.25,
        "min_claims": 36,
        "min_textual_anchors": 0,
        "max_queries": 140,
        "max_failed_sources": 35,
    },
    "exhaustive": {
        "required_waves": [
            "orientation",
            "authority",
            "detail",
            "counterpoint",
            "verification",
        ],
        "min_executed_queries": 55,
        "min_queries_per_wave": 12,
        "min_opened_sources": 24,
        "target_opened_sources": 100,
        "min_source_units": 65.0,
        "target_source_units": 180.0,
        "min_unique_domains": 22,
        "min_independent_sources": 20,
        "min_authoritative_sources": 12,
        "min_covered_lanes": 5,
        "max_domain_share": 0.15,
        "min_claims": 60,
        "min_textual_anchors": 0,
        "max_queries": 300,
        "max_failed_sources": 70,
    },
}

CULTURAL_MODES = {"cultural_criticism", "literary_criticism", "review"}
AUTHORITATIVE_SOURCE_TYPES = {
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
WORKFLOW_STAGES = [
    {
        "name": "brief_confirmed",
        "skill": "deep-research",
        "artifact": "brief.md",
        "requires_evidence_gate": False,
    },
    {
        "name": "research_plan",
        "skill": "research-orchestrator",
        "artifact": "research-plan.md",
        "requires_evidence_gate": False,
    },
    {
        "name": "evidence_preoutline_audit",
        "skill": "evidence-auditor",
        "artifact": "pre-outline-audit.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "insight_outline",
        "skill": "insight-architect",
        "artifact": "outline.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "insight_audit",
        "skill": "evidence-auditor",
        "artifact": "insight-audit.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "evidence_predraft_audit",
        "skill": "evidence-auditor",
        "artifact": "pre-draft-audit.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "visualization_review",
        "skill": "research-visualizer",
        "artifact": "visuals.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "style_sheet",
        "skill": "prose-humanizer",
        "artifact": "style-sheet.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "continuity_ready",
        "skill": "longform-writer",
        "artifact": "continuity.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "draft_complete",
        "skill": "longform-writer",
        "artifact": "draft.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "evidence_prehumanize_audit",
        "skill": "evidence-auditor",
        "artifact": "pre-humanize-audit.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "humanized_draft",
        "skill": "prose-humanizer",
        "artifact": "draft.md",
        "requires_evidence_gate": True,
    },
    {
        "name": "evidence_final_audit",
        "skill": "evidence-auditor",
        "artifact": "final-audit.md",
        "requires_evidence_gate": True,
    },
]
WORKFLOW_STAGE_BY_NAME = {stage["name"]: stage for stage in WORKFLOW_STAGES}
WORKFLOW_STAGE_NAMES = [stage["name"] for stage in WORKFLOW_STAGES]
MUTABLE_WORKFLOW_ARTIFACT_STAGES = {
    "continuity_ready",
    "draft_complete",
    "humanized_draft",
}
TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, value: dict | list) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSONL in {path}:{line_number}: {exc}") from exc
    return records


def append_jsonl(path: Path, value: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False) + "\n")


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if not parts.scheme or not parts.netloc:
        raise SystemExit(f"URL must include a scheme and host: {url}")
    query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        lowered = key.casefold()
        if lowered in TRACKING_QUERY_KEYS:
            continue
        if any(lowered.startswith(prefix) for prefix in TRACKING_QUERY_PREFIXES):
            continue
        query.append((key, value))
    path = parts.path.rstrip("/") or "/"
    return urlunsplit(
        (
            parts.scheme.casefold(),
            parts.netloc.casefold(),
            path,
            urlencode(sorted(query)),
            "",
        )
    )


def source_units(source: dict) -> float:
    """Reward deep, authoritative, independent, and uniquely useful sources."""
    units = 1.0
    if source.get("quality") == "high":
        units += 0.5
    if source.get("reading_depth") == "deep":
        units += 0.5
    if source.get("source_type") in AUTHORITATIVE_SOURCE_TYPES:
        units += 0.5
    if source.get("unique_value"):
        units += 0.5
    if source.get("independent"):
        units += 0.25
    return min(units, 2.5)


def next_id(prefix: str, records: list[dict]) -> str:
    highest = 0
    for record in records:
        match = re.fullmatch(rf"{re.escape(prefix)}-(\d+)", str(record.get("id", "")))
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{prefix}-{highest + 1:04d}"


def session_dir(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Research session does not exist: {path}")
    return path


def load_session(path: Path) -> dict:
    return read_json(path / "session.json")


def save_session(path: Path, state: dict) -> None:
    state["updated_at"] = utc_now()
    write_json(path / "session.json", state)


def invalidate_evidence_gate(state: dict) -> None:
    state["evidence_gate"] = "not_run"
    state["gate_reasons"] = []
    state["next_actions"] = ["Run the evidence gate after research state stabilizes"]


def invalidate_saturation(state: dict) -> None:
    state["saturation"] = {
        "status": "not_assessed",
        "note": None,
        "assessed_at": None,
        "evidence_query_ids": [],
    }
    invalidate_evidence_gate(state)


def ensure_workflow_state(state: dict) -> dict:
    workflow = state.setdefault(
        "workflow",
        {
            "required_stages": list(WORKFLOW_STAGE_NAMES),
            "completed": [],
        },
    )
    workflow.setdefault("required_stages", list(WORKFLOW_STAGE_NAMES))
    workflow.setdefault("completed", [])
    return workflow


def completed_stage_names(state: dict) -> list[str]:
    workflow = ensure_workflow_state(state)
    return [record["stage"] for record in workflow["completed"]]


def next_workflow_stage(state: dict) -> str | None:
    completed = set(completed_stage_names(state))
    return next((name for name in WORKFLOW_STAGE_NAMES if name not in completed), None)


def invalidate_workflow_from(state: dict, stage_name: str) -> None:
    workflow = ensure_workflow_state(state)
    start = WORKFLOW_STAGE_NAMES.index(stage_name)
    invalidated = set(WORKFLOW_STAGE_NAMES[start:])
    workflow["completed"] = [
        record for record in workflow["completed"] if record["stage"] not in invalidated
    ]
    next_stage = next_workflow_stage(state)
    state["status"] = "complete" if next_stage is None else f"awaiting_{next_stage}"


def require_completed_stage(state: dict, stage_name: str) -> None:
    if stage_name not in completed_stage_names(state):
        stage = WORKFLOW_STAGE_BY_NAME[stage_name]
        raise SystemExit(
            f"Complete workflow stage '{stage_name}' with {stage['skill']} before this action."
        )


def nonempty_markdown(path: Path) -> bool:
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8").strip()
    body = "\n".join(
        line for line in content.splitlines() if not line.lstrip().startswith("#")
    ).strip()
    return bool(body)


def insight_audit_passes(path: Path) -> bool:
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    required = (
        "Original contribution",
        "Strongest conventional alternative",
        "Counterevidence",
        "Required revisions",
    )
    return bool(re.search(r"(?im)^\s*(?:[-*]\s*)?Status\s*:\s*pass\s*$", content)) and all(
        re.search(rf"(?im)^\s*(?:[-*]\s*)?{re.escape(field)}\s*:\s*\S", content)
        for field in required
    )


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def update_workflow_status(state: dict, evidence_status: str | None = None) -> None:
    evidence_status = evidence_status or state.get("evidence_gate", "not_run")
    next_stage = next_workflow_stage(state)
    if evidence_status != "pass" and next_stage not in {"brief_confirmed", "research_plan"}:
        state["status"] = "researching"
    elif next_stage is None:
        state["status"] = "complete"
    else:
        state["status"] = f"awaiting_{next_stage}"


def touch_session_files(path: Path) -> None:
    for name in (
        "clarifications.jsonl",
        "queries.jsonl",
        "sources.jsonl",
        "claims.jsonl",
        "gaps.jsonl",
        "textual-anchors.jsonl",
    ):
        (path / name).touch(exist_ok=True)
    (path / "figures").mkdir(exist_ok=True)
    for name, heading in (
        ("brief.md", "# Research Brief\n"),
        ("research-plan.md", "# Research Plan\n"),
        ("pre-outline-audit.md", "# Pre-Outline Evidence Audit\n"),
        ("outline.md", "# Outline\n"),
        ("insight-audit.md", "# Insight Audit\n"),
        ("pre-draft-audit.md", "# Pre-Draft Evidence Audit\n"),
        ("visuals.md", "# Visualization Review\n"),
        ("style-sheet.md", "# Style Sheet\n"),
        ("continuity.md", "# Continuity Notes\n"),
        ("draft.md", "# Draft\n"),
        ("pre-humanize-audit.md", "# Pre-Humanize Evidence Audit\n"),
        ("final-audit.md", "# Final Evidence Audit\n"),
    ):
        target = path / name
        if not target.exists():
            target.write_text(heading, encoding="utf-8")


def init_command(args: argparse.Namespace) -> int:
    path = Path(args.session).expanduser().resolve()
    if path.exists() and any(path.iterdir()) and not args.force:
        raise SystemExit(f"Session directory is not empty: {path}. Use --force to reuse it.")
    path.mkdir(parents=True, exist_ok=True)
    if args.force:
        for name in (
            "session.json",
            "audit.json",
            "workflow-audit.json",
            "stage-log.jsonl",
            "clarifications.jsonl",
            "queries.jsonl",
            "sources.jsonl",
            "claims.jsonl",
            "gaps.jsonl",
            "textual-anchors.jsonl",
            "brief.md",
            "research-plan.md",
            "pre-outline-audit.md",
            "outline.md",
            "insight-audit.md",
            "pre-draft-audit.md",
            "visuals.md",
            "style-sheet.md",
            "continuity.md",
            "draft.md",
            "pre-humanize-audit.md",
            "final-audit.md",
            "researched-draft.md",
        ):
            target = path / name
            if target.exists() and target.is_file():
                target.unlink()
        figures = path / "figures"
        if figures.exists():
            if figures.is_symlink() or not figures.is_dir():
                raise SystemExit(f"Unsafe figures path in session: {figures}")
            shutil.rmtree(figures)
    touch_session_files(path)

    profile = dict(DEPTH_PROFILES[args.depth])
    if args.task_mode in CULTURAL_MODES:
        profile["min_textual_anchors"] = {
            "light": 8,
            "standard": 15,
            "deep": 25,
            "exhaustive": 40,
        }[args.depth]

    selected_min_sources = args.min_opened_sources or profile["min_opened_sources"]
    selected_target_sources = (
        args.target_opened_sources
        if args.target_opened_sources is not None
        else profile["target_opened_sources"]
    )
    selected_min_units = (
        args.min_source_units
        if args.min_source_units is not None
        else profile["min_source_units"]
    )
    selected_target_units = (
        args.target_source_units
        if args.target_source_units is not None
        else profile["target_source_units"]
    )
    if selected_target_sources < selected_min_sources:
        raise SystemExit("Dynamic source target cannot be lower than the source floor.")
    if selected_target_units < selected_min_units:
        raise SystemExit("Dynamic source-unit target cannot be lower than the source-unit floor.")

    required_lanes = list(dict.fromkeys(args.required_lane or []))
    state = {
        "schema_version": 2,
        "title": args.title,
        "task_mode": args.task_mode,
        "depth_profile": args.depth,
        "status": "briefing",
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "current_wave": None,
        "completed_waves": [],
        "required_waves": profile["required_waves"],
        "required_lanes": required_lanes,
        "must_cover": list(dict.fromkeys(args.must_cover or [])),
        "covered_items": [],
        "planned_sections": [],
        "budgets": {
            "max_queries": args.max_queries or profile["max_queries"],
            "max_failed_sources": args.max_failed_sources
            if args.max_failed_sources is not None
            else profile["max_failed_sources"],
        },
        "thresholds": {
            "min_executed_queries": args.min_executed_queries
            if args.min_executed_queries is not None
            else profile["min_executed_queries"],
            "min_queries_per_wave": args.min_queries_per_wave
            if args.min_queries_per_wave is not None
            else profile["min_queries_per_wave"],
            "min_opened_sources": selected_min_sources,
            "target_opened_sources": selected_target_sources,
            "min_source_units": selected_min_units,
            "target_source_units": selected_target_units,
            "min_unique_domains": args.min_unique_domains or profile["min_unique_domains"],
            "min_independent_sources": args.min_independent_sources
            if args.min_independent_sources is not None
            else profile["min_independent_sources"],
            "min_authoritative_sources": args.min_authoritative_sources
            if args.min_authoritative_sources is not None
            else profile["min_authoritative_sources"],
            "min_covered_lanes": args.min_covered_lanes
            if args.min_covered_lanes is not None
            else profile["min_covered_lanes"],
            "max_domain_share": args.max_domain_share
            if args.max_domain_share is not None
            else profile["max_domain_share"],
            "min_claims": args.min_claims or profile["min_claims"],
            "min_textual_anchors": args.min_textual_anchors
            if args.min_textual_anchors is not None
            else profile["min_textual_anchors"],
        },
        "evidence_gate": "not_run",
        "gate_reasons": [],
        "next_actions": ["Complete and confirm brief", "Start orientation research wave"],
        "saturation": {
            "status": "not_assessed",
            "note": None,
            "assessed_at": None,
            "evidence_query_ids": [],
        },
        "workflow": {
            "required_stages": list(WORKFLOW_STAGE_NAMES),
            "completed": [],
        },
    }
    save_session(path, state)
    write_json(path / "audit.json", {"status": "not_run", "checked_at": None, "reasons": []})
    write_json(
        path / "workflow-audit.json",
        {"status": "not_run", "checked_at": None, "reasons": []},
    )
    (path / "stage-log.jsonl").touch(exist_ok=True)
    print(path)
    return 0


def add_clarification_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    if "brief_confirmed" in completed_stage_names(state):
        raise SystemExit("Clarifications cannot change after brief_confirmed.")
    question = args.question.strip()
    answer = args.answer.strip()
    if not question or not answer:
        raise SystemExit("Clarification question and answer must be non-empty.")
    dimension = args.dimension.strip()
    impact = args.impact.strip()
    if not dimension:
        raise SystemExit("Clarification dimension must be non-empty.")
    if len(impact) < 12:
        raise SystemExit(
            "Clarification impact must explain what the answer changes."
        )
    anchor = (args.anchor or "").strip()
    records = read_jsonl(path / "clarifications.jsonl")
    normalized = normalize_text(question)
    if any(record.get("normalized_question") == normalized for record in records):
        raise SystemExit("Duplicate clarification question rejected.")
    record = {
        "id": next_id("CL", records),
        "question": question,
        "normalized_question": normalized,
        "answer": answer,
        "dimension": dimension,
        "normalized_dimension": normalize_text(dimension),
        "impact": impact,
        "question_form": args.question_form,
        "anchor": anchor or None,
        "created_at": utc_now(),
    }
    append_jsonl(path / "clarifications.jsonl", record)
    save_session(path, state)
    print(record["id"])
    return 0


def add_query_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    records = read_jsonl(path / "queries.jsonl")
    normalized = normalize_text(args.query)
    if any(record.get("normalized_query") == normalized for record in records):
        print("Duplicate query rejected.", file=sys.stderr)
        return 2
    if len(records) >= state["budgets"]["max_queries"]:
        print("Query budget exhausted.", file=sys.stderr)
        return 3
    record = {
        "id": next_id("Q", records),
        "query": args.query.strip(),
        "normalized_query": normalized,
        "wave": args.wave,
        "lane": args.lane,
        "status": args.status,
        "result_note": args.result_note,
        "created_at": utc_now(),
    }
    append_jsonl(path / "queries.jsonl", record)
    state["status"] = "researching"
    state["current_wave"] = args.wave
    invalidate_saturation(state)
    invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    print(record["id"])
    return 0


def add_source_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    records = read_jsonl(path / "sources.jsonl")
    canonical_url = canonicalize_url(args.url)
    existing = next(
        (record for record in records if record.get("canonical_url") == canonical_url),
        None,
    )
    if existing:
        print(f"Duplicate source rejected: {existing['id']}", file=sys.stderr)
        return 2
    record = {
        "id": next_id("S", records),
        "url": args.url.strip(),
        "canonical_url": canonical_url,
        "title": args.title.strip(),
        "publisher": args.publisher,
        "published_date": args.published_date,
        "lane": args.lane,
        "source_type": args.source_type,
        "quality": args.quality,
        "reading_depth": args.reading_depth,
        "opened": args.opened,
        "status": args.status,
        "relevance": args.relevance,
        "independent": args.independent,
        "unique_value": args.unique_value,
        "prompt_injection_suspected": args.prompt_injection_suspected,
        "created_at": utc_now(),
    }
    append_jsonl(path / "sources.jsonl", record)
    if args.status == "failed":
        state["status"] = "researching"
    invalidate_saturation(state)
    invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    print(record["id"])
    return 0


def update_source_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    records = read_jsonl(path / "sources.jsonl")
    found = False
    for record in records:
        if record.get("id") != args.source_id:
            continue
        if args.status is not None:
            record["status"] = args.status
        if args.opened is not None:
            record["opened"] = args.opened
        if args.prompt_injection_suspected is not None:
            record["prompt_injection_suspected"] = args.prompt_injection_suspected
        if args.relevance is not None:
            record["relevance"] = args.relevance
        if args.quality is not None:
            record["quality"] = args.quality
        if args.reading_depth is not None:
            record["reading_depth"] = args.reading_depth
        if args.unique_value is not None:
            record["unique_value"] = args.unique_value
        if args.independent is not None:
            record["independent"] = args.independent
        record["updated_at"] = utc_now()
        found = True
        break
    if not found:
        raise SystemExit(f"Unknown source ID: {args.source_id}")
    write_jsonl(path / "sources.jsonl", records)
    invalidate_saturation(state)
    invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    return 0


def add_claim_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    records = read_jsonl(path / "claims.jsonl")
    source_ids = list(dict.fromkeys(args.source_id or []))
    anchor_ids = list(dict.fromkeys(args.anchor_id or []))
    record = {
        "id": next_id("C", records),
        "claim": args.claim.strip(),
        "kind": args.kind,
        "confidence": args.confidence,
        "major": args.major,
        "source_ids": source_ids,
        "anchor_ids": anchor_ids,
        "section": args.section,
        "contradiction": args.contradiction,
        "created_at": utc_now(),
    }
    append_jsonl(path / "claims.jsonl", record)
    invalidate_saturation(state)
    invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    print(record["id"])
    return 0


def update_claim_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    records = read_jsonl(path / "claims.jsonl")
    found = False
    for record in records:
        if record.get("id") != args.claim_id:
            continue
        if args.claim is not None:
            record["claim"] = args.claim
        if args.kind is not None:
            record["kind"] = args.kind
        if args.confidence is not None:
            record["confidence"] = args.confidence
        if args.major is not None:
            record["major"] = args.major
        if args.source_id is not None:
            record["source_ids"] = list(dict.fromkeys(args.source_id))
        if args.anchor_id is not None:
            record["anchor_ids"] = list(dict.fromkeys(args.anchor_id))
        if args.section is not None:
            record["section"] = args.section
        if args.contradiction is not None:
            record["contradiction"] = args.contradiction
        record["updated_at"] = utc_now()
        found = True
        break
    if not found:
        raise SystemExit(f"Unknown claim ID: {args.claim_id}")
    write_jsonl(path / "claims.jsonl", records)
    section_only = args.section is not None and all(
        value is None
        for value in (
            args.claim,
            args.kind,
            args.confidence,
            args.major,
            args.source_id,
            args.anchor_id,
            args.contradiction,
        )
    )
    if section_only:
        invalidate_evidence_gate(state)
        invalidate_workflow_from(state, "insight_outline")
    else:
        invalidate_saturation(state)
        invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    return 0


def add_gap_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    records = read_jsonl(path / "gaps.jsonl")
    record = {
        "id": next_id("G", records),
        "question": args.question.strip(),
        "impact": args.impact,
        "status": args.status,
        "next_query": args.next_query,
        "created_at": utc_now(),
    }
    append_jsonl(path / "gaps.jsonl", record)
    invalidate_saturation(state)
    invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    print(record["id"])
    return 0


def resolve_gap_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    records = read_jsonl(path / "gaps.jsonl")
    found = False
    for record in records:
        if record.get("id") == args.gap_id:
            record["status"] = "resolved"
            record["resolution"] = args.resolution
            record["resolved_at"] = utc_now()
            found = True
            break
    if not found:
        raise SystemExit(f"Unknown gap ID: {args.gap_id}")
    write_jsonl(path / "gaps.jsonl", records)
    invalidate_saturation(state)
    invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    return 0


def add_anchor_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    records = read_jsonl(path / "textual-anchors.jsonl")
    record = {
        "id": next_id("A", records),
        "location": args.location,
        "feature": args.feature,
        "observation": args.observation,
        "interpretation": args.interpretation,
        "alternative_reading": args.alternative_reading,
        "section": args.section,
        "created_at": utc_now(),
    }
    append_jsonl(path / "textual-anchors.jsonl", record)
    invalidate_saturation(state)
    invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    print(record["id"])
    return 0


def complete_wave_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    if args.wave not in state["completed_waves"]:
        state["completed_waves"].append(args.wave)
    state["current_wave"] = None
    state["status"] = "researching"
    invalidate_saturation(state)
    invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    return 0


def add_section_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "evidence_preoutline_audit")
    if args.section not in state["planned_sections"]:
        state["planned_sections"].append(args.section)
    invalidate_evidence_gate(state)
    invalidate_workflow_from(state, "insight_outline")
    save_session(path, state)
    return 0


def cover_item_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    if args.item not in state["must_cover"]:
        raise SystemExit(f"Item is not in must-cover list: {args.item}")
    if args.item not in state["covered_items"]:
        state["covered_items"].append(args.item)
    invalidate_saturation(state)
    invalidate_workflow_from(state, "evidence_preoutline_audit")
    save_session(path, state)
    return 0


def assess_saturation_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    require_completed_stage(state, "research_plan")
    note = args.note.strip()
    if len(note) < 60:
        raise SystemExit(
            "Saturation note is too short. Explain what targeted searches were run, "
            "what repeated, and why remaining gaps are low impact."
        )
    if args.status == "pass":
        missing_waves = [
            wave
            for wave in state["required_waves"]
            if wave not in state["completed_waves"]
        ]
        if missing_waves:
            raise SystemExit(
                f"Cannot pass saturation before required waves complete: {', '.join(missing_waves)}"
            )
        open_high_gaps = [
            gap["id"]
            for gap in read_jsonl(path / "gaps.jsonl")
            if gap.get("status") != "resolved" and gap.get("impact") == "high"
        ]
        if open_high_gaps:
            raise SystemExit(
                f"Cannot pass saturation with open high-impact gaps: {', '.join(open_high_gaps)}"
            )
        required_check_waves = state["required_waves"][-2:]
        queries = read_jsonl(path / "queries.jsonl")
        evidence_queries = [
            query
            for query in queries
            if query.get("status") == "executed"
            and query.get("wave") in required_check_waves
            and len(str(query.get("result_note") or "").strip()) >= 20
        ]
        covered_check_waves = {query.get("wave") for query in evidence_queries}
        missing_check_waves = [
            wave for wave in required_check_waves if wave not in covered_check_waves
        ]
        if missing_check_waves:
            raise SystemExit(
                "Saturation requires one executed query with a substantive result note "
                f"in each final research wave: {', '.join(missing_check_waves)}"
            )
    else:
        evidence_queries = []
    state["saturation"] = {
        "status": args.status,
        "note": note,
        "assessed_at": utc_now(),
        "evidence_query_ids": [query["id"] for query in evidence_queries],
    }
    save_session(path, state)
    return 0


def gate_result(path: Path) -> dict:
    state = load_session(path)
    queries = read_jsonl(path / "queries.jsonl")
    sources = read_jsonl(path / "sources.jsonl")
    claims = read_jsonl(path / "claims.jsonl")
    gaps = read_jsonl(path / "gaps.jsonl")
    anchors = read_jsonl(path / "textual-anchors.jsonl")
    reasons: list[str] = []
    actions: list[str] = []
    warnings: list[str] = []
    thresholds = state["thresholds"]

    missing_waves = [
        wave for wave in state["required_waves"] if wave not in state["completed_waves"]
    ]
    if missing_waves:
        reasons.append(f"Missing required waves: {', '.join(missing_waves)}")
        actions.append(f"Complete research waves: {', '.join(missing_waves)}")

    executed_queries = [query for query in queries if query.get("status") == "executed"]
    minimum_executed_queries = thresholds.get("min_executed_queries", 0)
    if len(executed_queries) < minimum_executed_queries:
        reasons.append(
            f"Executed queries {len(executed_queries)}/{minimum_executed_queries}"
        )
        actions.append("Run more targeted searches across the required waves")

    minimum_queries_per_wave = thresholds.get("min_queries_per_wave", 0)
    undersearched_waves = []
    for wave in state["required_waves"]:
        wave_query_count = sum(query.get("wave") == wave for query in executed_queries)
        if wave_query_count < minimum_queries_per_wave:
            undersearched_waves.append(f"{wave} {wave_query_count}/{minimum_queries_per_wave}")
    if undersearched_waves:
        reasons.append(f"Under-researched waves: {', '.join(undersearched_waves)}")
        actions.append("Meet the minimum query depth in every required wave")

    opened_sources = [
        source
        for source in sources
        if source.get("opened") and source.get("status") == "usable"
    ]
    qualified_sources = [
        source
        for source in opened_sources
        if source.get("quality", "medium") != "low"
        and (
            source.get("independent")
            or source.get("unique_value")
            or source.get("reading_depth") == "deep"
            or source.get("source_type") in AUTHORITATIVE_SOURCE_TYPES
        )
    ]
    qualified_source_units = round(sum(source_units(source) for source in qualified_sources), 2)
    if len(qualified_sources) < thresholds["min_opened_sources"]:
        reasons.append(
            "Qualified usable sources "
            f"{len(qualified_sources)}/{thresholds['min_opened_sources']}"
        )
        actions.append("Add high-quality, deep-read, independent, authoritative, or uniquely valuable sources")

    minimum_source_units = thresholds.get(
        "min_source_units", float(thresholds["min_opened_sources"])
    )
    if qualified_source_units < minimum_source_units:
        reasons.append(
            f"Qualified source units {qualified_source_units}/{minimum_source_units}"
        )
        actions.append("Add deeper or more authoritative sources with material evidence value")

    target_opened_sources = thresholds.get("target_opened_sources", thresholds["min_opened_sources"])
    target_source_units = thresholds.get("target_source_units", float(target_opened_sources))
    saturation = state.get("saturation", {"status": "not_assessed"})
    saturation_note = str(saturation.get("note") or "").strip()
    if saturation.get("status") != "pass" or len(saturation_note) < 60:
        reasons.append("Information saturation has not been demonstrated")
        actions.append("Continue targeted gap research, then assess information saturation")
    else:
        saturation_query_ids = set(saturation.get("evidence_query_ids") or [])
        required_check_waves = state["required_waves"][-2:]
        covered_check_waves = {
            query.get("wave")
            for query in queries
            if query.get("id") in saturation_query_ids
            and query.get("status") == "executed"
            and len(str(query.get("result_note") or "").strip()) >= 20
        }
        missing_check_waves = [
            wave for wave in required_check_waves if wave not in covered_check_waves
        ]
        if missing_check_waves:
            reasons.append(
                "Saturation lacks substantive query evidence from final waves: "
                f"{', '.join(missing_check_waves)}"
            )
            actions.append("Record result notes for targeted checks in the final research waves")
        elif len(qualified_sources) < target_opened_sources:
            warnings.append(
                f"Qualified sources {len(qualified_sources)} below dynamic target "
                f"{target_opened_sources}; accepted because saturation passed"
            )
    if saturation.get("status") == "pass" and qualified_source_units < target_source_units:
        warnings.append(
            f"Qualified source units {qualified_source_units} below dynamic target "
            f"{target_source_units}; accepted because saturation passed"
        )

    domains = {
        urlsplit(source["canonical_url"]).netloc
        for source in qualified_sources
        if source.get("canonical_url")
    }
    if len(domains) < thresholds["min_unique_domains"]:
        reasons.append(
            f"Unique source domains {len(domains)}/{thresholds['min_unique_domains']}"
        )
        actions.append("Diversify source domains")

    independent_sources = [source for source in qualified_sources if source.get("independent")]
    minimum_independent_sources = thresholds.get("min_independent_sources", 0)
    if len(independent_sources) < minimum_independent_sources:
        reasons.append(
            f"Independent sources {len(independent_sources)}/{minimum_independent_sources}"
        )
        actions.append("Add more independently produced sources")

    authoritative_sources = [
        source
        for source in qualified_sources
        if source.get("source_type") in AUTHORITATIVE_SOURCE_TYPES
    ]
    minimum_authoritative_sources = thresholds.get("min_authoritative_sources", 0)
    if len(authoritative_sources) < minimum_authoritative_sources:
        reasons.append(
            f"Authoritative sources {len(authoritative_sources)}/{minimum_authoritative_sources}"
        )
        actions.append("Add primary, official, academic, filing, or equivalent authority sources")

    covered_lanes = {source.get("lane") for source in qualified_sources if source.get("lane")}
    minimum_covered_lanes = thresholds.get("min_covered_lanes", 0)
    if len(covered_lanes) < minimum_covered_lanes:
        reasons.append(f"Covered source lanes {len(covered_lanes)}/{minimum_covered_lanes}")
        actions.append("Expand research into additional source lanes")

    missing_lanes = [lane for lane in state["required_lanes"] if lane not in covered_lanes]
    if missing_lanes:
        reasons.append(f"Missing required source lanes: {', '.join(missing_lanes)}")
        actions.append(f"Research missing lanes: {', '.join(missing_lanes)}")

    domain_counts: dict[str, int] = {}
    for source in qualified_sources:
        domain = urlsplit(source.get("canonical_url", "")).netloc
        if domain:
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
    maximum_domain_share = thresholds.get("max_domain_share", 1.0)
    concentrated_domains = [
        f"{domain} {count}/{len(qualified_sources)}"
        for domain, count in sorted(domain_counts.items())
        if qualified_sources and count / len(qualified_sources) > maximum_domain_share
    ]
    if concentrated_domains:
        reasons.append(
            "Source concentration exceeds domain-share limit: "
            f"{', '.join(concentrated_domains)}"
        )
        actions.append("Reduce dependence on overrepresented domains")

    usable_claims = [claim for claim in claims if claim.get("claim")]
    if len(usable_claims) < thresholds["min_claims"]:
        reasons.append(f"Claims {len(usable_claims)}/{thresholds['min_claims']}")
        actions.append("Add claim-level evidence entries")

    unsupported_major = [
        claim["id"]
        for claim in claims
        if claim.get("major")
        and not claim.get("source_ids")
        and not claim.get("anchor_ids")
    ]
    if unsupported_major:
        reasons.append(f"Unsupported major claims: {', '.join(unsupported_major)}")
        actions.append("Support or remove major claims")

    unsupported_claims = [
        claim["id"]
        for claim in claims
        if not claim.get("source_ids") and not claim.get("anchor_ids")
    ]
    if unsupported_claims:
        reasons.append(f"Claims without evidence references: {', '.join(unsupported_claims)}")
        actions.append("Attach a source or textual anchor to every claim")

    known_source_ids = {source.get("id") for source in sources}
    qualified_source_ids = {source.get("id") for source in qualified_sources}
    known_anchor_ids = {anchor.get("id") for anchor in anchors}
    unknown_source_ids = sorted(
        {
            source_id
            for claim in claims
            for source_id in claim.get("source_ids", [])
            if source_id not in known_source_ids
        }
    )
    unknown_anchor_ids = sorted(
        {
            anchor_id
            for claim in claims
            for anchor_id in claim.get("anchor_ids", [])
            if anchor_id not in known_anchor_ids
        }
    )
    if unknown_source_ids:
        reasons.append(f"Unknown source IDs in claims: {', '.join(unknown_source_ids)}")
        actions.append("Fix invalid source references")
    if unknown_anchor_ids:
        reasons.append(f"Unknown textual-anchor IDs in claims: {', '.join(unknown_anchor_ids)}")
        actions.append("Fix invalid textual-anchor references")

    unusable_source_refs = sorted(
        {
            source_id
            for claim in claims
            for source_id in claim.get("source_ids", [])
            if source_id in known_source_ids and source_id not in qualified_source_ids
        }
    )
    if unusable_source_refs:
        reasons.append(
            f"Claims reference sources that are not qualified and usable: {', '.join(unusable_source_refs)}"
        )
        actions.append("Deep-read, qualify, replace, or remove weak claim sources")

    missing_must_cover = [
        item for item in state.get("must_cover", []) if item not in state.get("covered_items", [])
    ]
    if missing_must_cover:
        reasons.append(f"Uncovered must-cover items: {', '.join(missing_must_cover)}")
        actions.append("Research and mark all must-cover items")

    open_high_gaps = [
        gap["id"]
        for gap in gaps
        if gap.get("status") != "resolved" and gap.get("impact") == "high"
    ]
    if open_high_gaps:
        reasons.append(f"Open high-impact gaps: {', '.join(open_high_gaps)}")
        actions.append("Resolve high-impact research gaps")

    failed_sources = [source for source in sources if source.get("status") == "failed"]
    if len(failed_sources) > state["budgets"]["max_failed_sources"]:
        reasons.append(
            f"Failed sources {len(failed_sources)} exceed budget "
            f"{state['budgets']['max_failed_sources']}"
        )
        actions.append("Change retrieval strategy or document blocked-source limitations")

    if len(queries) > state["budgets"]["max_queries"]:
        reasons.append(
            f"Queries {len(queries)} exceed budget {state['budgets']['max_queries']}"
        )

    minimum_anchors = thresholds["min_textual_anchors"]
    if len(anchors) < minimum_anchors:
        reasons.append(f"Textual anchors {len(anchors)}/{minimum_anchors}")
        actions.append("Add primary-text close-reading anchors")

    missing_section_evidence = []
    for section in state["planned_sections"]:
        if not any(claim.get("section") == section for claim in claims):
            missing_section_evidence.append(section)
    if missing_section_evidence:
        reasons.append(
            f"Sections without claim evidence: {', '.join(missing_section_evidence)}"
        )
        actions.append("Assign evidence to every planned section")

    suspicious_used_sources = {
        source["id"]
        for source in sources
        if source.get("prompt_injection_suspected")
    }
    claims_using_suspicious_sources = [
        claim["id"]
        for claim in claims
        if suspicious_used_sources.intersection(claim.get("source_ids", []))
    ]
    if claims_using_suspicious_sources:
        reasons.append(
            "Claims use prompt-injection-suspected sources: "
            f"{', '.join(claims_using_suspicious_sources)}"
        )
        actions.append("Replace or independently verify suspicious-source claims")

    status = "pass" if not reasons else "fail"
    return {
        "status": status,
        "checked_at": utc_now(),
        "reasons": reasons,
        "warnings": warnings,
        "next_actions": list(dict.fromkeys(actions)),
        "metrics": {
            "queries": len(queries),
            "executed_queries": len(executed_queries),
            "opened_usable_sources": len(opened_sources),
            "qualified_usable_sources": len(qualified_sources),
            "target_qualified_sources": target_opened_sources,
            "qualified_source_units": qualified_source_units,
            "target_source_units": target_source_units,
            "saturation_status": saturation.get("status", "not_assessed"),
            "unique_domains": len(domains),
            "independent_sources": len(independent_sources),
            "authoritative_sources": len(authoritative_sources),
            "covered_lanes": sorted(covered_lanes),
            "claims": len(usable_claims),
            "textual_anchors": len(anchors),
            "open_high_impact_gaps": len(open_high_gaps),
        },
    }


def complete_stage_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    ensure_workflow_state(state)
    expected = next_workflow_stage(state)
    if expected is None:
        raise SystemExit("All workflow stages are already complete. Run workflow-gate.")
    if args.stage != expected:
        expected_skill = WORKFLOW_STAGE_BY_NAME[expected]["skill"]
        raise SystemExit(
            f"Cannot complete '{args.stage}' yet. Next required stage is "
            f"'{expected}' using {expected_skill}."
        )

    stage = WORKFLOW_STAGE_BY_NAME[args.stage]
    artifact = path / stage["artifact"]
    if not nonempty_markdown(artifact):
        raise SystemExit(
            f"Workflow stage '{args.stage}' requires a substantive {stage['artifact']} artifact."
        )
    if args.stage == "brief_confirmed":
        clarifications = read_jsonl(path / "clarifications.jsonl")
        if len(clarifications) < 3:
            raise SystemExit(
                "brief_confirmed requires at least 3 recorded clarifications."
            )
        dimensions = {
            record.get("normalized_dimension")
            or normalize_text(str(record.get("dimension", "")))
            for record in clarifications
            if str(record.get("dimension", "")).strip()
        }
        if len(dimensions) < 3:
            raise SystemExit(
                "brief_confirmed requires clarification questions from at least "
                "3 distinct dimensions."
            )
        if not any(
            record.get("question_form") == "open" for record in clarifications
        ):
            raise SystemExit(
                "brief_confirmed requires at least 1 genuinely open clarification question."
            )
    if args.stage == "insight_audit" and not insight_audit_passes(artifact):
        raise SystemExit(
            "insight_audit requires Status: pass and completed originality, alternative, "
            "counterevidence, and revision fields."
        )

    evidence = gate_result(path)
    if stage["requires_evidence_gate"] and evidence["status"] != "pass":
        raise SystemExit(
            f"Workflow stage '{args.stage}' requires a passing evidence gate. "
            f"Next actions: {'; '.join(evidence['next_actions'])}"
        )
    if args.stage == "insight_outline" and not state.get("planned_sections"):
        raise SystemExit(
            "The insight-architect stage requires planned sections. Add them with add-section."
        )

    note = args.note.strip()
    if len(note) < 40:
        raise SystemExit(
            "Stage note is too short. Record what the companion skill produced and checked."
        )

    researched_draft = path / "researched-draft.md"
    if args.stage == "evidence_prehumanize_audit":
        shutil.copyfile(path / "draft.md", researched_draft)
    if args.stage in {"humanized_draft", "evidence_final_audit"} and not researched_draft.exists():
        raise SystemExit(
            "Missing researched-draft.md snapshot. Re-run evidence_prehumanize_audit before humanizing."
        )

    record = {
        "stage": args.stage,
        "skill": stage["skill"],
        "artifact": stage["artifact"],
        "artifact_sha256": file_sha256(artifact),
        "note": note,
        "completed_at": utc_now(),
    }
    if args.stage == "evidence_final_audit":
        record["draft_sha256"] = file_sha256(path / "draft.md")
    if args.stage in {"evidence_prehumanize_audit", "evidence_final_audit"}:
        record["researched_draft_sha256"] = file_sha256(researched_draft)
    state["workflow"]["completed"].append(record)
    state["evidence_gate"] = evidence["status"]
    update_workflow_status(state, evidence["status"])
    save_session(path, state)
    append_jsonl(path / "stage-log.jsonl", record)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def workflow_gate_result(path: Path) -> dict:
    state = load_session(path)
    workflow = ensure_workflow_state(state)
    evidence = gate_result(path)
    completed = completed_stage_names(state)
    completed_set = set(completed)
    required_skills = {
        WORKFLOW_STAGE_BY_NAME[name]["skill"]
        for name in workflow["required_stages"]
        if name in WORKFLOW_STAGE_BY_NAME
    }
    completed_skills = {
        record.get("skill") for record in workflow["completed"] if record.get("skill")
    }
    reasons: list[str] = []
    actions: list[str] = []

    if evidence["status"] != "pass":
        reasons.append("Evidence gate is not currently passing")
        actions.extend(evidence["next_actions"])

    missing = [name for name in workflow["required_stages"] if name not in completed_set]
    if missing:
        reasons.append(f"Missing workflow stages: {', '.join(missing)}")
        next_missing = missing[0]
        actions.append(
            f"Load {WORKFLOW_STAGE_BY_NAME[next_missing]['skill']} and complete "
            f"workflow stage '{next_missing}'"
        )

    stage_skill_mismatches = [
        f"{record.get('stage')}:{record.get('skill')}"
        for record in workflow["completed"]
        if record.get("stage") in WORKFLOW_STAGE_BY_NAME
        and record.get("skill") != WORKFLOW_STAGE_BY_NAME[record["stage"]]["skill"]
    ]
    if stage_skill_mismatches:
        reasons.append(
            f"Workflow stages recorded with the wrong skill: {', '.join(stage_skill_mismatches)}"
        )
        actions.append("Re-complete the affected stages with their required companion skill")

    incomplete_artifacts = []
    changed_artifacts = []
    for record in workflow["completed"]:
        stage_name = record.get("stage")
        stage = WORKFLOW_STAGE_BY_NAME.get(stage_name)
        if not stage:
            continue
        artifact = path / stage["artifact"]
        if not nonempty_markdown(artifact):
            incomplete_artifacts.append(f"{stage_name}:{stage['artifact']}")
        elif (
            stage_name not in MUTABLE_WORKFLOW_ARTIFACT_STAGES
            and record.get("artifact_sha256")
            and record["artifact_sha256"] != file_sha256(artifact)
        ):
            changed_artifacts.append(f"{stage_name}:{stage['artifact']}")
    if incomplete_artifacts:
        reasons.append(
            f"Completed stages have empty artifacts: {', '.join(incomplete_artifacts)}"
        )
        actions.append("Restore substantive stage artifacts and re-complete invalid stages")
    if changed_artifacts:
        reasons.append(
            f"Stage artifacts changed after completion: {', '.join(changed_artifacts)}"
        )
        actions.append("Re-run the affected companion skill and re-complete downstream stages")

    researched_draft = path / "researched-draft.md"
    prehumanize_records = [
        record
        for record in workflow["completed"]
        if record.get("stage") == "evidence_prehumanize_audit"
    ]
    if prehumanize_records:
        expected_researched_hash = prehumanize_records[-1].get("researched_draft_sha256")
        if (
            not researched_draft.exists()
            or not expected_researched_hash
            or expected_researched_hash != file_sha256(researched_draft)
        ):
            reasons.append("Researched draft snapshot changed after the pre-humanize audit")
            actions.append("Restore the researched draft and re-run the pre-humanize audit")

    final_records = [
        record
        for record in workflow["completed"]
        if record.get("stage") == "evidence_final_audit"
    ]
    if final_records:
        final_draft_hash = final_records[-1].get("draft_sha256")
        if not final_draft_hash or final_draft_hash != file_sha256(path / "draft.md"):
            reasons.append("Draft changed after the final evidence audit")
            actions.append("Run evidence-auditor again and re-complete evidence_final_audit")
        final_researched_hash = final_records[-1].get("researched_draft_sha256")
        if (
            not researched_draft.exists()
            or not final_researched_hash
            or final_researched_hash != file_sha256(researched_draft)
        ):
            reasons.append("Researched draft snapshot changed after the final evidence audit")
            actions.append("Restore the snapshot and re-run evidence_final_audit")

    status = "pass" if not reasons else "fail"
    return {
        "status": status,
        "checked_at": utc_now(),
        "reasons": reasons,
        "next_actions": list(dict.fromkeys(actions)),
        "metrics": {
            "completed_stages": len(completed_set),
            "required_stages": len(workflow["required_stages"]),
            "next_stage": next_workflow_stage(state),
            "evidence_gate": evidence["status"],
            "completed_skills": sorted(completed_skills),
            "required_skills": sorted(required_skills),
            "missing_skills": sorted(required_skills - completed_skills),
        },
    }


def gate_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    result = gate_result(path)
    write_json(path / "audit.json", result)
    state = load_session(path)
    state["evidence_gate"] = result["status"]
    state["gate_reasons"] = result["reasons"]
    state["next_actions"] = result["next_actions"]
    if result["status"] == "pass":
        update_workflow_status(state, result["status"])
    else:
        invalidate_workflow_from(state, "evidence_preoutline_audit")
        state["status"] = "researching"
    save_session(path, state)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 4


def workflow_gate_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    result = workflow_gate_result(path)
    write_json(path / "workflow-audit.json", result)
    state = load_session(path)
    if result["status"] == "pass":
        state["status"] = "complete"
    else:
        update_workflow_status(state, result["metrics"]["evidence_gate"])
    state["next_actions"] = result["next_actions"]
    save_session(path, state)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 5


def status_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    result = gate_result(path)
    state = load_session(path)
    workflow = workflow_gate_result(path)
    output = {
        "title": state["title"],
        "status": state["status"],
        "depth_profile": state["depth_profile"],
        "current_wave": state["current_wave"],
        "completed_waves": state["completed_waves"],
        "clarifications": len(read_jsonl(path / "clarifications.jsonl")),
        "evidence_gate": result["status"],
        "workflow_gate": workflow["status"],
        "completed_workflow_stages": completed_stage_names(state),
        "next_workflow_stage": next_workflow_stage(state),
        "metrics": result["metrics"],
        "warnings": result["warnings"],
        "next_actions": workflow["next_actions"] or result["next_actions"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def resume_command(args: argparse.Namespace) -> int:
    path = session_dir(args.session)
    state = load_session(path)
    next_stage = next_workflow_stage(state)
    if next_stage in {"brief_confirmed", "research_plan"}:
        stage = WORKFLOW_STAGE_BY_NAME[next_stage]
        print(
            f"Load {stage['skill']} and complete workflow stage '{next_stage}' "
            f"using {stage['artifact']}."
        )
        return 4
    result = gate_result(path)
    if result["status"] != "pass":
        actions = result["next_actions"]
    elif next_stage is not None:
        stage = WORKFLOW_STAGE_BY_NAME[next_stage]
        actions = [
            f"Load {stage['skill']} and complete workflow stage '{next_stage}' "
            f"using {stage['artifact']}"
        ]
    else:
        workflow = workflow_gate_result(path)
        if workflow["status"] == "pass":
            print("Workflow gate passed. The researched deliverable is complete.")
            return 0
        actions = workflow["next_actions"]
    for index, action in enumerate(actions, 1):
        print(f"{index}. {action}")
    return 4


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a persistent research session.")
    init_parser.add_argument("--session", required=True)
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--task-mode", default="general_research")
    init_parser.add_argument("--depth", choices=DEPTH_PROFILES, default="deep")
    init_parser.add_argument("--required-lane", action="append")
    init_parser.add_argument("--must-cover", action="append")
    init_parser.add_argument("--max-queries", type=int)
    init_parser.add_argument("--max-failed-sources", type=int)
    init_parser.add_argument("--min-executed-queries", type=int)
    init_parser.add_argument("--min-queries-per-wave", type=int)
    init_parser.add_argument("--min-opened-sources", type=int)
    init_parser.add_argument("--target-opened-sources", type=int)
    init_parser.add_argument("--min-source-units", type=float)
    init_parser.add_argument("--target-source-units", type=float)
    init_parser.add_argument("--min-unique-domains", type=int)
    init_parser.add_argument("--min-independent-sources", type=int)
    init_parser.add_argument("--min-authoritative-sources", type=int)
    init_parser.add_argument("--min-covered-lanes", type=int)
    init_parser.add_argument("--max-domain-share", type=float)
    init_parser.add_argument("--min-claims", type=int)
    init_parser.add_argument("--min-textual-anchors", type=int)
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=init_command)

    clarification_parser = subparsers.add_parser(
        "add-clarification", help="Record one dynamic clarification and answer."
    )
    clarification_parser.add_argument("--session", required=True)
    clarification_parser.add_argument("--question", required=True)
    clarification_parser.add_argument("--answer", required=True)
    clarification_parser.add_argument(
        "--anchor",
        help="Optional prompt-, chat-, outline-, or material-specific anchor.",
    )
    clarification_parser.add_argument("--dimension", required=True)
    clarification_parser.add_argument("--impact", required=True)
    clarification_parser.add_argument(
        "--question-form",
        choices=("open", "choice", "confirmation"),
        required=True,
    )
    clarification_parser.set_defaults(func=add_clarification_command)

    query_parser = subparsers.add_parser("add-query", help="Log a unique research query.")
    query_parser.add_argument("--session", required=True)
    query_parser.add_argument("--query", required=True)
    query_parser.add_argument("--wave", required=True)
    query_parser.add_argument("--lane")
    query_parser.add_argument(
        "--status", choices=("planned", "executed", "failed"), default="executed"
    )
    query_parser.add_argument("--result-note")
    query_parser.set_defaults(func=add_query_command)

    source_parser = subparsers.add_parser("add-source", help="Log and canonicalize a source.")
    source_parser.add_argument("--session", required=True)
    source_parser.add_argument("--url", required=True)
    source_parser.add_argument("--title", required=True)
    source_parser.add_argument("--publisher")
    source_parser.add_argument("--published-date")
    source_parser.add_argument("--lane", required=True)
    source_parser.add_argument("--source-type", required=True)
    source_parser.add_argument(
        "--quality", choices=("high", "medium", "low"), default="medium"
    )
    source_parser.add_argument(
        "--reading-depth", choices=("skim", "read", "deep"), default="read"
    )
    source_parser.add_argument("--relevance")
    source_parser.add_argument(
        "--status", choices=("usable", "failed", "rejected"), default="usable"
    )
    source_parser.add_argument("--opened", action="store_true")
    source_parser.add_argument("--independent", action="store_true")
    source_parser.add_argument("--unique-value", action="store_true")
    source_parser.add_argument("--prompt-injection-suspected", action="store_true")
    source_parser.set_defaults(func=add_source_command)

    update_source_parser = subparsers.add_parser(
        "update-source", help="Correct source assessment fields."
    )
    update_source_parser.add_argument("--session", required=True)
    update_source_parser.add_argument("--source-id", required=True)
    update_source_parser.add_argument(
        "--status", choices=("usable", "failed", "rejected")
    )
    update_source_parser.add_argument(
        "--opened", action=argparse.BooleanOptionalAction, default=None
    )
    update_source_parser.add_argument(
        "--prompt-injection-suspected",
        action=argparse.BooleanOptionalAction,
        default=None,
    )
    update_source_parser.add_argument("--relevance")
    update_source_parser.add_argument("--quality", choices=("high", "medium", "low"))
    update_source_parser.add_argument(
        "--reading-depth", choices=("skim", "read", "deep")
    )
    update_source_parser.add_argument(
        "--unique-value", action=argparse.BooleanOptionalAction, default=None
    )
    update_source_parser.add_argument(
        "--independent", action=argparse.BooleanOptionalAction, default=None
    )
    update_source_parser.set_defaults(func=update_source_command)

    claim_parser = subparsers.add_parser("add-claim", help="Log a claim and its evidence.")
    claim_parser.add_argument("--session", required=True)
    claim_parser.add_argument("--claim", required=True)
    claim_parser.add_argument(
        "--kind", choices=("fact", "interpretation", "forecast"), default="fact"
    )
    claim_parser.add_argument(
        "--confidence", choices=("high", "medium", "low"), default="medium"
    )
    claim_parser.add_argument("--major", action="store_true")
    claim_parser.add_argument("--source-id", action="append")
    claim_parser.add_argument("--anchor-id", action="append")
    claim_parser.add_argument("--section")
    claim_parser.add_argument("--contradiction")
    claim_parser.set_defaults(func=add_claim_command)

    update_claim_parser = subparsers.add_parser(
        "update-claim", help="Correct a claim and replace its evidence references."
    )
    update_claim_parser.add_argument("--session", required=True)
    update_claim_parser.add_argument("--claim-id", required=True)
    update_claim_parser.add_argument("--claim")
    update_claim_parser.add_argument(
        "--kind", choices=("fact", "interpretation", "forecast")
    )
    update_claim_parser.add_argument(
        "--confidence", choices=("high", "medium", "low")
    )
    update_claim_parser.add_argument(
        "--major", action=argparse.BooleanOptionalAction, default=None
    )
    update_claim_parser.add_argument("--source-id", action="append")
    update_claim_parser.add_argument("--anchor-id", action="append")
    update_claim_parser.add_argument("--section")
    update_claim_parser.add_argument("--contradiction")
    update_claim_parser.set_defaults(func=update_claim_command)
    gap_parser = subparsers.add_parser("add-gap", help="Log an unresolved research gap.")
    gap_parser.add_argument("--session", required=True)
    gap_parser.add_argument("--question", required=True)
    gap_parser.add_argument("--impact", choices=("high", "medium", "low"), default="medium")
    gap_parser.add_argument("--status", choices=("open", "blocked"), default="open")
    gap_parser.add_argument("--next-query")
    gap_parser.set_defaults(func=add_gap_command)

    resolve_parser = subparsers.add_parser("resolve-gap", help="Resolve a research gap.")
    resolve_parser.add_argument("--session", required=True)
    resolve_parser.add_argument("--gap-id", required=True)
    resolve_parser.add_argument("--resolution", required=True)
    resolve_parser.set_defaults(func=resolve_gap_command)

    anchor_parser = subparsers.add_parser(
        "add-anchor", help="Log a primary-text or close-reading anchor."
    )
    anchor_parser.add_argument("--session", required=True)
    anchor_parser.add_argument("--location", required=True)
    anchor_parser.add_argument("--feature", required=True)
    anchor_parser.add_argument("--observation", required=True)
    anchor_parser.add_argument("--interpretation")
    anchor_parser.add_argument("--alternative-reading")
    anchor_parser.add_argument("--section")
    anchor_parser.set_defaults(func=add_anchor_command)

    wave_parser = subparsers.add_parser("complete-wave", help="Mark a research wave complete.")
    wave_parser.add_argument("--session", required=True)
    wave_parser.add_argument("--wave", required=True)
    wave_parser.set_defaults(func=complete_wave_command)

    section_parser = subparsers.add_parser("add-section", help="Add a planned report section.")
    section_parser.add_argument("--session", required=True)
    section_parser.add_argument("--section", required=True)
    section_parser.set_defaults(func=add_section_command)

    cover_parser = subparsers.add_parser("cover-item", help="Mark a must-cover item covered.")
    cover_parser.add_argument("--session", required=True)
    cover_parser.add_argument("--item", required=True)
    cover_parser.set_defaults(func=cover_item_command)

    saturation_parser = subparsers.add_parser(
        "assess-saturation", help="Record whether further research is materially useful."
    )
    saturation_parser.add_argument("--session", required=True)
    saturation_parser.add_argument("--status", choices=("pass", "continue"), required=True)
    saturation_parser.add_argument("--note", required=True)
    saturation_parser.set_defaults(func=assess_saturation_command)

    stage_parser = subparsers.add_parser(
        "complete-stage",
        help="Record one ordered companion-skill workflow stage.",
    )
    stage_parser.add_argument("--session", required=True)
    stage_parser.add_argument("--stage", choices=WORKFLOW_STAGE_NAMES, required=True)
    stage_parser.add_argument("--note", required=True)
    stage_parser.set_defaults(func=complete_stage_command)

    for command, help_text, func in (
        ("gate", "Run the hard evidence gate.", gate_command),
        ("workflow-gate", "Verify the full seven-skill workflow.", workflow_gate_command),
        ("status", "Show research progress and gate status.", status_command),
        ("resume", "Print the next required research actions.", resume_command),
    ):
        command_parser = subparsers.add_parser(command, help=help_text)
        command_parser.add_argument("--session", required=True)
        command_parser.set_defaults(func=func)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
