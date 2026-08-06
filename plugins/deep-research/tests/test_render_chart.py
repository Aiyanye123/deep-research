from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "render_chart.py"
SPEC = importlib.util.spec_from_file_location("render_chart", SCRIPT)
render_chart = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(render_chart)


class RenderChartTests(unittest.TestCase):
    def test_zero_bar_is_not_drawn_as_nonzero_and_series_have_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "data.csv"
            output = root / "chart.svg"
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerows((("year", "first", "second"), ("2025", "0", "2")))

            render_chart.render_chart(
                source=source,
                output=output,
                chart_type="bar",
                x_column="year",
                y_columns=["first", "second"],
                title="Values",
                x_label="Year",
                y_label="Value",
                source_note="Source: test",
            )

            svg = output.read_text(encoding="utf-8")
            self.assertIn('height="0.0"', svg)
            self.assertIn('fill="url(#series-0)"', svg)
            self.assertIn('fill="url(#series-1)"', svg)

    def test_line_legend_uses_series_dash_and_marker_encodings(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "data.csv"
            output = root / "chart.svg"
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerows((
                    ("year", "first", "second"),
                    ("2024", "1", "2"),
                    ("2025", "2", "3"),
                ))

            render_chart.render_chart(
                source=source,
                output=output,
                chart_type="line",
                x_column="year",
                y_columns=["first", "second"],
                title="Values",
                x_label="Year",
                y_label="Value",
                source_note="Source: test",
            )

            svg = output.read_text(encoding="utf-8")
            self.assertIn('stroke-dasharray="8 4"', svg)
            self.assertIn('<rect x="', svg)


if __name__ == "__main__":
    unittest.main()
