import React, { useState } from 'react';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom'; // Import zoomPlugin directly
import api from '../../services/api';
import './Chart.css'; // Include the Chart.css file

Chart.register(...registerables, zoomPlugin); // Register Chart.js components and the zoom plugin

const AreaChart = () => {
  const [symbol, setSymbol] = useState('AAPL'); // Default stock symbol
  const [chartData, setChartData] = useState(null); // Chart.js data object
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false); // Loading state for the "Get Chart" button

  // Fetch data for the selected stock symbol
  const fetchData = async () => {
    setLoading(true); // Show loading state
    setError(null); // Reset error state
    try {
      const response = await api.get(`/candlestick`, { params: { symbol } } ); // Correct API call syntax
      const rawData = response.data;

      // Process the data for Chart.js
      const labels = rawData.map((item) => new Date(item.x).toLocaleDateString()); // Dates
      const prices = rawData.map((item) => item.c); // Closing prices

      setChartData({
        labels,
        datasets: [
          {
            label: `${symbol} Closing Prices`,
            data: prices,
            fill: true,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            tension: 0.4, // Smooth curve
          },
        ],
      });
    } catch (error) {
      console.error('Error fetching stock data:', error);
      setError('Failed to fetch chart data. Please try again.');
    } finally {
      setLoading(false); // Hide loading state
    }
  };

  return (
    <div className="chart-container area-chart-container">
      <h1>Area Chart</h1>
      <div className="chart area-chart">
        <label htmlFor="stock-select">Symbol: </label>
        <select
          id="stock-select"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="form-select"
        >
          <option value="WFC">WFC</option>
          <option value="NVDA">NVDA</option>
          <option value="HD">HD</option>
          <option value="AMZN">AMZN</option>
          <option value="AAPL">AAPL</option>
          <option value="BAC">BAC</option>
          <option value="MSFT">MSFT</option>
          <option value="JPM">JPM</option>
        </select>
        <button onClick={fetchData} className="form-button" disabled={loading}>
          {loading ? 'Loading...' : 'Get Chart'}
        </button>
      </div>
      {error && <p className="error-message">{error}</p>}
      <div className="chart">
        {chartData ? (
          <canvas
            id="areaChart"
            ref={(canvas) => {
              if (canvas) {
                new Chart(canvas, {
                  type: 'line', // Area chart is a line chart with fill
                  data: chartData,
                  options: {
                    responsive: true,
                    plugins: {
                      zoom: {
                        pan: {
                          enabled: true,
                          mode: 'x', // Allow panning on the x-axis
                        },
                        zoom: {
                          wheel: {
                            enabled: true, // Allow zooming with the mouse wheel
                          },
                          pinch: {
                            enabled: true, // Allow zooming with pinch gestures
                          },
                          mode: 'x', // Zoom on the x-axis
                        },
                      },
                    },
                    scales: {
                      x: {
                        title: {
                          display: true,
                          text: 'Date',
                        },
                      },
                      y: {
                        title: {
                          display: true,
                          text: 'Price (USD)',
                        },
                      },
                    },
                  },
                });
              }
            }}
          />
        ) : (
          <p>Select a stock symbol and click "Get Chart" to load data.</p>
        )}
      </div>
    </div>
  );
};

export default AreaChart;