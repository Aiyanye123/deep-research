# Evaluation

Use evaluation to detect regressions after changing skills, scripts, models, or
research tools.

## Structural Evaluation

Run:

```powershell
python scripts/evaluate_run.py --session <session-path>
```

The deterministic evaluator scores:

- Research coverage.
- Source quality and diversity.
- Claim grounding.
- Analysis and originality structure.
- Presentation and long-form state.
- Reliability.
- Full seven-skill workflow integrity, including visualization review.

It does not judge whether prose is beautiful or whether an interpretation is
genuinely insightful.

Passing the evidence gate below the dynamic research target is allowed after
information saturation, but the evaluator still scores target progress. This
keeps a quality-rich niche corpus valid without treating a minimal pass as equal
to a fuller high-quality research run.

## Human Or Model Review Rubric

Review completed reports on:

1. User constraints: length, audience, format, tone, scope, and exclusions.
2. Information recall: important facts, entities, arguments, and missing context.
3. Evidence: citation completeness, support, authority, and independence.
4. Analysis: synthesis, counterevidence, uncertainty, and useful conclusions.
5. Originality: whether the thesis advances beyond rearranged source summaries.
   Confirm that `insight-audit.md` independently tests the original contribution,
   strongest conventional alternative, and counterevidence before drafting.
6. Presentation: structure, readability, continuity, and source visibility.
7. Prose: article-type fit, natural rhythm, and absence of mechanical AI patterns.
   Compare `draft.md` with the automatic `researched-draft.md` snapshot to confirm
   that Humanizer edits did not change claims, evidence, or uncertainty.

## Regression Set

Maintain a small set of repeatable prompts across:

- Literary or cultural criticism.
- Market or company research.
- Academic literature review.
- Policy or technical briefing.
- Product comparison.

Preserve the original prompt, clarification answers, session artifacts, final
report, and evaluation result for each run.
