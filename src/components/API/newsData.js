const apiKey = "pub_2529453bb1703552da9694fe294be8dd033c3";

const getNewsData = (searchTerm) => {
  return fetch(
    `https://newsdata.io/api/1/news?apikey=${apiKey}&q=${searchTerm}&language=en`
  )
    .then((response) => response.json())
    .then((data) => {
      const articles = data.results; // Assuming the array of articles is available under the 'results' property
      const articleArray = []; // Array to store the objects

      articles.forEach((article) => {
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

        articleArray.push(articleObject); // Add the object to the array
      });

      return articleArray; // Return the array of objects
    })
    .catch((error) => {
      console.error("Error fetching news data:", error);
    });
};

module.exports = getNewsData;
