# Contributing to gh-helper-agent

Thank you for your interest in contributing to gh-helper-agent! This project is designed to automate the maintenance of GitHub repositories, and your contributions help make it more robust and efficient.

## Code of Conduct
Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs
1. **Check existing issues** - Search the issue tracker to see if the bug has already been reported.
2. **Create a new issue** - If not found, create a new issue using the bug report template.
3. **Provide details** - Include:
   - Version of gh-helper-agent
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant logs or screenshots

### Suggesting Features
1. **Check existing requests** - Search issues for similar feature requests.
2. **Create a feature request** - Use the feature request template.
3. **Describe the use case** - Explain why this feature would be valuable for repository maintenance.

### Contributing Code
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Run tests**: `python3 test_github_helper_agent.py`
5. **Commit your changes** with a descriptive message following Conventional Commits.
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**

## Development Setup

### Prerequisites
- Python 3.12+
- Docker (for running the agent in container mode)
- A GitHub Personal Access Token with appropriate permissions (`repo`, `delete_repo`, `admin:org` if applicable).

### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jsoehner/gh-helper-agent.git
   cd gh-helper-agent
   ```
2. **Environment Variables**:
   Create a `.env` file (do not commit it!) with your credentials:
   ```bash
   GITHUB_TOKEN="your_token_here"
   GITHUB_OWNER="jsoehner"
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Tests**:
   ```bash
   python3 test_github_helper_agent.py
   ```

## Commit Message Guidelines
We use **Conventional Commits**. Please use the following prefixes:
- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `perf:` A code change that improves performance
- `test:` Adding missing tests or correcting existing tests
- `chore:` Changes to the build process or auxiliary tools and libraries

Example: `feat(audit): add support for scanning stale repositories`

## Pull Request Process
1. Ensure all tests pass.
2. Update documentation (if applicable).
3. Add tests for new functionality.
4. Fill out the PR template completely.
5. Request review from maintainers.

## Questions?
Feel free to open an issue for questions or join discussions in existing issues.
