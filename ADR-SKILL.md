# ADR Generator for GitHub Repositories

## Description
Use this skill to create, update, validate, and index Architecture Decision Records (ADRs) in any GitHub repository. The ADR format is designed for regulated, audit-sensitive environments but is lightweight enough for ordinary engineering teams. It creates Markdown ADRs with structured YAML front matter, decision rationale, alternatives, risk/control evidence, approval metadata, lifecycle state, traceability links, and supersession history.

This skill treats ADRs as durable governance evidence, not informal notes. Accepted or rejected ADRs should preserve decision history; substantive changes should be captured through a new ADR that supersedes the prior record.

## When to use this skill
Use this skill when the user asks to:

- Create a new ADR for a software, platform, cloud, data, security, identity, cryptography, resilience, third-party, AI/model, integration, infrastructure, or operational architecture decision.
- Initialize an ADR structure in a GitHub repository.
- Convert design notes, meeting notes, review comments, threat models, risk acceptances, or architecture decisions into an ADR.
- Review an ADR for completeness, auditability, governance evidence, risk tiering, lifecycle status, or traceability.
- Supersede, deprecate, retire, or archive an ADR.
- Generate an ADR index or decision register for a repository.
- Create pull request-ready ADR files and supporting repository artifacts.

## Objectives
When creating ADRs, produce records that answer:

1. What decision was made?
2. Why was the decision necessary?
3. What alternatives were considered?
4. Why was the selected option chosen?
5. What are the consequences and trade-offs?
6. Who owns and accepted the decision?
7. What risk, security, privacy, compliance, resilience, data, operational, third-party, or model/AI impacts were considered?
8. What evidence supports the decision?
9. How will implementation conformance be validated?
10. What supersession, review, retention, or archival rules apply?

## Repository conventions
Default ADR location:

```text
docs/architecture/decisions/
```

Default supporting files:

```text
docs/architecture/decisions/README.md
docs/architecture/decisions/_template.md
docs/architecture/decisions/index.md
```

Default ADR filename pattern:

```text
NNNN-short-decision-title.md
```

Examples:

```text
0001-use-centralized-session-management.md
0002-adopt-managed-key-vault-for-application-secrets.md
0003-supersede-basic-authentication-for-service-api.md
```

If the repository already has an ADR convention, follow the existing folder, numbering, filename style, template, and lifecycle vocabulary unless the user asks to standardize it.

## ADR lifecycle states
Use the following lifecycle states unless the repository has an existing standard:

- Candidate
- Draft
- Proposed
- In Review
- Rework
- Accepted
- Accepted with Conditions
- Rejected
- Implemented
- Validated
- Deferred
- Superseded
- Deprecated
- Retired
- Archived

State rules:

- `Draft`, `Proposed`, `In Review`, and `Rework` ADRs may be edited as part of normal review.
- `Accepted` and `Rejected` ADRs must not be substantively overwritten.
- If a material change is required after acceptance or rejection, create a new ADR and mark the prior one as `Superseded`.
- `Accepted with Conditions` must include conditions, owners, due dates, and evidence links.
- `Deprecated`, `Retired`, and `Archived` ADRs must include disposition evidence.

## Risk tiers
Classify each ADR using this default tiering model:

| Tier | Name | Decision profile | Minimum governance expectation |
|---|---|---|---|
| Tier 0 | Local reversible decision | Low impact, local to one component, easy to reverse, no material control implication | ADR optional unless useful for knowledge retention |
| Tier 1 | Product or application decision | Affects application structure, dependencies, interfaces, maintainability, or non-functional requirements | ADR required; owner and domain/technical review expected |
| Tier 2 | Cross-domain or controlled architecture decision | Affects multiple teams, shared platforms, data movement, standards, resilience, third-party dependencies, or production operations | ADR required; architecture review and relevant control reviews expected |
| Tier 3 | Material risk, exception, or regulatory decision | Introduces residual risk, policy deviation, standards exception, sensitive data impact, customer/channel exposure, model/AI impact, material third-party dependency, or critical security control impact | Formal approval and named risk/control stakeholder acceptance expected |
| Tier 4 | Strategic enterprise decision | Defines enterprise pattern, reference architecture, strategic platform, cryptographic strategy, critical resilience posture, or systemic exception | Enterprise-level governance and senior decision authority expected |

## Control domains
Use one or more of the following control domain labels:

- Architecture
- Security
- Privacy
- Data
- Resilience
- ThirdParty
- Compliance
- Operations
- ModelRisk
- AI
- Identity
- Cryptography
- Cloud
- Network
- API
- DevSecOps
- RecordsManagement
- ChangeManagement
- Other

## Required ADR metadata
Every ADR must include YAML front matter. Use `TBD` only when information is genuinely unavailable and add an action owner/date to resolve it.

Required fields:

```yaml
adr_id: "ADR-YYYY-NNNN"
title: "Short declarative decision statement"
status: "Draft"
risk_tier: "Tier 1"
control_domains:
  - Architecture
created_date: "YYYY-MM-DD"
proposed_date: ""
accepted_date: ""
implemented_date: ""
validated_date: ""
next_review_date: ""
review_triggers:
  - "Material architecture change"
  - "Security incident or audit finding"
  - "Technology standard change"
adr_owner:
  name: "TBD"
  role: "TBD"
decision_owner:
  name: "TBD"
  role: "TBD"
accountable_role_or_forum: "TBD"
acceptors:
  - name: "TBD"
    role: "TBD"
    forum: ""
    approval_evidence: ""
    date: ""
consulted_stakeholders:
  - role: "TBD"
    name: "TBD"
informed_stakeholders: []
affected_systems: []
affected_repositories: []
affected_services: []
data_classification: "TBD"
external_exposure: "TBD"
third_party_dependency: "TBD"
model_or_ai_impact: "TBD"
residual_risk_owner:
  name: ""
  role: ""
exceptions_or_risk_acceptances: []
technical_debt_items: []
technical_debt_assessment:
  impact: "None"
  score: 0
  rationale: "TBD"
  existing_debt_references: []
  new_or_changed_debt_items: []
  debt_owner:
    name: ""
    role: ""
  remediation_plan: ""
  remediation_due_date: ""
  review_date: ""
  related_exceptions_or_risk_acceptances: []
traceability:
  requirements: []
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
retention_classification: "TBD"
legal_hold: false
```

## ADR Markdown template
Use this structure for every generated ADR.

