import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data as any;
          localStorage.setItem('access_token', access);

          // Retry the original request
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (username: string, password: string) =>
    api.post('/auth/login/', { username, password }),
  refresh: (refresh: string) =>
    api.post('/auth/refresh/', { refresh }),
};

// Vendor API
export const vendorAPI = {
  getVendors: (params?: any) => 
    api.get('/vendors/', { params }),
  getVendor: (id: number) => 
    api.get(`/vendors/${id}/`),
  createVendor: (data: any) => 
    api.post('/vendors/', data),
  updateVendor: (id: number, data: any) => 
    api.patch(`/vendors/${id}/`, data),
  deleteVendor: (id: number) => 
    api.delete(`/vendors/${id}/`),
  getVendorServices: (id: number) => 
    api.get(`/vendors/${id}/services/`),
  getVendorsWithActiveServices: () => 
    api.get('/vendors/with-active-services/'),
};

// Service API
export const serviceAPI = {
  getServices: (params?: any) => 
    api.get('/services/', { params }),
  getService: (id: number) => 
    api.get(`/services/${id}/`),
  createService: (data: any) => 
    api.post('/services/', data),
  updateService: (id: number, data: any) => 
    api.patch(`/services/${id}/`, data),
  deleteService: (id: number) => 
    api.delete(`/services/${id}/`),
  updateServiceStatus: (id: number, status: string) =>
    api.patch(`/services/${id}/status/`, { status }),
  getExpiringSoon: () => 
    api.get('/services/expiring-soon/'),
  getPaymentDueSoon: () => 
    api.get('/services/payment-due-soon/'),
};

// Dashboard API
export const dashboardAPI = {
  getStats: () => 
    api.get('/dashboard/stats/'),
  getReminders: () => 
    api.get('/reminders/'),
};

export default api;
