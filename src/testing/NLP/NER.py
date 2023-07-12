import spacy
import multiprocessing
from pymongo import MongoClient
from collections import Counter

# Define the entities to exclude
exclude_entities = {'1', '2', '2020', '2021', '2022', '2023', '2024', 'a busy week', 'a day', 'African', 'a week', 'a year', 'annual', 'BBC', 'Billboard', 'daily', 'dozens', 'first', 'five', 'four', 'Friday', 'hundreds', 'last month', 'last week', 'last year', 'millions', 'Monday', 'more than a decade', 'next year', 'night', 'one', 'One', 'Saturday', 'second', 'Six', 'six', 'summer', 'Sunday', 'Sunday night', 'the next five years', 'the past year', 'the Forbes Business Council', 'the past 24 hours', 'the past few days', 'the past few years', 'the past week', 'the week', 'the year', 'third', 'thousands', 'this summer', 'this week', 'this year', 'three', 'Thursday', 'today', 'tomorrow', 'Tuesday', 'Two', 'two', 'two-day', 'Wednesday', 'week', 'yesterday', 'year'}
# Define a map for normalizing entities
normalize_entities = {
    "America": "United States",
    "American": "United States",
    "Americans": "United States",
    "Donald Trump's": "Donald Trump",
    "England": "United Kingdom",
    "German": "Germany",
    "Prince Harry": "Prince Harry & Meghan Markle",
    "Meghan Markle": "Prince Harry & Meghan Markle",
    "Russian": "Russia",
    "US": "United States",
    "the United States": "United States",
    "The United States": "United States",
    "the United States'": "United States",
    "the White House": "The White House",
    "USA": "United States",
    "UK": "United Kingdom",
    "Ukrainian": "Ukraine",
    "UN": "United Nations",
}

def process_article(article):
    print(f"Processing article: {article['_id']}")
    return article['summary'], article['link']

def fetch_and_process_articles():
    client = MongoClient('127.0.0.1', 27017)
    db = client['newsdata']
    collection = db['articledata']

    articles = list(collection.find())
    print(f"Fetched {len(articles)} articles from MongoDB.")
    
    with multiprocessing.Pool() as pool:
        results = pool.map(process_article, articles)

    return results

def perform_ner(article_data):
    print("Performing NER...")
    nlp = spacy.load("en_core_web_lg")

    # Create a dictionary to store entities and corresponding article links
    entity_articles = {}

    for article_summary, article_link in article_data:
        doc = nlp(article_summary)

        # Extract entities, normalize them, filter out the excluded ones, and associate them with the article link
        for ent in doc.ents:
            normalized_entity = normalize_entities.get(ent.text, ent.text)
            if normalized_entity not in exclude_entities:
                if normalized_entity not in entity_articles:
                    entity_articles[normalized_entity] = [article_link]
                else:
                    entity_articles[normalized_entity].append(article_link)

    print("NER completed.")
    return entity_articles

def print_top_entities(entity_articles, n=100):
    # Count the number of articles for each entity
    entity_freq = {entity: len(article_links) for entity, article_links in entity_articles.items()}
    entity_freq = Counter(entity_freq)

    print(f"Top {n} entities across all articles:")
    for entity, freq in entity_freq.most_common(n):
        print(f"{entity}: {freq}")
        #for article_link in entity_articles[entity]:
            #print(f"    Article link: {article_link}")

if __name__ == '__main__':
    # Fetch articles and perform NER
    article_data = fetch_and_process_articles()
    entity_articles = perform_ner(article_data)
    
    # Print top 50 entities across all articles along with associated article links
    print_top_entities(entity_articles)
