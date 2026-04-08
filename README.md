# Project overview
* An AI‑assisted tool that ingests a product description, extracts key themes, and then helps the user find relevant subreddits and live conversations where that product can be talked about in a rule‑compliant, non‑spammy way.
* The tool focuses on research, monitoring, and planning; it does not automate posting, voting, or anything that would conflict with Reddit’s API and content policies.

# Goals
* Help a maker quickly discover where on Reddit their ideal users hang out (subreddits and types of threads).
* Surface live conversations that match their product’s problem space, with suggestions on how to reply in a helpful, value‑first way.
* Keep track of how often they mention their product so they stay within Reddit’s self‑promotion expectations (roughly the “10% rule”).

# Scope
* The project will cover:
* Product analysis: Input is a description, landing page URL, or app store link. The system extracts keywords, pain points, and target personas via NLP.
* Subreddit discovery: Use Reddit’s search/API or a compliant third‑party data source to find and score relevant subreddits (fit, activity, friendliness to promos).
* Conversation monitoring: Watch selected subreddits for new posts that match the product’s themes and notify the user with a short summary and suggested response angles.
* Self‑promotion dashboard: Show a rough promotional/non‑promotional activity ratio and remind the user of subreddit‑specific rules where they exist.

# Non‑goals (important constraints)
* No automated posting, commenting, DMing, or upvoting.
* No scraping that ignores Reddit’s API terms or robots protections; use the official API and/or compliant scraping providers.
* No guarantees of karma or sales; the tool is there to point the user to good opportunities and keep them within community norms.

# Core components
1. Ingestion + NLP layer
* Take text/URL input.
* Extract feature keywords, related problems, and likely personas (e.g., founders, students, freelancers).
* Cluster these into “intent themes” that can be used for subreddit and thread search.

2. Subreddit finder
* For each theme, search for subreddits and fetch basic stats (members, activity, typical content).
* Try to parse rules/wikis for self‑promotion signals and tag each subreddit (e.g., green/yellow/red for promos).
* Present a ranked list with notes like “good for questions”, “showcase allowed on Fridays”, etc.

3. Conversation watcher
* Let the user pick target subreddits + keywords/intents.
* Monitor new posts that match; send alerts with: short summary, why it’s relevant, and a suggested response outline that is helpful first, with an optional product mention.

4. Promotion ratio + guidance
* Track (at a rough level) which of the user’s posts mention the product or include a link.
* Visualize this against a “safe” self‑promotion ratio inspired by Reddit’s 90/10 guidance, plus reminders about individual sub rules.
