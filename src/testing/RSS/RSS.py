import feedparser
from RSS_Feed_URLs import feed_urls

passed_feeds = []

for feed_url in feed_urls:
    feed = feedparser.parse(feed_url)
    
    if len(feed.entries) > 0:
        if 'summary' in feed.entries[0] and 'content' in feed.entries[0] and 'description' in feed.entries[0]:
            passed_feeds.append(feed_url)

print(passed_feeds)