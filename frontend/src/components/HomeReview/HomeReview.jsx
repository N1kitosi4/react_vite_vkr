import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./style.css";
import defaultImg from "../../img/reviews/default_img.jpg";

const HomeReview = ({ review }) => {
  const {
    id,
    book_title,
    book_author,
    book_img,
    content,
    created_at,
    username,
    genre,
    average_review_rating,
    rating,
  } = review;

  const formattedDate = new Date(created_at).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  const imageURL = book_img ? `http://127.0.0.1:8000${book_img}` : defaultImg;
  const navigate = useNavigate();

  const [userRating, setUserRating] = useState(() => {
    return localStorage.getItem(`userRating-${id}`)
      ? Number(localStorage.getItem(`userRating-${id}`))
      : null;
  });
  const [avgRating, setAvgRating] = useState(average_review_rating || 0);
  const [hoverRating, setHoverRating] = useState(0);
  const [isUserAuthorized, setIsUserAuthorized] = useState(false); // Новый state для проверки авторизации

  const current_token = sessionStorage.getItem("token");

  const API_URL = import.meta.env.VITE_API_URL;

  // Проверка авторизации
  useEffect(() => {
    if (current_token) {
      setIsUserAuthorized(true);
      axios
        .get(`${API_URL}/reviews/get_rating/${id}`, {
          headers: { Authorization: `Bearer ${current_token}` },
        })
        .then((response) => {
          setUserRating(response.data.user_rating);
          localStorage.setItem(`userRating-${id}`, response.data.user_rating); // Обновляем localStorage
        })
        .catch((error) => {
          if (error.response?.status === 401) {
            setIsUserAuthorized(false); // Если ошибка 401, то скрываем блок рейтинга
          }
          console.log(
            "Ошибка при загрузке рейтинга:",
            error.response?.data || error.message
          );
        });
    }
  }, [id, current_token, API_URL]);

  // Функция для выставления рейтинга
  const handleRating = (newRating) => {
    if (!isUserAuthorized) {
      alert("Пожалуйста, авторизуйтесь для выставления рейтинга.");
      return;
    }

    const newUserRating = userRating === newRating ? 0 : newRating;


    axios
      .post(
        `${API_URL}/reviews/rate/${id}`,
        { rating: newRating },
        {
          headers: {
            Authorization: `Bearer ${current_token}`,
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        }
      )
      .then((response) => {
        setUserRating(response.data.user_rating);
        setAvgRating(response.data.average_review_rating);
        if (newUserRating === 0) {
          localStorage.setItem(`userRating-${id}`, 0); // Удаляем из localStorage при обнулении
          localStorage.removeItem(`userRating-${id}`); // Удаляем из localStorage при обнулении
        } else {
          localStorage.setItem(`userRating-${id}`, response.data.user_rating);
        }
      })
      .catch((error) =>
        console.log(
          "Ошибка при выставлении рейтинга:",
          error.response?.data || error.message
        )
      );
  };

  const shortenedContent =
    content.length > 150 ? content.slice(0, 150) + "..." : content;

  return (
    <li className="review">
      <img
        src={imageURL}
        alt="review img"
        className="review__img"
        onClick={() => navigate(`/review/${id}`)}
      />
      <h3 className="review__title">{book_title}</h3>
      <h4 className="review__author">{book_author}</h4>
      <p className="review__username">{username}</p>
      <div className="review__parts">
        <p className="review__genre">{genre}</p>
        <p className="review__date">{formattedDate}</p>
      </div>

      <p className="review__content">
        {shortenedContent}
        {/* Если контент был обрезан, показываем ссылку "Читать далее" */}
        {content.length > 150 && (
          <span
            className="read__more"
            onClick={() => navigate(`/review/${id}`)}
          >
            Читать далее
          </span>
        )}
      </p>

      <p className="review__book-rating">
        Рейтинг книги: ★{(rating || 0).toFixed(1)}
      </p>
      <p className="review__rating">
        Средний рейтинг отзыва: ★{avgRating.toFixed(1)}
      </p>

      {/* Блок с выставлением оценки только для авторизованных пользователей */}
      {isUserAuthorized && (
        <div className="review__user-rating">
          <span>Ваш рейтинг:</span>
          {[1, 2, 3, 4, 5].map((star) => (
            <span
              key={star}
              className={`star ${
                (hoverRating || userRating) >= star ? "active" : ""
              }`}
              onClick={() => handleRating(star)}
              onMouseEnter={() => setHoverRating(star)}
              onMouseLeave={() => setHoverRating(0)}
            >
              ★
            </span>
          ))}
        </div>
      )}
      {!isUserAuthorized && (
        <p className="review__unauthorized">
          Пожалуйста, авторизуйтесь для выставления рейтинга.
        </p>
      )}
    </li>
  );
};

export default HomeReview;
