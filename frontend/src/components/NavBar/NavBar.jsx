import { NavLink } from "react-router-dom";

import BtnDark from "../BtnDark/BtnDark";

import "./style.css"


const NavBar = () => {

    const activeLink = "nav-list__link nav-list__link--active";
    const inactiveLink = "nav-list__link";

    return (
        <nav className="nav">
            <div className="container">
                <div className="nav-row">
                    <NavLink  to="/" className="logo">
                        <strong>📖 Book </strong>Reviews
                    </NavLink>

                    <BtnDark/>

                    <ul className="nav-list">

                        <li className="nav-list__item">
                            <NavLink to="/" className={({isActive}) => isActive ? activeLink : inactiveLink}>
                                Главная
                            </NavLink>
                        </li>

                        <li className="nav-list__item">
                            <NavLink to="/myreviews" className={({isActive}) => isActive ? activeLink : inactiveLink}>
                                Мои отзывы
                            </NavLink>
                        </li>

                        <li className="nav-list__item">
                            <NavLink to="/profile" className={({isActive}) => isActive ? activeLink : inactiveLink}>
                                Профиль
                            </NavLink>
                        </li>

                        <li className="nav-list__item">
                            <NavLink to="/recommendations" className={({isActive}) => isActive ? activeLink : inactiveLink}>
                                Рекомендации
                            </NavLink>
                        </li>

                        <li className="nav-list__item">
                            <NavLink to="/logout" className={({isActive}) => isActive ? activeLink : inactiveLink}>
                                Выйти
                            </NavLink>
                        </li>

                    </ul>
                </div>
            </div>
        </nav>
    );
}
 
export default NavBar;

