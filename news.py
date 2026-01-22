import feedparser
from datetime import datetime, timezone
from dateutil import parser


def isLastHour(s):
    now = datetime.now(timezone.utc)
    post = parser.parse(s)
    diff = post - now
    if abs(diff.total_seconds()) < 12600:
        return True
    else:
        return False



query = input("Enter Query - ")
URL = f"https://news.google.com/rss/search?q={query}"

feed = feedparser.parse(URL)

for entry in feed.entries:
    if isLastHour(entry.published):
        print(entry.title + " + " + entry.published)