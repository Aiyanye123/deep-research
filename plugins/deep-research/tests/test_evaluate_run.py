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
