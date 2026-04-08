# Reddit Made Easy - Reddit Assistant Project

A lightweight Reddit discovery and monitoring tool that helps identify relevant subreddits and track new posts related to a product or idea.

## Tech Stack

- **Backend:** Python + FastAPI
- **Reddit Client:** PRAW (Python Reddit API Wrapper)
- **Database:** Postgres via SQLAlchemy
- **Worker:** Plain Python script triggered by cron 3 times a day
- **Frontend:** React app

## Project Goal

The goal of this project is to:

- Accept a product description
- Extract useful keywords and intent clusters
- Discover relevant subreddits
- Monitor those subreddits for relevant new posts
- Store those posts for review inside the app

This MVP is intentionally minimal and does not include auth or advanced automation.

## Folder Structure

```text
reddit-assistant/
  backend/
    main.py              # FastAPI app
    models.py            # SQLAlchemy models
    schemas.py           # Pydantic request/response models
    reddit_client.py     # PRAW wrapper
    config.py            # Env vars (DB URL, Reddit creds)
    crud.py              # DB access helpers
  worker/
    monitor.py           # Worker script run by cron
  alembic/               # Optional: database migrations
  .env                   # Local secrets (ignored in git)
  requirements.txt
```

## Core Data Model (MVP)

### `projects`

Stores the raw project or product input.

```text
projects
  id (pk)
  name
  description_raw
  created_at
```

### `project_intents`

Stores extracted keyword or intent clusters for each project.

```text
project_intents
  id (pk)
  project_id (fk)
  label
  keywords (jsonb)
```

Example `label`:
- `cash flow management`
- `startup runway`
- `budget forecasting`

### `project_subreddits`

Stores subreddit recommendations for each project.

```text
project_subreddits
  id (pk)
  project_id (fk)
  subreddit_name
  relevance_score
  activity_score
  promo_tag
  created_at
```

Example `promo_tag` values:

- `green`
- `yellow`
- `red`

### `monitored_posts`

Stores relevant Reddit posts discovered by the worker.

```text
monitored_posts
  id (pk)
  project_id (fk)
  subreddit_name
  reddit_post_id
  title
  url
  author
  relevance_score
  first_seen_at
```

## API Endpoints

### `POST /projects`

Create a new project.

**Input**

```json
{
  "name": "string",
  "description": "string"
}
```

**What it does**

- Stores the project
- Runs simple NLP to extract keyword and intent clusters

**Response**

- Project object
- Extracted intents

---

### `POST /projects/{id}/discover-subreddits`

Discover relevant subreddits for a project.

**Input (optional)**

```json
{
  "max_subreddits": 20
}
```

**What it does**

- Builds search queries from stored intents
- Uses PRAW subreddit search to find candidates
- Scores and stores subreddit matches in `project_subreddits`[web:82][web:83]

**Response**

- List of recommended subreddits

---

### `GET /projects/{id}/subreddits`

Returns saved subreddit recommendations for a project.

---

### `GET /projects/{id}/posts`

Returns monitored Reddit posts found by the worker.

## MVP User Flow

This is enough to support the following basic flow:

1. Create a project
2. Discover relevant subreddits
3. Review relevant posts found in those subreddits

## Reddit Client

File: `backend/reddit_client.py`

This should be a thin wrapper around PRAW so it can be reused by both the API and the background worker.

Suggested methods:

- `search_subreddits(query, limit)`
- `get_subreddit(name)`
- `search_posts(subreddit, query, limit)`

PRAW supports subreddit and submission access through Reddit’s API, including subreddit search and reading new submissions.[web:79][web:81]

## Worker Script

File: `worker/monitor.py`

The worker is responsible for checking tracked subreddits and saving relevant new posts into the database.

### Trigger Schedule

The worker runs **3 times a day** using cron at fixed times.[web:92][web:106]

Example cron entry:

```bash
0 9,14,19 * * * /usr/bin/python3 /path/to/reddit-assistant/worker/monitor.py >> /path/to/reddit-assistant/worker.log 2>&1
```

This runs the worker every day at:

- 09:00
- 14:00
- 19:00

### Worker Flow

Each time the worker runs, it should:

1. Fetch all `project_subreddits`
2. For each subreddit:
   - Build a search query from the top project keywords
   - Use PRAW to fetch recent posts with `subreddit.search(...)` or `subreddit.new(...)`[web:79][web:81]
   - Skip posts already stored in `monitored_posts`
   - Compute a basic relevance score
   - Insert new relevant posts into `monitored_posts`

### Relevance Scoring

A simple MVP scoring approach can be:

- Keyword match count in title/body
- Optional embedding similarity later

This keeps the first version simple while leaving room for smarter ranking later.

## Notes

- Auth can be skipped in the first version
- A “selected subreddit” flag can be added later if needed
- Alerts, email notifications, and Slack integration can be added after the MVP
- The first version should focus on discovery, storage, and retrieval only
