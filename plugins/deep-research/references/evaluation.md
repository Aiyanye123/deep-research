# Evaluation

This reference is for maintainers and explicitly requested evaluation. It does
not add stages, files, or scoring to ordinary research delivery. Structural CLI
checks apply only to the optional managed runtime and remain subject to the user's
verification restrictions. The qualitative criteria can inform judgment without
requiring a separate review report.

Use evaluation to detect regressions after changing skills, scripts, models, or
research tools.

## Structural checks and activity metrics

Run:

```powershell
python scripts/evaluate_run.py --session <session-path>
```

The evaluator returns four distinct items:

- `structural_checks`: the current evidence and workflow gate results, plus whether
  the main report artifacts contain body text.
- `research_review_required`: always `true`; structure cannot establish the
  report's research quality.
- `qualitative_rubric`: reviewer criteria selected for the session's task mode,
  with a general research rubric as the fallback.
- `activity_metrics`: gate telemetry such as query, source, claim, anchor, and
  workflow-stage counts. Target progress belongs here and does not change a
  research-quality score.

Each evaluation calls `research_session.gate_result` and
`research_session.workflow_gate_result` against the current session files.
Persisted `audit.json` and `workflow-audit.json` are historical outputs and are
not used to determine current status. Evidence-reference validity is checked by
the evidence gate; this evaluator does not repeat that validation.

There is no overall research-quality score. Counts of textual anchors,
interpretation claims, or contradiction labels are activity data, not evidence of
originality or analytical quality. A passing gate confirms structural conditions
only; it does not replace the independent review below.

## Qualitative research-quality rubrics

Review the original brief and clarifications together with the actual final
report and its cited evidence. Judge each criterion as **Strong**, **Adequate**,
**Weak**, or **Critical failure**, and give a short explanation tied to the report
or sources. Do not average the judgments into a synthetic quality score. Record
the reviewer and review date. A critical failure in scope fidelity, evidence
integrity, or a central conclusion requires correction before delivery.

### Literary or cultural criticism

- Is the interpretive question, observation, or thesis specific and responsive to
  the requested work and angle, without requiring a novel central claim?
- Do interpretations rest on precise passages, scenes, formal choices, or other
  primary evidence?
- Does the report connect close reading to context without treating context as
  proof by itself?
- Where applicable, does it consider plausible alternative readings and details
  that complicate its interpretation without imposing false balance?
- Does it distinguish fact, inference, and uncertainty, and reach beyond plot or
  source summary?

### Academic literature review

- Does the review define a focused question, field boundary, and relevant time or
  method limits?
- Does it represent important theories, methods, evidence, and disagreements
  instead of listing papers one by one?
- Does it compare study designs, populations, measures, and limitations before
  combining findings?
- Does the synthesis explain agreement, disagreement, uncertainty, and gaps in
  the evidence?
- Are citations accurate, and does the proposed contribution or research gap
  follow from the reviewed literature?

### Market or company research

- Are the market, geography, customer segment, time period, and decision
  question defined consistently?
- Are market-size, growth, financial, and operating claims traceable to source
  data and consistent definitions?
- Does the report distinguish primary company disclosures from independent
  market evidence and compare them where relevant?
- Does it examine competitors, demand drivers, constraints, counterevidence, and
  material risks?
- Are assumptions and scenarios explicit, and do recommendations remain
  proportionate to the available evidence?

### Technical research

- Are the problem, system boundary, users, operating context, and decision
  clearly defined?
- Are technical or policy claims supported by relevant primary documentation,
  standards, data, or direct evidence?
- Does the report explain mechanisms and dependencies instead of listing
  features or rules?
- Does it examine failure cases, trade-offs, counterevidence, security or
  implementation constraints, and unresolved uncertainty?
- Are recommendations feasible in the stated context and supported by the
  analysis?

### Factual investigation or explanation

- Are the factual question, time frame, and included events clearly bounded?
- Are central claims traced to original records, with independent corroboration
  distinguished from repeated reporting?
- Are chronology and conflicting accounts checked without treating temporal
  succession as proof of causation?
- Are established facts, attributed claims, inference, and unknowns separated?
- Does the explanation answer the question and name missing evidence that could
  change the answer? Confirming a consensus or establishing an unknown can be a
  useful contribution.

## Real-output evaluation cases

These are repeatable input prompts and independent review standards. They define
four cases for evaluating actual completed reports; they are not reports or
results. All four cases are **Not run** until a session produces a final report
that an independent reviewer assesses.

For each managed-runtime evaluation execution, retain the exact prompt and clarification answers, session
artifacts, final `draft.md`, source records, evaluator JSON, and the reviewer's
criterion-by-criterion notes. Review the actual final report and cited sources,
not a paraphrase of the report. Compare `draft.md` with
`researched-draft.md` where available to identify whether editing changed claims,
evidence, or uncertainty.

### Literature case

**Input prompt:** “Write a 2,000–2,500 word Chinese-language literary analysis of
Lu Xun's *The New Year's Sacrifice* (《祝福》), focusing on how the narrative
voice and the recurring New Year ritual shape the reader's judgment of
Xianglin's Wife. Support the argument with specific textual details, distinguish
textual observation from historical context, consider the strongest alternative
reading, and cite sources for historical claims.”

**Independent review standard:** Verify the quoted or described textual details
against the work. Judge whether narrative form supports the thesis, whether
historical claims have suitable sources, and whether the alternative reading is
engaged with rather than dismissed. Flag claims about authorial intent that the
evidence cannot establish.

### Academic case

**Input prompt:** “Prepare a Chinese-language literature review of empirical
research published from 2019 through 2025 on remote work and knowledge-worker
productivity. Separate experimental and observational evidence, define how
productivity is measured, compare relevant study populations and methods, and
identify which conclusions remain uncertain. Do not infer a universal effect
from one setting.”

**Independent review standard:** Check coverage of relevant study designs and
measures against the cited papers. Verify that causal claims match the methods,
that unlike outcomes are not collapsed into one measure, and that the conclusion
reflects contradictory findings and population limits.

### Market case

**Input prompt:** “Assess the China residential battery-storage market as of the
research date for an executive deciding whether to fund a market-entry study.
Define the addressable customer segment and market boundaries, separate observed
installations from forecasts, explain unit and revenue assumptions, compare
competitors and route-to-market constraints, and present a downside case with
the evidence that would change the decision.”

**Independent review standard:** Recalculate material market estimates from
their stated inputs where possible. Check dates, units, definitions, and source
independence; distinguish reported results from forecasts; and verify that
competitor, regulatory, and channel claims support the recommendation and
downside case.

### Technical case

**Input prompt:** “Write a decision briefing for a web-engineering lead comparing
WebGPU with WebGL 2 for a browser-based interactive data-visualization product.
Use current official specifications and browser documentation, compare support,
capabilities, deployment constraints, performance considerations, and fallback
options, and state what must be benchmarked in the target workload before
choosing.”

**Independent review standard:** Verify capability and compatibility claims
against current official documentation. Check that the report distinguishes
specification guarantees from implementation status and workload-dependent
performance, describes failure and fallback paths, and does not recommend a
choice without naming the required product-specific validation.

## Regression set

Maintain these four cases plus a product-comparison case when suitable completed
sessions become available. Preserve the actual outputs and independent review
notes for each run; the case definitions alone do not count as completed
evaluations.
