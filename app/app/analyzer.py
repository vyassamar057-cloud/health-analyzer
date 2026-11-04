
from datetime import datetime, timezone

def analyze_repository(repo, contributors):
    updated = datetime.fromisoformat(
        repo["updated_at"].replace("Z", "+00:00")
    )

    days = (datetime.now(timezone.utc) - updated).days

    metrics = {
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "contributors": len(contributors),
        "days_since_update": days,
        "archived": repo["archived"],
        "has_license": bool(repo.get("license")),
        "has_description": bool(repo.get("description"))
    }

    score = 0
    score += 20 if days <= 90 else 0
    score += 15 if len(contributors) >= 5 else 0
    score += 15 if metrics["has_license"] else 0
    score += 10 if metrics["has_description"] else 0
    score += 15 if metrics["stars"] >= 100 else 0
    score += 10 if metrics["forks"] >= 20 else 0
    score += 15 if not metrics["archived"] else 0

    return {
        "health_score": score,
        "metrics": metrics
    }
