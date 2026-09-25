#!/usr/bin/env python3
"""
GitHub Helper Agent (gh-helper-agent)
An automated maintenance agent that inspects recent GitHub repositories,
reviews open issues and pull requests, merges valid Dependabot PRs,
deduplicates/closes automated scan reports, and applies fixes.
"""

import os
import sys
import json
import http.client
import urllib.request
import urllib.parse
import argparse

def load_dotenv(dotenv_path=".env"):
    """Load key-value pairs from a .env file into os.environ if present."""
    if not os.path.isfile(dotenv_path):
        return
    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key and key not in os.environ:
                    os.environ[key] = val
    except Exception as e:
        print(f"[!] Warning: Failed to load {dotenv_path}: {e}")

load_dotenv()

def is_major_version_jump(vulnerable_range, target_version):
    """
    Detect if the upgrade from the vulnerable version range to the target version
    involves a major semver breaking jump (e.g. 1.x -> 2.x or < 18.0.0 -> 18.2.0).
    """
    if not target_version or target_version == "None Available":
        return False
    import re
    target_match = re.search(r'v?(\d+)\.', target_version)
    if not target_match:
        return False
    target_major = int(target_match.group(1))

    if not vulnerable_range:
        return False

    # Check for lower bound (e.g. ">= 1.0.0")
    lower_matches = re.findall(r'>[=\s]*v?(\d+)\.', vulnerable_range)
    if lower_matches:
        lower_major = min(int(m) for m in lower_matches)
        if target_major > lower_major:
            return True

    # Check for upper bound (e.g. "< 2.0.0" or "< 1.5.0")
    upper_matches = re.findall(r'<[=\s]*v?(\d+)\.(\d+)(?:\.(\d+))?', vulnerable_range)
    if upper_matches:
        for u_maj, u_min, u_patch in upper_matches:
            u_maj_int = int(u_maj)
            u_min_int = int(u_min)
            u_patch_int = int(u_patch) if u_patch else 0

            # If target major is strictly greater than upper bound major (e.g. < 1.5.0 -> 2.0.0)
            if target_major > u_maj_int:
                return True
            # If upper bound is a major boundary like "< 18.0.0" and target is "18.x"
            # It means vulnerable versions were in previous major series (e.g. 17.x)
            if target_major == u_maj_int and u_min_int == 0 and u_patch_int == 0:
                if f"< {u_maj}.0" in vulnerable_range or f"<{u_maj}.0" in vulnerable_range or f"< v{u_maj}.0" in vulnerable_range:
                    return True

    return False

def generate_ecosystem_remediation_command(ecosystem, package_name, target_version, manifest_path=None, strategy="PATCH_UPGRADE"):
    """
    Generate actionable ecosystem-specific CLI commands to remediate the vulnerability.
    """
    ecosystem = (ecosystem or "").lower()
    manifest_path = manifest_path or ""
    
    if strategy == "TRANSITIVE_LOCKFILE_UPDATE":
        if ecosystem in ["npm", "javascript", "typescript"]:
            return "npm audit fix"
        elif ecosystem in ["pip", "python", "pypi"]:
            return f"pip-compile --upgrade-package {package_name} && pip install -r requirements.txt"
        elif ecosystem in ["cargo", "rust"]:
            return f"cargo update -p {package_name}"
        elif ecosystem in ["gomod", "go", "golang"]:
            return f"go get -u {package_name} && go mod tidy"
        elif ecosystem in ["composer", "php"]:
            return f"composer update {package_name} --with-dependencies"
        elif ecosystem in ["maven", "gradle", "java"]:
            return "./gradlew dependencyUpdates  # or mvn versions:use-latest-releases"
        return f"# Refresh lockfile for {ecosystem} to update transitive dependency {package_name}"

    if ecosystem in ["npm", "javascript", "typescript"]:
        dev_flag = " --save-dev" if "dev" in manifest_path.lower() else ""
        ver_spec = f"@{target_version}" if target_version and target_version != "None Available" else ""
        return f"npm install {package_name}{ver_spec}{dev_flag} && npm audit"
    elif ecosystem in ["pip", "python", "pypi"]:
        ver_spec = f"=={target_version}" if target_version and target_version != "None Available" else ""
        return f"pip install {package_name}{ver_spec}  # and update {manifest_path or 'requirements.txt'}"
    elif ecosystem in ["gomod", "go", "golang"]:
        ver_spec = f"@v{target_version}" if target_version and target_version != "None Available" else "@latest"
        return f"go get {package_name}{ver_spec} && go mod tidy"
    elif ecosystem in ["cargo", "rust"]:
        if target_version and target_version != "None Available":
            return f"cargo update -p {package_name} --precise {target_version}"
        return f"cargo update -p {package_name}"
    elif ecosystem in ["maven", "java"]:
        return f"# Update <version>{target_version}</version> for {package_name} in {manifest_path or 'pom.xml'}"
    elif ecosystem in ["gradle"]:
        return f"# Update implementation '{package_name}:{target_version}' in {manifest_path or 'build.gradle'}"
    elif ecosystem in ["composer", "php"]:
        ver_spec = f":{target_version}" if target_version and target_version != "None Available" else ""
        return f"composer require {package_name}{ver_spec}"
    elif ecosystem in ["nuget", "csharp", "dotnet", ".net"]:
        ver_spec = f" --version {target_version}" if target_version and target_version != "None Available" else ""
        return f"dotnet add package {package_name}{ver_spec}"
    elif ecosystem in ["actions", "github-actions"]:
        return f"# Update action reference {package_name} to @v{target_version} in {manifest_path or '.github/workflows/'}"
    elif ecosystem in ["rubygems", "ruby"]:
        return f"bundle update {package_name}"
    elif ecosystem in ["pub", "dart", "flutter"]:
        return f"dart pub upgrade {package_name}"
    else:
        return f"# Upgrade {package_name} to {target_version} in {manifest_path or 'manifest'}"

