import React, { useState, useEffect } from "react";

const NewsComponent = ({ inputText }) => {
  const [newsData, setNewsData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiKey = "7f4aef6ed2754581be403ac2e5f45724";
        const response = await fetch(
          `https://newsapi.org/v2/everything?q="${inputText}"&pageSize=10&apiKey=${apiKey}`
        );
        const data = await response.json();
        setNewsData(data.articles);
      } catch (error) {
        console.error("Error fetching news data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>Latest News</h2>
      <ul>
        {newsData.map((article, index) => (
          <li key={index}>
            <a href={article.url} target="_blank" rel="noopener noreferrer">
              {article.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NewsComponent;
