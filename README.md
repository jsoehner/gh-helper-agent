# GitHub Helper Agent (`gh-helper-agent`)

An automated maintenance and remediation agent for GitHub repositories.

`gh-helper-agent` connects to the GitHub REST API to inspect active repositories, review open issues and pull requests, auto-merge valid Dependabot updates, clean up duplicate security scan notifications, and execute fixes.

## 🚀 Features

- **Automated Repository Audit**: Analyzes your most active repositories sorted by recent updates.
- **Scan & Fix All Repositories**: Automatically iterates through all repositories to resolve open issues, Dependabot PRs, and security alerts (`--scan-and-fix-all`).
- **Fork Synchronization**: Syncs forked repositories with merged updates from their original upstream repositories (`--sync-forks`).
- **Stale Repository Cleanup**: Identifies repositories inactive for >1 year and prompts for confirmation before deletion (`--check-stale`).
- **Dependabot PR Automation**: Automatically merges approved dependency pull requests using squash merge.
- **Security Scan Deduplication**: Identifies automated scanner notifications (e.g., Semgrep findings) and deduplicates older historical issues while keeping the latest active issue open.
- **Notification Cleanup**: Automatically closes resolved dependency notification issues.
- **Dry-Run Support**: Inspect expected maintenance operations safely before executing changes.

## 📦 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jsoehner/gh-helper-agent.git
   cd gh-helper-agent
   ```

2. **Set Environment Variables**:
   Export your GitHub Personal Access Token (`GITHUB_TOKEN`):
   ```bash
   export GITHUB_TOKEN="ghp_your_github_token_here"
   ```

## 🛠️ Usage

### Run Audit in Dry-Run Mode (Safe Preview)
```bash
python3 github_helper_agent.py --owner jsoehner --dry-run --scan-and-fix-all --sync-forks --check-stale
```

### Scan and Fix All Repositories
```bash
python3 github_helper_agent.py --owner jsoehner --scan-and-fix-all
```

### Sync Forked Repositories
```bash
python3 github_helper_agent.py --owner jsoehner --sync-forks
```

### Identify Stale Repositories (>1 Year Inactive)
```bash
python3 github_helper_agent.py --owner jsoehner --check-stale
```

## 🤖 Subagent & Context Management

This repository includes:
- `AGENT.md`: Ready-to-import prompt definition for subagent runners, AI coding assistants (such as Antigravity), or CI/CD workflow tasks.
- `MEMORY.md`: Persistent memory file tracking repository architecture decisions, operational gotchas, and change logs for automated agents.


## ⚠️ Gotchas & Considerations

1. **GitHub Issues API Returns Pull Requests**: In the GitHub REST API (`/repos/{owner}/{repo}/issues`), PRs are considered issues. Always filter out items containing the `"pull_request"` key when fetching actual issues to prevent accidentally treating PRs as issues.
2. **Personal Access Token Scopes**: Writing or closing issues and merging PRs requires a PAT with `repo` scope (or fine-grained permissions for issues and pull requests). Unauthenticated or standard read requests will fail with HTTP 401/403 or silently fail write actions.
3. **GitHub API Rate Limits**: Unauthenticated API calls are limited to 60 requests/hour per IP, whereas authenticated requests allow up to 5,000 requests/hour. Always pass `GITHUB_TOKEN` in high-throughput or automated environments.
4. **Auto-Merge Conditions & CI Checks**: The agent's auto-merge mechanism uses squash merge (`PUT /repos/{owner}/{repo}/pulls/{number}/merge`). PRs must pass branch protection checks, required status checks, and merge conflict checks; otherwise, the merge API call returns HTTP 405/422.
5. **Local Package Manager Fallback for Dependency Upgrades**: Auto-merging remote Dependabot PRs may fail if breaking changes or build failures occur in isolated packages (e.g. `/httphandler` subdirectories). A local execution hook (e.g. `go get`, `npm update`) is required to run test validation before committing upgrades.
6. **Issue-Triggered Code Refactoring Scoping**: Automated refactoring hooks triggered by issue titles/labels (e.g. `refactor`, `tech debt`) must be explicitly scoped to prevent unintended AST modifications across multi-package repositories.
7. **Pagination Limits**: By default, listing endpoints (like `/user/repos` or `/issues`) return a limited page size (default 30, customizable up to 100 via `per_page`). When working across large repositories, handle pagination tokens or specify explicit limit parameters.
8. **Merged Dependency Branch PR Validation (HTTP 422)**: When automated dependency issues reference a branch (e.g., `automated/dependency-updates`), creating a PR will fail with HTTP 422 ("No commits between main and branch") if the changes are already merged. Always inspect branch diffs before PR creation, close obsolete issues, and delete the stale remote ref.
9. **Fork Upstream Synchronization API Requirements**: Syncing forked repos using `/repos/{owner}/{repo}/merge-upstream` requires write access to the fork and that the upstream repository branch is accessible. If there are merge conflicts between upstream and the fork, the API will return a 409 status code requiring manual conflict resolution.
10. **Repository Deletion (`delete_repo` Scope)**: Deleting repositories via `DELETE /repos/{owner}/{repo}` requires a token explicitly granted the `delete_repo` scope. Standard `repo` scope without `delete_repo` will return an HTTP 403 Forbidden error.
11. **ISO 8601 Timestamp Parsing for Stale Detection**: GitHub API returns timestamps in ISO 8601 format with a trailing `Z`. Standard Python `datetime.fromisoformat` in older versions expects `+00:00` instead of `Z`. Always replace `Z` with `+00:00` before parsing to ensure cross-python version compatibility.


## 📄 License
MIT License

