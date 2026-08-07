# Multi-stage Dockerfile for gh-helper-agent
# Minimal, secure, zero-dependency container powered by Chainguard Python base images

FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app

# Copy repository source files
COPY github_helper_agent.py .
COPY README.md .

# Final minimal & secure runtime image (distroless nonroot)
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

# Copy built app from builder stage
COPY --from=builder --chown=nonroot:nonroot /app /app

# Set nonroot execution context & environment flags
USER nonroot
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "/app/github_helper_agent.py"]
CMD ["--all"]
