"""
Unit tests for github_helper_agent.py
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import urllib.error
import io

from github_helper_agent import GitHubHelperAgent, load_dotenv

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

if __name__ == "__main__":
    unittest.main()
