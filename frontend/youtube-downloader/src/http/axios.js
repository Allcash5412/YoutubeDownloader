import axios from "axios";
// import config from "tailwindcss/defaultConfig";
// import Cookies from 'js-cookie';
export const API_URL = 'http://127.0.0.1:8000'

export default axios.create({
    baseURL: API_URL
});

export const axiosPrivate = axios.create({
    baseURL: API_URL,
    headers: {'Content-Type': 'application/json'},
    withCredentials: true
});
// api.interceptors.request.use((config) => {
//     config.headers.Authorization = `Bearer ${Cookies.get()}`
// })

