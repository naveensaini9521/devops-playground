// src/index.ts
export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
}

export interface Product {
  name: string;
  price: number;
  image?: string;
}

export interface OrderItem {
  name: string;
  quantity: number;
  price?: number;
  subtotal?: number;
}

export interface Order {
  id: number;
  order_number: string;
  customer_name: string;
  customer_id: number;
  total_amount: number;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED' | 'CANCELLED';
  transaction_id: string | null;
  created_at: string;
  updated_at: string;
  items?: OrderItem[];
}

export interface Payment {
  id: number;
  order_number: string;
  customer_id: number;
  amount: number;
  transaction_id: string;
  payment_status: 'PENDING' | 'COMPLETED' | 'FAILED' | 'REFUNDED';
  payment_method: string;
  created_at: string;
  updated_at: string;
}

export interface PaymentRequest {
  order_number: string;
  customer_id: number;
  amount: number;
  payment_method?: string;
}

export interface PaymentHeaders {
  'X-Timestamp': string;
  'X-Signature': string;
  'Content-Type': string;
}

export interface PaymentRequestBody {
  order_number: string;
  customer_id: number;
  amount: number;
  timestamp: string;
}

export interface PaymentRequestData {
  headers: PaymentHeaders;
  body: PaymentRequestBody;
}

export interface CreateOrderResponse {
  message: string;
  order_number: string;
  customer: string;
  total_amount: number;
  status: string;
  items: OrderItem[];
  payment_request: PaymentRequestData;
}