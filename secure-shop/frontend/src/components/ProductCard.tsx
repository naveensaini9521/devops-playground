import React from "react";
import { motion } from "framer-motion";
import { FaPlus, FaCheck } from "react-icons/fa";

interface ProductCardProps {
  name: string;
  price: number;
  image: string;
  onAdd: () => void;
  inCart?: boolean;
}

const ProductCard: React.FC<ProductCardProps> = ({
  name,
  price,
  image,
  onAdd,
  inCart,
}) => {
  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition"
    >
      <div className="relative overflow-hidden">
        <img
          src={image}
          alt={name}
          className="w-full h-64 object-cover hover:scale-105 transition duration-300"
        />
        <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-bold text-green-600">
          ₹{price}
        </div>
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800">{name}</h3>
        <p className="text-sm text-gray-500 mt-1">Premium quality</p>
        <button
          onClick={onAdd}
          className={`w-full mt-4 py-2 rounded-lg flex items-center justify-center gap-2 transition ${
            inCart
              ? "bg-green-100 text-green-600 hover:bg-green-200"
              : "bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700"
          }`}
        >
          {inCart ? (
            <>
              <FaCheck /> Added to Cart
            </>
          ) : (
            <>
              <FaPlus /> Add to Cart
            </>
          )}
        </button>
      </div>
    </motion.div>
  );
};

export default ProductCard;
