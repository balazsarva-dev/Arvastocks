import React from 'react';
import Navbar from './Navbar'; // Import Navbar from the same folder
import Footer from './others/Footer';
const Layout = ({ children }) => {
  return (
    <div>
      <Navbar />
      <main>{children}</main>
        <Footer />
    </div>
  );
};

export default Layout;