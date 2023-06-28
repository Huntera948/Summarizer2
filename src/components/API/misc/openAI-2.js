require("dotenv").config();
const { Configuration, OpenAIApi } = require("openai");

const fetchTextSummarization = async () => {
  const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
  });
  const openai = new OpenAIApi(configuration);

  try {
    const prompt = `Realme has introduced a groundbreaking design language for its flagship smartphone, the realme 11 Pro+. This remarkable device offers an unforgettable design, thanks to the collaboration with luxury fashion designer Matteo Menotto. The smartphone features a vegan leather finish, deviating from the typical plastic or glass rear design. With three attractive colors available, including Sunrise Beige, Oasis Green, and Astral Black, the green variant stands out with its sage green tone and a distinctive two-toned 3D-weave running down the middle of the back. The phone feels lightweight despite its large 6.7-inch AMOLED display and delivers a smooth user experience with up to 120 Hz refresh rates. The camera setup includes a prominent circular module housing a 200 MP OIS SuperZoom Camera, an ultra-micro camera, and an 8 MP ultra-wide camera. The outdoor shots are vibrant and sharp, with accurate skin tones and textures. While the device performs well in various lighting conditions, zooming beyond 4x can result in poorly-rendered subjects with noise. The realme 11 Pro+ runs on a MediaTek Dimensity 7050 5G chipset and features realme UI 4.0 based on Android 13. The phone offers a highly customizable always-on display, excellent battery life with a 5,000mAh battery and 100W SUPERVOOC fast-charging support. Overall, the realme 11 Pro+ impresses with its design, performance, and battery life, making it a compelling option in its price range, with only minor drawbacks such as bloatware and some photography nuances.`;
    const response = await openai.createCompletion({
      model: "gpt-3.5-turbo",
      prompt: `Summarize the following text:\n\n${prompt}`,
      max_tokens: 100, // Adjust the summary length as per your preference
      temperature: 0.3, // Adjust the temperature parameter for varied output
      n: 1, // Generate a single response
      stop: "\n\n", // Stop the summary at the first double newline character
    });

    console.log("Summary:", response.data.choices[0].text.trim());
  } catch (error) {
    console.error("Error:", error);
  }
};

fetchTextSummarization();
