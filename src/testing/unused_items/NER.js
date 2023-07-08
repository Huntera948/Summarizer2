const natural = require("natural");
const tokenizer = new natural.WordTokenizer();
const ner = natural.LogisticRegressionNER;
const lancasterStemmer = natural.LancasterStemmer;

// Stemming example
const word = "running";
const stemmedWord = lancasterStemmer.stem(word);
console.log("Stemmed Word:", stemmedWord);

const { MongoClient } = require("mongodb");

const url = "mongodb://127.0.0.1:27017/";
const dbName = "newsdata";
const collectionName = "articledata";

console.log("Connecting to MongoDB...");
MongoClient.connect(url, function (err, client) {
  if (err) {
    console.error("Error connecting to MongoDB:", err);
    return;
  }

  console.log("Connected to MongoDB");

  const db = client.db(dbName);
  const collection = db.collection(collectionName);

  console.log("Retrieving articles...");

  collection.find().toArray(function (err, articles) {
    if (err) {
      console.error("Error retrieving articles:", err);
      client.close();
      return;
    }

    console.log("Total articles:", articles.length);

    articles.forEach((article) => {
      const content = article.content;
      const tokens = tokenizer.tokenize(content);
      const entities = ner.process(tokens);

      console.log("Entities:", entities);
    });

    console.log("Finished processing articles");
    client.close();
  });
});
