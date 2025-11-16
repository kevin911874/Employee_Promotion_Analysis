import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
};

// Employees API
export const employeesAPI = {
  getAll: (params) => api.get('/employees', { params }),
  getById: (id) => api.get(`/employees/${id}`),
  create: (data) => api.post('/employees', data),
  update: (id, data) => api.put(`/employees/${id}`, data),
  delete: (id) => api.delete(`/employees/${id}`),
  bulkUpload: (formData) => 
    api.post('/employees/bulk-upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getStats: () => api.get('/employees/stats/summary'),
};

// Predictions API
export const predictionsAPI = {
  predictSingle: (data) => api.post('/predictions/predict', data),
  predictBatch: (employees) => api.post('/predictions/predict-batch', { employees }),
  getHistory: (employeeId) => api.get(`/predictions/history/${employeeId}`),
  getRecent: (limit = 10) => api.get('/predictions/recent', { params: { limit } }),
};

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get('/analytics/dashboard'),
  getTrainingScoreAnalysis: () => api.get('/analytics/training-score-analysis'),
  getPreviousRatingAnalysis: () => api.get('/analytics/previous-rating-analysis'),
  sensitivityAnalysis: (data) => api.post('/analytics/sensitivity-analysis', data),
  businessSimulation: (data) => api.post('/analytics/business-simulation', data),
  getRecommendations: () => api.get('/analytics/recommendations'),
};

export default api;
