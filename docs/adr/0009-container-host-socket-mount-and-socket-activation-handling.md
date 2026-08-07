---
adr_id: "ADR-2026-0009"
title: "Container Host Socket Mount and Socket Activation Handling"
status: "Accepted"
risk_tier: "Tier 2"
control_domains:
  - Architecture
  - Security
  - Operations
  - Cloud
created_date: "2026-08-07"
proposed_date: "2026-08-07"
accepted_date: "2026-08-07"
implemented_date: "2026-08-07"
validated_date: "2026-08-07"
next_review_date: "2027-08-07"
review_triggers:
  - "Material architecture change"
  - "Container runtime socket security policy update"
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
    approval_evidence: "PR #9 Code Review"
    date: "2026-08-07"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
  - "Host container execution environment"
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "Host Docker/Moby daemon"
data_classification: "Internal"
external_exposure: "Host socket volume mount"
third_party_dependency: "Host Docker daemon"
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
    - "Host Docker socket mount standardisation"
    - "Systemd socket activation compatibility"
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

# ADR-2026-0009: Container Host Socket Mount and Socket Activation Handling

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

- **Decision outcome:** Standardize host socket mounting (`-v /run/docker.sock:/var/run/docker.sock`) for workflows requiring local daemon interaction, while keeping pure REST API executions decoupled.
- **Primary reason:** Enable containerized tools (like Trivy or container build checkers) to interact with host Moby/Docker engines across Linux systemd socket activation setups.
- **Key risk or trade-off:** Mounting `/run/docker.sock` grants elevated host access and must be restricted to trusted executions.
- **Required controls or conditions:** Document security implications and enforce separate execution modes for API-only vs daemon-attached runs.
- **Implementation validation approach:** Execution test with Trivy scanner against local Docker daemon.

## 3. Context and problem statement

When containerizing `gh-helper-agent` or executing containerized maintenance tools alongside Docker/Moby engine instances, container workflows may need to interact with the underlying Docker daemon (for instance, performing containerized build checks, running security scanners such as Trivy against local images, or inspecting system container states).

On Linux hosts running Moby/Docker Engine (e.g. Fedora, RHEL, Ubuntu), the Docker API server uses systemd socket activation (`docker.socket`), creating the Unix domain socket at `/run/docker.sock` with a compatibility symlink at `/var/run/docker.sock`.

Without explicit socket volume mounting (`-v /run/docker.sock:/var/run/docker.sock`), containerized applications cannot connect to the host Docker daemon, resulting in `Cannot connect to the Docker daemon at unix:///var/run/docker.sock` errors. Additionally, containers mounted without proper socket permissions or group alignment (`docker` group GID mismatch) can experience permission denied errors.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Operational resilience | Reliable host Docker daemon interaction for scanning/building | High |
| Security and control posture | Strict isolation between REST API runs and socket-attached runs | High |
| Maintainability and supportability | Clear documentation for systemd socket activation gotchas | Medium |

## 5. Options considered

### Option 1: Standardized Socket Volume Mount (`-v /run/docker.sock:/var/run/docker.sock`)

**Description:** Document and support optional host socket mounting for containerized daemon interactions while keeping REST API mode isolated.

**Pros:**
- Enables local image scanning and container build checks.
- Compatible with Linux systemd socket activation patterns.

**Cons:**
- Socket mounting carries elevated host privilege implications.

**Risk/control implications:** Controlled elevation for specific local workflows.

**Disposition:** Accepted

### Option 2: Run Everything with Mandatory Socket Mounts

**Description:** Require socket mounting for all container runs regardless of whether daemon access is needed.

**Pros:**
- Single execution command.

**Cons:**
- Unnecessarily grants host socket access to standard REST API maintenance runs.

**Risk/control implications:** Unnecessary security exposure.

**Disposition:** Rejected

### Option 3: Status quo / do nothing

**Description:** Leave socket activation failures unhandled and undocumented.

**Pros:**
- No documentation updates.

**Cons:**
- Cryptic `Cannot connect to Docker daemon` errors for container users.

**Risk/control implications:** Operational confusion.

**Disposition:** Rejected

## 6. Decision outcome

**We will:**
1. Document `-v /run/docker.sock:/var/run/docker.sock` volume mount flags in documentation.
2. Separate API-only execution (requiring only `GITHUB_TOKEN`) from daemon-attached execution.
3. Record socket activation rules and permissions in `README.md` and `MEMORY.md`.

**We will not:** Require host socket mounting for standard REST API maintenance tasks.

**Decision scope:** Container runtime volume mounts and host daemon integration.

**Out of scope:** Docker-in-Docker (dind) privileged daemon setups.

## 7. Rationale

Standardizing explicit host socket mounts for local daemon tasks while preserving isolated REST API execution protects host security while granting full operational flexibility when local container inspections are required.

## 8. Consequences and trade-offs

### Positive consequences
- **Host Engine Interoperability**: Enables containerized executions of `gh-helper-agent` to build, scan, or manage local container images.
- **Clear Runtime Instructions**: Developers and CI/CD systems have unambiguous commands for both API-only and socket-attached container modes.

### Negative consequences
- **Security Considerations**: Mounting `/run/docker.sock` into a container grants elevated privileges over the host system. Socket mounting should be restricted to trusted images and executed only when local daemon access is explicitly required.

### Neutral or operational consequences
- Requires user awareness of host `docker` GID permissions.

### New constraints
- Socket mounts should never be enabled in untrusted pipeline contexts.

## 9. Risk and control impact

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Security | Host socket access privilege management | jsoehner | Explicit documentation & separation |
| Operations | Socket activation compatibility | jsoehner | Volume mount standard |

### Residual risk
- Residual risk description: Host socket exposed to malicious container payload if untrusted image is run.
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
| ADR Owner | jsoehner | Maintains record quality and traceability | PR #9 | 2026-08-07 |
| Decision Owner | jsoehner | Owns decision and lifecycle review | Architecture Review | 2026-08-07 |

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | README.md | Container execution examples |
| Operational guide | MEMORY.md | Socket activation notes |

## 12. Implementation plan

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| Document socket mount syntax | jsoehner | 2026-08-07 | README.md |
| Record socket activation notes | jsoehner | 2026-08-07 | MEMORY.md |

## 13. Validation plan

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Host socket mount execution test | jsoehner | CLI output logs | Yes |

## 14. Supersession, review, and retirement

- Supersedes: None
- Superseded by: None
- Review triggers:
  - Systemd socket path changes in major Linux distros

## 15. Open questions and actions

None.

## 16. References

- Docker Engine systemd socket activation documentation
