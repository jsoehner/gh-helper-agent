# ADR-0001: Automated SBOM & CBOM Supply Chain Governance and Post-Quantum Cryptography Readiness

- **Status**: Accepted
- **Date**: 2026-10-11
- **Security Classification**: Internal
- **Decision Makers**: Platform Security & DevSecOps Lead
- **Consulted / Informed**: Architecture Review Board, Security Engineering, Core Maintainers
- **Supersedes**: None

---

## 1. Context and Problem Statement

`gh-helper-agent` provides automated repository maintenance, Dependabot advisory triage and remediation strategy classification, fork synchronization, and automated pull request merging for GitHub repositories. Operating with elevated GitHub Personal Access Token (PAT) privileges and automated write access to pull requests and issue tracking, the agent's software supply chain and cryptographic integrity are critical to prevent malicious dependency tampering, unauthorized pipeline manipulation, or insecure cryptographic algorithms.

With the enforcement of Executive Order 14028, NIST SP 800-218 (Secure Software Development Framework - SSDF), NIST SP 800-161 (Cybersecurity Supply Chain Risk Management - C-SCRM), NTIA Minimum Elements for Software Bill of Materials (SBOM), and federal Post-Quantum Cryptography (PQC) transition mandates (NIST FIPS 203/204/205, CNSA 2.0), software systems must maintain transparent, machine-readable inventories of their dependencies and cryptographic primitives.

Prior to this decision, `gh-helper-agent` leveraged Chainguard minimal Python images, Trivy vulnerability scans, Semgrep SAST, and Gitleaks secret scanning, but required:
1. Standardized dual-format Software Bill of Materials (SBOM) generation compliant with NTIA minimum elements (CycloneDX and SPDX).
2. Automated Cryptographic Bill of Materials (CBOM) generation tracking cryptographic algorithms, key lengths, and protocols.
3. Post-Quantum Cryptography (PQC) readiness evaluation to identify classical, quantum-vulnerable algorithms versus quantum-safe primitives.
4. Semantic Abstract Syntax Tree (AST) scanning to correlate code call sites with inventory manifests.
5. In-pipeline verification harnesses ensuring corrupt or empty BOM artifacts break CI prior to deployment or distribution.

### 1.1 Business & Compliance Drivers
- **Regulatory / Compliance**: Executive Order 14028, NIST SP 800-218 (SSDF), NIST SP 800-161 (C-SCRM), NTIA Minimum Elements for SBOMs, CNSA 2.0 PQC migration milestones.
- **Supply Chain Assurance**: Guaranteeing that the automation tooling managing repository pull requests and security advisories is itself verified and auditable.

### 1.2 Threat & Vulnerability Context
- **Threat Vector (STRIDE)**: Tampering (malicious package injection or transit tampering), Information Disclosure, Elevation of Privilege.
- **Vulnerabilities Mitigated**: CWE-1395 (Dependency on Vulnerable Third-Party Component), CWE-327 (Use of a Broken or Risky Cryptographic Algorithm), CWE-1104 (Use of Unmaintained Third-Party Components).
- **CVSS / Risk Rating**: Medium (6.5)
- **Scope**: Repository dependencies, workflow actions, build scripts, and container artifacts.

---

## 2. Decision Drivers & Constraints

- Automatically generate dual-standard SBOMs: CycloneDX 1.5/1.6 JSON and SPDX 2.3 JSON using Anchore/Syft.
- Generate CycloneDX 1.6 Cryptographic Bill of Materials (CBOM) via `cbomkit-action` with fallback offline catalog reconciliation.
- Deploy dual-engine cryptographic discovery using semantic AST scanning (`scan_crypto_ast.py`) across source files.
- Provide automated CI test verification (`test_boms.sh`) verifying JSON validity, schema compliance, and asset presence.
- Evaluate Post-Quantum Cryptography (PQC) readiness and publish automated GitHub Actions Step Summaries and documentation (`analyze_cbom.py`).
- Maintain local CLI parity so developers and operators can generate and verify BOMs offline without requiring cloud CI.
- Adhere to GitHub Actions hardening standards: Node 24 runtime, immutable commit SHA pinning, and least-privilege permissions.

---

## 3. Considered Options

| Option | Approach Summary | Security Benefits | Trade-offs & Costs | Residual Risk Level |
| :--- | :--- | :--- | :--- | :--- |
| **Option A (Chosen)** | Automated dual-engine SBOM (CycloneDX + SPDX via Syft) and CBOM (cbomkit + semantic AST scanning) pipeline with PQC assessment and verification test harness. | Full NTIA compliance, cryptographic asset transparency, automated PQC readiness grading, zero vendor lock-in, local CLI parity. | Requires initial tooling setup (Syft, cbomkit, Python AST analyzer) and artifact storage in CI. | Low |
| **Option B** | Single SPDX-only SBOM generated at release time without CBOM or AST crypto scanning. | Minimal CI overhead and simple single-file generation. | Leaves zero visibility into cryptographic primitives or quantum vulnerability; lacks CycloneDX CBOM interoperability. | High |
| **Option C** | Proprietary commercial SaaS platform for supply chain governance. | Centralized enterprise dashboards managed externally. | High licensing cost, vendor lock-in, lack of offline execution for local pre-commit checks or air-gapped environments. | Medium |

