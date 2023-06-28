const apiKey = "pub_2529453bb1703552da9694fe294be8dd033c3";
const searchTerm = "Canada Fire";

const getNewsData = () => {
  return fetch(
    `https://newsdata.io/api/1/news?apikey=${apiKey}&q=${searchTerm}&language=en`
  )
    .then((response) => response.json())
    .then((data) => {
      const posts = data.results; // Assuming the array of posts is available under the 'results' property
      const postArray = []; // Array to store the objects

      posts.forEach((post) => {
        const postObject = {
          pubDate: post.pubDate,
          title: post.title,
          link: post.link,
          content: post.content,
        };

        postArray.push(postObject); // Add the object to the array
      });

      return postArray; // Return the array of objects
    })
    .catch((error) => {
      console.error("Error fetching news data:", error);
    });
};

module.exports = getNewsData;
