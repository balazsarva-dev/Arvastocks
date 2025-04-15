import React, { useState } from 'react';
import api from '../../services/api'; // Use the centralized Axios instance

const News = () => {
  const [symbol, setSymbol] = useState(''); // State for the stock symbol input
  const [news, setNews] = useState([]); // State for the fetched news articles
  const [error, setError] = useState(null); // State for error messages

  const getNews = async () => {
    if (!symbol) {
      alert('Please enter a stock symbol');
      return;
    }

    try {
      const response = await api.get(`/news_data?symbol=${symbol}`);

      // Set the news state with the received data
      setNews(response.data.feed || []); // Use `data.feed` if available, otherwise set an empty array
      setError(null); // Clear any previous errors
    } catch (error) {
      console.error('Error occurred while fetching news:', error);
      setError(
        error.response?.data?.message || 'An error occurred. Please try again later.'
      );
    }
  };

  return (
    <div className="news-container">
      <h1>Stock News</h1>
      <div className="news-input">
        <input
          type="text"
          placeholder="Enter stock symbol"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="form-input"
        />
        <button onClick={getNews} className="news-button">
          Get News
        </button>
      </div>
      {error && <p className="error-message">Error: {error}</p>}
      <div className="news-articles">
        {news.length > 0 ? (
          news.map((article, index) => (
            <div key={index} className="news-article">
              <h5>
                <a href={article.url} target="_blank" rel="noopener noreferrer" className="news-title">
                  {article.title}
                </a>
              </h5>
              <p className="news-summary">{article.summary}</p>
              <p className="news-source">Source: {article.source}</p>
              <hr />
            </div>
          ))
        ) : (
          !error && <p>No news found for this symbol.</p>
        )}
      </div>
    </div>
  );
};

export default News;
