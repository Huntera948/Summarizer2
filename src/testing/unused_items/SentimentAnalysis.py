import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
print("Connecting to MongoDB...")
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['newsdata']
collection = db['articledata']

# Retrieve news headlines from MongoDB
print("Retrieving news headlines from MongoDB...")
cursor = collection.find({}, {'title': 1, 'category': 1})  # Adjust the field names as per your data structure

# Convert the cursor to a pandas DataFrame
df = pd.DataFrame(list(cursor))

training_data, testing_data = train_test_split(df, test_size=0.2)

def tokenization_(training_headings, testing_headings, max_length=20, vocab_size=5000):
    print("Tokenizing headlines...")
    tokenizer = Tokenizer(num_words=vocab_size, oov_token='<oov>')
    # Tokenization and padding
    tokenizer.fit_on_texts(training_headings)
    word_index = tokenizer.word_index
    training_sequences = tokenizer.texts_to_sequences(training_headings)
    training_padded = pad_sequences(training_sequences, padding='post', maxlen=max_length, truncating='post')

    testing_sequences = tokenizer.texts_to_sequences(testing_headings)
    testing_padded = pad_sequences(testing_sequences, padding='post', maxlen=max_length, truncating='post')

    return tokenizer, training_padded, testing_padded

tokenizer, X_train, X_test = tokenization_(
    training_data['title'], testing_data['title'])
 
labels = {'sports':[0,1,0],'tech':[1,0,0],'world':[0,0,1],}
Y_train = np.array([labels[y] for y in training_data['category']])
Y_test = np.array([labels[y]  for y in testing_data['category']])

def build_model( n, vocab_size, embedding_size):
    print("Building the model...")
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Embedding(vocab_size,
              embedding_size,input_length=n))
    model.add(tf.keras.layers.GlobalAveragePooling1D()) 
    model.add(tf.keras.layers.Dense(3,activation = 'softmax'))       
    model.compile(loss='categorical_crossentropy',optimizer='adam',
                   metrics='accuracy')
    print(model.summary())
    return model

epochs = 25
model = build_model(len(X_train[0]), vocab_size=5000, embedding_size=16)

print("Training the model...")
history = model.fit(X_train, Y_train,
                    validation_data=(X_test, Y_test),
                    epochs=epochs,
                    verbose=1)

print("Training completed!")
