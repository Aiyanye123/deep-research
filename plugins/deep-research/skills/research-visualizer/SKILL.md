---
name: research-visualizer
description: Use when Deep Research must decide, design, generate, or audit charts, tables, diagrams, timelines, maps, statistical plots, or other evidence-based visual elements for academic papers, research reports, journals, policy work, market analysis, or technical documents.
---

# Research Visualizer

Turn researched evidence into figures that clarify an argument. Do not add
decorative charts or visualize data whose provenance, units, or transformations
cannot be explained.

## Required Output

Write the decision and figure manifest to `visuals.md`, then record
`visualization_review` with `scripts/research_session.py complete-stage`.

If no visual adds analytical value, write a substantive explanation covering the
available data, rejected visual options, and why prose or a table is clearer. This
still completes the review without manufacturing a figure.

For every planned figure record:

```text
Figure:
- ID and filename:
- Analytical question:
- Figure type:
- Generation method: data renderer, Mermaid, built-in image generation, or other tool
- Generation prompt, when applicable:
- Data file:
- Source IDs:
- Variables, units, period, geography, and population:
- Transformations:
- Uncertainty or missing-data treatment:
- Caption:
- Alt text:
- Placement:
- Status: planned, generated, checked, or rejected
```

Store generated assets and their source data under `figures/`. Keep the cleaned
CSV used to render each quantitative figure so another researcher can reproduce it.

## Choose The Visual

- Exact values or heterogeneous measures: table.
- Category comparison: bar chart; sort when order is meaningful.
- Change over ordered time: line chart.
- Relationship between numeric variables: scatter plot; do not imply causation.
- Distribution: histogram, density plot, box plot, or violin plot.
- Part-to-whole: stacked bar; use pie or donut only for a few stable categories.
- Two-dimensional magnitude: heatmap with an explicit scale.
- Geographic pattern: map only when location is analytically relevant.
- Process, mechanism, or decision path: Mermaid flowchart.
- Chronology: timeline.
- Relationships: network diagram only when nodes and edges have defined meaning.
- Conceptual synthesis: model diagram whose arrows and labels state the proposed
  relationship rather than presenting interpretation as measured fact.
- Explanatory illustration, scientific concept image, editorial visual, cover, or
  historically reconstructed scene: use Codex built-in image generation when a
  generated bitmap communicates the idea better than a chart or diagram.

Prefer the simplest visual that answers one analytical question. One figure may
support several claims, but it should not attempt to tell the whole report.

## Generation

For ordinary bar, line, and scatter charts from tidy CSV, use the bundled
dependency-free renderer:

```powershell
python <plugin-root>/scripts/render_chart.py `
  --input <session>/figures/data.csv `
  --output <session>/figures/figure-01.svg `
  --type line `
  --x year `
  --y value `
  --title "Measured value by year" `
  --x-label "Year" `
  --y-label "Value (unit)" `
  --source-note "Source: S-0001; author's calculation."
```

Repeat `--y` for multiple series. Use SVG for scalable document output.

For histograms, box plots, regression diagnostics, confidence intervals, maps,
networks, or publication-specific formats, use an available spreadsheet,
statistical, document, or plotting tool. Preserve the same manifest and audit
requirements. Use Mermaid for process and relationship diagrams when the target
format renders Mermaid; otherwise export a static image.

For generated bitmap visuals, explicitly load the system `imagegen` skill and use
the built-in `image_gen` tool by default. Shape the prompt around the document's
argument, audience, factual constraints, composition, labels, and intended placement.
Move the selected project-bound image into the session's `figures/` directory and
record the final prompt and method in `visuals.md`. Inspect the result before use.

Never use image generation for a quantitative chart, empirical result, archival
facsimile, documentary photograph, or other visual that readers could mistake for
observed evidence. Label conceptual, reconstructed, or illustrative images as such.
Verify generated labels independently; use SVG, Mermaid, or document-native text
when exact wording is important.

## Data And Evidence Rules

- Derive chart data from logged sources, supplied datasets, or transparent
  calculations. Link every factual series to source IDs.
- Preserve raw values separately from cleaned or transformed values.
- Record filters, joins, exclusions, normalization, inflation adjustment,
  rebasing, aggregation, and calculated fields.
- Keep denominators, units, currency basis, time period, geography, sample size,
  and uncertainty visible.
- Do not infer missing values silently or mix incompatible series.
- Do not digitize a chart from a source when the underlying table is available.
- Distinguish descriptive patterns, model estimates, forecasts, and author-created
  conceptual diagrams.
- Treat generated images as explanatory or editorial assets, never as source-backed
  evidence. Do not cite them as proof of a factual claim.
- Do not use a visual to strengthen a causal claim beyond the evidence.

## Design Rules

- Use a descriptive title and a caption that states the takeaway without
  overstating it.
- Label axes and units directly. Avoid unlabeled dual axes and 3D effects.
- Use a restrained, color-blind-safe palette; do not rely on color alone.
- Start bar-chart quantitative axes at zero unless a clearly disclosed exception
  is analytically necessary.
- Show uncertainty, missingness, and breaks in series where material.
- Make labels readable at the final document size.
- Include useful alt text for each figure.
- Cite the source and note author calculations below the figure.

## Figure Audit

Before marking a figure `checked`:

1. Recalculate at least one value or transformation from the source data.
2. Compare plotted values, labels, units, ordering, legend, and period with the
   cleaned CSV and evidence ledger.
3. Check whether the chosen form could mislead through scale, truncation,
   aggregation, area, color, or omitted uncertainty.
4. Verify the caption and surrounding prose make no stronger claim than the data.
5. Open or render the final asset and confirm it is nonblank and legible.

Hand the checked figure manifest to `evidence-auditor` and `longform-writer`.
