from pymongo import MongoClient

uri = "mongodb://127.0.0.1:27017/"
dbName = "newsdata"
collectionName = "articledata"

# Create a new MongoClient
client = MongoClient(uri)

def insert_articles(articles):
    try:
        # Connect to the MongoDB server
        print("Connected to MongoDB")

        # Select the database and collection
        db = client[dbName]
        collection = db[collectionName]

        # Insert each article into the collection
        for article in articles:
            # Check if an article with the same link exists
            existing_article = collection.find_one({'link': article['link']})

            if not existing_article:
                # Insert the article into the collection
                collection.insert_one(article)
                print(f"Inserted article: {article['title']}")
            else:
                print(f"Article already exists: {article['title']}")

    except Exception as e:
        print("Error inserting articles:", e)

    finally:
        # Close the connection
        client.close()
        print("MongoDB connection closed")
