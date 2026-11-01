# lakmus-dev

The working method of the [Lakmus](https://github.com/lakmuslabs/lakmus) project, as a Claude Code
plugin. It exists because the project's two real risks are not coding mistakes: silently changing a
contract that published suites depend on, and shipping a test suite whose methodology does not
survive scrutiny. Skills and reviewers address those directly; hooks stop the rest.

## Install

```text
/plugin install lakmus-dev --marketplace lakmuslabs/claude-plugins
```

In the `lakmus` repository this happens on its own: `.claude/settings.json` declares the
marketplace and enables the plugin.

## Skills

Each fires on its own when the task matches, and can be called by name
(`/lakmus-dev:architecture-first`).

| Skill | Fires on |
| --- | --- |
| `architecture-first` | A new module, public interface, format, CLI command or dependency. Produces a decision record and stops for validation before any code. |
| `suite-authoring` | Creating or reviewing a suite: layout, manifest fields, case design, thresholds, README, validation. |
| `target-adapter` | Implementing or changing an adapter for a model provider, an agent over HTTP, or an MCP server. |
| `scorer` | Writing a scorer, or changing how scores are aggregated, grouped or compared to thresholds. |
| `pair-testing` | Building counterfactual pair suites — two inputs identical except for one controlled variable. |
| `release` | Preparing a release: checks, changelog, version, tag. Never publishes by itself. |

## Subagents

| Agent | Model | Does |
| --- | --- | --- |
| `architect` | opus | Turns a request into a decision a developer can implement without guessing. Writes in `docs/` only. |
| `code-reviewer` | sonnet | Reviews a diff against the decision record it implements: correctness, async safety, determinism, typing, tests. Read-only. |
| `suite-reviewer` | opus | Reviews a suite's methodology before publication: validity, leakage, pair construction, statistics, data licensing, overclaiming. Read-only. |
| `security-reviewer` | sonnet | Reviews changes touching secrets, third-party suite code, archives or publishing. Read-only. |
| `test-writer` | sonnet | Writes tests from a specification or decision record rather than from the implementation. Writes under `tests/` only. |

Call one with `@agent-lakmus-dev:code-reviewer`, or just ask for the review by name.

## Hooks

`scripts/guard.py` runs before every file write and refuses three things: writing a file that looks
like a secret, touching reserved holdout cases, and editing the suite format specification while no
decision record is in progress. `scripts/format.py` runs after a Python file is written and applies
`ruff format` and `ruff check --fix`; it never blocks.

Both use `python3`. On Windows outside WSL, replace it with `python` in `hooks/hooks.json`.

## Adapting it

The rules are the project's, not universal. What is worth copying is the shape: one skill per
decision the assistant should not improvise, one reviewer per failure mode you actually fear, and a
hook on the one file that must never change quietly.
