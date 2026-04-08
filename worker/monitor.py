# monitor.py
# Worker script to monitor subreddits for new relevant posts
import sys
import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from backend import models, reddit_client, config

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

rc = reddit_client.RedditClient()

def main():
    db = SessionLocal()
    try:
        projects = db.query(models.Project).all()
        for project in projects:
            intents = db.query(models.ProjectIntent).filter(models.ProjectIntent.project_id == project.id).all()
            keywords = []
            for intent in intents:
                keywords.extend(intent.keywords)
            subreddits = db.query(models.ProjectSubreddit).filter(models.ProjectSubreddit.project_id == project.id).all()
            for sr in subreddits:
                # Search for new posts in subreddit
                posts = rc.search_posts(sr.subreddit_name, ' '.join(keywords), limit=10)
                for post in posts:
                    # Check if already stored
                    exists = db.query(models.MonitoredPost).filter(models.MonitoredPost.reddit_post_id == post.id).first()
                    if exists:
                        continue
                    # Simple relevance: keyword count in title
                    rel_score = sum(1 for k in keywords if k in post.title.lower())
                    db_post = models.MonitoredPost(
                        project_id=project.id,
                        subreddit_name=sr.subreddit_name,
                        reddit_post_id=post.id,
                        title=post.title,
                        url=post.url,
                        author=post.author.name if post.author else 'unknown',
                        relevance_score=rel_score,
                        first_seen_at=datetime.datetime.utcnow()
                    )
                    db.add(db_post)
        db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    main()
