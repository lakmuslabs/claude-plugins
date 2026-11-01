---
name: target-adapter
description: Use when implementing or modifying a Lakmus target adapter (model providers such as openai, anthropic, mistral, ollama, openai-compatible; agents over HTTP or Python; MCP servers over stdio or HTTP). Covers the Target protocol, fingerprinting, cost, error mapping, registration and tests.
---

# Implementing a target adapter

Read the `Target` protocol in `src/lakmus/targets/base.py` and section "Targets" of `docs/architecture/ARCHITECTURE.md` first.

## Contract

```python
class Target(Protocol):
    kind: Literal["model", "agent", "mcp"]
    async def setup(self, config: TargetConfig) -> None: ...
    async def invoke(self, case: RenderedCase) -> TargetOutput: ...
    async def teardown(self) -> None: ...
    def fingerprint(self) -> TargetFingerprint: ...
```

## Rules

- **Async only.** Use `httpx.AsyncClient` created in `setup` and closed in `teardown`. No blocking I/O.
- **No retries in the adapter.** Raise `TargetRateLimited` (429) or `TargetUnavailable` (5xx, timeouts) and let the engine retry with backoff. Raise `TargetBadRequest` for 4xx that will never succeed.
- **Never fail the run on one case.** Return `TargetOutput(error=...)` for case-level errors that are not retryable.
- **Secrets** come only from the env var named in config (`api_key_env`). Never log headers or keys; redact them in error messages.
- **Fingerprint** must include provider, model id, the exact model version or snapshot when the API returns it, and every generation parameter sent. If the provider gives no version, set `model_version=None`; the report will warn.
- **Usage and cost**: fill `usage` from the response. Compute `cost_usd` from `src/lakmus/targets/pricing.toml`; if the model is missing from the table, leave `cost_usd=None` rather than guessing.
- **Latency**: measure wall time around the request only, in milliseconds.
- **Agents**: map intermediate steps and tool calls into `trace` so `tool_called`-type scorers work.
- **MCP**: reuse the MCP client utilities; validate responses against the protocol and report violations in `TargetOutput.error`.

## Registration

Built-in adapters are registered in `src/lakmus/targets/__init__.py`. Third-party adapters expose an entry point in the `lakmus.targets` group:

```toml
[project.entry-points."lakmus.targets"]
myprovider = "lakmus_target_myprovider:MyProviderTarget"
```

CLI syntax: `--target <adapter>:<model-or-endpoint>`.

## Tests (required)

- Unit tests with `respx` for: success, 429, 500, timeout, malformed response, missing API key.
- A fingerprint test proving all parameters are included.
- One integration test marked `@pytest.mark.live`, skipped unless the env var is set.
