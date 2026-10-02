from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "evaluate_run.py"
SPEC = importlib.util.spec_from_file_location("evaluate_run", SCRIPT)
evaluate_run = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(evaluate_run)


class EvaluateRunTests(unittest.TestCase):
    def create_session(self, path: Path) -> None:
        parser = evaluate_run.research_session.build_parser()
        args = parser.parse_args(
            [
                "init",
                "--session",
                str(path),
                "--title",
                "Evaluation fixture",
                "--task-mode",
                "general_research",
                "--depth",
                "light",
            ]
        )
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(args.func(args), 0)

    def test_stale_passing_audits_do_not_override_current_gate_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            self.create_session(session)
            for name in ("audit.json", "workflow-audit.json"):
                (session / name).write_text(
                    json.dumps({"status": "pass", "reasons": []}),
                    encoding="utf-8",
                )

            result = evaluate_run.evaluate(session)

            self.assertEqual(result["structural_checks"]["evidence_gate"]["status"], "fail")
            self.assertEqual(result["structural_checks"]["workflow_gate"]["status"], "fail")

    def test_schema_four_reports_only_current_required_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            self.create_session(session)
            required_files = (
                "brief.md", "research-plan.md", "pre-outline-audit.md", "outline.md",
                "visuals.md", "draft.md", "structure-review.md", "final-audit.md",
            )
            for name in required_files:
                (session / name).write_text("# Artifact\n\nSubstantive review or writing content.\n", encoding="utf-8")

            result = evaluate_run.evaluate(session)
            artifacts = result["structural_checks"]["report_artifacts_nonempty"]
            self.assertEqual(set(artifacts), {
                "brief", "research_plan", "pre_outline_audit", "outline",
                "visuals", "draft", "structure_review", "final_audit",
            })
            self.assertTrue(all(artifacts.values()))
            for name in ("insight-audit.md", "researched-draft.md", "continuity.md"):
                self.assertFalse((session / name).exists())

    def test_legacy_schema_keeps_existing_artifact_report_names(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            self.create_session(session)
            state = evaluate_run.research_session.load_session(session)
            state["schema_version"] = 3
            state["workflow"]["required_stages"] = list(evaluate_run.research_session.LEGACY_WORKFLOW_STAGE_NAMES)
            evaluate_run.research_session.save_session(session, state)
            artifacts = evaluate_run.evaluate(session)["structural_checks"]["report_artifacts_nonempty"]
            self.assertEqual(set(artifacts), {
                "brief", "outline", "insight_audit", "researched_draft", "draft", "continuity",
            })

    def test_duplicate_anchors_are_telemetry_and_do_not_resolve_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session = Path(temp) / "session"
            self.create_session(session)
            without_anchors = evaluate_run.evaluate(session)

            anchors = [
                {"id": "anchor-1", "quote": "Repeated text", "locator": "p. 1"},
                {"id": "anchor-2", "quote": "Repeated text", "locator": "p. 1"},
            ]
            anchor_path = session / "textual-anchors.jsonl"
            anchor_path.write_text(
                "\n".join(json.dumps(anchor) for anchor in anchors) + "\n",
                encoding="utf-8",
            )
            with_duplicate_anchors = evaluate_run.evaluate(session)

            self.assertEqual(
                with_duplicate_anchors["qualitative_rubric"],
                without_anchors["qualitative_rubric"],
            )
            self.assertTrue(with_duplicate_anchors["research_review_required"])
            self.assertEqual(
                with_duplicate_anchors["activity_metrics"]["evidence_gate"]["textual_anchors"],
                2,
            )
            self.assertNotIn("overall", with_duplicate_anchors)
            self.assertNotIn("dimensions", with_duplicate_anchors)


if __name__ == "__main__":
    unittest.main()
