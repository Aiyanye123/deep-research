#!/usr/bin/env python3
"""Render accessible bar, line, or scatter charts from tidy CSV as SVG."""

from __future__ import annotations

import argparse
import csv
import html
import math
from pathlib import Path


COLORS = ("#2563eb", "#dc2626", "#059669", "#7c3aed", "#d97706", "#0891b2")
DASHES = ("", "8 4", "2 3", "10 3 2 3", "1 3", "12 4")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def svg_text(
    x: float,
    y: float,
    value: object,
    *,
    size: int = 13,
    anchor: str = "middle",
    weight: int = 400,
    rotate: int | None = None,
) -> str:
    transform = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-size="{size}" font-weight="{weight}"{transform}>{esc(value)}</text>'
    )


def marker_svg(x: float, y: float, color: str, index: int, title: str) -> str:
    shape = index % len(COLORS)
    if shape == 0:
        body = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}"/>'
    elif shape == 1:
        body = f'<rect x="{x-4.5:.1f}" y="{y-4.5:.1f}" width="9" height="9" fill="{color}"/>'
    elif shape == 2:
        body = f'<path d="M {x:.1f} {y-6:.1f} L {x+6:.1f} {y:.1f} L {x:.1f} {y+6:.1f} L {x-6:.1f} {y:.1f} Z" fill="{color}"/>'
    elif shape == 3:
        body = f'<path d="M {x:.1f} {y-6:.1f} L {x+6:.1f} {y+5:.1f} L {x-6:.1f} {y+5:.1f} Z" fill="{color}"/>'
    elif shape == 4:
        body = f'<path d="M {x-5:.1f} {y-5:.1f} L {x+5:.1f} {y+5:.1f} M {x+5:.1f} {y-5:.1f} L {x-5:.1f} {y+5:.1f}" stroke="{color}" stroke-width="3"/>'
    else:
        body = f'<path d="M {x-6:.1f} {y:.1f} L {x+6:.1f} {y:.1f} M {x:.1f} {y-6:.1f} L {x:.1f} {y+6:.1f}" stroke="{color}" stroke-width="3"/>'
    return f"<g><title>{esc(title)}</title>{body}</g>"


def pattern_svg(index: int, color: str) -> str:
    overlays = (
        "",
        '<path d="M-2 8 L8 -2 M2 10 L10 2" stroke="#ffffff" stroke-width="1.5"/>',
        '<path d="M-2 2 L8 12 M2 -2 L12 8" stroke="#ffffff" stroke-width="1.5"/>',
        '<path d="M3 0 V8" stroke="#ffffff" stroke-width="1.5"/>',
        '<path d="M0 3 H8" stroke="#ffffff" stroke-width="1.5"/>',
        '<circle cx="3" cy="3" r="1.4" fill="#ffffff"/>',
    )
    return (
        f'<pattern id="series-{index}" width="8" height="8" patternUnits="userSpaceOnUse">'
        f'<rect width="8" height="8" fill="{color}"/>{overlays[index]}</pattern>'
    )


def number(value: str, column: str, row_number: int) -> float:
    try:
        result = float(value.replace(",", "").strip())
    except (AttributeError, ValueError) as exc:
        raise SystemExit(
            f"Column '{column}' row {row_number} is not numeric: {value!r}"
        ) from exc
    if not math.isfinite(result):
        raise SystemExit(f"Column '{column}' row {row_number} is not finite.")
    return result


