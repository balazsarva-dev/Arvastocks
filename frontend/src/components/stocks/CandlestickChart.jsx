import React, { useState } from 'react';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts/highstock';
import api from '../../services/api';
import './Chart.css';

const CandlestickChart = () => {
  const [symbol, setSymbol] = useState('AAPL');
  const [range, setRange] = useState('all'); // '1m', '3m', or 'all'
  const [chartOptions, setChartOptions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    if (!symbol) {
      setError('Please select a stock symbol.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await api.get('/candlestick', { params: { symbol } });
      let rawData = response.data;

      if (!rawData || rawData.length === 0) {
        setError('No data available for the selected stock symbol.');
        setChartOptions(null);
        return;
      }

      // Sort data by date ascending
      rawData = rawData
        .map(item => ({
          ...item,
          timestamp: new Date(item.x).getTime(),
        }))
        .sort((a, b) => a.timestamp - b.timestamp);

      // Filter data based on selected range
      let filteredData = rawData;
      if (range !== 'all') {
        const now = Date.now();
        let months = range === '1m' ? 1 : 3;
        const cutoff = new Date();
        cutoff.setMonth(cutoff.getMonth() - months);
        filteredData = rawData.filter(item => item.timestamp >= cutoff.getTime());
      }

      const formattedData = filteredData.map(item => [
        item.timestamp,
        item.o,
        item.h,
        item.l,
        item.c,
      ]);

      setChartOptions({
        title: {
          text: `${symbol} Candlestick Chart`,
        },
        rangeSelector: {
          selected: 0,
        },
        chart: {
          zoomType: 'x',
          panning: true,
          panKey: 'shift',
        },
        xAxis: {
          type: 'datetime',
        },
        yAxis: {
          title: {
            text: 'Price (USD)',
          },
        },
        series: [
          {
            type: 'candlestick',
            name: symbol,
            data: formattedData,
            tooltip: {
              valueDecimals: 2,
            },
            dataGrouping: {
              enabled: true,
            },
          },
        ],
      });

      setError(null);
    } catch (err) {
      setError('Failed to fetch candlestick data.');
      setChartOptions(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chart-container">
      <h1>Candlestick Chart</h1>
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
        <label htmlFor="range-select" style={{ marginLeft: 16 }}>Range: </label>
        <select
          id="range-select"
          value={range}
          onChange={(e) => setRange(e.target.value)}
          className="form-select"
        >
          <option value="1m">1 Month</option>
          <option value="3m">3 Months</option>
          <option value="all">All</option>
        </select>
        <button onClick={fetchData} className="form-button" disabled={loading}>
          {loading ? 'Loading...' : 'Get Chart'}
        </button>
      </div>
      {error && <p className="error-message">{error}</p>}
      <div className="chart">
        {chartOptions && (
          <HighchartsReact
            highcharts={Highcharts}
            constructorType={'stockChart'}
            options={chartOptions}
          />
        )}
          <p>Select a stock symbol and the range, and click "Get Chart" to load data.</p>
      </div>
    </div>
  );
};

export default CandlestickChart;