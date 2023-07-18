import torch
from pymongo import MongoClient
from transformers import BartTokenizer, BartForConditionalGeneration
from multiprocessing.pool import ThreadPool

# Initialize the model and tokenizer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = BartForConditionalGeneration.from_pretrained('sshleifer/distilbart-xsum-12-6').to(device)
tokenizer = BartTokenizer.from_pretrained('sshleifer/distilbart-xsum-12-6')

# Define batch size
BATCH_SIZE = 16

# Function to summarize text
def summarize_text(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors='pt', max_length=1024, truncation=True).to(device)
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)  # skip special tokens during decoding

def fetch_and_process_articles():
    client = MongoClient('127.0.0.1', 27017)
    db = client['newsdata']
    collection = db['articledata']
    
    # Find only articles that do not have a 'summary' field yet
    articles = list(collection.find({ 'summary': { '$exists': False } }))
    num_articles = len(articles)
    num_batches = (num_articles - 1) // BATCH_SIZE + 1

    print(f"Processing {num_articles} articles in {num_batches} batches")

    # Create a ThreadPool for multithreading
    with ThreadPool(12) as pool:
        for batch_num in range(num_batches):
            start_index = batch_num * BATCH_SIZE
            end_index = min(start_index + BATCH_SIZE, num_articles)

            print(f"Processing batch {batch_num + 1} of {num_batches}")

            batch_articles = articles[start_index:end_index]
            batch_texts = [article['content'] for article in batch_articles]

            # Summarize articles in this batch
            summaries = pool.map(summarize_text, batch_texts)

            # Update the articles in the database with their summaries
            for article, summary in zip(batch_articles, summaries):
                collection.update_one({'_id': article['_id']}, {'$set': {'summary': summary}})

    print("Processing complete")

# Example usage
fetch_and_process_articles()
