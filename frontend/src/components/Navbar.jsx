import React, { useState } from 'react';
import './Navbar.css';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="navbar">
      <h1 className="navbar-logo">Arvastocks</h1>
      <button className="hamburger" onClick={toggleMenu}>
        ☰ {/* Hamburger icon */}
      </button>
      <ul className={`nav-links ${isMenuOpen ? 'show' : ''}`}>
        <li><a href="/">Home</a></li>
        <li><a href="/news">News</a></li>
        <li><a href="/area-chart">Area</a></li>
        <li><a href="/line-chart">Line</a></li>
        <li><a href="/candlestick-chart">Candlestick</a></li>
        <li><a href="/contact">Contact</a></li>
        <li><a href="/about">About</a></li>
        <li><a href='/donation'>Donation</a></li>
        <li><a href="/login">Login</a></li>
        <li><a href="/profile">Profile</a></li>
      </ul>
    </header>
  );
};

export default Navbar;