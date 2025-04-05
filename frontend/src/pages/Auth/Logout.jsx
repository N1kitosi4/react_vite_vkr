import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    sessionStorage.removeItem("token");
    console.log("Logout: ", sessionStorage);

    navigate("/login", { replace: true });
  }, [navigate]);

  return (
    <div className="container">
      <h2>Выход...</h2>
      <p>Вы успешно вышли из системы.</p>
    </div>
  );
};

export default Logout;
