import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import "./style.css";

const CreateReview = () => {
  const navigate = useNavigate();
  const token = sessionStorage.getItem("token");

  const savedReview = JSON.parse(sessionStorage.getItem("reviewData")) || {};

  const [bookTitle, setBookTitle] = useState(savedReview.bookTitle || "");
  const [bookAuthor, setBookAuthor] = useState(savedReview.bookAuthor || "");
  const [rating, setRating] = useState(savedReview.rating || 5);
  const [content, setContent] = useState(savedReview.content || "");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!token) {
      navigate("/login");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      sessionStorage.setItem(
        "reviewData",
        JSON.stringify({
          bookTitle,
          bookAuthor,
          rating,
          content,
        })
      );

      const response = await axios.post(
        "http://127.0.0.1:8000/reviews",
        { book_title: bookTitle, book_author: bookAuthor, rating, content },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      console.log("Отзыв успешно создан:", response.data);
      alert(
        "Отзыв успешно создан! Если он не отображается, обновите страницу."
      );

      // Отзыв успешно создан – удаляем данные из localStorage
      sessionStorage.removeItem("reviewData");

      navigate("/myreviews");
    } catch (err) {
      console.error("Ошибка:", err);

      if (err?.response?.status === 404) {
        navigate("/create-book", { state: { bookTitle, bookAuthor } });
      } else {
        setError("Ошибка при отправке отзыва, попробуйте снова.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="section">
      <div className="container">
        <h1 className="title-1">Добавить отзыв</h1>

        <form className="review-form" onSubmit={handleSubmit}>
          <label>
            Название книги:
            <input
              type="text"
              value={bookTitle}
              onChange={(e) => setBookTitle(e.target.value)}
              required
            />
          </label>

          <label>
            Автор книги:
            <input
              type="text"
              value={bookAuthor}
              onChange={(e) => setBookAuthor(e.target.value)}
              required
            />
          </label>

          <label>
            Оценка (1-5):
            <input
              type="number"
              value={rating}
              min="1"
              max="5"
              onChange={(e) => setRating(Number(e.target.value))}
              required
            />
          </label>

          <label>
            Текст отзыва:
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Отправка..." : "Добавить отзыв"}
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}
      </div>
    </main>
  );
};

export default CreateReview;
