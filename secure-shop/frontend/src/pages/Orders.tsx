// pages/Orders.tsx
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getOrders, type Order } from "../services/orderService";
import { useAuth } from "../hooks/useAuth";

const Orders = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const data = await getOrders();
      setOrders(data);
    } catch (error) {
      alert("Failed to load orders");
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
      case "CANCELLED":
        return "bg-red-100 text-red-600";
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

      <div className="max-w-6xl mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6">My Orders</h1>

        {orders.length === 0 ? (
          <div className="bg-white p-8 rounded-lg shadow text-center">
            <p className="text-gray-500 mb-4">
              You haven't placed any orders yet
            </p>
            <Link
              to="/products"
              className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
            >
              Start Shopping
            </Link>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="p-3 text-left text-sm font-medium text-gray-600">
                    Order #
                  </th>
                  <th className="p-3 text-left text-sm font-medium text-gray-600">
                    Customer
                  </th>
                  <th className="p-3 text-left text-sm font-medium text-gray-600">
                    Total
                  </th>
                  <th className="p-3 text-left text-sm font-medium text-gray-600">
                    Status
                  </th>
                  <th className="p-3 text-left text-sm font-medium text-gray-600">
                    Date
                  </th>
                  <th className="p-3 text-left text-sm font-medium text-gray-600">
                    Action
                  </th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id} className="border-t hover:bg-gray-50">
                    <td className="p-3 font-medium">{order.order_number}</td>
                    <td className="p-3">{order.customer_name}</td>
                    <td className="p-3 font-semibold text-green-600">
                      ₹{order.total_amount}
                    </td>
                    <td className="p-3">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}
                      >
                        {order.status || "PENDING"}
                      </span>
                    </td>
                    <td className="p-3 text-sm text-gray-500">
                      {new Date(order.created_at).toLocaleDateString()}
                    </td>
                    <td className="p-3">
                      <Link
                        to={`/orders/${order.id}`}
                        className="text-blue-600 hover:underline"
                      >
                        View
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Orders;
