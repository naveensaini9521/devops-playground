// src/services/paymentService.ts
import axios from 'axios';
import type { CreateOrderResponse } from "../index";
const API = import.meta.env.VITE_PAYMENT_API_URL || 'http://localhost:8003';

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

export const processPayment = async (data: PaymentRequest): Promise<Payment> => {
  const response = await api.post('/payment/process', data);
  return response.data;
};

export const getPayment = async (transactionId: string): Promise<Payment> => {
  const response = await api.get(`/payment/${transactionId}`);
  return response.data;
};

export const getPaymentsByOrder = async (orderNumber: string): Promise<Payment[]> => {
  const response = await api.get(`/payment/order/${orderNumber}`);
  return response.data;
};

export const getAllPayments = async (): Promise<Payment[]> => {
  const response = await api.get('/payment/');
  return response.data;
};