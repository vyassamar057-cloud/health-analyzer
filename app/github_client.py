
import os
import requests

BASE_URL = "https://api.github.com"

def get_repository(owner, repo):
    headers = {
        "Accept": "application/vnd.github+json"
    }

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}",
        headers=headers,
        timeout=15
    )
    response.raise_for_status()
    return response.json()


def get_contributors(owner, repo):
    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}/contributors",
        timeout=15
    )
    response.raise_for_status()
    return response.json()
