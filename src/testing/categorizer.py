from pymongo import MongoClient
from keywords import keywords

# Connect to MongoDB
print("Connecting to MongoDB...")
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['newsdata']
collection = db['articledata']

# Function to classify the category of a given article
def classify_category(article):
    # Perform category classification based on your specific logic or model

    category_counts = {category: 0 for category in keywords.keys()}
    keyword_rankings = {category: {} for category in keywords.keys()}

    for category, words in keywords.items():
        for word in words:
            count = article.lower().count(word.lower())
            # Assign a weight to each occurrence of the keyword
            weighted_count = count * (1 / (count + 1))
            category_counts[category] += weighted_count
            keyword_rankings[category][word] = weighted_count

    # Find the category with the maximum count
    max_category = max(category_counts, key=category_counts.get)

    # Calculate confidence scores based on total keyword count
    total_keyword_count = sum(category_counts.values())

    if total_keyword_count == 0:
        # Handle the case when no keywords are found in the article
        confidence_scores = {category: 0 for category in keywords.keys()}
    else:
        # Calculate confidence scores normally and round to 3 decimal points
        confidence_scores = {category: round(count / total_keyword_count, 3) for category, count in category_counts.items()}

    # If no category is matched, return a default category
    return max_category, keyword_rankings, confidence_scores

# Fetch all documents from the collection
print("Fetching articles from the collection...")
articles = collection.find()

# Update the category, keyword rankings, and confidence scores for each article
for article in articles:
    article_content = article['content']
    category, keyword_rankings, confidence_scores = classify_category(article_content)
    collection.update_one(
        {'_id': article['_id']},
        {'$set': {'category': category, 'keyword_rankings': keyword_rankings, 'confidence_scores': confidence_scores}}
    )
    print(f"Updated category, confidence scores, and keyword rankings for article with ID: {article['_id']}. Category: {category}, Confidence Scores: {confidence_scores}")

# Close the MongoDB connection
client.close()
print("Process completed.")
