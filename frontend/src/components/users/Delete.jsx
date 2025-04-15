import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api'; // Use the centralized Axios instance

const Delete = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [responseMessage, setResponseMessage] = useState(null);
  const navigate = useNavigate();

  const handleDelete = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post('/delete_user', { username, email, password });

      setResponseMessage(res.data.message);

      if (res.status === 200) {
        alert('Account deleted successfully.');
        navigate('/home'); // Redirect to the home page after successful deletion
      } else {
        console.error('Error deleting account:', res.data.message);
      }
    } catch (error) {
      console.error('Error:', error);
      setResponseMessage('Something went wrong. Please try again later.');
    }
  };

  return (
    <div className="delete-container">
      <h1>Delete Account</h1>
      <form onSubmit={handleDelete}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          className="form-input"
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="form-input"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="form-input"
        />
        <button type="submit" className="delete-button">Delete Account</button>
      </form>
      {responseMessage && (
        <div className="response-message">
          <p>{responseMessage}</p>
        </div>
      )}
    </div>
  );
};

export default Delete;
