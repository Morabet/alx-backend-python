#!/usr/bin/env python3
""" A module for testing the utils module"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock, MagicMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import HTTPError
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """ Tests the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get: MagicMock) -> None:
        """ Tests the org method"""
        client = GithubOrgClient(org_name)
        expected_argument = client.ORG_URL.format(org=org_name)
        client.org
        mock_get.assert_called_once_with(expected_argument)

    def test_public_repos_url(self) -> None:
        """ Tests the _public_repos_url property"""
        expected_url = "https://api.github.com/users/google/repos"
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': expected_url
            }
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get: MagicMock) -> None:
        """ Tests the public_repos method"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
                    "name": "episodes.dart",
                    "full_name": "google/episodes.dart",
                    "private": False, },
                {
                    "id": 7776515,
                    "node_id": "MDEwOlJlcG9zaXRvcnk3Nzc2NTE1",
                    "name": "cpp-netlib",
                    "full_name": "google/cpp-netlib",
                    "private": False,
                }
            ]
        }

        mock_get.return_value = test_payload['repos']
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:

            mock_repos_url.return_value = test_payload['repos_url']
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), [
                             "episodes.dart", "cpp-netlib"])
            mock_repos_url.assert_called_once()
            mock_get.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}},
         "my_license", False)
    ])
    def test_has_license(
        self, repo: Dict,
        license_key: str, expected_value: bool
    ) -> None:
        """ Tests the has_license method"""
        client = GithubOrgClient("google")
        client_has_licence = client.has_license(repo, license_key)
        self.assertEqual(client_has_licence, expected_value)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Performs integration tests for the GithubOrgClient class"""

    @classmethod
    def setUpClass(cls) -> None:
        """ Sets up class fixtures"""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """ Tests the public_repos method"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """ Tests the public_repos method with a license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(
            license="apache-2.0"), self.apache2_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """ Removes the class fixtures"""
        cls.get_patcher.stop


if __name__ == '__main__':
    unittest.main()
