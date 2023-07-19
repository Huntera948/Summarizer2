from pymongo import MongoClient

url = "mongodb://127.0.0.1:27017/"
dbName = "newsdata"

print("Starting...")

def connect_to_mongodb():
    try:
        client = MongoClient(url)

        print("Connected to MongoDB")

        db = client[dbName]
        collection = db['articledata']

        # Define the aggregation pipeline
        aggregation_pipeline = [
            {
                "$group": {
                    "_id": {"title": "$title", "content": "$content"},
                    "duplicate_ids": {"$addToSet": "$_id"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "count": {"$gt": 1}
                }
            }
        ]

        # Execute the aggregation pipeline
        duplicate_docs = list(collection.aggregate(aggregation_pipeline))

        print("Found", len(duplicate_docs), "sets of duplicate documents")

        total_deleted_count = 0

        for duplicate_set in duplicate_docs:
            print("Processing duplicate set...")

            duplicate_ids = duplicate_set['duplicate_ids']
            sorted_duplicate_ids = sorted(duplicate_ids)

            original_id = sorted_duplicate_ids[0]
            duplicate_ids_to_delete = sorted_duplicate_ids[1:]

            delete_result = collection.delete_many({
                "_id": {"$in": duplicate_ids_to_delete}
            })

            deleted_count = delete_result.deleted_count
            total_deleted_count += deleted_count

            print("Deleted", deleted_count, "duplicate documents")
            print("Duplicate set processed")

        print("Total number of deleted documents:", total_deleted_count)
        print("Processing completed")

        client.close()
        print("MongoDB connection closed")
    except Exception as e:
        print("Error:", e)

connect_to_mongodb()
