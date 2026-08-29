"""
Unit tests for github_helper_agent.py
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import urllib.error
import io

from github_helper_agent import (
    GitHubHelperAgent,
    load_dotenv,
    is_major_version_jump,
    generate_ecosystem_remediation_command,
)

class TestGitHubHelperAgent(unittest.TestCase):

    def setUp(self):
        self.agent = GitHubHelperAgent(token="test_token", owner="test_owner", dry_run=True)

    def test_init_headers(self):
        self.assertEqual(self.agent.headers["Authorization"], "token test_token")
        self.assertEqual(self.agent.headers["Accept"], "application/vnd.github.v3+json")

    @patch("urllib.request.urlopen")
    def test_api_call_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps({"key": "value"}).encode("utf-8")
        mock_resp.headers = {}
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        result = self.agent._api_call("/test")
        self.assertEqual(result, {"key": "value"})

    @patch("urllib.request.urlopen")
    def test_api_call_rate_limit_retry(self, mock_urlopen):
        # First call raises HTTP 429, second succeeds
        err_resp = io.BytesIO(b'{"message": "API rate limit exceeded"}')
        http_err = urllib.error.HTTPError("https://api.github.com/test", 429, "Too Many Requests", {"Retry-After": "0"}, err_resp)

        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps({"status": "ok"}).encode("utf-8")
        mock_resp.headers = {}

        mock_urlopen.side_effect = [http_err, MagicMock(__enter__=MagicMock(return_value=mock_resp))]

        result = self.agent._api_call("/test", retries=2)
        self.assertEqual(result, {"status": "ok"})

    def test_dry_run_delete_repo(self):
        result = self.agent.delete_repository("test_repo")
        self.assertTrue(result)

    # -------------------------------------------------------------
    # Version Jump & Command Generation Tests
    # -------------------------------------------------------------
    def test_is_major_version_jump(self):
        self.assertFalse(is_major_version_jump("< 4.19.2", "4.19.2"))
        self.assertFalse(is_major_version_jump(">= 2.1.0, < 2.5.0", "2.5.1"))
        self.assertTrue(is_major_version_jump("< 2.0.0", "2.0.1"))
        self.assertTrue(is_major_version_jump("< 1.5.0", "2.0.0"))
        self.assertTrue(is_major_version_jump("<= 0.9.1", "1.0.0"))
        self.assertFalse(is_major_version_jump(None, "1.0.0"))
        self.assertFalse(is_major_version_jump("< 1.0.0", None))
        self.assertFalse(is_major_version_jump("< 1.0.0", "None Available"))

    def test_generate_ecosystem_remediation_command(self):
        # npm
        cmd_npm = generate_ecosystem_remediation_command("npm", "lodash", "4.17.21", "package.json", "PATCH_UPGRADE")
        self.assertIn("npm install lodash@4.17.21", cmd_npm)

        cmd_npm_dev = generate_ecosystem_remediation_command("npm", "mocha", "10.0.0", "devDependencies/package.json", "PATCH_UPGRADE")
        self.assertIn("--save-dev", cmd_npm_dev)

        # pip / python
        cmd_pip = generate_ecosystem_remediation_command("pip", "requests", "2.31.0", "requirements.txt", "PATCH_UPGRADE")
        self.assertIn("pip install requests==2.31.0", cmd_pip)

        # gomod
        cmd_go = generate_ecosystem_remediation_command("gomod", "golang.org/x/net", "0.17.0", "go.mod", "PATCH_UPGRADE")
        self.assertIn("go get golang.org/x/net@v0.17.0", cmd_go)

        # cargo
        cmd_cargo = generate_ecosystem_remediation_command("cargo", "tokio", "1.38.1", "Cargo.toml", "PATCH_UPGRADE")
        self.assertIn("cargo update -p tokio --precise 1.38.1", cmd_cargo)

        # composer
        cmd_composer = generate_ecosystem_remediation_command("composer", "guzzlehttp/guzzle", "7.8.1", "composer.json", "PATCH_UPGRADE")
        self.assertIn("composer require guzzlehttp/guzzle:7.8.1", cmd_composer)

        # nuget
        cmd_nuget = generate_ecosystem_remediation_command("nuget", "Newtonsoft.Json", "13.0.3", "app.csproj", "PATCH_UPGRADE")
        self.assertIn("dotnet add package Newtonsoft.Json --version 13.0.3", cmd_nuget)

        # transitive lockfile update
        cmd_transitive = generate_ecosystem_remediation_command("npm", "brace-expansion", "2.0.1", "package-lock.json", "TRANSITIVE_LOCKFILE_UPDATE")
        self.assertEqual(cmd_transitive, "npm audit fix")

    # -------------------------------------------------------------
    # Dependabot Alert Assessment & Remediation Strategy Tests
    # -------------------------------------------------------------
    def test_determine_alert_remediation_with_open_pr(self):
        alert = {
            "number": 101,
            "html_url": "https://github.com/test_owner/test_repo/security/dependabot/101",
            "dependency": {
                "package": {"name": "axios", "ecosystem": "npm"},
                "manifest_path": "package.json",
                "scope": "runtime"
            },
            "security_advisory": {
                "ghsa_id": "GHSA-8hc4-vh64-cxmj",
                "cve_id": "CVE-2020-28168",
                "summary": "SSRF in axios",
                "severity": "high",
                "cvss": {"score": 7.5}
            },
            "security_vulnerability": {
                "vulnerable_version_range": "< 0.21.1",
                "first_patched_version": {"identifier": "0.21.1"}
            }
        }
        open_prs = [
            {
                "number": 14,
                "title": "Bump axios from 0.21.0 to 0.21.1",
                "head": {"ref": "dependabot/npm_and_yarn/axios-0.21.1"},
                "user": {"login": "dependabot[bot]"}
            }
        ]

        rem = self.agent.determine_alert_remediation(alert, open_prs=open_prs)
        self.assertEqual(rem["strategy"], "MERGE_DEPENDABOT_PR")
        self.assertEqual(rem["associated_pr"], 14)
        self.assertEqual(rem["package_name"], "axios")
        self.assertEqual(rem["severity"], "high")

    def test_determine_alert_remediation_patch_upgrade(self):
        alert = {
            "number": 102,
            "dependency": {
                "package": {"name": "urllib3", "ecosystem": "pip"},
                "manifest_path": "requirements.txt",
                "scope": "runtime"
            },
            "security_advisory": {
                "ghsa_id": "GHSA-v845-jxx5-vc9f",
                "cve_id": "CVE-2023-45803",
                "summary": "urllib3 Cookie Request Header Leak",
                "severity": "medium",
                "cvss": {"score": 5.3}
            },
            "security_vulnerability": {
                "vulnerable_version_range": "< 2.0.7",
                "first_patched_version": {"identifier": "2.0.7"}
            }
        }

        rem = self.agent.determine_alert_remediation(alert, open_prs=[])
        self.assertEqual(rem["strategy"], "PATCH_UPGRADE")
        self.assertEqual(rem["target_version"], "2.0.7")
        self.assertIn("pip install urllib3==2.0.7", rem["command"])

    def test_determine_alert_remediation_major_upgrade(self):
        alert = {
            "number": 103,
            "dependency": {
                "package": {"name": "react", "ecosystem": "npm"},
                "manifest_path": "package.json",
                "scope": "runtime"
            },
            "security_advisory": {
                "ghsa_id": "GHSA-xxxx-xxxx-xxxx",
                "summary": "Critical issue in react 17",
                "severity": "critical",
                "cvss": {"score": 9.1}
            },
            "security_vulnerability": {
                "vulnerable_version_range": "< 18.0.0",
                "first_patched_version": {"identifier": "18.2.0"}
            }
        }

        rem = self.agent.determine_alert_remediation(alert, open_prs=[])
        self.assertEqual(rem["strategy"], "MAJOR_UPGRADE")
        self.assertEqual(rem["target_version"], "18.2.0")

    def test_determine_alert_remediation_transitive_lockfile(self):
        alert = {
            "number": 104,
            "dependency": {
                "package": {"name": "semver", "ecosystem": "npm"},
                "manifest_path": "package-lock.json",
                "scope": "runtime"
            },
            "security_advisory": {
                "ghsa_id": "GHSA-c2qf-rxjj-qqgw",
                "summary": "ReDoS vulnerability in semver",
                "severity": "high"
            },
            "security_vulnerability": {
                "vulnerable_version_range": "< 7.5.2",
                "first_patched_version": {"identifier": "7.5.2"}
            }
        }

        rem = self.agent.determine_alert_remediation(alert, open_prs=[])
        self.assertEqual(rem["strategy"], "TRANSITIVE_LOCKFILE_UPDATE")
        self.assertEqual(rem["command"], "npm audit fix")

    def test_determine_alert_remediation_dev_dependency_no_patch(self):
        alert = {
            "number": 105,
            "dependency": {
                "package": {"name": "legacy-test-tool", "ecosystem": "npm"},
                "manifest_path": "package.json",
                "scope": "development"
            },
            "security_advisory": {
                "ghsa_id": "GHSA-unpatched-dev",
                "summary": "Unpatched dev tool vulnerability",
                "severity": "low"
            },
            "security_vulnerability": {
                "vulnerable_version_range": "*",
                "first_patched_version": None
            }
        }

        rem = self.agent.determine_alert_remediation(alert, open_prs=[])
        self.assertEqual(rem["strategy"], "DEV_DEPENDENCY_RISK_ACCEPTANCE")
        self.assertEqual(rem["target_version"], "None Available")

    def test_determine_alert_remediation_unpatched_runtime_workaround(self):
        alert = {
            "number": 106,
            "dependency": {
                "package": {"name": "vulnerable-lib", "ecosystem": "pip"},
                "manifest_path": "requirements.txt",
                "scope": "runtime"
            },
            "security_advisory": {
                "ghsa_id": "GHSA-zero-day",
                "summary": "Zero-day vulnerability",
                "severity": "critical"
            },
            "security_vulnerability": {
                "vulnerable_version_range": "*",
                "first_patched_version": None
            }
        }

        rem = self.agent.determine_alert_remediation(alert, open_prs=[])
        self.assertEqual(rem["strategy"], "WORKAROUND_OR_MITIGATION")
        self.assertEqual(rem["target_version"], "None Available")

    @patch.object(GitHubHelperAgent, "get_dependabot_alerts")
    def test_assess_dependabot_alerts_aggregation(self, mock_get_alerts):
        mock_get_alerts.return_value = [
            {
                "number": 1,
                "dependency": {"package": {"name": "a", "ecosystem": "npm"}, "manifest_path": "package.json"},
                "security_advisory": {"severity": "critical", "summary": "Vuln A"},
                "security_vulnerability": {"vulnerable_version_range": "< 1.0", "first_patched_version": {"identifier": "1.0.1"}}
            },
            {
                "number": 2,
                "dependency": {"package": {"name": "b", "ecosystem": "pip"}, "manifest_path": "requirements.txt"},
                "security_advisory": {"severity": "high", "summary": "Vuln B"},
                "security_vulnerability": {"vulnerable_version_range": "< 2.0", "first_patched_version": {"identifier": "2.0.1"}}
            }
        ]

        summary = self.agent.assess_dependabot_alerts("test_repo", verbose=False)
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["critical"], 1)
        self.assertEqual(summary["high"], 1)
        self.assertEqual(len(summary["alerts"]), 2)

    def test_dismiss_dependabot_alert(self):
        # Invalid reason check
        res_invalid = self.agent.dismiss_dependabot_alert("test_repo", 1, reason="invalid_reason")
        self.assertFalse(res_invalid)

        # Dry-run valid dismissal
        res_valid = self.agent.dismiss_dependabot_alert("test_repo", 1, reason="tolerable_risk")
        self.assertTrue(res_valid)

    @patch.object(GitHubHelperAgent, "get_all_repositories")
    @patch.object(GitHubHelperAgent, "process_repository")
    def test_scan_and_fix_all_aggregates_summaries(self, mock_proc, mock_get_all):
        mock_get_all.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        mock_proc.side_effect = [
            {"issues_count": 1, "prs_count": 0, "alerts_count": 2, "closed_prs": [], "failed_prs": [], "unclosed_prs": [], "closed_issues": [], "failed_issues": [], "unclosed_issues": []},
            {"issues_count": 0, "prs_count": 1, "alerts_count": 0, "closed_prs": [], "failed_prs": [], "unclosed_prs": [], "closed_issues": [], "failed_issues": [], "unclosed_issues": []}
        ]

        summaries = self.agent.scan_and_fix_all()
        self.assertEqual(len(summaries), 2)
        self.assertEqual(summaries["repo1"]["alerts_count"], 2)
        self.assertEqual(summaries["repo2"]["alerts_count"], 0)

if __name__ == "__main__":
    unittest.main()
