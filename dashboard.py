"""Interactive Streamlit dashboard for repository health research."""
import requests
import streamlit as st

from app.analyzer import analyze_repository
from app.github_client import get_contributors, get_repository
from app.security import scan_dependency

st.set_page_config(
    page_title="OpenSource Health Analyzer",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 OpenSource Health Analyzer")
st.caption("Explore GitHub repository maintenance signals and known dependency vulnerabilities.")
st.info(
    "The health score is an experimental heuristic, not a validated security or quality rating. "
    "A repository's popularity does not prove that it is safe or well maintained."
)

with st.sidebar:
    st.header("Repository")
    repository_input = st.text_input(
        "GitHub owner/repository",
        value="fastapi/fastapi",
        help="Example: pallets/flask",
    ).strip().strip("/")
    analyze_clicked = st.button("Analyze repository", type="primary", use_container_width=True)

if analyze_clicked:
    parts = repository_input.split("/")
    if len(parts) != 2 or not all(parts):
        st.error("Enter a repository in owner/repository format, such as fastapi/fastapi.")
    else:
        owner, repo_name = parts
        with st.spinner(f"Fetching {owner}/{repo_name} from GitHub..."):
            try:
                repository = get_repository(owner, repo_name)
                contributors = get_contributors(owner, repo_name)
                analysis = analyze_repository(repository, contributors)
                st.session_state["repository_result"] = repository
                st.session_state["analysis_result"] = analysis
                st.session_state["contributors_result"] = contributors
            except requests.HTTPError as exc:
                status = exc.response.status_code if exc.response is not None else "unknown"
                st.error(f"GitHub returned HTTP {status}. Check the repository name or API rate limit.")
            except requests.RequestException as exc:
                st.error(f"Could not contact GitHub: {exc}")
            except (KeyError, ValueError) as exc:
                st.error(f"Could not analyze this GitHub response: {exc}")

repository = st.session_state.get("repository_result")
analysis = st.session_state.get("analysis_result")

if repository and analysis:
    metrics = analysis["metrics"]
    st.subheader(repository.get("full_name", "Repository"))
    if repository.get("html_url"):
        st.markdown(f"[View on GitHub]({repository['html_url']})")
    if repository.get("description"):
        st.write(repository["description"])

    score_col, stars_col, forks_col, contributors_col = st.columns(4)
    score_col.metric("Health heuristic", f"{analysis['health_score']}/100")
    stars_col.metric("Stars", f"{metrics['stars']:,}")
    forks_col.metric("Forks", f"{metrics['forks']:,}")
    contributors_col.metric("Contributors returned", f"{metrics['contributors']:,}")

    st.progress(analysis["health_score"] / 100, text="Experimental repository health score")
    st.caption(analysis["score_note"])

    st.subheader("Maintenance indicators")
    left, right = st.columns(2)
    with left:
        st.write(f"**Last updated:** {metrics['days_since_update']} days ago")
        st.write(f"**Archived:** {'Yes' if metrics['archived'] else 'No'}")
        st.write(f"**License detected:** {'Yes' if metrics['has_license'] else 'No'}")
    with right:
        st.write(f"**Description present:** {'Yes' if metrics['has_description'] else 'No'}")
        st.write(f"**Default branch:** {repository.get('default_branch', 'Not reported')}")
        st.write(f"**Open issues:** {repository.get('open_issues_count', 'Not reported'):,}")

    with st.expander("View raw repository details"):
        st.json({
            "full_name": repository.get("full_name"),
            "created_at": repository.get("created_at"),
            "updated_at": repository.get("updated_at"),
            "license": repository.get("license"),
            "language": repository.get("language"),
            "topics": repository.get("topics", []),
        })

st.divider()
st.header("Dependency vulnerability lookup")
st.write("Check a specific package version against advisories indexed by OSV.dev.")
with st.form("dependency_scan"):
    c1, c2, c3 = st.columns(3)
    ecosystem = c1.selectbox("Ecosystem", ["PyPI", "npm", "Go", "Maven", "crates.io", "RubyGems"])
    package = c2.text_input("Package name", placeholder="requests")
    version = c3.text_input("Exact version", placeholder="2.31.0")
    scan_clicked = st.form_submit_button("Check vulnerabilities", type="primary")

if scan_clicked:
    if not package.strip() or not version.strip():
        st.warning("Enter both a package name and an exact version.")
    else:
        with st.spinner("Querying OSV.dev..."):
            try:
                scan = scan_dependency(ecosystem, package.strip(), version.strip())
                count = scan["vulnerability_count"]
                if count:
                    st.warning(f"{count} advisory/advisories returned by OSV.dev.")
                    for item in scan["vulnerabilities"]:
                        st.markdown(f"**{item.get('id', 'Unknown ID')}** — {item.get('summary') or 'No summary provided'}")
                        if item.get("aliases"):
                            st.caption("Aliases: " + ", ".join(item["aliases"]))
                else:
                    st.success("OSV.dev returned no known advisories for this exact package version.")
                st.caption("A clean result is not proof that a package is secure; coverage and advisory data can be incomplete.")
            except requests.RequestException as exc:
                st.error(f"OSV.dev request failed: {exc}")

st.divider()
st.caption("Research tool • Data fetched from GitHub REST API and OSV.dev at query time.")
