---
name: research-orchestrator
description: Use when Deep Research needs source strategy, multi-wave web research, gap searches, counterpoint checks, verification passes, and explicit stop conditions before drafting.
---

# Research Orchestrator

## Purpose

Plan and control the research phase. This skill merges source strategy and research loop control so the model does not stop after opening only a few pages.

Use after the Deep Research brief is confirmed and before evidence/auditing work.

For serious work, operate through the persistent session created by
`scripts/research_session.py`. Read `references/depth-profiles.md` for budgets and
`references/security.md` before using untrusted web or private sources.

Write the plan to `research-plan.md`, then record `research_plan` with
`complete-stage` before running queries. The runtime rejects research actions until
this stage exists.

## Output

Produce:

```text
Research plan:

- Research mode:
- Depth level:
- Source hierarchy:
- Search lanes:
- Must-find sources:
- Risky or weak sources:
- Language and region requirements:
- Search waves:
- Evidence gates:
- Gap checks:
- Counterpoint checks:
- Verification checks:
- Stop conditions:
```

## Depth Levels

- `light`: quick overview only when the user asks for speed.
- `standard`: normal article or report.
- `deep`: default for Deep Research, long-form work, criticism, market research, policy briefs, and literature reviews.
- `exhaustive`: book-length, high-stakes, academic, legal, financial, or explicitly exhaustive work.

## Source Hierarchy

Choose source authority by task.

Cultural criticism or review:

- Primary text: episodes, chapters, films, official translations, creator statements.
- Official context: studio notes, interviews, production material, official sites.
- Reception context: reviews, fan discussions, forums, logs, columns, and databases.
- Reference context: wikis and databases for orientation, not as final authority.

Market or company research:

- Primary company sources: filings, reports, presentations, earnings calls.
- Market sources: industry reports, regulator data, market share trackers.
- Competitive sources: competitor filings, products, pricing, channels.
- Sentiment sources: reviews, social media, communities. Treat as directional.
- News and analysts: useful context, but separate claims from interpretation.

Academic, policy, legal, or technical work:

- Prefer peer-reviewed papers, books, primary texts, official archives, statutes, regulations, standards, specs, case law, RFCs, and primary documentation.
- Use commentary only after primary authorities are mapped.

## Search Waves

Run research in waves and update the evidence base after each wave:

1. Orientation: map vocabulary, entities, timeline, source lanes.
2. Authority: find primary, official, academic, regulatory, filing, or direct text sources.
3. Detail: target must-cover people, products, scenes, concepts, metrics, episodes, or controversies.
4. Counterpoint: search for contradictions, dissenting readings, risks, negative evidence, or alternative interpretations.
5. Verification: re-check dates, numbers, names, quotes, source freshness, and high-impact claims.

After each wave:

1. Log every useful query with `add-query`; duplicate queries are rejected.
2. Log opened and assessed pages with `add-source`. Search snippets are not opened sources.
3. Log atomic findings with `add-claim` and unresolved questions with `add-gap`.
4. Mark the wave complete with `complete-wave`.
5. Assess information saturation after targeted gap searches.
6. Run `gate`.

Before marking saturation `pass`, ensure the final two required research waves each
contain at least one executed query with a substantive `--result-note`. The runtime
uses these records as a modest evidence floor; it does not require reaching the
dynamic source target when high-quality targeted searches have become repetitive.

If `gate` fails, execute its `next_actions`. Do not hand off to outlining or drafting.
When it passes, hand off to `evidence-auditor`; do not mark an audit stage yourself.

Research quality outranks raw source count. Count only opened and assessed sources
that are authoritative, independent, deeply read, or uniquely informative. Do not
add duplicate rewrites, shallow aggregations, irrelevant pages, or SEO material to
reach a numeric target. Read `references/depth-profiles.md` for the dynamic stop rule.

## Runtime Commands

```powershell
python <plugin-root>/scripts/research_session.py add-query --session <path> --query "<query>" --wave <wave> --lane <lane>
python <plugin-root>/scripts/research_session.py add-source --session <path> --url "<url>" --title "<title>" --lane <lane> --source-type <type> --opened --quality high --reading-depth deep --unique-value
python <plugin-root>/scripts/research_session.py add-gap --session <path> --question "<gap>" --impact high --next-query "<query>"
python <plugin-root>/scripts/research_session.py cover-item --session <path> --item "<must-cover item>"
python <plugin-root>/scripts/research_session.py complete-wave --session <path> --wave <wave>
python <plugin-root>/scripts/research_session.py assess-saturation --session <path> --status pass --note "<why further targeted search is low-yield>"
python <plugin-root>/scripts/research_session.py gate --session <path>
```

Use query, failure, and source budgets as upper bounds. If a budget is exhausted
before the gate passes, state the limitation and remaining gaps. Do not call the
result fully researched.

## Stop Conditions

Research may stop only when all are true:

- The evidence base can support the planned outline.
- More than one relevant source lane has been checked unless the brief legitimately has only one.
- Must-cover entities or themes have evidence or are marked unavailable.
- Primary or authoritative sources were checked when available.
- Major contradictions or alternative views were checked.
- Remaining gaps and source weaknesses are named.
- Further searches are likely repetitive or low-yield.
- Information saturation is documented with a concrete justification.
- The persistent evidence gate returns `pass`.

If tool limits, paywalls, blocked pages, or unavailable sources prevent deeper research, say so explicitly and do not call the result fully researched.
