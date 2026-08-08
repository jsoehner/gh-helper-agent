# Repository Persistent Memory (`MEMORY.md`)

This file stores persistent context, operational insights, architectural decisions, and repository guidelines for `gh-helper-agent`. Agents working in this codebase should read and update this document when significant changes or discoveries occur.

---

## 📌 Project Overview & Purpose

`gh-helper-agent` is an automated repository maintenance tool designed to run periodic audits across GitHub repositories.
Key functions:
- Auto-merge Dependabot PRs using squash merges.
- Deduplicate duplicate automated security scan issues (keeping the latest active issue open).
- Close automated dependency notification issues.

---

## 🧠 Architectural Insights & Operational Memory

1. **GitHub Issues Endpoint Traversal**:
   - `/repos/{owner}/{repo}/issues` returns both standard issues **and** pull requests.
   - Always filter out items containing `"pull_request"` in dictionary keys before processing issues.

2. **Authentication & Token Handling**:
   - Requires `GITHUB_TOKEN` set in environment or loaded from local configuration (`~/.github_token`).
   - Token must have `repo` permissions to perform issue patching or PR merging.
   - For git CLI operations (such as `git push`), **prefer using PAT authenticated HTTPS URLs (`https://${GITHUB_TOKEN}@github.com/...`) first** over SSH to prevent interactive key passphrase/askpass prompts.
   - Do **NOT** commit raw secret tokens to this repository.

3. **Standard Library Constraints**:
   - `github_helper_agent.py` relies exclusively on Python standard library modules (`urllib.request`, `json`, `os`, `sys`, `argparse`). Keep external runtime dependencies to zero.

4. **Safety & Execution Controls**:
   - Always verify changes with `--dry-run` flag before executing write mutations in production environments.

---

## 📝 Change Log & Decision History

| Date | Category | Summary |
| --- | --- | --- |
| 2026-08-05 | Architecture | Created ADR-0001 (`docs/architecture/decisions/0001-architecture-and-api-handling-strategy.md`) for API handling strategy. |
| 2026-08-05 | Architecture | Created ADR-0002 (`docs/architecture/decisions/0002-hybrid-dependency-upgrades-and-code-refactoring.md`) for dependency upgrades & refactoring. |
| 2026-08-05 | Architecture | Created ADR-0003 (`docs/architecture/decisions/0003-automated-resolution-of-merged-dependency-branch-issues.md`) for handling merged dependency issues & stale branches. |
| 2026-08-05 | Architecture | Created ADR-0004 (`docs/architecture/decisions/0004-all-repo-scan-fork-sync-and-stale-cleanup.md`) for full-account scanning, fork sync, and stale repo cleanup. |
| 2026-08-05 | Architecture | Created ADR-0005 (`docs/architecture/decisions/0005-local-divergence-evaluation-and-patch-diff-previews.md`) for local commit removal evaluation & patch diff previews during fork sync. |
| 2026-08-05 | Documentation | Updated Gotchas in `README.md` with fork local divergence handling and diff quality review. |
| 2026-08-05 | Memory System | Established `MEMORY.md` for in-repo persistent agent memory. |
| 2026-08-07 | Architecture | Created ADR-0006 (`docs/architecture/decisions/0006-environment-variable-loading-via-dotenv.md`) & implemented zero-dependency `.env` parsing in `github_helper_agent.py`. |
| 2026-08-07 | Containerization | Created Dockerfile using Chainguard Python base image & ADR-0007 (`docs/architecture/decisions/0007-containerization-via-chainguard-minimal-python-base-image.md`). |
| 2026-08-07 | Automation | Created daily container rebuild & vulnerability scan workflow (`.github/workflows/container-daily-update.yml`) & ADR-0008 (`docs/architecture/decisions/0008-daily-container-rebuild-and-vulnerability-scanning-workflow.md`). |
| 2026-08-07 | Architecture | Documented host Docker socket mounting & created ADR-0009 (`docs/architecture/decisions/0009-container-host-socket-mount-and-socket-activation-handling.md`). |
| 2026-08-07 | Workflow | Implemented unmergeable PR management workflow with diagnostic PR commenting, local rebase/conflict resolution hooks, and status tracking in `github_helper_agent.py`. |
| 2026-08-07 | Documentation | Refactored Gotchas into dedicated `docs/TROUBLESHOOTING.md` guide; updated `README.md` with links to the last 3 added gotchas (19-21). |
| 2026-08-07 | Architecture | Created ADR-0011 (`docs/architecture/decisions/0011-decoupled-dependency-update-and-security-testing-workflows.md`), superseding ADR-0008, to separate dependency update and security testing CI workflows with Node 24 support and explicit 40-character SHA pinning. Added Gotchas 22-25 to `docs/TROUBLESHOOTING.md` and updated `README.md`. |
| 2026-08-08 | Architecture & Testing | Created ADR-0012 (`docs/architecture/decisions/0012-resilient-api-rate-limiting-and-unit-testing-infrastructure.md`), superseding ADR-0001, implementing HTTP 429/403 rate-limiting retries with exponential backoff and `Retry-After` header parsing in `github_helper_agent.py`. Established `test_github_helper_agent.py` zero-dependency test suite integrated into `Dockerfile` build stage and `security-testing.yml`. Added Gotchas 26-27 to `docs/TROUBLESHOOTING.md` and updated `README.md`. |



---

## 🛠️ Instructions for AI Agents

When interacting with this repository:
1. **Read `MEMORY.md`** first to align on repository context and operational rules.
2. **Update `MEMORY.md`** whenever a new gotcha, architectural pattern, or significant feature is introduced.
3. Keep entries structured, concise, and focused on maintaining codebase quality.
