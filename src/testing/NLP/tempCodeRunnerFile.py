def fetch_and_process_articles():
    client = MongoClient('127.0.0.1', 27017)
    db = client['newsdata']
    collection = db['articledata']