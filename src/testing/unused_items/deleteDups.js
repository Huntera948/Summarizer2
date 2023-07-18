const { MongoClient } = require("mongodb");

// MongoDB connection URL
const url = "mongodb://127.0.0.1:27017/";
const dbName = "newsdata";

console.log("Starting...");

// Async function to connect to MongoDB
async function connectToMongoDB() {
  try {
    const client = new MongoClient(url);

    // Connect to the MongoDB server
    await client.connect();
    console.log("Connected to MongoDB");

    const db = client.db(dbName);
    const collection = db.collection("articledata");

    // Find duplicate documents
    const aggregationPipeline = [
      {
        $group: {
          _id: { title: "$title", content: "$content" },
          duplicateIds: { $addToSet: "$_id" },
          count: { $sum: 1 },
        },
      },
      {
        $match: {
          count: { $gt: 1 },
        },
      },
    ];

    const duplicateDocs = await collection
      .aggregate(aggregationPipeline)
      .toArray();
    console.log("Found", duplicateDocs.length, "sets of duplicate documents");

    let totalDeletedCount = 0;

    // Process each set of duplicate documents
    for (const duplicateSet of duplicateDocs) {
      console.log("Processing duplicate set...");

      // Get the array of duplicate document IDs
      const duplicateIds = duplicateSet.duplicateIds;

      // Sort the duplicate document IDs in ascending order
      const sortedDuplicateIds = duplicateIds.sort((a, b) => a - b);

      // Keep the first document ID as the original and remove the rest
      const originalId = sortedDuplicateIds[0];
      const duplicateIdsToDelete = sortedDuplicateIds.slice(1);

      // Delete the duplicate documents
      const deleteResult = await collection.deleteMany({
        _id: { $in: duplicateIdsToDelete },
      });
      const deletedCount = deleteResult.deletedCount;
      totalDeletedCount += deletedCount;

      console.log("Deleted", deletedCount, "duplicate documents");
      console.log("Duplicate set processed");
    }

    console.log("Total number of deleted documents:", totalDeletedCount);
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
