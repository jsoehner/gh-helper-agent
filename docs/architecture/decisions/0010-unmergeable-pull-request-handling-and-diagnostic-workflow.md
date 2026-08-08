---
adr_id: "ADR-2026-0010"
title: "Unmergeable Pull Request Handling and Diagnostic Workflow"
status: "Accepted"
risk_tier: "Tier 1"
control_domains:
  - Architecture
  - DevSecOps
  - Operations
created_date: "2026-08-07"
proposed_date: "2026-08-07"
accepted_date: "2026-08-07"
implemented_date: "2026-08-07"
validated_date: "2026-08-07"
next_review_date: "2027-08-07"
review_triggers:
  - "Material architecture change"
  - "GitHub Pull Request REST API behavior change"
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
    approval_evidence: "PR #10 Code Review"
    date: "2026-08-07"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "GitHub REST API"
data_classification: "Internal"
external_exposure: "PR comments on api.github.com"
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
    - "Unmergeable PR diagnostic feedback"
    - "Automated PR closure option"
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

# ADR-2026-0010: Unmergeable Pull Request Handling and Diagnostic Workflow

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**

- Created: 2026-08-07
- Proposed: 2026-08-07
- Accepted: 2026-08-07
- Implemented: 2026-08-07
- Validated: 2026-08-07
- Next review: 2027-08-07

## 2. Executive decision summary

- **Decision outcome:** Implement `handle_unmergeable_pr` diagnostic workflow to post explanatory PR comments when HTTP 405/422 errors occur, support optional PR closure, and format audit totals clearly.
- **Primary reason:** Inform maintainers why specific PRs cannot be auto-merged (e.g. failing CI or git merge conflicts).
- **Key risk or trade-off:** Slight increase in GitHub API call footprint for posting comments.
- **Required controls or conditions:** Verify PR status before posting duplicate diagnostic comments.
- **Implementation validation approach:** Execution test against failing PR scenario.

## 3. Context and problem statement

During repository audits across large GitHub organizations, pull requests (such as Dependabot version updates, badge updates, or manual PRs) may fail to auto-merge. Typical causes include failing or pending CI check runs, required status check policies, or git merge conflicts against the target branch (`main`/`master`).

When `gh-helper-agent` attempts to auto-merge unmergeable PRs via `PUT /repos/{owner}/{repo}/pulls/{number}/merge`, the GitHub API returns HTTP 405 (Method Not Allowed) or HTTP 422 (Unprocessable Entity). Previously, failed auto-merge attempts were logged without feedback, leaving PR authors and maintainers unaware of why automated maintenance bypassed specific PRs.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Business outcome | Clear maintainer visibility into blocking PR issues | High |
| Maintainability and supportability | Complete traceability for automated merge attempts | High |
| Operational resilience | Safe error handling preventing silent script bypasses | Medium |

## 5. Options considered

| Option | Description | Pros | Cons | Risk / Control Implications | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option 1: Structured Diagnostic Workflow with PR Comments** | Catch HTTP 405/422 merge errors, inspect PR state, post diagnostic PR comments, and provide option for automated closure. | <ul><li>Immediate actionable feedback in PR discussions.</li><li>Audit output explicitly logs total items audited and unmergeable causes.</li></ul> | Consumes additional API calls for comment creation. | Low risk, high maintainer utility. | **Accepted** |
| **Option 2: Log Warning to Console Only** | Log a local console warning without commenting on the GitHub PR. | Saves API requests. | PR authors looking at GitHub web interface have no context on why auto-merge bypassed their PR. | Reduced visibility. | **Rejected** |
| **Option 3: Status quo / do nothing** | Ignore merge failure API exceptions silently. | Simple code path. | Silent failures and unmanaged PR accumulation. | Operational blindness. | **Rejected** |

## 6. Decision outcome

**We will:**
1. Catch HTTP 405 / 422 exceptions during PR merge attempts.
2. Invoke `handle_unmergeable_pr` to post diagnostic comments on the PR issue thread.
3. Update repo audit formatting to show `Total Open Items Audited: X (Y issues, Z PRs)`.

**We will not:** Silently swallow PR merge errors or post duplicate diagnostic comments.

**Decision scope:** Unmergeable PR diagnostic workflow and logging.

**Out of scope:** Third-party CI fix generation.

## 7. Rationale

Posting clear diagnostic comments directly on failing PRs informs maintainers of CI or conflict issues, bridging the gap between automated tools and developer remediation.

## 8. Consequences and trade-offs

### Positive consequences
- **Maintainer Visibility**: Maintainers receive immediate actionable feedback directly on unmerged PRs detailing blocking CI checks or merge conflicts.
- **Robust Audit Summary**: Execution summaries clearly distinguish between successfully merged PRs, unmergeable PRs, and manual review candidates.
- **Traceability**: Audit logs and PR discussion threads maintain complete history of automated intervention attempts.

### Negative consequences
- **API Rate Footprint**: Posting diagnostic comments increases GitHub API call volume for repositories with multiple unmergeable PRs. (Mitigated by checking PR status before commenting).

### Neutral or operational consequences
- Audit summary outputs include detailed PR breakdowns.

### New constraints
- Diagnostic comments must be clear and non-repetitive.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Operations | Automated PR diagnostic feedback | jsoehner | Issue comment handler |
| DevSecOps | Complete merge attempt traceability | jsoehner | Execution summary logs |

### Residual risk
- Residual risk description: GitHub API comment endpoint rate limit on large batch PR runs.
- Residual risk owner: jsoehner
- Risk acceptance or exception ID: N/A
- Expiry or review date: 2027-08-07

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
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #10 | 2026-08-07 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-07 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | AGENT.md | Diagnostic workflow specification |
| Code implementation | github_helper_agent.py | `handle_unmergeable_pr` |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Add handle_unmergeable_pr | jsoehner | 2026-08-07 | github_helper_agent.py |
| Update audit summary formatting | jsoehner | 2026-08-07 | github_helper_agent.py |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Diagnostic comment post test | jsoehner | PR comment logs | Yes |

## 14. Supersession, review, and retirement

- Supersedes: None
- Superseded by: None
- Review triggers:
  - GitHub PR merge endpoint status code changes

## 15. Open questions and actions

None.

## 16. References

- GitHub REST API Pull Requests & Issue Comments documentation
