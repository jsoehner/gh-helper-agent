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
import urllib.request
import urllib.parse
import argparse

class GitHubHelperAgent:
    def __init__(self, token=None, owner="jsoehner", dry_run=False):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.owner = owner
        self.dry_run = dry_run
        if not self.token:
            print("[!] Warning: GITHUB_TOKEN environment variable is not set.")
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def _api_call(self, endpoint, method="GET", data=None):
        url = f"https://api.github.com{endpoint}"
        req = urllib.request.Request(url, headers=self.headers, method=method)
        payload = None
        if data:
            req.add_header("Content-Type", "application/json")
            payload = json.dumps(data).encode("utf-8")
        try:
            with urllib.request.urlopen(req, data=payload) as resp:
                if resp.status == 204:
                    return True
                res_data = resp.read().decode("utf-8")
                return json.loads(res_data) if res_data else True
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8', errors='ignore')
            print(f"[-] HTTP {e.code} for {method} {url}: {err_msg}")
            return None
        except Exception as e:
            print(f"[-] Error calling {method} {url}: {e}")
            return None

    def get_recent_repositories(self, limit=10):
        print(f"[*] Fetching top {limit} recent repositories for {self.owner}...")
        res = self._api_call(f"/user/repos?sort=updated&per_page={limit}")
        return res if res else []

    def get_open_issues_and_prs(self, repo_name):
        issues = self._api_call(f"/repos/{self.owner}/{repo_name}/issues?state=open") or []
        prs = self._api_call(f"/repos/{self.owner}/{repo_name}/pulls?state=open") or []
        actual_issues = [i for i in issues if "pull_request" not in i]
        return actual_issues, prs

    def merge_pr(self, repo_name, pr_number, merge_method="squash"):
        if self.dry_run:
            print(f"[DRY-RUN] Would merge PR #{pr_number} in {repo_name}")
            return True
        res = self._api_call(f"/repos/{self.owner}/{repo_name}/pulls/{pr_number}/merge", method="PUT", data={"merge_method": merge_method})
        merged = res.get("merged", False) if res else False
        if merged:
            print(f"[+] Successfully merged PR #{pr_number} in {repo_name}")
        else:
            print(f"[-] Could not merge PR #{pr_number} in {repo_name}")
        return merged

    def close_issue(self, repo_name, issue_number, reason="completed"):
        if self.dry_run:
            print(f"[DRY-RUN] Would close Issue #{issue_number} in {repo_name}")
            return True
        res = self._api_call(f"/repos/{self.owner}/{repo_name}/issues/{issue_number}", method="PATCH", data={"state": "closed", "state_reason": reason})
        if res:
            print(f"[+] Successfully closed Issue #{issue_number} in {repo_name}")
            return True
        return False

    def process_repository(self, repo_name):
        print(f"\n==========================================")
        print(f"[*] Processing Repository: {repo_name}")
        print(f"==========================================")
        issues, prs = self.get_open_issues_and_prs(repo_name)
        print(f"Found {len(issues)} open issues and {len(prs)} open PRs.")

        # Process PRs (Dependabot merges & dependency updates)
        for pr in prs:
            pr_num = pr["number"]
            title = pr["title"]
            user = pr.get("user", {}).get("login", "")
            print(f" -> PR #{pr_num}: {title} (Author: {user})")
            if "dependabot" in user.lower() or "bump" in title.lower():
                print(f"    Attempting auto-merge for dependency update PR #{pr_num}...")
                merged = self.merge_pr(repo_name, pr_num)
                if merged:
                    print(f"    [Info] Dependency upgrade confirmed & auto-merged for PR #{pr_num}.")
                else:
                    print(f"    [Notice] Dependabot PR #{pr_num} required manual review or CI checks passed condition failure.")

        # Process issues (Security scan deduplication & automated notifications)
        security_issues = [i for i in issues if "security" in i.get("title", "").lower() or "security" in [l["name"] for l in i.get("labels", [])]]
        if len(security_issues) > 1:
            print(f" -> Found {len(security_issues)} security scan issues. Deduplicating...")
            # Keep newest issue open, close older duplicates
            security_issues.sort(key=lambda x: x["number"], reverse=True)
            for old_issue in security_issues[1:]:
                print(f"    Closing duplicate security issue #{old_issue['number']}...")
                self.close_issue(repo_name, old_issue["number"])

        for issue in issues:
            title = issue.get("title", "")
            num = issue["number"]
            if "automated dependency branch" in title.lower():
                print(f"    Closing automated branch notification issue #{num}...")
                self.close_issue(repo_name, num)
            elif "refactor" in title.lower() or "tech debt" in title.lower():
                print(f" -> Refactoring / Tech Debt candidate found in Issue #{num}: {title}")
                print(f"    [Info] Local workspace refactoring hook triggered for issue #{num}.")

    def perform_local_dependency_upgrade(self, repo_path, package_name, target_version):
        """
        Helper method to run local dependency upgrades via package manager (e.g. go get, npm update).
        """
        print(f"[*] Running local dependency upgrade for {package_name} -> {target_version} at {repo_path}")
        if self.dry_run:
            print(f"[DRY-RUN] Would run local dependency upgrade command for {package_name}")
            return True
        # Future local execution command hook for agent tooling
        return True

    def perform_code_refactoring(self, repo_path, refactor_instruction):
        """
        Helper method to trigger automated code refactoring routines on a repository path.
        """
        print(f"[*] Triggering code refactoring at {repo_path} with instruction: {refactor_instruction}")
        if self.dry_run:
            print(f"[DRY-RUN] Would execute code refactoring routine for {repo_path}")
            return True
        return True

    def get_all_repositories(self):
        """Fetch all repositories owned by user, handling pagination."""
        print(f"[*] Fetching all repositories for {self.owner}...")
        repos = []
        page = 1
        while True:
            res = self._api_call(f"/user/repos?type=all&per_page=100&page={page}")
            if not res:
                break
            repos.extend(res)
            if len(res) < 100:
                break
            page += 1
        return repos

    def scan_and_fix_all(self):
        """Scan and fix all issues and PRs across all repositories."""
        repos = self.get_all_repositories()
        print(f"[*] Starting scan and fix across {len(repos)} repositories...")
        for r in repos:
            self.process_repository(r["name"])

    def sync_forks(self):
        """Sync any forked repos with updates from their upstream/original repository."""
        repos = self.get_all_repositories()
        forked_repos = [r for r in repos if r.get("fork", False)]
        print(f"[*] Found {len(forked_repos)} forked repositories to check for upstream sync.")

        for r in forked_repos:
            repo_name = r["name"]
            default_branch = r.get("default_branch", "main")
            print(f"\n[*] Checking fork sync for {repo_name} (branch: {default_branch})...")
            if self.dry_run:
                print(f"[DRY-RUN] Would sync fork {repo_name} with upstream branch {default_branch}")
                continue

            res = self._api_call(
                f"/repos/{self.owner}/{repo_name}/merge-upstream",
                method="POST",
                data={"branch": default_branch}
            )
            if res and isinstance(res, dict) and res.get("message"):
                msg = res.get("message")
                if "successfully merged" in msg.lower() or "synced" in msg.lower():
                    print(f"[+] Successfully synced {repo_name} with upstream.")
                else:
                    print(f"[Info] {repo_name}: {msg}")
            elif res is True:
                print(f"[+] Successfully synced {repo_name} with upstream.")
            else:
                print(f"[-] Could not sync fork {repo_name}.")

    def identify_and_manage_stale_repos(self, days_inactive=365):
        """
        Identify all repos that have not been accessed/pushed/updated for more than 1 year (or specified days).
        Ask for user confirmation before deleting each stale repo.
        """
        from datetime import datetime, timezone, timedelta

        repos = self.get_all_repositories()
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_inactive)
        stale_repos = []

        print(f"[*] Checking for repositories inactive for more than {days_inactive} days (cutoff: {cutoff_date.isoformat()})...")

        for r in repos:
            pushed_at_str = r.get("pushed_at") or r.get("updated_at")
            if not pushed_at_str:
                continue
            # Parse ISO 8601 timestamp
            pushed_at = datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
            if pushed_at < cutoff_date:
                stale_repos.append((r, pushed_at_str))

        if not stale_repos:
            print("[+] No stale repositories found!")
            return

        print(f"\n[!] Found {len(stale_repos)} repository/repositories inactive for more than {days_inactive} days:")
        for r, last_active in stale_repos:
            print(f"  - {r['full_name']} (Last active: {last_active})")

        for r, last_active in stale_repos:
            repo_name = r["name"]
            full_name = r["full_name"]
            print(f"\n[!] Repository '{full_name}' has not been active since {last_active}.")
            if self.dry_run:
                print(f"[DRY-RUN] Would prompt for confirmation and delete repository {full_name}")
                continue

            confirm = input(f"Are you sure you want to DELETE repository '{full_name}'? (y/N): ").strip().lower()
            if confirm in ["y", "yes"]:
                print(f"[*] Deleting repository {full_name}...")
                success = self.delete_repository(repo_name)
                if success:
                    print(f"[+] Repository {full_name} deleted successfully.")
                else:
                    print(f"[-] Failed to delete repository {full_name}.")
            else:
                print(f"[Info] Skipped deletion of {full_name}.")

    def delete_repository(self, repo_name):
        """Delete a repository given its name."""
        if self.dry_run:
            print(f"[DRY-RUN] Would delete repository {self.owner}/{repo_name}")
            return True
        return self._api_call(f"/repos/{self.owner}/{repo_name}", method="DELETE")

    def run_all(self, limit=10):
        repos = self.get_recent_repositories(limit=limit)
        for r in repos:
            self.process_repository(r["name"])

def main():
    parser = argparse.ArgumentParser(description="GitHub Helper Agent - Automates PR merges, issue closures, fork sync, and repo maintenance.")
    parser.add_argument("--owner", default="jsoehner", help="GitHub repository owner/username")
    parser.add_argument("--limit", type=int, default=10, help="Number of recent repositories to audit in default run mode")
    parser.add_argument("--scan-and-fix-all", action="store_true", help="Scan and fix all issues and PRs across ALL repositories")
    parser.add_argument("--sync-forks", action="store_true", help="Sync all forked repositories with upstream changes")
    parser.add_argument("--check-stale", action="store_true", help="Identify repos inactive for >1 year and ask for confirmation before deletion")
    parser.add_argument("--dry-run", action="store_true", help="Run audit without performing write actions")
    args = parser.parse_args()

    agent = GitHubHelperAgent(owner=args.owner, dry_run=args.dry_run)

    if args.scan_and_fix_all or args.sync_forks or args.check_stale:
        if args.scan_and_fix_all:
            agent.scan_and_fix_all()
        if args.sync_forks:
            agent.sync_forks()
        if args.check_stale:
            agent.identify_and_manage_stale_repos()
    else:
        agent.run_all(limit=args.limit)

if __name__ == "__main__":
    main()
