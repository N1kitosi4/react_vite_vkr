import { useEffect, useState } from "react";
import axios from "axios";
import Header from "../components/Header/Header";
import HomeReview from "../components/HomeReview/HomeReview";

const Home = () => {
  const [reviews, setReviews] = useState([]);
  const [filteredReviews, setFilteredReviews] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalReviews, setTotalReviews] = useState(0);
  const [sortBy, setSortBy] = useState("date");
  const [sortDirection, setSortDirection] = useState("desc");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("");

  const API_URL = import.meta.env.VITE_API_URL;

  const reviewsPerPage = 9;

  const fetchAllReviews = async (sortOption, direction, query, genre) => {
    try {
      const params = new URLSearchParams({
        limit: 1000,
        sort: sortOption,
        direction,
        query,
        genre,
      });

      const response = await axios.get(
        `${API_URL}/reviews/search_reviews?${params.toString()}`
      );
      console.log(`${API_URL}/reviews/search_reviews?${params.toString()}`)
      if (response.status === 200) {
        const allReviews = response.data.reviews;
        setReviews(allReviews);
        setFilteredReviews(allReviews);
        setTotalReviews(allReviews.length);
      }
    } catch (error) {
      console.error("Ошибка загрузки отзывов:", error);
      setReviews([]);
      setFilteredReviews([]);
    }
  };

  useEffect(() => {
    fetchAllReviews(sortBy, sortDirection, searchQuery, selectedGenre);
  }, [sortBy, sortDirection, searchQuery, selectedGenre]);

  useEffect(() => {
    let filtered = reviews;

    if (searchQuery) {
      filtered = filtered.filter(
        (review) =>
          (review.book_title &&
            review.book_title
              .toLowerCase()
              .includes(searchQuery.toLowerCase())) ||
          (review.book_author &&
            review.book_author
              .toLowerCase()
              .includes(searchQuery.toLowerCase()))
      );
    }

    if (selectedGenre) {
      filtered = filtered.filter((review) => review.genre === selectedGenre);
    }

    if (sortBy === "date") {
      filtered = filtered.sort((a, b) =>
        sortDirection === "desc"
          ? new Date(b.created_at) - new Date(a.created_at)
          : new Date(a.created_at) - new Date(b.created_at)
      );
    } else if (sortBy === "popularity") {
      filtered = filtered.sort((a, b) =>
        sortDirection === "desc" ? b.popularity - a.popularity : a.popularity - b.popularity
      );
    } else if (sortBy === "rating") {
      filtered = filtered.sort((a, b) =>
        sortDirection === "desc"
          ? b.average_review_rating - a.average_review_rating
          : a.average_review_rating - b.average_review_rating
      );
    }

    setFilteredReviews(filtered);
    setTotalReviews(filtered.length);
  }, [reviews, searchQuery, selectedGenre, sortBy, sortDirection]);

  useEffect(() => {
    if (searchQuery || selectedGenre) {
      setCurrentPage(1);
    }
  }, [searchQuery, selectedGenre]);

  const currentReviews = filteredReviews.slice(
    (currentPage - 1) * reviewsPerPage,
    currentPage * reviewsPerPage
  );

  const totalPages = Math.ceil(totalReviews / reviewsPerPage);

  const handleSortChange = (sortOption) => {
    setSortBy(sortOption);
  };

  const handleDirectionChange = (direction) => {
    setSortDirection(direction);
  };

  const handleSearch = (query, genre) => {
    setSearchQuery(query);
    setSelectedGenre(genre);
  };

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [currentPage]);

  return (
    <>
      <Header onSearch={handleSearch} />
      <main className="section">
        <div className="container">
          <h2 className="title-1">Отзывы</h2>

          <div className="sort-dropdown">
            <label htmlFor="sort">Сортировать по:</label>
            <div className="sort-dropdown__items">
              <select
                id="sort"
                value={sortBy}
                onChange={(e) => handleSortChange(e.target.value)}
              >
                <option value="date">По дате</option>
                <option value="popularity">По популярности (отзыва)</option>
                <option value="rating">По рейтингу (книги)</option>
              </select>

              <select
                value={sortDirection}
                onChange={(e) => handleDirectionChange(e.target.value)}
              >
                <option value="desc">По убыванию</option>
                <option value="asc">По возрастанию</option>
              </select>
            </div>
          </div>

          <ul className="reviews">
            {currentReviews.length > 0 ? (
              currentReviews.map((review) => (
                <HomeReview key={review.id} review={review} />
              ))
            ) : (
              <h2 className="title-1">Отзывы не найдены.</h2>
            )}
          </ul>

          {totalReviews > reviewsPerPage && (
            <div className="pagination">
              <button
                onClick={() => setCurrentPage((prevPage) => Math.max(prevPage - 1, 1))}
                disabled={currentPage === 1}
              >
                Назад
              </button>

              <span>
                {currentPage} из {totalPages}
              </span>

              <button
                onClick={() => setCurrentPage((prevPage) => Math.min(prevPage + 1, totalPages))}
                disabled={currentPage === totalPages}
              >
                Вперед
              </button>
            </div>
          )}
        </div>
      </main>
    </>
  );
};

export default Home;
