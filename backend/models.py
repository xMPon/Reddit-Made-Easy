# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description_raw = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProjectIntent(Base):
    __tablename__ = 'project_intents'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    label = Column(String, nullable=False)
    keywords = Column(JSON, nullable=False)

class ProjectSubreddit(Base):
    __tablename__ = 'project_subreddits'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    subreddit_name = Column(String, nullable=False)
    relevance_score = Column(Float, nullable=False)
    activity_score = Column(Float, nullable=False)
    promo_tag = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MonitoredPost(Base):
    __tablename__ = 'monitored_posts'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    subreddit_name = Column(String, nullable=False)
    reddit_post_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    author = Column(String, nullable=False)
    relevance_score = Column(Float, nullable=False)
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
