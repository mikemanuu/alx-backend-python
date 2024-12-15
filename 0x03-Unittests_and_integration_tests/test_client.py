#!/usr/bin/env python3
"""A module for testing the client module.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class, parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  # Mock get_json
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Define the mock return value for get_json
        mock_get_json.return_value = {"login": org_name}

        # Instantiate the client with the org_name
        client = GithubOrgClient(org_name)

        # Call the org method and capture the result
        result = client.org()

        # Assertions
        # Ensure the return value matches
        self.assertEqual(result, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    def test_public_repos_url(self):
        """Test the _public_repos_url property"""
        # Define a mock payload for GithubOrgClient.org
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos"
        }

        # Patch GithubOrgClient.org and mock its return value
        with patch("client.GithubOrgClient.org", new_callable=property) as mock_org:
            mock_org.return_value = mock_payload

            # Instantiate the client and access the _public_repos_url property
            client = GithubOrgClient("test-org")
            result = client._public_repos_url

            # Assertions
            self.assertEqual(result, mock_payload["repos_url"])
            mock_org.assert_called_once()  # Ensure org is called once


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @patch("client.get_json")  # Mock get_json
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        # Define the payload returned by get_json
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        # Mock the _public_repos_url property
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            # Define the mocked property value
            mock_repos_url.return_value = "https://api.github.com/orgs/test_org/repos"

            # Instantiate the client
            client = GithubOrgClient("test_org")

            # Call the method being tested
            repos = client.public_repos()

            # Assert the results
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test_org/repos"
            )
            mock_repos_url.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method with parameterized inputs"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {"org_payload": org_payload,
     "repos_payload": repos_payload,
     "expected_repos": expected_repos,
     "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up for integration tests."""
        # Mock requests.get
        cls.get_patcher = patch("requests.get")

        # Start the patcher
        cls.mock_get = cls.get_patcher.start()

        # Configure side_effect for requests.get().json()
        def side_effect(url):
            if "orgs/" in url:
                return cls.org_payload
            elif "repos" in url:
                return cls.repos_payload
            return None

        cls.mock_get.return_value.json.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down after integration tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with a specific license."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
