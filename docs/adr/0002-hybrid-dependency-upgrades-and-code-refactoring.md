---
adr_id: "ADR-2026-0002"
title: "Hybrid Dependency Upgrades & Automated Code Refactoring Strategy"
status: "Accepted"
risk_tier: "Tier 1"
control_domains:
  - Architecture
  - DevSecOps
  - Operations
created_date: "2026-08-02"
proposed_date: "2026-08-02"
accepted_date: "2026-08-02"
implemented_date: "2026-08-02"
validated_date: "2026-08-02"
next_review_date: "2027-08-02"
review_triggers:
  - "Material architecture change"
  - "Package manager CLI breaking changes"
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
    approval_evidence: "PR #2 Code Review"
    date: "2026-08-02"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "GitHub REST API"
  - "Local package managers (npm, go, pip)"
data_classification: "Internal"
external_exposure: "Local command execution & API calls"
third_party_dependency: "GitHub REST API"
model_or_ai_impact: "None"
residual_risk_owner:
  name: "jsoehner"
  role: "Repository Maintainer"
exceptions_or_risk_acceptances: []
technical_debt_items: []
traceability:
  requirements:
    - "Dual-phase remote/local dependency upgrades"
    - "Monorepo module upgrade support"
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

# ADR-2026-0002: Hybrid Dependency Upgrades & Automated Code Refactoring Strategy

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**

- Created: 2026-08-02
- Proposed: 2026-08-02
- Accepted: 2026-08-02
- Implemented: 2026-08-02
- Validated: 2026-08-02
- Next review: 2027-08-02

## 2. Executive decision summary

- **Decision outcome:** Combine remote REST API auto-merging with local package manager fallback hooks (`perform_local_dependency_upgrade`) and issue-triggered refactoring.
- **Primary reason:** Address monorepo dependency structures and branch protection restrictions where remote API merges fail.
- **Key risk or trade-off:** Local execution relies on installed CLI binaries (`go`, `npm`, `python`) in the execution environment.
- **Required controls or conditions:** Verify workspace cleanliness and dry-run flags before applying local code transformations.
- **Implementation validation approach:** Execution tests against monorepo test fixtures.

## 3. Context and problem statement

While `gh-helper-agent` automates remote Dependabot PR merging, several edge cases require hybrid execution:
1. **Subdirectory & Monorepo Upgrades**: Dependency updates occurring in nested directory modules (e.g. `/httphandler` in Go projects) may require local verification or package manager invocations when remote auto-merges fail CI/protection rules.
2. **Issue-Driven Code Refactoring**: Code quality improvements and technical debt cleanup identified in issues require explicit refactoring hooks and local workspace AST/formatting passes.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Business outcome | Seamless handling of complex monorepo dependency structures | High |
| Maintainability and supportability | Clean architectural hooks for issue-triggered code transformations | High |
| Operational resilience | Prevent silent failures when branch protection rules block REST merges | High |

## 5. Options considered

### Option 1: Dual-Phase Remote API Merge + Local Fallback Hooks

**Description:** Combine remote REST API auto-merging with local CLI package manager invocations when remote merges cannot proceed.

**Pros:**
- Solves branch protection and monorepo path limitations.
- Enables local AST/formatting passes driven by issue tags.

**Cons:**
- Requires host environment to have target CLI tools installed.

**Risk/control implications:** Low risk, high flexibility.

**Disposition:** Accepted

### Option 2: Remote API Merge Only

**Description:** Restrict all operations to remote REST API calls.

**Pros:**
- Fully decoupled from local environment dependencies.

**Cons:**
- Cannot resolve monorepo dependency updates or issue-triggered local refactoring.

**Risk/control implications:** Limits maintenance scope.

**Disposition:** Rejected

### Option 3: Status quo / do nothing

**Description:** Manually resolve monorepo dependency updates and refactoring issues.

**Pros:**
- No automated local tool invocation.

**Cons:**
- High manual toil for developers.

**Risk/control implications:** Technical debt accumulation.

**Disposition:** Rejected

## 6. Decision outcome

**We will:**
1. Implement dual-phase dependency upgrade hooks combining REST API calls with local package manager fallbacks.
2. Add issue-triggered refactoring logic (`perform_code_refactoring`) to process technical debt tags.
3. Document operational gotchas and constraints in documentation.

**We will not:** Force local tool execution without verifying environment availability.

**Decision scope:** Dependency resolution and refactoring execution paths.

**Out of scope:** Custom third-party IDE plugins.

## 7. Rationale

Providing local fallback execution allows `gh-helper-agent` to handle complex monorepos and branch protection environments where simple API merge calls fail, significantly reducing manual intervention.

## 8. Consequences and trade-offs

### Positive consequences
- Allows seamless handling of complex monorepo dependency structures.
- Establishes a clean architectural path for automated code refactoring.
- Prevents silent failures when remote GitHub REST API merges cannot bypass branch protections.

### Negative consequences
- Local execution hooks require local CLI tool availability (e.g. `go`, `npm`, `python`).

### Neutral or operational consequences
- System logs reflect dual-phase execution paths.

### New constraints
- Local execution steps must respect dry-run flags and safety boundaries.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Operations | Fallback command invocation in local workspace | jsoehner | Workspace validation |
| DevSecOps | Package manager command safety checks | jsoehner | Parameter sanitization |

### Residual risk
- Residual risk description: Tooling version mismatch between host environment and target repository.
- Residual risk owner: jsoehner
- Risk acceptance or exception ID: N/A
- Expiry or review date: 2027-08-02

### Technical debt
- None.

## 10. Governance and acceptance

| Role or forum | Named person | Responsibility | Evidence | Date |
|---|---|---|---|---|
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #2 | 2026-08-02 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-02 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | AGENT.md | Hybrid upgrade requirements |
| Code implementation | github_helper_agent.py | Dual-phase handlers |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Add perform_local_dependency_upgrade | jsoehner | 2026-08-02 | github_helper_agent.py |
| Add perform_code_refactoring | jsoehner | 2026-08-02 | github_helper_agent.py |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Monorepo local upgrade test | jsoehner | Execution logs | Yes |

## 14. Supersession, review, and retirement

- Supersedes: None
- Superseded by: None
- Review triggers:
  - Package manager CLI flag changes

## 15. Open questions and actions

None.

## 16. References

- Go module / npm package manager update documentation
