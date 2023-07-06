const { MongoClient } = require("mongodb");

// Connection URI
const uri = "mongodb://127.0.0.1:27017/"; // Replace with your MongoDB connection URI

// Database Name
const dbName = "newsdata"; // Replace with your database name

// Collection Name
const collectionName = "articledata"; // Replace with your collection name

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

    console.log("Articles inserted successfully.");
  } catch (error) {
    console.error("Error inserting articles:", error);
  } finally {
    // Close the connection
    await client.close();
  }
};

module.exports = insertArticles;
