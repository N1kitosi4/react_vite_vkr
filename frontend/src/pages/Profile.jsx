import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import axios from "axios";
import book from "./../img/book.svg";
import vk from "./../img/icons/vk.svg";
import ok from "./../img/icons/ok.svg";
import telegram from "./../img/icons/telegram.svg";

import { Swiper, SwiperSlide } from "swiper/react";
import { EffectCoverflow } from "swiper/modules";
import "swiper/css";
import "swiper/css/effect-coverflow";

import "./../styles/profile.css";

const Profile = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [profileStats, setProfileStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [avatar, setAvatar] = useState(null);
  const token = sessionStorage.getItem("token");

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    const fetchProfile = async () => {
      if (!token) {
        navigate("/login");
        return;
      }

      try {
        const { data: currentUser } = await axios.get(
          `${API_URL}/users/me`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        setUser(currentUser);

        const { data: reviewsData } = await axios.get(
          `${API_URL}/reviews/my_reviews`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (Array.isArray(reviewsData)) {
          const formattedReviews = reviewsData.map((review) => ({
            ...review,
            formattedDate: new Date(review.created_at).toLocaleDateString(
              "ru-RU",
              {
                day: "numeric",
                month: "long",
                year: "numeric",
              }
            ),
          }));
          setReviews(formattedReviews);
        } else {
          setReviews([]);
        }

        const { data: stats } = await axios.get(`${API_URL}/reviews/profile_stats`, {
            headers: {
              Authorization: `Bearer ${token}`,
              Accept: "application/json",
            },
          });
          setProfileStats(stats);

      } catch (err) {
        setError(err);
        console.error("Ошибка загрузки профиля:", err);
        sessionStorage.removeItem("token");
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [navigate, token, API_URL]);

  const handleAvatarChange = (event) => {
    setAvatar(event.target.files[0]);
  };

  const handleAvatarUpload = async () => {
    if (!avatar) {
      return;
    }

    const formData = new FormData();
    formData.append("file", avatar);

    try {
      const response = await axios.post(
        `${API_URL}/users/me/avatar`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setUser((prev) => ({ ...prev, avatar: response.data.avatar_url }));
    } catch (error) {
      console.error("Ошибка загрузки аватара:", error);
    }
  };


  if (loading) return <p>Загрузка...</p>;
  if (error) return <p className="error-message">{error.message}</p>;

  return (
    <main className="section">
      <div className="container">
        <h1 className="title-1">Профиль пользователя</h1>
        <div className="profile-info">
          <div className="profile-info__avatar">
            <img
              src={user.avatar ? `${API_URL}${user.avatar}` : book}
              alt="User Avatar"
              className="profile-info__avatar-img"
            />
          </div>
          <div className="profile-info__details">
            <h2 className="profile-info__name">{user.username}</h2>
            <p className="profile-info__job">Читатель и критик</p>
            {profileStats ? (
              <div className="user-stats">
                <p>Оценено отзывов: {profileStats.rated_reviews_count}</p>
                <p>Сделано отзывов: {profileStats.user_reviews_count}</p>
                <p>Средняя оценка оцененных отзывов: {profileStats.rated_reviews_avg_rating || 0}</p>
                <p>Средняя оценка книг: {profileStats.user_reviews_avg_rating || 0}</p>
              </div>
            ) : (
              <p>Загрузка статистики...</p>
            )}
            
            <div className="profile-info__socials">
              <a href="https://vk.com" className="social__item">
                <img src={vk} alt="VK" />
              </a>
              <a href="https://instagram.com" className="social__item">
                <img src={telegram} alt="Telegram" />
              </a>
              <a href="https://twitter.com" className="social__item">
                <img src={ok} alt="Odnokassniki" />
              </a>
            </div>

            {/* Форма загрузки нового аватара */}
            <div className="profile-avatar-upload">
              <input
                className="input-profile"
                type="file"
                onChange={handleAvatarChange}
                accept="image/*"
              />
              <button className="btn-profile" onClick={handleAvatarUpload}>
                Обновить аватар
              </button>
            </div>
          </div>
        </div>

        <h2 className="title-2__profile">Мои отзывы</h2>

        {reviews.length > 0 ? (
          <Swiper
            modules={[EffectCoverflow]}
            grabCursor={true}
            initialSlide={0}
            centeredSlides={true}
            slidesPerView="auto"
            speed={800}
            slideToClickedSlide={true}
            loop={true}
            loopedslides={reviews.length}
            effect="coverflow"
            coverflowEffect={{
              rotate: 30,
              stretch: 0,
              depth: 100,
              modifier: 1,
              slideShadows: false,
            }}
            breakpoints={{
              320: { spaceBetween: 40 },
              430: { spaceBetween: 50 },
              580: { spaceBetween: 70 },
              650: { spaceBetween: 30 },
            }}
            className="reviews-slider"
          >
            {reviews.map((review) => (
              <SwiperSlide
                key={review.id}
                style={{
                  backgroundImage: `url(${API_URL}${review.book_img})`,
                  backgroundRepeat: "no-repeat",
                  backgroundPosition: "center",
                  backgroundSize: "cover",
                }}
              >
                <NavLink to={`/review/${review.id}`} className="review-card">
                  <div className="title">
                    <h1>{review.book_title}</h1>
                  </div>
                  <div className="content">
                    <div className="score">{review.rating}</div>
                    <div className="text">
                      <h2>{review.book_author}</h2>
                      <p>
                        {review.content.length > 100 ? (
                          <>
                            {review.content.slice(0, 100)}...
                            <span className="review__content_ref">
                              Читать далее
                            </span>
                          </>
                        ) : (
                          review.content
                        )}
                      </p>
                    </div>
                    <div className="genre">
                      <span>{review.genre}</span>
                    </div>
                    <p className="review-card__date">
                      Дата отзыва: {review.formattedDate.toLocaleString()}
                    </p>
                  </div>
                </NavLink>
              </SwiperSlide>
            ))}
          </Swiper>
        ) : (
          <h1 className="title-1">Вы еще не оставили отзывов.</h1>
        )}
      </div>
    </main>
  );
};

export default Profile;
