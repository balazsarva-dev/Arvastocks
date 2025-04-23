import React, { useEffect, useState } from 'react';
import api from '../../services/api';
import './StockTicker.css';

const StockTicker = () => {
  const [stocks, setStocks] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const res = await api.get('/important_stocks');
        setStocks(res.data);
      } catch (err) {
        setError('Failed to fetch stock data.');
      }
    };

    fetchStocks();
  }, []);

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  return (
    <div className="stock-ticker">
      <div className="ticker-content">
        {stocks.map((stock, index) => (
          <div key={index} className="ticker-item">
            {stock.name}: ${stock.price} ({stock.change})
          </div>
        ))}
      </div>
    </div>
  );
};

export default StockTicker;