```markdown
---
adr_id: "ADR-YYYY-NNNN"
title: "Short declarative decision statement"
status: "Draft"
risk_tier: "Tier 1"
control_domains:
  - Architecture
created_date: "YYYY-MM-DD"
proposed_date: ""
accepted_date: ""
implemented_date: ""
validated_date: ""
next_review_date: ""
review_triggers:
  - "Material architecture change"
  - "Security incident or audit finding"
  - "Technology standard change"
adr_owner:
  name: "TBD"
  role: "TBD"
decision_owner:
  name: "TBD"
  role: "TBD"
accountable_role_or_forum: "TBD"
acceptors:
  - name: "TBD"
    role: "TBD"
    forum: ""
    approval_evidence: ""
    date: ""
consulted_stakeholders: []
informed_stakeholders: []
affected_systems: []
affected_repositories: []
affected_services: []
data_classification: "TBD"
external_exposure: "TBD"
third_party_dependency: "TBD"
model_or_ai_impact: "TBD"
residual_risk_owner:
  name: ""
  role: ""
exceptions_or_risk_acceptances: []
technical_debt_items: []
technical_debt_assessment:
  impact: "None"
  score: 0
  rationale: "TBD"
  existing_debt_references: []
  new_or_changed_debt_items: []
  debt_owner:
    name: ""
    role: ""
  remediation_plan: ""
  remediation_due_date: ""
  review_date: ""
  related_exceptions_or_risk_acceptances: []
traceability:
  requirements: []
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
retention_classification: "TBD"
legal_hold: false
---

# ADR-YYYY-NNNN: Short declarative decision statement

## 1. Status

**Current status:** Draft

**Lifecycle notes:**

- Created: YYYY-MM-DD
- Proposed: TBD
- Accepted: TBD
- Implemented: TBD
- Validated: TBD
- Next review: TBD

## 2. Executive decision summary

Summarize the decision in 3 to 5 concise bullets:

- Decision outcome:
- Primary reason:
- Key risk or trade-off:
- Required controls or conditions:
- Implementation validation approach:

## 3. Context and problem statement

Describe the business, technical, operational, regulatory, security, resilience, or delivery context that makes this decision necessary.

Include:

- The problem being solved.
- The affected systems, services, users, data, interfaces, or operating model.
- The timing driver or decision deadline.
- Why the decision is architecturally significant.

## 4. Decision drivers

List the material drivers and constraints.

| Driver | Description | Priority |
|---|---|---|
| Business outcome | TBD | High/Medium/Low |
| Security and control posture | TBD | High/Medium/Low |
| Operational resilience | TBD | High/Medium/Low |
| Regulatory or compliance need | TBD | High/Medium/Low |
| Delivery or cost constraint | TBD | High/Medium/Low |
| Maintainability and supportability | TBD | High/Medium/Low |

## 5. Options considered

| Option | Description | Pros | Cons | Risk / Control Implications | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option 1: TBD** | TBD | <ul><li>TBD</li></ul> | TBD | TBD | Accepted / Rejected / Deferred |
| **Option 2: TBD** | TBD | <ul><li>TBD</li></ul> | TBD | TBD | Accepted / Rejected / Deferred |
| **Option 3: Status quo / do nothing** | Continue without making the proposed architecture change. | <ul><li>TBD</li></ul> | TBD | TBD | Accepted / Rejected / Deferred |

## 6. Decision outcome

State the selected decision clearly and affirmatively.

**We will:** TBD

**We will not:** TBD

**Decision scope:** TBD

**Out of scope:** TBD

## 7. Rationale

Explain why the selected option is appropriate given the drivers, constraints, evidence, and alternatives.

Address:

- Why this decision best satisfies the decision drivers.
- Why rejected options were not selected.
- What evidence supports the decision.
- What assumptions must remain true for the decision to remain valid.

## 8. Consequences and trade-offs

### Positive consequences

- TBD

### Negative consequences

- TBD

### Neutral or operational consequences

- TBD

### New constraints

- TBD

## 9. Risk and control impact

Describe threats, control requirements, residual risks, exceptions, technical debt, and compensating controls.

| Area | Impact | Owner | Evidence or action |
|---|---|---|---|
| Security | TBD | TBD | TBD |
| Privacy | TBD | TBD | TBD |
| Data | TBD | TBD | TBD |
| Resilience | TBD | TBD | TBD |
| Third-party | TBD | TBD | TBD |
| Compliance | TBD | TBD | TBD |
| Operations | TBD | TBD | TBD |
| Model/AI | TBD | TBD | TBD |

### Residual risk

- Residual risk description: TBD
- Residual risk owner: TBD
- Risk acceptance or exception ID: TBD
- Expiry or review date: TBD

## Technical debt assessment

**Debt impact:** None / New Debt / Increased Debt / Reduced Debt / Mixed Impact / TBD

**Technical debt score:** TBD

**Assessment rationale:**

TBD

| Debt item | New, increased, reduced, or none | Driver | Impact | Owner | Remediation plan | Due date | Evidence |
|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

### Existing debt affected

- TBD

### New or changed debt

- TBD

### Net debt impact

TBD

## 10. Governance and acceptance

| Role or forum | Named person | Responsibility | Evidence | Date |
|---|---|---|---|---|
| ADR Owner | TBD | Maintains record quality and traceability | TBD | TBD |
| Decision Owner | TBD | Owns decision and lifecycle review | TBD | TBD |
| Architecture reviewer/forum | TBD | Reviews architecture alignment | TBD | TBD |
| Security/risk reviewer | TBD | Reviews control implications | TBD | TBD |
| Business/system owner | TBD | Accepts business or operational impact | TBD | TBD |
| Residual risk owner | TBD | Accepts residual risk where applicable | TBD | TBD |

Approval expectations:

- Tier 0: Local acceptance unless the repository requires otherwise.
- Tier 1: ADR owner, decision owner, and technical or domain reviewer.
- Tier 2: Domain architecture review plus relevant control stakeholders.
- Tier 3: Formal architecture authority plus named risk/control owner acceptance.
- Tier 4: Enterprise architecture governance and senior accountable authority.

## 11. Traceability and evidence

| Evidence type | Link or ID | Notes |
|---|---|---|
| Requirements | TBD | TBD |
| Architecture diagrams | TBD | TBD |
| Threat model | TBD | TBD |
| Risk assessment / TRA | TBD | TBD |
| Standards exception | TBD | TBD |
| Change record | TBD | TBD |
| Pull request / commit | TBD | TBD |
| Test evidence | TBD | TBD |
| Deployment evidence | TBD | TBD |
| Runbook or operational readiness | TBD | TBD |
| Monitoring or alerting | TBD | TBD |

## 12. Implementation plan

Describe the implementation approach, sequencing, dependencies, rollout, rollback, migration, and operational readiness steps.

| Step | Owner | Target date | Evidence |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## 13. Validation plan

Describe how implementation conformance and control effectiveness will be validated.

| Validation activity | Validator | Evidence | Required before release? |
|---|---|---|---|
| Architecture conformance review | TBD | TBD | Yes/No |
| Security control validation | TBD | TBD | Yes/No |
| Resilience or failover test | TBD | TBD | Yes/No |
| Operational readiness review | TBD | TBD | Yes/No |
| Post-implementation review | TBD | TBD | Yes/No |

## 14. Supersession, review, and retirement

- Supersedes: None / ADR links
- Superseded by: None / ADR links
- Review triggers:
  - Material architecture change
  - Security incident, vulnerability, or audit finding
  - Technology standard or reference architecture change
  - Regulatory or policy change
  - Third-party dependency change
  - Operational resilience test or incident outcome
- Retirement or archival notes: TBD

## 15. Open questions and actions

| Action | Owner | Due date | Status |
|---|---|---|---|
| TBD | TBD | TBD | Open |

## 16. References

- TBD
```


## Automation support for ADR lifecycle
This skill can create repository-native automation to manage ADR lifecycle quality gates, review routing, indexing, and release traceability. Prefer lightweight GitHub-native automation first, then integrate enterprise tooling when required.

Default automation artifacts:

```text
.github/workflows/adr-validate.yml
.github/workflows/adr-index.yml
.github/CODEOWNERS
.github/pull_request_template.md
docs/architecture/decisions/_template.md
docs/architecture/decisions/index.md
docs/architecture/decisions/schema/adr.schema.json
scripts/adr/validate-adr.py
scripts/adr/update-adr-index.py
```

### Lifecycle automation objectives

- Validate ADR metadata and required sections on every pull request.
- Prevent invalid lifecycle transitions, especially edits to accepted or rejected ADRs without supersession.
- Require risk-tier appropriate reviewers using CODEOWNERS, branch rules, and pull request checks.
- Route Tier 2 to Tier 4 ADRs to architecture, security, risk, privacy, data, resilience, operations, third-party, model/AI, or compliance reviewers based on metadata.
- Update the ADR index automatically when ADR files are added or changed.
- Detect overdue review dates, expired exceptions, open conditional approvals, and stale technical debt items.
- Produce a pull request summary that identifies decision owner, risk tier, affected domains, required evidence, and validation status.
- Support audit extraction by making ADR metadata machine-readable.

### Recommended GitHub Actions workflow: ADR validation

Create `.github/workflows/adr-validate.yml` when the user requests automation.

```yaml
name: ADR Validation

on:
  pull_request:
    paths:
      - "docs/architecture/decisions/**/*.md"
      - "docs/architecture/decisions/schema/**/*.json"
      - "scripts/adr/**"
  push:
    branches:
      - main
    paths:
      - "docs/architecture/decisions/**/*.md"
      - "docs/architecture/decisions/schema/**/*.json"
      - "scripts/adr/**"

permissions:
  contents: read
  pull-requests: read

jobs:
  validate-adrs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install pyyaml jsonschema

      - name: Validate ADRs
        run: |
          python scripts/adr/validate-adr.py \
            --adr-dir docs/architecture/decisions \
            --schema docs/architecture/decisions/schema/adr.schema.json \
            --base-ref origin/${{ github.base_ref || 'main' }}
```

### Recommended GitHub Actions workflow: ADR index update check

Create `.github/workflows/adr-index.yml` when the user requests automated index enforcement.

```yaml
name: ADR Index Check

on:
  pull_request:
    paths:
      - "docs/architecture/decisions/**/*.md"
      - "scripts/adr/update-adr-index.py"

permissions:
  contents: read

jobs:
  check-index:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install pyyaml

      - name: Regenerate ADR index and fail on drift
        run: |
          python scripts/adr/update-adr-index.py \
            --adr-dir docs/architecture/decisions \
            --index docs/architecture/decisions/index.md
          git diff --exit-code docs/architecture/decisions/index.md
```

### Lifecycle transition rules

The validation automation should enforce these rules:

| From status | To status | Allowed? | Required evidence |
|---|---:|---:|---|
| Candidate | Draft | Yes | ADR owner assigned |
| Draft | Proposed | Yes | Context, options, decision drivers, initial recommendation |
| Proposed | In Review | Yes | Required reviewers identified |
| In Review | Rework | Yes | Open findings or actions |
| Rework | Proposed | Yes | Findings addressed or accepted as conditions |
| Proposed/In Review | Accepted | Yes | Named acceptors, approval date, authority/forum, evidence ID |
| Proposed/In Review | Accepted with Conditions | Yes | Conditions, owners, due dates, residual risk owner where applicable |
| Proposed/In Review | Rejected | Yes | Rejection rationale and path forward |
| Accepted | Implemented | Yes | PR/change/deployment evidence |
| Implemented | Validated | Yes | Test, conformance, operational readiness, or control validation evidence |
| Accepted/Rejected | Draft/In Review/Proposed | No | Create a new superseding ADR instead |
| Accepted/Rejected | Superseded | Yes | Superseding ADR link and reason for change |
| Validated | Deprecated | Yes | Migration or remediation plan |
| Deprecated | Retired | Yes | Retirement evidence |
| Retired | Archived | Yes | Retention class and archive location |

