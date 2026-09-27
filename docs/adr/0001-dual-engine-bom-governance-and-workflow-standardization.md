# ADR 0001: Dual-Engine BOM Governance, Action Pinning, and Workflow Standardization

* **Status:** Accepted
* **Deciders:** GitHub Helper Agent Engineering, Security Architecture
* **Date:** 2026-09-27

---

## 1. Context & Problem Statement

To satisfy modern supply chain and cryptographic risk posture requirements, the repository requires automated dual-engine Bill of Materials generation (both Software BOM and Cryptographic BOM), automated Post-Quantum Cryptography (PQC) readiness auditing, commit validation, and removal of invalid workflows:
1. Software dependencies and cryptographic assets must be automatically inventoried and validated on every build and push to main.
2. Actions in workflows must be pinned to immutable commit SHAs with Node 24 support.
3. Automated commit message linting is required to maintain Conventional Commits, with appropriate length limits for squash merges.
4. Non-functional changelog workflows must be removed.

---

## 2. Decision Drivers

1. **Dual-Engine BOM Integrity**: Both CycloneDX/SPDX SBOMs and CycloneDX v1.6+ CBOMs with cryptographic algorithm and key-length tagging must be maintained.
2. **PQC Readiness Assessment**: Automated scoring of quantum-safe vs. quantum-vulnerable primitives.
3. **Immutability & Node 24 Compatibility**: Workflows must run on Node 24 runners with SHA-pinned actions.
4. **Developer Experience & Validation**: Automated pre-commit and CI verification test harness.

---

## 3. Considered Options

* **Option 1**: Single SBOM-only approach without cryptographic tracking.
* **Option 2 (Chosen)**: Standardized dual-engine BOM suite (`sbom.yml`, `scripts/generate_boms.sh`, `scripts/scan_crypto_ast.py`, `scripts/analyze_cbom.py`, `scripts/test_boms.sh`) with Conventional Commit enforcement and relaxed line length rules.

---

## 4. Decision Outcome

Adopted Option 2:
1. Replaced legacy SBOM workflow with Node 24 SHA-pinned `sbom.yml`.
2. Standardized cryptographic AST scanner (`scan_crypto_ast.py`) and CBOM analyzer (`analyze_cbom.py`).
3. Installed `commit-lint.yml` (wagoid v6.2.1) and `commitlint.config.mjs`.
4. Removed invalid changelog workflow.
5. Added `--actor` argument support to `scripts/adr_security_gatekeeper.py`.

---

## 5. Consequences

* **Positive**: Full visibility into OSS and cryptographic dependencies; automated PQC migration progress metrics; pristine CI pipeline execution.
* **Negative**: Additional CI step overhead for BOM generation.
