from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

def train_model(X, y):
    # Split the data into a training set and a test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a Naive Bayes classifier
    clf = MultinomialNB()

    # Train the classifier
    clf.fit(X_train, y_train)

    # Evaluate the classifier on the test data
    accuracy = clf.score(X_test, y_test)

    print(f"Model accuracy: {accuracy*100:.2f}%")

    return clf

# Example usage:
# Assuming X is your list of document vectors and y is your list of labels
# X, y = ..., ...
# clf = train_model(X, y)
