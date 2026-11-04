# OpenSource Health Analyzer

An open-source Python research platform for analyzing GitHub repository health, maintenance activity, community participation, and software supply-chain security.

## Project Goals

- Analyze open-source repository activity.
- Study contributor participation.
- Evaluate repository maintenance indicators.
- Investigate software dependency vulnerabilities.
- Generate research-oriented reports.

## Technology

- Python
- FastAPI
- GitHub REST API
- OSV Vulnerability API
- Pandas
- Streamlit
- Pytest

## Current Features

- Repository metadata collection
- Contributor statistics
- Basic repository health scoring
- REST API for repository analysis
- Automated tests

## Installation

```bash
git clone https://github.com/vyassamar057-cloud  /opensource-health-analyzer.git

cd opensource-health-analyzer

pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000/docs

## Research Direction

The project aims to investigate open-source software sustainability, maintenance quality, community activity, and dependency security.

## Project Status

Early development. Contributions and suggestions are welcome.

## License

MIT
