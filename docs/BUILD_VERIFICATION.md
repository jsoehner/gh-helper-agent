# Build & Functional Verification Report

- **Verification Date:** `2026-11-20`
- **Verified By:** **Jeffs' Automated build and deploy agent**
- **Repository:** `jsoehner/gh-helper-agent` (`main`)
- **Status:** `VERIFIED`

---

## 1. Trusted OSS Split-Horizon Registry Configuration

Configured via `setup_trusted_oss_repo.py` in `virtual` mode with split-horizon LAN/WAN routing and mTLS authentication for GitHub Actions:

| Scope | Setting | Value |
| :--- | :--- | :--- |
| Local LAN (`.env`, gitignored) | `TRUSTED_OSS_CACHE_URL` | `http://oss.jsigroup.local:8080` |
| GitHub Actions Variable | `TRUSTED_OSS_CACHE_URL` | `https://jsigroup-oss.duckdns.org` |
| GitHub Actions Variable | `TRUSTED_OSS_MODE` | `virtual` |
| GitHub Actions Variable | `TRUSTED_OSS_GPG_EMAIL` | `oss-signing@the-techy.com` |
| GitHub Actions Secrets | `OSS_MTLS_CLIENT_CERT`, `OSS_MTLS_CLIENT_KEY` | Configured from local mTLS PKI |

Local git exclude hygiene (`.git/info/exclude`) enforces exclusion of `.env`, `uv.toml`, `.mvn/settings.xml`, `.mvn/maven.config`, and `.npmrc`.

---

## 2. Build & Runtime Stack

- **Runtime:** Zero-dependency Python 3 standard-library CLI (`github_helper_agent.py`)
- **Container:** Multi-stage `Dockerfile` using `cgr.dev/chainguard/python:latest-dev` (builder + build-phase `unittest`) and `cgr.dev/chainguard/python:latest` (distroless `nonroot` runtime)

### Commands Executed

```bash
# Syntax / bytecode check
python3 -m py_compile github_helper_agent.py test_github_helper_agent.py

# Native unittest discovery
python3 -m unittest discover -s . -p "test_*.py" -v

# Pytest execution via Trusted OSS Harbor virtual PyPI index
uv run --index-url http://oss.jsigroup.local:8080/pypi/virtual/simple --with pytest pytest -v

# Host CLI smoke test
python3 github_helper_agent.py --help

# Multi-stage Chainguard Docker build & container CLI smoke test
docker build -t gh-helper-agent-verify:local .
docker run --rm gh-helper-agent-verify:local --help
```

---

## 3. Functional Verification Results

| Check | Result | Details |
| :--- | :--- | :--- |
| Fork Guardrail (`check_fork_guardrail.py`) | **PASS** | `ALLOWED_STANDALONE` (not a fork) |
| Python Bytecode (`py_compile`) | **PASS** | `github_helper_agent.py`, `test_github_helper_agent.py` compiled cleanly |
| Native Unit Tests (`unittest discover`) | **PASS** | **34/34 tests passed** in `0.019s` (17 test cases in `test_github_helper_agent.py`, also re-exported via `tests/test_agent.py`) |
| Trusted OSS `uv` + `pytest` Suite | **PASS** | **34/34 tests passed** in `0.12s` (`pytest-9.2.0` resolved from `http://oss.jsigroup.local:8080/pypi/virtual/simple`) |
| Host CLI Smoke Test (`--help`) | **PASS** | Exit code `0`; verified all CLI flags (`--owner`, `--repo`, `--all`, `--scan-and-fix-all`, `--check-alerts`, `--severity`, `--ecosystem`, `--sync-forks`, `--check-stale`, `--dry-run`) |
| Docker Multi-Stage Build (`Dockerfile`) | **PASS** | Builder stage ran `python -m unittest discover -s . -p "test_*.py"` and produced minimal `nonroot` Chainguard runtime image |
| Container CLI Smoke Test (`docker run --rm ... --help`) | **PASS** | Exit code `0`; printed full CLI usage from distroless `nonroot` container |
| Web UI / HTTP API Probes | **N/A** | Pure CLI / container agent (no HTTP server or Web UI) |
