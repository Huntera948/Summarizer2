import spacy
from entities import exclude_entities, normalize_entities

def perform_ner_extraction(article_data):
    nlp = spacy.load("en_core_web_lg")
    
    entity_articles = {}
    for article in article_data:
        article_content = article['content']
        article_link = article['link']
        
        doc = nlp(article_content)
        
        for ent in doc.ents:
            normalized_entity = normalize_entities.get(ent.text, ent.text)
            if normalized_entity not in exclude_entities:
                if normalized_entity not in entity_articles:
                    entity_articles[normalized_entity] = [article_link]
                else:
                    entity_articles[normalized_entity].append(article_link)

    return entity_articles
