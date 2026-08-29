# GitHub Helper Agent (`gh-helper-agent`)

An automated maintenance and remediation agent for GitHub repositories.

`gh-helper-agent` connects to the GitHub REST API to inspect active repositories, review open issues and pull requests, auto-merge valid Dependabot updates, clean up duplicate security scan notifications, and execute fixes.

## 🚀 Features

- **Automated Repository Audit**: Analyzes your most active repositories sorted by recent updates.
- **Dependabot Alert Assessment & Remediation**: Audits open Dependabot security advisories across repositories, classifies them into 6 remediation strategies (`MERGE_DEPENDABOT_PR`, `PATCH_UPGRADE`, `MAJOR_UPGRADE`, `TRANSITIVE_LOCKFILE_UPDATE`, `WORKAROUND_OR_MITIGATION`, `DEV_DEPENDENCY_RISK_ACCEPTANCE`), and outputs ecosystem-tailored CLI commands (`--check-alerts`).
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

### Assess & Review Dependabot Alerts Across Repositories
```bash
# Audit all open Dependabot alerts across account
python3 github_helper_agent.py --owner jsoehner --check-alerts

# Filter alerts by severity and ecosystem
python3 github_helper_agent.py --owner jsoehner --check-alerts --severity critical --ecosystem npm

# Audit alerts for a specific repository
python3 github_helper_agent.py --owner jsoehner --repo my-app --check-alerts
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

### Highlights & Gotchas Reference:
- **[Gotcha 1-10: Core API & Permission Constraints](docs/TROUBLESHOOTING.md#gotcha-1)**: GitHub REST API issues vs PR filtering, PAT scope requirements (`repo`, `delete_repo`), rate limit thresholds, auto-merge squash requirements, and pagination.
- **[Gotcha 11-17: Timestamps, Fork Sync & Container Mounts](docs/TROUBLESHOOTING.md#gotcha-11)**: ISO 8601 `Z` parsing, divergent local commit handling (`HTTP 409`), patch diff previews, `.env` parsing hierarchy, and host Docker socket `/run/docker.sock` volume mounting.
- **[Gotcha 18-20: Socket Permissions & Distroless Containers](docs/TROUBLESHOOTING.md#gotcha-18)**: Container non-root socket permission boundaries, Chainguard minimal image interactive debugging limits, and secret environment volume vs variable injection.
- **[Gotcha 21: Unmergeable PR Handling & Diagnostic Commenting](docs/TROUBLESHOOTING.md#gotcha-21)**: Diagnostic PR issue commenting and status tracking for PRs returning HTTP 405/422.
- **[Gotcha 22: Decoupled Workflow Execution Boundaries](docs/TROUBLESHOOTING.md#gotcha-22)**: Independent scheduling for container image publishing and security/SAST scanning workflows.
- **[Gotcha 23: Node 24 GitHub Actions Deprecation Warning](docs/TROUBLESHOOTING.md#gotcha-23)**: Node 24 runtime support via updated action versions.
- **[Gotcha 24: Immutable 40-Character Commit SHA Action Pinning](docs/TROUBLESHOOTING.md#gotcha-24)**: Supply chain hardening via explicit commit SHA action pinning.
- **[Gotcha 25: Gitleaks Action Strict Input Validation](docs/TROUBLESHOOTING.md#gotcha-25)**: `gitleaks/gitleaks-action@v3` parameter schema compliance.
- **[Gotcha 26: API Rate Limit Throttling & Backoff](docs/TROUBLESHOOTING.md#gotcha-26)**: Automatic retry with exponential backoff on HTTP 429/403 rate limit responses.
- **[Gotcha 27: Build-Phase Container Unit Tests](docs/TROUBLESHOOTING.md#gotcha-27)**: Running unit tests during Docker builder phase ensures zero regressions before container push.
- **[Gotcha 28: Dependabot Security Alerts API & Strategy Classification](docs/TROUBLESHOOTING.md#gotcha-28)**: Dependabot alerts API querying, semver jump classification, and ecosystem-specific remediation planning.



## 📄 License
MIT License

