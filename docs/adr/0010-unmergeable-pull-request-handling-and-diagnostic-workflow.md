# ADR-0010: Unmergeable Pull Request Handling and Diagnostic Workflow

## Status

Accepted

## Context

During repository audits across large GitHub organizations, pull requests (such as Dependabot version updates, badge updates, or manual PRs) may fail to auto-merge. Typical causes include failing or pending CI check runs, required status check policies, or git merge conflicts against the target branch (`main`/`master`).

When `gh-helper-agent` attempts to auto-merge unmergeable PRs via `PUT /repos/{owner}/{repo}/pulls/{number}/merge`, the GitHub API returns HTTP 405 (Method Not Allowed) or HTTP 422 (Unprocessable Entity). Previously, failed auto-merge attempts were logged without feedback, leaving PR authors and maintainers unaware of why automated maintenance bypassed specific PRs.

## Decision

We decided to:
1. Implement a structured unmergeable PR diagnostic workflow (`handle_unmergeable_pr`) in `github_helper_agent.py`.
2. Automatically post diagnostic comments on PR issue endpoints explaining why auto-merge could not be completed (e.g., CI failures, pending checks, or merge conflicts).
3. Support optional automated closure of stale or invalid failing PRs (`close_pr`).
4. Update repo audit formatting to clearly reflect total audited items per repository (`[*] Repository: <name> | Total Open Items Audited: X (Y issues, Z PRs)`).
5. Document unmergeable PR operational gotchas in `README.md` and `MEMORY.md`.

## Consequences

### Positive
- **Maintainer Visibility**: Maintainers receive immediate actionable feedback directly on unmerged PRs detailing blocking CI checks or merge conflicts.
- **Robust Audit Summary**: Execution summaries clearly distinguish between successfully merged PRs, unmergeable PRs, and manual review candidates.
- **Traceability**: Audit logs and PR discussion threads maintain complete history of automated intervention attempts.

### Negative
- **API Rate Footprint**: Posting diagnostic comments increases GitHub API call volume for repositories with multiple unmergeable PRs. (Mitigated by checking PR status before commenting).
