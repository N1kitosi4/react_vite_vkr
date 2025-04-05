import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

import defaultImg from "./../img/reviews/default_img.jpg";

const MyReview = () => {
  const { id } = useParams();

  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(null);
  const [error, setError] = useState(null);

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    const fetchReview = async () => {
      try {
        const response = await axios.get(
          `${API_URL}/reviews/review/${id}`
        );
        setReview(response.data);
        console.log(response.data);
      } catch (error) {
        setError("Ошибка загрузки отзыва");
        console.error("Ошибка:", error.response.data.detail);
      } finally {
        setLoading(false);
      }
    };

    fetchReview();
  }, [id, API_URL]);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p>{error}</p>;
  if (!review) return <p>Отзыв не найден</p>;

  const {
    book_title,
    book_author,
    book_img,
    content,
    rating,
    created_at,
    username,
    genre,
  } = review;
  const formattedDate = new Date(created_at).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  const imageURL = book_img ? `${API_URL}${book_img}` : defaultImg;

  return (
    <main className="section">
      <div className="container">
        <div className="review-details">
          <h1 className="title-1">Отзыв</h1>

          <button type="submit" disabled={loading}>
            {loading ? "Отправка..." : "Добавить отзыв"}
          </button>

          <div className="review-details__desc">
            <img
              src={imageURL || defaultImg}
              alt="review img"
              className="review-details__cover"
            />
            <h3 className="review__title">{book_title}</h3>
            <h4 className="review__author">{book_author}</h4>
            <p className="review__username">{username}</p>
            <div className="review__parts">
              <p className="review__genre">{genre}</p>
              <p className="review__date">{formattedDate}</p>
            </div>
            <p className="review__content">{content}</p>
            <p className="review__username">Оценка: ★{rating}</p>
          </div>
        </div>
      </div>
    </main>
  );
};

export default MyReview;
