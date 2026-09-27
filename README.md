<div align="center">

# 🔎 Explainable GitHub Issue Recommendation System

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
```

#### 3. Vocabulary Mismatch & Keyword Limitations
Exact keyword searching fails to recognize semantic equivalents (e.g., searching for "Backend" won't match an issue described as "Server-side routing and API endpoints").

#### 4. The Black-Box Recommendation Problem
Existing recommendation systems provide ranked lists without explaining *why* an item was chosen, leaving developers unsure if a task matches their expertise.

---

## 💡 Solution

The Explainable GitHub Issue Recommender automates and personalizes open-source issue discovery by combining:
- **Live Data Integration:** Direct fetching via GitHub REST API.
- **Dense Semantic Vector Matching:** High-dimensional NLP embeddings (`all-MiniLM-L6-v2`) with a robust TF-IDF fallback.
- **Multi-Signal Hybrid Scoring:** Simultaneous evaluation of semantics, skills, technical fit, metadata, recency, and experience difficulty.
- **Transparent Diagnostics:** Full breakdown of scoring metrics and human-readable explanation triggers.
- **Offline Evaluation Suite:** Formal benchmark metrics (Precision@K, Recall@K, MRR, NDCG@K) to measure recommendation quality against ground-truth datasets.

---

## 🎯 End-to-End Workflow

```text
Developer Profile Input
(Skills, Languages, Frameworks, Experience)
        │
        ▼
GitHub API Integration
(Fetch Open Issues from Target Repositories)
        │
        ▼
Semantic Embedding Pipeline
(Sentence-Transformer Encoding / TF-IDF Fallback)
        │
        ▼
Hybrid Compatibility Scoring
┌───────┬───────┬───────┬───────┬───────┐
│ Sem.  │ Skill │ Tech  │ Meta  │ Act.  │
└───┬───┴───┬───┴───┬───┴───┬───┴───┬───┘
    │       │       │       │       │
    └───────┴───────┼───────┴───────┘
                    ▼
            Ranked Recommendations
                    │
                    ▼
        Explainable Output Generation
        (Component Fits & Reason List)
        │
        ▼
Streamlit Interactive Dashboard
```

---

## ✨ Core Features


### 🧠 Hybrid Scoring Engine

The recommendation score combines seven weighted compatibility signals to produce a balanced, multi-dimensional ranking:

| Feature / Signal | Weight | Description |
| :--- | :---: | :--- |
| **Semantic Similarity** | `40%` | Vector cosine similarity between profile embeddings and issue title/body text. |
| **Skill Compatibility** | `20%` | Exact and token overlap between developer skills and issue descriptions. |
| **Technical Compatibility** | `15%` | Overlap in languages, frameworks, tools, and target domains. |
| **Repository Metadata** | `10%` | Popularity metrics including repository stars, forks, and comment activity. |
| **Activity & Recency** | `5%` | Exponential decay scoring based on issue update recency. |
| **Contributor Friendliness** | `5%` | Positive weighting for labels like `good first issue`, `help wanted`, `documentation`. |
| **Experience Alignment** | `5%` | Match between developer experience level (Beginner/Advanced) and issue complexity labels. |

---

### 🗣️ Explainable AI (XAI) Engine

Instead of providing opaque numeric outputs, the system generates actionable insights:

#### Diagnostic Component Scores
```json
{
  "semantic_fit": "82.5%",
  "skill_fit": "75.0%",
  "technical_fit": "100.0%",
  "metadata_score": "68.4%",
  "activity_score": "91.2%"
}
```

#### Human-Readable Reason Triggers
- `✓` *"The repository primarily uses Python, matching a stated language."*
- `✓` *"Flask matches your framework experience."*
- `✓` *"Contributor-friendly labels suggest an accessible entry point."*
- `✓` *"The issue has a difficulty signal compatible with beginner experience."*

---

### 📊 Offline Benchmark & Evaluation

Includes an evaluation module to measure recommendation accuracy against human-labeled relevance matrices:

- **Precision@K:** Fraction of top-K recommended issues that are truly relevant.
- **Recall@K:** Fraction of total relevant issues captured in top-K.
- **MRR (Mean Reciprocal Rank):** Evaluates the position of the first relevant recommendation.
- **NDCG@K:** Discounted Cumulative Gain accounting for rank positions.

---

## 🧠 System Architecture

                     Developer Profile
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
     Skills             Embeddings           Experience
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                       Compatibility
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
    Technical             Metadata             Activity
                             │
                             ▼
                        Hybrid Score
                             │
                             ▼
                  Explainable Output Ranking

---

## 🛠️ Technology Stack

| Category | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Interactive web application and dashboard UI |
| **Backend Core** | Python 3.10+ | Core recommendation logic and pipeline |
| **NLP & Embeddings** | Sentence-Transformers | `all-MiniLM-L6-v2` dense embedding generation |
| **Fallback NLP** | Scikit-Learn | TF-IDF Vectorizer & Cosine Similarity fallback |
| **Data Processing** | Pandas / NumPy | DataFrame manipulations and vector arithmetic |
| **API Client** | Requests | GitHub REST API v3 integration |
| **ML Core** | PyTorch | Deep learning backbone for transformers |

---

## 📂 Project Structure

github_issue_recommender_v2/
│
├── app.py                      # Main Streamlit Dashboard Application
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment configuration
├── .gitignore                  # Git ignore rules
│
├── .streamlit/
│   └── config.toml             # Streamlit UI configuration
│
├── src/
│   ├── __init__.py             # Package initializer
│   ├── models.py               # Dataclasses (DeveloperProfile, Issue, Recommendation)
│   ├── recommender.py          # Hybrid scoring engine & embedding generator
│   ├── github_client.py        # GitHub REST API interaction module
│   └── evaluation.py           # Ranking metrics (Precision@K, MRR, NDCG@K)
│
└── data/
    └── evaluation_template.csv # Evaluation dataset template
```

