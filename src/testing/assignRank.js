const { MongoClient } = require("mongodb");

const url = "mongodb://127.0.0.1:27017/";
const dbName = "newsdata";
const collectionName = "articledata";

const ranks = {
  bbc: 9,
  billboard: 6,
  cnet: 8,
  cbsnews: 6,
  futurism: 7,
  gizmodo: 7,
  forbes: 8,
  ibtimes: 7,
  nasa: 7,
  npr: 9,
  nytimes: 10,
  pcgamer: 8,
  propublica: 10,
  reutersagency: 7,
  techcrunch: 9,
  theverge: 7,
  time: 9,
  thurrott: 6,
  universetoday: 7,
  wired: 8,
  wsj: 10,
  yahoo: 4,
};

async function updateArticlesWithRank() {
  try {
    console.log("Starting the script...");

    // Create a new MongoClient instance
    const client = new MongoClient(url);

    // Connect to the MongoDB server
    await client.connect();
    console.log("Connected to MongoDB");

    // Access the database and collection
    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    console.log("Retrieving articles...");

    // Retrieve all articles
    const articles = await collection.find().toArray();
    console.log("Total articles:", articles.length);

    let count = 0;

    // Update articles with rank
    for (const article of articles) {
      const rank = ranks[article.source_id.toLowerCase()] || 0;
      await collection.updateOne(
        { _id: article._id },
        { $set: { rank: rank } }
      );

      count++;
      console.log("Processed:", count, "articles");
    }

    console.log("Rank data points added to articles.");

    // Close the MongoDB connection
    await client.close();
    console.log("MongoDB connection closed");
  } catch (error) {
    console.error("Error:", error);
  }
}

// Call the function to start the script
updateArticlesWithRank();
