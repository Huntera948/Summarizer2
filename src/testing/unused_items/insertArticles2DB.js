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
    for (let article of articles) {
      // Check if an article with the same link exists
      const existingArticle = await collection.findOne({ link: article.link });

      if (!existingArticle) {
        // Insert the article into the collection
        await collection.insertOne(article);
        console.log(`Inserted article: ${article.title}`);
      } else {
        console.log(`Article already exists: ${article.title}`);
      }
    }
  } catch (error) {
    console.error("Error inserting articles:", error);
  } finally {
    // Close the connection
    await client.close();
  }
};

module.exports = insertArticles;
