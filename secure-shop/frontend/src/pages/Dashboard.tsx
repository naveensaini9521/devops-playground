// pages/Dashboard.tsx
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const Dashboard = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-xl font-bold">OrderHub</h1>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto p-4">
        <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
        <p className="text-gray-600 mb-8">
          Welcome to the Order Management System
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => navigate("/products")}
            className="bg-blue-600 text-white p-6 rounded-lg hover:bg-blue-700 transition text-left"
          >
            <h2 className="text-xl font-semibold">Products</h2>
            <p className="text-blue-100">Browse and shop products</p>
          </button>

          <button
            onClick={() => navigate("/orders")}
            className="bg-green-600 text-white p-6 rounded-lg hover:bg-green-700 transition text-left"
          >
            <h2 className="text-xl font-semibold">My Orders</h2>
            <p className="text-green-100">View your order history</p>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
