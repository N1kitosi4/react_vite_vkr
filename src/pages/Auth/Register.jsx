// import { useState } from "react";
// import { NavLink, useNavigate } from "react-router-dom";
// import axios from "axios";
// import { ToastContainer, toast } from "react-toastify";
// import "react-toastify/dist/ReactToastify.css";
// import "./style.css";

// const Register = () => {
//   const navigate = useNavigate();
//   const [formData, setFormData] = useState({
//     email: "",
//     username: "",
//     password: "",
//     confirmPassword: "",
//   });
//   const [loading, setLoading] = useState(false);

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     if (formData.password !== formData.confirmPassword) {
//       toast.error("Пароли не совпадают");
//       return;
//     }

//     setLoading(true);
//     try {
//       const response = await axios.post("http://127.0.0.1:8000/users/register", {
//         email: formData.email,
//         username: formData.username,
//         password: formData.password,
//       });

//       toast.success("Перейдите на почту, Вам пришло письмо.");
//       setTimeout(() => navigate("/login"), 3000);
//     } catch (err) {
//       toast.error(err.response?.data?.detail || "Ошибка регистрации");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="container">
//       <ToastContainer position="top-right" autoClose={3000} />
//       <div className="auth-container">
//         <h2>Регистрация</h2>
//         <form className="auth-form" onSubmit={handleSubmit}>
//           <div className="form-group">
//             <label htmlFor="email">Электронная почта</label>
//             <input
//               type="email"
//               id="email"
//               name="email"
//               placeholder="Введите вашу почту"
//               required
//               value={formData.email}
//               onChange={handleChange}
//             />
//           </div>
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
//           <div className="form-group">
//             <label htmlFor="confirm-password">Подтвердите пароль</label>
//             <input
//               type="password"
//               id="confirm-password"
//               name="confirmPassword"
//               placeholder="Повторите пароль"
//               required
//               value={formData.confirmPassword}
//               onChange={handleChange}
//             />
//           </div>

//           <button type="submit" className="btn-auth" disabled={loading}>
//             {loading ? "Регистрация..." : "Зарегистрироваться"}
//           </button>

//           <div className="auth-link">
//             <p>
//               Уже есть аккаунт? <NavLink to="/login">Войти</NavLink>
//             </p>
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// };

// export default Register;


import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./style.css";

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    password: "",
    confirmPassword: "",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      toast.error("Пароли не совпадают");
      return;
    }

    setLoading(true);
    try {
      await axios.post("http://127.0.0.1:8000/users/register", {
        email: formData.email,
        username: formData.username,
        password: formData.password,
      });

      toast.success("Перейдите на почту, Вам пришло письмо.");
      setTimeout(() => navigate("/login"), 3000);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Ошибка регистрации");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <ToastContainer position="top-right" autoClose={1500} />
      <div className="auth-container">
        <h2>Регистрация</h2>
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Электронная почта</label>
            <input
              type="email"
              id="email"
              name="email"
              placeholder="Введите вашу почту"
              required
              value={formData.email}
              onChange={handleChange}
            />
          </div>
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
          <div className="form-group">
            <label htmlFor="confirm-password">Подтвердите пароль</label>
            <input
              type="password"
              id="confirm-password"
              name="confirmPassword"
              placeholder="Повторите пароль"
              required
              value={formData.confirmPassword}
              onChange={handleChange}
            />
          </div>

          <button type="submit" className="btn-auth" disabled={loading}>
            {loading ? "Регистрация..." : "Зарегистрироваться"}
          </button>

          <div className="auth-link">
            <p>
              Уже есть аккаунт? <NavLink to="/login">Войти</NavLink>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
