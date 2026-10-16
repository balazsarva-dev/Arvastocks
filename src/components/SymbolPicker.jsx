import { useState } from 'react';

export const POPULAR = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'META', 'TSLA', 'JPM', 'V', 'INTC'];

export default function SymbolPicker({ symbol, onChange }) {
  const [draft, setDraft] = useState('');

  const submit = (e) => {
    e.preventDefault();
    const value = draft.trim().toUpperCase();
    if (value) onChange(value);
    setDraft('');
  };

  return (
    <div className="picker">
      <form onSubmit={submit} className="search">
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Search symbol, e.g. NFLX"
          aria-label="Stock symbol"
        />
        <button type="submit">Go</button>
      </form>
      <div className="chips">
        {POPULAR.map((s) => (
          <button
            key={s}
            className={s === symbol ? 'chip active' : 'chip'}
            onClick={() => onChange(s)}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
