---
adr_id: "ADR-2026-0011"
title: "Decoupled Dependency Update and Security Testing Workflows"
status: "Accepted"
risk_tier: "Tier 2"
control_domains:
  - Architecture
  - Security
  - DevSecOps
  - Cloud
created_date: "2026-08-07"
proposed_date: "2026-08-07"
accepted_date: "2026-08-07"
implemented_date: "2026-08-07"
validated_date: "2026-08-07"
next_review_date: "2027-08-07"
review_triggers:
  - "Material architecture change"
  - "GitHub Actions security policy changes"
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
    approval_evidence: "PR #11 Code Review"
    date: "2026-08-07"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "GitHub Actions CI/CD"
  - "GitHub Container Registry (GHCR)"
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "Trivy vulnerability scanner"
  - "Semgrep SAST scanner"
data_classification: "Internal"
external_exposure: "Container publishing on ghcr.io"
third_party_dependency: "Trivy scanner action, Semgrep scanner action"
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
    - "Decouple dependency updates and security testing workflows"
    - "Independent execution schedules and triggers"
    - "Commit SHA pinning and Node 24 support"
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
supersedes:
  - "ADR-2026-0008"
superseded_by: []
retention_classification: "Standard"
legal_hold: false
---

# ADR-2026-0011: Decoupled Dependency Update and Security Testing Workflows

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

- **Decision outcome:** Replace monolithic single-file workflow (`container-daily-update.yml`) with two separate, non-sequential workflows: `.github/workflows/dependency-update.yml` and `.github/workflows/security-testing.yml`.
- **Primary reason:** Eliminate sequential coupling between container build/publish operations and security vulnerability scans. Allow security testing (Trivy + SAST) to run on Pull Requests and independent schedules without blocking or depending on container release pipelines.
- **Key risk or trade-off:** Slight increase in GitHub Actions workflow definitions (2 files instead of 1).
- **Required controls or conditions:** Action steps must be pinned to explicit 40-character commit SHAs with Node 24 compatibility per repository standards.
- **Implementation validation approach:** Independent execution of workflow dispatch and scheduled runs.

## 3. Context and problem statement

Previously, [ADR-2026-0008](file:///home/jsoehner/gh-helper-agent/docs/adr/0008-daily-container-rebuild-and-vulnerability-scanning-workflow.md) established a single monolithic workflow (`container-daily-update.yml`) that executed container vulnerability scanning as a strict prerequisite step prior to building and publishing updated container images to GHCR.

However, tightly coupling container build/push automation with security testing created several operational limitations:
1. Security testing could not be triggered on PRs without building/pushing container artifacts.
2. Code-level SAST security scanning (Semgrep) was missing from the CI pipeline.
3. A failure in container base image build could block independent security audit tasks.

To achieve high modularity and follow DevSecOps best practices, we required breaking out the dependency update workflow and the security testing workflow into separate, non-sequential GitHub Actions workflows.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Modularity and separation of concerns | Independent lifecycle management for container publishing vs. security auditing | High |
| Security Posture | Ability to run comprehensive security testing (Trivy container scan + Semgrep SAST) on PRs | High |
| Supply Chain Security | Explicit 40-character commit SHA pinning for all GitHub Actions steps | High |

## 5. Options considered

| Option | Description | Pros | Cons | Risk / Control Implications | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option 1: Decoupled Independent Workflows** | Separate `dependency-update.yml` (daily 03:00 UTC) and `security-testing.yml` (daily 04:00 UTC + PRs). | <ul><li>Independent execution paths.</li><li>Security scan on PRs without image push.</li><li>Includes SAST scanning.</li></ul> | Manages 2 workflow files instead of 1. | Minimal risk, enhanced security audit coverage. | **Accepted** |
| **Option 2: Retain Monolithic Sequential Workflow** | Keep `container-daily-update.yml` with inline scan step. | Single file configuration. | Tight coupling; no SAST scanning; scans tied strictly to scheduled container builds. | Inflexible pipeline layout. | **Rejected (Superseded)** |

## 6. Decision outcome

**We will:**
1. Create `.github/workflows/dependency-update.yml` for automated container build, tag, GHCR push, and agent execution.
2. Create `.github/workflows/security-testing.yml` containing non-sequential parallel jobs for Trivy container vulnerability scanning and Semgrep SAST code analysis.
3. Supersede [ADR-2026-0008](file:///home/jsoehner/gh-helper-agent/docs/adr/0008-daily-container-rebuild-and-vulnerability-scanning-workflow.md) with this document (ADR-2026-0011).
4. Pin all GitHub Actions steps to explicit commit SHAs with Node 24 compatible action major versions.

**We will not:** Sequentially block container dependency pushes on inline scan steps in a single job.

## 7. Rationale

Decoupling dependency updates and security testing allows security checks to execute on PRs and pull request branches before code is merged into `main`, while dependency update jobs can build and publish release containers on their own schedule without being coupled to code analysis pipelines.

## 8. Consequences and trade-offs

### Positive consequences
- Independent execution and clear diagnostic boundary between security scans and container build pipelines.
- Addition of SAST code scanning (`returntocorp/semgrep-action`).
- Full compliance with Node 24 and SHA-pinning security controls.

### Negative consequences
- None.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Security | Multi-layer scanning (Container + SAST) | jsoehner | `security-testing.yml` |
| DevSecOps | Independent CI/CD workflow triggers | jsoehner | `dependency-update.yml` |

## 10. Governance and acceptance

| Role or forum | Named person | Responsibility | Evidence | Date |
|---|---|---|---|---|
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #11 | 2026-08-07 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-07 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | `.github/workflows/dependency-update.yml` | Container build & publish workflow |
| Security evidence | `.github/workflows/security-testing.yml` | Trivy + SAST workflow |

## 12. Supersession

- **Supersedes:** [ADR-2026-0008](file:///home/jsoehner/gh-helper-agent/docs/adr/0008-daily-container-rebuild-and-vulnerability-scanning-workflow.md)
- **Superseded by:** None
