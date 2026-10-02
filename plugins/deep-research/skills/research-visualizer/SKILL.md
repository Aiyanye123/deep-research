---
name: research-visualizer
description: Use when a chart, table, diagram, timeline, map, or illustration can materially improve a research explanation or deliverable.
---

# Research Visualizer

Use a visual when it makes a relationship, comparison, process, or finding easier
to understand. Choose it for the question and genre, not to complete a workflow
stage. If prose already works well, continue without a figure or an explanation
file about that decision. A visual manifest is useful only when managing several
assets actually requires one.

The lead decides whether a visual helps, what question it answers, and its
substantive data choices and interpretation. Delegate useful extraction,
calculations under a stated method, rendering, formatting, and export under
`deep-research`'s division of labor. Return the actual figure, source data or
locations, and material transformations. The lead inspects the resulting figure
and its fit with the prose; a verbal completion report is insufficient.

## Choose A Useful Form

Prefer a simple form that answers a clear question. Tables suit exact values or
heterogeneous measures; bars suit category comparisons; lines show change over
ordered time; scatter plots show numeric relationships; distributions need an
appropriate distribution plot. Use maps when geography matters, timelines for
chronology, and diagrams for processes or defined relationships. Conceptual
diagrams should identify proposed relationships without presenting them as
measured findings.

Do not add decorative charts or imply that association establishes causation.
An illustration or editorial image can be useful for some articles; literary
work may need no visual at all.

## Data And Generation

Build factual figures from source data, supplied datasets, or transparent
calculations. Keep the data used for a quantitative figure together with its
source, units, period, population or geography, and material transformations.
Preserve original values when cleaning or transforming them. Explain filters,
exclusions, normalization, rebasing, aggregation, missing values, and estimates
where they affect interpretation. Do not silently mix incompatible series or
invent missing observations. Use an available underlying table instead of
digitizing an image when possible.

Use existing plotting, spreadsheet, or document tools that fit the output. The
bundled `scripts/render_chart.py` can render ordinary bar, line, and scatter
charts from tidy CSV; it is optional and does not require a managed research
session. Prefer scalable output when the document benefits from it. Mermaid is
useful for a small process or relationship diagram when the target supports it;
export a static asset when necessary.

For a generated bitmap, load the system `imagegen` skill and use the built-in
`image_gen` tool. Describe the purpose, audience, factual constraints,
composition, and intended placement, then inspect the result before using it.
Retain the prompt when useful for later revisions, without requiring a separate
manifest.

Never use image generation to fabricate a quantitative chart, empirical result,
archival facsimile, documentary photograph, or another image readers could
mistake for observed evidence. Label conceptual, reconstructed, or illustrative
images accordingly and do not cite them as proof. Check generated labels;
prefer SVG, Mermaid, or document-native text when exact wording matters.

## Make It Readable And Honest

Use readable labels, direct axis titles and units, a restrained accessible
palette, and a caption that states the finding without overstating it. Do not
rely on color alone. Avoid unexplained dual axes and 3D effects. Bar axes normally
start at zero; disclose and justify an exception. Show material uncertainty,
missingness, and breaks in a series. Include the source and author calculations
near the figure and useful alternative text where the delivery format supports it.

Before delivery, compare values, labels, units, ordering, period, and caption with
the source data. Check calculations and transformations in proportion to their
complexity and consequence. Examine whether scale, area, aggregation, or omitted
uncertainty could mislead. Open or render the final asset to check legibility at
the intended size and that surrounding prose says no more than the data supports.

Place the figure near the passage it clarifies and preserve the data and source
information needed to understand or reproduce it. Recheck affected parts when a
figure changes. In the default/full workflow, retain the visual decision and
relevant source/method information in `visuals.md` and complete
`visualization_review` under the current session's dependencies. This can run
alongside drafting; figure production may be delegated, but the lead checks
finished assets and their integration before whole-text polish and final review.
A text-only decision needs a concise actual explanation in `visuals.md`, not a
decorative figure. Flexible operation requires no stage record or separate visual
file unless managed operation is selected. No fingerprints are used.
