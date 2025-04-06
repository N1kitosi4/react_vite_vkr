import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../utils/AuthContext";

const Logout = () => {
  const navigate = useNavigate();
    const { logout } = useAuth(); // получаем login из контекста

  useEffect(() => {
    logout("token");
    console.log("Logout: ", sessionStorage);

    navigate("/login", { replace: true });
  }, [navigate, logout]);

  return (
    <div className="container">
      <h2>Выход...</h2>
      <p>Вы успешно вышли из системы.</p>
    </div>
  );
};

export default Logout;
