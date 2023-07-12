import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
#from vectorizer import vectorize_text

def text_preprocessor(text):
    # Convert text to lowercase
    text = text.lower()

    # Tokenize the text - break it up into words
    text = word_tokenize(text)

    # Remove punctuation
    text = [word for word in text if word.isalnum()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = [word for word in text if not word in stop_words]

    # Lemmatize the words - reduce them to their root form
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text]

    # Convert the tokens back to a single string
    text = " ".join(text)

    return text
