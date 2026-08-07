# ADR-0007: Containerization via Chainguard Minimal Python Base Image

## Status

Accepted

## Context

To run `gh-helper-agent` reliably across diverse environments (Kubernetes clusters, cloud cron runners, serverless container platforms, local Docker runtimes) without OS-level dependency pollution or vulnerability risks, a secure containerization strategy is needed.

Standard container images (e.g. `python:3.11-slim` or `ubuntu`) often contain unused utilities, shell environments, and package managers (apt/dpkg) that expand the attack surface and trigger vulnerability scanner flags (CVEs).

Additionally, `gh-helper-agent` relies purely on Python standard library modules (`urllib`, `os`, `json`, `argparse`), meaning no heavy third-party C dependencies or package compilation steps are required.

## Decision

We decided to containerize `gh-helper-agent` into a single, minimal, and secure container image utilizing Chainguard's minimal Python base images (`cgr.dev/chainguard/python`):

1. **Chainguard Base Image**: Sourced `cgr.dev/chainguard/python:latest` (and `latest-dev` for multi-stage build context validation). Chainguard images are updated daily, generated with zero known vulnerabilities, and contain no unnecessary binaries, shells, or package managers.
2. **Multi-Stage Build Pattern**: Use a multi-stage Dockerfile architecture separating the workspace preparation (`builder`) from the final runtime container (`runtime`).
3. **Non-Root Execution**: Enforce non-privileged user execution (`USER nonroot`) within the container workspace (`/app`).
4. **Environment & Entrypoint Standardization**: Set default `PYTHONUNBUFFERED=1` and define `ENTRYPOINT ["python", "/app/github_helper_agent.py"]` with configurable flags via `CMD ["--all"]`.

## Consequences

### Positive
- **Minimal Attack Surface**: Zero unnecessary tools or shells included in the container runtime layer.
- **Zero Known Vulnerabilities**: Chainguard daily rebuilds ensure CVE-free base images.
- **Single-Artifact Deployment**: All runtime functionality encapsulated in a single lightweight image (~30MB).
- **Environment Isolation**: Eliminates local environment mismatch issues when executing automated scans and fork synchronizations.

### Negative
- Distroless execution environment lacks standard debugging tools (`bash`, `curl`, `sh`), requiring multi-stage or sidecar patterns if interactive shell access inside the container is needed for debugging.
