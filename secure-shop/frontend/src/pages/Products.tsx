// pages/Products.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createOrder } from "../services/orderService";
import { useAuth } from "../hooks/useAuth";

const products = [
  { name: "T-Shirt", price: 799 },
  { name: "Jeans", price: 1999 },
  { name: "Pajama", price: 999 },
  { name: "Hoodie", price: 2499 },
  { name: "Jacket", price: 3999 },
  { name: "Shoes", price: 3499 },
];

const Products = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [cart, setCart] = useState<{ name: string; quantity: number }[]>([]);
  const [loading, setLoading] = useState(false);

  const addToCart = (name: string) => {
    const existing = cart.find((item) => item.name === name);
    if (existing) {
      setCart(
        cart.map((item) =>
          item.name === name ? { ...item, quantity: item.quantity + 1 } : item,
        ),
      );
    } else {
      setCart([...cart, { name, quantity: 1 }]);
    }
  };

  const removeFromCart = (name: string) => {
    setCart(cart.filter((item) => item.name !== name));
  };

  const handleOrder = async () => {
    if (cart.length === 0) {
      alert("Cart is empty");
      return;
    }

    setLoading(true);
    try {
      const result = await createOrder(cart);
      alert(
        `Order created successfully!\nOrder Number: ${result.order_number}`,
      );
      setCart([]);
    } catch (error: any) {
      alert(error.response?.data?.detail || "Failed to create order");
    } finally {
      setLoading(false);
    }
  };

  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
  const totalAmount = cart.reduce((sum, item) => {
    const product = products.find((p) => p.name === item.name);
    return sum + (product?.price || 0) * item.quantity;
  }, 0);

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

      <div className="max-w-7xl mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6">Products</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {products.map((product) => (
            <div key={product.name} className="bg-white p-4 rounded-lg shadow">
              <h2 className="text-lg font-semibold">{product.name}</h2>
              <p className="text-green-600 font-bold text-xl">
                ₹{product.price}
              </p>
              <button
                onClick={() => addToCart(product.name)}
                className="mt-3 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
              >
                Add to Cart
              </button>
            </div>
          ))}
        </div>

        <div className="mt-8 bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-2">Cart ({totalItems} items)</h2>

          {cart.length === 0 ? (
            <p className="text-gray-500">Your cart is empty</p>
          ) : (
            <>
              {cart.map((item) => {
                const product = products.find((p) => p.name === item.name);
                return (
                  <div
                    key={item.name}
                    className="flex justify-between items-center border-b py-2"
                  >
                    <span>
                      {item.name} × {item.quantity}
                    </span>
                    <span className="font-semibold">
                      ₹{(product?.price || 0) * item.quantity}
                    </span>
                    <button
                      onClick={() => removeFromCart(item.name)}
                      className="text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </div>
                );
              })}
              <div className="mt-4 flex justify-between items-center">
                <span className="text-xl font-bold">Total: ₹{totalAmount}</span>
                <button
                  onClick={handleOrder}
                  disabled={loading}
                  className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition disabled:opacity-50"
                >
                  {loading ? "Processing..." : "Place Order"}
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Products;
