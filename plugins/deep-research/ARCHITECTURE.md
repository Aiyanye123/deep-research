# Deep Research Architecture

Deep Research combines a concise skill pipeline with a persistent filesystem runtime.

## State Machine

```text
clarify
  -> confirm brief
  -> record brief_confirmed
  -> create research session
  -> load research-orchestrator and record research_plan
  -> research waves
  -> evidence gate
     -> fail: continue research
     -> pass: load evidence-auditor and record evidence_preoutline_audit
  -> load insight-architect and record insight_outline
  -> independent insight_audit
  -> evidence_predraft_audit
  -> load research-visualizer and record visualization_review
  -> style_sheet and continuity_ready
  -> draft_complete
  -> evidence_prehumanize_audit
  -> snapshot researched-draft.md
  -> humanized_draft
  -> evidence_final_audit
  -> workflow gate
```

The evidence gate is the transition boundary between research and writing. A serious
research deliverable must not enter outlining or drafting while the gate fails.
The workflow gate is the completion boundary. It prevents a passing evidence gate
from being mistaken for a finished seven-skill research and writing run.

## Responsibilities

- `deep-research`: interaction contract and state-machine entry point.
- `research-orchestrator`: research lanes, waves, gaps, queries, and stop decisions.
- `evidence-auditor`: claims, sources, citation support, and evidence gate interpretation.
- `insight-architect`: thesis, counterreading, novelty, and outline.
- `research-visualizer`: visual selection, reproducible charts, generated imagery,
  figure manifests, accessibility, and visual evidence checks.
- `longform-writer`: installment drafting and continuity.
- `prose-humanizer`: article-type-aware style direction, Chinese prose profile
  selection, protected-content rules, and fact-preserving prose editing.
- `scripts/research_session.py`: persistent state and deterministic gate enforcement.
- `scripts/render_chart.py`: dependency-free common chart rendering.
- `scripts/check_chinese_prose.py`: profile-aware Chinese prose diagnostics that
  protect quotations, citations, structured content, and formal conventions.
- `scripts/evaluate_run.py`: structural regression scoring.

## Session Artifacts

See `references/session-schema.md`. Store serious projects in a dedicated session
directory so research can resume after context compression or a new conversation.

## Design Boundary

The scripts do not browse the web or call a model. Codex performs research with the
tools available in the current environment, then records results through the runtime.
This keeps the plugin provider-independent while making its research rules observable.

The Chinese prose checker is advisory except for high-confidence generated residue.
It does not rewrite text or decide whether evidence is sufficient. The evidence gate
owns research sufficiency, and `researched-draft.md` plus the final evidence audit own
factual preservation.
