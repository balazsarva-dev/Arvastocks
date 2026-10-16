import { useEffect, useState } from 'react';
import { fetchNews } from '../api';
import useSymbol from '../useSymbol';
import SymbolPicker from '../components/SymbolPicker';

const timeAgo = (seconds) => {
  const mins = Math.round((Date.now() / 1000 - seconds) / 60);
  if (mins < 60) return `${mins}m ago`;
  if (mins < 60 * 24) return `${Math.round(mins / 60)}h ago`;
  return `${Math.round(mins / 60 / 24)}d ago`;
};

export default function News() {
  const [symbol, setSymbol] = useSymbol();
  const [state, setState] = useState({ loading: true });

  useEffect(() => {
    let cancelled = false;
    setState({ loading: true });
    fetchNews(symbol)
      .then((articles) => !cancelled && setState({ articles }))
      .catch((error) => !cancelled && setState({ error: error.message }));
    return () => {
      cancelled = true;
    };
  }, [symbol]);

  const { articles, error, loading } = state;

  return (
    <>
      <SymbolPicker symbol={symbol} onChange={setSymbol} />
      <h1 className="page-title">{symbol} news</h1>

      {loading && <p className="message">Loading…</p>}
      {error && <p className="message error">{error}</p>}
      {articles?.length === 0 && <p className="message">No news found for {symbol}.</p>}

      <div className="news">
        {articles?.map((a) => {
          const thumb = a.thumbnail?.resolutions?.find((r) => r.tag === '140x140');
          return (
            <a key={a.uuid} href={a.link} target="_blank" rel="noopener noreferrer" className="card article">
              {thumb && <img src={thumb.url} alt="" loading="lazy" />}
              <div>
                <h3>{a.title}</h3>
                <p className="muted">
                  {a.publisher} · {timeAgo(a.providerPublishTime)}
                </p>
              </div>
            </a>
          );
        })}
      </div>
    </>
  );
}
