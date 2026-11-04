# OpenSource Health Analyzer

A research-oriented Python project for exploring open-source repository maintenance signals and known dependency vulnerabilities.

> **Status:** Early development. The health score is a transparent heuristic for experimentation, not a validated measure of software quality.

## Features

- Fetch public repository metadata and contributor counts from GitHub.
- Calculate a transparent 0–100 heuristic from update recency, contributor count, license, description, stars, forks, and archived status.
- Interactive Streamlit dashboard for repository analysis.
- FastAPI endpoints for programmatic analysis.
- Query OSV.dev for known vulnerabilities affecting an exact package version.

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
├── .github/workflows/tests.yml
├── dashboard.py
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

Install dependencies and run tests:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Launch the web dashboard

```bash
streamlit run dashboard.py
```

Streamlit will print a local address, usually http://localhost:8501. Enter a GitHub repository as `owner/repository`, for example `fastapi/fastapi`. The dashboard displays repository metadata, maintenance indicators, the experimental score, and an OSV dependency lookup form.

## Run the API

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation at http://127.0.0.1:8000/docs.

### API examples

```text
GET /analyze/fastapi/fastapi
GET /security/PyPI/requests/2.31.0
```

## Health-score methodology

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

These thresholds are intentionally simple and should not be interpreted as proof that a repository is secure, actively maintained, or high quality. Stars and forks are popularity signals, not direct quality measures. The contributor count is based on the first 100 contributors returned by GitHub's API.

## Configuration

For higher GitHub API rate limits, optionally set a personal access token in the `GITHUB_TOKEN` environment variable. Never commit tokens or other secrets.

## Data sources and limitations

- Repository information comes from the GitHub REST API.
- Dependency advisories come from OSV.dev.
- Results reflect the data available at query time and may be incomplete.
- A package with no returned advisories is not guaranteed to be vulnerability-free.
- This project is an educational research tool, not a security certification service.

## License

MIT. See [LICENSE](LICENSE).
