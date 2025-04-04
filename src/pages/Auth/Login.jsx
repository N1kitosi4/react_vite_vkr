// import { useState } from "react";

// import { NavLink, useNavigate } from "react-router-dom";

// import axios from "axios";

// import "./style.css";

// const Login = () => {
//   const navigate = useNavigate();
//   const [formData, setFormData] = useState({
//     username: "",
//     password: "",
//   });
//   const [error, setError] = useState(null);
//   const [loading, setLoading] = useState(false);

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setError(null);
//     setLoading(true);

//     try {
//       const response = await axios.post(
//         "http://127.0.0.1:8000/users/login",
//         new URLSearchParams({
//           username: formData.username,
//           password: formData.password,
//         }),
//         {
//           headers: { "Content-Type": "application/x-www-form-urlencoded" },
//         }
//       );

//       const { access_token } = response.data;
//       sessionStorage.setItem("token", access_token); // Сохраняем токен в localStorage
//       console.log("Login: ", sessionStorage);
//       console.log("Успешный вход:", access_token);
//       navigate("/"); // Перенаправляем на главную страницу
//     } catch (err) {
//       console.error("Ошибка входа:", err.response?.data?.detail || err.message);
//       setError(err.response?.data?.detail || "Ошибка авторизации");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="container">
//       <div className="auth-container">
//         <h2>Вход в систему</h2>
//         <form className="auth-form" onSubmit={handleSubmit}>
//           <div className="form-group">
//             <label htmlFor="username">Имя пользователя</label>
//             <input
//               type="text"
//               id="username"
//               name="username"
//               placeholder="Введите имя пользователя"
//               required
//               value={formData.username}
//               onChange={handleChange}
//             />
//           </div>

//           <div className="form-group">
//             <label htmlFor="password">Пароль</label>
//             <input
//               type="password"
//               id="password"
//               name="password"
//               placeholder="Введите пароль"
//               required
//               value={formData.password}
//               onChange={handleChange}
//             />
//           </div>

//           {error && <p className="error-message">{error}</p>}

//           <button type="submit" className="btn-auth" disabled={loading}>
//             {loading ? "Вход..." : "Войти"}
//           </button>

//           <div className="auth-link">
//             <p>
//               Нет аккаунта? <NavLink to="/register">Зарегистрироваться</NavLink>
//             </p>
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// };

// export default Login;


import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./style.css";

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/users/login",
        new URLSearchParams({
          username: formData.username,
          password: formData.password,
        }),
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );

      const { access_token } = response.data;

      // Проверка верификации пользователя
      if (!response.data.access_token) {
        toast.error("Ваш аккаунт не верифицирован. Проверьте почту для подтверждения.");
        return;
      }

      // Сохраняем токен в sessionStorage
      sessionStorage.setItem("token", access_token);
      console.log("Login: ", sessionStorage);
      console.log("Успешный вход:", access_token);

      navigate("/"); // Перенаправляем на главную страницу
    } catch (err) {
      console.error("Ошибка входа:", err.response?.data?.detail || err.message);
      setError(err.response?.data?.detail || "Ошибка авторизации");
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
              placeholder="Введите имя пользователя"
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
              placeholder="Введите пароль"
              required
              value={formData.password}
              onChange={handleChange}
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button type="submit" className="btn-auth" disabled={loading}>
            {loading ? "Вход..." : "Войти"}
          </button>

          <div className="auth-link">
            <p>
              Нет аккаунта? <NavLink to="/register">Зарегистрироваться</NavLink>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
