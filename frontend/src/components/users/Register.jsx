import React, { useState } from 'react';
import api from '../../services/api'; // Adjusted the import path

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/register', {
        username,
        email,
        password,
      });

      setResponse(res.data);
      alert('Registration successful!'); // Keep this as requested
    } catch (error) {
      // Improved error handling
      setError(error.response?.data?.message || 'Failed to register. Please try again.');
    }
  };

  return (
    <div className="form-container">
      <h1>Register</h1>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          id="username"
          name="username"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          className="form-input"
	  autocomplete="username"
        />
        <input
          type="email"
          id="email"
          name="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="form-input"
	  autocomplete="email"
        />
        <input
          type="password"
          id="password"
          name="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="form-input"
	  autocomplete="new-password"
        />
        <button type="submit" className='form-button'>Register</button>
      </form>
      {response && (
        <div>
          <h2>Response:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default Register;
