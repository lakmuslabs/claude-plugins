---
name: suite-authoring
description: Use when creating, editing or reviewing a Lakmus test suite (a folder with lakmus.yaml, cases, prompts and optional scorers), including the flagship suites in suites/. Covers folder layout, manifest fields, case design, thresholds, README content and validation.
---

# Authoring a Lakmus suite

The authoritative format is `docs/spec/suite-format.md`. Read it first; this skill is the practical checklist.

## Layout

```text
<domain>/<suite-name>/
├── lakmus.yaml
├── README.md
├── cases/<name>.jsonl        # public cases, one JSON object per line, unique "id"
├── cases/holdout.enc         # optional, never written by Claude
├── prompts/<name>.j2         # Jinja2 template rendered per case
├── scorers/<name>.py         # optional custom scorers
└── LICENSE
```

Scaffold with `uv run lakmus init <domain>/<suite-name>` when the CLI supports it.

## Manifest essentials

- `id` is `<domain>/<suite-name>`, kebab-case, stable forever.
- `version` is semver. Major = results are not comparable (cases, metric definitions or output contract changed). Minor = thresholds or documentation. Patch = typos.
- `target.kind` is one of `model`, `agent`, `mcp`; `target.output.schema` must describe exactly what scorers read.
- Every metric names a scorer (`builtin:<name>` or `scorers/<file>.py:<function>`) and, when results differ by subgroup, a `group_by`.
- Every metric used for pass/fail has a threshold, and the README justifies its value.
- `run.repeats` ≥ 3 for anything compared in a leaderboard; `temperature: 0` unless the suite explicitly tests sampling.

## Case design rules

1. Each case tests one thing. If a case fails, a reader must understand why from the case alone.
2. Expected answers come from a domain expert or a documented source, never from a model's output.
3. Cover the boring majority and the hard edge cases; tag cases with `meta.difficulty` and `meta.category`.
4. No personal data from real people. Use synthetic content; document how it was generated.
5. Keep at least 20% of cases as holdout for any suite meant for public leaderboards (maintainers create the encrypted file).
6. 50 cases is a minimum for a first version; prefer 200+ before publishing a leaderboard.

## README sections (required)

Objective · What a pass means · Method (how cases were built, by whom) · Metrics and thresholds (with rationale) · Known limits · Changelog · License and sources.

## Before finishing

- Run `uv run lakmus validate <path>` and fix every error.
- Run the suite once against a cheap or local target (`ollama:...`) and look at 5 failing cases by hand: a failure caused by the suite itself (ambiguous case, wrong expected answer, parser too strict) must be fixed in the suite.
- Ask the `suite-reviewer` agent to review methodology for any suite meant for publication.
