import { useState, useEffect } from "react";
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import { useAuth } from "./../../utils/AuthContext";

import "./style.css";

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const { login } = useAuth(); // получаем login из контекста
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const message = queryParams.get("message");

    if (message === "email_verified") {
      toast.success("Ваша почта успешно подтверждена! Пожалуйста, войдите в аккаунт.");
    }
  }, [location]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
  
    try {
      const response = await axios.post(
        `${API_URL}/users/login`,
        new URLSearchParams({
          username: formData.username,
          password: formData.password,
        }),
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );
  
      const { access_token } = response.data;
  
      if (!access_token) {
        toast.error("Ваша учетная запись не подтверждена. Пожалуйста, проверьте свою электронную почту.");
        return;
      }

  
      login(access_token); // ✅ контекст авторизации
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Login error.");
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div className="container">
      <ToastContainer position="top-right" autoClose={3000} />
      <div className="auth-container">
        <h2>Вход в систему</h2>
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Имя пользователя</label>
            <input
              type="text"
              id="username"
              name="username"
              placeholder="Введите Ваше имя"
              required
              value={formData.username}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              name="password"
              placeholder="Введите Ваш пароль"
              required
              value={formData.password}
              onChange={handleChange}
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button type="submit" className="btn-auth" disabled={loading}>
            {loading ? "Авторизация..." : "Вход"}
          </button>

          <div className="auth-link">
            <p>
              Ещё нет аккаунта? <NavLink to="/register">Зарегистрироваться</NavLink>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