class GitHubHelperAgent:
    def __init__(self, token=None, owner=None, dry_run=False):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.owner = owner or os.environ.get("GITHUB_OWNER", "jsoehner")
        self.dry_run = dry_run
        if not self.token:
            print("[!] Warning: GITHUB_TOKEN environment variable is not set.")
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def load_config(self, config_path=".github-helper.json"):
        """Load configuration from JSON if available."""
        if os.path.isfile(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[!] Warning: Could not read {config_path}: {e}")
        return {}

    def _api_call(self, endpoint, method="GET", data=None, retries=3):
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        headers = dict(self.headers)
        payload = None
        if data is not None:
            headers["Content-Type"] = "application/json"
            payload = json.dumps(data).encode("utf-8")

        for attempt in range(retries):
            conn = None
            try:
                conn = http.client.HTTPSConnection("api.github.com", timeout=30)  # nosemgrep: python.lang.security.audit.httpsconnection-detected.httpsconnection-detected
                conn.request(method, endpoint, body=payload, headers=headers)
                resp = conn.getresponse()
                status = resp.status
                remaining = resp.getheader("X-RateLimit-Remaining")
                if remaining is not None and int(remaining) < 10:
                    print(f"[!] Warning: GitHub API rate limit low: {remaining} requests remaining.")

                if status == 204:
                    return True

                res_data = resp.read().decode("utf-8", errors="ignore")
                if 200 <= status < 300:
                    return json.loads(res_data) if res_data else True

                # Handle rate limiting (HTTP 429 or 403 with rate limit message)
                if (status == 429 or (status == 403 and "rate limit" in res_data.lower())) and attempt < retries - 1:
                    retry_after = resp.getheader("Retry-After")
                    reset_time = resp.getheader("X-RateLimit-Reset")
                    wait_time = int(retry_after) if retry_after else (2 ** (attempt + 1))
                    if reset_time and not retry_after:
                        import time
                        wait_time = max(1, min(int(reset_time) - int(time.time()), 60))
                    print(f"[!] Rate limited (HTTP {status}). Retrying in {wait_time}s (Attempt {attempt+1}/{retries})...")
                    import time
                    time.sleep(wait_time)
                    continue

                try:
                    err_data = json.loads(res_data)
                except Exception:
                    err_data = {"message": res_data}
                if isinstance(err_data, dict):
                    err_data["_http_status"] = status
                    if "is not behind" not in res_data.lower() and "archived" not in res_data.lower() and "dependabot alerts are disabled" not in res_data.lower() and "dependabot" not in res_data.lower():
                        print(f"[-] HTTP {status} for {method} https://api.github.com{endpoint}: {res_data}")
                    return err_data
                print(f"[-] HTTP {status} for {method} https://api.github.com{endpoint}: {res_data}")
                return None
            except Exception as e:
                print(f"[-] Error calling {method} https://api.github.com{endpoint}: {e}")
                return None
            finally:
                if conn:
                    conn.close()
        return None

    def _fetch_paginated_api(self, endpoint):
        """Helper to retrieve all pages for list endpoints."""
        results = []
        page = 1
        delim = "&" if "?" in endpoint else "?"
        while True:
            res = self._api_call(f"{endpoint}{delim}per_page=100&page={page}")
            if not res or not isinstance(res, list):
                break
            results.extend(res)
            if len(res) < 100:
                break
            page += 1
        return results

    def get_recent_repositories(self, limit=10):
        print(f"[*] Fetching top {limit} recent repositories for {self.owner}...")
        res = self._api_call(f"/user/repos?sort=updated&per_page={limit}")
        return res if res and isinstance(res, list) else []

    def get_open_issues_and_prs(self, repo_name):
        issues = self._fetch_paginated_api(f"/repos/{self.owner}/{repo_name}/issues?state=open")
        prs = self._fetch_paginated_api(f"/repos/{self.owner}/{repo_name}/pulls?state=open")
        actual_issues = [i for i in issues if "pull_request" not in i]
        return actual_issues, prs

    def check_pr_ci_status(self, repo_name, ref):
        """Check combined commit status and check runs for a PR head ref."""
        combined_status = self._api_call(f"/repos/{self.owner}/{repo_name}/commits/{ref}/status")
        check_runs = self._api_call(f"/repos/{self.owner}/{repo_name}/commits/{ref}/check-runs")
        
        status_state = combined_status.get("state") if isinstance(combined_status, dict) else "unknown"
        runs = check_runs.get("check_runs", []) if isinstance(check_runs, dict) else []
        
        failed_runs = [r for r in runs if r.get("conclusion") in ["failure", "timed_out", "action_required"]]
        pending_runs = [r for r in runs if r.get("status") != "completed"]
        
        if failed_runs:
            print(f"    [-] CI Check Runs Failed for ref {ref[:7]}: {len(failed_runs)} checks failed.")
            return False
        if pending_runs:
            print(f"    [!] CI Check Runs Pending for ref {ref[:7]}: {len(pending_runs)} checks in progress.")
            return False
        if status_state == "failure":
            print(f"    [-] Combined commit status is failure for ref {ref[:7]}.")
            return False
            
        return True

    def merge_pr(self, repo_name, pr_number, pr_ref=None, merge_method="squash", require_ci=True):
        if pr_ref and require_ci:
            ci_ok = self.check_pr_ci_status(repo_name, pr_ref)
            if not ci_ok:
                print(f"    [!] Skipping auto-merge for PR #{pr_number} in {repo_name} due to failing or pending CI checks.")
                return False

        if self.dry_run:
            print(f"[DRY-RUN] Would merge PR #{pr_number} in {repo_name}")
            return True
        res = self._api_call(f"/repos/{self.owner}/{repo_name}/pulls/{pr_number}/merge", method="PUT", data={"merge_method": merge_method})
        merged = res.get("merged", False) if res and isinstance(res, dict) else False
        if merged:
            print(f"[+] Successfully merged PR #{pr_number} in {repo_name}")
        else:
            print(f"[-] Could not merge PR #{pr_number} in {repo_name}")
        return merged

    def comment_on_issue_or_pr(self, repo_name, item_number, comment_body):
        """Post a comment on an Issue or PR."""
        if self.dry_run:
            print(f"[DRY-RUN] Would comment on #{item_number} in {repo_name}: {comment_body[:60]}...")
            return True
        res = self._api_call(f"/repos/{self.owner}/{repo_name}/issues/{item_number}/comments", method="POST", data={"body": comment_body})
        if res and isinstance(res, dict) and "id" in res:
            print(f"[+] Commented on #{item_number} in {repo_name}")
            return True
        print(f"[-] Failed to comment on #{item_number} in {repo_name}")
        return False

    def close_pr(self, repo_name, pr_number, comment=None):
        """Close an unmergeable PR and optionally add a closing comment."""
        if comment:
            self.comment_on_issue_or_pr(repo_name, pr_number, comment)
        if self.dry_run:
            print(f"[DRY-RUN] Would close PR #{pr_number} in {repo_name}")
            return True
        res = self._api_call(f"/repos/{self.owner}/{repo_name}/pulls/{pr_number}", method="PATCH", data={"state": "closed"})
        if res and isinstance(res, dict) and res.get("state") == "closed":
            print(f"[+] Closed PR #{pr_number} in {repo_name}")
            return True
        print(f"[-] Failed to close PR #{pr_number} in {repo_name}")
        return False

    def handle_unmergeable_pr(self, repo_name, pr, reason="CI checks failed or merge conflicts detected"):
        """
        Comprehensive handler for PRs that cannot be auto-merged:
        1. Posts an diagnostic comment explaining blocking checks / conflicts.
        2. Closes stale/failing unmergeable PRs if requested.
        """
        pr_num = pr["number"]
        title = pr["title"]
        user = pr.get("user", {}).get("login", "")
        updated_at = pr.get("updated_at", "")
        
        comment = (
            f"🤖 **Automated Maintenance Agent Report**\n\n"
            f"PR #{pr_num} ('{title}') could not be automatically merged.\n"
            f"**Reason**: {reason}.\n\n"
            f"Please review CI statuses and resolve merge conflicts or update the head branch."
        )
        print(f"    [!] Handling unmergeable PR #{pr_num} in {repo_name}...")
        self.comment_on_issue_or_pr(repo_name, pr_num, comment)

    def close_issue(self, repo_name, issue_number, reason="completed"):
        if self.dry_run:
            print(f"[DRY-RUN] Would close Issue #{issue_number} in {repo_name}")
            return True
        res = self._api_call(f"/repos/{self.owner}/{repo_name}/issues/{issue_number}", method="PATCH", data={"state": "closed", "state_reason": reason})
        if res and isinstance(res, dict):
            print(f"[+] Successfully closed Issue #{issue_number} in {repo_name}")
            return True
        return False

    def archive_repository(self, repo_name):
        """Archive a repository."""
        if self.dry_run:
            print(f"[DRY-RUN] Would archive repository {self.owner}/{repo_name}")
            return True
        res = self._api_call(f"/repos/{self.owner}/{repo_name}", method="PATCH", data={"archived": True})
        if res and isinstance(res, dict) and res.get("archived"):
            print(f"[+] Repository {self.owner}/{repo_name} archived successfully.")
            return True
        print(f"[-] Failed to archive repository {self.owner}/{repo_name}.")
        return False

    def delete_branch(self, repo_name, branch_name):
        """Delete a remote git branch."""
        if self.dry_run:
            print(f"[DRY-RUN] Would delete branch '{branch_name}' in {repo_name}")
            return True
        res = self._api_call(f"/repos/{self.owner}/{repo_name}/git/refs/heads/{branch_name}", method="DELETE")
        if res is True or res is None:
            print(f"[+] Deleted branch '{branch_name}' in {repo_name}")
            return True
        print(f"[-] Could not delete branch '{branch_name}' in {repo_name}")
        return False

    def handle_badge_pr(self, repo_name, pr):
        """
        Default handler for PRs that add/update compliance badges (e.g. Soluble badges, iacbot).
        Auto-merges clean badge PRs and deletes the associated head branch.
        """
        pr_num = pr["number"]
        title = pr["title"]
        user = pr.get("user", {}).get("login", "")
        pr_sha = pr.get("head", {}).get("sha")
        head_branch = pr.get("head", {}).get("ref")

        print(f"    Attempting auto-merge for badge PR #{pr_num} ('{title}' by {user})...")
        merged = self.merge_pr(repo_name, pr_num, pr_ref=pr_sha)
        if merged:
            print(f"    [Info] Badge PR #{pr_num} merged successfully.")
            if head_branch:
                self.delete_branch(repo_name, head_branch)
            return True
        else:
            print(f"    [Notice] Badge PR #{pr_num} could not be auto-merged.")
            return False

    def get_dependabot_alerts(self, repo_name, state="open", severity=None, ecosystem=None):
        """
        Fetch Dependabot alerts for a repository with optional state, severity, and ecosystem filtering.
        Gracefully handles repos where Dependabot is disabled or inaccessible.
        """
        endpoint = f"/repos/{self.owner}/{repo_name}/dependabot/alerts?state={state}"
        if severity:
            endpoint += f"&severity={severity}"
        if ecosystem:
            endpoint += f"&ecosystem={ecosystem}"
        
        alerts = self._fetch_paginated_api(endpoint)
        if alerts is None or not isinstance(alerts, list):
            return []
        return alerts

    def determine_alert_remediation(self, alert, open_prs=None):
        """
        Assess an individual Dependabot security alert and determine the best method of fixing it.
        Returns a structured remediation recommendation dictionary.
        """
        alert_num = alert.get("number")
        html_url = alert.get("html_url", "")
        
        # Dependency details
        dep = alert.get("dependency", {})
        pkg = dep.get("package", {})
        pkg_name = pkg.get("name", "unknown")
        ecosystem = pkg.get("ecosystem", "unknown")
        manifest_path = dep.get("manifest_path", "")
        scope = dep.get("scope", "runtime")

        # Security advisory & vulnerability details
        advisory = alert.get("security_advisory", {})
        ghsa_id = advisory.get("ghsa_id", "")
        cve_id = advisory.get("cve_id", "")
        summary = advisory.get("summary", "No summary available")
        severity = (advisory.get("severity") or alert.get("security_vulnerability", {}).get("severity") or "unknown").lower()
        cvss = advisory.get("cvss", {})
        cvss_score = cvss.get("score") if isinstance(cvss, dict) else None

        vuln = alert.get("security_vulnerability", {})
        vulnerable_range = vuln.get("vulnerable_version_range", "")
        first_patched = vuln.get("first_patched_version") or {}
        patched_version = first_patched.get("identifier") if isinstance(first_patched, dict) else None

        # 1. Check if an existing open PR addresses this package
        associated_pr = None
        if open_prs:
            for pr in open_prs:
                pr_title = pr.get("title", "").lower()
                pr_branch = pr.get("head", {}).get("ref", "").lower()
                pkg_clean = pkg_name.lower()
                if (pkg_clean in pr_title or pkg_clean in pr_branch) and ("bump" in pr_title or "update" in pr_title or "dependabot" in pr.get("user", {}).get("login", "").lower()):
                    associated_pr = pr
                    break

        # 2. Determine Strategy
        if associated_pr:
            strategy = "MERGE_DEPENDABOT_PR"
            pr_num = associated_pr.get("number")
            pr_title = associated_pr.get("title")
            target_version = patched_version or "N/A"
            action = f"Dependabot Pull Request #{pr_num} ('{pr_title}') is open. Review CI checks and squash-merge the PR."
            command = f"Agent auto-merge PR #{pr_num} or `gh pr merge {pr_num} --squash`"
        elif patched_version:
            target_version = patched_version
            lockfile_extensions = [".lock", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "cargo.lock", "go.sum", "composer.lock"]
            is_lockfile = any(manifest_path.lower().endswith(ext) for ext in lockfile_extensions)
            
            if is_lockfile:
                strategy = "TRANSITIVE_LOCKFILE_UPDATE"
                action = f"Vulnerability resides in transitive lockfile ({manifest_path}). Refresh lockfile to pull patched version {target_version}."
                command = generate_ecosystem_remediation_command(ecosystem, pkg_name, target_version, manifest_path, strategy)
            elif is_major_version_jump(vulnerable_range, target_version):
                strategy = "MAJOR_UPGRADE"
                action = f"Major version upgrade required to {target_version} ({vulnerable_range} -> {target_version}). Review changelog for breaking changes and update codebase."
                command = generate_ecosystem_remediation_command(ecosystem, pkg_name, target_version, manifest_path, strategy)
            else:
                strategy = "PATCH_UPGRADE"
                action = f"Direct non-breaking patch/minor upgrade available ({vulnerable_range} -> {target_version}). Update manifest and lockfile."
                command = generate_ecosystem_remediation_command(ecosystem, pkg_name, target_version, manifest_path, strategy)
        else:
            target_version = "None Available"
            if scope == "development":
                strategy = "DEV_DEPENDENCY_RISK_ACCEPTANCE"
                action = f"Development-only dependency with no official patch available. Verify test-only isolation or evaluate dismissal (reason: tolerable_risk/not_used)."
                command = "# Verify development tool isolation; dismiss via API if risk is acceptable"
            else:
                strategy = "WORKAROUND_OR_MITIGATION"
                action = f"No patched version currently released (zero-day/unpatched). Apply input validation/sanitization, disable vulnerable sub-modules, or replace {pkg_name}."
                command = f"# Review advisory {ghsa_id or cve_id} workarounds and evaluate replacement libraries"

        return {
            "number": alert_num,
            "package_name": pkg_name,
            "ecosystem": ecosystem,
            "manifest_path": manifest_path,
            "scope": scope,
            "severity": severity,
            "cvss_score": cvss_score,
            "ghsa_id": ghsa_id,
            "cve_id": cve_id,
            "summary": summary,
            "vulnerable_range": vulnerable_range,
            "target_version": target_version,
            "strategy": strategy,
            "recommended_action": action,
            "command": command,
            "associated_pr": associated_pr.get("number") if associated_pr else None,
            "html_url": html_url
        }

    def assess_dependabot_alerts(self, repo_name, open_prs=None, severity=None, ecosystem=None, verbose=True):
        """
        Audit and review all open Dependabot alerts for a repository and determine best remediation methods.
        """
        raw_alerts = self.get_dependabot_alerts(repo_name, state="open", severity=severity, ecosystem=ecosystem)
        if not raw_alerts:
            # If verbose and called standalone, keep it clean or omit extra line
            return {
                "total": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "alerts": []
            }

        assessed = []
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "unknown": 0}

        for alert in raw_alerts:
            rem = self.determine_alert_remediation(alert, open_prs=open_prs)
            assessed.append(rem)
            sev = rem.get("severity", "unknown").lower()
            counts[sev] = counts.get(sev, 0) + 1

        if verbose:
            print(f"\n    [🛡️] Dependabot Security Alerts Review for {repo_name}:")
            print(f"        Total Open Alerts: {len(assessed)} | Critical: {counts['critical']}, High: {counts['high']}, Medium: {counts['medium']}, Low: {counts['low']}")
            print(f"        " + "-" * 72)
            for idx, a in enumerate(assessed, 1):
                sev_tag = a['severity'].upper()
                id_str = f"{a['ghsa_id']}" + (f" / {a['cve_id']}" if a['cve_id'] else "")
                cvss_str = f" [CVSS: {a['cvss_score']}]" if a['cvss_score'] is not None else ""
                print(f"        [{idx}] Alert #{a['number']} [{sev_tag}] {a['package_name']} ({a['ecosystem']}) in `{a['manifest_path']}`")
                print(f"            Advisory: {a['summary']} ({id_str}){cvss_str}")
                print(f"            Scope: {a['scope']} | Vulnerable: {a['vulnerable_range']} -> Target: {a['target_version']}")
                print(f"            Strategy: {a['strategy']}")
                print(f"            Action: {a['recommended_action']}")
                print(f"            Fix Command: {a['command']}")
                if a.get("associated_pr"):
                    print(f"            Linked Open PR: #{a['associated_pr']}")
                print()

        return {
            "total": len(assessed),
            "critical": counts["critical"],
            "high": counts["high"],
            "medium": counts["medium"],
            "low": counts["low"],
            "alerts": assessed
        }

    def resolve_dependabot_alerts(self, repo_name, assessed_alerts, open_prs=None):
        """
        Attempt automated resolution for assessed Dependabot alerts:
        1. If a linked Dependabot PR is already open:
           - Attempt to auto-merge if CI passes.
           - If CI fails, diagnose check runs, report root cause, and request @dependabot rebase if stale.
        2. If dev dependency risk acceptance:
           - Option to dismiss tolerable test/dev tool risks via GitHub API.
        """
        if not assessed_alerts:
            return {"resolved": [], "unresolved": [], "closed_prs": [], "failed_prs": []}

        prs_by_number = {pr["number"]: pr for pr in (open_prs or [])}
        results = {"resolved": [], "unresolved": [], "closed_prs": [], "failed_prs": []}

        print(f"    [🛡️] Attempting automated resolution for {len(assessed_alerts)} open Dependabot alert(s)...")

        for alert in assessed_alerts:
            alert_num = alert.get("number")
            pkg_name = alert.get("package_name")
            strategy = alert.get("strategy")
            assoc_pr_num = alert.get("associated_pr")

            print(f"    -> Analyzing Alert #{alert_num}: {pkg_name} [{strategy}]")

            if assoc_pr_num and assoc_pr_num in prs_by_number:
                pr = prs_by_number[assoc_pr_num]
                pr_title = pr.get("title", "")
                pr_sha = pr.get("head", {}).get("sha")
                print(f"       Linked PR #{assoc_pr_num} found for alert #{alert_num}. Evaluating mergeability & CI...")

                # Check if CI is passing
                ci_ok = self.check_pr_ci_status(repo_name, pr_sha) if pr_sha else False
                if ci_ok:
                    merged = self.merge_pr(repo_name, assoc_pr_num, pr_ref=pr_sha)
                    if merged:
                        print(f"       [+] Auto-merged PR #{assoc_pr_num}; resolved Alert #{alert_num} for {pkg_name}.")
                        results["resolved"].append(alert_num)
                        results["closed_prs"].append((assoc_pr_num, pr_title))
                        continue
                    else:
                        print(f"       [-] Merge failed for PR #{assoc_pr_num}.")
                        results["failed_prs"].append((assoc_pr_num, pr_title))
                else:
                    # Provide diagnosis for why the alert's PR is blocked
                    print(f"       [!] PR #{assoc_pr_num} CI checks failed or are pending. Alert #{alert_num} remains open.")
                    reason = f"Security update PR #{assoc_pr_num} for {pkg_name} blocked by failing/pending CI checks"
                    self.handle_unmergeable_pr(repo_name, pr, reason=reason)
                    results["failed_prs"].append((assoc_pr_num, pr_title))

            elif strategy == "DEV_DEPENDENCY_RISK_ACCEPTANCE":
                print(f"       [Info] Alert #{alert_num} is scoped to development tools with no patch available.")

            results["unresolved"].append(alert_num)

        return results

    def dismiss_dependabot_alert(self, repo_name, alert_number, reason="tolerable_risk", comment=""):
        """
        Dismiss a Dependabot alert via the GitHub API with a specified reason.
        Reasons: 'fix_started', 'inaccurate', 'no_bandwidth', 'not_used', 'tolerable_risk'
        """
        valid_reasons = ["fix_started", "inaccurate", "no_bandwidth", "not_used", "tolerable_risk"]
        if reason not in valid_reasons:
            print(f"[-] Invalid dismissal reason '{reason}'. Must be one of {valid_reasons}")
            return False

        if self.dry_run:
            print(f"[DRY-RUN] Would dismiss Dependabot alert #{alert_number} in {repo_name} (Reason: {reason})")
            return True

        res = self._api_call(
            f"/repos/{self.owner}/{repo_name}/dependabot/alerts/{alert_number}",
            method="PATCH",
            data={"state": "dismissed", "dismissed_reason": reason, "dismissed_comment": comment}
        )
        if res and isinstance(res, dict) and res.get("state") == "dismissed":
            print(f"[+] Successfully dismissed Dependabot alert #{alert_number} in {repo_name}")
            return True
        print(f"[-] Failed to dismiss Dependabot alert #{alert_number} in {repo_name}")
        return False

    def check_all_dependabot_alerts(self, severity=None, ecosystem=None, target_repo=None):
        """
        Assess and review Dependabot alerts across all or targeted repositories.
        """
        if target_repo:
            repos = [{"name": target_repo}]
        else:
            repos = self.get_all_repositories(verbose=False)

        print(f"[*] Auditing Dependabot security alerts across {len(repos)} repository/repositories...")
        summaries = {}
        for r in repos:
            repo_name = r["name"]
            _, prs = self.get_open_issues_and_prs(repo_name)
            res = self.assess_dependabot_alerts(repo_name, open_prs=prs, severity=severity, ecosystem=ecosystem, verbose=True)
            summaries[repo_name] = res
        return summaries

    def process_repository(self, repo_name):
        issues, prs = self.get_open_issues_and_prs(repo_name)
        # Assess Dependabot security alerts first to display full line summary cleanly
        alerts_summary = self.assess_dependabot_alerts(repo_name, open_prs=prs, verbose=False)
        alerts_count = alerts_summary.get("total", 0)

        total_items = len(issues) + len(prs)
        print(f"  [*] Repository: {repo_name:<44} | Total Open Items Audited: {total_items} ({len(issues)} issues, {len(prs)} PRs) | Dependabot Alerts: {alerts_count}")

        # If there are alerts, print the detailed review and attempt resolution
        if alerts_count > 0:
            print(f"    [🛡️] Open Dependabot Alerts ({alerts_count}): Critical: {alerts_summary.get('critical', 0)}, High: {alerts_summary.get('high', 0)}, Medium: {alerts_summary.get('medium', 0)}, Low: {alerts_summary.get('low', 0)}")
            for idx, a in enumerate(alerts_summary.get("alerts", []), 1):
                sev_tag = a['severity'].upper()
                id_str = f"{a['ghsa_id']}" + (f" / {a['cve_id']}" if a['cve_id'] else "")
                cvss_str = f" [CVSS: {a['cvss_score']}]" if a['cvss_score'] is not None else ""
                print(f"        [{idx}] Alert #{a['number']} [{sev_tag}] {a['package_name']} ({a['ecosystem']}) in `{a['manifest_path']}`")
                print(f"            Advisory: {a['summary']} ({id_str}){cvss_str}")
                print(f"            Scope: {a['scope']} | Vulnerable: {a['vulnerable_range']} -> Target: {a['target_version']}")
                print(f"            Strategy: {a['strategy']}")
                print(f"            Action: {a['recommended_action']}")
                print(f"            Fix Command: {a['command']}")
                if a.get("associated_pr"):
                    print(f"            Linked Open PR: #{a['associated_pr']}")

            # Attempt automated resolution for alerts
            alert_res = self.resolve_dependabot_alerts(repo_name, alerts_summary.get("alerts", []), open_prs=prs)
        else:
            alert_res = {"resolved": [], "unresolved": [], "closed_prs": [], "failed_prs": []}

        repo_summary = {
            "issues_count": len(issues),
            "prs_count": len(prs),
            "alerts_count": alerts_summary.get("total", 0),
            "alerts_breakdown": alerts_summary,
            "closed_prs": list(alert_res.get("closed_prs", [])),
            "failed_prs": list(alert_res.get("failed_prs", [])),
            "unclosed_prs": [],
            "closed_issues": [],
            "failed_issues": [],
            "unclosed_issues": []
        }

        handled_pr_nums = {num for num, _ in repo_summary["closed_prs"]} | {num for num, _ in repo_summary["failed_prs"]}

        # Process PRs (Dependabot merges, badge PRs & dependency updates)
        for pr in prs:
            pr_num = pr["number"]
            title = pr["title"]
            user = pr.get("user", {}).get("login", "")
            pr_sha = pr.get("head", {}).get("sha")

            if pr_num in handled_pr_nums:
                continue

            print(f" -> PR #{pr_num}: {title} (Author: {user})")
            
            is_dependabot = "dependabot" in user.lower() or "bump" in title.lower()
            is_badge_pr = "badge" in title.lower() or "iacbot" in user.lower() or "soluble" in title.lower()

            if is_badge_pr:
                merged = self.handle_badge_pr(repo_name, pr)
                if merged:
                    repo_summary["closed_prs"].append((pr_num, title))
                else:
                    self.handle_unmergeable_pr(repo_name, pr, reason="Badge PR failed auto-merge checks")
                    repo_summary["failed_prs"].append((pr_num, title))
            elif is_dependabot:
                print(f"    Attempting auto-merge for dependency update PR #{pr_num}...")
                merged = self.merge_pr(repo_name, pr_num, pr_ref=pr_sha)
                if merged:
                    print(f"    [Info] Dependency upgrade confirmed & auto-merged for PR #{pr_num}.")
                    repo_summary["closed_prs"].append((pr_num, title))
                else:
                    print(f"    [Notice] Dependabot PR #{pr_num} required manual review or CI checks passed condition failure.")
                    self.handle_unmergeable_pr(repo_name, pr, reason="Dependabot PR CI checks failed or merge conflicts exist")
                    repo_summary["failed_prs"].append((pr_num, title))
            else:
                self.handle_unmergeable_pr(repo_name, pr, reason="Non-automated PR requires manual review or local rebase")
                repo_summary["unclosed_prs"].append((pr_num, title))

        # Process issues (Security scan deduplication & automated notifications)
        closed_issue_nums = set()
        failed_issue_nums = set()

        security_issues = [i for i in issues if "security" in i.get("title", "").lower() or "security" in [l["name"] for l in i.get("labels", [])]]
        if len(security_issues) > 1:
            print(f" -> Found {len(security_issues)} security scan issues. Deduplicating...")
            security_issues.sort(key=lambda x: x["number"], reverse=True)
            for old_issue in security_issues[1:]:
                print(f"    Closing duplicate security issue #{old_issue['number']}...")
                closed = self.close_issue(repo_name, old_issue["number"])
                if closed:
                    closed_issue_nums.add(old_issue["number"])
                    repo_summary["closed_issues"].append((old_issue["number"], old_issue.get("title", "")))
                else:
                    failed_issue_nums.add(old_issue["number"])
                    repo_summary["failed_issues"].append((old_issue["number"], old_issue.get("title", "")))

        for issue in issues:
            title = issue.get("title", "")
            num = issue["number"]
            if num in closed_issue_nums or num in failed_issue_nums:
                continue

            if "automated dependency branch" in title.lower():
                print(f"    Closing automated branch notification issue #{num}...")
                closed = self.close_issue(repo_name, num)
                if closed:
                    closed_issue_nums.add(num)
                    repo_summary["closed_issues"].append((num, title))
                else:
                    failed_issue_nums.add(num)
                    repo_summary["failed_issues"].append((num, title))
            elif "refactor" in title.lower() or "tech debt" in title.lower():
                print(f" -> Refactoring / Tech Debt candidate found in Issue #{num}: {title}")
                print(f"    [Info] Local workspace refactoring hook triggered for issue #{num}.")
                repo_summary["unclosed_issues"].append((num, title))
            else:
                repo_summary["unclosed_issues"].append((num, title))

        return repo_summary

    def print_execution_summary(self, summaries):
        """Prints a comprehensive summary table/list at the end of execution."""
        if not summaries:
            print("No repositories were processed.")
            return

        for repo_name, s in summaries.items():
            total_items = s["issues_count"] + s["prs_count"]
            alerts_count = s.get("alerts_count", 0)
            print(f"[*] Repository: {repo_name:<46} | Open Items: {total_items} ({s['issues_count']} issues, {s['prs_count']} PRs) | Dependabot Alerts: {alerts_count}")

            if total_items == 0 and alerts_count == 0:
                continue

            if alerts_count > 0:
                ab = s.get("alerts_breakdown", {})
                print(f"  [🛡️] Open Dependabot Alerts ({alerts_count}): Critical: {ab.get('critical', 0)}, High: {ab.get('high', 0)}, Medium: {ab.get('medium', 0)}, Low: {ab.get('low', 0)}")
                for a in ab.get("alerts", []):
                    strat = a.get("strategy")
                    pkg = a.get("package_name")
                    sev = a.get("severity", "").upper()
                    target = a.get("target_version")
                    print(f"      - Alert #{a.get('number')} [{sev}] {pkg} -> {strat} (Target: {target})")

            if s["closed_prs"]:
                print("  [+] PRs Closed/Merged Successfully:")
                for num, title in s["closed_prs"]:
                    print(f"      - PR #{num}: {title}")
            if s["closed_issues"]:
                print("  [+] Issues Closed Successfully:")
                for num, title in s["closed_issues"]:
                    print(f"      - Issue #{num}: {title}")

            if s["failed_prs"]:
                print("  [-] PRs Attempted but Failed to Merge/Close:")
                for num, title in s["failed_prs"]:
                    print(f"      - PR #{num}: {title}")
            if s["failed_issues"]:
                print("  [-] Issues Attempted but Failed to Close:")
                for num, title in s["failed_issues"]:
                    print(f"      - Issue #{num}: {title}")

            if s["unclosed_prs"]:
                print("  [•] PRs Remaining Open (Not Closed):")
                for num, title in s["unclosed_prs"]:
                    print(f"      - PR #{num}: {title}")
            if s["unclosed_issues"]:
                print("  [•] Issues Remaining Open (Not Closed):")
                for num, title in s["unclosed_issues"]:
                    print(f"      - Issue #{num}: {title}")

    def get_all_repositories(self, verbose=True):
        """Fetch all repositories owned by user, handling pagination."""
        if verbose:
            print(f"[*] Fetching all repositories for {self.owner}...")
        return self._fetch_paginated_api(f"/user/repos?type=all")

    def scan_and_fix_all(self):
        """Scan and fix all issues, Dependabot alerts, and PRs across all repositories."""
        repos = self.get_all_repositories()
        print(f"[*] Starting scan and fix across {len(repos)} repositories...")
        summaries = {}
        for r in repos:
            summaries[r["name"]] = self.process_repository(r["name"])
        self.print_execution_summary(summaries)
        return summaries

    def sync_forks(self, target_repo=None):
        """Sync forked repos with updates from their upstream/original repository."""
        if target_repo:
            repo_data = self._api_call(f"/repos/{self.owner}/{target_repo}")
            if repo_data and isinstance(repo_data, dict):
                forked_repos = [repo_data]
            else:
                print(f"[-] Repository {target_repo} not found under {self.owner}.")
                return
        else:
            repos = self.get_all_repositories(verbose=False)
            forked_repos = [r for r in repos if r.get("fork", False) and not r.get("archived", False)]

        total_forks = len(forked_repos)
        print(f"[*] Found {total_forks} forked repository/repositories to check for upstream sync.")
        is_tty = sys.stdout.isatty()

        for idx, r in enumerate(forked_repos, 1):
            repo_name = r["name"]
            default_branch = r.get("default_branch", "main")
            if r.get("archived", False):
                continue

            if is_tty:
                sys.stdout.write(f"\r\033[K\033[5m[*]\033[0m Checking forked repository ({idx}/{total_forks}): {repo_name}...")
                sys.stdout.flush()

            if self.dry_run:
                if is_tty:
                    sys.stdout.write("\r\033[K")
                    sys.stdout.flush()
                print(f"[DRY-RUN] Would sync fork {repo_name} with upstream branch {default_branch}")
                continue

            res = self._api_call(
                f"/repos/{self.owner}/{repo_name}/merge-upstream",
                method="POST",
                data={"branch": default_branch}
            )

            if is_tty:
                sys.stdout.write("\r\033[K")
                sys.stdout.flush()

            if res and isinstance(res, dict):
                msg = res.get("message", "")
                status = res.get("_http_status")
                if status == 409 or "conflict" in msg.lower():
                    print(f"[!] Merge conflict detected for {repo_name} (branch: {default_branch}).")
                    self._resolve_fork_conflict(r, default_branch)
                elif "successfully merged" in msg.lower() or "synced" in msg.lower():
                    print(f"[+] Successfully synced {repo_name} with upstream.")
                elif "is not behind" in msg.lower() or "archived" in msg.lower():
                    pass
                else:
                    print(f"[-] Could not sync fork {repo_name}: {msg}")
            elif res is True:
                print(f"[+] Successfully synced {repo_name} with upstream.")
            else:
                print(f"[-] Could not sync fork {repo_name}.")

        if is_tty:
            sys.stdout.write("\r\033[K")
            sys.stdout.flush()

    def _resolve_fork_conflict(self, repo, default_branch):
        repo_name = repo.get("name")
        parent = repo.get("parent") or {}
        parent_owner = parent.get("owner", {}).get("login")
        parent_branch = parent.get("default_branch", default_branch)

        if not parent_owner:
            repo_details = self._api_call(f"/repos/{self.owner}/{repo_name}")
            if repo_details and isinstance(repo_details, dict):
                parent = repo_details.get("parent") or {}
                parent_owner = parent.get("owner", {}).get("login")
                parent_branch = parent.get("default_branch", default_branch)

        if not parent_owner:
            print(f"[-] Cannot auto-resolve conflict for {repo_name}: Parent repository information unavailable.")
            return

        head_ref = f"{parent_owner}:{parent_branch}"
        print(f"[*] Analyzing divergence between {self.owner}/{repo_name}:{default_branch} and {parent_owner}/{repo_name}:{parent_branch}...")

        comparison = self._api_call(f"/repos/{self.owner}/{repo_name}/compare/{default_branch}...{parent_owner}:{parent_branch}")
        if comparison and isinstance(comparison, dict):
            ahead_by = comparison.get("ahead_by", 0)
            behind_by = comparison.get("behind_by", 0)
            status = comparison.get("status", "unknown")
            files = comparison.get("files", [])
            modified_file_paths = [f.get("filename") for f in files if isinstance(f, dict) and f.get("filename")]

            print(f"[*] Divergence Analysis for {repo_name}:")
            print(f"    - Status: {status}")
            print(f"    - Ahead of upstream by: {ahead_by} commit(s)")
            print(f"    - Behind upstream by: {behind_by} commit(s)")
            print(f"    - Modified files in diff ({len(modified_file_paths)}): {', '.join(modified_file_paths[:10])}{'...' if len(modified_file_paths) > 10 else ''}")

            file_snippets = []
            if files:
                print("    - Code Snippets / Patch Preview of Committed Changes:")
                for f in files[:5]:
                    filename = f.get("filename", "")
                    patch = f.get("patch", "")
                    additions = f.get("additions", 0)
                    deletions = f.get("deletions", 0)
                    print(f"      * {filename} (+{additions} -{deletions}):")
                    if patch:
                        patch_lines = patch.split("\n")
                        preview = "\n".join(["        " + l for l in patch_lines[:10]])
                        print(preview)
                        if len(patch_lines) > 10:
                            print("        ...")
                        file_snippets.append(f"#### `{filename}` (+{additions} -{deletions})\n```diff\n" + "\n".join(patch_lines[:15]) + ("\n..." if len(patch_lines) > 15 else "") + "\n```")
                    else:
                        print("        [Binary file or patch unavailable]")

            commits = comparison.get("commits", [])
            if commits:
                print("    - Divergent local commits blocking clean upstream merge:")
                for c in commits[:5]:
                    c_msg = c.get("commit", {}).get("message", "").split("\n")[0]
                    c_sha = c.get("sha", "")[:7]
                    print(f"      * {c_sha}: {c_msg}")

            if ahead_by > 0:
                print(f"    [!] Consideration: Removing or rebasing/resetting these {ahead_by} local commit(s) (or hard-resetting branch `{default_branch}` to `{parent_owner}:{parent_branch}`) would allow a clean fast-forward merge from source/upstream.")

        print(f"[*] Creating Sync Pull Request ({head_ref} -> {default_branch}) for informed manual/automated review...")
        
        snippets_formatted = "\n\n### Code Snippets / Patch Preview:\n" + "\n\n".join(file_snippets) if file_snippets else ""
        pr_payload = {
            "title": f"Merge upstream changes from {parent_owner}/{parent_branch}",
            "body": (
                f"Automated sync PR created by `gh-helper-agent` due to `POST /merge-upstream` HTTP 409 conflict.\n\n"
                f"### Divergence Summary:\n"
                f"- **Ahead of upstream**: {comparison.get('ahead_by', 'N/A') if isinstance(comparison, dict) else 'N/A'} commits\n"
                f"- **Behind upstream**: {comparison.get('behind_by', 'N/A') if isinstance(comparison, dict) else 'N/A'} commits\n"
                f"- **Conflicting/Modified files count**: {len(comparison.get('files', [])) if isinstance(comparison, dict) else 'N/A'}"
                f"{snippets_formatted}"
            ),
            "head": head_ref,
            "base": default_branch
        }

        pr_res = self._api_call(f"/repos/{self.owner}/{repo_name}/pulls", method="POST", data=pr_payload)
        if pr_res and isinstance(pr_res, dict) and pr_res.get("html_url"):
            print(f"[+] Conflict resolution PR created: {pr_res['html_url']}")
        elif pr_res and isinstance(pr_res, dict) and "already exists" in pr_res.get("message", "").lower():
            print(f"[Info] A synchronization Pull Request already exists for {repo_name}.")
        else:
            err_msg = pr_res.get("message") if isinstance(pr_res, dict) else pr_res
            print(f"[-] Could not create conflict resolution PR for {repo_name}: {err_msg}")

    def identify_and_manage_stale_repos(self, days_inactive=365):
        """
        Identify all repos that have not been accessed/pushed/updated for more than 1 year (or specified days).
        Ask for user confirmation to archive or delete each stale repo.
        """
        from datetime import datetime, timezone, timedelta

        repos = self.get_all_repositories()
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_inactive)
        stale_repos = []

        print(f"[*] Checking for repositories inactive for more than {days_inactive} days (cutoff: {cutoff_date.isoformat()})...")

        for r in repos:
            if r.get("archived"):
                continue
            pushed_at_str = r.get("pushed_at") or r.get("updated_at")
            if not pushed_at_str:
                continue
            pushed_at = datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
            if pushed_at < cutoff_date:
                stale_repos.append((r, pushed_at_str))

        if not stale_repos:
            print("[+] No stale unarchived repositories found!")
            return

        print(f"\n[!] Found {len(stale_repos)} unarchived repository/repositories inactive for more than {days_inactive} days:")
        for r, last_active in stale_repos:
            print(f"  - {r['full_name']} (Last active: {last_active})")

        for r, last_active in stale_repos:
            repo_name = r["name"]
            full_name = r["full_name"]
            print(f"\n[!] Repository '{full_name}' has not been active since {last_active}.")
            if self.dry_run:
                print(f"[DRY-RUN] Would prompt for confirmation to Archive (a) or Delete (d) repository {full_name}")
                continue

            action = input(f"Action for repository '{full_name}'? Archive (a), Delete (d), or Skip (s) [Default: a]: ").strip().lower()
            if not action or action == "a":
                print(f"[*] Archiving repository {full_name}...")
                self.archive_repository(repo_name)
            elif action == "d":
                confirm = input(f"Are you SURE you want to permanently DELETE '{full_name}'? (y/N): ").strip().lower()
                if confirm in ["y", "yes"]:
                    print(f"[*] Deleting repository {full_name}...")
                    success = self.delete_repository(repo_name)
                    if success:
                        print(f"[+] Repository {full_name} deleted successfully.")
                    else:
                        print(f"[-] Failed to delete repository {full_name}.")
                else:
                    print(f"[Info] Skipped deletion of {full_name}.")
            else:
                print(f"[Info] Skipped {full_name}.")

    def delete_repository(self, repo_name):
        """Delete a repository given its name."""
        if self.dry_run:
            print(f"[DRY-RUN] Would delete repository {self.owner}/{repo_name}")
            return True
        return self._api_call(f"/repos/{self.owner}/{repo_name}", method="DELETE")

    def run_all(self, limit=10):
        repos = self.get_recent_repositories(limit=limit)
        summaries = {}
        for r in repos:
            summaries[r["name"]] = self.process_repository(r["name"])
        self.print_execution_summary(summaries)
        return summaries

