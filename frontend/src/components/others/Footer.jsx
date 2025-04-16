import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="footer">
      <p>
      © 2025 Arvastocks. All rights reserved.<Link to="/terms">Terms and Services</Link>
      </p>
    </footer>
  );
};

export default Footer;