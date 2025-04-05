import "./style.css";

import vk from "./../../img/icons/vk.svg";
import ok from "./../../img/icons/ok.svg";
import telegram from "./../../img/icons/telegram.svg";
import yandex from "./../../img/icons/yandex.svg";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer__wrapper">
          <ul className="social">
            <li className="social__item">
              <a href="#!">
                <img src={vk} alt="Link" />
              </a>
            </li>
            <li className="social__item">
              <a href="#!">
                <img src={ok} alt="Link" />
              </a>
            </li>
            <li className="social__item">
              <a href="#!">
                <img src={telegram} alt="Link" />
              </a>
            </li>
            <li className="social__item">
              <a href="#!">
                <img src={yandex} alt="Link" />
              </a>
            </li>
          </ul>
          <div className="copyright">
            <p>© 2025 Book Review</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