### Risk-tier automation rules

The validation automation should apply stricter checks as risk tier increases:

- Tier 0: permit lightweight ADRs, but require title, context, decision, consequences, owner, and status if an ADR is created.
- Tier 1: require complete metadata, options considered, rationale, decision owner, validation plan, and ADR index entry.
- Tier 2: require architecture review, affected systems, traceability links, implementation plan, and operational impact analysis.
- Tier 3: require named acceptors, residual risk owner where applicable, exception or risk acceptance evidence, control stakeholder review, and explicit conditions or expiry dates.
- Tier 4: require enterprise governance forum, senior accountable authority, strategic impact statement, adoption or migration plan, and review cadence.

### Pull request automation behaviour

When a pull request changes ADR files, automation should:

1. List new, changed, superseded, deprecated, retired, and archived ADRs.
2. Fail if required YAML front matter is missing or invalid.
3. Fail if mandatory sections are missing.
4. Fail if ADR IDs are duplicated.
5. Fail if filenames do not match the configured naming convention.
6. Fail if accepted or rejected ADRs are substantively changed without supersession.
7. Warn when `TBD` appears in accepted ADRs.
8. Warn when review dates, exception expiry dates, or technical-debt due dates are overdue.
9. Warn when Tier 2 to Tier 4 ADRs have missing evidence links.
10. Regenerate or validate `index.md`.

### CODEOWNERS example

Use CODEOWNERS only as a starter. Repositories should align this with actual team names.

```text
# ADR governance ownership
/docs/architecture/decisions/ @architecture-governance
/docs/architecture/decisions/*security* @security-architecture
/docs/architecture/decisions/*identity* @identity-architecture
/docs/architecture/decisions/*crypto* @cryptography-architecture
/docs/architecture/decisions/*data* @data-architecture
/docs/architecture/decisions/*resilience* @sre-operations
```

### Pull request template additions

Add these ADR checks to `.github/pull_request_template.md` when requested:

```markdown
## ADR impact

- [ ] This PR does not require an ADR.
- [ ] This PR creates or updates ADR(s).
- [ ] The ADR index has been updated.
- [ ] Required reviewers are identified based on ADR risk tier and control domains.
- [ ] Accepted or rejected ADRs were not materially changed without supersession.

## ADR references

- ADR(s): TBD
- Risk tier(s): TBD
- Control domain(s): TBD
- Required approval evidence: TBD
```

## ADR template support
This skill supports both a default enterprise-grade ADR template and repository-specific templates. Always prefer the repository's existing template if one exists unless the user asks to replace or standardize it.

### Template discovery order

When creating an ADR, look for templates in this order:

1. `docs/architecture/decisions/_template.md`
2. `docs/adr/_template.md`
3. `.github/ADR_TEMPLATE.md`
4. `.github/ISSUE_TEMPLATE/adr.md`
5. Existing ADR files that clearly show a repository convention
6. The default template embedded in this skill

### Template modes

Support these template modes:

- `default`: use the skill's default regulated ADR template.
- `repo`: derive structure from the current repository's existing ADR template or prior ADRs.
- `minimal`: create a lightweight ADR with essential sections only.
- `regulated`: use full metadata, governance, risk, traceability, and validation sections.
- `custom`: use a user-provided template exactly, adding missing governance fields only if requested.

### Template variables

The template engine should support these variables:

```text
{{adr_id}}
{{sequence_number}}
{{title}}
{{title_slug}}
{{status}}
{{risk_tier}}
{{control_domains}}
{{created_date}}
{{next_review_date}}
{{adr_owner_name}}
{{adr_owner_role}}
{{decision_owner_name}}
{{decision_owner_role}}
{{accountable_role_or_forum}}
{{affected_systems}}
{{decision_context}}
{{decision_outcome}}
{{recommended_reviewers}}
```

### Minimal ADR template

Use this only when the user asks for a lightweight ADR or when repository convention is intentionally minimal.

```markdown
---
adr_id: "{{adr_id}}"
title: "{{title}}"
status: "{{status}}"
risk_tier: "{{risk_tier}}"
control_domains: {{control_domains}}
created_date: "{{created_date}}"
adr_owner:
  name: "{{adr_owner_name}}"
  role: "{{adr_owner_role}}"
decision_owner:
  name: "{{decision_owner_name}}"
  role: "{{decision_owner_role}}"
supersedes: []
superseded_by: []
---

# {{adr_id}}: {{title}}

## Status

{{status}}

## Context

{{decision_context}}

## Decision

{{decision_outcome}}

## Options considered

- Option 1: TBD
- Option 2: TBD
- Status quo / do nothing: TBD

## Consequences

- Positive: TBD
- Negative: TBD
- Neutral: TBD

## Validation

TBD

## References

- TBD
```

### ADR JSON schema support

When automation is requested, create `docs/architecture/decisions/schema/adr.schema.json` to validate YAML front matter. Use this baseline schema and adapt it for repository-specific metadata.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Architecture Decision Record Metadata",
  "type": "object",
  "required": [
    "adr_id",
    "title",
    "status",
    "risk_tier",
    "control_domains",
    "created_date",
    "adr_owner",
    "decision_owner",
    "traceability",
    "supersedes",
    "superseded_by"
  ],
  "properties": {
    "adr_id": { "type": "string", "pattern": "^ADR-[0-9]{4}-[0-9]{4}$|^ADR-[0-9]{4}$|^[0-9]{4}$" },
    "title": { "type": "string", "minLength": 5 },
    "status": {
      "type": "string",
      "enum": [
        "Candidate",
        "Draft",
        "Proposed",
        "In Review",
        "Rework",
        "Accepted",
        "Accepted with Conditions",
        "Rejected",
        "Implemented",
        "Validated",
        "Deferred",
        "Superseded",
        "Deprecated",
        "Retired",
        "Archived"
      ]
    },
    "risk_tier": { "type": "string", "enum": ["Tier 0", "Tier 1", "Tier 2", "Tier 3", "Tier 4"] },
    "control_domains": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" }
    },
    "created_date": { "type": "string" },
    "adr_owner": {
      "type": "object",
      "required": ["name", "role"],
      "properties": {
        "name": { "type": "string" },
        "role": { "type": "string" }
      }
    },
    "decision_owner": {
      "type": "object",
      "required": ["name", "role"],
      "properties": {
        "name": { "type": "string" },
        "role": { "type": "string" }
      }
    },
    "acceptors": { "type": "array" },
    "traceability": { "type": "object" },
    "supersedes": { "type": "array" },
    "superseded_by": { "type": "array" },
    "legal_hold": { "type": "boolean" }
  },
  "additionalProperties": true
}
```

### Baseline validation script support

When the user requests implementation files, generate `scripts/adr/validate-adr.py`. The script should:

- Parse YAML front matter from Markdown files.
- Validate metadata against `adr.schema.json`.
- Check required Markdown headings.
- Detect duplicate ADR IDs.
- Detect invalid status and risk tier.
- Enforce accepted and conditional acceptance evidence requirements.
- Enforce Tier 2 to Tier 4 evidence expectations.
- Detect overdue dates when dates are provided.
- Optionally compare changed ADRs against the base branch to flag substantive edits to accepted or rejected ADRs.
- Exit with non-zero status on blocking errors.
- Print warnings for non-blocking issues.

### Baseline index update script support

When the user requests implementation files, generate `scripts/adr/update-adr-index.py`. The script should:

- Scan ADR Markdown files.
- Parse YAML front matter.
- Sort ADRs by sequence number or ADR ID.
- Write `docs/architecture/decisions/index.md`.
- Include columns for ADR, title, status, risk tier, decision owner, accepted date, next review date, technical debt impact, technical debt score, supersedes, and superseded by.
- Preserve a short explanatory heading in the index.


## Technical debt assessment model
ADRs must not allow an unsupported declaration of `Technical debt: None`. Every ADR must include a technical debt impact assessment that explains whether the decision introduces new debt, increases existing debt, reduces existing debt, or has no material technical debt impact.

### Technical debt impact values

Use one of the following values:

- `None`
- `New Debt`
- `Increased Debt`
- `Reduced Debt`
- `Mixed Impact`
- `TBD`

### How to determine technical debt impact

Classify technical debt based on the effect of the decision on future maintainability, control posture, operational burden, architectural alignment, lifecycle risk, and remediation obligations.

#### New Debt

Use `New Debt` when the ADR introduces one or more of the following:

- Temporary workaround or tactical implementation.
- Deferred control, deferred automation, or deferred remediation.
- Compensating control required because the preferred control is not implemented.
- Standards exception, reference architecture deviation, or non-standard integration.
- Unsupported, deprecated, end-of-life, or non-strategic technology.
- Manual operational process that should be automated.
- Known design limitation accepted for schedule, cost, dependency, or delivery reasons.
- Increased coupling, duplicated capability, custom framework, or bespoke integration.
- Missing test, monitoring, rollback, observability, resilience, or operational readiness capability.

#### Increased Debt

Use `Increased Debt` when the ADR worsens or extends an existing debt condition, including:

- Expanding the scope of an existing exception.
- Extending the life of unsupported or deprecated technology.
- Delaying an existing remediation plan.
- Increasing the number of systems dependent on a known problematic pattern.
- Adding operational complexity to a fragile or constrained design.
- Increasing cost, maintenance effort, or support burden associated with a known debt item.

#### Reduced Debt

Use `Reduced Debt` when the ADR reduces or eliminates existing debt, including:

- Retiring legacy or unsupported technology.
- Removing a standards exception or compensating control.
- Replacing manual operational activity with automation.
- Consolidating duplicate capabilities.
- Aligning implementation to approved reference architecture.
- Improving validation, observability, resilience, or supportability.
- Reducing custom code, bespoke integration, or non-standard platform dependency.

#### None

Use `None` only when the ADR includes a rationale explaining why no material technical debt is introduced, increased, or reduced.

A valid `None` rationale should confirm that the decision:

- Aligns with approved reference architecture and technology standards.
- Introduces no new exception, workaround, deferred control, or compensating control.
- Does not extend the life of unsupported, deprecated, or non-strategic technology.
- Does not increase manual operations, complexity, coupling, or support burden.
- Does not defer test, monitoring, resilience, security, privacy, data, or operational readiness controls.

### Technical debt scoring model

Use the score as a directional governance indicator. It is not a substitute for expert review.

| Indicator | Score |
|---|---:|
| Security exception or deferred security control | +5 |
| Unsupported, deprecated, or end-of-life technology | +5 |
| Standards exception or reference architecture deviation | +3 |
| Temporary workaround or tactical solution | +3 |
| Compensating control required | +3 |
| Manual operational process introduced or extended | +2 |
| Missing automation | +2 |
| Increased operational complexity | +2 |
| Increased coupling or additional dependency | +1 |
| Missing validation, observability, or runbook evidence | +2 |
| Delayed remediation date or extended exception | +2 |
| Retires unsupported technology | -5 |
| Removes exception or compensating control | -5 |
| Replaces manual process with automation | -3 |
| Aligns to approved reference architecture | -2 |
| Reduces coupling or removes duplicate capability | -2 |

Score interpretation:

| Net score | Interpretation |
|---:|---|
| Less than or equal to 0 | Debt reduced or no measurable debt increase |
| 1 to 3 | Low debt increase |
| 4 to 8 | Moderate debt increase |
| 9 or higher | Significant debt increase requiring explicit governance attention |

### Required technical debt fields

Each ADR must include this structure in YAML front matter:

```yaml
technical_debt_assessment:
  impact: "None"
  score: 0
  rationale: "TBD"
  existing_debt_references: []
  new_or_changed_debt_items: []
  debt_owner:
    name: ""
    role: ""
  remediation_plan: ""
  remediation_due_date: ""
  review_date: ""
  related_exceptions_or_risk_acceptances: []
