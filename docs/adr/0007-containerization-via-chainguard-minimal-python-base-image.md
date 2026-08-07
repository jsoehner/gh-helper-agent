---
adr_id: "ADR-2026-0007"
title: "Containerization via Chainguard Minimal Python Base Image"
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
  - "Base image security vulnerability finding"
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
    approval_evidence: "PR #7 Code Review"
    date: "2026-08-07"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
  - "Container build pipeline"
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "GitHub Container Registry (GHCR)"
data_classification: "Internal"
external_exposure: "Container image distribution via GHCR"
third_party_dependency: "Chainguard minimal Python image"
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
    - "Minimal attack surface containerization"
    - "Non-root execution posture"
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

# ADR-2026-0007: Containerization via Chainguard Minimal Python Base Image

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

- **Decision outcome:** Package `gh-helper-agent` into a distroless container using Chainguard minimal Python base image (`cgr.dev/chainguard/python`) with multi-stage Dockerfile builds and non-root execution (`USER nonroot`).
- **Primary reason:** Eliminate OS vulnerability surface area (CVEs), package managers, and unused shell utilities.
- **Key risk or trade-off:** Distroless container lacks interactive debugging shells (`bash`, `sh`).
- **Required controls or conditions:** Enforce `USER nonroot` and multi-stage build separation.
- **Implementation validation approach:** Trivy container vulnerability scan and Docker execution test.

## 3. Context and problem statement

To run `gh-helper-agent` reliably across diverse environments (Kubernetes clusters, cloud cron runners, serverless container platforms, local Docker runtimes) without OS-level dependency pollution or vulnerability risks, a secure containerization strategy is needed.

Standard container images (e.g. `python:3.11-slim` or `ubuntu`) often contain unused utilities, shell environments, and package managers (apt/dpkg) that expand the attack surface and trigger vulnerability scanner flags (CVEs).

Additionally, `gh-helper-agent` relies purely on Python standard library modules (`urllib`, `os`, `json`, `argparse`), meaning no heavy third-party C dependencies or package compilation steps are required.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Security and control posture | Minimal attack surface and zero-CVE base image guarantees | High |
| Maintainability and supportability | Single lightweight container artifact (~30MB) | High |
| Operational resilience | Immutable non-root execution context | High |

## 5. Options considered

### Option 1: Chainguard Minimal Python Image (`cgr.dev/chainguard/python`)

**Description:** Multi-stage Dockerfile build using Chainguard distroless Python runtime image as final base.

**Pros:**
- Zero known vulnerabilities, updated daily.
- Distroless architecture eliminates OS shell and package manager attack vectors.
- Minimal image size (~30MB).

**Cons:**
- Lacks `bash` or `sh` inside runtime container.

**Risk/control implications:** Industry-leading security posture.

**Disposition:** Accepted

### Option 2: Standard Official Python Image (`python:3.11-slim`)

**Description:** Standard Debian-based slim Python base image.

**Pros:**
- Includes standard OS utilities and package managers for debugging.

**Cons:**
- Higher CVE scanner noise and unnecessary OS binaries.
- Larger footprint (~150MB).

**Risk/control implications:** Increased vulnerability exposure.

**Disposition:** Rejected

### Option 3: Status quo / do nothing

**Description:** Run script directly on host systems without containerization.

**Pros:**
- No container build step.

**Cons:**
- Inconsistent execution across different OS environments.

**Risk/control implications:** Platform inconsistency.

**Disposition:** Rejected

## 6. Decision outcome

**We will:**
1. Use `cgr.dev/chainguard/python:latest` in a multi-stage Dockerfile.
2. Enforce non-root user execution (`USER nonroot`).
3. Set `ENTRYPOINT ["python", "/app/github_helper_agent.py"]`.

**We will not:** Include shell environments or package managers in production runtime images.

**Decision scope:** Container image architecture and Dockerfile configuration.

**Out of scope:** VM-based virtualization setups.

## 7. Rationale

Using Chainguard minimal Python images provides a zero-CVE container foundation, aligning perfectly with the zero-dependency, security-focused architecture of `gh-helper-agent`.

## 8. Consequences and trade-offs

### Positive consequences
- **Minimal Attack Surface**: Zero unnecessary tools or shells included in the container runtime layer.
- **Zero Known Vulnerabilities**: Chainguard daily rebuilds ensure CVE-free base images.
- **Single-Artifact Deployment**: All runtime functionality encapsulated in a single lightweight image (~30MB).
- **Environment Isolation**: Eliminates local environment mismatch issues when executing automated scans and fork synchronizations.

### Negative consequences
- Distroless execution environment lacks standard debugging tools (`bash`, `curl`, `sh`), requiring multi-stage or sidecar patterns if interactive shell access inside the container is needed for debugging.

### Neutral or operational consequences
- Container builds require docker/podman engines.

### New constraints
- Runtime environment cannot rely on OS utilities outside Python stdlib.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Security | Distroless non-root container posture | jsoehner | Trivy CVE audit |
| DevSecOps | Daily base image security updates | jsoehner | Container workflow |

### Residual risk
- Residual risk description: Upstream base image breaking change.
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
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #7 | 2026-08-07 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-07 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | Dockerfile | Multi-stage build definitions |
| Security evidence | Trivy scan logs | Zero CRITICAL/HIGH findings |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Create multi-stage Dockerfile | jsoehner | 2026-08-07 | Dockerfile |
| Configure nonroot user | jsoehner | 2026-08-07 | Dockerfile |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Container build and run test | jsoehner | Container output logs | Yes |

## 14. Supersession, review, and retirement

- Supersedes: None
- Superseded by: None
- Review triggers:
  - Chainguard base image repository structural changes

## 15. Open questions and actions

None.

## 16. References

- Chainguard Images documentation (`cgr.dev/chainguard/python`)
