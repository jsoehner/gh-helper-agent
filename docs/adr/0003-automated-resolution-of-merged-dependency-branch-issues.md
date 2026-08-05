# ADR-0003: Automated Resolution of Merged Dependency Branch Issues

## Status

Accepted

## Context

During repository audits across user accounts, automated maintenance tools (such as dependency updater bots or previous CI pipeline runs) may create tracking issues to notify maintainers of automated dependency branches (e.g. `automated/dependency-updates`). 

When processing these issues during a maintenance review:
1. The tracking issue might report that a branch is ready for a PR, but the branch changes may have already been incorporated into `main`.
2. Attempting to create a Pull Request for a fully merged branch results in a GitHub REST API validation error (`HTTP 422: No commits between main and automated/dependency-updates`).
3. Leaving open tracking issues and stale branches creates clutter and degrades repository metrics.

## Decision

We decided to:
1. **Verify Branch Diff Status Before PR Creation**: Before creating a Pull Request for automated dependency branches, check whether there are unmerged commits between `main` and the feature branch.
2. **Auto-Close Obsolete Tracking Issues**: If a tracking issue references a branch that is already fully merged or has no diff relative to `main`, automatically close the issue as `completed`.
3. **Delete Obsolete Branches**: Automatically issue a `DELETE /repos/{owner}/{repo}/git/refs/heads/{branch_name}` call to remove stale dependency update branches after closing the corresponding issue.

## Consequences

### Positive
- Prevents HTTP 422 validation errors when attempting to open empty PRs.
- Keeps repository issue trackers clean and accurate.
- Automatically cleans up orphaned remote git branches.

### Negative
- Deleting branches requires proper `repo` write permissions on the authenticated Personal Access Token.
