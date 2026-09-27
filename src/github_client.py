import requests
from typing import List
from .models import Issue

class GitHubClient:
    BASE_URL = "https://api.github.com"
    def __init__(self, token=None, timeout=20):
        self.timeout = timeout
        self.headers = {
            "Accept":"application/vnd.github+json",
            "X-GitHub-Api-Version":"2022-11-28",
            "User-Agent":"Explainable-GitHub-Issue-Recommender"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def _get(self, url, params=None):
        r = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
        if r.status_code == 403:
            raise RuntimeError("GitHub API rate limit reached. Add a GitHub token and retry.")
        r.raise_for_status()
        return r.json()

    def get_repository_issues(self, full_name: str, per_page=30) -> List[Issue]:
        repo = self._get(f"{self.BASE_URL}/repos/{full_name}")
        raw = self._get(f"{self.BASE_URL}/repos/{full_name}/issues",
                        params={"state":"open","per_page":per_page,"sort":"updated","direction":"desc"})
        issues=[]
        for x in raw:
            if "pull_request" in x:
                continue
            issues.append(Issue(
                repository=full_name, number=x["number"], title=x.get("title",""),
                body=x.get("body") or "", labels=[z.get("name","") for z in x.get("labels",[]) if z.get("name")],
                language=repo.get("language") or "Unknown", stars=repo.get("stargazers_count",0),
                forks=repo.get("forks_count",0), open_issues=repo.get("open_issues_count",0),
                updated_at=x.get("updated_at",""), created_at=x.get("created_at",""),
                comments=x.get("comments",0), state=x.get("state","open"), html_url=x.get("html_url","")
            ))
        return issues
