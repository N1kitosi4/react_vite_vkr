import { useEffect, useState } from "react";
import axios from "axios";
import { NavLink, useNavigate } from "react-router-dom";
import defaultImg from "./../img/reviews/default_img.jpg";

const Recommendations = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const navigate = useNavigate();
  const token = sessionStorage.getItem("token");

  useEffect(() => {
    const fetchReviews = async () => {
      if (!token) {
        navigate("/login");
        return;
      }

      try {
        const { data } = await axios.get("http://127.0.0.1:8000/recs", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setReviews(data);
        console.log(data);
      } catch (err) {
        console.error("Ошибка загрузки отзывов:", err);
        setError("Ошибка загрузки отзывов");
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, [navigate, token]);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p className="error-message">{error}</p>;

  return (
    <main className="section">
      <div className="container">
        <h1 className="title-1">Мои рекомендации</h1>
        {console.log(reviews)}

        {/*, , , content, rating, created_at, username, */}

        {reviews.length < 5 ? (
          <h1 className="title-1">
            Напишите отзывы, чтоб понять ваши предпочтения.
          </h1>
        ) : (
          <ul className="reviews">
            {reviews.map((review) => (
              <li key={review.id} className="review">
                {/*<NavLink to={`/review/${review.id}`}>*/}
                <div>
                  <div className="review__img">
                    <img
                      src={
                        review.img
                          ? `http://127.0.0.1:8000${review.img}`
                          : defaultImg
                      }
                      alt="Book Cover"
                    />
                  </div>
                  <h3 className="review__title">{review.title}</h3>
                  <h4 className="review__author">{review.author}</h4>
                  <p className="review__genre">{review.genre}</p>
                </div>

                {/* </NavLink>*/}
              </li>
            ))}
          </ul>
        )}
      </div>
    </main>
  );
};

export default Recommendations;
