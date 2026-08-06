<div align="center">
  <img src="plugins/deep-research/assets/logo.png" width="112" alt="Deep Research icon">
  <h1>Deep Research for Codex</h1>
  <p>Controllable, resumable, evidence-driven research for high-quality long-form writing.</p>
  <p><a href="README.md">简体中文</a> | <strong>English</strong></p>
</div>

Deep Research is a local Codex plugin for controllable, source-backed long-form
research and writing.

It preserves the useful brief-first interaction:

1. Ask and persist at least 3 dynamic questions before research, with no fixed upper limit.
2. Confirm and rewrite the user's brief.
3. Research in multiple waves.
4. Persist queries, sources, claims, gaps, and textual anchors.
5. Block outlining and drafting until the evidence gate passes.
6. Build original insight and pass an independent insight audit.
7. Select, generate, and audit useful charts, diagrams, or explanatory images.
8. Draft with long-form continuity.
9. Snapshot the researched draft, humanize the working copy, and audit both versions.

The plugin is not an official ChatGPT Deep Research implementation and does not
claim access to private OpenAI internals.

## Installation

Add this repository as a Codex Git marketplace, then install the plugin:

```powershell
codex plugin marketplace add Aiyanye123/deep-research
codex plugin add deep-research@aiyanye-deep-research
```

Start a new Codex task after installation or upgrade so the new Skills are loaded
from a fresh context.

## Why It Is Different

Most research prompts rely on the model to remember that it should search deeply.
This plugin adds a lightweight filesystem runtime so research depth is observable
and resumable.

The runtime rejects duplicate queries and sources, tracks research waves and
high-impact gaps, distinguishes qualified evidence from low-value source padding,
tracks information saturation, and returns a machine-readable evidence-gate result.
If the gate fails, the workflow must continue researching instead of drafting.
It also records ordered companion-skill stages and rejects final completion when a
research plan, evidence audit, insight architecture, style sheet, continuity pass,
visualization review, humanizer pass, or final audit was skipped.

## Bundled Skills

The plugin source lives under `plugins/deep-research`. Paths in the following
sections are relative to that directory.

```text
skills/deep-research/SKILL.md
skills/research-orchestrator/SKILL.md
skills/evidence-auditor/SKILL.md
skills/insight-architect/SKILL.md
skills/research-visualizer/SKILL.md
skills/longform-writer/SKILL.md
skills/prose-humanizer/SKILL.md
```

## Persistent Research Runtime

Create a session:

```powershell
cd plugins/deep-research
python scripts/research_session.py init `
  --session research-sessions/example `
  --title "Example Research" `
  --task-mode cultural_criticism `
  --depth deep `
  --required-lane primary_text `
  --required-lane official
```

Before research, record at least three answered clarifications, write `brief.md` and
`research-plan.md`, then record:

```powershell
python scripts/research_session.py add-clarification --session research-sessions/example --dimension "task-specific dimension" --impact "what this answer changes" --question-form open --question "..." --answer "..."
python scripts/research_session.py complete-stage --session research-sessions/example --stage brief_confirmed --note "Confirmed the binding brief, audience, scope, length, voice, and source constraints."
python scripts/research_session.py complete-stage --session research-sessions/example --stage research_plan --note "Loaded research-orchestrator and defined source hierarchy, lanes, waves, gaps, verification, and stop conditions."
```

Log research:

```powershell
python scripts/research_session.py add-query --session research-sessions/example --query "..." --wave orientation --lane official
python scripts/research_session.py add-source --session research-sessions/example --url "https://example.com" --title "Example" --lane official --source-type official --opened --quality high --reading-depth deep
python scripts/research_session.py add-claim --session research-sessions/example --claim "..." --source-id S-0001 --section "Section 1" --major
python scripts/research_session.py add-gap --session research-sessions/example --question "..." --impact high --next-query "..."
python scripts/research_session.py cover-item --session research-sessions/example --item "..."
python scripts/research_session.py complete-wave --session research-sessions/example --wave orientation
python scripts/research_session.py assess-saturation --session research-sessions/example --status pass --note "Targeted follow-up searches across the remaining source lanes repeated existing evidence; counterpoint and verification searches found no unresolved high-impact gaps."
```

Before saturation can pass, the final two required waves must each contain an
executed query with a substantive `--result-note`.

Run the hard gate:

```powershell
python scripts/research_session.py gate --session research-sessions/example
python scripts/research_session.py resume --session research-sessions/example
```

Do not outline or draft while `gate` returns `fail`.

Record each ordered companion-skill stage with `complete-stage`. Before returning
the final deliverable, run:

```powershell
python scripts/research_session.py workflow-gate --session research-sessions/example
```

Do not call the run complete while `workflow-gate` returns `fail`.

The outline must pass `insight_audit` before pre-draft approval. Immediately before
Humanizer editing, `evidence_prehumanize_audit` automatically copies `draft.md` to
immutable `researched-draft.md`; the final audit compares both versions.

## Charts And Visuals

`research-visualizer` decides whether a visual adds analytical value. It can create
reproducible bar, line, and scatter charts from CSV with `scripts/render_chart.py`,
use available statistical or spreadsheet tools for advanced plots, use Mermaid for
structured diagrams, or call Codex built-in image generation for explanatory and
editorial imagery. Generated images are labeled as illustration and never treated
as empirical evidence. Every retained figure is recorded in `visuals.md` with its
source data or prompt, caption, alt text, placement, and audit status.

Source targets are dynamic. The plugin requires a meaningful floor so research
cannot stop after a few pages, but it does not reward padding. Shallow rewrites,
irrelevant pages, and low-quality aggregations do not count.

Rare primary material, deeply read scholarship, authoritative records, independent
reporting, and uniquely informative niche sources receive additional evidence-value
units. This rewards depth and usefulness without allowing the agent to stop with
only a handful of ordinary pages.

## Literary And Cultural Criticism

The plugin does not treat online commentary as a substitute for reading the work.
Use `add-anchor` to record scenes, passages, framing, motifs, dialogue, editing,
music, omissions, and alternative readings.

Before drafting, the insight stage identifies dominant interpretations, rejects
conventional thesis candidates, and stress-tests the chosen argument.

## Long-Form Writing

For long projects, the session preserves:

- Confirmed brief.
- Research trace and evidence ledger.
- Insight architecture and outline.
- Section evidence assignments.
- Continuity notes.
- Current draft and audit result.

This allows a new conversation or compressed context to resume from the session
instead of reconstructing the project from memory.

## Evaluation

Run deterministic structural evaluation:

```powershell
python scripts/evaluate_run.py --session research-sessions/example
```

The evaluator checks research coverage, source quality and diversity, claim
grounding, analysis structure, long-form artifacts, reliability, and workflow
integrity. It does not replace semantic review of prose or argument quality.

## References

- `ARCHITECTURE.md`
- `references/official-mechanism.md`
- `references/session-schema.md`
- `references/depth-profiles.md`
- `references/security.md`
- `references/evaluation.md`
- `references/literary-research.md`
- `THIRD_PARTY_NOTICES.md`
