import React, { useEffect, useState } from "react";

const NewsDataComponent = () => {
  const [newsData, setNewsData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiKey = "pub_2529453bb1703552da9694fe294be8dd033c3"; // Replace with your NewData.io API key
        const response = await fetch(`https://newsdata.io/api/1/news?apikey=${apiKey}&q=pizza`, {
          headers: {
            "X-API-Key": apiKey,
          },
        });
        const data = await response.json();
        setNewsData(data.articles);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Latest News</h1>
      {newsData.map((newsItem) => (
        <div key={newsItem.id}>
          <h2>{newsItem.title}</h2>
          <p>{newsItem.content}</p>
        </div>
      ))}
    </div>
  );
};

export default NewsDataComponent;
