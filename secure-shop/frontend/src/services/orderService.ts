// src/services/orderService.ts
import axios from 'axios';
import type {
  Order,
  OrderItem,
  CreateOrderResponse,
} from "../index";
const API = import.meta.env.VITE_ORDER_API_URL || 'http://localhost:8002';

const api = axios.create({
  baseURL: API,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const createOrder = async (items: OrderItem[]): Promise<CreateOrderResponse> => {
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

export const updateOrderStatus = async (
  orderNumber: string,
  status: string,
  transactionId?: string
): Promise<Order> => {
  const response = await api.put(`/orders/${orderNumber}/status`, null, {
    params: { status, transaction_id: transactionId }
  });
  return response.data;
};