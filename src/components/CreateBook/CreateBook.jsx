import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

import "./style.css";

const genres = [
  { value: "classic", label: "Классическая литература" },
  { value: "science", label: "Научная литература" },
  { value: "psychology", label: "Психология" },
  { value: "novella", label: "Новеллы" },
  { value: "fantasy", label: "Фэнтези" },
  { value: "detective", label: "Детектив" },
  { value: "science-fiction", label: "Научная фантастика" },
  { value: "horror", label: "Ужасы" },
  { value: "thriller", label: "Триллер" },
  { value: "mystery", label: "Мистика" },
  { value: "historical", label: "Историческая литература" },
  { value: "romance", label: "Роман" },
  { value: "poetry", label: "Поэзия" },
  { value: "poem", label: "Поэма" },
  { value: "drama", label: "Драма" },
  { value: "adventure", label: "Приключения" },
  { value: "biography", label: "Биографии и мемуары" },
  { value: "self-help", label: "Саморазвитие" },
  { value: "business", label: "Бизнес-литература" },
  { value: "humor", label: "Юмор" },
  { value: "childrens", label: "Детская литература" },
  { value: "philosophy", label: "Философия" },
  { value: "graphic-novel", label: "Графические романы" },
];

const CreateBook = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { bookTitle, bookAuthor } = location.state || {};

  const [title, setTitle] = useState(bookTitle || "");
  const [author, setAuthor] = useState(bookAuthor || "");
  const [genre, setGenre] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [bookId, setBookId] = useState(null);
  const [image, setImage] = useState(null);

  const token = sessionStorage.getItem("token");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!token) {
      navigate("/login");
      return;
    }

    if (!genre) {
      setError("Выберите жанр книги.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post("http://127.0.0.1:8000/books", {
        title,
        author,
        genre,
      });

      const newBookId = response.data.id;
      setBookId(newBookId);

      console.log("Книга успешно добавлена!");
      alert("Книга создана! Теперь можно загрузить обложку.");
    } catch (err) {
      console.error("Ошибка:", err);
      setError("Ошибка при создании книги, попробуйте снова.");
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (e) => {
    e.preventDefault();
    if (!image || !bookId) return;

    const formData = new FormData();
    formData.append("file", image);

    try {
      await axios.post(
        `http://127.0.0.1:8000/books/upload-book-image/${bookId}`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      console.log("Изображение загружено!");
      alert(
        "Изображение загружено! Вы будете перенаправлены на создание отзыва."
      );

      navigate("/create-review", {
        state: { bookTitle: title, bookAuthor: author },
      });
    } catch (err) {
      console.error("Ошибка загрузки изображения:", err);
      setError("Ошибка при загрузке изображения, попробуйте снова.");
    }
  };

  return (
    <main className="section">
      <div className="container">
        <h1 className="title-1">Добавить книгу</h1>

        {!bookId ? (
          <form className="review-form" onSubmit={handleSubmit}>
            <label>
              Название книги:
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </label>

            <label>
              Автор книги:
              <input
                type="text"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                required
              />
            </label>

            <label>
              Жанр книги:
              <p></p>
              <select
                className="genre-select"
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                required
              >
                <option value="">Выберите жанр</option>
                {genres.map((g) => (
                  <option key={g.value} value={g.value}>
                    {g.label}
                  </option>
                ))}
              </select>
            </label>

            <button type="submit" disabled={loading}>
              {loading ? "Создание..." : "Добавить книгу"}
            </button>
          </form>
        ) : (
          <form className="review-form" onSubmit={handleImageUpload}>
            <label>
              Загрузите изображение книги:
              <input
                className="review-form__input"
                type="file"
                accept="image/*"
                onChange={(e) => setImage(e.target.files[0])}
                required
              />
            </label>

            <button type="submit" disabled={!image}>
              Загрузить изображение
            </button>

            <button
              type="button"
              onClick={() =>
                navigate("/create-review", {
                  state: { bookTitle: title, bookAuthor: author },
                })
              }
            >
              Пропустить
            </button>
          </form>
        )}

        {error && <p className="error-message">{error}</p>}
      </div>
    </main>
  );
};

export default CreateBook;
