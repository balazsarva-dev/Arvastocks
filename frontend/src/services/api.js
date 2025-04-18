import axios from 'axios';

// Log the baseURL for debugging
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'; // Fallback to localhost if VITE_API_URL is not set
console.log('API Base URL:', baseURL);

const api = axios.create({
  baseURL, // Dynamically set the base URL
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Include cookies if needed
});

export default api;
