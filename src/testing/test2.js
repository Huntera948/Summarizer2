const apiKey = "pub_2529453bb1703552da9694fe294be8dd033c3";
const domains = [
  "bbc,billboard,cnet,cbsnews,futurism",
  "gizmodo,forbes,ibtimes,nasa,npr",
  "nytimes,pcgamer,propublica,reutersagency,techcrunch",
  "theverge,time,thurrott,universetoday,wired",
  "wsj,yahoo",
];

const getNewsData = () => {
  const articleArray = [];

  const fetchNewsData = (url) => {
    return fetch(url)
      .then((response) => response.json())
      .then((data) => {
        const articles = data.results;

        articles.forEach((article) => {
          if (article.content !== null && article.content.length >= 1000) {
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
            };

            articleArray.push(articleObject);
          }
        });

        const nextPage = data.nextPage;
        if (nextPage) {
          const nextPageUrl = `https://newsdata.io/api/1/news?apikey=${apiKey}&page=${nextPage}`;
          return fetchNewsData(nextPageUrl);
        } else {
          return articleArray;
        }
      })
      .catch((error) => {
        console.error("Error fetching news data:", error);
      });
  };

  const initialUrl = `https://newsdata.io/api/1/news?apikey=${apiKey}&domain=${domains[0]}`;
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
