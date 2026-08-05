# ADR-0004: All-Repo Maintenance, Upstream Fork Synchronization, and Interactive Stale Repo Cleanup

## Status

Accepted

## Context

As user account repository footprints grow, maintaining health, synchronization, and storage hygiene across all repositories becomes challenging:
1. **Unbounded Audits**: Previously, repository scanning was limited to a fixed recent limit (`limit=10`). A complete scan across all user-owned repositories was needed.
2. **Out-of-Sync Forks**: User forks often lag behind upstream parent repositories, requiring manual git fetches or web interface clicks to sync merged upstream updates.
3. **Stale/Abandoned Repositories**: Repositories inactive for over a year (e.g. legacy experiments, old forks) consume account noise and security surface area without providing active value.

## Decision

We decided to implement three distinct operational modes in `github_helper_agent.py`:
1. **Full-Account Scanning (`--scan-and-fix-all`)**: Implement paginated repository fetching (`get_all_repositories()`) to iterate through all user-owned repos and execute issue/PR remediation.
2. **Upstream Fork Sync (`--sync-forks`)**: Automatically query forked repositories (`"fork": True`) and issue GitHub REST API `POST /repos/{owner}/{repo}/merge-upstream` requests to keep default branches updated with upstream changes.
3. **Interactive Stale Repo Management (`--check-stale`)**: Compare each repository's `pushed_at`/`updated_at` ISO 8601 timestamp against a 1-year (365 days) cutoff. For stale repositories, require explicit interactive user confirmation (`y/N`) before issuing a destructive `DELETE /repos/{owner}/{repo}` call.

## Consequences

### Positive
- Total visibility and automated maintenance coverage across the entire GitHub user account.
- Hands-free synchronization of forked repositories via GitHub REST API.
- Safe lifecycle management for inactive repositories with explicit user confirmation guards.

### Negative
- Synchronizing forks with upstream merge conflicts returns HTTP 409 and requires manual intervention.
- Deleting stale repositories requires a Personal Access Token explicitly granted `delete_repo` scope.
