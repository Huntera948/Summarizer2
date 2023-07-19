from pymongo import MongoClient

url = "mongodb://127.0.0.1:27017/"
dbName = "newsdata"
collectionName = "articledata"

ranks = {
    "bbc": 9,
    "billboard": 6,
    "cnet": 8,
    "cbsnews": 6,
    "futurism": 7,
    "gizmodo": 7,
    "forbes": 8,
    "ibtimes": 6,
    "nasa": 7,
    "npr": 9,
    "nytimes": 10,
    "pcgamer": 8,
    "propublica": 10,
    "reutersagency": 9,
    "techcrunch": 9,
    "theverge": 7,
    "time": 9,
    "thurrott": 6,
    "universetoday": 7,
    "wired": 8,
    "wsj": 10,
    "yahoo": 4,
}

def pubRanker():
    try:
        print("Starting the script...")

        # Create a new MongoClient instance
        client = MongoClient(url)

        # Access the database and collection
        db = client[dbName]
        collection = db[collectionName]

        print("Retrieving articles...")

        # Retrieve all articles
        articles = collection.find()
        articles_count = collection.count_documents({})
        print("Total articles:", articles_count)

        count = 0

        # Update articles with rank
        for article in articles:
            rank = ranks.get(article["source_id"].lower(), 0)
            collection.update_one(
                {"_id": article["_id"]},
                {"$set": {"rank": rank}}
            )

            count += 1
            print("Processed:", count, "articles")
            print("Rank assigned:", rank)

        print("Rank data points added to articles.")

        # Close the MongoDB connection
        client.close()
        print("MongoDB connection closed")
    except Exception as e:
        print("Error:", e)

# Call the function to start the script
pubRanker()
