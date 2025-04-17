import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../../services/api'; // Use the centralized Axios instance

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false); // State for "Remember Me"
  const [error, setError] = useState(null); // State for error messages
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/login', {
        username,
        password,
      });

      const data = res.data;
      if (data.success) {
        // Save user data to localStorage
        localStorage.setItem(
          'user',
          JSON.stringify({
            username: data.username,
            email: data.email,
            loginDate: new Date().toLocaleString(),
          })
        );

        // Redirect to the profile page
        navigate('/profile');
      } else {
        setError(data.message || 'Login failed. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred. Please try again later.');
    }
  };

  return (
    <div className="form-container">
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          id="login-username"
          name="username"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          className="form-input"
        />
        <input
          type="password"
          id="login-password"
          name="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="form-input"
          autoComplete="current-password"
        />
        <div className="checkbox-container">
          <input
            type="checkbox"
            id="rememberMe"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
          />
          <label htmlFor="rememberMe">Remember me</label>
        </div>
        <button type="submit" className="form-button">
          Login
        </button>
      </form>
      <div className="register-container">
        <p>Don't have an account?</p>
        <Link to="/register">
          <button className="register-button">Register</button>
        </Link>
      </div>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default Login;