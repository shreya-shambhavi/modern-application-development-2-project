import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export function setAuthenticationToken(token) {
  if (token) {
    apiClient.defaults.headers.common['Authentication-Token'] = `${token}`;
    console.log('Token set in axios headers:', apiClient.defaults.headers.common['Authentication-Token']); // Debug log
  } else {
    delete apiClient.defaults.headers.common['Authentication-Token'];
    console.log('Token removed from axios headers'); // Debug log
  }
}

export default apiClient;
