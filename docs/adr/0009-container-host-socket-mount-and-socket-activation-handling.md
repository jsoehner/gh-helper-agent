# ADR-0009: Container Host Socket Mount and Socket Activation Handling

## Status

Accepted

## Context

When containerizing `gh-helper-agent` or executing containerized maintenance tools alongside Docker/Moby engine instances, container workflows may need to interact with the underlying Docker daemon (for instance, performing containerized build checks, running security scanners such as Trivy against local images, or inspecting system container states).

On Linux hosts running Moby/Docker Engine (e.g. Fedora, RHEL, Ubuntu), the Docker API server uses systemd socket activation (`docker.socket`), creating the Unix domain socket at `/run/docker.sock` with a compatibility symlink at `/var/run/docker.sock`.

Without explicit socket volume mounting (`-v /run/docker.sock:/var/run/docker.sock`), containerized applications cannot connect to the host Docker daemon, resulting in `Cannot connect to the Docker daemon at unix:///var/run/docker.sock` errors. Additionally, containers mounted without proper socket permissions or group alignment (`docker` group GID mismatch) can experience permission denied errors.

## Decision

We decided to:
1. Standardize and document host Docker socket mounting (`-v /run/docker.sock:/var/run/docker.sock`) in `README.md` for containerized workflows requiring host engine interaction.
2. Maintain clean separation between standard REST API container runs (which only require environment variables like `GITHUB_TOKEN`) and host-engine container runs requiring host socket volume mounts.
3. Document socket activation gotchas and permissions rules in `README.md` and `MEMORY.md`.

## Consequences

### Positive
- **Host Engine Interoperability**: Enables containerized executions of `gh-helper-agent` to build, scan, or manage local container images.
- **Clear Runtime Instructions**: Developers and CI/CD systems have unambiguous commands for both API-only and socket-attached container modes.

### Negative
- **Security Considerations**: Mounting `/run/docker.sock` into a container grants elevated privileges over the host system. Socket mounting should be restricted to trusted images and executed only when local daemon access is explicitly required.
