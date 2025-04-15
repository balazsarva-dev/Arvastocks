import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import api from './services/api'; // Use the centralized Axios instance
import Home from './components/others/Home';
import About from './components/others/About';
import Terms from './components/others/Terms';
import Footer from './components/others/Footer';
import Register from './components/users/Register';
import Login from './components/users/Login';
import Logout from './components/users/Logout';
import Profile from './components/users/Profile';
import Delete from './components/users/Delete';
import News from './components/stocks/News';
import Candlestick from './components/stocks/Candlestick';
import ChangeEmail from './components/users/ChangeEmail';
import ChangePassword from './components/users/ChangePassword';
import Contact from './components/others/Contact';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const res = await api.get('/profile', { withCredentials: true });

        if (res.status === 200) {
          setIsLoggedIn(true); // User is logged in
        } else {
          setIsLoggedIn(false); // User is not logged in
          localStorage.removeItem('user'); // Clear localStorage if session is invalid
        }
      } catch (error) {
        console.error('Error checking login status:', error);
        setIsLoggedIn(false);
        localStorage.removeItem('user'); // Clear localStorage on error
      }
    };

    checkLoginStatus();
  }, []);

  return (
    <Router>
      <div className="app-container">
        <nav className="navigation-bar">
          <Link to="/home">
            <button>Home</button>
          </Link>
          <Link to="/register">
            <button>Register</button>
          </Link>
          <Link to="/login">
            <button>Login</button>
          </Link>
          <Link to="/news">
            <button>News</button>
          </Link>
          {isLoggedIn && (
            <Link to="/profile">
              <button>Profile</button>
            </Link>
          )}
          <Link to="/candlestick">
            <button>Candlestick</button>
          </Link>
          <Link to="/contact">
            <button>Contact</button>
          </Link>
          {isLoggedIn && (
            <Link to="/logout">
              <button>Logout</button>
            </Link>
          )}
            <Link to="/about">
            <button>About</button>
          </Link>
        </nav>
      </div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/about" element={<About />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/terms" element={<Terms />} />
        <Route path="/news" element={<News />} />
        <Route path="/delete_account" element={<Delete />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/candlestick" element={<Candlestick />} />
        <Route path="/update_email" element={<ChangeEmail />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/update_password" element={<ChangePassword />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;
