import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

api.interceptors.request.use((config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
});

api.interceptors.response.use(
    (response) => {
        console.log(`[API] ${response.config.method?.toUpperCase()} ${response.config.url} -> ${response.status}`);
        return response;
    },
    (error) => {
        console.error(
            "[API] Request failed",
            error?.config?.method?.toUpperCase(),
            error?.config?.url,
            error?.response?.status,
            error?.message
        );
        return Promise.reject(error);
    }
);

export default api;
