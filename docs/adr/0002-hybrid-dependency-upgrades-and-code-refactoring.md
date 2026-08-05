# ADR-0002: Hybrid Dependency Upgrades & Automated Code Refactoring Strategy

## Status

Accepted

## Context

While `gh-helper-agent` automates remote Dependabot PR merging, several edge cases require hybrid execution:
1. **Subdirectory & Monorepo Upgrades**: Dependency updates occurring in nested directory modules (e.g. `/httphandler` in Go projects) may require local verification or package manager invocations when remote auto-merges fail CI/protection rules.
2. **Issue-Driven Code Refactoring**: Code quality improvements and technical debt cleanup identified in issues require explicit refactoring hooks and local workspace AST/formatting passes.

## Decision

We decided to:
1. **Implement Dual-Phase Dependency Upgrade Hooks**: Combine remote REST API auto-merging with local fallback handlers (`perform_local_dependency_upgrade`) for package managers (`go get`, `npm update`).
2. **Add Issue-Triggered Code Refactoring Logic**: Introduce structured handlers (`perform_code_refactoring`) inside `GitHubHelperAgent` to detect refactor/tech-debt issue tags and trigger local code transformations.
3. **Document Gotchas in README**: Explicitly record edge cases and operational constraints around CI status requirements, package boundaries, and local workspace safety.

## Consequences

### Positive
- Allows seamless handling of complex monorepo dependency structures.
- Establishes a clean architectural path for automated code refactoring.
- Prevents silent failures when remote GitHub REST API merges cannot bypass branch protections.

### Negative
- Local execution hooks require local CLI tool availability (e.g., `go`, `npm`, `python`).
