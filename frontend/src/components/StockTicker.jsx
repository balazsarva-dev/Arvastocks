import React from 'react';
import './StockTicker.css'; // Add styles for the ticker

const StockTicker = ({ stocks }) => {
  return (
    <div className="stock-ticker">
      <div className="ticker-content">
        {stocks.map((stock, index) => (
          <div key={index} className="ticker-item">
            {stock.name}: {stock.price} ({stock.change}%)
          </div>
        ))}
      </div>
    </div>
  );
};

export default StockTicker;
