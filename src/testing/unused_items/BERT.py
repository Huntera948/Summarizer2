import torch
from transformers import BertTokenizer, BertForSequenceClassification
from pymongo import MongoClient

# Connect to MongoDB
print("Connecting to MongoDB...")
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['newsdata']
collection = db['articledata']

# Define the keywords and categories
keywords = {
    'technology': ['technology', 'computer', 'software', 'programming', 'internet', 'AI', 'machine learning'],
    'sports': ['sports', 'football', 'basketball', 'soccer', 'tennis', 'cricket', 'baseball'],
    'politics': ['politics', 'government', 'election', 'legislation', 'democracy', 'policy', 'leadership'],
    'health': ['health', 'medicine', 'fitness', 'nutrition', 'wellness', 'mental health', 'disease'],
    'entertainment': ['entertainment', 'movies', 'celebrities', 'art', 'theater', 'film'],
    'business': ['business', 'economy', 'finance', 'entrepreneurship', 'startups', 'investment', 'market'],
    'science': ['science', 'research', 'discovery', 'experiment', 'technology', 'innovation', 'astronomy'],
    'education': ['education', 'learning', 'school', 'university', 'knowledge', 'teaching', 'students'],
    'travel': ['travel', 'vacation', 'adventure', 'explore', 'destination', 'tourism', 'journey'],
    'environment': ['environment', 'sustainability', 'climate', 'nature', 'ecology', 'conservation', 'green'],
    'music': ['music', 'musician', 'song', 'artist', 'album', 'concert', 'band', 'genre', 'record industry', 'music industry', 'singer-songwriter', 'hit single', 'Spotify', 'final tour']
}

# Load the pre-trained BERT model and tokenizer
print("Loading BERT model and tokenizer...")
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=len(keywords))

# Set device to GPU if available, otherwise use CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Function to preprocess and tokenize the article content
def preprocess_text(text):
    # Tokenize the text
    tokens = tokenizer.encode_plus(text, max_length=512, truncation=True, padding='max_length', add_special_tokens=True, return_tensors='pt')
    input_ids = tokens['input_ids'].to(device)
    attention_mask = tokens['attention_mask'].to(device)
    return input_ids, attention_mask

# Function to classify the category of a given article
def classify_category(article):
    input_ids, attention_mask = preprocess_text(article['content'])
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()
    category = list(keywords.keys())[predicted_label]
    return category

# Fetch all documents from the collection
articles = collection.find()

# Update the category for each article
print("Starting classification process...")
for idx, article in enumerate(articles, 1):
    print(f"Processing article {idx}")
    category = classify_category(article)
    collection.update_one(
        {'_id': article['_id']},
        {'$set': {'category': category}}
    )

# Close the MongoDB connection
client.close()
print("Classification process completed.")
