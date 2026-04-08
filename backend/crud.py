# crud.py
from sqlalchemy.orm import Session
from . import models

def create_project(db: Session, name: str, description: str):
    project = models.Project(name=name, description_raw=description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def create_project_intent(db: Session, project_id: int, label: str, keywords):
    intent = models.ProjectIntent(project_id=project_id, label=label, keywords=keywords)
    db.add(intent)
    db.commit()
    db.refresh(intent)
    return intent

def create_project_subreddit(db: Session, project_id: int, subreddit_name: str, relevance_score: float, activity_score: float, promo_tag: str):
    subreddit = models.ProjectSubreddit(
        project_id=project_id,
        subreddit_name=subreddit_name,
        relevance_score=relevance_score,
        activity_score=activity_score,
        promo_tag=promo_tag
    )
    db.add(subreddit)
    db.commit()
    db.refresh(subreddit)
    return subreddit

def create_monitored_post(db: Session, project_id: int, subreddit_name: str, reddit_post_id: str, title: str, url: str, author: str, relevance_score: float):
    post = models.MonitoredPost(
        project_id=project_id,
        subreddit_name=subreddit_name,
        reddit_post_id=reddit_post_id,
        title=title,
        url=url,
        author=author,
        relevance_score=relevance_score
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
