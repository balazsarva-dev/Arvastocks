import React, { useState } from 'react';
import api from '../../services/api';
import * as yup from 'yup';

const passwordSchema = yup.object().shape({
  old_password: yup.string().required('Old password is required'),
  new_password: yup
    .string()
    .min(8, 'New password must be at least 8 characters')
    .required('New password is required'),
});

const ChangePassword = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await passwordSchema.validate({ old_password: oldPassword, new_password: newPassword });
      const response = await api.post('/update_user_password', {
        old_password: oldPassword,
        new_password: newPassword,
      });

      setSuccessMessage('Password updated successfully!');
      setErrorMessage('');
      setOldPassword('');
      setNewPassword('');
    } catch (error) {
      setErrorMessage(
        error.name === 'ValidationError'
          ? error.message
          : error.response?.data?.message || 'An error occurred. Please try again later.'
      );
      setSuccessMessage('');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="form-container">
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

        <button type="submit" className="register-button" disabled={isLoading}>
          {isLoading ? 'Updating...' : 'Update Password'}
        </button>
      </form>
    </div>
  );
};

export default ChangePassword;