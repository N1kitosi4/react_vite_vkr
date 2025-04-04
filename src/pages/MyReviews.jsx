import { useEffect, useState } from "react";
import axios from "axios";
import { NavLink, useNavigate } from "react-router-dom";
import defaultImg from "./../img/reviews/default_img.jpg";

const MyReviews = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingReviewId, setEditingReviewId] = useState(null);
  const [updatedData, setUpdatedData] = useState({});
  const navigate = useNavigate();
  const token = sessionStorage.getItem("token");

  useEffect(() => {
    const fetchReviews = async () => {
      if (!token) {
        navigate("/login");
        return;
      }

      try {
        const { data } = await axios.get(
          "http://127.0.0.1:8000/reviews/my_reviews",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setReviews(data);
      } catch (err) {
        console.error("Ошибка загрузки отзывов:", err);
        setError("Ошибка загрузки отзывов");
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, [navigate, token]);

  const handleEdit = (review) => {
    alert(
      "Обновите рейтинг или свой отзыв. Учтите, что рейтинг должен быть от 1 до 5 включительно."
    );
    setEditingReviewId(review.id);
    setUpdatedData({
      rating: review.rating,
      content: review.content,
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUpdatedData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSave = async (reviewId) => {
    try {
      await axios.put(
        `http://127.0.0.1:8000/reviews/${reviewId}`,
        updatedData,

        { headers: { Authorization: `Bearer ${token}` } }
      );

      setReviews((prevReviews) =>
        prevReviews.map((review) =>
          review.id === reviewId ? { ...review, ...updatedData } : review
        )
      );

      setEditingReviewId(null);
    } catch (err) {
      console.error("Ошибка сохранения изменений:", err);
    }
  };

  const handleDelete = async (reviewId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/reviews/${reviewId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setReviews((prevReviews) =>
        prevReviews.filter((review) => review.id !== reviewId)
      );
    } catch (err) {
      console.error("Ошибка удаления отзыва:", err);
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p className="error-message">{error}</p>;

  return (
    <main className="section">
      <div className="container">
        <h1 className="title-1">Мои отзывы</h1>

        {reviews.length === 0 ? (
          <h1 className="title-1">У вас пока нет отзывов.</h1>
        ) : (
          <ul className="reviews">
            {reviews.map((review) => (
              <li key={review.id} className="review">
                <NavLink to={`/review/${review.id}`}>
                  <div className="review__img">
                    <img
                      src={
                        review.book_img
                          ? `http://127.0.0.1:8000${review.book_img}`
                          : defaultImg
                      }
                      alt="Book Cover"
                    />
                  </div>
                </NavLink>
                {editingReviewId === review.id ? (
                  <div>
                    <input
                      type="number"
                      name="rating"
                      value={updatedData.rating}
                      onChange={handleChange}
                    />
                    <textarea
                      name="content"
                      value={updatedData.content}
                      onChange={handleChange}
                    />
                    <button onClick={() => handleSave(review.id)}>
                      Сохранить
                    </button>
                  </div>
                ) : (
                  <div>
                    <h3 className="review__title">{review.book_title}</h3>
                    <h4 className="review__author">{review.book_author}</h4>
                    <p className="review__genre">{review.genre}</p>
                    <p className="review__content">
                      {review.content.length > 100
                        ? `${review.content.slice(0, 100)}...`
                        : review.content}
                    </p>
                    <p>Рейтинг: ★{review.rating}</p>
                    <button onClick={() => handleEdit(review)}>
                      Редактировать
                    </button>
                    <button onClick={() => handleDelete(review.id)}>
                      Удалить
                    </button>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </main>
  );
};

export default MyReviews;
