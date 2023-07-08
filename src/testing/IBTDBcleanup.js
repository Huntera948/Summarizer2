const { MongoClient } = require("mongodb");

// MongoDB connection URL
const url = "mongodb://127.0.0.1:27017/";
const dbName = "newsdata";

console.log("Starting...");

// Function to clean the text
function cleanText(text) {
  console.log("Original text:", text);

  text = text.replace(/NEWSLETTER SIGNUP*?KEY POINTS/, "");
  text = text.replace(/NEWSLETTER SIGNUP*?Reddit Share on/, "");
  text = text.replace(/REGISTER FOR FREE[\s\S]*?All Rights Reserved\./, "");
  text = text.replace(/pic\.twitter\.com\/\w+/g, "");
  text = text.replace(/ABOUT About Us.*$/, "");
  text = text.replace(/\s+/g, " ").trim();

  console.log("Cleaned text:", text);
  return text;
}

// Async function to connect to MongoDB
async function connectToMongoDB() {
  try {
    const client = new MongoClient(url);

    // Connect to the MongoDB server
    await client.connect();
    console.log("Connected to MongoDB");

    const db = client.db(dbName);
    const collection = db.collection("articledata");

    // Find documents with source_id of "ibtimes"
    const query = { source_id: "ibtimes" };

    const docs = await collection.find(query).toArray();
    console.log("Found", docs.length, "documents to process");

    // Process each document
    for (const doc of docs) {
      console.log("Processing document:", doc._id);

      // Clean the content of each document
      const cleanedText = cleanText(doc.content);

      // Update the document in the collection with the cleaned text
      await collection.updateOne(
        { _id: doc._id },
        { $set: { content: cleanedText } }
      );

      console.log("Document updated:", doc._id);
    }

    console.log("Processing completed");

    // Close the MongoDB connection
    await client.close();
    console.log("MongoDB connection closed");
  } catch (error) {
    console.error("Error:", error);
  }
}

// Call the async function to start the script
connectToMongoDB();
