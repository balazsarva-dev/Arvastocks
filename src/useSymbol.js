import { useSearchParams } from 'react-router-dom';

// The selected symbol lives in the URL (?symbol=MSFT) so it survives reloads and is shared between pages.
export default function useSymbol() {
  const [params, setParams] = useSearchParams();
  const symbol = params.get('symbol') || 'AAPL';
  const setSymbol = (value) => setParams({ symbol: value });
  return [symbol, setSymbol];
}
