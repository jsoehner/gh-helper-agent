---
adr_id: "ADR-2026-0013"
title: "Dependabot Security Alerts Assessment, Strategy Classification, and Automated Remediation Framework"
status: "Accepted"
risk_tier: "Tier 1"
control_domains:
  - Architecture
  - API
  - DevSecOps
  - Security
  - Operations
created_date: "2026-08-29"
proposed_date: "2026-08-29"
accepted_date: "2026-08-29"
implemented_date: "2026-08-29"
validated_date: "2026-08-29"
next_review_date: "2027-08-29"
review_triggers:
  - "Material architecture change"
  - "GitHub Dependabot Alerts API changes"
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
    approval_evidence: "Code Review"
    date: "2026-08-29"
consulted_stakeholders: []
informed_stakeholders: []
affected_systems:
  - "gh-helper-agent CLI"
  - "GitHub Actions CI/CD"
  - "Docker container execution"
affected_repositories:
  - "jsoehner/gh-helper-agent"
affected_services:
  - "GitHub REST API (Dependabot Alerts API)"
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
  rationale: "No technical debt introduced. Implements structured vulnerability assessment without adding external dependencies."
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
    - "GitHub Dependabot Alerts REST API querying and pagination"
    - "Automated remediation strategy classification"
    - "Ecosystem-tailored CLI fix command generation"
    - "Alert dismissal via GitHub API"
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
supersedes: []
superseded_by: []
retention_classification: "Standard"
legal_hold: false
---

# ADR-2026-0013: Dependabot Security Alerts Assessment, Strategy Classification, and Automated Remediation Framework

## 1. Status

**Current status:** Accepted

**Lifecycle notes:**

- Created: 2026-08-29
- Proposed: 2026-08-29
- Accepted: 2026-08-29
- Implemented: 2026-08-29
- Validated: 2026-08-29
- Next review: 2027-08-29

## 2. Executive decision summary

- **Decision outcome:** Integrate GitHub Dependabot Alerts REST API assessment and remediation planning into `gh-helper-agent`. The agent audits open security advisories across repositories, categorizes vulnerabilities into 6 distinct remediation strategies (`MERGE_DEPENDABOT_PR`, `PATCH_UPGRADE`, `MAJOR_UPGRADE`, `TRANSITIVE_LOCKFILE_UPDATE`, `WORKAROUND_OR_MITIGATION`, `DEV_DEPENDENCY_RISK_ACCEPTANCE`), generates ecosystem-specific CLI upgrade commands, and provides alert dismissal capability.
- **Primary reason:** Enable end-to-end vulnerability triage and proactive resolution beyond existing PR merging, allowing maintainers to instantly assess security posture, determine optimal remediation methods, and automate fixes.
- **Key risk or trade-off:** Certain repositories may have Dependabot alerts disabled or require specific token scopes (`security_events` or `repo`), which are handled gracefully with non-blocking diagnostic logs.

## 3. Context and problem statement

While `gh-helper-agent` previously merged opened Dependabot PRs and deduplicated scan issues, repositories frequently contain open Dependabot alerts where:
1. No automated PR has been submitted yet (e.g. unpatched zero-days, transitive dependencies, or disabled automated PR creation).
2. Upgrades entail major breaking version changes requiring codebase adjustments.
3. Vulnerabilities reside in indirect lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`, `go.sum`) needing lockfile deduplication.
4. Advisories affect development-only dependencies with zero production runtime exposure.

Maintainers required a systematic review mechanism to inspect open security advisories, determine the best method of fixing each alert, and generate exact CLI commands for remediation.

## 4. Decision drivers

| Driver | Description | Priority |
|---|---|---|
| Security Posture | Comprehensive audit of all repository Dependabot security advisories | High |
| Actionability | Determine the exact remediation strategy and generate ecosystem-specific fix commands | High |
| Zero Dependencies | Implement all API querying, version parsing, and strategy heuristics using Python standard library | High |
| Resilience | Gracefully handle repositories with disabled security alerts or insufficient permissions | High |

## 5. Options considered

| Option | Description | Pros | Cons | Risk / Control Implications | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option 1: Comprehensive In-Agent Strategy Classifier & Ecosystem Command Generator** | Query `/repos/{owner}/{repo}/dependabot/alerts`, correlate with open PRs, evaluate semantic version ranges, classify into 6 strategies, and output actionable commands. | <ul><li>Zero external dependencies.</li><li>Correlates alerts with open PRs.</li><li>Supports npm, pip, go, cargo, maven, gradle, composer, nuget, ruby, actions.</li><li>Supports alert dismissal via API.</li></ul> | Requires maintaining command templates for supported ecosystems. | Low risk; provides maximum immediate developer value and automation. | **Accepted** |
| **Option 2: Raw Advisory Listing Only** | Dump alert JSON/text without remediation classification or command generation. | Simple implementation. | Requires developer to manually analyze version jumps and formulate CLI commands. | High manual toil. | **Rejected** |
| **Option 3: External CLI Tool Dependency (e.g. `gh` CLI extensions)** | Shell out to external third-party tools to inspect alerts. | Offloads API querying. | Introduces runtime tool dependencies; breaks minimal distroless container execution. | Moderate supply chain and portability risk. | **Rejected** |

## 6. Decision outcome

**We will:**
1. Provide `get_dependabot_alerts()` to fetch paginated open alerts from `/repos/{owner}/{repo}/dependabot/alerts`.
2. Implement `determine_alert_remediation()` classifying alerts into 6 strategies:
   - `MERGE_DEPENDABOT_PR`: Dependabot PR is already open; review CI checks and squash-merge.
   - `PATCH_UPGRADE`: Direct non-breaking minor/patch upgrade available.
   - `MAJOR_UPGRADE`: Major semver breaking change required.
   - `TRANSITIVE_LOCKFILE_UPDATE`: Vulnerability resides in transitive lockfile; update via lockfile audit tools.
   - `WORKAROUND_OR_MITIGATION`: Zero-day or unpatched advisory; apply code mitigations or library replacement.
   - `DEV_DEPENDENCY_RISK_ACCEPTANCE`: Development-only scope with no runtime exposure; evaluate for dismissal (`tolerable_risk`).
3. Provide `generate_ecosystem_remediation_command()` generating commands for `npm`, `pip`, `gomod`, `cargo`, `composer`, `maven`, `gradle`, `nuget`, `rubygems`, `pub`, and `actions`.
4. Provide `dismiss_dependabot_alert()` supporting valid reasons (`fix_started`, `inaccurate`, `no_bandwidth`, `not_used`, `tolerable_risk`).
5. Integrate alert review into `process_repository`, `print_execution_summary`, and CLI flags (`--check-alerts`, `--severity`, `--ecosystem`).
6. Cover all classification strategies and command generators in `test_github_helper_agent.py`.

**We will not:** Add external packaging or semver parsing libraries.
