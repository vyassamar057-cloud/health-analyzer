# OpenSource Health Analyzer

A research-oriented Python project for exploring open-source repository maintenance signals and known dependency vulnerabilities.

> **Status:** Early development. The health score is a transparent heuristic for experimentation, not a validated measure of software quality.

## Current capabilities

- Fetch public repository metadata and contributor counts from the GitHub REST API.
- Calculate a 0–100 heuristic score from update recency, contributor count, license, description, stars, forks, and archived status.
- Expose repository analysis through a FastAPI endpoint.
- Query the OSV.dev API for known vulnerabilities affecting an exact package version.

## Project structure

```text
health-analyzer/
├── app/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── github_client.py
│   ├── main.py
│   └── security.py
├── tests/
│   ├── __init__.py
│   └── test_analyzer.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Setup

Requires Python 3.10 or newer.

```bash
git clone https://github.com/vyassamar057-cloud/health-analyzer.git
cd health-analyzer
python -m venv .venv
```

Activate the virtual environment:

- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Install dependencies and run the tests:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation at http://127.0.0.1:8000/docs.

## API examples

Analyze a public GitHub repository:

```text
GET /analyze/fastapi/fastapi
```

Check a package version against OSV (example: requests 2.31.0):

```text
GET /security/PyPI/requests/2.31.0
```

The security endpoint accepts the ecosystem, package name, and exact version as path parameters. OSV results reflect the advisories available from OSV.dev at query time.

## Health-score methodology

The score adds fixed points for these observable signals:

| Signal | Points |
|---|---:|
| Updated within 90 days | 20 |
| At least 5 contributors | 15 |
| License detected | 15 |
| Description present | 10 |
| At least 100 stars | 15 |
| At least 20 forks | 10 |
| Repository is not archived | 15 |
| **Total** | **100** |

These thresholds are intentionally simple and should not be interpreted as proof that a repository is secure, actively maintained, or high quality. Stars and forks are popularity signals, not direct quality measures.

## Configuration

For higher GitHub API rate limits, optionally set a personal access token in the `GITHUB_TOKEN` environment variable. Never commit tokens or other secrets.

## Research direction

Potential next steps include historical trend analysis, dependency-file parsing, richer security metadata, reproducible evaluation datasets, and a dashboard for comparing repositories.

## License

MIT. See [LICENSE](LICENSE).
