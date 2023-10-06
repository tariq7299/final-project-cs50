// api.js
import axios from 'axios';

// Create a new Axios instance with a base URL
const apiInstance = axios.create({
  baseURL: '/api',  // Prefix all requests with '/api'
});

export default apiInstance;
