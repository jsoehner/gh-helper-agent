---
adr_id: "ADR-2026-0004"
title: "All-Repo Maintenance, Upstream Fork Synchronization, and Interactive Stale Repo Cleanup"
status: "Accepted"
risk_tier: "Tier 2"
control_domains:
  - Architecture
  - Operations
  - Security
created_date: "2026-08-04"
proposed_date: "2026-08-04"
accepted_date: "2026-08-04"
implemented_date: "2026-08-04"
validated_date: "2026-08-04"
next_review_date: "2027-08-04"
review_triggers:
  - "Material architecture change"
  - "GitHub API pagination or repository endpoint changes"
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
    approval_evidence: "PR #4 Code Review"
    date: "2026-08-04"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
affected_repositories:
  - "All repositories owned by authenticated user"
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
    - "Account-wide repository scanning"
    - "Automated fork synchronization"
    - "Interactive stale repository cleanup"
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

# ADR-2026-0004: All-Repo Maintenance, Upstream Fork Synchronization, and Interactive Stale Repo Cleanup

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**

- Created: 2026-08-04
- Proposed: 2026-08-04
- Accepted: 2026-08-04
- Implemented: 2026-08-04
- Validated: 2026-08-04
- Next review: 2027-08-04

## 2. Executive decision summary

- **Decision outcome:** Implement `--scan-and-fix-all` (paginated account-wide scan), `--sync-forks` (REST API fork sync), and `--check-stale` (interactive confirmation before repository deletion).
- **Primary reason:** Scale maintenance across large repository portfolios and keep forked repositories updated while guarding against accidental deletion.
- **Key risk or trade-off:** Destructive repository deletion requires interactive confirmation (`y/N`) and explicit `delete_repo` token scope.
- **Required controls or conditions:** Check 365-day inactivity cutoff and enforce interactive prompt before calling `DELETE /repos/{owner}/{repo}`.
- **Implementation validation approach:** Manual verification against test user repositories and API pagination tests.

## 3. Context and problem statement

As user account repository footprints grow, maintaining health, synchronization, and storage hygiene across all repositories becomes challenging:
1. **Unbounded Audits**: Previously, repository scanning was limited to a fixed recent limit (`limit=10`). A complete scan across all user-owned repositories was needed.
2. **Out-of-Sync Forks**: User forks often lag behind upstream parent repositories, requiring manual git fetches or web interface clicks to sync merged upstream updates.
3. **Stale/Abandoned Repositories**: Repositories inactive for over a year (e.g. legacy experiments, old forks) consume account noise and security surface area without providing active value.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Business outcome | Complete maintenance coverage across user account repositories | High |
| Operational resilience | Hands-free fork synchronization with upstream parents | High |
| Security and control posture | Safe interactive guardrails for repository deletion | High |

## 5. Options considered

### Option 1: Paginated Account Scan + REST Fork Sync + Interactive Stale Cleanup

**Description:** Use paginated API calls for complete coverage, REST merge-upstream endpoint for forks, and 365-day cutoff with interactive confirmation for stale repos.

**Pros:**
- Full account coverage without missing repositories.
- Zero manual web interface clicks for fork sync.
- Strict safety guard preventing unintended repository deletion.

**Cons:**
- Deletion requires interactive CLI terminal context.

**Risk/control implications:** High control, zero unintended deletion risk.

**Disposition:** Accepted

### Option 2: Automatic Background Deletion of Stale Repositories

**Description:** Automatically delete repositories older than 365 days without prompting.

**Pros:**
- Fully autonomous cleanup.

**Cons:**
- High risk of destroying unpushed historical code or archived projects.

**Risk/control implications:** Unacceptable risk of data loss.

**Disposition:** Rejected

### Option 3: Status quo / do nothing

**Description:** Manually audit, sync, and delete repositories via GitHub Web UI.

**Pros:**
- No code to maintain.

**Cons:**
- High friction and time consumption across multi-repo accounts.

**Risk/control implications:** Outdated forks and accumulating account noise.

**Disposition:** Rejected

## 6. Decision outcome

**We will:**
1. Implement `get_all_repositories()` with page-based pagination for `--scan-and-fix-all`.
2. Issue `POST /repos/{owner}/{repo}/merge-upstream` for forked repositories in `--sync-forks`.
3. Evaluate `pushed_at`/`updated_at` against a 365-day cutoff in `--check-stale` and require explicit interactive confirmation (`y/N`) before deletion.

**We will not:** Automatically delete any repository without explicit interactive confirmation.

**Decision scope:** Account-wide auditing, fork synchronization, and repository lifecycle management.

**Out of scope:** Third-party organization repository admin management.

## 7. Rationale

Adding paginated account scanning ensures no repositories are skipped, while interactive confirmation guards protect against accidental code loss when deleting stale repositories.

## 8. Consequences and trade-offs

### Positive consequences
- Total visibility and automated maintenance coverage across the entire GitHub user account.
- Hands-free synchronization of forked repositories via GitHub REST API.
- Safe lifecycle management for inactive repositories with explicit user confirmation guards.

### Negative consequences
- Synchronizing forks with upstream merge conflicts returns HTTP 409 and requires manual intervention.
- Deleting stale repositories requires a Personal Access Token explicitly granted `delete_repo` scope.

### Neutral or operational consequences
- Execution logs detail pagination parameters and timestamp evaluations.

### New constraints
- Stale repository deletion cannot be executed in non-interactive unattended scripts unless dry-run is enabled.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Operations | Destructive repository deletion flag | jsoehner | Interactive prompt requirement |
| Security | `delete_repo` token permission scope | jsoehner | Scope check & confirmation |

### Residual risk
- Residual risk description: User accidentally confirms deletion during interactive prompt.
- Residual risk owner: jsoehner
- Risk acceptance or exception ID: N/A
- Expiry or review date: 2027-08-04

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
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #4 | 2026-08-04 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-04 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | AGENT.md | Account-wide maintenance requirements |
| Code implementation | github_helper_agent.py | Fork sync and stale check handlers |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Implement get_all_repositories | jsoehner | 2026-08-04 | github_helper_agent.py |
| Implement merge-upstream handler | jsoehner | 2026-08-04 | github_helper_agent.py |
| Add interactive stale repo check | jsoehner | 2026-08-04 | github_helper_agent.py |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Interactive confirmation prompt test | jsoehner | CLI output logs | Yes |

## 14. Supersession, review, and retirement

- Supersedes: None
- Superseded by: None
- Review triggers:
  - GitHub merge-upstream API changes

## 15. Open questions and actions

None.

## 16. References

- GitHub REST API Repositories & Sync documentation
