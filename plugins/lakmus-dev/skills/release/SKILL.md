---
name: release
description: Use when preparing a release of the lakmus package (version bump, changelog, tag, PyPI publication through GitHub Actions trusted publishing). Only when JIJI explicitly asks for a release.
---

# Releasing lakmus

1. Make sure `main` is green: `make check`.
2. Decide the version (semver). Any change to the suite format, `run.json` schema or CLI flags is at least minor; breaking ones are major after 1.0.
3. Update `CHANGELOG.md` (Keep a Changelog format): Added / Changed / Fixed / Security, with links to PRs.
4. Bump `version` in `pyproject.toml`.
5. Commit `chore(release): vX.Y.Z` and create the tag `vX.Y.Z` locally.
6. Stop. Show JIJI the changelog section and the commands to push (`git push && git push --tags`). Never push or publish yourself: the `release.yml` workflow publishes to PyPI via trusted publishing when the tag lands.
