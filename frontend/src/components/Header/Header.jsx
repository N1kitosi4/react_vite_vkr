import { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";
import "./style.css";

const genres = [
  { value: "", label: "Все жанры" },
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

const Header = ({ onSearch }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("");

  useEffect(() => {
    const timeout = setTimeout(() => {
      onSearch(searchQuery, selectedGenre);
    }, 500);

    return () => clearTimeout(timeout);
  }, [searchQuery, selectedGenre, onSearch]);

  return (
    <header className="header">
      <div className="header__wrapper">
        <h1 className="header__title">
          <strong>
            Добро пожаловать в <em>Book Reviews</em>
          </strong>
          <br />
          Читайте, делитесь мнениями и находите лучшие книги!
        </h1>
        <div className="header__text">
          <p>
            Оставляйте отзывы и находите лучшие книги по рекомендациям других
            пользователей.
          </p>
        </div>
        <div className="container search-sort-container">
          <input
            type="text"
            className="search-input"
            placeholder="Поиск по названию или автору..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <select
            className="genre-select"
            value={selectedGenre}
            onChange={(e) => setSelectedGenre(e.target.value)}
          >
            {genres.map((g) => (
              <option key={g.value} value={g.value}>
                {g.label}
              </option>
            ))}
          </select>
        </div>
        <NavLink to="/create-review">
          <button className="btn">Создать свой отзыв</button>
        </NavLink>
      </div>
    </header>
  );
};

export default Header;
