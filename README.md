# GitHub Helper Agent (`gh-helper-agent`)

An automated maintenance and remediation agent for GitHub repositories.

`gh-helper-agent` connects to the GitHub REST API to inspect active repositories, review open issues and pull requests, auto-merge valid Dependabot updates, clean up duplicate security scan notifications, and execute fixes.

## 🚀 Features

- **Automated Repository Audit**: Analyzes your most active repositories sorted by recent updates.
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
python3 github_helper_agent.py --owner jsoehner --limit 10 --dry-run
```

### Run Active Maintenance (Auto-merge & Fix Issues)
```bash
python3 github_helper_agent.py --owner jsoehner --limit 10
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

## 📄 License
MIT License

