import math, re
from datetime import datetime, timezone
from typing import List
import numpy as np
from .models import DeveloperProfile, Issue, Recommendation

MODEL_NAME="all-MiniLM-L6-v2"
STOPWORDS={"the","and","for","with","from","this","that","issue","should","would","could","into","have","has","are","was","were","been","will"}

def normalize(text):
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9+#.\-\s]"," ",(text or "").lower())).strip()

def tokens(text):
    return {x for x in normalize(text).split() if len(x)>2 and x not in STOPWORDS}

def overlap_score(terms,text):
    t=tokens(text)
    return min(1.0,len(t & terms)/max(len(terms),1))

def phrase_overlap(terms,text):
    text=normalize(text)
    return min(1.0,sum(1 for x in terms if normalize(x) in text)/max(len(terms),1))

def recency_score(updated):
    try:
        dt=datetime.fromisoformat(updated.replace("Z","+00:00"))
        return math.exp(-max((datetime.now(timezone.utc)-dt).days,0)/180)
    except Exception:
        return .3

def contributor_score(labels):
    good={"good first issue","help wanted","documentation","beginner","easy","first timers only"}
    return min(1.0,len({normalize(x) for x in labels}&good)/2)

def experience_score(profile,labels,title):
    text=normalize(" ".join(labels)+" "+title)
    beginner={"good first issue","beginner","documentation","easy","first timers only"}
    advanced={"architecture","breaking change","performance","security","compiler","optimization"}
    if profile.experience=="Beginner": return 1.0 if any(x in text for x in beginner) else .55
    if profile.experience=="Advanced": return 1.0 if any(x in text for x in advanced) else .70
    return .85

def metadata_score(issue):
    stars=min(math.log10(issue.stars+1)/6,1)
    forks=min(math.log10(issue.forks+1)/5,1)
    comments=min(issue.comments/20,1)
    return min(1,.45*stars+.30*forks+.25*comments)

def profile_text(p):
    return f"Skills: {', '.join(p.skills)}. Languages: {', '.join(p.languages)}. Frameworks: {', '.join(p.frameworks)}. Experience: {p.experience}. Domain: {p.domain}."

def issue_text(i):
    return f"Repository: {i.repository}. Language: {i.language}. Title: {i.title}. Labels: {', '.join(i.labels)}. Description: {i.body}"

def semantic_embeddings(profile, issues):
    ptxt=profile_text(profile)
    texts=[issue_text(i) for i in issues]
    try:
        from sentence_transformers import SentenceTransformer
        model=SentenceTransformer(MODEL_NAME)
        emb=model.encode([ptxt]+texts,normalize_embeddings=True,show_progress_bar=False)
        sims=np.dot(emb[1:],emb[0])
        return np.clip((sims+1)/2,0,1)
    except Exception:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        v=TfidfVectorizer(ngram_range=(1,2),stop_words="english")
        m=v.fit_transform([ptxt]+texts)
        return np.clip(cosine_similarity(m[0:1],m[1:]).flatten(),0,1)

def recommend_issues(profile: DeveloperProfile, issues: List[Issue], top_k=8):
    if not issues: return []
    semantic=semantic_embeddings(profile,issues)
    skill_terms=profile.skills
    tech_terms=profile.languages+profile.frameworks
    domain_terms=[x.strip() for x in re.split(r"[,/]",profile.domain) if x.strip()]
    langs={normalize(x) for x in profile.languages}
    results=[]
    for i,issue in enumerate(issues):
        text=issue_text(issue)
        skill=max(overlap_score(tokens(" ".join(profile.skills)),text),phrase_overlap(profile.skills,text))
        tech=max(overlap_score(tokens(" ".join(tech_terms)),text),phrase_overlap(tech_terms,text))
        domain=max(overlap_score(tokens(" ".join(domain_terms)),text),phrase_overlap(domain_terms,text))
        lang=1.0 if normalize(issue.language) in langs else 0.0
        technical=min(1,.55*tech+.30*lang+.15*domain)
        metadata=metadata_score(issue)
        activity=recency_score(issue.updated_at)
        contributor=contributor_score(issue.labels)
        experience=experience_score(profile,issue.labels,issue.title)

        score=(.40*semantic[i]+.20*skill+.15*technical+.10*metadata+.05*activity+.05*contributor+.05*experience)

        reasons=[]
        if semantic[i]>=.55: reasons.append("The issue is semantically aligned with the developer profile.")
        if skill>=.25: reasons.append("The issue contains skills that overlap with the developer profile.")
        if lang: reasons.append(f"The repository primarily uses {issue.language}, matching a stated language.")
        if technical>=.40: reasons.append("Repository technology and developer tools show technical compatibility.")
        if domain>=.25: reasons.append("The issue overlaps with the developer's preferred domain.")
        if contributor>0: reasons.append("Contributor-friendly labels suggest an accessible entry point.")
        if activity>=.65: reasons.append("The issue has been updated relatively recently.")
        if experience>=.85: reasons.append(f"The issue has a difficulty signal compatible with {profile.experience.lower()} experience.")
        if not reasons: reasons.append("The recommendation is produced from the combined hybrid score.")

        results.append(Recommendation(issue,float(score),{
            "semantic":float(semantic[i]),"skill":float(skill),"technical":float(technical),
            "metadata":float(metadata),"activity":float(activity),
            "contributor":float(contributor),"experience":float(experience)},reasons))
    return sorted(results,key=lambda x:x.score,reverse=True)[:top_k]