```

Each ADR must include this Markdown section:

```markdown
## Technical debt assessment

**Debt impact:** None / New Debt / Increased Debt / Reduced Debt / Mixed Impact / TBD

**Technical debt score:** TBD

**Assessment rationale:**

TBD

| Debt item | New, increased, reduced, or none | Driver | Impact | Owner | Remediation plan | Due date | Evidence |
|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

### Existing debt affected

- TBD

### New or changed debt

- TBD

### Net debt impact

TBD
```

### Technical debt validation rules

Validation must fail for accepted ADRs when:

- Technical debt impact is `None` but no rationale is provided.
- Technical debt impact is `New Debt`, `Increased Debt`, or `Mixed Impact` but no owner is assigned.
- Technical debt impact is `New Debt`, `Increased Debt`, or `Mixed Impact` but no remediation plan is provided.
- Technical debt impact is `New Debt`, `Increased Debt`, or `Mixed Impact` but no due date or review date is provided.
- A standards exception, risk acceptance, compensating control, unsupported technology, or deferred control is described elsewhere in the ADR but the debt impact is marked `None`.
- The debt score is `9` or higher and no governance escalation or explicit acceptance evidence is provided.

Validation should warn when:

- Technical debt score and rationale appear inconsistent.
- Debt is reduced but no retired debt item, removed exception, or operational simplification is identified.
- `TBD` remains in technical debt fields for Tier 2 to Tier 4 ADRs.
- Technical debt remediation due date is overdue.
- Technical debt review date is overdue.

### Technical debt automation behavior

When creating ADR automation files, the validation script should:

1. Parse `technical_debt_assessment` from YAML front matter.
2. Calculate or verify the technical debt score when debt indicators are provided.
3. Search ADR body text for debt indicators such as `exception`, `temporary`, `manual`, `unsupported`, `deprecated`, `compensating control`, `deferred`, `workaround`, `technical debt`, and `remediation`.
4. Warn if debt indicators are present but impact is marked `None`.
5. Fail accepted ADRs with unmanaged technical debt.
6. Include technical debt impact and score in the ADR index.
7. Include overdue debt remediation in audit or dashboard outputs.

### Technical debt examples

#### Valid None example

```markdown
**Debt impact:** None

**Technical debt score:** 0

**Assessment rationale:**
The decision aligns to the approved reference architecture, introduces no standards exception, uses supported platform capabilities, does not defer required controls, and does not add manual operational activity or non-standard dependencies.
```

#### New Debt example

```markdown
**Debt impact:** New Debt

**Technical debt score:** 7

**Assessment rationale:**
The decision introduces a temporary manual certificate rotation process and defers automation until the platform integration is available.

| Debt item | New, increased, reduced, or none | Driver | Impact | Owner | Remediation plan | Due date | Evidence |
|---|---|---|---|---|---|---|---|
| Manual certificate rotation | New | Platform dependency unavailable | Increased operational burden and rotation error risk | Platform Security Lead | Implement automated certificate lifecycle management | 2027-03-31 | Backlog item TBD |
```

#### Increased Debt example

```markdown
**Debt impact:** Increased Debt

**Technical debt score:** 10

**Assessment rationale:**
The decision extends an existing unsupported authentication integration from five applications to twelve applications and delays the current remediation plan.
```

#### Reduced Debt example

```markdown
**Debt impact:** Reduced Debt

**Technical debt score:** -8

**Assessment rationale:**
The decision retires a custom secrets store, removes a standards exception, and replaces manual secret rotation with managed platform automation.
```

## Workflow: initialize ADR support in a repository
When the user asks to initialize ADRs in a GitHub repository:

1. Inspect the repository structure if files are available.
2. If an ADR convention already exists, preserve it.
3. If no convention exists, create the default folder:

   ```text
   docs/architecture/decisions/
   ```

4. Create `_template.md` using the ADR Markdown template above.
5. Create `README.md` explaining how to create, review, accept, supersede, and validate ADRs.
6. Create `index.md` with a table of ADRs.
7. If requested, create a GitHub pull request description with summary, governance rationale, files changed, and validation steps.

Default `README.md` content:

```markdown
# Architecture Decision Records

This folder contains Architecture Decision Records (ADRs) for this repository.

ADRs capture architecturally significant decisions, including context, options, decision outcome, rationale, consequences, governance acceptance, risk/control impacts, and traceability evidence.

## When an ADR is required

Create an ADR when a decision materially affects architecture, security, resilience, data, regulatory obligations, operational support, third-party dependency, standards alignment, technical debt, or implementation constraints.

## Lifecycle

ADRs may use these states: Candidate, Draft, Proposed, In Review, Rework, Accepted, Accepted with Conditions, Rejected, Implemented, Validated, Deferred, Superseded, Deprecated, Retired, Archived.

Accepted and rejected ADRs should not be substantively overwritten. Create a new ADR to supersede a prior accepted or rejected decision.

## Naming

Use `NNNN-short-decision-title.md`, for example `0001-use-managed-key-vault.md`.

## Minimum evidence

Accepted ADRs should include owners, acceptors, decision authority, rationale, alternatives, risk/control impacts, traceability links, and validation evidence.
```

Default `index.md` content:

```markdown
# ADR Index

