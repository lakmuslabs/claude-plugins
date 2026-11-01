#!/usr/bin/env python3
"""PreToolUse guard for Lakmus.

Blocks (exit 2, reason on stderr, which Claude Code shows to Claude):
- any write to .env files or files that look like secrets;
- any write to reserved (holdout) test cases;
- edits to the suite format spec unless an ADR is being added or changed
  in the same working tree.
"""
import json
import os
import subprocess
import sys
from pathlib import PurePosixPath

SPEC_PATH = "docs/spec/suite-format.md"


def block(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def adr_in_progress(project_dir: str) -> bool:
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--", "docs/adr"],
            cwd=project_dir, capture_output=True, text=True, timeout=10,
        ).stdout
    except Exception:
        return False
    return bool(out.strip())


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    file_path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not file_path:
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    norm = file_path.replace("\\", "/")
    if os.path.isabs(norm):
        rel = os.path.relpath(norm, project_dir).replace("\\", "/")
    else:
        rel = norm
    name = PurePosixPath(rel).name.lower()

    if name == ".env" or name.startswith(".env.") or name.endswith((".pem", ".key")):
        block(f"Blocked: {rel} looks like a secrets file. Never write secrets; read them from environment variables.")

    if "/cases/" in f"/{rel}" and name.startswith("holdout"):
        block(f"Blocked: {rel} is a reserved holdout case file. Holdout cases are managed by maintainers only.")

    if rel == SPEC_PATH and not adr_in_progress(project_dir):
        block(
            "Blocked: the suite format spec is the project's central contract. "
            "Write or update an ADR in docs/adr/ first (use the architecture-first skill), "
            "then edit the spec and bump the format version."
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
