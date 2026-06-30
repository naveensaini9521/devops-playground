// src/pages/OrderDetails.tsx
import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { getOrder } from "../services/orderService";
import { getPaymentsByOrder } from "../services/paymentService";
import { useAuth } from "../hooks/useAuth";
import type { Order, Payment } from "../index";

const OrderDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [order, setOrder] = useState<Order | null>(null);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      loadOrder(parseInt(id));
    }
  }, [id]);

  const loadOrder = async (orderId: number) => {
    try {
      const data = await getOrder(orderId);
      setOrder(data);

      if (data.transaction_id) {
        try {
          const paymentData = await getPaymentsByOrder(data.order_number);
          setPayments(paymentData);
        } catch (error) {
          console.log("No payment details found");
        }
      }
    } catch (error) {
      alert("Failed to load order details");
      navigate("/orders");
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status?.toUpperCase()) {
      case "COMPLETED":
        return "bg-green-100 text-green-600";
      case "PENDING":
        return "bg-yellow-100 text-yellow-600";
      case "PROCESSING":
        return "bg-blue-100 text-blue-600";
      case "FAILED":
        return "bg-red-100 text-red-600";
      case "CANCELLED":
        return "bg-gray-100 text-gray-600";
      default:
        return "bg-gray-100 text-gray-600";
    }
  };

  const getPaymentStatusColor = (status: string) => {
    switch (status?.toUpperCase()) {
      case "COMPLETED":
        return "bg-green-100 text-green-600";
      case "PENDING":
        return "bg-yellow-100 text-yellow-600";
      case "FAILED":
        return "bg-red-100 text-red-600";
      case "REFUNDED":
        return "bg-purple-100 text-purple-600";
      default:
        return "bg-gray-100 text-gray-600";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
            <h1 className="text-xl font-bold">OrderHub</h1>
          </div>
        </nav>
        <div className="flex justify-center items-center h-64">
          <div className="text-gray-500">Loading...</div>
        </div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
            <h1
              className="text-xl font-bold cursor-pointer"
              onClick={() => navigate("/dashboard")}
            >
              OrderHub
            </h1>
            <button
              onClick={() => {
                logout();
                navigate("/");
              }}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </nav>
        <div className="max-w-4xl mx-auto p-4 text-center">
          <p className="text-gray-500">Order not found</p>
          <Link to="/orders" className="text-blue-600 hover:underline">
            Back to Orders
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
          <h1
            className="text-xl font-bold cursor-pointer"
            onClick={() => navigate("/dashboard")}
          >
            OrderHub
          </h1>
          <button
            onClick={() => {
              logout();
              navigate("/");
            }}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto p-4">
        <Link
          to="/orders"
          className="text-blue-600 hover:underline mb-4 inline-block"
        >
          ← Back to Orders
        </Link>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-2xl font-bold">Order Details</h1>
              <p className="text-gray-500">Order #{order.order_number}</p>
            </div>
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                order.status,
              )}`}
            >
              {order.status || "PENDING"}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded">
              <p className="text-sm text-gray-500">Customer</p>
              <p className="font-semibold">{order.customer_name}</p>
              <p className="text-sm text-gray-500">ID: #{order.customer_id}</p>
            </div>

            <div className="bg-gray-50 p-4 rounded">
              <p className="text-sm text-gray-500">Total Amount</p>
              <p className="text-2xl font-bold text-green-600">
                ₹{order.total_amount}
              </p>
            </div>

            <div className="bg-gray-50 p-4 rounded">
              <p className="text-sm text-gray-500">Created At</p>
              <p className="font-medium">
                {new Date(order.created_at).toLocaleString()}
              </p>
            </div>

            <div className="bg-gray-50 p-4 rounded">
              <p className="text-sm text-gray-500">Transaction ID</p>
              <p className="font-medium font-mono">
                {order.transaction_id || "Pending"}
              </p>
            </div>
          </div>

          <div className="mt-6 bg-gray-50 p-4 rounded">
            <p className="text-sm text-gray-500">Last Updated</p>
            <p className="font-medium">
              {new Date(order.updated_at).toLocaleString()}
            </p>
          </div>

          {payments.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-3">Payment Details</h3>
              <div className="space-y-2">
                {payments.map((payment) => (
                  <div
                    key={payment.id}
                    className="bg-gray-50 p-4 rounded border"
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="text-sm text-gray-500">Transaction ID</p>
                        <p className="font-mono text-sm">
                          {payment.transaction_id}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-500">Status</p>
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${getPaymentStatusColor(
                            payment.payment_status,
                          )}`}
                        >
                          {payment.payment_status}
                        </span>
                      </div>
                    </div>
                    <div className="flex justify-between mt-2">
                      <div>
                        <p className="text-sm text-gray-500">Amount</p>
                        <p className="font-semibold">₹{payment.amount}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Method</p>
                        <p className="font-medium">
                          {payment.payment_method || "CARD"}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OrderDetails;
