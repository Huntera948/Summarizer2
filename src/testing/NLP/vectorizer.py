from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_text(documents):
    # Create the TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the documents and transform the documents into vectors
    document_vectors = vectorizer.fit_transform(documents)

    return document_vectors, vectorizer

# Example usage:
documents = [
    "the quick brown fox",
    "jumped over the lazy dog",
    "the dog",
    "the fox"
]

document_vectors, vectorizer = vectorize_text(documents)
