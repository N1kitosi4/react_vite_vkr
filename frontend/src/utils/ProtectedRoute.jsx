import { Navigate, Outlet } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

const ProtectedRoute = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const token = sessionStorage.getItem("token");

  useEffect(() => {
    const checkAuth = async () => {
      if (!token) {
        setIsAuthenticated(false);
        return;
      }

      try {
        await axios.get("http://127.0.0.1:8000/users/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setIsAuthenticated(true);
      } catch (error) {
        console.error("Ошибка авторизации:", error);
        sessionStorage.removeItem("token");
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, [token]);

  if (isAuthenticated === null) return <p>Загрузка...</p>;
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoute;
