import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

// Optional: Error Boundary Component
const ErrorBoundary = ({ children }) => {
  return (
    <StrictMode>
      {children}
    </StrictMode>
  );
};

createRoot(document.getElementById('root')).render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);
