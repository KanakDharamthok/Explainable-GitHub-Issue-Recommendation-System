import pandas as pd
import streamlit as st
from src.github_client import GitHubClient
from src.models import DeveloperProfile
from src.recommender import recommend_issues
from src.evaluation import precision_at_k, recall_at_k, mrr, ndcg_at_k

st.set_page_config(page_title="Explainable GitHub Issue Recommender", page_icon="🔎", layout="wide")
st.title("🔎 Explainable GitHub Issue Recommender")
st.caption("Hybrid recommendation using embeddings, skills, technical compatibility, metadata and activity.")

with st.sidebar:
    st.header("Developer Profile")
    name = st.text_input("Name", "Developer")
    skills = st.text_input("Skills", "Python, REST API, Backend Development, SQL")
    languages = st.text_input("Languages", "Python, SQL")
    frameworks = st.text_input("Frameworks / Tools", "FastAPI, Flask, PostgreSQL, Docker")
    experience = st.selectbox("Experience", ["Beginner", "Intermediate", "Advanced"])
    domain = st.text_input("Preferred domain", "Backend, API Development")
    max_results = st.slider("Recommendations", 3, 15, 5)
    st.divider()
    st.header("GitHub Data")
    repositories = st.text_input("Repositories", "tiangolo/fastapi, pallets/flask")
    token = st.text_input("GitHub token (optional)", type="password")
    run = st.button("Generate Recommendations", type="primary", use_container_width=True)

if run:
    profile = DeveloperProfile(
        name=name,
        skills=[x.strip() for x in skills.split(",") if x.strip()],
        languages=[x.strip() for x in languages.split(",") if x.strip()],
        frameworks=[x.strip() for x in frameworks.split(",") if x.strip()],
        experience=experience,
        domain=domain,
    )
    repos = [x.strip() for x in repositories.split(",") if x.strip()]
    client = GitHubClient(token=token or None)
    all_issues = []
    progress = st.progress(0)
    for i, repo in enumerate(repos):
        try:
            all_issues.extend(client.get_repository_issues(repo))
        except Exception as exc:
            st.warning(f"Could not fetch {repo}: {exc}")
        progress.progress((i + 1) / max(len(repos), 1))
    progress.empty()

    if not all_issues:
        st.error("No GitHub issues retrieved. Check repository names, network access or rate limits.")
        st.stop()

    with st.spinner("Computing semantic embeddings and hybrid scores..."):
        recommendations = recommend_issues(profile, all_issues, top_k=max_results)

    st.success(f"Analyzed {len(all_issues)} issues from {len(repos)} repositories.")
    avg = lambda key: sum(x.components[key] for x in recommendations) / len(recommendations)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Candidate Issues", len(all_issues))
    c2.metric("Top-K Avg Match", f"{sum(x.score for x in recommendations)/len(recommendations)*100:.1f}%")
    c3.metric("Avg Semantic Fit", f"{avg('semantic')*100:.1f}%")
    c4.metric("Avg Skill Fit", f"{avg('skill')*100:.1f}%")

    st.subheader("Ranked Recommendations")
    for idx, item in enumerate(recommendations, 1):
        issue = item.issue
        with st.container(border=True):
            a,b = st.columns([5,1])
            a.subheader(f"{idx}. {issue.title}")
            a.caption(f"{issue.repository} • #{issue.number} • {issue.language}")
            b.metric("Match", f"{item.score*100:.1f}%")
            st.write(issue.body[:900] + ("..." if len(issue.body)>900 else ""))
            st.markdown("**Labels:** " + (", ".join(issue.labels) if issue.labels else "None"))
            cols = st.columns(5)
            for col, key, label in zip(cols, ["semantic","skill","technical","metadata","activity"],
                                       ["Semantic","Skills","Technical","Metadata","Activity"]):
                col.metric(label, f"{item.components[key]*100:.0f}%")
            st.markdown("**Why this issue was recommended**")
            for reason in item.reasons:
                st.write("• " + reason)
            if issue.html_url:
                st.link_button("Open GitHub Issue", issue.html_url)

    diagnostics = pd.DataFrame([{
        "Issue": r.issue.title[:80], "Repository": r.issue.repository,
        "Overall": round(r.score*100,1), "Semantic": round(r.components["semantic"]*100,1),
        "Skill": round(r.components["skill"]*100,1), "Technical": round(r.components["technical"]*100,1),
        "Metadata": round(r.components["metadata"]*100,1), "Activity": round(r.components["activity"]*100,1)
    } for r in recommendations])
    st.subheader("Recommendation Diagnostics")
    st.dataframe(diagnostics, use_container_width=True, hide_index=True)

st.divider()
st.subheader("📊 Offline Evaluation")
st.write("Upload manually labelled developer–issue relevance to calculate formal ranking metrics.")
uploaded = st.file_uploader("Evaluation labels CSV", type=["csv"])
if uploaded is not None:
    labels = pd.read_csv(uploaded)
    if not {"issue_url","relevant"}.issubset(labels.columns):
        st.error("CSV must contain issue_url and relevant columns (1=relevant, 0=not relevant).")
    elif run:
        urls = [r.issue.html_url for r in recommendations]
        mapping = {str(row.issue_url): int(row.relevant) for _,row in labels.iterrows()}
        relevance = [mapping.get(url,0) for url in urls]
        total = int(labels["relevant"].sum())
        e1,e2,e3,e4 = st.columns(4)
        e1.metric("Precision@K", f"{precision_at_k(relevance):.3f}")
        e2.metric("Recall@K", f"{recall_at_k(relevance,total):.3f}" if total else "N/A")
        e3.metric("MRR", f"{mrr(relevance):.3f}")
        e4.metric("NDCG@K", f"{ndcg_at_k(relevance):.3f}")
        st.info("These metrics are meaningful only when labels are human-reviewed ground truth.")

st.caption("Current scope: explainable hybrid recommendation for open-source GitHub issues.")
