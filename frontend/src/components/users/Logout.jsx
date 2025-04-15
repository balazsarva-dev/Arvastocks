import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api'; // Use the centralized Axios instance

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        const res = await api.post('/logout', {}, { withCredentials: true });

        if (res.status === 200) {
          // Clear user data from localStorage
          localStorage.removeItem('user');
          alert('You have been logged out successfully.');
          navigate('/login'); // Redirect to the login page
        } else {
          console.error('Failed to log out');
          alert('Failed to log out. Please try again.');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
      }
    };

    handleLogout();
  }, [navigate]);

  return <p>Logging out...</p>; // Show a message while logging out
};

export default Logout;
