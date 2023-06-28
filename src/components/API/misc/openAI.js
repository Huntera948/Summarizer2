const apiKey = "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";

const articleText = `MOSCOW: The Kremlin said Wednesday that Russian forces only hit military-linked targets in Ukraine, after a strike on a restaurant in the eastern city of Kramatorsk killed at least 10 people. The comments come a day after the Ria Pizza restaurant, — popular with soldiers, journalists, and aid workers — was destroyed in the city, one of the largest still under Ukrainian control in the east. "Strikes are only carried out on objects that are in one way or another linked to military infrastructure," said Kremlin spokesman Dmitry Peskov. "The Russian Federation does not carry out strikes on civilian infrastructure," he added. Kyiv's National Police said the strike, which came in the evening as the eatery was busy with guests, had also wounded 61 people. The Ukrainian emergency services said three children were among the dead. They added that a baby born in 2022 was among those wounded and warned that some people were still under the rubble. An AFP journalist on the scene shortly after the strike saw the restaurant in ruins surrounded by debris, with rescuers rushing to clear the rubble and search for bodies. Russia has denied striking civilian infrastructure throughout its 16-month-long Ukraine campaign.`;

fetch("https://api.openai.com/v1/engines/text-davinci-003/completions", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey}`,
  },
  body: JSON.stringify({
    prompt: `Summarize the following news article:\n\n${articleText}`,
    max_tokens: 1000, // Adjust the summary length as per your preference
    temperature: 0.3, // Adjust the temperature parameter for varied output
    n: 1, // Generate a single response
    stop: "\n\n", // Stop the summary at the first double newline character
  }),
})
  .then((response) => response.json())
  .then((json) => {
    console.log(json); // Log the JSON response for debugging

    if (json.choices && json.choices.length > 0) {
      const summarizedText = json.choices[0].text.trim();
      console.log(summarizedText);
    } else {
      console.error("No summarized text available.");
    }
  })
  .catch((error) => console.error("Error:", error));
