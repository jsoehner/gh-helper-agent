# ADR-0001: Architecture & API Handling Strategy for gh-helper-agent

## Status

Accepted

## Context

`gh-helper-agent` automates repository maintenance by querying the GitHub REST API to list open issues, merge Dependabot pull requests, and deduplicate automated security scan notifications.

During initial implementation and testing, several architectural factors and GitHub API nuances were identified:
1. **GitHub Issues Endpoint Behavior**: `/repos/{owner}/{repo}/issues` returns both standard issues and pull requests (PRs are modeled as issues in GitHub's backend schema).
2. **Authentication & Rate Limits**: Unauthenticated REST requests are throttled to 60 requests/hour, which breaks multi-repo audits.
3. **Merge Workflow Constraints**: Attempting to merge PRs programmatically using the REST API requires checking mergeability and handling branch protection rules.

## Decision

We decided to:
1. **Implement Explicit Issue/PR Filtering**: In `get_open_issues_and_prs`, filter out items containing the `"pull_request"` key when analyzing open issues.
2. **Use Pure Standard Library HTTP Client**: Keep zero external runtime dependencies (`urllib.request` and `json`) for maximum portability across environment configurations and lightweight agent runners.
3. **Provide Dry-Run Mode**: Include `--dry-run` flag support in the core helper class to ensure safe preview execution prior to applying issue closures or pull request merges.

## Consequences

### Positive
- Prevents double-processing or incorrect mutation of PRs as issues.
- Ensures zero third-party package setup overhead for quick agent invocation.
- Gives users a safe mechanism (`--dry-run`) to audit API actions before writing state changes.

### Negative
- Pure `urllib.request` handling requires explicit status code and byte-stream decoding error logic compared to higher-level libraries like `requests` or `httpx`.
