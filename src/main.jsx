import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Markets from './pages/Markets';
import News from './pages/News';
import About from './pages/About';
import Donate from './pages/Donate';
import './index.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Markets />} />
          <Route path="news" element={<News />} />
          <Route path="about" element={<About />} />
          <Route path="donation" element={<Donate />} />
          <Route path="donation-success" element={<Donate thanks />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