| ADR | Title | Status | Risk tier | Decision owner | Accepted date | Supersedes | Superseded by |
|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
```

## Workflow: create a new ADR
When creating a new ADR:

1. Gather or infer the decision title, context, options, chosen outcome, risk tier, control domains, owners, and evidence links.
2. If required information is missing, use `TBD` and create an action item rather than inventing facts.
3. Determine the next ADR number by scanning existing ADR filenames.
4. Create the filename using the next number and a lowercase hyphenated slug.
5. Populate YAML front matter.
6. Populate each ADR section using concise, evidence-oriented language.
7. Include explicit alternatives, including status quo or do nothing.
8. Include risk/control impacts proportionate to the tier.
9. Include named individuals and durable roles where provided.
10. Include traceability links when provided.
11. Include validation plan and review triggers.
12. Update `index.md` when possible.
13. Provide a pull request-ready summary.

## Workflow: review an ADR
When reviewing an ADR, evaluate it against these checks:

### Completeness checks

- ADR ID exists and is unique.
- Title is a decision statement, not a topic label.
- Status is valid.
- Risk tier is present.
- Control domains are present.
- ADR owner and decision owner are identified.
- Accountable role or forum is identified.
- Named acceptors are present for accepted ADRs.
- Context and decision drivers are clear.
- Options considered include credible alternatives.
- Decision outcome is explicit.
- Rationale explains why the selected option was chosen.
- Consequences include positive and negative trade-offs.
- Risk/control impacts are addressed.
- Traceability links are included or explicitly marked as not applicable.
- Validation plan identifies validator, evidence, and release dependency.
- Supersession links are maintained where applicable.

### Governance checks

- Tier 2-4 ADRs include appropriate architecture and control stakeholder review.
- Tier 3-4 ADRs include explicit residual risk ownership where residual risk exists.
- Exceptions or technical debt have owner, due date, and remediation path.
- Accepted with Conditions includes conditions, owners, dates, and evidence IDs.
- Accepted or rejected ADRs have not been materially rewritten without supersession.

### Output format for review findings

```markdown
## ADR Review Findings

### Summary

- Overall assessment: Pass / Pass with observations / Needs rework
- Highest severity finding: Critical / High / Medium / Low / None
- Recommended next state: Draft / Proposed / In Review / Accepted / Accepted with Conditions / Rework

### Findings

| Severity | Area | Finding | Recommended correction |
|---|---|---|---|
| High | Traceability | TBD | TBD |

### Missing evidence

- TBD

### Suggested wording changes

- TBD
```

## Workflow: supersede an ADR
When superseding an ADR:

1. Create a new ADR with the next available number.
2. Set the new ADR `supersedes` field to the prior ADR ID or filename.
3. In the prior ADR, only update metadata and supersession notes if repository policy allows non-substantive lifecycle updates.
4. Set the prior ADR status to `Superseded` and `superseded_by` to the new ADR.
5. Do not rewrite the prior rationale, acceptance, or decision content.
6. Explain why the decision changed and what migration actions are required.

## Workflow: generate a pull request description
Use this PR description format when adding or changing ADRs:

```markdown
## Summary

Adds or updates Architecture Decision Record(s) for [decision/system].

## ADRs changed

| ADR | Change type | Status | Risk tier |
|---|---|---|---|
| ADR-YYYY-NNNN | New / Updated / Superseded | Draft | Tier X |

## Governance notes

- Decision owner: TBD
- Required reviewers: TBD
- Risk/control domains: TBD
- Approval evidence: TBD

## Traceability

- Requirements: TBD
- Threat/risk assessment: TBD
- Change record: TBD
- Pull requests: TBD
- Validation evidence: TBD

## Validation

- [ ] ADR metadata complete
- [ ] Options and rationale documented
- [ ] Risk/control impacts documented
- [ ] Required reviewers identified
- [ ] Index updated
```

## Writing guidance
Use this tone and style:

- Clear, concise, professional, and audit-ready.
- Prefer active voice: `We will use...`, `The platform will enforce...`.
- Avoid vague language such as `best practice`, `secure`, `robust`, or `enterprise-grade` unless evidence explains why.
- Distinguish facts from assumptions.
- Use `TBD` for missing facts instead of inventing evidence.
- Capture rejected options respectfully and objectively.
- Explain trade-offs directly.
- Include both benefits and adverse consequences.
- Keep the ADR focused on one decision. Split unrelated decisions into separate ADRs.

## Validation rules for generated ADRs
Before returning a generated ADR or automation package, perform a secondary consistency check. Do not rely only on template generation.

### Structural validation

- ADR has YAML front matter bounded by `---` delimiters.
- ADR has exactly one top-level `# ADR...` heading.
- Required sections are present: Status, Executive decision summary, Context and problem statement, Decision drivers, Options considered, Decision outcome, Rationale, Consequences and trade-offs, Risk and control impact, Governance and acceptance, Traceability and evidence, Implementation plan, Validation plan, Supersession/review/retirement, Open questions/actions, and References.
- Title is a decision statement, not merely a topic label.
- Filename matches the repository naming convention or the default `NNNN-title-slug.md` convention.
- ADR ID is unique and matches the filename sequence where applicable.
- `index.md` is updated or an explicit note explains why index update was not possible.

### Metadata validation

- `adr_id`, `title`, `status`, `risk_tier`, `control_domains`, `created_date`, `adr_owner`, `decision_owner`, `traceability`, `supersedes`, and `superseded_by` are present.
- Status appears in the approved lifecycle state list.
- Risk tier appears in the approved Tier 0 to Tier 4 list.
- At least one control domain is identified.
- Dates use ISO format `YYYY-MM-DD` where actual dates are known.
- Owners include both name and role when provided.
- Missing facts are marked `TBD` and linked to an action item.
- No fabricated names, dates, approvals, evidence IDs, or links are introduced.

### Decision-quality validation

- The ADR covers one decision only. Split unrelated decisions into separate ADRs.
- Context explains why the decision is architecturally significant.
- At least two credible options are documented unless the user explicitly provides only one.
- `Status quo / do nothing` is considered unless explicitly not applicable.
- The selected decision is stated clearly using active voice.
- Rationale links the selected decision to drivers, constraints, evidence, and rejected options.
- Positive, negative, and neutral consequences are documented.
- Assumptions and dependencies are explicit.

### Risk and governance validation

- Technical debt impact is assessed as `None`, `New Debt`, `Increased Debt`, `Reduced Debt`, `Mixed Impact`, or `TBD`.
- `None` technical debt impact includes a rationale.
- New, increased, or mixed technical debt includes owner, remediation plan, due date or review date, and related exception or risk acceptance where applicable.
- Significant technical debt score identifies governance escalation or acceptance evidence.
- Tier 2 to Tier 4 ADRs identify required architecture and control reviewers.
- Tier 3 to Tier 4 ADRs identify named acceptors, durable role/forum, authority basis, date, and approval evidence when the ADR is accepted.
- Accepted with Conditions includes conditions, owners, due dates, and evidence IDs.
- Residual risks have an accountable owner and risk acceptance or exception reference where applicable.
- Technical debt has owner, remediation plan, and due date.
- Security, privacy, data, resilience, third-party, model/AI, compliance, and operations impacts are addressed when selected as control domains.
- Traceability links are provided or explicitly marked `TBD` or `Not applicable`.
- Validation activities identify validator, evidence, and whether completion is required before release.

### Lifecycle validation

- Accepted and rejected ADRs are not substantively rewritten.
- Supersession uses a new ADR and links both predecessor and successor when repository policy permits lifecycle metadata updates.
- Deprecated ADRs include migration or remediation plan.
- Retired ADRs include retirement evidence.
- Archived ADRs include retention classification and archive location when known.
- Review triggers and next review date are present for material ADRs.

### Automation validation

When generating automation files, verify:

- GitHub workflow paths match the repository ADR directory.
- The validation workflow installs required dependencies.
- The validation command points to the correct ADR directory and schema path.
- JSON schema required fields match the ADR YAML template.
- CODEOWNERS entries are placeholders unless actual teams are provided.
- Pull request template checks align with the lifecycle and risk tier rules.
- Scripts fail on blocking validation errors and warn on non-blocking quality issues.

### Output validation checklist

Return a short checklist with generated outputs:

```markdown
## Generation validation checklist

- [x] ADR template included or repository template preserved
- [x] YAML front matter included
- [x] Required lifecycle states supported
- [x] Risk-tier validation included
- [x] Traceability fields included
- [x] Governance and acceptance fields included
- [x] Validation plan included
- [x] Supersession support included
- [x] ADR index support included
- [x] Automation files included when requested
```

## Example prompt handling

### User asks: "Create an ADR for using Azure Key Vault for secrets"
Return:

- Proposed filename, for example `0001-use-managed-key-vault-for-application-secrets.md`.
- Completed ADR Markdown.
- Any assumptions and `TBD` items.
- Suggested reviewers.
- Suggested PR description.

### User asks: "Initialize this repo for ADRs"
Return:

- Folder structure.
- `_template.md`.
- `README.md`.
- `index.md`.
- Optional PR description.

### User asks: "Review this ADR"
Return:

- Completeness findings.
- Governance findings.
- Missing evidence.
- Recommended next state.
- Specific wording corrections.

