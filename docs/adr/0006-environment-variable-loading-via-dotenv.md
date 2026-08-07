# ADR-0006: Environment Variable Loading via Zero-Dependency `.env` File Parser

## Status

Accepted

## Context

Running scripts in diverse environments (local development CLI, cron jobs, CI/CD runners, containerized environments) requires loading secrets such as `GITHUB_TOKEN` and configurations like `GITHUB_OWNER`. Requiring manual `export GITHUB_TOKEN=...` commands or adding external third-party library dependencies (like `python-dotenv`) violates the core design principle of zero external dependencies for `github_helper_agent.py`.

Without automatic `.env` reading, users or automated runners executing `python3 github_helper_agent.py` in directory locations containing `.env` configuration files encounter HTTP 401 unauthenticated API errors.

## Decision

We decided to implement a zero-dependency `.env` file parser (`load_dotenv`) directly in `github_helper_agent.py`:

1. **Automatic Detection**: Automatically look for `.env` in the current working directory or specified path upon script execution.
2. **Zero External Dependencies**: Read `.env` using standard Python `open` and string parsing, ignoring empty lines, comments (`#`), and stripping surrounding quotes (`"` and `'`).
3. **Environment Variable Precedence**: Only populate `os.environ` keys if they are not already set in the host environment, allowing environment variables passed explicitly via OS/shell to take precedence.
4. **Fallback & Graceful Error Handling**: If `.env` is absent or unreadable, log warnings gracefully without crashing execution.

## Consequences

### Positive
- Automatic loading of tokens and configuration parameters when executing locally or via background workers.
- Preserves the zero external library dependency constraint of `github_helper_agent.py`.
- Preserves shell variable override hierarchy (existing OS environment variables take priority over `.env`).

### Negative
- Simple `.env` parser does not support complex multiline variables or shell variable expansion syntax without additional parser logic.
