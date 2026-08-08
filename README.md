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

## 🐳 Docker Containerization & Daily Workflow

`gh-helper-agent` is containerized into a minimal, secure single-container image powered by **Chainguard Python** (`cgr.dev/chainguard/python`).

### Run via Docker

```bash
# Build the container image locally
docker build -t gh-helper-agent .

# Standard run using environment variables
docker run --rm \
  -e GITHUB_TOKEN="ghp_your_github_token_here" \
  -e GITHUB_OWNER="jsoehner" \
  gh-helper-agent --all

# Run with host Docker socket access (if running local container builds/scans)
docker run --rm \
  -v /run/docker.sock:/var/run/docker.sock \
  --env-file .env \
  gh-helper-agent --all
```

### Daily Security & Base Image Update Workflow

Automated GitHub Actions pipelines decouple container builds and security testing into separate, non-sequential workflows:
1. **Dependency Update Pipeline** (`.github/workflows/dependency-update.yml`): Runs daily at 03:00 UTC to build, tag, and publish updated Chainguard Python containers to GHCR (`ghcr.io/jsoehner/gh-helper-agent:latest`).
2. **Security Testing Pipeline** (`.github/workflows/security-testing.yml`): Runs daily at 04:00 UTC and on PRs to perform non-blocking **Trivy** container vulnerability scanning (`CRITICAL,HIGH` severity gates) and **Semgrep** SAST code scanning.


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


## ⚠️ Gotchas & Troubleshooting

For a complete reference of operational constraints and edge cases, see the full [Troubleshooting & Gotchas Guide](docs/TROUBLESHOOTING.md).

### Latest Gotchas & Highlights:
- **[Gotcha 21: Unmergeable PR Handling & Diagnostic Commenting](docs/TROUBLESHOOTING.md#gotcha-21)**: PRs that fail auto-merge return HTTP 405/422 due to failing CI checks or git merge conflicts. The agent posts diagnostic comments on PR issue endpoints and tracks items for maintainer rebase or automated cleanup.
- **[Gotcha 22: Decoupled Workflow Execution Boundaries](docs/TROUBLESHOOTING.md#gotcha-22)**: Splitting monolithic CI pipelines into separate workflows (`dependency-update.yml` vs `security-testing.yml`) ensures container publishing pipelines run independently of vulnerability and SAST scanning.
- **[Gotcha 23: Node 24 GitHub Actions Deprecation Warning](docs/TROUBLESHOOTING.md#gotcha-23)**: Bumping actions to Node 24 compatible major versions (`checkout@v7`, `build-push-action@v7`, `metadata-action@v6`) prevents runtime deprecation warnings.
- **[Gotcha 24: Immutable 40-Character Commit SHA Action Pinning](docs/TROUBLESHOOTING.md#gotcha-24)**: Using mutable action tags (e.g. `@v4`) introduces supply-chain vulnerabilities; all action steps must be explicitly pinned to 40-character commit SHAs.
- **[Gotcha 25: Gitleaks Action Strict Input Validation](docs/TROUBLESHOOTING.md#gotcha-25)**: `gitleaks/gitleaks-action@v3` rejects `with: args:`; omitting `args` allows default automated scanning.
- **[Gotcha 26: API Rate Limit Throttling & Backoff](docs/TROUBLESHOOTING.md#gotcha-26)**: Automatic retry with exponential backoff on HTTP 429/403 rate limit responses.
- **[Gotcha 27: Build-Phase Container Unit Tests](docs/TROUBLESHOOTING.md#gotcha-27)**: Running unit tests during Docker builder phase ensures zero regressions before container push.



## 📄 License
MIT License

