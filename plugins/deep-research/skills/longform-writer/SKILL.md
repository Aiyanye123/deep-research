---
name: longform-writer
description: Use when Deep Research needs chapter-by-chapter drafting, long-form continuity, stable terminology, section handoffs, claims already established, and installment management.
---

# Longform Writer

## Purpose

Draft long-form work in controlled sections while preserving continuity. This skill merges chapter writing and continuity management.

Use after the brief, evidence, insight architecture, and style direction are ready.

Write the initial continuity state to `continuity.md` and record
`continuity_ready` before drafting. Write the researched draft to `draft.md` and
record `draft_complete` when all requested sections are present. Do not record the
humanizer or audit stages.

## Inputs

Require:

- Confirmed brief.
- Passing persistent evidence gate.
- Section card or outline.
- Evidence IDs assigned to the section.
- Style sheet from `prose-humanizer`.
- Checked figure manifest from `research-visualizer`, when visuals are required.
- Continuity note if this is not the first installment.

## Output

For each installment:

```text
Draft installment:

- Section:
- Target words:
- Evidence used:
- Continuity links:
- Draft:
- Notes for next installment:
```

Then update:

```text
Continuity note:

- Project title:
- Current thesis:
- Target voice:
- Publication context:
- Completed sections:
- Claims already established:
- Evidence already used:
- Terms and naming conventions:
- Character, entity, or concept handling:
- Open loops:
- Repetition risks:
- Contradictions to resolve:
- Next section goal:
- Prose-humanizer notes:
```

## Drafting Rules

- Write the requested section, not a summary of the whole project.
- Follow the section card's job and word target.
- Use evidence naturally. Do not dump sources mechanically.
- In literary or cultural criticism, every section should advance the original reading.
- Keep citations or source references in the requested format.
- If evidence is weak, write with caveats rather than pretending certainty.
- If the source material conflicts, make the conflict visible.
- Do not introduce major claims absent from the evidence base unless labeled as interpretation.
- Do not let each section sound like a fresh standalone answer.
- Do not begin a new section when the persistent gate has returned to `fail`
  because new high-impact gaps or unsupported claims were discovered.
- Place each figure near the claim it supports, refer to it in the prose, and explain
  the analytical takeaway rather than repeating every plotted value.
- Preserve figure IDs, captions, source notes, units, and alt text. Do not introduce
  a new chart or table whose data was not audited.

## Long-Form Controls

For projects over about 8,000 words:

- Draft by section or chapter.
- Keep each installment bounded.
- End with a continuity update and next-section handoff.
- Track repeated examples, repeated phrasing, term drift, and thesis drift.
- If a later section changes the thesis, record whether earlier sections need revision.
