import nltk
import string
import multiprocessing
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

# Download stopwords if not already downloaded
nltk.download('stopwords')
nltk.download('wordnet')

stop = list(set(stopwords.words('english')))
custom_stop_words = ["new", "according", "best", "world", "week", "year", "time", "country", "stories", "news",
                     "state", "company", "look", "one", "latest", "first", "medium", "day", "social", "said"]
stop.extend(custom_stop_words)

exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([word for word in doc.lower().split() if word not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def calculate_tfidf(texts):
    print("Calculating TF-IDF...")
    texts = [clean(text) for text in texts]
    vectorizer = TfidfVectorizer(stop_words=stop)
    matrix = vectorizer.fit_transform(texts)
    print("TF-IDF calculation completed.")
    return matrix, vectorizer.get_feature_names_out(), vectorizer

def process_article(article):
    print(f"Processing article: {article['_id']}")
    return article['content']

def fetch_and_process_articles():
    client = MongoClient('127.0.0.1', 27017)
    db = client['newsdata']
    collection = db['articledata']

    articles = list(collection.find())
    print(f"Fetched {len(articles)} articles from MongoDB.")
    
    with multiprocessing.Pool() as pool:
        texts = pool.map(process_article, articles)

    return texts

# Protect the main loop using if __name__ == '__main__':
if __name__ == '__main__':
    # Fetch articles and perform TF-IDF
    texts = fetch_and_process_articles()
    matrix, feature_names, vectorizer = calculate_tfidf(texts)

    # Print matrix shape and first 10 feature names
    print(matrix.shape)

    # Print top 10 words across all articles
    sum_words = matrix.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    print("Top 10 words across all articles:")
    for word, freq in words_freq[:10]:
        print(f"{word}: {freq}")
