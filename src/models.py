from dataclasses import dataclass, field
from typing import List

@dataclass
class DeveloperProfile:
    name: str
    skills: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    experience: str = "Beginner"
    domain: str = ""

@dataclass
class Issue:
    repository: str
    number: int
    title: str
    body: str
    labels: List[str]
    language: str
    stars: int
    forks: int
    open_issues: int
    updated_at: str
    created_at: str
    comments: int
    state: str
    html_url: str = ""

@dataclass
class Recommendation:
    issue: Issue
    score: float
    components: dict
    reasons: List[str]
