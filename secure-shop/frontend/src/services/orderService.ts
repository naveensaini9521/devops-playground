// services/orderService.ts
import axios from 'axios';

const API = import.meta.env.VITE_ORDER_API_URL || 'http://localhost:8002';

const api = axios.create({
  baseURL: API,
  headers: { 
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Add token to every request
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

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export interface OrderItem {
  name: string;
  quantity: number;
}

export interface Order {
  id: number;
  order_number: string;
  customer_name: string;
  customer_id: number;
  total_amount: number;
  status: string;
  transaction_id: string | null;
  created_at: string;
  updated_at: string;
}

export const createOrder = async (items: OrderItem[]) => {
  const response = await api.post('/orders', { items });
  return response.data;
};

export const getOrders = async (): Promise<Order[]> => {
  const response = await api.get('/orders');
  return response.data;
};

export const getOrder = async (id: number): Promise<Order> => {
  const response = await api.get(`/orders/${id}`);
  return response.data;
};