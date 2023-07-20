import spacy
from pymongo import MongoClient
from collections import Counter

# Define excluded entity types
excluded_entity_types = ['TIME', 'MONEY', 'CARDINAL', 'DATE']

def perform_ner_extraction(article_data):
    nlp = spacy.load("en_core_web_lg")
    
    entity_counter = Counter()

    for article in article_data:
        article_summary = article['summary']
        
        doc = nlp(article_summary)
        
        entities = []
        for ent in doc.ents:
            normalized_entity = ent.text
            entity_type = ent.label_
            
            # Exclude certain entity types
            if entity_type in excluded_entity_types:
                continue
            
            entities.append(normalized_entity)
        
        entity_counter.update(entities)

        article['entities'] = entities

    return article_data, entity_counter

# Connect to MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['newsdata']
collection = db['articledata']

# Fetch articles from the MongoDB collection
print("Fetching articles from MongoDB...")
articles = list(collection.find())
print(f"Fetched {len(articles)} articles.")

# Perform NER extraction on article summaries and count entities
print("Performing NER extraction and counting entities...")
extracted_articles, entity_counter = perform_ner_extraction(articles)
print("NER extraction and entity counting completed.")

# Update the articles in the database with the extracted entities
print("Updating articles in the database...")
for article in extracted_articles:
    article_id = article['_id']
    entities = article['entities']
    collection.update_one({'_id': article_id}, {'$set': {'entities': entities}})
print("Article update completed.")

# Print the duplicate entities and their occurrence counts
print("Duplicate entities and their occurrence counts:")
for entity, count in entity_counter.items():
    print(f"{entity}: {count}")

print("NER extraction, entity update, and counting completed.")
