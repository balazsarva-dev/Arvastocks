import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./components/others/Home";
import News from "./components/stocks/News";
import AreaChart from "./components/stocks/AreaChart";
import LineChart from "./components/stocks/LineChart";
import Contact from "./components/others/Contact";
import About from "./components/others/About";
import Terms from "./components/others/Terms";
import Register from "./components/users/Register";
import Login from "./components/users/Login";
import Logout from "./components/users/Logout";
import Profile from "./components/users/Profile"; 
import ChangeEmail from "./components/users/ChangeEmail";
import ChangePassword from "./components/users/ChangePassword";
import Delete from "./components/users/Delete";

const App = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/news" element={<News />} />
          <Route path="/area-chart" element={<AreaChart />} />
          <Route path="/line-chart" element={<LineChart />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/about" element={<About />} />
          <Route path="/terms" element={<Terms />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/update_email" element={<ChangeEmail />} />
          <Route path="/change_password" element={<ChangePassword />} />
          <Route path="/delete_account" element={<Delete />} />
          {/* Add more routes as needed */}
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;