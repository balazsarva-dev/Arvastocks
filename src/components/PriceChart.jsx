import { useEffect, useRef } from 'react';
import { createChart, AreaSeries, LineSeries, CandlestickSeries, ColorType } from 'lightweight-charts';

const UP = '#22c55e';
const DOWN = '#ef4444';

function addSeries(chart, type, candles) {
  const rising = candles.at(-1).close >= candles[0].close;
  const color = rising ? UP : DOWN;
  const line = candles.map((c) => ({ time: c.time, value: c.close }));

  if (type === 'candles') {
    chart
      .addSeries(CandlestickSeries, {
        upColor: UP,
        downColor: DOWN,
        borderVisible: false,
        wickUpColor: UP,
        wickDownColor: DOWN,
      })
      .setData(candles);
  } else if (type === 'area') {
    chart
      .addSeries(AreaSeries, {
        lineColor: color,
        topColor: color + '55',
        bottomColor: color + '00',
        lineWidth: 2,
      })
      .setData(line);
  } else {
    chart.addSeries(LineSeries, { color, lineWidth: 2 }).setData(line);
  }
}

export default function PriceChart({ candles, type }) {
  const container = useRef(null);

  useEffect(() => {
    const chart = createChart(container.current, {
      autoSize: true,
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' },
        textColor: '#94a3b8',
        attributionLogo: false,
      },
      grid: {
        vertLines: { color: '#1e293b' },
        horzLines: { color: '#1e293b' },
      },
      rightPriceScale: { borderVisible: false },
      timeScale: { borderVisible: false },
    });
    addSeries(chart, type, candles);
    chart.timeScale().fitContent();
    return () => chart.remove();
  }, [candles, type]);

  return <div ref={container} className="chart" />;
}
