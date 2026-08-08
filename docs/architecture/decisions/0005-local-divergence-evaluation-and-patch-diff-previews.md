---
adr_id: "ADR-2026-0005"
title: "Local Divergence Commit Removal Evaluation and Patch Diff Quality Previews for Fork Sync"
status: "Accepted"
risk_tier: "Tier 2"
control_domains:
  - Architecture
  - DevSecOps
  - Operations
created_date: "2026-08-05"
proposed_date: "2026-08-05"
accepted_date: "2026-08-05"
implemented_date: "2026-08-05"
validated_date: "2026-08-05"
next_review_date: "2027-08-05"
review_triggers:
  - "Material architecture change"
  - "GitHub API comparison endpoint changes"
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
    approval_evidence: "PR #5 Code Review"
    date: "2026-08-05"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
affected_repositories:
  - "Forked repositories in user account"
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
    - "Divergent commit analysis"
    - "Inline patch diff previews"
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

# ADR-2026-0005: Local Divergence Commit Removal Evaluation and Patch Diff Quality Previews for Fork Sync

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**

- Created: 2026-08-05
- Proposed: 2026-08-05
- Accepted: 2026-08-05
- Implemented: 2026-08-05
- Validated: 2026-08-05
- Next review: 2027-08-05

## 2. Executive decision summary

- **Decision outcome:** Analyze comparison data (`ahead_by` vs `behind_by`) and include inline patch previews (`files[].patch`) in console output and synchronization PR descriptions.
- **Primary reason:** Resolve HTTP 409 fork merge conflicts by informing maintainers why conflicts occurred and providing diff visibility.
- **Key risk or trade-off:** Large comparison payloads for repositories with extensive diffs.
- **Required controls or conditions:** Truncate large patch outputs to avoid payload limit issues.
- **Implementation validation approach:** Execution tests against conflicting fork scenarios.

## 3. Context and problem statement

When synchronizing forked repositories with upstream parent repositories via `POST /repos/{owner}/{repo}/merge-upstream`, merge conflicts return an HTTP 409 status code. 

Previously, when an HTTP 409 conflict occurred:
1. The agent created a synchronization PR without inspecting why the conflict occurred.
2. The agent did not evaluate whether local commits (`ahead_by`) on the fork branch were blocking a clean upstream merge.
3. The reviewer had no inline patch snippets/code previews in the console output or PR description to assess the quality of changes before deciding whether to merge or reset local commits.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Business outcome | Clear visibility into fork conflict causes and code diffs | High |
| Maintainability and supportability | Quality code review previews in generated sync PRs | High |
| Operational resilience | Informed decision-making regarding rebase vs reset | Medium |

## 5. Options considered

| Option | Description | Pros | Cons | Risk / Control Implications | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option 1: Divergence Analysis with Inline Patch Extraction** | Inspect `ahead_by`/`behind_by` metrics and include file patch diffs (`files[].patch`) in sync PR bodies and terminal logs. | <ul><li>Complete transparency into conflict root causes.</li><li>Direct code previews without opening separate git web views.</li></ul> | Moderately larger API payload handling. | Low risk, high utility. | **Accepted** |
| **Option 2: Generic Sync PR without Diff Details** | Create a generic PR stating a conflict occurred without diff details. | Simple implementation. | Forces maintainers to manually run local git commands to see what conflicted. | Developer friction. | **Rejected** |
| **Option 3: Status quo / do nothing** | Fail silently on HTTP 409 conflicts. | No extra logic. | Out-of-sync forks remain broken. | Unmaintained fork drift. | **Rejected** |

## 6. Decision outcome

**We will:**
1. Analyze comparison metrics (`ahead_by` vs `behind_by`) in `_resolve_fork_conflict`.
2. Extract patch snippets (`files[].patch`) and embed them in terminal logs and PR descriptions.
3. Provide actionable recommendations (e.g. rebase or hard-reset) for clean upstream synchronization.

**We will not:** Force automatic branch reset without maintainer review.

**Decision scope:** Fork synchronization conflict handling.

**Out of scope:** Non-fork branch merges.

## 7. Rationale

Embedding patch previews and divergence metrics directly in PR descriptions enables maintainers to quickly evaluate quality and decide whether local commits should be reset or rebased.

## 8. Consequences and trade-offs

### Positive consequences
- Clear visibility into why fork synchronization encounters HTTP 409 merge conflicts.
- Informed decision-making regarding whether local commits should be preserved or removed/reset to enable clean upstream sync.
- Previews of code patch diffs directly in console output and PR descriptions, enabling code quality review before merging.

### Negative consequences
- Comparison payload responses for repositories with large numbers of modified files may increase API response payload size.

### Neutral or operational consequences
- Logs include file patch summaries.

### New constraints
- Patch previews must be truncated if they exceed markdown description limits.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Operations | Fork conflict diagnostic transparency | jsoehner | Comparison API parsing |
| DevSecOps | Code quality visibility before PR merge | jsoehner | Patch snippet embedding |

### Residual risk
- Residual risk description: Large patch payloads truncated in output.
- Residual risk owner: jsoehner
- Risk acceptance or exception ID: N/A
- Expiry or review date: 2027-08-05

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
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #5 | 2026-08-05 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-05 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | AGENT.md | Fork divergence analysis |
| Code implementation | github_helper_agent.py | `_resolve_fork_conflict` |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Add ahead/behind comparison logic | jsoehner | 2026-08-05 | github_helper_agent.py |
| Add patch snippet extraction | jsoehner | 2026-08-05 | github_helper_agent.py |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Fork conflict diff preview test | jsoehner | PR description check | Yes |

## 14. Supersession, review, and retirement

- Supersedes: None
- Superseded by: None
- Review triggers:
  - GitHub compare API patch payload structure changes

## 15. Open questions and actions

None.

## 16. References

- GitHub REST API Repositories Comparison documentation
