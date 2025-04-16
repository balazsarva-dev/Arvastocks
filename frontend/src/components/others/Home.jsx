import React from "react";
import "./Home.css";

const HomePage = () => {
  return (
    <div className="homepage-container">
      <div className="homepage-content">
        <h1 className="homepage-title">Welcome</h1>
        <ul className="home-description-list">
          <li>This app is designed to help you make smarter investment decisions.</li>
          <li>Search for stock symbols, view charts, and stay updated with the latest news.</li>
          <li>With Machine Learning tools, we aim to support your investment journey.</li>
        </ul>
      </div>
    </div>
  );
};

export default HomePage;