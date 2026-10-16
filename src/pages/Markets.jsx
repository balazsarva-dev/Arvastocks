import { useEffect, useState } from 'react';
import { fetchPrices, RANGES } from '../api';
import useSymbol from '../useSymbol';
import SymbolPicker from '../components/SymbolPicker';
import PriceChart from '../components/PriceChart';

const CHART_TYPES = { area: 'Area', line: 'Line', candles: 'Candles' };

const usd = (n, currency = 'USD') =>
  n.toLocaleString('en-US', { style: 'currency', currency });

export default function Markets() {
  const [symbol, setSymbol] = useSymbol();
  const [range, setRange] = useState('1y');
  const [type, setType] = useState('area');
  const [state, setState] = useState({ loading: true });

  useEffect(() => {
    let cancelled = false;
    setState((s) => ({ ...s, loading: true, error: null }));
    fetchPrices(symbol, range)
      .then((data) => !cancelled && setState({ data }))
      .catch((error) => !cancelled && setState({ error: error.message }));
    return () => {
      cancelled = true;
    };
  }, [symbol, range]);

  const { data, error, loading } = state;

  return (
    <>
      <SymbolPicker symbol={symbol} onChange={setSymbol} />

      <section className="card">
        {data && <Summary meta={data.meta} candles={data.candles} range={range} />}

        <div className="toolbar">
          <Segmented options={RANGES} value={range} onChange={setRange} getLabel={(r) => r.label} />
          <Segmented options={CHART_TYPES} value={type} onChange={setType} />
        </div>

        {error ? (
          <p className="message error">{error}</p>
        ) : data ? (
          <div className={loading ? 'loading' : undefined}>
            <PriceChart candles={data.candles} type={type} />
          </div>
        ) : (
          <p className="message">Loading…</p>
        )}
      </section>
    </>
  );
}

function Summary({ meta, candles, range }) {
  const first = candles[0].close;
  const last = meta.regularMarketPrice ?? candles.at(-1).close;
  const change = last - first;
  const pct = (change / first) * 100;
  const cls = change >= 0 ? 'up' : 'down';
  const currency = meta.currency || 'USD';

  return (
    <div className="summary">
      <div>
        <h1>
          {meta.symbol} <span className="muted">{meta.longName || meta.shortName}</span>
        </h1>
        <div className="price">
          {usd(last, currency)}
          <span className={cls}>
            {change >= 0 ? '+' : ''}
            {change.toFixed(2)} ({pct.toFixed(2)}%) · {RANGES[range].label}
          </span>
        </div>
      </div>
      <dl className="stats">
        <Stat label="Day range" value={`${meta.regularMarketDayLow?.toFixed(2)} – ${meta.regularMarketDayHigh?.toFixed(2)}`} />
        <Stat label="52w range" value={`${meta.fiftyTwoWeekLow?.toFixed(2)} – ${meta.fiftyTwoWeekHigh?.toFixed(2)}`} />
        <Stat label="Volume" value={meta.regularMarketVolume?.toLocaleString('en-US')} />
        <Stat label="Exchange" value={meta.fullExchangeName || meta.exchangeName} />
      </dl>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value ?? '—'}</dd>
    </div>
  );
}

function Segmented({ options, value, onChange, getLabel = (l) => l }) {
  return (
    <div className="segmented">
      {Object.entries(options).map(([key, opt]) => (
        <button key={key} className={key === value ? 'active' : ''} onClick={() => onChange(key)}>
          {getLabel(opt)}
        </button>
      ))}
    </div>
  );
}
