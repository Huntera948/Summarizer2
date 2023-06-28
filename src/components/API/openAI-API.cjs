// Install axios package if not already installed: npm install axios
const axios = require("axios");

// Define your OpenAI API credentials
const apiKey = "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";

// Define the function to summarize a news article
async function summarizeArticle(articleText) {
  try {
    // Make a POST request to OpenAI API
    const response = await axios.post(
      "https://api.openai.com/v1/engines/text-davinci-003/completions",
      {
        prompt: `Summarize the following news article:\n\n${articleText}`,
        max_tokens: 1000, // Adjust the summary length as per your preference
        temperature: 0.3, // Adjust the temperature parameter for varied output
        n: 1, // Generate a single response
        stop: "\n\n", // Stop the summary at the first double newline character
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
      }
    );

    // Extract the summarized text from the API response
    const summary = response.data.choices[0].text.trim();

    return summary;
  } catch (error) {
    console.error("Error:", error.response.data.error.message);
    return null;
  }
}

// Usage example
const getNewsData = require("./newsData");

const processNewsData = async () => {
  try {
    const newsArray = await getNewsData();

    const processedData = [];
    for (const article of newsArray) {
      const { pubDate, title, link, content } = article;
      const articleText = `Pub Date: ${pubDate}\nTitle: ${title}\nLink: ${link}\nContent: ${content}\n`;
      const summary = await summarizeArticle(articleText);
      processedData.push(summary);
    }

    console.log("Processed Data:", processedData);
  } catch (error) {
    console.error("Error:", error);
  }
};

processNewsData();
