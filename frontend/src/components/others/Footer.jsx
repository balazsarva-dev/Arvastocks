import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="footer">
      <p>
        Arvastocks Ltd. <Link to="/terms">Terms and Services</Link>
      </p>
    </footer>
  );
};

export default Footer;