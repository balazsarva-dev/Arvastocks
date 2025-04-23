import React, { useState } from 'react';
import api from '../../services/api';
import * as yup from 'yup';

const emailSchema = yup.object().shape({
  new_email: yup.string().email('Invalid email format').required('Email is required'),
  password: yup.string().required('Password is required'),
});

const ChangeEmail = () => {
  const [newEmail, setNewEmail] = useState('');
  const [password, setPassword] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!newEmail || !password) {
      setErrorMessage('Both fields are required.');
      return;
    }

    setIsLoading(true); // Show loading state

    try {
      await emailSchema.validate({ new_email: newEmail, password });
      const response = await api.post('/update_user_email', {
        new_email: newEmail,
        password,
      });

      setSuccessMessage(response.data.message || 'Email updated successfully!');
      setErrorMessage('');
      setNewEmail('');
      setPassword('');
    } catch (error) {
      console.error('Error:', error);
      setErrorMessage(
        error.response?.data?.message || 'An error occurred. Please try again later.'
      );
      setSuccessMessage('');
    } finally {
      setIsLoading(false); // Hide loading state
    }
  };

  return (
    <div className="form-container">
      <h2>Update Email</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="newEmail">New Email:</label>
        <input
          type="email"
          id="newEmail"
          value={newEmail}
          onChange={(e) => setNewEmail(e.target.value)}
          className="form-input"
          placeholder="Enter your new email"
          required
        />

        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="form-input"
          placeholder="Enter your password"
          required
        />

        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <button type="submit" className="register-button" disabled={isLoading}>
          {isLoading ? 'Updating...' : 'Update Email'}
        </button>
      </form>
    </div>
  );
};

export default ChangeEmail;
