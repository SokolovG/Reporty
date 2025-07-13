import axios from 'axios'
import {API_BASE_URL} from "$lib/config";

const apiClient = axios.create({
    baseURL: API_BASE_URL
})

apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem("authToken");
    if (token) {
         config.headers.Authorization = token;
    }
    config.headers["Content-Type"] = "application/json"
    console.log(config.headers)
    return config;
});

apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401 && !error.config.url.includes('/login')) {
            localStorage.removeItem('authToken');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default apiClient;
