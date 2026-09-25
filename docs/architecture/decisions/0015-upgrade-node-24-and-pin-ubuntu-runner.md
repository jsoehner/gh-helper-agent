---
adr_id: "ADR-2026-0015"
title: "Upgrade GitHub Actions to Node 24 and Pin Runner Environment to Ubuntu 24.04"
status: "Accepted"
risk_tier: "Tier 1"
control_domains:
  - DevSecOps
  - Architecture
  - Governance
  - Security
created_date: "2026-09-25"
proposed_date: "2026-09-25"
accepted_date: "2026-09-25"
implemented_date: "2026-09-25"
validated_date: "2026-09-25"
next_review_date: "2027-09-25"
review_triggers:
  - "GitHub Actions runner image changes"
  - "Node runtime version deprecations"
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
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "GitHub Actions Workflows"
data_classification: "Internal"
external_exposure: "None"
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
  rationale: "Eliminates deprecation warnings for Node 20 and preempts breaking changes from upcoming Ubuntu 26 runner migration."
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
    - "Migrate GitHub Actions workflows to Node 24 compatible action releases"
    - "Pin Ubuntu runner images to ubuntu-24.04 LTS"
    - "Pin all actions to explicit 40-character commit SHAs"
  diagrams: []
  threat_model: []
  risk_assessment: []
  standards_exception: []
  change_records: []
  pull_requests: []
  test_evidence:
    - "scripts/test_boms.sh"
    - "scripts/adr_security_gatekeeper.py"
  deployment_evidence: []
  runbooks: []
  monitoring: []
supersedes: []
superseded_by: []
retention_classification: "Standard"
legal_hold: false
---

# ADR-2026-0015: Upgrade GitHub Actions to Node 24 and Pin Runner Environment to Ubuntu 24.04

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**
- Created: 2026-09-25
- Accepted: 2026-09-25
- Implemented: 2026-09-25
- Validated: 2026-09-25

## 2. Executive Decision Summary

- **Decision Outcome:**
  1. Pin all GitHub Actions workflow runners from the moving label `ubuntu-latest` to explicit `ubuntu-24.04` across all CI pipelines (`sbom-cbom.yml`, `security-governance.yml`, `dependency-update.yml`).
  2. Upgrade `actions/upload-artifact` from v4 (`ea165f8d65b6e75b540449e92b4886f43607fa02`) to v7 (`043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7.0.1`), which runs natively on `node24`.
  3. Upgrade `actions/setup-python` from v5 (`42375524e23c412d93fb67b49958b491fce71c38`) to v7 (`5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0`), which runs natively on `node24`.
  4. Pin `actions/checkout` and `actions/setup-node` to explicit commit SHAs and bump `setup-node` target `node-version` from `20` to `24`.
- **Primary Reason:** Preempt runner failures from the impending migration of `ubuntu-latest` to Ubuntu 26.04 (October 2026), eliminate Node 20 runner deprecation warnings, and adhere to supply chain security standards by pinning all actions to full commit SHAs.
- **Key Risk or Trade-Off:** None. `ubuntu-24.04` is the stable LTS runner image and Node 24 is fully supported across GitHub Actions runners.

## 3. Context & Problem Statement

GitHub runners began issuing two notices on recent workflow executions:
1. Deprecation of Node 20 runners forcing legacy actions (`actions/upload-artifact@v4`) into compatibility mode on Node 24 runners.
2. Upcoming migration of `ubuntu-latest` to Ubuntu 26 starting October 19, 2026 (actions/runner-images#14748).

## 4. Decision Drivers

- **Zero Deprecation Warnings:** Ensure all actions target Node 24 directly.
- **Deterministic Runner Environments:** Pin `ubuntu-24.04` to avoid unexpected environmental drift when GitHub migrates `ubuntu-latest`.
- **Supply-Chain Security:** Pin all third-party GitHub Actions to 40-character immutable commit SHAs.

## 5. Decision Outcome

**We will:**
1. Update `runs-on` in `.github/workflows/sbom-cbom.yml`, `.github/workflows/security-governance.yml`, and `.github/workflows/dependency-update.yml` to `ubuntu-24.04`.
2. Upgrade `actions/upload-artifact` to `v7.0.1` (`043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`).
3. Upgrade `actions/setup-python` to `v7.0.0` (`5fda3b95a4ea91299a34e894583c3862153e4b97`).
4. Upgrade `actions/setup-node` to `v7.0.0` (`820762786026740c76f36085b0efc47a31fe5020`) with `node-version: '24'`.
5. Pin `actions/checkout` to `v7.0.1` (`3d3c42e5aac5ba805825da76410c181273ba90b1`).

## 6. Validation

- [x] Tested ADR Gatekeeper against new ADR.
- [x] Validated YAML workflow syntax.
- [x] Confirmed zero remaining mutable tags in `sbom-cbom.yml`.
