from pymongo import MongoClient, UpdateOne
import language_tool_python
import textstat
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from text_preprocessor import text_preprocessor
from multiprocessing import Pool, current_process
import time
from pymongo.errors import BulkWriteError
import logging

# Initialize language tool
tool = language_tool_python.LanguageTool('en-US')

def analyze_text_quality(document):
    # Assume the article text is stored in the 'content' field of the document
    text = document['content']

    # Preprocess text
    text = text_preprocessor(text)

    # Check for grammar and spelling mistakes
    matches = tool.check(text)
    num_errors = len(matches)
    
    # Check for punctuation errors
    num_punctuation_errors = sum(1 for match in matches if 'Punctuation' in match.ruleId)

    # Create an errors dictionary
    error_dict = {f"Error_{i+1}": str(error) for i, error in enumerate(matches)}

    # Check for passive voice
    num_passive_voice = sum(1 for match in matches if 'PASSIVE_VOICE' in match.ruleId)

    # Measure readability scores
    flesch_reading_ease = textstat.flesch_reading_ease(text)
    gunning_fog = textstat.gunning_fog(text)
    coleman_liau = textstat.coleman_liau_index(text)

    # Compute lexical diversity
    words = word_tokenize(text)
    lexical_diversity_score = len(set(words)) / len(words) if words else 0

    # Calculate average sentence length
    sentences = sent_tokenize(text)
    avg_sentence_length = sum(len(word_tokenize(sent)) for sent in sentences) / len(sentences) if sentences else 0

    # Word frequency analysis
    word_frequency = Counter(words)

    # Create a dictionary with analysis results
    analysis = {
        'num_errors': num_errors,
        'num_punctuation_errors': num_punctuation_errors,
        'num_passive_voice': num_passive_voice,
        'flesch_reading_ease': flesch_reading_ease,
        'gunning_fog': gunning_fog,
        'coleman_liau': coleman_liau,
        'lexical_diversity_score': lexical_diversity_score,
        'avg_sentence_length': avg_sentence_length,
        'word_frequency': word_frequency,
        'error_list': error_dict
    }

    # Create an update operation for this document
    update_operation = UpdateOne({'_id': document['_id']}, {'$set': {'text_quality_analysis': analysis}})

    logging.info(f'Process {current_process().name} finished document {document["_id"]}')

    print(f"Finished analysis for document {document['_id']}")

    return update_operation

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    mongo_client = MongoClient("mongodb://127.0.0.1:27017/")
    db = mongo_client["newsdata"]
    collection = db["articledata"]

    print("Starting text quality analysis...")
    start_time = time.time()

    # Create a multiprocessing pool
    with Pool() as p:
        # Get a list of all documents
        documents = list(collection.find())
        
        # Analyze all documents in parallel and get a list of update operations
        operations = p.map(analyze_text_quality, documents)

        print("Finished analyzing all documents. Starting bulk write...")

        # Execute all operations in bulk
        try:
            collection.bulk_write(operations)
        except BulkWriteError as bwe:
            print(bwe.details)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Finished text quality analysis for all documents in {elapsed_time} seconds.")

if __name__ == '__main__':
    main()
