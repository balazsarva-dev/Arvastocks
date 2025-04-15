import React, { useState } from 'react';
import api from '../../services/api'; // Use the centralized Axios instance

const Contact = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!name || !email || !message) {
      setErrorMessage('All fields are required.');
      return;
    }

    try {
      const response = await api.post('/contact', { name, email, message });

      setSuccessMessage(response.data.message || 'Your message has been sent successfully!');
      setErrorMessage('');
      setName('');
      setEmail('');
      setMessage('');
    } catch (error) {
      console.error('Error:', error);
      setErrorMessage(
        error.response?.data?.message || 'An error occurred. Please try again later.'
      );
      setSuccessMessage('');
    }
  };

  return (
    <div className="contact-container">
      <h2>Contact Us</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="form-input"
          placeholder="Enter your name"
          required
        />

        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="form-input"
          placeholder="Enter your email"
          required
        />

        <label htmlFor="message">Message:</label>
        <textarea
          id="message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="form-textarea fixed-size"
          placeholder="Enter your message"
          required
        ></textarea>

        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <button type="submit" className="contact-button">
          Send Message
        </button>
      </form>
    </div>
  );
};

export default Contact;