---

## ⚙️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/KanakDharamthok/github_issue_recommender_v2.git
cd github_issue_recommender_v2
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Environment
#### Windows (PowerShell):
```powershell
.venv\Scripts\activate
```
#### Linux / macOS:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env` and add your GitHub Personal Access Token to avoid API rate limits:
```bash
cp .env.example .env
```
In `.env`:
```env
GITHUB_TOKEN=your_github_personal_access_token_here
```

---

## ▶️ Running the Project

Launch the application using Streamlit:
```bash
streamlit run app.py
```

> **Note:** On first startup, the application will automatically download the `all-MiniLM-L6-v2` transformer model weights.

---

## 🔮 Future Enhancements

- **RAG Architecture Integration:** Incorporating Retrieval-Augmented Generation over full repository document sets.
- **Dynamic LLM Explanations:** Generating free-form natural language rationales via local LLM inference (Ollama/Gemma2).
- **Task Effort Prediction:** Machine learning estimation of issue resolution time/complexity.
- **Progressive Contribution Roadmap:** Recommending stepped issue paths (Beginner → Intermediate → Architecture) for repository onboarding.

---

## 🤝 Contributions

Contributions, suggestions, and pull requests are warmly welcomed!

### Contribution Workflow

Fork Repository
       ↓
Create Feature Branch
       ↓
Implement Feature / Fix
       ↓
Commit Changes
       ↓
Submit Pull Request
       ↓
Review & Merge

---

## 📬 Contact

👨‍💻 **Developer:** Kanak Dharamthok  
📧 **Email:** ms.kanak.dharamthok@gmail.com  
🐙 **GitHub:** [https://github.com/KanakDharamthok](https://github.com/KanakDharamthok)  
💼 **Domain:** AI/ML • Recommendation Systems • NLP • Software Engineering  

---

## ⭐ Support

If you find this project helpful or inspiring:
- ⭐ **Star** this repository
- 🍴 **Fork** it to build your own extensions
- 🤝 **Contribute** fixes or features
- 📢 **Share** it with fellow developers

---

<div align="center">

### 🔎 Explainable GitHub Issue Recommendation System
*Transforming Open-Source Contribution Discovery through Artificial Intelligence.*

</div>
