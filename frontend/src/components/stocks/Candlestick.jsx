import React, { useState } from 'react';
import api from '../../services/api'; // Use the centralized Axios instance

const Candlestick = () => {
  const [symbol, setSymbol] = useState('');
  const [chartHtml, setChartHtml] = useState('');
  const [error, setError] = useState(null);

  const fetchCandlestickChart = async () => {
    if (!symbol) {
      alert('Please enter a stock symbol');
      return;
    }

    try {
      const res = await api.post('/candlestick', {
        symbol,
        candlestick_setting: true,
      });

      setChartHtml(res.data.figure); // Assuming `figure` contains HTML for the chart
      setError(null);
    } catch (error) {
      console.error('Error fetching candlestick chart:', error);
      setError(
        error.response?.data?.message || 'An error occurred. Please try again later.'
      );
    }
  };

  return (
    <div className="candlestick-container">
      <h1>Candlestick Chart</h1>
      <div className="candlestick-input">
        <input
          type="text"
          id="stock-symbol"
          name="stock-symbol"
          placeholder="Enter stock symbol"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="form-input"
        />
        <button onClick={fetchCandlestickChart} className="candlestick-button">
          Get Chart
        </button>
      </div>
      {error && <p className="error-message">Error: {error}</p>}
      {chartHtml && (
        <iframe
          title="Candlestick Chart"
          srcDoc={chartHtml} // Use srcDoc to embed the HTML
          style={{ width: '100%', height: '500px', border: 'none' }}
        />
      )}
    </div>
  );
};

export default Candlestick;
