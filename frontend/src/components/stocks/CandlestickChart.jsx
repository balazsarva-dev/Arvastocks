import React, { useState, useEffect } from 'react';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts/highstock';
import api from '../../services/api'; // Axios instance for API calls
import './Chart.css'; // Reuse the same CSS as AreaChart

const CandlestickChart = () => {
  const [symbol, setSymbol] = useState(''); // State for the stock symbol input
  const [chartOptions, setChartOptions] = useState(null); // State for chart configuration
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state

  // Function to fetch candlestick data
  const fetchData = async () => {
    if (!symbol) {
      setError('Please enter a stock symbol.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Fetch data from the backend
      const response = await api.post('/candlestick', { symbol });
      const rawData = response.data;

      console.log('Raw Data:', rawData); // Debugging: Log the raw data

      if (!rawData || rawData.length === 0) {
        setError('No data available for the selected stock symbol.');
        return;
      }

      // Format the data for Highcharts
      const formattedData = rawData.map((item) => [
        new Date(item.x).getTime(), // Convert date to timestamp
        item.o, // Open
        item.h, // High
        item.l, // Low
        item.c, // Close
      ]);

      console.log('Formatted Data:', formattedData); // Debugging: Log the formatted data

      // Update chart options
      setChartOptions({
        title: {
          text: `${symbol} Candlestick Chart`,
        },
        rangeSelector: {
          selected: 0, // Default range selector option
        },
        chart: {
          zoomType: 'x', // Enable zooming on the x-axis
          panning: true, // Enable panning
          panKey: 'shift', // Hold "Shift" to pan
        },
        xAxis: {
          type: 'datetime', // Time-based x-axis
        },
        yAxis: {
          title: {
            text: 'Price-USD',
          },
        },
        series: [
          {
            type: 'candlestick',
            name: symbol,
            data: formattedData,
            tooltip: {
              valueDecimals: 2, // Show 2 decimal places in tooltips
            },
            dataGrouping: {
              enabled: false,
            },
          },
        ],
      });

      setError(null);
    } catch (err) {
      console.error('Error fetching candlestick data:', err);
      setError('Failed to fetch candlestick data.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chart">
      <h1>Candlestick Chart</h1>
      <div className="chart-input">
        {/* Search bar for stock symbol */}
        <input
          type="text"
          placeholder="Enter stock symbol"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          className="chart-input-field"
        />
        <button onClick={fetchData} className="chart-button" disabled={loading}>
          {loading ? 'Loading...' : 'Get Chart'}
        </button>
      </div>
      {error && <p className="error-message">{error}</p>}
      {chartOptions && (
        <HighchartsReact
          highcharts={Highcharts}
          constructorType={'stockChart'} // Use Highcharts Stock for candlestick charts
          options={chartOptions}
        />
      )}
    </div>
  );
};

export default CandlestickChart;