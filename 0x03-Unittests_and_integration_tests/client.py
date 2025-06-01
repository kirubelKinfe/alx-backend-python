#!/usr/bin/env python3
"""Client module for interacting with GitHub organizations."""

from typing import Dict, List
from utils import get_json


class GithubOrgClient:
    """A client for GitHub organization data."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize with the organization name."""
        self.org_name = org_name

    @property
    def org(self) -> Dict:
        """Retrieve organization data from GitHub API."""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self) -> str:
        """Extract the public repos URL from the org data."""
        return self.org.get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        """Fetch public repo names. Optionally filter by license."""
        repos_data = get_json(self._public_repos_url)
        repo_names = []

        for repo in repos_data:
            if license is None:
                repo_names.append(repo["name"])
            else:
                repo_license = repo.get("license", {}).get("key")
                if repo_license == license:
                    repo_names.append(repo["name"])

        return repo_names
