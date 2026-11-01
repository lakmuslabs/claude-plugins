---
name: scorer
description: Use when writing or changing a Lakmus scorer (built-in in src/lakmus/scorers or custom in a suite's scorers/ folder), or when changing how scores are aggregated, grouped or compared to thresholds.
---

# Writing a scorer

## Signature

```python
from lakmus.scorers import scorer, Score

@scorer(name="exact_match")
def exact_match(case: Case, output: TargetOutput) -> Score:
    ...
```

Pair scorers receive `PairOutputs` (`.a`, `.b`) instead of a single output. A scorer returns one `Score(value: float, details: dict)` per case; aggregation is the engine's job.

## Rules

- **Deterministic and pure.** No network, no randomness, no clock, no global state. Same inputs, same score.
- **Total.** A malformed or missing output yields a score (usually 0 or the worst value) plus `details["error"]`, never an exception.
- **Explicit direction.** Declare `higher_is_better` in the decorator; thresholds use `min` or `max` accordingly.
- **Explainable.** Put what a human needs to understand a failure in `details` (expected vs got, matched items).
- **LLM judge** scorers must take the judge model, rubric and prompt as explicit config, include them in the suite fingerprint, and set `deterministic=False` so the report flags them.

## Aggregation (engine side, for reference)

Mean per metric, 95% bootstrap confidence interval (1,000 resamples, fixed seed), and per-group values when `group_by` is set. Changing aggregation is an ADR-level change because it affects leaderboard comparability.

## Tests (required)

Table-driven pytest cases covering: perfect output, wrong output, partial output, empty output, malformed JSON, unicode and accents (French content), and for pair scorers identical pairs (score must be the neutral value).
