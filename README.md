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

An automated GitHub Actions pipeline (`.github/workflows/container-daily-update.yml`) runs daily at 03:00 UTC to:
1. Sourcing the latest Chainguard Python zero-vulnerability base image.
2. Building and scanning the container image with **Trivy** (`CRITICAL,HIGH` severity gates).
3. Pushing updated images to GitHub Container Registry (`ghcr.io/jsoehner/gh-helper-agent:latest`).
4. Running automated maintenance across all target repositories.


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
- **[Gotcha 19: Distroless Container Debugging Limits](docs/TROUBLESHOOTING.md#gotcha-19)**: Chainguard minimal Python images (`cgr.dev/chainguard/python`) omit shells (`sh`/`bash`) and package managers; use multi-stage build targets or ephemeral debug containers for shell inspection.
- **[Gotcha 20: Environment File Volume vs Variable Mounts](docs/TROUBLESHOOTING.md#gotcha-20)**: `--env-file .env` injects credentials into container environment variables without mounting sensitive file system paths into non-root containers.
- **[Gotcha 21: Unmergeable PR Handling & Diagnostic Commenting](docs/TROUBLESHOOTING.md#gotcha-21)**: PRs that fail auto-merge return HTTP 405/422 due to failing CI checks or git merge conflicts. The agent posts diagnostic comments on PR issue endpoints and tracks items for maintainer rebase or automated cleanup.



## 📄 License
MIT License

