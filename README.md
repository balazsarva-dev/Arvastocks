# Arvastocks

Stock charts (area, line, candlestick) and company news in one small React app.
Data is loaded live from Yahoo Finance — no backend, database or API key needed.

## Run

```bash
npm install
npm run dev
```

The app opens at http://localhost:5173.

## Notes

- Yahoo Finance does not allow direct browser requests (CORS), so the Vite dev server
  proxies `/yahoo/*` to `query1.finance.yahoo.com` (see `vite.config.js`). `npm run preview`
  uses the same proxy. A static deployment (e.g. Vercel, Netlify, nginx) needs an equivalent
  rewrite rule.
- The selected symbol is kept in the URL (`/?symbol=MSFT`), so links can be shared.

## Structure

```
src/
  api.js                 Yahoo Finance calls (prices, news)
  main.jsx               routes
  useSymbol.js           symbol <-> URL query param
  components/            Layout, SymbolPicker, PriceChart
  pages/                 Markets, News, About (+FAQ, terms), Donate
```
