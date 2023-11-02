import feedparser
from datetime import datetime, timedelta
import requests
import spacy
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['newsdata']
collection = db['articledata']

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
entities = set()  # Use a set to automatically remove duplicates
for trend in all_trends:
    doc = nlp(trend)
    entities.update(ent.text for ent in doc.ents if ent.label_ not in {"", "TIME", "CARDINAL", "MONEY", "DATE", "ORDINAL", "NORP"})

# Print the array of named entities
print("Named entities:")
for entity in entities:
    print(entity)

# Define the categories
categories = [
    "art & design", "books", "business", "crypto", "culture", "economy", "film-TV", "food", "gaming", "health",
    "investing", "music", "opinion", "politics", "programming", "real estate", "science", "sports", "style",
    "tech", "travel", "u.s.", "world"
]

# Initialize the ranked article lists
ranked_articles = {category: [] for category in categories}

# Find matching articles in the MongoDB database
print("Finding matching articles...")
for entity in entities:
    print(f"Searching for articles related to: {entity}")
    matching_articles = collection.find(
        {
            "entities": {"$elemMatch": {"$elemMatch": {"$eq": entity}}}
        },
        {
            "_id": 0,
            "summary": 1,
            "rank": 1,
            "category": 1,
            "link": 1 
        }
    ).limit(5)

    for article in matching_articles:
        ranked_articles[article['category']].append((article['summary'], article['link']))

# Fill out the ranked article lists with highest ranking articles from the past 24 hours
print("Filling out ranked article lists...")
for category in categories:
    if len(ranked_articles[category]) < 5:
        print(f"Category: {category}")
        top_ranking_articles = collection.find(
            {
                #"pubDate": {"$gte": time_24_hours_ago},
                "category": category
            },
            {
                "_id": 0,
                "summary": 1,
                "rank": 1,
                "link": 1
            }
        ).sort("rank", -1).limit(5 - len(ranked_articles[category]))

        for article in top_ranking_articles:
            ranked_articles[category].append((article['summary'], article['link']))

# Print the summaries of the top-ranking articles for each category
print("Top-ranking articles:")
for category, articles in ranked_articles.items():
    print(f"{category}:")
    for summary, link in articles:  # Unpack the tuple
        print(summary)  # Print the summary
        print(link)  # Print the link
        print("\n")  # Print a newline for readability
