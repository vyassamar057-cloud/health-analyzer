from datetime import datetime, timedelta, timezone

from app.analyzer import analyze_repository


def sample_repo(**overrides):
    repo = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "stargazers_count": 500,
        "forks_count": 100,
        "archived": False,
        "description": "Test project",
        "license": {"key": "mit"},
    }
    repo.update(overrides)
    return repo


def test_healthy_repository_reaches_maximum_score():
    result = analyze_repository(sample_repo(), [{"login": f"user{i}"} for i in range(5)])
    assert result["health_score"] == 100
    assert result["metrics"]["contributors"] == 5


def test_archived_repository_loses_active_maintenance_points():
    result = analyze_repository(sample_repo(archived=True), [])
    assert result["health_score"] == 70
    assert result["metrics"]["archived"] is True


def test_old_repository_update_loses_recency_points():
    old_date = (datetime.now(timezone.utc) - timedelta(days=180)).isoformat()
    result = analyze_repository(sample_repo(updated_at=old_date), [])
    assert result["health_score"] == 65
    assert result["metrics"]["days_since_update"] >= 180


def test_missing_license_and_description_are_reported():
    result = analyze_repository(
        sample_repo(license=None, description=None), []
    )
    assert result["metrics"]["has_license"] is False
    assert result["metrics"]["has_description"] is False
