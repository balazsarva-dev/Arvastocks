import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="homepage-container">
      <div className="homepage-content">
        <h1 className="homepage-title">Welcome</h1>
        <p className="homepage-description">
          This app is designed to help you make smarter investment decisions.
        </p>
        <div className="homepage-buttons">
          <button
            className="homepage-button register-button"
            onClick={() => navigate("/register")}
          >
            Register
          </button>
          <button
            className="homepage-button login-button"
            onClick={() => navigate("/login")}
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;