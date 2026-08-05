# ADR-0005: Local Divergence Commit Removal Evaluation and Patch Diff Quality Previews for Fork Sync

## Status

Accepted

## Context

When synchronizing forked repositories with upstream parent repositories via `POST /repos/{owner}/{repo}/merge-upstream`, merge conflicts return an HTTP 409 status code. 

Previously, when an HTTP 409 conflict occurred:
1. The agent created a synchronization PR without inspecting why the conflict occurred.
2. The agent did not evaluate whether local commits (`ahead_by`) on the fork branch were blocking a clean upstream merge.
3. The reviewer had no inline patch snippets/code previews in the console output or PR description to assess the quality of changes before deciding whether to merge or reset local commits.

## Decision

We decided to enhance the fork conflict resolution workflow (`_resolve_fork_conflict` in `github_helper_agent.py`) by:

1. **Local Divergent Commit Analysis**: Analyzing comparison data (`ahead_by` vs `behind_by`) between the fork branch and upstream parent branch. Evaluating and highlighting that removing/rebasing local commits or hard-resetting the branch allows a clean fast-forward merge from the source repository.
2. **Patch Snippet Extraction**: Fetching file patch diffs (`files[].patch`) from the comparison API response and outputting code previews in both the terminal console logs and the body of generated synchronization PRs.

## Consequences

### Positive
- Clear visibility into why fork synchronization encounters HTTP 409 merge conflicts.
- Informed decision-making regarding whether local commits should be preserved or removed/reset to enable clean upstream sync.
- Previews of code patch diffs directly in console output and PR descriptions, enabling code quality review before merging.

### Negative
- Comparison payload responses for repositories with large numbers of modified files may increase API response payload size.
