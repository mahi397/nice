// src/axios.js
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/', // Your Django backend base URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
