// Install axios and dotenv packages if not already installed: npm install axios dotenv
const axios = require("axios");
require("dotenv").config();

// Define your OpenAI API credentials
const apiKey = process.env.OPENAI_API_KEY;

// Define the function to summarize a news article
async function summarizeArticle(articleText) {
  try {
    // Make a POST request to OpenAI API
    const response = await axios.post(
      "https://api.openai.com/v1/engines/text-davinci-003/completions",
      {
        prompt: `Summarize this news article in 5 sentences or less. Include Date Published, Author, Headline and link on the first line:\n\n${articleText}`,
        max_tokens: 1000, // Adjust the summary length as per your preference
        temperature: 0, // Adjust the temperature parameter for varied output
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
