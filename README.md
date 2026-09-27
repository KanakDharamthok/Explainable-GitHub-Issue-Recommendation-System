<div align="center">

# 🔎 Explainable GitHub Issue Recommender V2

## Open-Source Discovery • Semantic Embeddings • Hybrid Scoring • XAI Recommendations

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Sentence-Transformers](https://img.shields.io/badge/Sentence--Transformers-NLP-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow)
![GitHub API](https://img.shields.io/badge/GitHub_API-Data-black)

</div>

---

## 🚀 Project Overview

**Explainable GitHub Issue Recommender V2** is an AI-driven recommendation platform designed to help developers discover open-source GitHub issues tailored precisely to their skills, programming language proficiency, framework experience, and domain interests.

Unlike conventional search mechanisms that rely strictly on keyword matching, this platform employs a **hybrid AI recommendation engine**. It retrieves live open issues via the GitHub API, computes deep semantic vector embeddings using sentence-transformers, evaluates explicit technical compatibility, and incorporates repository metadata (such as stars, forks, recency, and beginner-friendly labels).

Crucially, the system is **Explainable (XAI)**—it exposes granular component fit scores and generates human-readable reasoning for every recommendation, eliminating the "black-box" nature of traditional recommenders.

---

## 🛑 Problem Statement

Developers seeking to contribute to open source face several operational hurdles:

#### 1. Information Overload & Scalability Issues
GitHub hosts millions of repositories with hundreds of thousands of open issues, making manual discovery exhausting and time-consuming.

#### 2. Friction in Manual Navigation
Finding an issue currently requires a tedious manual cycle:
```text
Search Repositories → Filter Issues → Read Descriptions → Verify Tech Stack → Gauge Difficulty
