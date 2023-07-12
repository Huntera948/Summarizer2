import nltk
import string
import multiprocessing
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models
from pymongo import MongoClient

# Download stopwords if not already downloaded
nltk.download('stopwords')
nltk.download('wordnet')

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([word for word in doc.lower().split() if word not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def determine_topics(texts, num_topics=5):
    print("Starting LDA modeling...")
    doc_clean = [clean(doc).split() for doc in texts]

    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    
    Lda = models.ldamodel.LdaModel
    ldamodel = Lda(doc_term_matrix, num_topics=num_topics, id2word = dictionary, passes=50, update_every=1, eval_every=1)
    
    print("LDA modeling completed.")
    return ldamodel.print_topics(num_topics=num_topics)

def process_article(article):
    print(f"Processing article: {article['_id']}")
    return article['summary']

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
    # Fetch articles and perform LDA
    texts = fetch_and_process_articles()
    topics = determine_topics(texts)
    for topic in topics:
        print(topic)
