---
adr_id: "ADR-2026-0014"
title: "Consolidate Security Governance, Automate ADR Gatekeeping, and Remediate Dynamic Urllib CWE-939"
status: "Accepted"
risk_tier: "Tier 1"
control_domains:
  - Architecture
  - API
  - DevSecOps
  - Security
  - Governance
created_date: "2026-09-25"
proposed_date: "2026-09-25"
accepted_date: "2026-09-25"
implemented_date: "2026-09-25"
validated_date: "2026-09-25"
next_review_date: "2027-09-25"
review_triggers:
  - "Security scanning framework changes"
  - "Workflow restructuring"
adr_owner:
  name: "jsoehner"
  role: "Repository Maintainer"
decision_owner:
  name: "jsoehner"
  role: "Repository Maintainer"
accountable_role_or_forum: "gh-helper-agent Architecture Forum"
acceptors:
  - name: "jsoehner"
    role: "Repository Maintainer"
    forum: "Security & Architecture Review"
    approval_evidence: "Code Review"
    date: "2026-09-25"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "GitHub Actions CI/CD"
  - "gh-helper-agent CLI"
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "GitHub Actions Security Governance"
data_classification: "Internal"
external_exposure: "Outbound API calls to api.github.com"
third_party_dependency: "GitHub Actions"
model_or_ai_impact: "None"
residual_risk_owner:
  name: "jsoehner"
  role: "Repository Maintainer"
exceptions_or_risk_acceptances: []
technical_debt_items: []
technical_debt_assessment:
  impact: "None"
  score: 0
  rationale: "Remediates legacy workflow divergence and hardens outbound API network calls against custom scheme hijacking."
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
    - "Consolidate security workflows to security-governance.yml"
    - "Enforce ADR Gatekeeper on security architecture changes"
    - "Remediate dynamic urllib CWE-939 findings in Semgrep"
  diagrams: []
  threat_model: []
  risk_assessment: []
  standards_exception: []
  change_records: []
  pull_requests: []
  test_evidence:
    - "test_github_helper_agent.py"
    - "Semgrep auto scan: 0 findings"
  deployment_evidence: []
  runbooks: []
  monitoring: []
supersedes:
  - "ADR-2026-0011"
superseded_by: []
retention_classification: "Standard"
legal_hold: false
---

# ADR-2026-0014: Consolidate Security Governance, Automate ADR Gatekeeping, and Remediate Dynamic Urllib CWE-939

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**
- Created: 2026-09-25
- Accepted: 2026-09-25
- Implemented: 2026-09-25
- Validated: 2026-09-25

## 2. Executive Decision Summary

- **Decision Outcome:** 
  1. Retire redundant `.github/workflows/security-testing.yml` and establish `.github/workflows/security-governance.yml` as the sole authoritative workflow triggering Gitleaks secret detection, Semgrep SAST, Trivy CVE scanning, and Python ADR gatekeeping.
  2. Deploy `scripts/adr_security_gatekeeper.py` to audit pull request diffs touching security paths and enforce Architectural Decision Records across both `docs/adr/` and `docs/architecture/decisions/`.
  3. Remediate CWE-939 (`dynamic-urllib-use-detected`) in `github_helper_agent.py` by adding an explicit URL prefix validation guard constraining requests to `https://api.github.com/`.
- **Primary Reason:** Eliminate conflicting workflow executions, enforce architectural governance via CI gates, and eliminate blocking Semgrep findings.
- **Key Risk or Trade-Off:** None. Outbound requests remain bound strictly to GitHub's HTTPS REST API.

## 3. Context & Problem Statement

Prior updates left an unhardened `.github/workflows/security-testing.yml` that ran duplicated scans conflicting with organization-wide `security-governance` policies. Additionally, Semgrep scanning identified `python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected` in `github_helper_agent.py` due to variable interpolation into `urllib.request.urlopen()`.

## 4. Decision Drivers

- **Single Security Source of Truth**: Security gates must reside in a unified `security-governance.yml` pipeline.
- **Architectural Traceability**: Security-critical path modifications must be accompanied by an ADR.
- **Zero SAST Findings**: Resolve all Semgrep blocking findings across tracked files.

## 5. Decision Outcome

**We will:**
1. Remove `.github/workflows/security-testing.yml`.
2. Add `.github/workflows/security-governance.yml` with Gitleaks, Semgrep, Trivy, and ADR gatekeeping jobs.
3. Deploy `scripts/adr_security_gatekeeper.py` with multi-path ADR discovery.
4. Constrain `_api_call` in `github_helper_agent.py` to `https://api.github.com/` URLs.
5. Record ADR 0014 in `docs/architecture/decisions/`.

## 6. Validation

- [x] Semgrep scan completed with 0 findings across all 26 repository files.
- [x] All 17 unit tests in `test_github_helper_agent.py` pass.
- [x] ADR Gatekeeper verified on staged changes.