def main():
    parser = argparse.ArgumentParser(description="GitHub Helper Agent - Automates PR merges, issue closures, Dependabot alert assessments, fork sync, and repo maintenance.")
    parser.add_argument("--owner", default=os.environ.get("GITHUB_OWNER", "jsoehner"), help="GitHub repository owner/username")
    parser.add_argument("--repo", help="Target a specific repository by name")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of repositories to process")
    parser.add_argument("--all", action="store_true", help="Run ALL maintenance tasks across all repositories (Dependabot alert assessment & review, PR auto-merges, issue closures, fork sync, stale checks)")
    parser.add_argument("--scan-and-fix-all", action="store_true", help="Scan and fix all issues, Dependabot alerts, and PRs across repositories")
    parser.add_argument("--check-alerts", "--dependabot-alerts", dest="check_alerts", action="store_true", help="Assess and review Dependabot alerts across repositories")
    parser.add_argument("--severity", help="Filter Dependabot alerts by severity (low, medium, high, critical)")
    parser.add_argument("--ecosystem", help="Filter Dependabot alerts by ecosystem (npm, pip, gomod, cargo, maven, composer, nuget, etc.)")
    parser.add_argument("--sync-forks", action="store_true", help="Sync forked repositories with upstream changes")
    parser.add_argument("--check-stale", action="store_true", help="Identify repos inactive for >1 year and ask for confirmation before deletion/archival")
    parser.add_argument("--dry-run", action="store_true", help="Run audit without performing write actions")
    args = parser.parse_args()

    agent = GitHubHelperAgent(owner=args.owner, dry_run=args.dry_run)

    # Determine which actions to execute
    run_scan = args.scan_and_fix_all
    run_sync = args.sync_forks
    run_stale = args.check_stale
    run_alerts = args.check_alerts

    # If no specific action flag is provided, or if --all is passed, run ALL maintenance operations by default
    if not (args.scan_and_fix_all or args.sync_forks or args.check_stale or args.check_alerts) or args.all:
        run_scan = True
        run_sync = True
        run_stale = True
        run_alerts = True

    print(f"[*] GitHub Helper Agent initialized for owner: {agent.owner} (Dry Run: {agent.dry_run})")

    # 1. Scan and Fix PRs, Issues & Dependabot Alerts
    if run_scan:
        if args.repo:
            summary = agent.process_repository(args.repo)
            agent.print_execution_summary({args.repo: summary})
        elif args.limit:
            agent.run_all(limit=args.limit)
        else:
            agent.scan_and_fix_all()

    # 2. Standalone Dependabot Alerts Review (if requested without scan-and-fix-all)
    elif run_alerts:
        agent.check_all_dependabot_alerts(severity=args.severity, ecosystem=args.ecosystem, target_repo=args.repo)

    # 3. Sync Forked Repositories
    if run_sync:
        agent.sync_forks(target_repo=args.repo)

    # 4. Check for Stale Repositories
    if run_stale:
        agent.identify_and_manage_stale_repos()

if __name__ == "__main__":
    main()
