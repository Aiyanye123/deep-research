---
name: evidence-auditor
description: Use when Deep Research needs a claim-level evidence ledger, source confidence tracking, contradiction notes, citation checks, factual verification, and post-edit audit.
---

# Evidence Auditor

## Purpose

Maintain the evidence base and audit the draft against it. This skill merges evidence ledger and citation audit so claims, citations, and final prose stay aligned.

Use throughout research, before drafting, before prose-humanizer, and after prose-humanizer.

For serious work, write separate audit artifacts and record these ordered stages:

- `evidence_preoutline_audit` -> `pre-outline-audit.md`
- `insight_audit` -> `insight-audit.md`
- `evidence_predraft_audit` -> `pre-draft-audit.md`
- `evidence_prehumanize_audit` -> `pre-humanize-audit.md`
- `evidence_final_audit` -> `final-audit.md`

Run `complete-stage` after each audit. The final audit snapshots `draft.md`; editing
the draft afterward invalidates the full workflow gate.

## Independent Insight Audit

After `insight-architect` prepares the outline but before drafting, independently
test whether the proposed thesis advances beyond source rearrangement. Revise the
outline before recording stages when the audit fails. A passing `insight-audit.md`
must include:

```text
Status: pass
Original contribution: [specific contribution]
Strongest conventional alternative: [best established or obvious reading]
Counterevidence: [evidence that could weaken the thesis]
Required revisions: none
```

Fail the audit when the thesis merely summarizes sources, renames a common reading,
cannot survive its strongest alternative, or has no section-level argumentative
progression. Once it passes, record `insight_outline` and then `insight_audit`.

For serious work, store atomic evidence in the persistent session:

```powershell
python <plugin-root>/scripts/research_session.py add-claim --session <path> --claim "<claim>" --source-id S-0001 --section "<section>" --major
python <plugin-root>/scripts/research_session.py update-claim --session <path> --claim-id C-0001 --source-id S-0002
python <plugin-root>/scripts/research_session.py gate --session <path>
```

## Evidence Ledger

Maintain:

```text
Evidence ledger:

| ID | Claim or detail | Source | Source type | Date | Evidence note | Confidence | Contradictions | Use in section |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

For each entry:

- Use one claim, statistic, date, quote, plot detail, or interpretation per row.
- Mark source type: primary, official, academic, filing, news, review, community, wiki, estimate.
- Mark confidence: high, medium, low.
- Keep interpretation separate from source-backed fact.
- Record contradictions, caveats, missing context, and source period.

## Evidence Gates

Before outlining or drafting, check:

- Does every major planned section have evidence?
- Does each must-cover detail have a source or an explicit gap note?
- Are central claims supported by stronger sources than wikis, snippets, or community summaries?
- Are numbers preserved with units, dates, region, denominators, and source period?
- Are quotes short, accurate, and attributed?
- Are company claims separated from independent verification?
- Are analyst estimates, fan interpretations, and forecasts labeled as such?
- Are search snippets excluded from the opened-source count?
- Are weak, duplicate, irrelevant, or superficial sources excluded from the qualified-source count?
- Are required source lanes covered by independently assessed sources?
- Are high-impact gaps resolved?
- Does every planned section have assigned claim evidence?
- Does the persistent evidence gate return `pass`?
- Is information saturation justified instead of asserted only to stop early?

The script gate is structural, not semantic. Review whether each cited source
actually supports the claim before approving the draft.

For figures and tables, also check:

- Every factual series maps to logged sources and a preserved data file.
- Values, units, denominators, dates, geography, filters, and transformations match
  the evidence ledger.
- Captions and surrounding prose do not overstate association, causation, precision,
  forecast certainty, or statistical significance.
- Scale, truncation, aggregation, missing data, uncertainty, and source notes are
  disclosed where material.

## Citation Audit

Return:

```text
Citation audit:

- Status: pass, pass with fixes, or fail
- Unsupported claims:
- Weakly supported claims:
- Citation mismatches:
- Number, date, and unit checks:
- Quote checks:
- Source quality concerns:
- Interpretation checks:
- Figure and table checks:
- Prose-humanizer preservation checks:
- Required fixes:
```

## Rules

- Do not approve a draft because it sounds good.
- If a claim cannot be supported, remove it, weaken it, or research further.
- For literary claims, distinguish primary text evidence, source commentary, and the author's own reading.
- For current topics, verify dates and avoid timeless phrasing.
- Run the audit again after `prose-humanizer` to catch softened caveats, changed numbers, blurred uncertainty, or altered names.
- Compare immutable `researched-draft.md` with humanized `draft.md`; preserve facts,
  citations, quotations, qualifications, dates, numbers, names, and uncertainty.
- Never approve outlining or drafting while the persistent evidence gate is `fail`.
- Never reuse an earlier audit artifact as proof of a later audit stage.
