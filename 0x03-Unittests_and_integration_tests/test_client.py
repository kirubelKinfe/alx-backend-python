#!/usr/bin/env python3
"""Unit and integration tests for client.GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns the correct repos_url."""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        client = GithubOrgClient("testorg")
        self.assertEqual(client._public_repos_url,
                         "https://api.github.com/orgs/testorg/repos")

    @patch('client.get_json')
    @patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_url, mock_get_json):
        """Test public_repos returns expected repo names."""
        mock_url.return_value = "https://api.github.com/orgs/testorg/repos"
        mock_get_json.return_value = repos_payload
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), expected_repos)
        mock_get_json.assert_called_once()
        mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), [
    (org_payload, repos_payload, expected_repos, apache2_repos),
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get with fixture side effects."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            response = unittest.mock.Mock()
            if url == "https://api.github.com/orgs/testorg":
                response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                response.json.return_value = cls.repos_payload
            return response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test integration of public_repos without license filter."""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test integration of public_repos with license filter."""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
