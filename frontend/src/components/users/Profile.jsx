import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api'; // Use the centralized Axios instance

const Profile = () => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const res = await api.get('/profile', { withCredentials: true });

        setUserData(res.data); // Update state with data from the backend
      } catch (error) {
        if (error.response?.status === 401) {
          console.error('Unauthorized. Redirecting to login...');
          navigate('/login'); // Redirect to login if unauthorized
        } else {
          console.error('Error fetching user data:', error);
          setError('Failed to load profile. Please try again later.');
        }
      }
    };

    fetchUserData();
  }, [navigate]);

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  if (!userData) {
    return <p>Loading...</p>;
  }

  return (
    <div className="profile-container">
      <h1>Profile</h1>
      <div className="profile-details">
        <p><strong>Username:</strong> {userData.username}</p>
        <p><strong>Email:</strong> {userData.email}</p>
      </div>
      <div className="profile-actions">
        <button onClick={() => navigate('/update_email')}>Update email</button>
        <button onClick={() => navigate('/change_password')}>Update password</button>
        <button onClick={() => navigate('/delete_account')}>Delete account</button>
      </div>
    </div>
  );
};

export default Profile;
