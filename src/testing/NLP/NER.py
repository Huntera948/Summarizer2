import spacy
import multiprocessing
from pymongo import MongoClient
from collections import Counter

# Define the entities you want to exclude
exclude_entities = {"BBC", "One", "the year", "year", "Billboard", "week", "2", '1', "the next five years", "dozens", "more than a decade", "thousands", "night", "Two", "hundreds", "six", "a day", "the past few years", "Sunday night", "a busy week", "daily", "last month", "a week", "the week", "annual", "two-day", "the past few days", "the past 24 hours", "first", "second", "third", "one", "two", "three", "four", "five", "the past week", "this week", "last week", "2023", "2024", "Monday", "Tuesday", "Wednesday" "Thursday", "Friday", "Saturday", "Sunday", "today", "tomorrow", "yesterday", "this year", "last year", "next year", "2020", "2021", "2022"}

def process_article(article):
    print(f"Processing article: {article['_id']}")
    return article['summary']

def fetch_and_process_articles():
    client = MongoClient('127.0.0.1', 27017)
    db = client['newsdata']
    collection = db['articledata']

    articles = list(collection.find())
    print(f"Fetched {len(articles)} articles from MongoDB.")
    
    with multiprocessing.Pool() as pool:
        texts = pool.map(process_article, articles)

    return texts

def perform_ner(texts):
    print("Performing NER...")
    nlp = spacy.load("en_core_web_lg")

    # Flatten all texts into one large text for NER
    all_text = " ".join(texts)
    doc = nlp(all_text)

    # Extract entities and filter out the excluded ones
    entities = [ent.text for ent in doc.ents if ent.text not in exclude_entities]
    print("NER completed.")
    return entities

def print_top_entities(entities, n=100):
    entity_freq = Counter(entities)
    print(f"Top {n} entities across all articles:")
    for entity, freq in entity_freq.most_common(n):
        print(f"{entity}: {freq}")

if __name__ == '__main__':
    # Fetch articles and perform NER
    texts = fetch_and_process_articles()
    entities = perform_ner(texts)
    
    # Print top 50 entities across all articles
    print_top_entities(entities)
