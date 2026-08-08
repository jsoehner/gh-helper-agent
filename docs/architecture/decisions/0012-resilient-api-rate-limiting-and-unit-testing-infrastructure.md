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
- **Primary reason:** Prevent HTTP 429/403 rate-limit failures during extensive multi-repo account audits while superseding [ADR-2026-0001](file:///home/jsoehner/gh-helper-agent/docs/architecture/decisions/0001-architecture-and-api-handling-strategy.md) with resilient API error handling and continuous test verification.
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

## 5. Options considered

| Option | Description | Pros | Cons | Risk / Control Implications | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option 1: Standard Library HTTP Client with Exponential Backoff & Header Retries** | Enhance `_api_call` with `Retry-After` / `X-RateLimit-Reset` parsing and exponential backoff retry loop (max 3 attempts). | <ul><li>Prevents HTTP 429/403 call failures.</li><li>Preserves zero PyPI runtime dependencies.</li><li>Includes automated `unittest` suite.</li></ul> | Adds ~40 lines of retry logic to `_api_call`. | Low risk, significantly improved operational resilience. | **Accepted** |
| **Option 2: Integrate PyPI Retry Libraries (`urllib3` / `tenacity` / `requests`)** | Depend on PyPI packages for HTTP connection pooling and retries. | Built-in backoff decorator functions. | Violates zero-runtime-dependency constraint; expands container vulnerability surface. | Moderate supply chain risk. | **Rejected** |
| **Option 3: Status quo / do nothing** | Retain single-shot `urllib.request` implementation without retry logic or automated test suite. | No changes to HTTP engine. | Operation failures under rate-limiting; no automated regression testing. | High operational failure risk during large account audits. | **Rejected (Superseded)** |

## 6. Decision outcome

**We will:**
1. Parse `Retry-After`, `X-RateLimit-Reset`, and `X-RateLimit-Remaining` headers in `_api_call`.
2. Apply exponential backoff retries (up to 3 attempts) on rate limit errors (HTTP 429/403).
3. Maintain zero external runtime dependencies by using Python standard library `unittest` and `unittest.mock`.
4. Include `test_github_helper_agent.py` test suite in `Dockerfile` builder stage and `.github/workflows/security-testing.yml`.

**We will not:** Add external PyPI runtime dependencies for HTTP request retries or test assertion frameworks.

**Decision scope:** `github_helper_agent.py` HTTP call engine, rate-limiting handlers, and unit test infrastructure.

**Out of scope:** Third-party API proxies or external rate limiting middleware.

## 7. Rationale

Standard library `urllib` header parsing provides complete rate-limiting resilience without compromising the repository's strict zero-external-dependency requirement. Executing `unittest` during `Dockerfile` container creation guarantees zero-defect container artifacts are published to GHCR.

## 8. Consequences and trade-offs

### Positive consequences
- Self-healing API execution under GitHub REST API rate throttling.
- Automated unit test suite (`test_github_helper_agent.py`) guarding against API regression bugs.
- Container image build fails fast if unit tests fail.

### Negative consequences
- Maximum ~14 second execution delay when experiencing severe rate-limiting before exhausting retries.

### Neutral or operational consequences
- Warnings printed to `sys.stderr` when remaining rate limit drops below 10 requests.

### New constraints
- All future HTTP API modifications must pass unit tests in `test_github_helper_agent.py`.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Security | Safe handling of API token rate limits | jsoehner | Header inspection in `_api_call` |
| Operations | Pre-flight test execution during container build | jsoehner | `Dockerfile` test build stage |
| DevSecOps | Automated CI unit test verification | jsoehner | `security-testing.yml` |

### Residual risk

- Residual risk description: Total API quota exhaustion when running unauthenticated without a `GITHUB_TOKEN`.
- Residual risk owner: jsoehner
- Risk acceptance or exception ID: N/A
- Expiry or review date: 2027-08-08

## Technical debt assessment

**Debt impact:** None

**Technical debt score:** 0

**Assessment rationale:**

No new or unmanaged technical debt introduced by this decision; resolves missing automated test verification and rate-limit edge cases.

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
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #12 | 2026-08-08 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-08 |
| Architecture reviewer | jsoehner | Reviews architecture alignment | Code Review | 2026-08-08 |
| QA reviewer | jsoehner | Reviews test suite coverage | Code Review | 2026-08-08 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Code implementation | `github_helper_agent.py` | `_api_call` backoff & rate limit handling |
| Test evidence | `test_github_helper_agent.py` | Unit test suite covering retry logic |
| CI/CD evidence | `.github/workflows/security-testing.yml` | CI unit test run step |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Implement backoff in _api_call | jsoehner | 2026-08-08 | `github_helper_agent.py` |
| Create test_github_helper_agent.py | jsoehner | 2026-08-08 | `test_github_helper_agent.py` |
| Embed test step into Dockerfile | jsoehner | 2026-08-08 | `Dockerfile` builder stage |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Unit test execution | jsoehner | `python3 test_github_helper_agent.py` | Yes |
| Docker build test check | jsoehner | `docker build` log | Yes |

## 14. Supersession, review, and retirement

- Supersedes: [ADR-2026-0001](file:///home/jsoehner/gh-helper-agent/docs/architecture/decisions/0001-architecture-and-api-handling-strategy.md)
- Superseded by: None
- Review triggers:
  - Material architecture change
  - GitHub API rate limit policy changes

## 15. Open questions and actions

None.

## 16. References

- [GitHub REST API Rate Limiting Documentation](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)
- Python standard library `urllib.request` and `unittest` documentation

