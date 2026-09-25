import os
import sys
import unittest

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from test_github_helper_agent import TestGitHubHelperAgent

if __name__ == "__main__":
    unittest.main()
