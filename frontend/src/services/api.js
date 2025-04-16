import axios from 'axios';

// Log the baseURL for debugging
const baseURL = import.meta.env.VITE_API_URL || 'https://arvastocks.com/api';
console.log('API Base URL:', baseURL);

const api = axios.create({
  baseURL, // Dynamically set the base URL
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Include cookies if needed
});

export default api;
