import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./components/others/Home";
import News from "./components/stocks/News";
import Candlestick from "./components/stocks/Candlestick";
import Contact from "./components/others/Contact";
import About from "./components/others/About";
import Terms from "./components/others/Terms";
import Register from "./components/users/Register";
import Login from "./components/users/Login";


const App = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/news" element={<News />} />
          <Route path="/candlestick" element={<Candlestick />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/about" element={<About />} />
          <Route path="/terms" element={<Terms />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;