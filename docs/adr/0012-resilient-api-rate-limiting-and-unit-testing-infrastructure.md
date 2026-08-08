---
adr_id: "ADR-2026-0012"
title: "Resilient API Rate-Limiting, Exponential Backoff, and Automated Unit Testing Infrastructure"
status: "Accepted"
risk_tier: "Tier 1"
control_domains:
  - Architecture
  - API
  - DevSecOps
  - Operations
created_date: "2026-08-08"
proposed_date: "2026-08-08"
accepted_date: "2026-08-08"
implemented_date: "2026-08-08"
validated_date: "2026-08-08"
next_review_date: "2027-08-08"
review_triggers:
  - "Material architecture change"
  - "GitHub API rate limit policy changes"
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
    approval_evidence: "PR #12 Code Review"
    date: "2026-08-08"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
  - "GitHub Actions CI/CD"
  - "Docker build environment"
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
  rationale: "No new technical debt introduced; addresses rate-limiting edge cases and missing automated test verification."
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
    - "Exponential backoff and rate limit header awareness"
    - "Zero-dependency unit testing suite"
    - "Container build & CI/CD test execution"
  diagrams: []
  threat_model: []
  risk_assessment: []
  standards_exception: []
  change_records: []
  pull_requests: []
  test_evidence:
    - "test_github_helper_agent.py"
  deployment_evidence: []
  runbooks: []
  monitoring: []
supersedes:
  - "ADR-2026-0001"
superseded_by: []
retention_classification: "Standard"
legal_hold: false
---

# ADR-2026-0012: Resilient API Rate-Limiting, Exponential Backoff, and Automated Unit Testing Infrastructure

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**

- Created: 2026-08-08
- Proposed: 2026-08-08
- Accepted: 2026-08-08
- Implemented: 2026-08-08
- Validated: 2026-08-08
- Next review: 2027-08-08

## 2. Executive decision summary

- **Decision outcome:** Upgrade `github_helper_agent.py` HTTP engine (`_api_call`) with exponential backoff, `Retry-After` / `X-RateLimit-Reset` header parsing, rate limit threshold warnings (`X-RateLimit-Remaining < 10`), and establish an automated zero-dependency unit testing suite executed during Docker builds and CI security workflows.
- **Primary reason:** Prevent HTTP 429/403 rate-limit failures during extensive multi-repo account audits while superseding [ADR-2026-0001](file:///home/jsoehner/gh-helper-agent/docs/adr/0001-architecture-and-api-handling-strategy.md) with resilient API error handling and continuous test verification.
- **Key risk or trade-off:** Slight execution delay when retrying rate-limited calls (capped by backoff timeouts).

## 3. Context and problem statement

`gh-helper-agent` performs automated operations (fork synchronization, stale repository checks, issue/PR scans) across large GitHub accounts. Under high request volume or when unauthenticated rate limits apply:
1. HTTP 429 / 403 rate limit errors previously resulted in aborted operations without retry logic.
2. ADR-0001 established basic standard library HTTP calls, but lacked explicit rate limit header parsing and automated regression unit tests.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Reliability | Self-healing API interaction under rate throttling | High |
| Quality Assurance | Automated test suite verifying core helper logic | High |
| Operational Excellence | Pre-flight test execution in Docker container build stage | High |

## 5. Decision outcome

**We will:**
1. Parse `Retry-After`, `X-RateLimit-Reset`, and `X-RateLimit-Remaining` headers in `_api_call`.
2. Apply exponential backoff retries (up to 3 attempts) on rate limit errors (HTTP 429/403).
3. Maintain zero external runtime dependencies by using standard library `unittest` and `unittest.mock`.
4. Include `test_github_helper_agent.py` in `Dockerfile` builder stage and `.github/workflows/security-testing.yml`.

**Supersedes:** [ADR-2026-0001](file:///home/jsoehner/gh-helper-agent/docs/adr/0001-architecture-and-api-handling-strategy.md).
