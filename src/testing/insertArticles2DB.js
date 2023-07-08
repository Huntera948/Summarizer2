const { MongoClient } = require("mongodb");

const uri = "mongodb://127.0.0.1:27017/";
const dbName = "newsdata";
const collectionName = "articledata";

// Create a new MongoClient
const client = new MongoClient(uri);

// Function to insert articles into the database
const insertArticles = async (articles) => {
  try {
    // Connect to the MongoDB server
    await client.connect();

    // Select the database and collection
    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    // Insert each article into the collection
    await collection.insertMany(articles);

    console.log("Articles inserted into MongoDB database successfully.");
  } catch (error) {
    console.error("Error inserting articles:", error);
  } finally {
    // Close the connection
    await client.close();
  }
};

module.exports = insertArticles;
