#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        expected_result = {"login": org_name, "id": 1234}
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_result)

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns the correct repos_url."""
        expected_url = "https://api.github.com/orgs/testorg/repos"
        mock_org.return_value = {"repos_url": expected_url}

        client = GithubOrgClient("testorg")
        result = client._public_repos_url

        self.assertEqual(result, expected_url)

    @patch('client.get_json')
    @patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test public_repos returns the list of repo names."""
        expected_url = "https://api.github.com/orgs/testorg/repos"
        mock_repos_url.return_value = expected_url

        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = repos_payload

        client = GithubOrgClient("testorg")
        result = client.public_repos()

        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        mock_get_json.assert_called_once_with(expected_url)

    @patch('client.get_json')
    @patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock)
    def test_public_repos_with_license(self, mock_repos_url, mock_get_json):
        """Test public_repos filters repos by license key."""
        mock_repos_url.return_value = "https://api.github.com/orgs/testorg/repos"
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]

        client = GithubOrgClient("testorg")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, ["repo2"])

