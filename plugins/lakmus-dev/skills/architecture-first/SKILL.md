---
name: architecture-first
description: Use BEFORE writing code for any new module, public interface, file format, CLI command, dependency or cross-cutting change in Lakmus. Produces a short design rationale and an ADR in docs/adr/, updates docs/architecture when needed, then stops for validation. Also use when asked to "design", "plan", "architect" or "write an ADR".
---

# Architecture first

JIJI's rule for this project: a concise rationale and the architecture documentation come before any code. Follow these steps in order and do not skip to implementation.

## 1. Decide whether an ADR is needed

An ADR is required when the change:
- adds or changes a public interface (CLI command or flag, `Target` protocol, scorer signature, `run.json` field, suite manifest field);
- touches `docs/spec/suite-format.md` (also requires a format version bump);
- adds a runtime dependency;
- changes how data, secrets or third-party code are handled;
- picks between several reasonable designs.

A bug fix, a refactor with no interface change, or a test addition needs no ADR: give a 3-line rationale and continue.

## 2. Read the sources of truth

Read `docs/architecture/ARCHITECTURE.md`, `docs/spec/suite-format.md` and the existing ADRs in `docs/adr/` that relate to the change. If the request contradicts an accepted ADR, say so and propose superseding it rather than silently diverging.

## 3. Write the ADR

Create `docs/adr/NNNN-short-kebab-title.md` with the next free number, using this template:

```markdown
# NNNN. <Decision title>

- Status: proposed
- Date: YYYY-MM-DD
- Deciders: JIJI

## Context
What problem we are solving and the constraints (2–6 sentences).

## Decision
What we will do, stated plainly. Include the interface (signature, schema, CLI syntax) when there is one.

## Alternatives considered
- Option A — why not.
- Option B — why not.

## Consequences
- Positive:
- Negative / costs:
- Impact on the suite format spec: none | requires format bump to X.Y
- Impact on run.json / leaderboard comparability: none | ...

## Implementation plan
Ordered steps, each small enough for one commit, with the tests that prove it.
```

Keep it under one page. Write in English (the repository is open source).

## 4. Update the architecture docs

If module boundaries, data flow or interfaces change, update `docs/architecture/ARCHITECTURE.md` in the same change. If the spec changes, edit `docs/spec/suite-format.md` and bump `lakmus` format version in the spec header.

## 5. Stop and ask for validation

End your turn with: the rationale in 3–5 lines (in French, to JIJI), the path of the ADR, and the question "Je valide et je passe à l'implémentation ?". Do not write production code until JIJI confirms. Once confirmed, set the ADR status to `accepted`.
