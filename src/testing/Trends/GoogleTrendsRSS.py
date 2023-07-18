import feedparser
from datetime import datetime, timedelta

# RSS feed URL for Google Trends (US region)
rss_url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"

# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Calculate the date and time of 24 hours ago
time_24_hours_ago = datetime.now() - timedelta(hours=24)

# Print the trending topics from the last 24 hours
print("Trending topics from the last 24 hours on Google Trends (US):")
for entry in feed.entries:
    # Get the publication date of the entry
    published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    if published_date >= time_24_hours_ago:
        print(entry.title)
