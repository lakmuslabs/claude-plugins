---
name: pair-testing
description: Use when building counterfactual pair suites (two inputs identical except for one attribute) to measure fairness or robustness, including the flagship French CV screening fairness study.
---

# Counterfactual pair testing

The method: build pairs of inputs identical except for one controlled variable, run both through the target, and measure how much the output changes. No ground truth is needed: a fair, robust system gives the same answer to both.

## Building pairs

1. Start from a base document (e.g. a synthetic CV) written once, realistic, with no attribute that hints at the tested variable.
2. Derive variant A and variant B by changing **only** the tested variable: name, gender markers (including grammatical agreement in French), age or birth year, address, career gap. Everything else must be byte-identical; write a test that diffs A and B and fails if more than the intended fields differ.
3. Randomise which variant is presented first when the target sees both, and run each variant in a separate call by default.
4. Balance: each value of the variable appears equally often as A and as B, across jobs and seniority levels.

## Sources for variable values

Use documented public sources (e.g. official first-name statistics) and record the source, date and selection rule in the suite README. Never invent lists ad hoc and never use real people's identities.

## Metrics

- `pair_gap`: mean absolute difference of the numeric score.
- `pair_flip`: share of pairs where the decision changes.
- Report both per variable value (`group_by`), with confidence intervals, and the direction of the gap.

## Interpretation and wording

- A gap is a measured difference on these synthetic inputs, not proof of how a deployed product behaves. Say so in the README and in any published study.
- Publish method, cases and code so anyone can reproduce the result.
- Before publishing results naming a vendor, have the `suite-reviewer` agent check methodology, and give the vendor the chance to reproduce.
