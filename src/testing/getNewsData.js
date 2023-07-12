const insertArticles = require("./insertArticles2DB");
const cleanText_ibtimes = require("./text_cleanup_ibtimes");

const apiKey = "pub_2529453bb1703552da9694fe294be8dd033c3";
const domains = [
  ["bbc", "billboard", "cnet", "cbsnews", "futurism"],
  ["gizmodo", "forbes", "ibtimes", "nasa", "npr"],
  ["nytimes", "pcgamer", "propublica", "reutersagency", "techcrunch"],
  ["theverge", "time", "thurrott", "universetoday", "wired"],
  ["wsj", "yahoo"],
];

const getNewsData = () => {
  const articleArray = [];

  const fetchNewsData = (url) => {
    return fetch(url)
      .then((response) => response.json())
      .then((data) => {
        //console.log("Data:", data); // Inspect the data structure

        const articles = data.results;
        //console.log("Articles:", articles); // Inspect the articles array

        articles.forEach((article) => {
          if (
            article.content !== null &&
            article.content.length >= 1000 &&
            //(article.country === "united states of america" ||
            //article.country === "united kingdom") &&
            article.language === "english"
          ) {
            // If source_id is "ibtimes", clean the article content
            if (article.source_id === "ibtimes") {
              article.content = cleanText_ibtimes(article.content);
            }

            const articleObject = {
              pubDate: article.pubDate,
              title: article.title,
              link: article.link,
              content: article.content,
              creator: article.creator,
              keywords: article.keywords,
              country: article.country,
              category: article.category,
              source_id: article.source_id,
              language: article.language,
              description: article.description,
            };

            articleArray.push(articleObject);
          }
        });

        const nextPage = data.nextPage;
        if (nextPage) {
          const nextPageUrl = `https://newsdata.io/api/1/news?apikey=${apiKey}&domain=${domains[0].join(
            ","
          )}&page=${nextPage}`;
          return fetchNewsData(nextPageUrl);
        } else if (domains.length > 1) {
          domains.shift(); // Remove the first set of domains from the API call
          const newUrl = `https://newsdata.io/api/1/news?apikey=${apiKey}&domain=${domains[0].join(
            ","
          )}`;
          return fetchNewsData(newUrl);
        } else {
          if (articleArray.length === 0) {
            console.log("No articles to insert");
          } else {
            insertArticles(articleArray); // Insert articles into the database
          }
          return articleArray;
        }
      })
      .catch((error) => {
        console.error("Error fetching news data:", error);
      });
  };

  const initialUrl = `https://newsdata.io/api/1/news?apikey=${apiKey}&domain=${domains[0].join(
    ","
  )}`;
  return fetchNewsData(initialUrl)
    .then((results) => {
      console.log(results);
      return results;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

getNewsData();
