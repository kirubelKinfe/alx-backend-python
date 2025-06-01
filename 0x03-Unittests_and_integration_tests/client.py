#!/usr/bin/env python3
"""GitHub client module."""

from typing import Dict, List
from utils import get_json


class GithubOrgClient:
    """Client for interacting with GitHub organizations."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize with org name."""
        self.org_name = org_name

    @property
    def org(self) -> Dict:
        """Get organization details."""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self) -> str:
        """Extract public repos URL from org."""
        return self.org.get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        """Return list of public repo names, filtered by license if specified."""
        repos = get_json(self._public_repos_url)
        names = []
        for repo in repos:
            if license is None or (repo.get("license") or {}).get("key") == license:
                names.append(repo["name"])
        return names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repo has a specific license."""
        return (repo.get("license") or {}).get("key") == license_key
