import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api'; // Use the centralized Axios instance

const Logout = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null); // State for error messages

  useEffect(() => {
    let isMounted = true; // Track if the component is mounted

    const handleLogout = async () => {
      try {
        const res = await api.post('/logout', {}, { withCredentials: true });

        if (isMounted) {
          if (res.status === 200) {
            // Clear user data from localStorage
            localStorage.removeItem('user');
            navigate('/login'); // Redirect to the login page
          } else {
            console.error('Failed to log out');
            setError('Failed to log out. Please try again.');
          }
        }
      } catch (error) {
        if (isMounted) {
          console.error('Error:', error);
          setError('An error occurred while logging out. Please try again later.');
        }
      }
    };

    handleLogout();

    return () => {
      isMounted = false; // Cleanup on unmount
    };
  }, [navigate]);

  return (
    <>
      {error ? (
        <p className="error-message" aria-live="polite">{error}</p> // Show error message if logout fails
      ) : (
        <p aria-live="polite">Logging out...</p> // Show "Logging out..." while the process is ongoing
      )}
    </>
  );
};

export default Logout;