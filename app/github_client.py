"""Small GitHub REST API client used by the analyzer."""
import os

import requests

BASE_URL = "https://api.github.com"


def _headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_repository(owner: str, repo: str) -> dict:
    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}",
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def get_contributors(owner: str, repo: str) -> list:
    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}/contributors",
        headers=_headers(),
        params={"per_page": 100},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
