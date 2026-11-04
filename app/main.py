"""FastAPI service for open-source repository research."""
from fastapi import FastAPI, HTTPException
import requests

from .analyzer import analyze_repository
from .github_client import get_contributors, get_repository
from .security import scan_dependency

app = FastAPI(
    title="OpenSource Health Analyzer",
    description="Research-oriented repository maintenance and dependency-security indicators.",
    version="0.2.0",
)


@app.get("/")
def home():
    return {
        "name": "OpenSource Health Analyzer",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/analyze/{owner}/{repo}")
def analyze(owner: str, repo: str):
    try:
        repository = get_repository(owner, repo)
        contributors = get_contributors(owner, repo)
        result = analyze_repository(repository, contributors)
        return {"repository": repository["full_name"], "health": result}
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 502
        raise HTTPException(status_code=status, detail="GitHub API request failed") from exc
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail="Could not reach GitHub API") from exc
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=f"Invalid GitHub response: {exc}") from exc


@app.get("/security/{ecosystem}/{package}/{version}")
def dependency_security(ecosystem: str, package: str, version: str):
    try:
        return scan_dependency(ecosystem, package, version)
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail="Could not reach OSV vulnerability API") from exc
