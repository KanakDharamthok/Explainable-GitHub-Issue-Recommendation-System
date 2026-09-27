# Explainable Hybrid GitHub Issue Recommender V2

## Project idea

The project addresses the open-source discovery problem: developers need help finding repositories and issues that match their skills, experience and interests.

**Current scope:** Explainable Hybrid Recommendation System for GitHub Issues.

The system retrieves open GitHub issues, represents the developer and issues semantically, combines semantic similarity with technical and metadata signals, ranks issues, and explains the ranking.

## V2 improvements

- Sentence-transformer semantic embeddings (`all-MiniLM-L6-v2`)
- Skill compatibility
- Language/framework/domain compatibility
- Repository language matching
- Contributor-friendly labels
- Experience-aware signals
- Stars, forks, comments and recency metadata
- Explainable component scores
- Formal evaluation: Precision@K, Recall@K, MRR, NDCG@K
- TF-IDF fallback if embeddings cannot load

## Hybrid score

40% semantic similarity
20% skill compatibility
15% technical compatibility
10% metadata
5% activity/recency
5% contributor friendliness
5% experience compatibility

These are baseline weights, not proven optimal weights. Tune them using labelled data.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The first embedding run downloads the sentence-transformer model.

## Formal evaluation

Create a human-reviewed CSV:

```text
developer_id,issue_url,relevant
dev_1,https://github.com/example/repo/issues/1,1
dev_1,https://github.com/example/repo/issues/2,0
```

Metrics:

- Precision@K — proportion of top-K recommendations that are relevant
- Recall@K — proportion of known relevant issues retrieved in top-K
- MRR — position of the first relevant recommendation
- NDCG@K — ranking quality with higher weight for relevant items near the top

For a proper experiment, keep the same candidate issues and developer profiles when comparing V1 vs V2.

## Suggested experiment

Use 10–20 developer profiles and manually label candidate issues. Compare:

1. TF-IDF baseline
2. Embedding-only
3. Skills + metadata
4. Full hybrid model

Then report Precision@5, Recall@5, MRR and NDCG@5.

## Future work

After this scope is evaluated, possible extensions are RAG over repository documentation/issues, LLM-grounded explanations, issue effort prediction, developer–repository–issue graphs, and progressive contribution pathways.
