import axios from 'axios';

//creating custom axios instance configured for flask backend 
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:5000', // Update this if you deploy to a live server
  headers: {
    'Content-Type': 'application/json'
  }
}) 

//Request Interceptor : this runs before every single API call 
apiClient.interceptors.request.use(
    (config) => {
        //grab token from local storage (saved during login)
        const token = localStorage.getItem('auth_token');

        // If the user is logged in, attach the token to the exact header Flask expects
    if (token) {
      config.headers['Authentication-Token'] = token;
    }
    return config;
    },
    (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;