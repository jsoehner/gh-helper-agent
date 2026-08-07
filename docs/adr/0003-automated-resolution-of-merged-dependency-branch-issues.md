---
adr_id: "ADR-2026-0003"
title: "Automated Resolution of Merged Dependency Branch Issues"
status: "Accepted"
risk_tier: "Tier 1"
control_domains:
  - Architecture
  - DevSecOps
  - Operations
created_date: "2026-08-03"
proposed_date: "2026-08-03"
accepted_date: "2026-08-03"
implemented_date: "2026-08-03"
validated_date: "2026-08-03"
next_review_date: "2027-08-03"
review_triggers:
  - "Material architecture change"
  - "GitHub git ref API changes"
adr_owner:
  name: "jsoehner"
  role: "Repository Maintainer"
decision_owner:
  name: "jsoehner"
  role: "Repository Maintainer"
accountable_role_or_forum: "gh-helper-agent Engineering"
acceptors:
  - name: "jsoehner"
    role: "Repository Maintainer"
    forum: "Architecture Review"
    approval_evidence: "PR #3 Code Review"
    date: "2026-08-03"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "GitHub REST API"
data_classification: "Internal"
external_exposure: "Outbound API calls to api.github.com"
third_party_dependency: "GitHub REST API"
model_or_ai_impact: "None"
residual_risk_owner:
  name: "jsoehner"
  role: "Repository Maintainer"
exceptions_or_risk_acceptances: []
technical_debt_items: []
technical_debt_assessment:
  impact: "None"
  score: 0
  rationale: "No new or unmanaged technical debt introduced by this decision."
  existing_debt_references: []
  new_or_changed_debt_items: []
  debt_owner:
    name: "jsoehner"
    role: "Repository Maintainer"
  remediation_plan: "N/A"
  remediation_due_date: "N/A"
  review_date: "N/A"
  related_exceptions_or_risk_acceptances: []
traceability:
  requirements:
    - "Automated obsolete branch and issue cleanup"
  diagrams: []
  threat_model: []
  risk_assessment: []
  standards_exception: []
  change_records: []
  pull_requests: []
  test_evidence: []
  deployment_evidence: []
  runbooks: []
  monitoring: []
supersedes: []
superseded_by: []
retention_classification: "Standard"
legal_hold: false
---

# ADR-2026-0003: Automated Resolution of Merged Dependency Branch Issues

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**

- Created: 2026-08-03
- Proposed: 2026-08-03
- Accepted: 2026-08-03
- Implemented: 2026-08-03
- Validated: 2026-08-03
- Next review: 2027-08-03

## 2. Executive decision summary

- **Decision outcome:** Verify branch diff status before opening PRs, auto-close obsolete tracking issues as `completed`, and delete stale dependency update branches.
- **Primary reason:** Prevent HTTP 422 API errors when attempting to create PRs for already merged branches and reduce repository clutter.
- **Key risk or trade-off:** Requires `repo` write scope on the GitHub Personal Access Token to delete git refs.
- **Required controls or conditions:** Verify zero unmerged commits (`ahead_by == 0`) before closing tracking issues and deleting refs.
- **Implementation validation approach:** Execution tests against merged branch scenarios.

## 3. Context and problem statement

During repository audits across user accounts, automated maintenance tools (such as dependency updater bots or previous CI pipeline runs) may create tracking issues to notify maintainers of automated dependency branches (e.g. `automated/dependency-updates`). 

When processing these issues during a maintenance review:
1. The tracking issue might report that a branch is ready for a PR, but the branch changes may have already been incorporated into `main`.
2. Attempting to create a Pull Request for a fully merged branch results in a GitHub REST API validation error (`HTTP 422: No commits between main and automated/dependency-updates`).
3. Leaving open tracking issues and stale branches creates clutter and degrades repository metrics.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Business outcome | Eliminate repo clutter and obsolete open issues | High |
| Operational resilience | Prevent HTTP 422 API exceptions during automated sweeps | High |
| Security and control posture | Safely clean up orphaned remote git branches | Medium |

## 5. Options considered

