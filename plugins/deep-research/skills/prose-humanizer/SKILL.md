---
name: prose-humanizer
description: Use when Deep Research needs article-type-aware voice design, Chinese or English prose editing, natural long-form rhythm, anti-AI-pattern review, and fact-preserving humanization after evidence-backed drafting.
---

# Prose Humanizer

## Purpose

Design a specific voice before drafting and remove mechanical prose after the
research draft passes evidence review. Preserve the research, source boundaries,
and requested format.

Write pre-draft direction to `style-sheet.md` and record `style_sheet`.
Completing `evidence_prehumanize_audit` creates the immutable
`researched-draft.md`. Edit only `draft.md`, compare it with that snapshot, and
record `humanized_draft`. Hand the result to `evidence-auditor`; do not record the
final evidence audit yourself.

This stage must not restart clarification, create a second research plan, silently
shorten the deliverable, or invent material. When prose work exposes an evidence
gap, return the gap to the research workflow.

## Style Sheet

Record:

```text
Style sheet:

- Target voice:
- Article type:
- Topic or issue type:
- Reader relationship:
- Register:
- Sentence rhythm:
- Paragraph movement:
- Level of personal presence:
- Humor or edge:
- Technical density:
- Citation visibility:
- Formatting rules:
- Language profile:
- Chinese prose profile: essayistic | formal | technical | not-applicable
- Protected content:
- Evidence-preservation policy:
- Checker profile: essayistic | formal | technical | not-applicable
- Phrases or habits to prefer:
- Phrases or habits to avoid:
```

Do not treat publication platform as a style preset. Infer direction from the
subject, article type, evidence density, reader relationship, and user's examples
or constraints.

## Voice Calibration

When the user provides a sample:

- Observe sentence length, transitions, paragraph openings, punctuation, word
  choice, opinion level, and useful irregularities.
- Match the sample's behavior without copying its content.
- Preserve roughness or looseness when it is part of the voice and does not weaken
  accuracy.

When no sample exists:

- Infer a narrow style target from the brief, topic, article type, and evidence.
- Let the material determine rhythm and structure instead of applying generic
  polish.

Useful directions include:

- Literary or cultural criticism: close-reading led, essayistic, willing to
  sustain ambiguity, and clear about interpretive risk.
- Review or commentary: concrete examples, visible judgment, and no synopsis
  padding.
- Public explanation: accessible and structured around reader questions rather
  than a memo outline.
- Narrative nonfiction: scene or process led, but only when the evidence supports
  those details.
- Academic, policy, legal, financial, or market analysis: precise, source-forward,
  proportionate, and explicit about limits.
- Technical work: stable terminology, direct procedures, and no ornamental voice.

## Chinese Deliverables

Read `<plugin-root>/references/chinese-prose.md` before creating `style-sheet.md`
or editing Chinese prose. Select exactly one profile:

- `essayistic` for criticism, reviews, columns, public essays, narrative
  nonfiction, opinion, and voice-led explanation.
- `formal` for academic, policy, legal, financial, market, journal, and
  institution-facing research.
- `technical` for engineering, standards, specifications, methods, and
  documentation-like research.

Use the session's claim ledger, textual anchors, outline, and evidence audits as
the material base. Deep Research's evidence gate replaces external writing-skill
rules about minimum material counts, extra intake questions, or automatic length
reduction.

Before the final Chinese edit, also read
`<plugin-root>/references/humanizer-zh.md`. Treat it as a diagnostic layer, not a
voice template.

After editing, run:

```powershell
python <plugin-root>/scripts/check_chinese_prose.py <session>/draft.md --profile <essayistic|formal|technical>
```

Fix high-confidence failures. Review warnings in context; do not mechanically
delete punctuation, contrast, first person, repetition, or required structure.

## English Deliverables

Use the article-specific style sheet and the general humanization pass below.
Do not load Chinese references or run the Chinese checker.

## Evidence And Protected Content

Preserve:

- Claims, counterclaims, uncertainty, and caveats.
- Citation markers, source roles, links, footnotes, and bibliography entries.
- Direct quotations and primary-text excerpts.
- Names, dates, numbers, ranges, units, formulas, and technical terms.
- Laws, standards, definitions, code, commands, identifiers, and schemas.
- Required headings, tables, figure IDs, captions, source notes, alt text, and
  cross-references.
- The section's argument, terminology, and continuity handoff.

Do not paraphrase a quotation merely because it contains a disfavored construction.
Do not change structured or machine-readable material for stylistic consistency.

## Humanization Pass

Rewrite the unnecessary performance around meaning; do not delete the meaning.

Remove or reduce:

- Inflated significance and promotional wording.
- Vague authority when a named source is available.
- Generic introductions, conclusions, and compulsory future-outlook sections.
- Chat residue, praise, process narration, and offers of more help.
- Formulaic three-part padding and repeated paragraph scaffolds.
- Mechanical bold headings and excessive visual labeling.
- Repetitive mid-length sentence rhythm.
- Business or model jargon that hides actors, actions, costs, or consequences.
- Fake personal experience and unsupported scene details.

Add or preserve when justified:

- Specific evidence, observable actions, and named sources.
- A defensible point of view and explicit limits.
- Natural differences in sentence and paragraph length.
- Useful first person in essayistic work without false firsthand authority.
- Stable repetition in formal or technical work when it prevents ambiguity.
- Counterevidence and unresolved tension.

For literary and cultural criticism, keep interpretation tied to textual anchors
and do not flatten the article into a neutral source summary. For formal and
technical documents, plain precision is already a human voice.

## Final Check

Before returning the edited draft:

1. Compare `draft.md` with `researched-draft.md`.
2. Restore any lost citation, quotation, caveat, number, date, unit, term, source
   boundary, figure reference, or required structure.
3. Confirm that each substantive paragraph still performs evidentiary or
   analytical work.
4. Run the configured prose checker for Chinese work and review its warnings.
5. Never modify or regenerate `researched-draft.md`.
6. Hand both drafts to `evidence-auditor` for the final factual-drift audit.
