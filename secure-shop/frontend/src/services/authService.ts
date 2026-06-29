// services/authService.ts
import axios from 'axios';

const API = import.meta.env.VITE_AUTH_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API,
  headers: { 
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  const response = await api.post('/auth/login', data);
  return response.data;
};

export const register = async (data: RegisterRequest) => {
  const response = await api.post('/auth/register', data);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('token');
};