---

## 4. Decision Outcome

**Chosen Option**: **Option A** — Deploy automated dual-format SBOM & CBOM generation, AST cryptographic scanning, verification testing, and PQC migration analysis.

### 4.1 Rationale
Adopting Anchore/Syft provides industry-standard dual-format SBOM generation covering CycloneDX and SPDX. Integrating `cbomkit` alongside semantic AST scanning provides an automated cryptographic inventory capable of tracking quantum-safe readiness (e.g., ML-KEM, ML-DSA) versus classical algorithms (e.g., RSA, ECC). Incorporating a deterministic verification harness (`test_boms.sh`) directly into the CI pipeline guarantees that any corrupt or missing BOM artifact breaks the build, preventing unverified releases.

### 4.2 Pipeline Architecture & Data Flow

```
[Git Commit / PR / Push]
           │
           ▼
[GitHub Actions: sbom-cbom.yml]
           │
           ├──► [1. Syft SBOM Engine] ──────────► oss/sbom.cyclonedx.json & oss/sbom.spdx.json
           │
           ├──► [2. cbomkit Action Engine] ────► oss/cbom.json
           │
           ├──► [3. Semantic AST Scanner] ─────► oss/crypto-callsites.json (Reconciliation)
           │
           ├──► [4. Verification Harness] ─────► test_boms.sh (Schema & Asset Checks)
           │
           ├──► [5. PQC Readiness Analyzer] ───► oss/crypto-analysis.json & GitHub Step Summary
           │
           ├──► [6. Audit Publishing] ─────────► docs/security/CRYPTOGRAPHIC_AUDIT.md
           │
           └──► [7. Artifact Retention] ──────► Uploaded as bom-artifacts (90 days)
```

### 4.3 Component Specifications
1. **`.github/workflows/sbom-cbom.yml`**: GitHub Actions workflow executing checkout (Node 24 `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`), Syft, cbomkit, AST scanning, verification harness, and PQC step summary.
2. **`scripts/generate_boms.sh`**: Local execution script generating CycloneDX and SPDX SBOMs, executing cbomkit, and triggering analysis.
3. **`scripts/scan_crypto_ast.py`**: Semantic AST scanner discovering cryptographic library invocations and reconciling call sites with the CBOM.
4. **`scripts/analyze_cbom.py`**: Cryptographic analyzer assessing classical vs. post-quantum readiness, algorithm distributions, and generating markdown reports.
5. **`scripts/test_boms.sh`**: Automated verification test harness validating JSON syntax, CycloneDX schema, and cryptographic asset counts.
6. **`scripts/attach_oci_bom.sh` & `scripts/fetch_oci_cbom.py`**: OCI registry integration for attaching and retrieving BOM layers from container artifacts.

---

## 5. Security, Risk & Compliance Impact

### 5.1 CIA Triad Evaluation
- **Confidentiality**: BOM files document public package metadata and cryptographic algorithms; secrets, credentials, and API keys are strictly excluded and governed by Gitleaks.
- **Integrity**: Standardized JSON artifacts provide verifiable cryptographic digests (SHA-256) of every dependency and tool, preventing unauthorized tampering.
- **Availability**: BOM generation is automated in CI and runs in under two minutes, with local tooling providing offline execution without external SaaS dependency.

### 5.2 Post-Quantum Cryptography (PQC) Transition
The CBOM analyzer flags classical asymmetric cryptography (RSA, DSA, ECDSA, DH, ECDH) as quantum-vulnerable, providing continuous visibility as upstream dependencies and tooling transition to post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA).

---

## 6. Consequences

### Positive Consequences
- **Audit Readiness**: Immediate compliance with Executive Order 14028, NIST SSDF, and federal SBOM requirements.
- **Dual Format Interoperability**: Support for both CycloneDX and SPDX ensures broad compatibility across scanning tools and enterprise consumers.
- **Cryptographic Transparency**: Continuous inventory of cryptographic algorithms and post-quantum migration tracking.
- **Automated Quality Gate**: The verification test harness prevents defective or empty BOMs from passing CI.
- **Local Developer Parity**: Developers can run BOM generation and verification locally using identical scripts.

### Negative Consequences & Trade-offs
- **CI Build Duration**: Adds approximately 1–2 minutes to pipeline runs.
- **Storage Overhead**: Generates artifact files in the `oss/` directory during workflow runs (managed via 90-day retention and gitignored locally).

### New Constraints
- The `oss/` directory must remain ignored in version control (`.gitignore`) to avoid committing ephemeral scan outputs.
- Future dependency additions or cryptographic updates must pass `scripts/test_boms.sh` in pull requests.

### Follow-on Activities
- Maintain automated GitHub Actions runs bundling verified SBOMs alongside container image publishes.
- Periodically update Syft and cbomkit action versions pinned to immutable commit hashes.
