import axios from 'axios';

// 从 localStorage 获取当前用户名
// 注意：这里不用 hook，因为 api.ts 是普通 js 文件
const getUsername = () => localStorage.getItem('aichef_username') || 'default';

const api = axios.create({
    baseURL: '', // 使用相对路径，Vite 代理会处理
});

// 请求拦截器：自动注入 X-Username
api.interceptors.request.use((config) => {
    config.headers['X-Username'] = getUsername();
    return config;
});

export default api;
