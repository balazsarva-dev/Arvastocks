// Interval per range keeps every chart at a readable number of points.
export const RANGES = {
  '1mo': { label: '1M', interval: '1d' },
  '3mo': { label: '3M', interval: '1d' },
  '6mo': { label: '6M', interval: '1d' },
  '1y': { label: '1Y', interval: '1d' },
  '5y': { label: '5Y', interval: '1wk' },
  max: { label: 'Max', interval: '1mo' },
};

async function getJson(url) {
  const res = await fetch(url);
  // Yahoo answers unknown symbols with a 404 that still has a JSON body, so let callers inspect it.
  if (!res.ok && res.status !== 404) throw new Error(`Request failed (${res.status})`);
  return res.json();
}

export async function fetchPrices(symbol, range) {
  const { interval } = RANGES[range];
  const data = await getJson(
    `/yahoo/v8/finance/chart/${encodeURIComponent(symbol)}?range=${range}&interval=${interval}`
  );
  const result = data.chart?.result?.[0];
  if (!result?.timestamp) throw new Error(`No data found for "${symbol}"`);

  const quote = result.indicators.quote[0];
  const candles = result.timestamp
    .map((time, i) => ({
      time,
      open: quote.open[i],
      high: quote.high[i],
      low: quote.low[i],
      close: quote.close[i],
    }))
    .filter((c) => c.close != null && c.open != null);
  if (candles.length === 0) throw new Error(`No price data for "${symbol}"`);

  return { meta: result.meta, candles };
}

export async function fetchNews(symbol) {
  const data = await getJson(
    `/yahoo/v1/finance/search?q=${encodeURIComponent(symbol)}&newsCount=20&quotesCount=0`
  );
  return data.news ?? [];
}
