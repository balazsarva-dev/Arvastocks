import React, { useEffect, useRef, useState } from 'react';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns'; // For time-based x-axis
import zoomPlugin from 'chartjs-plugin-zoom'; // For zooming functionality
import api from '../../services/api'; // Centralized Axios instance
import './Chart.css'; // Import CSS for styling

// Register chart.js components and plugins
Chart.register(...registerables, zoomPlugin);

const AreaChart = () => {
  const chartRef = useRef(null); // Reference for the chart container
  const chartInstance = useRef(null); // Reference to store the chart instance
  const [symbol, setSymbol] = useState(''); // State for the stock symbol
  const [error, setError] = useState(null); // State for error messages
  const [loading, setLoading] = useState(false); // State for loading indicator

  const fetchChartData = async () => {
    if (!symbol) {
      setError('Please enter a stock symbol.');
      return;
    }

    setLoading(true); // Start loading
    setError(null); // Clear previous errors

    try {
      // Fetch chart data from the backend
      const response = await api.post('/candlestick', { symbol });

      let rawData = response.data;

      if (!rawData || rawData.length === 0) {
        setError('No valid data available for the selected stock symbol.');
        return;
      }

      // Filter data to include only the last 12 months
      const twelveMonthsAgo = new Date();
      twelveMonthsAgo.setMonth(twelveMonthsAgo.getMonth() - 12);

      rawData = rawData.filter((item) => new Date(item.x) >= twelveMonthsAgo);

      // If a chart already exists, destroy it before creating a new one
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      // Create the area chart
      const ctx = chartRef.current.getContext('2d');
      chartInstance.current = new Chart(ctx, {
        type: 'line', // Area chart is a line chart with `fill: true`
        data: {
          labels: rawData.map((item) => item.x), // Use x values as labels
          datasets: [
            {
              label: `${symbol} Closing Prices`,
              data: rawData.map((item) => item.c), // Use closing prices as data points
              borderColor: 'rgba(75, 192, 192, 1)', // Line color
              backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill color
              borderWidth: 2,
              fill: true, // Enable area fill
              tension: 0.4, // Smooth the line
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false, // Hide the legend
            },
            tooltip: {
              enabled: true, // Enable tooltips
            },
            zoom: {
              pan: {
                enabled: true, // Enable panning
                mode: 'xy', // Allow panning on both x and y axes
              },
              zoom: {
                wheel: {
                  enabled: true, // Enable zooming with the mouse wheel
                },
                pinch: {
                  enabled: true, // Enable zooming with pinch gestures
                },
                mode: 'xy', // Allow zooming on both x and y axes
              },
            },
          },
          scales: {
            x: {
              type: 'time', // Use a time scale for the x-axis
              time: {
                unit: 'month', // Group data by month
              },
              title: {
                display: true,
                text: 'Date',
              },
              grid: {
                display: false, // Remove grid lines on the x-axis
              },
            },
            y: {
              title: {
                display: true,
                text: 'Price',
              },
              grid: {
                display: true, // Keep grid lines on the y-axis
              },
            },
          },
        },
      });

      setError(null); // Clear any previous errors
    } catch (err) {
      console.error('Error fetching chart data:', err);
      setError(
        err.response?.data?.message || 'An error occurred. Please try again later.'
      );
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="chart">
      <h1>Area Chart (Last 12 Months)</h1>
      <div className="chart-input">
        <input
          type="text"
          placeholder="Enter stock symbol"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())} // Convert input to uppercase
          className="chart-input-field"
        />
        <button onClick={fetchChartData} className="chart-button" disabled={loading}>
          {loading ? 'Loading...' : 'Get Chart'}
        </button>
      </div>
      {error && <p className="error-message">{error}</p>}
      <canvas ref={chartRef} style={{ width: '100%', height: '500px', backgroundColor: 'white' }} /> {/* Chart container */}
    </div>
  );
};

export default AreaChart;