import math

def precision_at_k(relevance):
    return sum(relevance)/len(relevance) if relevance else 0.0

def recall_at_k(relevance,total_relevant):
    return min(1.0,sum(relevance)/total_relevant) if total_relevant else 0.0

def mrr(relevance):
    for i,x in enumerate(relevance,1):
        if x: return 1.0/i
    return 0.0

def ndcg_at_k(relevance):
    if not relevance: return 0.0
    dcg=sum((2**r-1)/math.log2(i+1) for i,r in enumerate(relevance,1))
    ideal=sorted(relevance,reverse=True)
    idcg=sum((2**r-1)/math.log2(i+1) for i,r in enumerate(ideal,1))
    return dcg/idcg if idcg else 0.0
