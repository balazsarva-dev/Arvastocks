import React, { useState } from 'react';
import { Chart, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
import api from '../../services/api';
import './Chart.css';

Chart.register(...registerables, zoomPlugin);

const AreaChart = () => {
  const [symbol, setSymbol] = useState('AAPL');
  const [range, setRange] = useState('all');
  const [chartData, setChartData] = useState(null);
  const [rawData, setRawData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/candlestick`, { params: { symbol } });
      const data = response.data
        .map(item => ({
          ...item,
          timestamp: new Date(item.x).getTime(),
        }))
        .sort((a, b) => a.timestamp - b.timestamp);

      setRawData(data);
      filterAndSetChartData(data, range);
    } catch (error) {
      console.error('Error fetching stock data:', error);
      setError('Failed to fetch chart data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const filterAndSetChartData = (data, selectedRange) => {
    let filtered = data;
    if (selectedRange !== 'all') {
      const now = Date.now();
      let months = 0;
      if (selectedRange === '1m') months = 1;
      if (selectedRange === '3m') months = 3;
      if (selectedRange === '6m') months = 6;
      if (selectedRange === '1y') months = 12;
      const cutoff = new Date();
      cutoff.setMonth(cutoff.getMonth() - months);
      filtered = data.filter(item => item.timestamp >= cutoff.getTime());
    }

    const labels = filtered.map(item => new Date(item.x).toLocaleDateString());
    const prices = filtered.map(item => item.c);

    setChartData({
      labels,
      datasets: [
        {
          label: `${symbol} Closing Prices`,
          data: prices,
          fill: true,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          tension: 0.4,
        },
      ],
    });
  };

  // When range changes, filter the already-fetched data
  React.useEffect(() => {
    if (rawData.length > 0) {
      filterAndSetChartData(rawData, range);
    }
    // eslint-disable-next-line
  }, [range]);

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
          {/* ...options... */}
          <option value="WFC">WFC</option>
          <option value="NVDA">NVDA</option>
          <option value="HD">HD</option>
          <option value="AMZN">AMZN</option>
          <option value="AAPL">AAPL</option>
          <option value="BAC">BAC</option>
          <option value="MSFT">MSFT</option>
          <option value="JPM">JPM</option>
          <option value="TMUS">TMUS</option>
          <option value="VZ">VZ</option>
          <option value="PEP">PEP</option>
          <option value="TSM">TSM</option>
          <option value="V">V</option>
          <option value="UNP">UNP</option>
          <option value="MA">MA</option>
          <option value="INTC">INTC</option>
        </select>
        <label htmlFor="range-select" style={{ marginLeft: 16 }}>Range: </label>
        <select
          id="range-select"
          value={range}
          onChange={e => setRange(e.target.value)}
          className="form-select"
          disabled={rawData.length === 0}
        >
          <option value="1m">1 Month</option>
          <option value="3m">3 Months</option>
          <option value="6m">6 Months</option>
          <option value="1y">1 Year</option>
          <option value="all">All</option>
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
            ref={canvas => {
              if (canvas) {
                new Chart(canvas, {
                  type: 'line',
                  data: chartData,
                  options: {
                    responsive: true,
                    plugins: {
                      zoom: {
                        pan: {
                          enabled: true,
                          mode: 'x',
                        },
                        zoom: {
                          wheel: { enabled: true },
                          pinch: { enabled: true },
                          mode: 'x',
                        },
                      },
                    },
                    scales: {
                      x: {
                        title: { display: true, text: 'Date' },
                      },
                      y: {
                        title: { display: true, text: 'Price (USD)' },
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