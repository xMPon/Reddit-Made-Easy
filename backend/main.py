# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from . import models, schemas, crud, reddit_client
from .config import DATABASE_URL
import uvicorn
import os

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple keyword extraction for MVP
def extract_keywords(text):
    # Naive: split on spaces, filter stopwords, return top N
    stopwords = set(['the','and','for','with','that','this','from','are','was','but','not','can','all','has','have','will','you','your','about','into','more','than','their','they','them','who','what','when','where','which','how','why','also','any','use','one','our','out','get','just','now','new','like','some','see','had','its','too','may','his','her','she','him','been','were','did','does','each','other','such','only','very','over','most','many','these','those','then','there','because','could','should','would','after','before','while','during','between','under','above','again','still','even','off','on','in','at','by','to','of','as','is','it','an','or','if','be','do','so','no','up','down','over','under','my','me','i','a'])
    words = [w.strip('.,!?()[]{}:;"').lower() for w in text.split()]
    keywords = [w for w in words if w and w not in stopwords and len(w) > 2]
    freq = {}
    for w in keywords:
        freq[w] = freq.get(w, 0) + 1
    sorted_kw = sorted(freq, key=freq.get, reverse=True)
    return sorted_kw[:8]  # top 8 keywords

@app.post('/projects', response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = crud.create_project(db, project.name, project.description)
    # Extract intents (MVP: one intent cluster with top keywords)
    keywords = extract_keywords(project.description)
    crud.create_project_intent(db, db_project.id, label='main', keywords=keywords)
    return db_project

@app.post('/projects/{project_id}/discover-subreddits')
def discover_subreddits(project_id: int, req: schemas.SubredditDiscoveryRequest = None, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    intent = db.query(models.ProjectIntent).filter(models.ProjectIntent.project_id == project_id).first()
    if not intent:
        raise HTTPException(status_code=404, detail='No intents found')
    rc = reddit_client.RedditClient()
    max_subreddits = req.max_subreddits if req else 20
    found = rc.search_subreddits(' '.join(intent.keywords), limit=max_subreddits)
    results = []
    for sr in found:
        # MVP: fake scores and promo_tag
        relevance_score = 1.0
        activity_score = float(sr.subscribers) if hasattr(sr, 'subscribers') else 0.0
        promo_tag = 'yellow'
        sub = crud.create_project_subreddit(db, project_id, sr.display_name, relevance_score, activity_score, promo_tag)
        results.append(sub)
    return results

@app.get('/projects/{project_id}/subreddits', response_model=list[schemas.ProjectSubreddit])
def get_subreddits(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.ProjectSubreddit).filter(models.ProjectSubreddit.project_id == project_id).all()

@app.get('/projects/{project_id}/posts', response_model=list[schemas.MonitoredPost])
def get_posts(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.MonitoredPost).filter(models.MonitoredPost.project_id == project_id).all()

if __name__ == '__main__':
    uvicorn.run('backend.main:app', host='0.0.0.0', port=int(os.getenv('PORT', 8000)), reload=True)
