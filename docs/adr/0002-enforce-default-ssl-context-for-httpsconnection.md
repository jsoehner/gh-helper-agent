# ADR 0002: Enforce Default SSL Context for HTTPSConnection Certificate Verification

* **Status:** Accepted
* **Deciders:** GitHub Helper Agent Engineering, Security Architecture
* **Date:** 2026-09-30

---

## 1. Context & Problem Statement

Static Application Security Testing (SAST) alert #5 flagged the usage of `http.client.HTTPSConnection` in `github_helper_agent.py` under rule `python.lang.security.audit.httpsconnection-detected.httpsconnection-detected` (CWE-295: Improper Certificate Validation).
To ensure robust Transport Layer Security (TLS) validation against man-in-the-middle (MITM) attacks and comply with secure API communication standards:
1. `http.client.HTTPSConnection` must explicitly instantiate and utilize a verified SSL context via `ssl.create_default_context()`.
2. Python certificate validation rules and standard root CA trust stores must be enforced unconditionally.

---

## 2. Decision Drivers

1. **Strict Certificate Verification (CWE-295)**: Guarantee that outbound calls to `api.github.com` strictly validate TLS server certificates and hostnames.
2. **Standard Library Purity**: Preserve the zero-external-pip-dependency architectural requirement by leveraging `ssl` and `http.client` directly from Python's standard library.
3. **SAST Policy Compliance**: Resolve and prevent security findings in Semgrep and GitHub Code Scanning without weakening security controls.

---

## 3. Considered Options

* **Option 1**: Suppress alert without code modification.
  - *Drawbacks*: Leaves configuration implicit and fails to demonstrate defense-in-depth posture.
* **Option 2 (Chosen)**: Explicitly initialize `context = ssl.create_default_context()` and pass it to `http.client.HTTPSConnection("api.github.com", timeout=30, context=context)`.
  - *Benefits*: Explicit TLS verification with default CA certs, full CWE-295 compliance, zero external dependencies.

---

## 4. Decision Outcome

Adopted Option 2:
1. Added `import ssl` to `github_helper_agent.py`.
2. Configured `_api_call` to create an explicit default SSL context (`ssl.create_default_context()`) for every HTTPS connection.
3. Updated unit tests in `test_github_helper_agent.py` to assert that the SSL context is properly configured and supplied.

---

## 5. Consequences

* **Positive**: Outbound HTTPS connections to GitHub API have explicit TLS certificate and hostname validation; SAST alert #5 resolved.
* **Negative**: None.
