# Lakmus Claude Code plugins

The Claude Code marketplace used to build [Lakmus](https://github.com/lakmuslabs/lakmus). It holds
one plugin, `lakmus-dev`, which encodes the project's working method so that the method survives
contact with an assistant: design before code, tests from the specification, specialised reviewers,
and hooks that refuse the edits this project cannot afford.

It is published because it is useful to read. If you maintain an evaluation project, the skills and
reviewers here are worth more as a worked example than as a dependency — fork them and change the
rules to yours.

## Install

```text
/plugin marketplace add lakmuslabs/claude-plugins
/plugin install lakmus-dev@lakmuslabs
```

The `lakmus` repository commits a `.claude/settings.json` that registers this marketplace and
enables the plugin, but the command above is still needed there: Claude Code does not fetch a
plugin from an external marketplace on the strength of project settings alone.

## What is in it

[`plugins/lakmus-dev`](plugins/lakmus-dev) — six skills, five subagents, and two hooks. Its
[README](plugins/lakmus-dev/README.md) describes each one and when it fires.

## Developing the plugin

Point Claude Code at a working copy instead of the published marketplace:

```bash
claude --plugin-dir ./plugins/lakmus-dev
```

Validate before committing. Continuous integration runs the same command:

```bash
claude plugin validate plugins/lakmus-dev
```

The hooks shell out to `python3`. On Windows outside WSL, replace `python3` with `python` in
`plugins/lakmus-dev/hooks/hooks.json`.

## Conventions and licence

Organisation conventions are in
[CONVENTIONS.md](https://github.com/lakmuslabs/.github/blob/main/CONVENTIONS.md). Plugin releases
use the `plugin/v<semver>` tag namespace. [Apache-2.0](LICENSE).
