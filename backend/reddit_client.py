# reddit_client.py
import praw
from .config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

    def search_subreddits(self, query, limit=10):
        return list(self.reddit.subreddits.search(query, limit=limit))

    def get_subreddit(self, name):
        return self.reddit.subreddit(name)

    def search_posts(self, subreddit_name, query, limit=10):
        subreddit = self.get_subreddit(subreddit_name)
        return list(subreddit.search(query, limit=limit))
