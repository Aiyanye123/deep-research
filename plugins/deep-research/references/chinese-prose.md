# Chinese Prose Profiles

Use this reference only for Chinese deliverables. It adapts material-driven,
natural Chinese writing practices to Deep Research without replacing the brief,
evidence gate, claim ledger, or citation audit.

## Priority

Apply rules in this order:

1. The confirmed brief and the user's explicit article requirements.
2. Factual accuracy, quotation fidelity, source boundaries, and required format.
3. The selected prose profile in this document.
4. General anti-AI-pattern guidance.

Never sacrifice a fact, citation, quotation, technical term, or required format to
make prose appear less machine-generated.

## Select One Profile

### `essayistic`

Use for literary and cultural criticism, reviews, columns, public-facing essays,
narrative nonfiction, opinion writing, and explanatory articles whose voice is
part of the value.

- Keep a visible thinking presence without inventing personal experience.
- Let close reading, evidence, and the writer's judgment move together.
- Permit uneven paragraph lengths, brief asides, restrained humor, and qualified
  first person when they suit the brief.
- Do not turn every paragraph into a balanced summary.

### `formal`

Use for academic papers, policy research, legal or financial analysis, market
reports, literature reviews, journals, and institutional deliverables.

- Prefer precise, calm prose and explicit source attribution.
- Let evidence hierarchy, causal limits, and uncertainty carry the voice.
- Preserve conventional headings, citations, footnotes, definitions, captions,
  and reference formatting.
- Do not add personality merely to signal that a person wrote the text.

### `technical`

Use for technical reports, standards analysis, engineering explanations, methods,
specifications, and documentation-like research.

- Prefer stable terminology, direct verbs, short dependency chains, and explicit
  conditions.
- Keep code, identifiers, formulas, units, schemas, and procedure ordering exact.
- Use repetition when it prevents ambiguity. Terminological consistency outranks
  stylistic variation.

## Material-Driven Writing

Deep Research has already decided whether the evidence base is sufficient. At the
writing stage, use the session rather than starting a second research workflow.

- Ground each substantive paragraph in one or more claims, textual anchors,
  sources, data points, examples, or explicitly marked reasoning steps.
- A new paragraph must add a fact, observation, distinction, mechanism,
  counterargument, consequence, or interpretive advance. Restating the previous
  paragraph with new adjectives is not progress.
- If a planned section lacks support, record a gap and return it to the research
  workflow. Do not invent examples, scenes, consensus, quotations, or user
  experience, and do not silently shorten the requested deliverable.
- In literary criticism, let specific scenes, formal features, dialogue, editing,
  framing, sound, omissions, or textual contrasts support interpretation.
- In formal and technical work, distinguish observed fact, source claim,
  inference, interpretation, and forecast.

## Find A Speaking Position

The writer's presence comes from selection and judgment, not simulated biography.
Before drafting, identify internally:

- What the evidence establishes and what remains uncertain.
- Which finding or contradiction makes this article worth writing.
- What the writer currently believes, why, and where that judgment stops.
- What a reader will naturally need to know after each section.

Do not fabricate having watched, interviewed, tested, visited, or experienced
something. First person may express a defensible judgment or describe a real
research action, but it must not create false firsthand authority.

## Build Natural Movement

- Reach the subject quickly. Avoid announcing the article structure unless the
  article type requires an abstract, executive summary, or methods overview.
- Put the actor, action, claim, or observed feature early enough that the reader
  can follow a long sentence.
- Connect sections through evidence and unresolved questions, not generic depth
  markers such as "更深一层" or "值得注意的是".
- Vary sentence and paragraph length in response to information density. Do not
  manufacture roughness, slang, errors, or random asides.
- Let concrete evidence carry emotion and significance. Do not explain a scene a
  second time after its effect is already clear.
- State judgments directly, then place their reasons nearby. Do not create a
  straw misunderstanding solely to perform a dramatic reversal.
- Stop when the argument is complete. Do not append a generic summary, optimism,
  historical significance, or forced elevation.

## Protected Content

Treat the following as protected unless the user explicitly asks to transform it:

- Direct quotations and primary-text excerpts.
- Laws, standards, definitions, formulas, code, commands, and identifiers.
- Names, dates, numbers, ranges, units, statistical notation, and technical terms.
- Citation markers, footnotes, bibliography entries, URLs, and link targets.
- Headings required by a journal, report template, or publication.
- Tables, figure IDs, captions, source notes, alt text, and cross-references.
- Markdown, document, and machine-readable structure.

Colons, dashes, parallel structures, contrast sentences, and first person are not
global errors. Judge their frequency and function under the selected profile.

## Rewrite Rules

- Replace inflated significance and promotional claims with the specific fact or
  consequence that justifies them.
- Replace vague authority with a named source, institution, document, date, or a
  clearly marked uncertainty.
- Prefer direct verbs over nominalized management language when precision is not
  lost.
- Remove chat residue, praise of the user, process narration, and generic offers
  of further help from the deliverable.
- Break repetitive three-part structures and uniform mid-length sentences when
  they are habits rather than necessary organization.
- Keep useful repetition in formal and technical writing when it preserves a
  defined term or prevents reference ambiguity.
- Preserve counterarguments, qualifications, and inconvenient evidence. Natural
  prose is not permission to make the thesis cleaner than the research.

## Handoff

After rewriting, run `scripts/check_chinese_prose.py` with the selected profile.
Warnings require judgment, not automatic deletion. Then compare `draft.md` with
`researched-draft.md` and hand both to `evidence-auditor` for the final factual
drift review.
