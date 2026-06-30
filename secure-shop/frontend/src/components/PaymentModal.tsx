// src/components/PaymentModal.tsx
import React, { useState } from "react";
import { processPayment } from "../services/paymentService";
import type { CreateOrderResponse } from "../index";
interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (transactionId: string) => void;
  orderData: CreateOrderResponse;
}

const PaymentModal: React.FC<PaymentModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  orderData,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [paymentMethod, setPaymentMethod] = useState("CARD");

  if (!isOpen) return null;

  const handlePayment = async () => {
    setLoading(true);
    setError(null);

    try {
      const paymentData = {
        order_number: orderData.order_number,
        customer_id: Number(orderData.payment_request.body.customer_id),
        amount: orderData.total_amount,
        payment_method: paymentMethod,
      };

      const result = await processPayment(paymentData);
      onSuccess(result.transaction_id);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || "Payment failed. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Complete Payment</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>

        <div className="space-y-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500">Order Number</p>
            <p className="font-semibold">{orderData.order_number}</p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500">Total Amount</p>
            <p className="text-2xl font-bold text-green-600">
              ₹{orderData.total_amount}
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Payment Method
            </label>
            <select
              value={paymentMethod}
              onChange={(e) => setPaymentMethod(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="CARD">Credit/Debit Card</option>
              <option value="UPI">UPI</option>
              <option value="NETBANKING">Net Banking</option>
              <option value="WALLET">Wallet</option>
            </select>
          </div>

          {error && (
            <div className="bg-red-50 text-red-500 p-3 rounded-lg text-sm border border-red-200">
              {error}
            </div>
          )}

          <div className="flex gap-3 mt-6">
            <button
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              onClick={handlePayment}
              disabled={loading}
              className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition disabled:opacity-50"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg
                    className="animate-spin h-4 w-4 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Processing...
                </span>
              ) : (
                "Pay Now"
              )}
            </button>
          </div>

          <p className="text-xs text-gray-500 text-center mt-4">
            Secure payment powered by HMAC signature verification
          </p>
        </div>
      </div>
    </div>
  );
};

export default PaymentModal;