def read_csv(source: Path, x_column: str, y_columns: list[str]) -> list[dict[str, str]]:
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        missing = [name for name in [x_column, *y_columns] if name not in fields]
        if missing:
            raise SystemExit(f"Missing CSV columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise SystemExit("Input CSV has no data rows.")
    return rows


def render_chart(
    *,
    source: Path,
    output: Path,
    chart_type: str,
    x_column: str,
    y_columns: list[str],
    title: str,
    x_label: str,
    y_label: str,
    source_note: str,
    width: int = 960,
    height: int = 600,
) -> None:
    if chart_type not in {"bar", "line", "scatter"}:
        raise SystemExit("Chart type must be bar, line, or scatter.")
    if not y_columns:
        raise SystemExit("At least one --y column is required.")
    if len(y_columns) > len(COLORS):
        raise SystemExit(f"At most {len(COLORS)} data series are supported.")
    if width < 480 or height < 360:
        raise SystemExit("Chart dimensions must be at least 480x360.")

    rows = read_csv(source, x_column, y_columns)
    y_values = {
        column: [number(row[column], column, index) for index, row in enumerate(rows, 2)]
        for column in y_columns
    }
    categorical_x = [row[x_column].strip() for row in rows]
    numeric_x = (
        [number(row[x_column], x_column, index) for index, row in enumerate(rows, 2)]
        if chart_type == "scatter"
        else list(range(len(rows)))
    )

    legend_rows = math.ceil(len(y_columns) / 3) if len(y_columns) > 1 else 0
    left, right, top, bottom = 90, 35, 75 + legend_rows * 24, 105
    plot_width = width - left - right
    plot_height = height - top - bottom
    flat_y = [value for values in y_values.values() for value in values]
    y_min = min(0.0, min(flat_y)) if chart_type == "bar" else min(flat_y)
    y_max = max(0.0, max(flat_y)) if chart_type == "bar" else max(flat_y)
    if y_min == y_max:
        y_min -= 1
        y_max += 1
    else:
        padding = (y_max - y_min) * 0.08
        if chart_type != "bar":
            y_min -= padding
            y_max += padding

    x_min, x_max = min(numeric_x), max(numeric_x)
    if x_min == x_max:
        x_min -= 1
        x_max += 1

    def x_pos(value: float) -> float:
        if chart_type == "scatter":
            return left + (value - x_min) / (x_max - x_min) * plot_width
        return left + (value + 0.5) / len(rows) * plot_width

    def y_pos(value: float) -> float:
        return top + (y_max - value) / (y_max - y_min) * plot_height

    elements = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title chart-desc">'
        ),
        f'<title id="chart-title">{esc(title)}</title>',
        (
            f'<desc id="chart-desc">{esc(chart_type)} chart of {esc(y_label)} '
            f'by {esc(x_label)}. {esc(source_note)}</desc>'
        ),
        "<defs>",
        *(pattern_svg(index, color) for index, color in enumerate(COLORS)),
        "</defs>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<g font-family="Arial, Helvetica, sans-serif" fill="#111827">',
        svg_text(left, 35, title, size=22, anchor="start", weight=700),
    ]

    for tick in range(6):
        value = y_min + (y_max - y_min) * tick / 5
        y = y_pos(value)
        elements.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" '
            'stroke="#e5e7eb" stroke-width="1"/>'
        )
        elements.append(svg_text(left - 10, y + 4, f"{value:g}", anchor="end"))

    elements.extend(
        (
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#374151"/>',
            f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#374151"/>',
        )
    )
    if chart_type == "bar":
        zero = y_pos(0)
        elements.append(
            f'<line x1="{left}" y1="{zero:.1f}" x2="{width-right}" y2="{zero:.1f}" '
            'stroke="#374151" stroke-width="1.5"/>'
        )

    if chart_type == "bar":
        group_width = plot_width / len(rows) * 0.78
        bar_width = group_width / len(y_columns)
        for row_index, _row in enumerate(rows):
            center = x_pos(row_index)
            start = center - group_width / 2
            for series_index, column in enumerate(y_columns):
                value = y_values[column][row_index]
                y = y_pos(value)
                elements.append(
                    f'<rect x="{start + series_index * bar_width:.1f}" y="{min(y, zero):.1f}" '
                    f'width="{max(1, bar_width - 2):.1f}" height="{abs(zero-y):.1f}" '
                    f'fill="url(#series-{series_index})"><title>{esc(column)}: {value:g}</title></rect>'
                )
    else:
        for series_index, column in enumerate(y_columns):
            color = COLORS[series_index % len(COLORS)]
            points = [
                (x_pos(numeric_x[index]), y_pos(value))
                for index, value in enumerate(y_values[column])
            ]
            if chart_type == "line":
                path = " ".join(
                    f"{'M' if index == 0 else 'L'} {x:.1f} {y:.1f}"
                    for index, (x, y) in enumerate(points)
                )
                elements.append(
                    f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3" '
                    f'stroke-dasharray="{DASHES[series_index]}"/>'
                )
            for index, (x, y) in enumerate(points):
                elements.append(marker_svg(
                    x,
                    y,
                    color,
                    series_index,
                    f"{column}: {y_values[column][index]:g}",
                ))

    if chart_type == "scatter":
        for tick in range(6):
            value = x_min + (x_max - x_min) * tick / 5
            elements.append(svg_text(left + plot_width * tick / 5, height - bottom + 24, f"{value:g}"))
    else:
        step = max(1, math.ceil(len(rows) / 12))
        for index, label in enumerate(categorical_x):
            if index % step == 0 or index == len(rows) - 1:
                elements.append(
                    svg_text(x_pos(index), height - bottom + 22, label, anchor="end", rotate=-35)
                )

    elements.append(svg_text(left + plot_width / 2, height - 44, x_label, size=14, weight=600))
    elements.append(
        svg_text(24, top + plot_height / 2, y_label, size=14, weight=600, rotate=-90)
    )
    if len(y_columns) > 1:
        for index, column in enumerate(y_columns):
            column_index = index % 3
            row_index = index // 3
            legend_x = left + column_index * plot_width / 3
            y = 58 + row_index * 24
            if chart_type == "bar":
                elements.append(
                    f'<rect x="{legend_x}" y="{y-11}" width="13" height="13" '
                    f'fill="url(#series-{index})"/>'
                )
            else:
                color = COLORS[index]
                if chart_type == "line":
                    elements.append(
                        f'<line x1="{legend_x}" y1="{y-4}" x2="{legend_x+14}" y2="{y-4}" '
                        f'stroke="{color}" stroke-width="3" '
                        f'stroke-dasharray="{DASHES[index]}"/>'
                    )
                elements.append(marker_svg(legend_x + 7, y - 4, color, index, column))
            elements.append(svg_text(legend_x + 20, y, column, anchor="start"))
    elements.append(svg_text(left, height - 12, source_note, size=11, anchor="start"))
    elements.extend(("</g>", "</svg>"))

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(elements) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--type", choices=("bar", "line", "scatter"), required=True)
    parser.add_argument("--x", required=True)
    parser.add_argument("--y", action="append", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--x-label", required=True)
    parser.add_argument("--y-label", required=True)
    parser.add_argument("--source-note", required=True)
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=600)
    args = parser.parse_args()
    render_chart(
        source=args.input,
        output=args.output,
        chart_type=args.type,
        x_column=args.x,
        y_columns=args.y,
        title=args.title,
        x_label=args.x_label,
        y_label=args.y_label,
        source_note=args.source_note,
        width=args.width,
        height=args.height,
    )
    return 0
