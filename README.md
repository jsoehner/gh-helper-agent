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

## 🤖 Subagent Definition

This agent includes a prompt definition (`AGENT.md`) ready to be imported into subagent runners, AI coding assistants (such as Antigravity), or CI/CD automated workflow tasks.

## 📄 License
MIT License
