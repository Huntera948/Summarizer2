const re = require("re");

export default function cleanText_ibtimes(text) {
  // Remove unwanted text at the beginning
  text = text.replace(/^[\s\S]*?NEWSLETTER SIGNUP.*?KEY POINTS/, "");
  text = text.replace(/REGISTER FOR FREE[\s\S]*?All Rights Reserved\./, "");
  text = text.replace(/pic\.twitter\.com\/\w+/g, ""); // Remove chunks like "pic.twitter.com/kwkFzy0Us0"
  // Remove unwanted text at the end
  text = text.replace(/ABOUT About Us.*$/, "");
  // Remove extra whitespaces
  text = text.replace(/\s+/g, " ").trim();
  return text;
}
