from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "research_session.py"
SPEC = importlib.util.spec_from_file_location("research_session", SCRIPT)
research_session = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(research_session)


class ResearchSessionTests(unittest.TestCase):
    def complete_stage(self, session: Path, stage: str, note: str) -> None:
        args = research_session.build_parser().parse_args(
            [
                "complete-stage",
                "--session",
                str(session),
                "--stage",
                stage,
                "--note",
                note,
            ]
        )
        self.assertEqual(args.func(args), 0)

    def complete_opening_stages(self, session: Path) -> None:
        parser = research_session.build_parser()
        for index, dimension in enumerate(("object", "angle", "scope")):
            args = parser.parse_args(
                [
                    "add-clarification",
                    "--session",
                    str(session),
                    "--dimension",
                    dimension,
                    "--impact",
                    f"This answer changes research decision {index + 1}.",
                    "--question-form",
                    "open" if index == 0 else "choice",
                    "--question",
                    f"Material question {index + 1}?",
                    "--answer",
                    f"Substantive answer {index + 1}.",
                ]
            )
            self.assertEqual(args.func(args), 0)
        (session / "brief.md").write_text(
            "# Research Brief\n\nConfirmed scope, audience, deliverable, and source rules.\n",
            encoding="utf-8",
        )
        (session / "research-plan.md").write_text(
            "# Research Plan\n\nUse multiple source lanes, waves, gap checks, and verification.\n",
            encoding="utf-8",
        )
        for stage, note in (
            (
                "brief_confirmed",
                "Confirmed the binding scope, audience, deliverable, voice, and source constraints.",
            ),
            (
                "research_plan",
                "Loaded research-orchestrator and defined lanes, waves, gaps, verification, and stop conditions.",
            ),
        ):
            self.complete_stage(session, stage, note)

    def test_canonicalize_url_removes_tracking(self) -> None:
        actual = research_session.canonicalize_url(
            "https://Example.com/article/?utm_source=x&b=2&a=1#fragment"
        )
        self.assertEqual(actual, "https://example.com/article?a=1&b=2")

    def test_gate_fails_empty_deep_session(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            args = research_session.build_parser().parse_args(
                [
                    "init",
                    "--session",
                    str(session),
                    "--title",
                    "Test",
                    "--task-mode",
                    "cultural_criticism",
                    "--depth",
                    "deep",
                    "--required-lane",
                    "primary_text",
                ]
            )
            self.assertEqual(args.func(args), 0)
            result = research_session.gate_result(session)
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("Missing required waves" in item for item in result["reasons"]))
            self.assertTrue(any("Textual anchors" in item for item in result["reasons"]))

    def test_force_init_clears_stale_figures(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "First", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            stale = session / "figures" / "stale.csv"
            stale.write_text("private,old,data\n", encoding="utf-8")
            force_args = parser.parse_args(
                [
                    "init",
                    "--session",
                    str(session),
                    "--title",
                    "Second",
                    "--depth",
                    "light",
                    "--force",
                ]
            )
            self.assertEqual(force_args.func(force_args), 0)
            self.assertFalse(stale.exists())

    def test_gate_rejects_unopened_claim_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            session.mkdir()
            state = {
                "schema_version": 1,
                "title": "Test",
                "task_mode": "general_research",
                "depth_profile": "light",
                "status": "researching",
                "created_at": research_session.utc_now(),
                "updated_at": research_session.utc_now(),
                "current_wave": None,
                "completed_waves": [],
                "required_waves": [],
                "required_lanes": [],
                "must_cover": [],
                "covered_items": [],
                "planned_sections": [],
                "budgets": {"max_queries": 5, "max_failed_sources": 2},
                "thresholds": {
                    "min_executed_queries": 0,
                    "min_queries_per_wave": 0,
                    "min_opened_sources": 0,
                    "target_opened_sources": 0,
                    "min_unique_domains": 0,
                    "min_independent_sources": 0,
                    "min_authoritative_sources": 0,
                    "min_covered_lanes": 0,
                    "max_domain_share": 1.0,
                    "min_claims": 1,
                    "min_textual_anchors": 0,
                },
                "evidence_gate": "not_run",
                "gate_reasons": [],
                "next_actions": [],
                "saturation": {"status": "pass", "note": "No material gaps remain."},
            }
            research_session.write_json(session / "session.json", state)
            for name in ("queries.jsonl", "gaps.jsonl", "textual-anchors.jsonl"):
                (session / name).write_text("", encoding="utf-8")
            (session / "sources.jsonl").write_text(
                json.dumps(
                    {
                        "id": "S-0001",
                        "canonical_url": "https://example.com/source",
                        "opened": False,
                        "status": "usable",
                        "source_type": "official",
                        "quality": "high",
                        "reading_depth": "deep",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (session / "claims.jsonl").write_text(
                json.dumps(
                    {
                        "id": "C-0001",
                        "claim": "Claim",
                        "major": True,
                        "source_ids": ["S-0001"],
                        "anchor_ids": [],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            result = research_session.gate_result(session)
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("not qualified and usable" in item for item in result["reasons"]))

    def test_gate_passes_configured_minimal_session(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            session.mkdir()
            state = {
                "schema_version": 1,
                "title": "Test",
                "task_mode": "general_research",
                "depth_profile": "light",
                "status": "researching",
                "created_at": research_session.utc_now(),
                "updated_at": research_session.utc_now(),
                "current_wave": None,
                "completed_waves": ["orientation"],
                "required_waves": ["orientation"],
                "required_lanes": ["official"],
                "must_cover": [],
                "covered_items": [],
                "planned_sections": ["Findings"],
                "budgets": {"max_queries": 5, "max_failed_sources": 2},
                "thresholds": {
                    "min_executed_queries": 0,
                    "min_queries_per_wave": 0,
                    "min_opened_sources": 1,
                    "target_opened_sources": 1,
                    "min_unique_domains": 1,
                    "min_independent_sources": 0,
                    "min_authoritative_sources": 1,
                    "min_covered_lanes": 1,
                    "max_domain_share": 1.0,
                    "min_claims": 1,
                    "min_textual_anchors": 0,
                },
                "evidence_gate": "not_run",
                "gate_reasons": [],
                "next_actions": [],
                "saturation": {
                    "status": "pass",
                    "note": "Targeted verification and counterpoint searches repeated existing evidence, and no unresolved high-impact gap remains.",
                    "evidence_query_ids": ["Q-0001"],
                },
            }
            research_session.write_json(session / "session.json", state)
            research_session.write_json(session / "audit.json", {})
            (session / "queries.jsonl").write_text(
                json.dumps(
                    {
                        "id": "Q-0001",
                        "query": "Targeted verification query",
                        "wave": "orientation",
                        "status": "executed",
                        "result_note": "Repeated the established evidence without a material new gap.",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (session / "gaps.jsonl").write_text("", encoding="utf-8")
            (session / "textual-anchors.jsonl").write_text("", encoding="utf-8")
            (session / "sources.jsonl").write_text(
                json.dumps(
                    {
                        "id": "S-0001",
                        "canonical_url": "https://example.com/source",
                        "lane": "official",
                        "source_type": "official",
                        "quality": "high",
                        "reading_depth": "deep",
                        "opened": True,
                        "status": "usable",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (session / "claims.jsonl").write_text(
                json.dumps(
                    {
                        "id": "C-0001",
                        "claim": "Supported claim",
                        "major": True,
                        "source_ids": ["S-0001"],
                        "anchor_ids": [],
                        "section": "Findings",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            self.assertEqual(research_session.gate_result(session)["status"], "pass")

    def test_low_quality_source_does_not_count_as_qualified(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            session.mkdir()
            state = {
                "schema_version": 1,
                "title": "Test",
                "task_mode": "general_research",
                "depth_profile": "light",
                "status": "researching",
                "created_at": research_session.utc_now(),
                "updated_at": research_session.utc_now(),
                "current_wave": None,
                "completed_waves": [],
                "required_waves": [],
                "required_lanes": [],
                "must_cover": [],
                "covered_items": [],
                "planned_sections": [],
                "budgets": {"max_queries": 5, "max_failed_sources": 2},
                "thresholds": {
                    "min_executed_queries": 0,
                    "min_queries_per_wave": 0,
                    "min_opened_sources": 1,
                    "target_opened_sources": 1,
                    "min_unique_domains": 0,
                    "min_independent_sources": 0,
                    "min_authoritative_sources": 0,
                    "min_covered_lanes": 0,
                    "max_domain_share": 1.0,
                    "min_claims": 0,
                    "min_textual_anchors": 0,
                },
                "evidence_gate": "not_run",
                "gate_reasons": [],
                "next_actions": [],
                "saturation": {"status": "pass", "note": "No material gaps remain."},
            }
            research_session.write_json(session / "session.json", state)
            for name in (
                "queries.jsonl",
                "claims.jsonl",
                "gaps.jsonl",
                "textual-anchors.jsonl",
            ):
                (session / name).write_text("", encoding="utf-8")
            (session / "sources.jsonl").write_text(
                json.dumps(
                    {
                        "id": "S-0001",
                        "canonical_url": "https://example.com/seo",
                        "lane": "commentary",
                        "source_type": "news",
                        "quality": "low",
                        "reading_depth": "skim",
                        "independent": True,
                        "opened": True,
                        "status": "usable",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            result = research_session.gate_result(session)
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["metrics"]["opened_usable_sources"], 1)
            self.assertEqual(result["metrics"]["qualified_usable_sources"], 0)

    def test_new_query_invalidates_saturation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            args = research_session.build_parser().parse_args(
                [
                    "init",
                    "--session",
                    str(session),
                    "--title",
                    "Test",
                    "--depth",
                    "light",
                ]
            )
            self.assertEqual(args.func(args), 0)
            self.complete_opening_stages(session)
            state = research_session.load_session(session)
            state["saturation"] = {
                "status": "pass",
                "note": "No material gaps remain.",
                "assessed_at": research_session.utc_now(),
            }
            research_session.save_session(session, state)
            query_args = research_session.build_parser().parse_args(
                [
                    "add-query",
                    "--session",
                    str(session),
                    "--query",
                    "new targeted query",
                    "--wave",
                    "orientation",
                ]
            )
            self.assertEqual(query_args.func(query_args), 0)
            self.assertEqual(
                research_session.load_session(session)["saturation"]["status"],
                "not_assessed",
            )

    def test_research_commands_require_research_orchestrator_stage(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "Test", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            query_args = parser.parse_args(
                [
                    "add-query",
                    "--session",
                    str(session),
                    "--query",
                    "premature query",
                    "--wave",
                    "orientation",
                ]
            )
            with self.assertRaises(SystemExit):
                query_args.func(query_args)

    def test_complete_stage_enforces_companion_skill_order(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "Test", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            (session / "research-plan.md").write_text(
                "# Research Plan\n\nA substantive research plan.\n",
                encoding="utf-8",
            )
            stage_args = parser.parse_args(
                [
                    "complete-stage",
                    "--session",
                    str(session),
                    "--stage",
                    "research_plan",
                    "--note",
                    "Loaded research-orchestrator and produced a substantive research plan.",
                ]
            )
            with self.assertRaises(SystemExit):
                stage_args.func(stage_args)

    def test_brief_accepts_distinct_production_questions_when_material(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "Test", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            for index, dimension in enumerate(("audience", "form", "citation")):
                clarification_args = parser.parse_args(
                    [
                        "add-clarification",
                        "--session",
                        str(session),
                        "--dimension",
                        dimension,
                        "--impact",
                        f"This answer changes production decision {index + 1}.",
                        "--question-form",
                        "open" if index == 0 else "confirmation",
                        "--question",
                        f"Production question {index + 1}?",
                        "--answer",
                        f"Production answer {index + 1}.",
                    ]
                )
                self.assertEqual(clarification_args.func(clarification_args), 0)
            (session / "brief.md").write_text(
                "# Brief\n\nA substantive confirmed brief.\n", encoding="utf-8"
            )
            stage_args = parser.parse_args(
                [
                    "complete-stage",
                    "--session",
                    str(session),
                    "--stage",
                    "brief_confirmed",
                    "--note",
                    "Confirmed a complete brief with scope and source constraints.",
                ]
            )
            self.assertEqual(stage_args.func(stage_args), 0)

    def test_brief_requires_distinct_task_induced_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "Test", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            for index in range(3):
                command = [
                    "add-clarification",
                    "--session",
                    str(session),
                    "--dimension",
                    "same decision",
                    "--impact",
                    f"This answer changes decision detail {index + 1}.",
                    "--question-form",
                    "open" if index == 0 else "choice",
                    "--question",
                    f"Question {index + 1}?",
                    "--answer",
                    f"Answer {index + 1}.",
                ]
                clarification_args = parser.parse_args(command)
                self.assertEqual(clarification_args.func(clarification_args), 0)
            (session / "brief.md").write_text(
                "# Brief\n\nA substantive confirmed brief.\n", encoding="utf-8"
            )
            stage_args = parser.parse_args(
                [
                    "complete-stage",
                    "--session",
                    str(session),
                    "--stage",
                    "brief_confirmed",
                    "--note",
                    "Confirmed a complete brief with scope and source constraints.",
                ]
            )
            with self.assertRaises(SystemExit):
                stage_args.func(stage_args)

    def test_brief_requires_a_genuinely_open_question(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "Test", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            for index, dimension in enumerate(("audience", "thesis", "sources")):
                clarification_args = parser.parse_args(
                    [
                        "add-clarification",
                        "--session",
                        str(session),
                        "--dimension",
                        dimension,
                        "--impact",
                        f"This answer changes material decision {index + 1}.",
                        "--question-form",
                        "choice",
                        "--question",
                        f"Choice question {index + 1}?",
                        "--answer",
                        f"Choice answer {index + 1}.",
                    ]
                )
                self.assertEqual(clarification_args.func(clarification_args), 0)
            (session / "brief.md").write_text(
                "# Brief\n\nA substantive confirmed brief.\n", encoding="utf-8"
            )
            stage_args = parser.parse_args(
                [
                    "complete-stage",
                    "--session",
                    str(session),
                    "--stage",
                    "brief_confirmed",
                    "--note",
                    "Confirmed a complete brief with scope and source constraints.",
                ]
            )
            with self.assertRaises(SystemExit):
                stage_args.func(stage_args)

    def test_brief_requires_three_clarifications(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "Test", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            (session / "brief.md").write_text(
                "# Brief\n\nA substantive confirmed brief.\n", encoding="utf-8"
            )
            stage_args = parser.parse_args(
                [
                    "complete-stage",
                    "--session",
                    str(session),
                    "--stage",
                    "brief_confirmed",
                    "--note",
                    "Confirmed a complete brief with scope and source constraints.",
                ]
            )
            with self.assertRaises(SystemExit):
                stage_args.func(stage_args)

    def test_clarification_requires_decision_impact(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "Test", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            clarification_args = parser.parse_args(
                [
                    "add-clarification",
                    "--session",
                    str(session),
                    "--dimension",
                    "tension",
                    "--impact",
                    "Too short",
                    "--question-form",
                    "open",
                    "--question",
                    "Which contradiction should lead the analysis?",
                    "--answer",
                    "The contradiction in the central relationship.",
                ]
            )
            with self.assertRaises(SystemExit):
                clarification_args.func(clarification_args)

    def test_workflow_gate_rejects_skipped_companion_stages(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "Test", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            self.complete_opening_stages(session)
            result = research_session.workflow_gate_result(session)
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("Missing workflow stages" in item for item in result["reasons"]))

    def test_workflow_requires_visualization_review(self) -> None:
        self.assertIn("visualization_review", research_session.WORKFLOW_STAGE_NAMES)
        stage = research_session.WORKFLOW_STAGE_BY_NAME["visualization_review"]
        self.assertEqual(stage["skill"], "research-visualizer")
        self.assertEqual(stage["artifact"], "visuals.md")

    def test_workflow_gate_detects_draft_change_after_final_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            session.mkdir()
            draft = session / "draft.md"
            draft.write_text("# Draft\n\nAudited final draft.\n", encoding="utf-8")
            researched_draft = session / "researched-draft.md"
            researched_draft.write_text(
                "# Draft\n\nResearched draft before prose editing.\n", encoding="utf-8"
            )
            (session / "final-audit.md").write_text(
                "# Final Evidence Audit\n\nAll current claims and citations were checked.\n",
                encoding="utf-8",
            )
            state = {
                "schema_version": 2,
                "title": "Test",
                "task_mode": "general_research",
                "depth_profile": "light",
                "status": "complete",
                "created_at": research_session.utc_now(),
                "updated_at": research_session.utc_now(),
                "current_wave": None,
                "completed_waves": [],
                "required_waves": [],
                "required_lanes": [],
                "must_cover": [],
                "covered_items": [],
                "planned_sections": [],
                "budgets": {"max_queries": 5, "max_failed_sources": 2},
                "thresholds": {
                    "min_executed_queries": 0,
                    "min_queries_per_wave": 0,
                    "min_opened_sources": 0,
                    "target_opened_sources": 0,
                    "min_source_units": 0,
                    "target_source_units": 0,
                    "min_unique_domains": 0,
                    "min_independent_sources": 0,
                    "min_authoritative_sources": 0,
                    "min_covered_lanes": 0,
                    "max_domain_share": 1.0,
                    "min_claims": 0,
                    "min_textual_anchors": 0,
                },
                "evidence_gate": "pass",
                "gate_reasons": [],
                "next_actions": [],
                "saturation": {
                    "status": "pass",
                    "note": "Targeted verification searches repeated existing evidence and no high-impact gaps remain.",
                },
                "workflow": {
                    "required_stages": ["evidence_final_audit"],
                    "completed": [
                        {
                            "stage": "evidence_final_audit",
                            "skill": "evidence-auditor",
                            "artifact": "final-audit.md",
                            "draft_sha256": research_session.file_sha256(draft),
                            "researched_draft_sha256": research_session.file_sha256(
                                researched_draft
                            ),
                        }
                    ],
                },
            }
            research_session.write_json(session / "session.json", state)
            for name in (
                "queries.jsonl",
                "sources.jsonl",
                "claims.jsonl",
                "gaps.jsonl",
                "textual-anchors.jsonl",
            ):
                (session / name).write_text("", encoding="utf-8")
            self.assertEqual(research_session.workflow_gate_result(session)["status"], "pass")
            draft.write_text("# Draft\n\nChanged after audit.\n", encoding="utf-8")
            result = research_session.workflow_gate_result(session)
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("changed after" in item for item in result["reasons"]))

    def test_full_ordered_six_skill_workflow_can_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            parser = research_session.build_parser()
            init_args = parser.parse_args(
                ["init", "--session", str(session), "--title", "Test", "--depth", "light"]
            )
            self.assertEqual(init_args.func(init_args), 0)
            self.complete_opening_stages(session)

            state = research_session.load_session(session)
            state["required_waves"] = []
            for key in (
                "min_executed_queries",
                "min_queries_per_wave",
                "min_opened_sources",
                "target_opened_sources",
                "min_source_units",
                "target_source_units",
                "min_unique_domains",
                "min_independent_sources",
                "min_authoritative_sources",
                "min_covered_lanes",
                "min_claims",
                "min_textual_anchors",
            ):
                state["thresholds"][key] = 0
            state["thresholds"]["max_domain_share"] = 1.0
            research_session.save_session(session, state)

            anchor_args = parser.parse_args(
                [
                    "add-anchor",
                    "--session",
                    str(session),
                    "--location",
                    "Chapter 1",
                    "--feature",
                    "motif",
                    "--observation",
                    "A recurring image establishes the central tension.",
                    "--section",
                    "Findings",
                ]
            )
            self.assertEqual(anchor_args.func(anchor_args), 0)
            claim_args = parser.parse_args(
                [
                    "add-claim",
                    "--session",
                    str(session),
                    "--claim",
                    "The recurring image establishes the central tension.",
                    "--kind",
                    "interpretation",
                    "--anchor-id",
                    "A-0001",
                    "--section",
                    "Findings",
                ]
            )
            self.assertEqual(claim_args.func(claim_args), 0)
            saturation_args = parser.parse_args(
                [
                    "assess-saturation",
                    "--session",
                    str(session),
                    "--status",
                    "pass",
                    "--note",
                    "Targeted authority, detail, counterpoint, and verification searches repeated existing evidence and left no high-impact gaps.",
                ]
            )
            self.assertEqual(saturation_args.func(saturation_args), 0)

            artifacts = {
                "evidence_preoutline_audit": "pre-outline-audit.md",
                "insight_outline": "outline.md",
                "insight_audit": "insight-audit.md",
                "evidence_predraft_audit": "pre-draft-audit.md",
                "visualization_review": "visuals.md",
                "style_sheet": "style-sheet.md",
                "continuity_ready": "continuity.md",
                "draft_complete": "draft.md",
                "evidence_prehumanize_audit": "pre-humanize-audit.md",
                "humanized_draft": "draft.md",
                "evidence_final_audit": "final-audit.md",
            }
            (session / artifacts["evidence_preoutline_audit"]).write_text(
                "# Audit\n\nEvidence supports moving to outline.\n", encoding="utf-8"
            )
            self.complete_stage(
                session,
                "evidence_preoutline_audit",
                "Loaded evidence-auditor and verified the claim ledger before outlining.",
            )
            section_args = parser.parse_args(
                ["add-section", "--session", str(session), "--section", "Findings"]
            )
            self.assertEqual(section_args.func(section_args), 0)

            for stage in research_session.WORKFLOW_STAGE_NAMES[3:]:
                artifact = session / artifacts[stage]
                if stage == "insight_audit":
                    artifact.write_text(
                        "# Insight Audit\n\nStatus: pass\nOriginal contribution: A specific synthesis.\nStrongest conventional alternative: The dominant reading.\nCounterevidence: A material contrary example.\nRequired revisions: none\n",
                        encoding="utf-8",
                    )
                elif stage == "humanized_draft":
                    artifact.write_text(
                        "# Draft\n\nHumanized researched draft with preserved evidence.\n",
                        encoding="utf-8",
                    )
                else:
                    artifact.write_text(
                        f"# {stage}\n\nSubstantive artifact produced for {stage}.\n",
                        encoding="utf-8",
                    )
                self.complete_stage(
                    session,
                    stage,
                    f"Loaded {research_session.WORKFLOW_STAGE_BY_NAME[stage]['skill']} and completed the required {stage} checks.",
                )

            workflow = research_session.workflow_gate_result(session)
            self.assertEqual(workflow["status"], "pass")
            self.assertIn(
                "Substantive artifact produced for draft_complete.",
                (session / "researched-draft.md").read_text(encoding="utf-8"),
            )
            self.assertNotEqual(
                (session / "researched-draft.md").read_text(encoding="utf-8"),
                (session / "draft.md").read_text(encoding="utf-8"),
            )
            (session / "outline.md").write_text(
                "# Outline\n\nChanged after the insight stage was recorded.\n",
                encoding="utf-8",
            )
            workflow = research_session.workflow_gate_result(session)
            self.assertEqual(workflow["status"], "fail")
            self.assertTrue(any("Stage artifacts changed" in item for item in workflow["reasons"]))

    def test_profiles_use_dynamic_targets_without_hard_fifty_source_floor(self) -> None:
        self.assertLess(
            research_session.DEPTH_PROFILES["exhaustive"]["min_opened_sources"],
            50,
        )
        self.assertGreater(
            research_session.DEPTH_PROFILES["exhaustive"]["target_opened_sources"],
            research_session.DEPTH_PROFILES["exhaustive"]["min_opened_sources"],
        )
        self.assertGreater(
            research_session.DEPTH_PROFILES["deep"]["min_source_units"],
            research_session.DEPTH_PROFILES["deep"]["min_opened_sources"],
        )

    def test_deep_authoritative_source_has_more_evidence_units(self) -> None:
        normal = {"quality": "medium", "reading_depth": "read", "source_type": "news"}
        deep_primary = {
            "quality": "high",
            "reading_depth": "deep",
            "source_type": "primary",
            "unique_value": True,
            "independent": True,
        }
        self.assertEqual(research_session.source_units(normal), 1.0)
        self.assertEqual(research_session.source_units(deep_primary), 2.5)

    def test_saturation_requires_completed_waves_and_substantive_note(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            init_args = research_session.build_parser().parse_args(
                [
                    "init",
                    "--session",
                    str(session),
                    "--title",
                    "Test",
                    "--depth",
                    "light",
                ]
            )
            self.assertEqual(init_args.func(init_args), 0)
            short_args = research_session.build_parser().parse_args(
                [
                    "assess-saturation",
                    "--session",
                    str(session),
                    "--status",
                    "pass",
                    "--note",
                    "Enough.",
                ]
            )
            with self.assertRaises(SystemExit):
                short_args.func(short_args)
            long_args = research_session.build_parser().parse_args(
                [
                    "assess-saturation",
                    "--session",
                    str(session),
                    "--status",
                    "pass",
                    "--note",
                    "Targeted authority, detail, and verification searches repeated existing evidence and revealed no unresolved high-impact gap.",
                ]
            )
            with self.assertRaises(SystemExit):
                long_args.func(long_args)


if __name__ == "__main__":
    unittest.main()
