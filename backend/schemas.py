# schemas.py
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: str

class Project(BaseModel):
    id: int
    name: str
    description_raw: str
    created_at: datetime
    class Config:
        orm_mode = True

class ProjectIntent(BaseModel):
    id: int
    project_id: int
    label: str
    keywords: Any
    class Config:
        orm_mode = True

class ProjectSubreddit(BaseModel):
    id: int
    project_id: int
    subreddit_name: str
    relevance_score: float
    activity_score: float
    promo_tag: str
    created_at: datetime
    class Config:
        orm_mode = True

class MonitoredPost(BaseModel):
    id: int
    project_id: int
    subreddit_name: str
    reddit_post_id: str
    title: str
    url: str
    author: str
    relevance_score: float
    first_seen_at: datetime
    class Config:
        orm_mode = True

class SubredditDiscoveryRequest(BaseModel):
    max_subreddits: Optional[int] = 20
