import spacy
import multiprocessing
from pymongo import MongoClient
from collections import Counter
from entities import exclude_entities, normalize_entities

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

        # Extract relations
        relations = extract_relations(doc)
        for relation in relations:
            if relation not in entity_relations:
                entity_relations[relation] = [article_link]
            else:
                entity_relations[relation].append(article_link)

    print("NER and relation extraction completed.")
    return entity_articles, entity_relations

def print_top_entities(entity_articles, n=50):
    # Count the number of articles for each entity
    entity_freq = {entity: len(article_links) for entity, article_links in entity_articles.items()}
    entity_freq = Counter(entity_freq)

    print(f"Top {n} entities across all articles:")
    for entity, freq in entity_freq.most_common(n):
        print(f"{entity}: {freq}")

def print_relations(entity_relations):
    print("Relations across all articles:")
    for relation, article_links in entity_relations.items():
        print(f"Relation: {relation}, found in {len(article_links)} articles")

if __name__ == '__main__':
    # Fetch articles and perform NER and relation extraction
    article_data = fetch_and_process_articles()
    entity_articles, entity_relations = perform_ner_and_relation_extraction(article_data)
    
    # Print top 50 entities across all articles along with associated article links
    print_top_entities(entity_articles)

    # Print all relations
    print_relations(entity_relations)
