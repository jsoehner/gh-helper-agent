---
adr_id: "ADR-2026-0001"
title: "Architecture & API Handling Strategy for gh-helper-agent"
status: "Accepted"
risk_tier: "Tier 1"
control_domains:
  - Architecture
  - API
  - DevSecOps
created_date: "2026-08-01"
proposed_date: "2026-08-01"
accepted_date: "2026-08-01"
implemented_date: "2026-08-01"
validated_date: "2026-08-01"
next_review_date: "2027-08-01"
review_triggers:
  - "Material architecture change"
  - "GitHub API v3 deprecation or structural change"
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
    approval_evidence: "PR #1 Code Review"
    date: "2026-08-01"
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
    - "Zero external runtime dependencies"
    - "Safe dry-run preview execution"
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

# ADR-2026-0001: Architecture & API Handling Strategy for gh-helper-agent

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**

- Created: 2026-08-01
- Proposed: 2026-08-01
- Accepted: 2026-08-01
- Implemented: 2026-08-01
- Validated: 2026-08-01
- Next review: 2027-08-01

## 2. Executive decision summary

- **Decision outcome:** Use pure standard library HTTP clients (`urllib.request`), filter PRs from issue responses, and provide `--dry-run` safety flags.
- **Primary reason:** Maintain zero external runtime dependencies while safely auditing GitHub repositories via REST API.
- **Key risk or trade-off:** Verbose HTTP byte-stream and status code parsing compared to third-party libraries (`requests`, `httpx`).
- **Required controls or conditions:** Filter items containing `"pull_request"` key in issue listing; pass authorization header for rate limit mitigation.
- **Implementation validation approach:** CLI dry-run execution tests and GitHub REST API integration validation.

## 3. Context and problem statement

`gh-helper-agent` automates repository maintenance by querying the GitHub REST API to list open issues, merge Dependabot pull requests, and deduplicate automated security scan notifications.

During initial implementation and testing, several architectural factors and GitHub API nuances were identified:
1. **GitHub Issues Endpoint Behavior**: `/repos/{owner}/{repo}/issues` returns both standard issues and pull requests (PRs are modeled as issues in GitHub's backend schema).
2. **Authentication & Rate Limits**: Unauthenticated REST requests are throttled to 60 requests/hour, which breaks multi-repo audits.
3. **Merge Workflow Constraints**: Attempting to merge PRs programmatically using the REST API requires checking mergeability and handling branch protection rules.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Business outcome | Automate repository health checks and maintenance cleanly | High |
| Maintainability and supportability | Zero third-party dependencies for maximum agent portability | High |
| Security and control posture | Safe `--dry-run` preview before mutating repository state | High |
| Delivery or cost constraint | Low setup overhead on standard Python 3 runtime environments | Medium |

## 5. Options considered

| Option | Description | Pros | Cons | Risk / Control Implications | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option 1: Pure Standard Library HTTP Client (`urllib.request` + `json`)** | Implement HTTP requests and JSON serialization purely with Python standard library modules. | <ul><li>Zero external package installation or virtualenv management required.</li><li>Extremely fast startup time and low risk of third-party supply chain vulnerabilities.</li></ul> | Requires custom error handling for HTTP statuses and JSON payload decoding. | Low risk, high stability. | **Accepted** |
| **Option 2: Third-Party HTTP Libraries (`requests` / `httpx` / `PyGithub`)** | Depend on external PyPI packages for GitHub REST API interaction. | Higher-level abstractions and simpler API call syntax. | <ul><li>Adds external dependencies requiring `pip install` and virtual environment setup.</li><li>Increases vulnerability scanning scope for container images.</li></ul> | Moderate dependency management overhead. | **Rejected** |
| **Option 3: Status quo / do nothing** | Perform repository maintenance and issue/PR management manually. | No code to write. | Scalability bottle-neck across multi-repo organizations. | Operational burden and delayed security updates. | **Rejected** |

## 6. Decision outcome

**We will:**
1. Filter out items containing the `"pull_request"` key in `get_open_issues_and_prs` when analyzing standard issues.
2. Use standard library `urllib.request` and `json` exclusively.
3. Support `--dry-run` execution mode across all state-mutating helper methods.

**We will not:** Add external runtime dependencies or process pull requests using standard issue endpoints.

**Decision scope:** `github_helper_agent.py` API communications and execution workflow.

**Out of scope:** Third-party CI/CD runner extensions.

## 7. Rationale

Using pure standard library modules guarantees that `github_helper_agent.py` can execute immediately in minimal container runtimes (e.g. Chainguard Python) or lightweight agent runners without pre-installing PyPI packages. Explicit filtering of `"pull_request"` keys prevents mutating pull requests during issue operations.

## 8. Consequences and trade-offs

### Positive consequences
- Prevents double-processing or incorrect mutation of PRs as issues.
- Ensures zero third-party package setup overhead for quick agent invocation.
- Gives users a safe mechanism (`--dry-run`) to audit API actions before writing state changes.

### Negative consequences
- Pure `urllib.request` handling requires explicit status code and byte-stream decoding error logic compared to higher-level libraries.

### Neutral or operational consequences
- Requires maintaining explicit HTTP error handling helpers in `github_helper_agent.py`.

### New constraints
- All new features must maintain the zero-external-dependency architectural constraint.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Security | Outbound HTTPS API traffic authenticated via `GITHUB_TOKEN` | jsoehner | Header authorization checks |
| DevSecOps | Zero external supply chain dependencies | jsoehner | Standard library audit |
| Operations | Safe preview execution via `--dry-run` | jsoehner | Dry-run execution logs |

### Residual risk
- Residual risk description: GitHub API rate limits if `GITHUB_TOKEN` is missing or unauthenticated.
- Residual risk owner: jsoehner
- Risk acceptance or exception ID: N/A
- Expiry or review date: 2027-08-01

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
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #1 | 2026-08-01 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-01 |
| Architecture reviewer | jsoehner | Reviews architecture alignment | Code Review | 2026-08-01 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | AGENT.md | Architectural requirements |
| Code implementation | github_helper_agent.py | Pure urllib implementation |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Implement urllib HTTP wrappers | jsoehner | 2026-08-01 | github_helper_agent.py |
| Add issue/PR separation logic | jsoehner | 2026-08-01 | get_open_issues_and_prs |
| Implement --dry-run mode | jsoehner | 2026-08-01 | --dry-run flag handling |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| API dry-run execution check | jsoehner | Execution logs | Yes |
| Zero-dependency audit | jsoehner | stdlib import check | Yes |

## 14. Supersession, review, and retirement

- Supersedes: None
- Superseded by: None
- Review triggers:
  - GitHub REST API version changes
  - Addition of external dependencies

## 15. Open questions and actions

None.

## 16. References

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- Python `urllib.request` standard documentation