## Safety and confidentiality

- Do not invent approvals, named acceptors, evidence IDs, risk acceptances, or committee decisions.
- Do not include secrets, credentials, private keys, tokens, or sensitive production details in ADRs.
- If the user provides sensitive information, summarize at an appropriate level and recommend storing sensitive evidence in approved systems with links or evidence IDs.
- For regulated or high-risk decisions, clearly identify missing risk, security, privacy, resilience, third-party, model/AI, or compliance evidence.


## Implementation file templates for ADR automation
When the user asks to implement automation, generate these files as copy/paste-ready repository artifacts. The scripts are intentionally dependency-light and designed to run in GitHub Actions or locally.

### File: `scripts/adr/validate-adr.py`

Purpose:

- Parse Markdown ADR files with YAML front matter.
- Validate required metadata and lifecycle status values.
- Validate required ADR sections.
- Detect duplicate ADR IDs.
- Detect technical debt indicators and calculate a directional score.
- Fail accepted or implemented ADRs that contain unmanaged debt.
- Warn on draft/proposed ADRs that appear inconsistent.
- Optionally detect substantive edits to accepted or rejected ADRs when a base Git ref is available.

```python
#!/usr/bin/env python3
"""
validate-adr.py

Validates Architecture Decision Records stored as Markdown files with YAML front matter.
Designed for GitHub Actions and local execution.

Example usage:
  python scripts/adr/validate-adr.py --adr-dir docs/architecture/decisions
  python scripts/adr/validate-adr.py --adr-dir docs/architecture/decisions --fail-on-unmanaged-debt
  python scripts/adr/validate-adr.py --adr-dir docs/architecture/decisions --schema docs/architecture/decisions/schema/adr.schema.json
  python scripts/adr/validate-adr.py --adr-dir docs/architecture/decisions --base-ref origin/main
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: Missing dependency PyYAML. Install with: python -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    import jsonschema
except ImportError:  # schema validation is optional
    jsonschema = None

VALID_STATUSES = {
    "Candidate",
    "Draft",
    "Proposed",
    "In Review",
    "Rework",
    "Accepted",
    "Accepted with Conditions",
    "Rejected",
    "Implemented",
    "Validated",
    "Deferred",
    "Superseded",
    "Deprecated",
    "Retired",
    "Archived",
}

BLOCKING_STATUSES = {
    "Accepted",
    "Accepted with Conditions",
    "Implemented",
    "Validated",
}

VALID_RISK_TIERS = {"Tier 0", "Tier 1", "Tier 2", "Tier 3", "Tier 4"}

VALID_DEBT_IMPACTS = {"None", "New Debt", "Increased Debt", "Reduced Debt", "Mixed Impact", "TBD"}

REQUIRED_METADATA = [
    "adr_id",
    "title",
    "status",
    "risk_tier",
    "control_domains",
    "created_date",
    "adr_owner",
    "decision_owner",
    "traceability",
    "supersedes",
    "superseded_by",
]

REQUIRED_HEADINGS = [
    "Status",
    "Context",
    "Decision",
    "Options",
    "Consequences",
    "Risk",
    "Technical debt",
    "Traceability",
    "Validation",
]

DEBT_INDICATORS = {
    "security exception": 5,
    "deferred security control": 5,
    "unsupported": 5,
    "deprecated": 5,
    "end-of-life": 5,
    "eol": 5,
    "standards exception": 3,
    "reference architecture deviation": 3,
    "temporary": 3,
    "workaround": 3,
    "compensating control": 3,
    "manual operational": 2,
    "manual process": 2,
    "manual": 2,
    "missing automation": 2,
    "increased complexity": 2,
    "additional dependency": 1,
    "legacy": 2,
    "custom integration": 2,
    "bespoke": 2,
    "deferred": 2,
    "defer": 2,
    "remediation": 1,
    "risk acceptance": 3,
    "known limitation": 2,
    "non-standard": 3,
    "not strategic": 2,
}

DEBT_REDUCTION_INDICATORS = {
    "retires unsupported": -5,
    "retire unsupported": -5,
    "removes exception": -5,
    "remove exception": -5,
    "removes compensating control": -5,
    "replace manual": -3,
    "replaces manual": -3,
    "automation": -2,
    "aligns to approved reference architecture": -2,
    "reduces coupling": -2,
    "removes duplicate": -2,
}

@dataclass
class FindingSet:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_front_matter(text: str, path: Path, findings: FindingSet) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        findings.error(f"{path}: missing YAML front matter delimiters.")
        return {}, text

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, flags=re.DOTALL)
    if not match:
        findings.error(f"{path}: malformed YAML front matter.")
        return {}, text

    yaml_text, body = match.group(1), match.group(2)
    try:
        data = yaml.safe_load(yaml_text) or {}
        if not isinstance(data, dict):
            findings.error(f"{path}: YAML front matter must be a mapping/object.")
            return {}, body
        return data, body
    except Exception as exc:
        findings.error(f"{path}: cannot parse YAML front matter: {exc}")
        return {}, body


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def calculate_debt_score(text: str) -> tuple[int, list[str], list[str]]:
    lowered = normalize_text(text)
    score = 0
    positive_matches: list[str] = []
    reduction_matches: list[str] = []

    for term, weight in DEBT_INDICATORS.items():
        if term in lowered:
            score += weight
            positive_matches.append(term)

    for term, weight in DEBT_REDUCTION_INDICATORS.items():
        if term in lowered:
            score += weight
            reduction_matches.append(term)

    return score, positive_matches, reduction_matches


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list | tuple | set | dict):
        return len(value) == 0
    return False


def parse_iso_date(value: Any) -> dt.date | None:
    if not value:
        return None
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def get_nested(data: dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def validate_schema(metadata: dict[str, Any], schema_path: Path | None, path: Path, findings: FindingSet) -> None:
    if not schema_path:
        return
    if not schema_path.exists():
        findings.error(f"Schema file not found: {schema_path}")
        return
    if jsonschema is None:
        findings.warn("jsonschema package is not installed; skipping JSON schema validation.")
        return
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.validate(instance=metadata, schema=schema)
    except Exception as exc:
        findings.error(f"{path}: schema validation failed: {exc}")


def validate_metadata(metadata: dict[str, Any], path: Path, findings: FindingSet) -> None:
    for field_name in REQUIRED_METADATA:
        if field_name not in metadata:
            findings.error(f"{path}: missing required metadata field '{field_name}'.")

    status = metadata.get("status")
    if status and status not in VALID_STATUSES:
        findings.error(f"{path}: invalid status '{status}'.")

    risk_tier = metadata.get("risk_tier")
    if risk_tier and risk_tier not in VALID_RISK_TIERS:
        findings.error(f"{path}: invalid risk_tier '{risk_tier}'.")

    control_domains = metadata.get("control_domains")
    if not isinstance(control_domains, list) or not control_domains:
        findings.error(f"{path}: control_domains must be a non-empty list.")

    for owner_field in ("adr_owner", "decision_owner"):
        owner = metadata.get(owner_field)
        if not isinstance(owner, dict):
            findings.error(f"{path}: {owner_field} must contain name and role.")
            continue
        if is_blank(owner.get("name")) and is_blank(owner.get("role")):
            findings.warn(f"{path}: {owner_field} has neither name nor role populated.")

    created = metadata.get("created_date")
    if created and parse_iso_date(created) is None:
        findings.warn(f"{path}: created_date should use YYYY-MM-DD format.")


def validate_headings(body: str, path: Path, findings: FindingSet) -> None:
    headings = [m.group(2).strip().lower() for m in re.finditer(r"^(#{1,6})\s+(.+)$", body, flags=re.MULTILINE)]
    heading_text = "\n".join(headings)
    for required in REQUIRED_HEADINGS:
        if required.lower() not in heading_text:
            findings.warn(f"{path}: expected ADR section containing heading text '{required}'.")


def validate_technical_debt(metadata: dict[str, Any], body: str, path: Path, findings: FindingSet) -> None:
    status = metadata.get("status", "")
    debt = metadata.get("technical_debt_assessment") or {}
    if not isinstance(debt, dict):
        findings.error(f"{path}: technical_debt_assessment must be an object.")
        return

    impact = debt.get("impact", "TBD")
    declared_score = debt.get("score")
    rationale = debt.get("rationale", "")
    owner = debt.get("debt_owner") or {}
    remediation_plan = debt.get("remediation_plan", "")
    remediation_due_date = debt.get("remediation_due_date", "")
    review_date = debt.get("review_date", "")
    evidence = debt.get("related_exceptions_or_risk_acceptances") or []

    combined_text = body + "\n" + json.dumps(metadata, default=str)
    score, debt_matches, reduction_matches = calculate_debt_score(combined_text)

    if impact not in VALID_DEBT_IMPACTS:
        findings.error(f"{path}: invalid technical debt impact '{impact}'.")

    if impact == "None" and is_blank(rationale):
        findings.error(f"{path}: technical debt impact is None but rationale is missing.")

    if impact == "None" and debt_matches:
        message = f"{path}: debt impact is None but debt indicators were detected: {', '.join(sorted(set(debt_matches)))}."
        if status in BLOCKING_STATUSES:
            findings.error(message)
        else:
            findings.warn(message)

    if impact in {"New Debt", "Increased Debt", "Mixed Impact"}:
        if not isinstance(owner, dict) or (is_blank(owner.get("name")) and is_blank(owner.get("role"))):
            findings.error(f"{path}: technical debt exists but no debt owner is assigned.")
        if is_blank(remediation_plan):
            findings.error(f"{path}: technical debt exists but remediation plan is missing.")
        if is_blank(remediation_due_date) and is_blank(review_date):
            findings.error(f"{path}: technical debt exists but remediation due date or review date is missing.")

    if declared_score not in (None, ""):
        try:
            declared_int = int(declared_score)
            if abs(declared_int - score) >= 5:
                findings.warn(f"{path}: declared technical debt score {declared_int} differs materially from detected score {score}.")
        except Exception:
            findings.warn(f"{path}: technical debt score should be numeric.")

    if score >= 9 and status in BLOCKING_STATUSES and not evidence:
        findings.error(f"{path}: detected significant technical debt score {score}; governance evidence, exception, or risk acceptance is required.")

    if impact == "Reduced Debt" and not reduction_matches:
        findings.warn(f"{path}: debt impact is Reduced Debt but no debt-reduction indicators were detected.")

    today = dt.date.today()
    for date_field in ("remediation_due_date", "review_date"):
        raw = debt.get(date_field)
        parsed = parse_iso_date(raw)
        if raw and parsed is None:
            findings.warn(f"{path}: {date_field} should use YYYY-MM-DD format.")
        if parsed and parsed < today and impact in {"New Debt", "Increased Debt", "Mixed Impact"}:
            findings.warn(f"{path}: {date_field} is overdue: {parsed.isoformat()}.")


def validate_acceptance(metadata: dict[str, Any], path: Path, findings: FindingSet) -> None:
    status = metadata.get("status", "")
    risk_tier = metadata.get("risk_tier", "")
    acceptors = metadata.get("acceptors") or []

    if status in {"Accepted", "Accepted with Conditions", "Implemented", "Validated"}:
        if not isinstance(acceptors, list) or not acceptors:
            findings.error(f"{path}: accepted/implemented ADR requires named acceptors or approval forum evidence.")
        if is_blank(metadata.get("accepted_date")):
            findings.error(f"{path}: accepted/implemented ADR requires accepted_date.")

    if status == "Accepted with Conditions":
        debt = metadata.get("technical_debt_assessment") or {}
        exceptions = metadata.get("exceptions_or_risk_acceptances") or []
        if not exceptions and is_blank(debt.get("related_exceptions_or_risk_acceptances")):
            findings.warn(f"{path}: Accepted with Conditions should reference conditions, exceptions, or risk acceptance evidence.")

    if risk_tier in {"Tier 3", "Tier 4"} and status in BLOCKING_STATUSES:
        if is_blank(metadata.get("accountable_role_or_forum")):
            findings.error(f"{path}: Tier 3/4 accepted ADR requires accountable_role_or_forum.")
        if is_blank(get_nested(metadata, "residual_risk_owner", "name")) and is_blank(get_nested(metadata, "residual_risk_owner", "role")):
            findings.warn(f"{path}: Tier 3/4 accepted ADR should identify residual_risk_owner when residual risk exists.")


def validate_supersession(metadata: dict[str, Any], path: Path, findings: FindingSet) -> None:
    status = metadata.get("status", "")
    supersedes = metadata.get("supersedes") or []
    superseded_by = metadata.get("superseded_by") or []
    if status == "Superseded" and not superseded_by:
        findings.error(f"{path}: Superseded ADR must identify superseded_by.")
    if supersedes and not isinstance(supersedes, list):
        findings.error(f"{path}: supersedes must be a list.")
    if superseded_by and not isinstance(superseded_by, list):
        findings.error(f"{path}: superseded_by must be a list.")


def git_show(base_ref: str, path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "show", f"{base_ref}:{path.as_posix()}"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            return None
        return result.stdout
    except Exception:
        return None


def strip_non_substantive(text: str) -> str:
    # Normalize content and ignore lifecycle-only fields that may be allowed by policy.
    ignored = {
        "status",
        "superseded_by",
        "implemented_date",
        "validated_date",
        "next_review_date",
    }
    findings = FindingSet()
    metadata, body = extract_front_matter(text, Path("baseline"), findings)
    for key in ignored:
        metadata.pop(key, None)
    return normalize_text(json.dumps(metadata, sort_keys=True, default=str) + "\n" + body)


def validate_immutable_history(path: Path, metadata: dict[str, Any], current_text: str, base_ref: str | None, findings: FindingSet) -> None:
    if not base_ref:
        return
    previous_text = git_show(base_ref, path)
    if previous_text is None:
        return
    prior_findings = FindingSet()
    prior_metadata, _ = extract_front_matter(previous_text, path, prior_findings)
    prior_status = prior_metadata.get("status")
    if prior_status in {"Accepted", "Rejected"}:
        if strip_non_substantive(previous_text) != strip_non_substantive(current_text):
            current_status = metadata.get("status")
            if current_status != "Superseded":
                findings.error(f"{path}: accepted/rejected ADR appears substantively changed. Create a superseding ADR instead.")


def validate_file(path: Path, schema_path: Path | None, base_ref: str | None) -> FindingSet:
    findings = FindingSet()
    text = read_text(path)
    metadata, body = extract_front_matter(text, path, findings)
    if not metadata:
        return findings
    validate_schema(metadata, schema_path, path, findings)
    validate_metadata(metadata, path, findings)
    validate_headings(body, path, findings)
    validate_technical_debt(metadata, body, path, findings)
    validate_acceptance(metadata, path, findings)
    validate_supersession(metadata, path, findings)
    validate_immutable_history(path, metadata, text, base_ref, findings)
    return findings


def find_adr_files(adr_dir: Path) -> list[Path]:
    if not adr_dir.exists():
        raise FileNotFoundError(f"ADR directory not found: {adr_dir}")
    return sorted(
        p for p in adr_dir.rglob("*.md")
        if p.name.lower() not in {"readme.md", "index.md", "_template.md"}
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Architecture Decision Records.")
    parser.add_argument("--adr-dir", default="docs/architecture/decisions", help="ADR directory")
    parser.add_argument("--schema", default="", help="Optional JSON schema path")
    parser.add_argument("--base-ref", default="", help="Optional Git base ref for immutable history checks")
    parser.add_argument("--fail-on-warnings", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--fail-on-unmanaged-debt", action="store_true", help="Reserved flag for compatibility; unmanaged accepted debt already fails")
    args = parser.parse_args()

    adr_dir = Path(args.adr_dir)
    schema_path = Path(args.schema) if args.schema else None
    base_ref = args.base_ref or None

    all_errors: list[str] = []
    all_warnings: list[str] = []

    try:
        files = find_adr_files(adr_dir)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not files:
        print(f"WARNING: No ADR Markdown files found under {adr_dir}")
        return 0

    seen_ids: dict[str, Path] = {}
    for file_path in files:
        findings = validate_file(file_path, schema_path, base_ref)
        all_errors.extend(findings.errors)
        all_warnings.extend(findings.warnings)

        metadata, _ = extract_front_matter(read_text(file_path), file_path, FindingSet())
        adr_id = metadata.get("adr_id")
        if adr_id:
            if adr_id in seen_ids:
                all_errors.append(f"Duplicate ADR ID '{adr_id}' in {file_path} and {seen_ids[adr_id]}.")
            else:
                seen_ids[adr_id] = file_path

    for warning in all_warnings:
        print(f"WARNING: {warning}")
    for error in all_errors:
        print(f"ERROR: {error}", file=sys.stderr)

    print(f"Validated {len(files)} ADR file(s): {len(all_errors)} error(s), {len(all_warnings)} warning(s).")

    if all_errors or (args.fail_on_warnings and all_warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### File: `scripts/adr/update-adr-index.py`

Purpose:

- Generate or refresh `docs/architecture/decisions/index.md`.
- Include technical debt impact and score so governance can trend debt across ADRs.
- Keep the ADR register machine-generated and reviewable in pull requests.

```python
#!/usr/bin/env python3
"""
update-adr-index.py

Regenerates a Markdown ADR index from ADR YAML front matter.

Example usage:
  python scripts/adr/update-adr-index.py --adr-dir docs/architecture/decisions --index docs/architecture/decisions/index.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    raise SystemExit("ERROR: Missing dependency PyYAML. Install with: python -m pip install pyyaml")


def extract_front_matter(text: str) -> dict[str, Any]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        return {}
    data = yaml.safe_load(match.group(1)) or {}
    return data if isinstance(data, dict) else {}


def adr_sort_key(path: Path, metadata: dict[str, Any]) -> tuple[int, str]:
    adr_id = str(metadata.get("adr_id", ""))
    name = path.name
    for text in (name, adr_id):
        match = re.search(r"(\d{4})", text)
        if match:
            return int(match.group(1)), name
    return 999999, name


def md_link(text: str, target: str) -> str:
    safe = text.replace("|", "\\|") if text else "TBD"
    return f"[{safe}]({target})"


def scalar(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else default
    if isinstance(value, dict):
        return default
    text = str(value)
    return text if text else default


def owner_label(owner: Any) -> str:
    if not isinstance(owner, dict):
        return "TBD"
    name = scalar(owner.get("name"), "")
    role = scalar(owner.get("role"), "")
    if name and role:
        return f"{name} / {role}"
    return name or role or "TBD"


def build_index(adr_dir: Path) -> str:
    rows = []
    files = sorted(
        p for p in adr_dir.rglob("*.md")
        if p.name.lower() not in {"readme.md", "index.md", "_template.md"}
    )
    items = []
    for path in files:
        metadata = extract_front_matter(path.read_text(encoding="utf-8"))
        if not metadata:
            continue
        items.append((path, metadata))

    items.sort(key=lambda item: adr_sort_key(item[0], item[1]))

    for path, metadata in items:
        rel = path.relative_to(adr_dir).as_posix()
        debt = metadata.get("technical_debt_assessment") or {}
        if not isinstance(debt, dict):
            debt = {}
        rows.append(
            "| " + " | ".join([
                md_link(scalar(metadata.get("adr_id"), path.stem), rel),
                scalar(metadata.get("title"), "TBD").replace("|", "\\|"),
                scalar(metadata.get("status"), "TBD"),
                scalar(metadata.get("risk_tier"), "TBD"),
                owner_label(metadata.get("decision_owner")).replace("|", "\\|"),
                scalar(metadata.get("accepted_date"), ""),
                scalar(metadata.get("next_review_date"), ""),
                scalar(debt.get("impact"), "TBD"),
                scalar(debt.get("score"), "TBD"),
                scalar(metadata.get("supersedes"), ""),
                scalar(metadata.get("superseded_by"), ""),
            ]) + " |"
        )

    header = """# ADR Index

