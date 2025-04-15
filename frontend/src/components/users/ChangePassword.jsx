import React, { useState } from 'react';
import api from '../../services/api'; // Use the centralized Axios instance

const ChangePassword = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!oldPassword || !newPassword) {
      setErrorMessage('Both fields are required.');
      return;
    }

    try {
      const response = await api.post('/update_user_password', {
        old_password: oldPassword,
        new_password: newPassword,
      });

      setSuccessMessage('Password updated successfully!');
      setErrorMessage('');
      setOldPassword('');
      setNewPassword('');
    } catch (error) {
      console.error('Error:', error);
      setErrorMessage(
        error.response?.data?.message || 'An error occurred. Please try again later.'
      );
      setSuccessMessage('');
    }
  };

  return (
    <div className="change-password-container">
      <h2>Change Password</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="oldPassword">Old Password:</label>
        <input
          type="password"
          id="old_password"
          value={oldPassword}
          onChange={(e) => setOldPassword(e.target.value)}
          className="form-input"
          placeholder="Enter your old password"
          required
        />

        <label htmlFor="newPassword">New Password:</label>
        <input
          type="password"
          id="new_password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          className="form-input"
          placeholder="Enter your new password"
          required
        />

        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <button type="submit" className="change-password-button">
          Update Password
        </button>
      </form>
    </div>
  );
};

export default ChangePassword;
