"""Heuristic repository-health metrics.

The score is an educational heuristic, not a validated measure of project quality.
"""
from datetime import datetime, timezone


def analyze_repository(repo: dict, contributors: list) -> dict:
    """Calculate transparent maintenance indicators for a GitHub repository."""
    updated_at = repo.get("updated_at")
    if not updated_at:
        raise ValueError("Repository response is missing updated_at")

    updated = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    if updated.tzinfo is None:
        updated = updated.replace(tzinfo=timezone.utc)

    days_since_update = max(
        0, (datetime.now(timezone.utc) - updated.astimezone(timezone.utc)).days
    )
    metrics = {
        "stars": int(repo.get("stargazers_count") or 0),
        "forks": int(repo.get("forks_count") or 0),
        "contributors": len(contributors),
        "days_since_update": days_since_update,
        "archived": bool(repo.get("archived", False)),
        "has_license": bool(repo.get("license")),
        "has_description": bool(repo.get("description")),
    }

    score = 0
    score += 20 if days_since_update <= 90 else 0
    score += 15 if metrics["contributors"] >= 5 else 0
    score += 15 if metrics["has_license"] else 0
    score += 10 if metrics["has_description"] else 0
    score += 15 if metrics["stars"] >= 100 else 0
    score += 10 if metrics["forks"] >= 20 else 0
    score += 15 if not metrics["archived"] else 0

    return {
        "health_score": score,
        "score_scale": "0-100",
        "score_note": "Heuristic indicator for research; not a validated quality rating.",
        "metrics": metrics,
    }
