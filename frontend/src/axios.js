import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:5000', 
  headers: {
    'Content-Type': 'application/json'
  }
}) 

 
apiClient.interceptors.request.use(
    (config) => {
        
        const token = localStorage.getItem('auth_token');

        
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