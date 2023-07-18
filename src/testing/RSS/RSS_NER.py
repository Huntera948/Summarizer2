import spacy
import multiprocessing
from pymongo import MongoClient
from collections import Counter
from entities import exclude_entities, normalize_entities

def process_article(article):
    print(f"Processing article: {article['_id']}")
    return article['summary']

def fetch_and_process_articles():
    client = MongoClient('127.0.0.1', 27017)
    db = client['newsdata']
    collection = db['RSSdata']

    articles = list(collection.find())
    print(f"Fetched {len(articles)} articles from MongoDB.")

    with multiprocessing.Pool() as pool:
        results = pool.map(process_article, articles)

    return results

def extract_relations(doc):
    relations = []
    for token in doc:
        if token.dep_ in ('attr', 'dobj') and token.ent_type_:
            subject = [w for w in token.head.lefts if w.dep_ in ('nsubj', 'nsubjpass') and w.ent_type_]
            if subject:
                subject = subject[0]
                relations.append((str(subject), str(token.head), str(token)))
    return relations

def perform_ner_and_relation_extraction(article_data):
    print("Performing NER and relation extraction...")
    nlp = spacy.load("en_core_web_lg")

    # Create dictionaries to store entities with corresponding article links and relations
    entity_articles = {}
    entity_relations = {}

    for article_summary in article_data:
        doc = nlp(article_summary)

        # Extract entities, normalize them, filter out the excluded ones
        for ent in doc.ents:
            normalized_entity = normalize_entities.get(ent.text, ent.text)
            if normalized_entity not in exclude_entities:
                if normalized_entity not in entity_articles:
                    entity_articles[normalized_entity] = 1
                else:
                    entity_articles[normalized_entity] += 1

        # Extract relations
        relations = extract_relations(doc)
        for relation in relations:
            if relation not in entity_relations:
                entity_relations[relation] = 1
            else:
                entity_relations[relation] += 1

    print("NER and relation extraction completed.")
    return entity_articles, entity_relations

def print_top_entities(entity_articles, n=50):
    entity_freq = Counter(entity_articles)

    print(f"Top {n} entities across all articles:")
    for entity, freq in entity_freq.most_common(n):
        print(f"{entity}: {freq}")

def print_relations(entity_relations):
    print("Relations across all articles:")
    for relation, count in entity_relations.items():
        print(f"Relation: {relation}, found in {count} articles")

if __name__ == '__main__':
    article_data = fetch_and_process_articles()
    entity_articles, entity_relations = perform_ner_and_relation_extraction(article_data)

    print_top_entities(entity_articles)
    print_relations(entity_relations)
