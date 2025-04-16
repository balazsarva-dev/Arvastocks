import React from 'react';
import Navbar from './Navbar'; // Import Navbar from the same folder

const Layout = ({ children }) => {
  return (
    <div>
      <Navbar />
      <main>{children}</main>
    </div>
  );
};

export default Layout;