#!/usr/bin/env python3
"""PostToolUse formatter: ruff format + ruff check --fix on edited Python files.

Never blocks: remaining problems are reported by `make check`.
"""
import json
import shutil
import subprocess
import sys


def run(cmd: list[str]) -> None:
    try:
        subprocess.run(cmd, capture_output=True, timeout=60)
    except Exception:
        pass


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    file_path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not file_path.endswith(".py"):
        sys.exit(0)

    if shutil.which("uv"):
        prefix = ["uv", "run", "--quiet", "ruff"]
    elif shutil.which("ruff"):
        prefix = ["ruff"]
    else:
        sys.exit(0)

    run(prefix + ["format", file_path])
    run(prefix + ["check", "--fix", "--quiet", file_path])
    sys.exit(0)


if __name__ == "__main__":
    main()
