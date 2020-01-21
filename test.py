import praw
from config import getReddit



print("test")

reddit = getReddit()

subreddit = reddit.subreddit("python")

hot_python = subreddit.hot(limit=5)

for submission in hot_python:
    print(submission.title)


print("test_after")