This file is generated from ADR YAML front matter. Do not edit table rows manually; update the ADR source files and regenerate the index.

| ADR | Title | Status | Risk tier | Decision owner | Accepted date | Next review | Debt impact | Debt score | Supersedes | Superseded by |
|---|---|---|---|---|---|---|---|---:|---|---|
"""
    if not rows:
        rows.append("| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |")
    return header + "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate ADR index.")
    parser.add_argument("--adr-dir", default="docs/architecture/decisions", help="ADR directory")
    parser.add_argument("--index", default="docs/architecture/decisions/index.md", help="Index file path")
    args = parser.parse_args()

    adr_dir = Path(args.adr_dir)
    index_path = Path(args.index)
    if not adr_dir.exists():
        raise SystemExit(f"ERROR: ADR directory not found: {adr_dir}")

    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(build_index(adr_dir), encoding="utf-8")
    print(f"Updated {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### File: `.github/workflows/adr-validate.yml`

Use this workflow to validate ADRs and fail pull requests when accepted ADRs contain unmanaged technical debt.

```yaml
name: ADR Validation

on:
  pull_request:
    paths:
      - "docs/architecture/decisions/**/*.md"
      - "docs/architecture/decisions/schema/**/*.json"
      - "scripts/adr/**"
      - ".github/workflows/adr-validate.yml"
  push:
    branches:
      - main
    paths:
      - "docs/architecture/decisions/**/*.md"
      - "docs/architecture/decisions/schema/**/*.json"
      - "scripts/adr/**"

permissions:
  contents: read
  pull-requests: read

jobs:
  validate-adrs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install pyyaml jsonschema

      - name: Validate ADRs
        run: |
          python scripts/adr/validate-adr.py \
            --adr-dir docs/architecture/decisions \
            --schema docs/architecture/decisions/schema/adr.schema.json \
            --base-ref origin/${{ github.base_ref || 'main' }} \
            --fail-on-unmanaged-debt
```

### File: `.github/workflows/adr-index.yml`

Use this workflow to ensure the ADR index remains synchronized with ADR metadata.

```yaml
name: ADR Index Check

on:
  pull_request:
    paths:
      - "docs/architecture/decisions/**/*.md"
      - "scripts/adr/update-adr-index.py"
      - ".github/workflows/adr-index.yml"

permissions:
  contents: read

jobs:
  check-index:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install pyyaml

      - name: Regenerate ADR index and fail on drift
        run: |
          python scripts/adr/update-adr-index.py \
            --adr-dir docs/architecture/decisions \
            --index docs/architecture/decisions/index.md
          git diff --exit-code docs/architecture/decisions/index.md
```

### File: `.github/pull_request_template.md` ADR addition

```markdown
## ADR impact

- [ ] This PR does not require an ADR.
- [ ] This PR creates or updates ADR(s).
- [ ] The ADR index has been updated.
- [ ] Required reviewers are identified based on ADR risk tier and control domains.
- [ ] Accepted or rejected ADRs were not materially changed without supersession.
- [ ] Technical debt impact was assessed.
- [ ] New or increased technical debt has an owner, remediation plan, due date or review date, and evidence reference.

## ADR references

- ADR(s): TBD
- Risk tier(s): TBD
- Control domain(s): TBD
- Technical debt impact: TBD
- Debt score: TBD
- Required approval evidence: TBD
```

### File: `docs/architecture/decisions/schema/adr.schema.json`

Use this schema as the baseline validator for ADR YAML front matter. Repositories may add properties, but should not remove the technical debt fields.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Architecture Decision Record Metadata",
  "type": "object",
  "required": [
    "adr_id",
    "title",
    "status",
    "risk_tier",
    "control_domains",
    "created_date",
    "adr_owner",
    "decision_owner",
    "technical_debt_assessment",
    "traceability",
    "supersedes",
    "superseded_by"
  ],
  "properties": {
    "adr_id": { "type": "string", "minLength": 4 },
    "title": { "type": "string", "minLength": 5 },
    "status": {
      "type": "string",
      "enum": [
        "Candidate",
        "Draft",
        "Proposed",
        "In Review",
        "Rework",
        "Accepted",
        "Accepted with Conditions",
        "Rejected",
        "Implemented",
        "Validated",
        "Deferred",
        "Superseded",
        "Deprecated",
        "Retired",
        "Archived"
      ]
    },
    "risk_tier": { "type": "string", "enum": ["Tier 0", "Tier 1", "Tier 2", "Tier 3", "Tier 4"] },
    "control_domains": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" }
    },
    "created_date": { "type": "string" },
    "adr_owner": {
      "type": "object",
      "required": ["name", "role"],
      "properties": {
        "name": { "type": "string" },
        "role": { "type": "string" }
      },
      "additionalProperties": true
    },
    "decision_owner": {
      "type": "object",
      "required": ["name", "role"],
      "properties": {
        "name": { "type": "string" },
        "role": { "type": "string" }
      },
      "additionalProperties": true
    },
    "technical_debt_assessment": {
      "type": "object",
      "required": ["impact", "score", "rationale"],
      "properties": {
        "impact": { "type": "string", "enum": ["None", "New Debt", "Increased Debt", "Reduced Debt", "Mixed Impact", "TBD"] },
        "score": { "type": ["integer", "string"] },
        "rationale": { "type": "string" },
        "existing_debt_references": { "type": "array" },
        "new_or_changed_debt_items": { "type": "array" },
        "debt_owner": { "type": "object" },
        "remediation_plan": { "type": "string" },
        "remediation_due_date": { "type": "string" },
        "review_date": { "type": "string" },
        "related_exceptions_or_risk_acceptances": { "type": "array" }
      },
      "additionalProperties": true
    },
    "traceability": { "type": "object" },
    "supersedes": { "type": "array" },
    "superseded_by": { "type": "array" },
    "legal_hold": { "type": "boolean" }
  },
  "additionalProperties": true
}
```

### Consistency checks for generated automation
Before returning automation files, verify:

- `validate-adr.py` imports only standard library modules plus `pyyaml` and optional `jsonschema`.
- GitHub Actions install `pyyaml` and `jsonschema` before validation.
- ADR schema requires `technical_debt_assessment`.
- ADR index includes `Debt impact` and `Debt score`.
- Accepted ADRs with unmanaged new, increased, or mixed debt fail validation.
- Draft or proposed ADRs with possible debt indicators produce warnings rather than unnecessary blocking failures.

## Expected deliverables
Depending on the user request, produce one or more of:

- A complete ADR Markdown file.
- Repository initialization files.
- An ADR index.
- A pull request description.
- A review findings report.
- A supersession note and migration action list.

Always make the output copy/paste-ready for GitHub Markdown unless the user requests another format.
