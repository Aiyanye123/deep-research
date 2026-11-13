# Repository Guidelines

## Project Structure

This repository distributes a Codex Deep Research plugin. The marketplace catalog is `.agents/plugins/marketplace.json`; the plugin and its manifest live under `plugins/deep-research/`. Its `skills/*/SKILL.md` files define workflows, `references/` holds supporting guidance, `scripts/` contains Python utilities, `tests/` contains regression tests, and `assets/` holds plugin assets. Consult `ARCHITECTURE.md` for workflow boundaries. The root README files provide English and Chinese documentation.

## Development and Commands

Run commands from the repository root. There is no separate build step documented for the plugin.

- `python -m unittest discover -s plugins/deep-research/tests` runs the regression suite.
- `python plugins/deep-research/tests/test_check_chinese_prose.py` runs one focused test file; substitute another `test_*.py` file as needed.
- `python plugins/deep-research/scripts/check_chinese_prose.py <draft.md> --profile formal` checks a draft with the formal prose profile.
- `python plugins/deep-research/scripts/evaluate_run.py --session <research-session-directory>` evaluates a managed research session.

For installation, use the marketplace commands in the root README and start a new Codex task to load updated skills.

## Style and Testing

Follow existing Python conventions: four-space indentation, `snake_case` functions and files, descriptive names, and type annotations where appropriate. Keep skill instructions in Markdown with the existing `SKILL.md` frontmatter and directory naming. Update related references and documentation when behavior changes.

Tests use Python's `unittest`; name files and methods `test_*.py` and `test_*`. Add focused regression coverage for changed behavior. Validate affected tools, skill frontmatter, and the plugin manifest when changing the package. Structural checks alone do not establish research or writing quality; assess model behavior with actual research and writing trials when relevant.

## Commits and Pull Requests

Record project updates in an update log under `../docs/`, the `docs` directory beside this repository.

Recent commits use short, imperative descriptions, such as `Restore dependency-based research gates and strengthen prose revision`. Keep each commit focused. For pull requests, describe the problem and resulting behavior, link any relevant issue, and list the checks performed. Include examples or screenshots when they help reviewers assess output or visual changes.
