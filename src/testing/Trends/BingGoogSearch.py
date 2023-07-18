import feedparser
from datetime import datetime, timedelta
import requests
import spacy

# Fetch trends from Google Trends RSS feed
rss_url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
feed = feedparser.parse(rss_url)
time_24_hours_ago = datetime.now() - timedelta(hours=24)

google_trends = []
for entry in feed.entries:
    published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    if published_date.replace(tzinfo=None) >= time_24_hours_ago:
        google_trends.append(entry.title)

# Fetch trends from Bing News API
url = "https://bing-news-search1.p.rapidapi.com/news/trendingtopics"
querystring = {"textFormat": "Raw", "safeSearch": "Off"}
headers = {
    "X-BingApis-SDK": "true",
    "X-RapidAPI-Key": "2ae68ace42msh9fb07e15283ad8ep158364jsn6f0d7bebe76d",
    "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
}
response = requests.get(url, headers=headers, params=querystring)
data = response.json()

bing_trends = [topic['query']['text'] for topic in data['value']]

# Combine trends from both sources
all_trends = google_trends + bing_trends

# Initialize spaCy's English model
nlp = spacy.load("en_core_web_lg")

# Extract named entities from all trends/headlines
entities = []
for trend in all_trends:
    doc = nlp(trend)
    entities.extend([ent.text for ent in doc.ents if ent.label_ != ""])

# Print the array of named entities
print("Named entities:")
print(entities)
