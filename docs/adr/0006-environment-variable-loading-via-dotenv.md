---
adr_id: "ADR-2026-0006"
title: "Environment Variable Loading via Zero-Dependency .env File Parser"
status: "Accepted"
risk_tier: "Tier 1"
control_domains:
  - Architecture
  - Security
  - DevSecOps
created_date: "2026-08-06"
proposed_date: "2026-08-06"
accepted_date: "2026-08-06"
implemented_date: "2026-08-06"
validated_date: "2026-08-06"
next_review_date: "2027-08-06"
review_triggers:
  - "Material architecture change"
  - "Security token handling policy update"
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
    approval_evidence: "PR #6 Code Review"
    date: "2026-08-06"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "Local environment configuration"
data_classification: "Internal"
external_exposure: "Local .env file reading"
third_party_dependency: "None"
model_or_ai_impact: "None"
residual_risk_owner:
  name: "jsoehner"
  role: "Repository Maintainer"
exceptions_or_risk_acceptances: []
technical_debt_items: []
traceability:
  requirements:
    - "Zero-dependency dotenv loading"
    - "Shell environment precedence"
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

# ADR-2026-0006: Environment Variable Loading via Zero-Dependency `.env` File Parser

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**

- Created: 2026-08-06
- Proposed: 2026-08-06
- Accepted: 2026-08-06
- Implemented: 2026-08-06
- Validated: 2026-08-06
- Next review: 2027-08-06

## 2. Executive decision summary

- **Decision outcome:** Implement custom `load_dotenv` function using standard Python string parsing, maintaining shell environment precedence.
- **Primary reason:** Load secrets (`GITHUB_TOKEN`) and config (`GITHUB_OWNER`) without introducing external third-party library dependencies (like `python-dotenv`).
- **Key risk or trade-off:** Custom parser does not support complex multiline variables or shell variable expansion syntax.
- **Required controls or conditions:** Do not overwrite variables already present in `os.environ`.
- **Implementation validation approach:** Execution tests with and without `.env` files present.

## 3. Context and problem statement

Running scripts in diverse environments (local development CLI, cron jobs, CI/CD runners, containerized environments) requires loading secrets such as `GITHUB_TOKEN` and configurations like `GITHUB_OWNER`. Requiring manual `export GITHUB_TOKEN=...` commands or adding external third-party library dependencies (like `python-dotenv`) violates the core design principle of zero external dependencies for `github_helper_agent.py`.

Without automatic `.env` reading, users or automated runners executing `python3 github_helper_agent.py` in directory locations containing `.env` configuration files encounter HTTP 401 unauthenticated API errors.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Business outcome | Seamless secret and configuration loading across local and containerized environments | High |
| Maintainability and supportability | Maintain zero external package dependencies | High |
| Security and control posture | Safe token loading without committing secrets to git | High |

## 5. Options considered

### Option 1: Built-in Custom `.env` Parser

**Description:** Read `.env` using standard Python file operations, ignoring comments and whitespace, populating `os.environ` only for unset keys.

**Pros:**
- Zero external package dependencies.
- Immediate execution without `pip install`.
- Respects OS shell variable overrides.

**Cons:**
- Limited support for complex multiline variable syntax.

**Risk/control implications:** Low risk, high portability.

**Disposition:** Accepted

### Option 2: Add `python-dotenv` Dependency

**Description:** Add `python-dotenv` to project requirements.

**Pros:**
- Full spec support for multiline and variable expansion.

**Cons:**
- Violates zero-dependency architectural constraint.

**Risk/control implications:** External dependency overhead.

**Disposition:** Rejected

### Option 3: Status quo / do nothing

**Description:** Require manual shell `export` commands before running the script.

**Pros:**
- No code to write.

**Cons:**
- Frequent HTTP 401 auth failures for users expecting `.env` support.

**Risk/control implications:** Poor user experience.

**Disposition:** Rejected

## 6. Decision outcome

**We will:**
1. Implement `load_dotenv()` directly in `github_helper_agent.py`.
2. Automatically check for `.env` in execution paths.
3. Preserve existing host environment variables over `.env` values.

**We will not:** Add `python-dotenv` or other external dependencies.

**Decision scope:** Environment configuration loading.

**Out of scope:** External key management service (KMS) integration.

## 7. Rationale

Writing a lightweight `.env` parser using Python standard library primitives upholds the project's zero-dependency rule while delivering seamless developer experience across CLI and container contexts.

## 8. Consequences and trade-offs

### Positive consequences
- Automatic loading of tokens and configuration parameters when executing locally or via background workers.
- Preserves the zero external library dependency constraint of `github_helper_agent.py`.
- Preserves shell variable override hierarchy (existing OS environment variables take priority over `.env`).

### Negative consequences
- Simple `.env` parser does not support complex multiline variables or shell variable expansion syntax without additional parser logic.

### Neutral or operational consequences
- Log output indicates whether `.env` was detected and loaded.

### New constraints
- Secrets in `.env` must follow standard key-value formatting without multiline blocks.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Security | Secret loading into environment memory | jsoehner | .gitignore entry check |
| DevSecOps | Zero external supply chain dependencies | jsoehner | Import audit |

### Residual risk
- Residual risk description: Accidental commitment of `.env` to source control if `.gitignore` is missing.
- Residual risk owner: jsoehner
- Risk acceptance or exception ID: N/A
- Expiry or review date: 2027-08-06

### Technical debt
- None.

## 10. Governance and acceptance

| Role or forum | Named person | Responsibility | Evidence | Date |
|---|---|---|---|---|
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #6 | 2026-08-06 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-06 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | AGENT.md | Zero-dependency config loading |
| Code implementation | github_helper_agent.py | `load_dotenv` implementation |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Implement load_dotenv function | jsoehner | 2026-08-06 | github_helper_agent.py |
| Add env precedence checks | jsoehner | 2026-08-06 | github_helper_agent.py |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Dotenv parsing validation test | jsoehner | Execution logs | Yes |

## 14. Supersession, review, and retirement

- Supersedes: None
- Superseded by: None
- Review triggers:
  - Requirements for complex secret expansion

## 15. Open questions and actions

None.

## 16. References

- Standard Python `os` and `open` documentation