### Option 1: Diff Pre-Verification with Issue Closure & Ref Deletion

**Description:** Query comparison API (`GET /repos/{owner}/{repo}/compare/{base}...{head}`) before creating PRs; close issues and delete branches if fully merged.

**Pros:**
- Complete elimination of empty PR errors and stale branch clutter.
- Keeps repository metrics clean automatically.

**Cons:**
- Requires write permissions to delete git references.

**Risk/control implications:** Safe with proper commit diff checks.

**Disposition:** Accepted

### Option 2: Attempt PR Creation & Catch HTTP 422 Exception

**Description:** Attempt PR creation blindly and swallow HTTP 422 errors.

**Pros:**
- Simpler initial logic.

**Cons:**
- Leaves stale tracking issues open and orphaned branches in the repository.

**Risk/control implications:** Accumulates repository noise.

**Disposition:** Rejected

### Option 3: Status quo / do nothing

**Description:** Manually close tracking issues and delete merged branches.

**Pros:**
- No automated ref deletion risk.

**Cons:**
- Continuous manual maintenance overhead.

**Risk/control implications:** Manual toil.

**Disposition:** Rejected

## 6. Decision outcome

**We will:**
1. Verify branch diff status via GitHub comparison REST API before creating PRs.
2. Automatically close obsolete tracking issues as `completed`.
3. Issue `DELETE /repos/{owner}/{repo}/git/refs/heads/{branch_name}` to purge merged feature branches.

**We will not:** Delete unmerged branches containing active commits (`ahead_by > 0`).

**Decision scope:** Dependency tracking issue handling and branch lifecycle cleanup.

**Out of scope:** Non-dependency feature branch deletions.

## 7. Rationale

Checking diff status prior to PR creation guarantees clean API operations and ensures that completed work does not leave orphaned issues or stale git branches behind.

## 8. Consequences and trade-offs

### Positive consequences
- Prevents HTTP 422 validation errors when attempting to open empty PRs.
- Keeps repository issue trackers clean and accurate.
- Automatically cleans up orphaned remote git branches.

### Negative consequences
- Deleting branches requires proper `repo` write permissions on the authenticated Personal Access Token.

### Neutral or operational consequences
- Logs explicit branch comparison metrics during execution.

### New constraints
- Branch deletion must always be preceded by commit diff verification.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Operations | Automated issue state transition & branch deletion | jsoehner | Comparison API check |
| Security | PAT write scope requirement for ref deletion | jsoehner | Permission check |

### Residual risk
- Residual risk description: Accidental deletion if target branch name is improperly parsed.
- Residual risk owner: jsoehner
- Risk acceptance or exception ID: N/A
- Expiry or review date: 2027-08-03

## Technical debt assessment

**Debt impact:** None

**Technical debt score:** 0

**Assessment rationale:**

No new or unmanaged technical debt introduced by this architecture decision.

| Debt item | New, increased, reduced, or none | Driver | Impact | Owner | Remediation plan | Due date | Evidence |
|---|---|---|---|---|---|---|---|
| None | None | N/A | None | jsoehner | N/A | N/A | Code review |

### Existing debt affected

- None

### New or changed debt

- None

### Net debt impact

Zero net technical debt.
## 10. Governance and acceptance

| Role or forum | Named person | Responsibility | Evidence | Date |
|---|---|---|---|---|
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #3 | 2026-08-03 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-03 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | AGENT.md | Obsolete issue resolution |
| Code implementation | github_helper_agent.py | Branch comparison & ref deletion |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Add branch diff verification | jsoehner | 2026-08-03 | github_helper_agent.py |
| Add issue auto-closure | jsoehner | 2026-08-03 | github_helper_agent.py |
| Add git ref deletion | jsoehner | 2026-08-03 | github_helper_agent.py |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Obsolete issue resolution test | jsoehner | Execution logs | Yes |

## 14. Supersession, review, and retirement

- Supersedes: None
- Superseded by: None
- Review triggers:
  - GitHub compare API endpoint updates

## 15. Open questions and actions

None.

## 16. References

- GitHub REST API Git Refs & Compare documentation
