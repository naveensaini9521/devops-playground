import React from "react";
import Navbar from "../components/Navbar";

interface Props {
  children: React.ReactNode;
}

const MainLayout: React.FC<Props> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <main className="max-w-7xl mx-auto p-8">{children}</main>
    </div>
  );
};

export default MainLayout;
