"""Dependency vulnerability lookups using the public OSV API."""
import requests

OSV_QUERY_URL = "https://api.osv.dev/v1/query"


def scan_dependency(ecosystem: str, package: str, version: str) -> dict:
    """Return known OSV advisories for one exact package version."""
    payload = {
        "package": {"name": package, "ecosystem": ecosystem},
        "version": version,
    }
    response = requests.post(OSV_QUERY_URL, json=payload, timeout=20)
    response.raise_for_status()
    data = response.json()
    vulnerabilities = data.get("vulns", [])
    return {
        "ecosystem": ecosystem,
        "package": package,
        "version": version,
        "vulnerability_count": len(vulnerabilities),
        "vulnerabilities": [
            {
                "id": item.get("id"),
                "summary": item.get("summary"),
                "modified": item.get("modified"),
                "aliases": item.get("aliases", []),
            }
            for item in vulnerabilities
        ],
        "source": "OSV.dev",
    }
