// src/pages/Products.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createOrder } from "../services/orderService";
import { useAuth } from "../hooks/useAuth";
import PaymentModal from "../components/PaymentModal";
import type { CreateOrderResponse, Product } from "../index";
const PRODUCTS: Product[] = [
  { name: "T-Shirt", price: 799 },
  { name: "Jeans", price: 1999 },
  { name: "Pajama", price: 999 },
  { name: "Hoodie", price: 2499 },
  { name: "Jacket", price: 3999 },
  { name: "Shoes", price: 3499 },
  { name: "Track Pant", price: 1499 },
  { name: "Cap", price: 499 },
  { name: "Shorts", price: 899 },
  { name: "Sweater", price: 2299 },
];

const Products = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [cart, setCart] = useState<{ name: string; quantity: number }[]>([]);
  const [loading, setLoading] = useState(false);
  const [showPayment, setShowPayment] = useState(false);
  const [orderData, setOrderData] = useState<CreateOrderResponse | null>(null);

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

  const updateQuantity = (name: string, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(name);
      return;
    }
    setCart(
      cart.map((item) => (item.name === name ? { ...item, quantity } : item)),
    );
  };

  const handleOrder = async () => {
    if (cart.length === 0) {
      alert("Cart is empty");
      return;
    }

    setLoading(true);
    try {
      const result = await createOrder(cart);
      setOrderData(result);
      setShowPayment(true);
    } catch (error: any) {
      alert(error.response?.data?.detail || "Failed to create order");
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentSuccess = (transactionId: string) => {
    setShowPayment(false);
    setCart([]);
    setOrderData(null);
    navigate("/orders");
  };

  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
  const totalAmount = cart.reduce((sum, item) => {
    const product = PRODUCTS.find((p) => p.name === item.name);
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

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {PRODUCTS.map((product) => {
            const inCart = cart.find((item) => item.name === product.name);
            return (
              <div
                key={product.name}
                className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition"
              >
                <h2 className="text-lg font-semibold">{product.name}</h2>
                <p className="text-green-600 font-bold text-xl">
                  ₹{product.price}
                </p>
                <button
                  onClick={() => addToCart(product.name)}
                  className={`mt-3 w-full py-2 rounded transition ${
                    inCart
                      ? "bg-green-100 text-green-600 hover:bg-green-200"
                      : "bg-blue-600 text-white hover:bg-blue-700"
                  }`}
                >
                  {inCart ? "Add More" : "Add to Cart"}
                </button>
              </div>
            );
          })}
        </div>

        <div className="mt-8 bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-2">
            Cart ({totalItems} {totalItems === 1 ? "item" : "items"})
          </h2>

          {cart.length === 0 ? (
            <p className="text-gray-500">Your cart is empty</p>
          ) : (
            <>
              {cart.map((item) => {
                const product = PRODUCTS.find((p) => p.name === item.name);
                return (
                  <div
                    key={item.name}
                    className="flex justify-between items-center border-b py-2"
                  >
                    <div className="flex items-center gap-4">
                      <span className="font-medium">{item.name}</span>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() =>
                            updateQuantity(item.name, item.quantity - 1)
                          }
                          className="w-6 h-6 bg-gray-200 rounded hover:bg-gray-300"
                        >
                          -
                        </button>
                        <span className="w-8 text-center">{item.quantity}</span>
                        <button
                          onClick={() =>
                            updateQuantity(item.name, item.quantity + 1)
                          }
                          className="w-6 h-6 bg-gray-200 rounded hover:bg-gray-300"
                        >
                          +
                        </button>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
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

      {orderData && (
        <PaymentModal
          isOpen={showPayment}
          onClose={() => {
            setShowPayment(false);
            setOrderData(null);
          }}
          onSuccess={handlePaymentSuccess}
          orderData={orderData}
        />
      )}
    </div>
  );
};

export default Products;
